#!/usr/bin/env python3
"""First voiceover spike: clone the English dub cast with OmniVoice.

The reference clips are the packed <=10 s files in
``character_voices_eng/<Character>/<tone>/10s combined clips/``. Their
transcripts come straight from ``combined_clips.csv`` (``text`` column), so
Whisper is never used: every request passes ``ref_text`` explicitly.

Each probe line is rendered twice, once from the combined clip and once from a
single clean clip, so the two reference strategies can be compared by ear. A
few extra variants check the inline paralinguistic tags (``[laughter]``,
``[question-en]``, ...).

By default the script talks to the running low-VRAM demo server
(http://127.0.0.1:8001) through its Gradio API. Pass ``--local`` to load the
model in-process instead (needed for the full chapter, where a cached
``VoiceClonePrompt`` per character/emotion avoids re-encoding the reference).

Run:
    ~/OmniVoice/.venv/bin/python scripts/voice/spike.py
    ~/OmniVoice/.venv/bin/python scripts/voice/spike.py --local
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

DATASET_DEFAULT = Path.home() / "projects/mushokuTensei/character_voices_eng"
WORK_DEFAULT = Path.home() / "projects/voiceClone"
MODEL = "k2-fsa/OmniVoice"
SERVER_DEFAULT = "http://127.0.0.1:8001"
SAMPLE_RATE = 24000

# Probe lines taken from Volume 16, chapter 2 ("Guardian Beast").
ITEMS = [
    {
        "id": "narr_rudeus",
        "label": "Narration (Rudeus)",
        "voice": "Rudeus Greyrat",
        "tone": "serious",
        "text": "But first, I had another objective to complete. Namely, the very reason "
        "why I'd agreed to work under Orsted to begin with, so I could protect my family.",
        "tags": [],
        "speed": 0.97,
    },
    {
        "id": "rudeus_speech",
        "label": "Rudeus - neutral announcement",
        "voice": "Rudeus Greyrat",
        "tone": "neutral",
        "text": "In a moment, I will be summoning the Guardian Beast that will serve our "
        "family. Feel free to clap.",
        "tags": [],
        "speed": 1.0,
    },
    {
        "id": "sylphiette_worried",
        "label": "Sylphiette - worried question",
        "voice": "Sylphiette Greyrat",
        "tone": "worried",
        "text": "Are you sure this will be okay? That this thing won't eat us all while "
        "you're gone?",
        "tags": [],
        "speed": 1.0,
    },
    {
        "id": "almanfi_angry",
        "label": "Arumanfi - angry demand",
        "voice": "Almanfi",
        "tone": "serious",
        "text": "What's the meaning of this?!",
        "tags": [],
        "speed": 1.05,
    },
    {
        "id": "eris_excited",
        "label": "Eris - excited",
        "voice": "Eris Boreas Greyrat",
        "tone": "excited",
        "text": "Sounds good to me!",
        "tags": [],
        "speed": 1.03,
    },
    {
        "id": "aisha_excited",
        "label": "Aisha - delighted",
        "voice": "Aisha Greyrat",
        "tone": "excited",
        "text": "It's adorable!",
        "tags": [],
        "speed": 1.02,
    },
]

# Extra renders that only exercise the inline control tags.
TAG_VARIANTS = [
    {
        "id": "sylphiette_question_tag",
        "base": "sylphiette_worried",
        "variant": "combined 10s + tag",
        "group": "Sylphiette (tags)",
        "tags": ["question-en"],
    },
    {
        "id": "almanfi_dissatisfaction_tag",
        "base": "almanfi_angry",
        "variant": "combined 10s + tag",
        "group": "Arumanfi (tags)",
        "tags": ["dissatisfaction-hnn"],
    },
    {
        "id": "aisha_laughter_tag",
        "base": "aisha_excited",
        "variant": "combined 10s + tag",
        "group": "Aisha (tags)",
        "tags": ["laughter"],
    },
    {
        "id": "rudeus_laughter_tag",
        "base": "rudeus_speech",
        "variant": "combined 10s + tag",
        "group": "Rudeus (tags)",
        "tags": ["laughter"],
    },
]


def clean(text: str) -> str:
    """Collapse the ASS line breaks and stray whitespace in subtitle text."""
    text = text.replace("\\N", " ").replace("\\n", " ")
    text = re.sub(r"\s+/\s+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pick_combined(rows: list[dict], character: str, tone: str) -> dict:
    """Longest packed clip for this character/tone, preferring real packings."""
    candidates = [
        row
        for row in rows
        if row["character"] == character
        and row["tone"] == tone
        and int(row["source_count"]) >= 2
        and row["text_is_transcript"] == "true"
        and row["text"].strip()
    ]
    if not candidates:
        candidates = [
            row
            for row in rows
            if row["character"] == character and row["tone"] == tone and row["text"].strip()
        ]
    if not candidates:
        raise SystemExit(f"no combined clip with transcript for {character}/{tone}")
    candidates.sort(key=lambda row: (-float(row["duration_sec"]), row["file"]))
    return candidates[0]


def pick_single(rows: list[dict], character: str, tone: str) -> dict:
    """Longest plain-speech single clip, 3.5-9.5 s, for the second strategy."""
    candidates = [
        row
        for row in rows
        if row["character"] == character
        and row["tone"] == tone
        and row["delivery"] == ""
        and 3.5 <= float(row["duration_sec"]) <= 9.5
        and row["text"].strip()
    ]
    if not candidates:
        # Eris/excited, for example, has no clip longer than 3 s.
        candidates = [
            row
            for row in rows
            if row["character"] == character
            and row["tone"] == tone
            and row["delivery"] == ""
            and float(row["duration_sec"]) >= 1.5
            and row["text"].strip()
        ]
    if not candidates:
        raise SystemExit(f"no single clip for {character}/{tone}")
    candidates.sort(key=lambda row: (-float(row["duration_sec"]), row["file"]))
    return candidates[0]


def build_plan(combined_rows: list[dict], single_rows: list[dict]) -> list[dict]:
    plan: list[dict] = []
    for item in ITEMS:
        combined = pick_combined(combined_rows, item["voice"], item["tone"])
        single = pick_single(single_rows, item["voice"], item["tone"])
        plan.append({**item, "variant": "combined 10s", "ref": combined, "group": item["label"]})
        plan.append({**item, "variant": "single clip", "ref": single, "group": item["label"]})

    by_id = {item["id"]: item for item in ITEMS}
    for variant in TAG_VARIANTS:
        base = by_id[variant["base"]]
        combined = pick_combined(combined_rows, base["voice"], base["tone"])
        plan.append(
            {
                **base,
                "id": variant["id"],
                "variant": variant["variant"],
                "group": variant["group"],
                "tags": variant["tags"],
                "ref": combined,
            }
        )
    return plan


def tts_text_for(entry: dict) -> str:
    prefix = " ".join(f"[{tag}]" for tag in entry["tags"])
    return f"{prefix} {entry['text']}".strip()


def synth_server(server: str, entry: dict, ref_path: Path, ref_text: str) -> tuple[Path, float]:
    from gradio_client import Client, handle_file

    client = Client(server, verbose=False)
    began = time.time()
    audio_path, status = client.predict(
        text=tts_text_for(entry),
        lang="English",
        ref_aud=handle_file(str(ref_path)),
        ref_text=ref_text,
        instruct="",
        ns=32,
        gs=2.0,
        dn=True,
        sp=float(entry.get("speed", 1.0)),
        du=None,
        pp=True,
        po=True,
        api_name="/_clone_fn",
    )
    if audio_path is None:
        raise SystemExit(f"server returned no audio: {status}")
    return Path(audio_path), time.time() - began


def synth_local(model, prompt, entry: dict) -> tuple[Path, float]:
    import soundfile as sf
    import torch

    torch.manual_seed(1234)
    began = time.time()
    audio = model.generate(
        text=tts_text_for(entry),
        voice_clone_prompt=prompt,
        language="English",
        num_step=32,
        speed=float(entry.get("speed", 1.0)),
    )
    out = Path("/tmp") / "omnivoice-spike.wav"
    sf.write(str(out), audio[0], SAMPLE_RATE)
    return out, time.time() - began


def prompt_for(model, ref_path: Path, ref_text: str, cache_dir: Path):
    from omnivoice import VoiceClonePrompt

    key = hashlib.sha1(f"{ref_path}|{ref_text}".encode("utf-8")).hexdigest()[:12]
    cache = cache_dir / f"{key}.pt"
    if cache.exists():
        return VoiceClonePrompt.load(str(cache)), cache
    prompt = model.create_voice_clone_prompt(
        ref_audio=str(ref_path),
        ref_text=ref_text,
    )
    prompt.save(str(cache))
    return prompt, cache


def render_html(results: list[dict], out_dir: Path) -> Path:
    groups: dict[str, list[dict]] = {}
    for item in results:
        groups.setdefault(item["group"], []).append(item)

    parts = [
        "<!doctype html><meta charset='utf-8'>",
        "<title>OmniVoice spike - Mushoku Tensei vol.16 ch.2</title>",
        "<style>",
        "body{font:16px/1.5 system-ui,sans-serif;max-width:920px;margin:40px auto;padding:0 20px;background:#14130f;color:#e8e4da}",
        "h1{font-size:26px;margin-bottom:4px}",
        "h2{margin-top:34px;border-bottom:1px solid #3a382f;padding-bottom:6px;font-size:17px}",
        ".row{display:grid;grid-template-columns:210px 1fr;gap:16px;align-items:start;padding:12px 0;border-bottom:1px solid #262520}",
        ".tag{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:#b9a86a}",
        ".meta{font-size:12px;color:#8d887a;margin-top:3px}",
        ".line{font-size:14px;color:#cfc9ba;margin-bottom:6px}",
        "audio{width:100%}",
        "</style>",
        "<h1>Voice spike — vol. 16, ch. 2</h1>",
        "<p style='color:#8d887a'>English dub references. Reference text comes from "
        "<code>combined_clips.csv</code>; Whisper is never used.</p>",
    ]
    for group, items in groups.items():
        parts.append(f"<h2>{html.escape(group)}</h2>")
        for item in items:
            parts.append(
                "<div class='row'>"
                f"<div><div class='tag'>{html.escape(item['variant'])}</div>"
                f"<div class='meta'>{item['duration']:.1f}s out · {item['ref_duration']:.1f}s ref"
                f"<br>{html.escape(item['ref_name'])}</div></div>"
                f"<div><div class='line'>{html.escape(item['line'])}</div>"
                f"<audio controls preload='none' src='{html.escape(item['mp3'])}'></audio></div>"
                "</div>"
            )
    path = out_dir / "index.html"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    parser.add_argument("--work", type=Path, default=WORK_DEFAULT)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--server", default=SERVER_DEFAULT)
    parser.add_argument("--local", action="store_true", help="load the model in-process")
    args = parser.parse_args()

    out_dir = args.out or (args.work / "out" / "spike")
    refs_dir = args.work / "refs"
    for path in (out_dir / "audio", out_dir / "mp3", refs_dir):
        path.mkdir(parents=True, exist_ok=True)

    combined_rows = load_rows(args.dataset / "combined_clips.csv")
    single_rows = load_rows(args.dataset / "clips.csv")
    plan = build_plan(combined_rows, single_rows)

    model = None
    if args.local:
        import torch
        from omnivoice import OmniVoice

        began = time.time()
        model = OmniVoice.from_pretrained(
            MODEL, device_map="cuda:0", dtype=torch.float16, load_asr=False
        )
        model.audio_tokenizer.to("cpu")
        print(
            f"model ready in {time.time() - began:.1f}s, "
            f"VRAM {torch.cuda.memory_allocated() / 1024**3:.2f} GiB",
            flush=True,
        )

    results: list[dict] = []
    started = time.time()
    for index, entry in enumerate(plan):
        ref_path = args.dataset / entry["ref"]["file"]
        ref_text = clean(entry["ref"]["text"])

        if args.local:
            prompt, cache = prompt_for(model, ref_path, ref_text, refs_dir)
            produced, elapsed = synth_local(model, prompt, entry)
            prompt_label = str(cache)
        else:
            produced, elapsed = synth_server(args.server, entry, ref_path, ref_text)
            prompt_label = ""

        wav_path = out_dir / "audio" / f"{entry['id']}__{entry['variant'].split()[0]}.wav"
        mp3_path = out_dir / "mp3" / f"{wav_path.stem}.mp3"
        shutil.copyfile(produced, wav_path)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path),
             "-codec:a", "libmp3lame", "-b:a", "128k", str(mp3_path)],
            check=True,
        )
        try:
            import soundfile as sf

            duration = sf.info(str(wav_path)).duration
        except Exception:
            duration = 0.0

        print(
            f"{index + 1:2d}/{len(plan)}  {entry['id']:30} {entry['variant']:18} "
            f"out {duration:5.2f}s  took {elapsed:5.1f}s  ref {entry['ref']['duration_sec']}s",
            flush=True,
        )
        results.append(
            {
                "id": entry["id"],
                "group": entry["group"],
                "variant": entry["variant"],
                "line": tts_text_for(entry),
                "duration": duration,
                "ref": entry["ref"]["file"],
                "ref_name": Path(entry["ref"]["file"]).name,
                "ref_text": ref_text,
                "ref_duration": float(entry["ref"]["duration_sec"]),
                "mp3": f"mp3/{mp3_path.name}",
                "prompt": prompt_label,
            }
        )

    report = out_dir / "spike.json"
    report.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    qa = render_html(results, out_dir)
    print(f"\nwrote {report}\nwrote {qa}")
    print(f"total {time.time() - started:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
