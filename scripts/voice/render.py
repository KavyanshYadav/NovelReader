#!/usr/bin/env python3
"""Render a chapter voiceover from its segment plan.

Two stages, both resumable:

  render    one WAV per segment, via the running OmniVoice demo server
  assemble  normalise, concatenate with pauses, encode MP3, write timings

The reference clip for every (voice, tone) pair is the longest packed <=10 s
clip that has a real transcript. Its transcript is left to the server, which
runs Whisper on the *processed* clip (``--ref-text asr``, the default). A
transcript from the CSV describes the untrimmed audio, so the words left over
after silence removal get voiced before the target line. ``--ref-text csv``
restores that older behaviour for comparison.

Run:
    python3 scripts/voice/render.py render --limit 3
    python3 scripts/voice/render.py render
    python3 scripts/voice/render.py assemble
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
DATASET_DEFAULT = Path.home() / "projects/mushokuTensei/character_voices_eng"
WORK_DEFAULT = Path.home() / "projects/voiceClone"
SERVER_DEFAULT = "http://127.0.0.1:8001"
SR = 24000

SEG_GAP = 0.18          # between segments inside one block
BLOCK_GAP = 0.45        # between blocks
SCENE_GAP = 1.00        # between scenes
LEAD_IN = 0.30
TAIL = 0.80

TARGET_RMS_DB = -20.0
PEAK_CEILING = 0.85


def clean(text: str) -> str:
    import re

    text = text.replace("\\N", " ").replace("\\n", " ")
    text = re.sub(r"\s+/\s+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pick_ref(rows: list[dict], character: str, tone: str, rank: int = 0) -> dict:
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
            if row["character"] == character
            and row["tone"] == tone
            and row["text"].strip()
        ]
    if not candidates:
        raise SystemExit(f"no usable reference for {character}/{tone}")
    candidates.sort(key=lambda row: (-float(row["duration_sec"]), row["file"]))
    return candidates[rank % len(candidates)]


def build_refs(
    segments: list[dict], dataset: Path, ranks: dict[str, int] | None = None
) -> dict[tuple[str, str], dict]:
    rows = load_rows(dataset / "combined_clips.csv")
    ranks = ranks or {}
    refs: dict[tuple[str, str], dict] = {}
    for segment in segments:
        key = (segment["voice"], segment["tone"])
        if key in refs:
            continue
        row = pick_ref(rows, *key, rank=ranks.get(key[0], 0))
        refs[key] = {
            "path": str(dataset / row["file"]),
            "file": row["file"],
            "text": clean(row["text"]),
            "duration": float(row["duration_sec"]),
            "source_count": int(row["source_count"]),
        }
    return refs


def connect(server: str):
    from gradio_client import Client

    return Client(server, verbose=False)


def synth(client, text: str, ref: dict, speed: float, ref_text: str | None = None) -> Path:
    from gradio_client import handle_file

    audio, status = client.predict(
        text=text,
        lang="English",
        ref_aud=handle_file(ref["path"]),
        ref_text=ref_text,
        instruct="",
        ns=32,
        gs=2.0,
        dn=True,
        sp=float(speed),
        du=None,
        pp=True,
        po=True,
        api_name="/_clone_fn",
    )
    if not audio:
        raise RuntimeError(f"no audio returned ({status})")
    return Path(audio)


def cmd_render(args) -> int:
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    segments = plan["segments"]
    ranks: dict[str, int] = {}
    for item in filter(None, (part.strip() for part in args.ref_rank.split(","))):
        voice, _, value = item.rpartition("=")
        ranks[voice.strip()] = int(value)
    refs = build_refs(segments, args.dataset, ranks)
    print(f"reference text: {args.ref_text}", flush=True)
    print("references:", flush=True)
    for (voice, tone), ref in refs.items():
        print(
            f"  {voice:22} {tone:12} {ref['duration']:5.2f}s src={ref['source_count']} "
            f"{ref['file'].split('/')[-1]}",
            flush=True,
        )
    wav_dir = args.work / "out" / f"vol{plan['volume']}" / plan["chapter"] / "wav"
    wav_dir.mkdir(parents=True, exist_ok=True)
    (args.work / "out" / f"vol{plan['volume']}" / plan["chapter"] / "refs.json").write_text(
        json.dumps({f"{k[0]} | {k[1]}": v for k, v in refs.items()}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    todo = segments
    if args.voice:
        todo = [s for s in todo if s["voice"] == args.voice]
    if args.only:
        wanted = set(args.only.split(","))
        todo = [s for s in segments if s["id"] in wanted]
    if args.limit:
        todo = todo[: args.limit]

    total = len(todo)
    done = 0
    began = time.time()
    client = connect(args.server)
    for index, segment in enumerate(todo):
        out = wav_dir / f"{segment['id']}.wav"
        if out.exists() and out.stat().st_size > 1000 and not args.force:
            done += 1
            continue
        ref = refs[(segment["voice"], segment["tone"])]
        error = None
        for attempt in range(3):
            try:
                ref_text = None if args.ref_text == "asr" else ref["text"]
                produced = synth(client, segment["text"], ref, segment["speed"], ref_text)
                shutil.copyfile(produced, out)
                error = None
                break
            except Exception as exc:  # noqa: BLE001 - server hiccups are expected
                error = exc
                time.sleep(2 + attempt * 3)
                try:
                    client = connect(args.server)
                except Exception:
                    pass
        if error:
            print(f"FAIL {segment['id']}: {error}", flush=True)
            continue
        done += 1
        elapsed = time.time() - began
        rate = (index + 1) / elapsed if elapsed else 0
        left = (total - index - 1) / rate / 60 if rate else 0
        print(
            f"{index + 1:3d}/{total}  {segment['id']:22} {segment['voice'][:20]:20} "
            f"{segment['tone']:12} {segment['speed']:.2f}  {elapsed / 60:5.1f}m elapsed, "
            f"~{left:4.1f}m left",
            flush=True,
        )
    print(f"done {done}/{total}")
    return 0


def normalise(audio: np.ndarray) -> np.ndarray:
    """RMS-match a segment and keep peaks under the ceiling."""
    if audio.size == 0:
        return audio
    frame = max(1, int(SR * 0.025))
    usable = audio[: audio.size - audio.size % frame].reshape(-1, frame)
    rms = np.sqrt(np.mean(usable**2, axis=1))
    active = rms[rms > 10 ** (-50 / 20)]
    if active.size == 0:
        return audio
    level = float(np.sqrt(np.mean(active**2)))
    gain = 10 ** (TARGET_RMS_DB / 20) / max(level, 1e-6)
    peak = float(np.max(np.abs(audio))) * gain
    if peak > PEAK_CEILING:
        gain *= PEAK_CEILING / peak
    return audio * gain


def cmd_assemble(args) -> int:
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    segments = plan["segments"]
    base = args.work / "out" / f"vol{plan['volume']}" / plan["chapter"]
    wav_dir = base / "wav"

    missing = [s["id"] for s in segments if not (wav_dir / f"{s['id']}.wav").exists()]
    if missing:
        print(f"{len(missing)} segments still missing, first: {missing[:5]}")
        return 1

    cache: dict[str, np.ndarray] = {}
    for segment in segments:
        path = wav_dir / f"{segment['id']}.wav"
        audio, rate = sf.read(str(path), dtype="float32", always_2d=False)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        if rate != SR:
            raise SystemExit(f"{path} is {rate} Hz, expected {SR}")
        cache[segment["id"]] = normalise(audio)

    total = int((LEAD_IN + TAIL + len(segments) * (SEG_GAP + 12)) * SR) + 10
    track = np.zeros(total, dtype=np.float32)
    cursor = int(LEAD_IN * SR)

    timing_segments: list[dict] = []
    timing_blocks: list[dict] = []
    last_scene = None
    first_block = True

    for block in plan["blocks"]:
        if last_scene is not None and block["scene"] != last_scene:
            cursor += int(SCENE_GAP * SR)
        elif not first_block:
            cursor += int(BLOCK_GAP * SR)
        block_start = cursor

        for offset, seg_index in enumerate(block["segments"]):
            segment = segments[seg_index]
            audio = cache[segment["id"]]
            if offset:
                cursor += int(SEG_GAP * SR)
            seg_start = cursor
            end = cursor + audio.size
            if end > track.size:
                track = np.pad(track, (0, end - track.size + SR * 30))
            track[cursor:end] += audio
            cursor = end
            timing_segments.append(
                {
                    "id": segment["id"],
                    "blockId": segment["blockId"],
                    "speaker": segment["speaker"],
                    "role": segment["role"],
                    "tone": segment["tone"],
                    "text": segment["text"],
                    "start": round(seg_start / SR, 3),
                    "end": round(cursor / SR, 3),
                }
            )
        timing_blocks.append(
            {
                "id": block["id"],
                "scene": block["scene"],
                "type": block["type"],
                "speaker": block["speaker"],
                "start": round(block_start / SR, 3),
                "end": round(cursor / SR, 3),
            }
        )
        last_scene = block["scene"]
        first_block = False

    duration = (cursor + int(TAIL * SR)) / SR
    track = track[: cursor + int(TAIL * SR)]

    raw = base / "chapter.raw.wav"
    sf.write(str(raw), track, SR, subtype="PCM_16")

    final_wav = base / "chapter.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(raw),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", str(SR), "-ac", "1", str(final_wav),
        ],
        check=True,
    )
    mp3 = base / "chapter.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(final_wav),
            "-codec:a", "libmp3lame", "-b:a", "96k", "-ar", str(SR), "-ac", "1",
            "-metadata", f"title=Mushoku Tensei vol.{plan['volume']} {plan['title']}",
            str(mp3),
        ],
        check=True,
    )

    manifest = {
        "volume": plan["volume"],
        "chapter": plan["chapter"],
        "title": plan["title"],
        "duration": round(duration, 3),
        "sampleRate": SR,
        "file": "chapter.mp3",
        "scenes": [s["id"] for s in _scenes(plan)],
        "blocks": timing_blocks,
        "segments": timing_segments,
    }
    (base / "chapter.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    page = render_page(manifest, base)
    print(f"{duration / 60:.1f} min, {mp3.stat().st_size / 1024**2:.1f} MB -> {mp3}")
    print(f"timings -> {base / 'chapter.json'}")
    print(f"player  -> {page}")
    return 0


def _scenes(plan: dict):
    seen = []
    for block in plan["blocks"]:
        if not seen or seen[-1]["id"] != block["scene"]:
            seen.append({"id": block["scene"]})
    return seen


def render_page(manifest: dict, base: Path) -> Path:
    import html as h

    rows = []
    for block in manifest["blocks"]:
        segs = [s for s in manifest["segments"] if s["blockId"] == block["id"]]
        speaker = block["speaker"] or "Narration"
        tones = ", ".join(sorted({s["tone"] for s in segs}))
        text = " ".join(s["text"] for s in segs)
        rows.append(
            f"<li class='row' data-start='{block['start']}'>"
            f"<button class='seek'>{_clock(block['start'])}</button>"
            f"<div class='body'><div class='who'>{h.escape(speaker)}"
            f"<span class='tone'>{h.escape(tones)}</span></div>"
            f"<div class='text'>{h.escape(text)}</div></div></li>"
        )

    page = f"""<!doctype html>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Mushoku Tensei vol.{manifest['volume']} - {h.escape(manifest['title'])}</title>
<style>
:root{{color-scheme:dark}}
body{{margin:0;background:#14130f;color:#e8e4da;font:16px/1.55 system-ui,sans-serif}}
header{{position:sticky;top:0;z-index:2;background:#14130fee;backdrop-filter:blur(8px);border-bottom:1px solid #2e2c25;padding:14px 20px}}
h1{{font-size:17px;margin:0 0 2px;font-weight:600}}
.sub{{font-size:12px;color:#8d887a}}
audio{{width:100%;margin-top:10px}}
ol{{list-style:none;margin:0 auto;padding:0 20px 40vh;max-width:860px}}
.row{{display:grid;grid-template-columns:58px 1fr;gap:12px;padding:10px 0;border-bottom:1px solid #232219}}
.row.playing{{background:#1d1c15}}
.seek{{font:12px/1 ui-monospace,monospace;color:#b9a86a;background:none;border:1px solid #3a382f;border-radius:5px;height:24px;cursor:pointer}}
.seek:hover{{background:#2a2820}}
.who{{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#9d9682}}
.tone{{margin-left:8px;color:#6f6a5c;text-transform:none;letter-spacing:0}}
.text{{font-size:15px;color:#d6d0c2}}
</style>
<header>
  <h1>Vol. {manifest['volume']} — {h.escape(manifest['title'])}</h1>
  <div class='sub'>{manifest['duration'] / 60:.1f} min · {len(manifest['blocks'])} blocks · {len(manifest['segments'])} segments</div>
  <audio id='player' controls preload='metadata' src='{h.escape(manifest['file'])}'></audio>
</header>
<ol id='list'>{''.join(rows)}</ol>
<script>
const player = document.getElementById('player');
const rows = [...document.querySelectorAll('.row')];
let current = -1;
document.getElementById('list').addEventListener('click', e => {{
  const row = e.target.closest('.row');
  if (!row) return;
  player.currentTime = parseFloat(row.dataset.start);
  player.play();
}});
player.addEventListener('timeupdate', () => {{
  const t = player.currentTime;
  let index = -1;
  for (let i = 0; i < rows.length; i++) {{
    if (t >= parseFloat(rows[i].dataset.start)) index = i;
    else break;
  }}
  if (index !== current) {{
    if (current >= 0) rows[current].classList.remove('playing');
    current = index;
    if (index >= 0) {{
      rows[index].classList.add('playing');
      rows[index].scrollIntoView({{block: 'center', behavior: 'smooth'}});
    }}
  }}
}});
</script>
"""
    path = base / "index.html"
    path.write_text(page, encoding="utf-8")
    return path


def _clock(seconds: float) -> str:
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def cmd_check(args) -> int:
    """Flag segments whose length looks wrong for their word count."""
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    base = args.work / "out" / f"vol{plan['volume']}" / plan["chapter"]
    wav_dir = base / "wav"
    flags = []
    for segment in plan["segments"]:
        path = wav_dir / f"{segment['id']}.wav"
        if not path.exists():
            flags.append((segment, 0.0, "missing"))
            continue
        duration = sf.info(str(path)).duration
        words = len(segment["text"].split())
        minutes = duration / 60
        wpm = words / minutes if minutes else 0
        if duration < 0.25:
            flags.append((segment, duration, "too short"))
        elif words >= 3 and not (75 <= wpm <= 250):
            flags.append((segment, duration, f"{wpm:.0f} wpm"))
    for segment, duration, why in flags:
        print(f"{segment['id']:22} {duration:6.2f}s  {why:12} {segment['text'][:70]}")
    print(f"{len(flags)} flagged of {len(plan['segments'])}")
    return 0



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["render", "assemble", "check"])
    parser.add_argument("--volume", type=int, default=16)
    parser.add_argument("--chapter", default="ch02")
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    parser.add_argument("--work", type=Path, default=WORK_DEFAULT)
    parser.add_argument("--server", default=SERVER_DEFAULT)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--only", default="")
    parser.add_argument("--voice", default="", help="only render segments spoken by this voice")
    parser.add_argument("--ref-text", choices=["asr", "csv"], default="asr",
                        help="reference transcript: server ASR of the processed clip (default) "
                             "or the CSV transcript")
    parser.add_argument(
        "--ref-rank",
        default="",
        help='pick the Nth best reference per voice, e.g. "Rudeus Greyrat=1"',
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    args.plan = args.plan or (DATA / f"voice{args.volume}" / f"{args.chapter}.segments.json")
    if args.command == "check":
        return cmd_check(args)
    return cmd_render(args) if args.command == "render" else cmd_assemble(args)


if __name__ == "__main__":
    sys.exit(main())
