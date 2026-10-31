#!/usr/bin/env python3
"""Turn a chapter of the reader data into a voiceover plan.

Every block is split into *segments*: the quoted spans are spoken by the
block's attributed speaker, everything else is the POV narrator. Each segment
gets a voice folder from the English voice dataset, an emotion folder, a speed
and any inline control tags.

The emotion pass below is hand written for volume 16, chapter 2 ("Guardian
Beast"); everything not listed falls back to neutral narration at 0.92x.

Run:
    python3 scripts/voice/plan.py --volume 16 --chapter ch02
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
DATASET_DEFAULT = Path.home() / "projects/mushokuTensei/character_voices_eng"

# Novel speaker -> English dataset folder.
CAST = {
    "Rudeus": "Rudeus Greyrat",
    "Sylphiette": "Sylphiette Greyrat",
    "Roxy": "Roxy Migurdia",
    "Eris": "Eris Boreas Greyrat",
    "Aisha": "Aisha Greyrat",
    "Lilia": "Lilia Greyrat",
    "Norn": "Norn Greyrat",
    "Arumanfi": "Almanfi",
    # No folder exists for these; the narrator reads them.
    "Leo": "Rudeus Greyrat",
    "Crowd": "Aisha Greyrat",
}

# Speakers whose lines are read by the narrator rather than in character.
NARRATED = {"Leo"}

NARRATION_SPEED = 0.92
NARRATION_TONE = "neutral"

# (tone, speed) per block. Speech blocks apply to their quoted spans; narration
# blocks apply to the whole block. Segment-level overrides are keyed by segment
# suffix when a block needs two different readings.
OVERRIDES: dict[str, dict] = {
    # --- scene 1: the plan ------------------------------------------------
    "ch02-p0002": {"tone": "serious"},
    "ch02-p0003": {"tone": "serious"},
    # --- scene 2: the first summoning ------------------------------------
    "ch02-p0009": {"tone": "neutral", "speed": 1.0},
    "ch02-p0010": {"tone": "excited", "speed": 1.02},
    "ch02-p0011": {"tone": "playful"},
    "ch02-p0012": {"tone": "playful"},
    "ch02-p0013": {"tone": "neutral", "speed": 1.0},
    "ch02-p0014": {"tone": "worried", "speed": 1.0},
    "ch02-p0015": {"tone": "worried"},
    "ch02-p0016": {"tone": "serious"},
    "ch02-p0017": {"tone": "neutral", "speed": 1.0},
    "ch02-p0018": {"tone": "worried", "speed": 1.0},
    "ch02-p0019": {"tone": "neutral"},
    "ch02-p0020": {"tone": "playful"},
    "ch02-p0021": {"tone": "neutral"},
    "ch02-p0022": {"tone": "neutral", "speed": 1.0},
    "ch02-p0023": {"tone": "excited", "speed": 1.02},
    "ch02-p0024": {"tone": "playful"},
    "ch02-p0025": {"tone": "excited", "speed": 1.02},
    "ch02-p0026": {"tone": "playful"},
    "ch02-p0027": {"tone": "neutral"},
    "ch02-p0028": {"tone": "neutral", "speed": 1.0},
    "ch02-p0029": {"tone": "neutral"},
    "ch02-p0030": {"tone": "worried", "speed": 1.0},
    "ch02-p0031": {"tone": "neutral"},
    "ch02-p0032": {"tone": "serious"},
    "ch02-p0033": {"tone": "neutral", "speed": 1.0},
    "ch02-p0034": {"tone": "serious"},
    "ch02-p0035": {"tone": "neutral", "speed": 1.0},
    "ch02-p0036": {"tone": "neutral", "speed": 0.85},
    "ch02-p0037": {"tone": "worried", "speed": 1.0},
    "ch02-p0038": {"tone": "playful", "speed": 1.0},
    "ch02-p0039": {"tone": "worried"},
    "ch02-p0040": {"tone": "worried"},
    "ch02-p0041": {"tone": "serious", "speed": 0.98},
    "ch02-p0042": {"tone": "playful"},
    "ch02-p0043": {"tone": "worried"},
    "ch02-p0044": {"tone": "serious"},
    "ch02-p0045": {"tone": "serious", "speed": 1.0},
    "ch02-p0048": {"tone": "serious", "speed": 1.0},
    "ch02-p0049": {"tone": "serious"},
    "ch02-p0050": {"tone": "serious"},
    "ch02-p0053": {"tone": "playful"},
    "ch02-p0054": {"tone": "playful"},
    "ch02-p0055": {"tone": "excited"},
    "ch02-p0056": {"tone": "excited", "speed": 1.05},
    "ch02-p0057": {"tone": "surprised"},
    "ch02-p0058": {"tone": "worried"},
    "ch02-p0059": {"tone": "serious"},
    "ch02-p0060": {"tone": "excited", "speed": 1.06},
    "ch02-p0061": {"tone": "surprised"},
    "ch02-p0062": {"tone": "excited", "speed": 1.05},
    "ch02-p0063": {"tone": "surprised"},
    "ch02-p0064": {"tone": "serious", "speed": 0.9},
    "ch02-p0065": {"tone": "surprised"},
    "ch02-p0066": {"tone": "serious", "speed": 0.95},
    "ch02-p0067": {"tone": "neutral"},
    "ch02-p0068": {"tone": "serious", "speed": 1.05},
    "ch02-p0069": {"tone": "surprised"},
    "ch02-p0070": {"tone": "neutral"},
    "ch02-p0071": {"tone": "playful"},
    "ch02-p0072": {"tone": "serious", "speed": 1.06},
    "ch02-p0073": {"tone": "neutral"},
    "ch02-p0074": {"tone": "playful"},
    "ch02-p0075": {"tone": "worried"},
    "ch02-p0076": {"tone": "playful"},
    "ch02-p0077": {"tone": "worried", "speed": 1.02},
    "ch02-p0078": {"tone": "serious"},
    "ch02-p0079": {"tone": "neutral", "speed": 1.0},
    "ch02-p0080": {"tone": "serious"},
    "ch02-p0081": {"tone": "worried", "speed": 1.0},
    "ch02-p0082": {"tone": "serious"},
    "ch02-p0083": {"tone": "surprised"},
    "ch02-p0084": {"tone": "playful"},
    "ch02-p0085": {"tone": "neutral", "speed": 1.0},
    "ch02-p0086": {"tone": "serious"},
    "ch02-p0087": {"tone": "neutral"},
    "ch02-p0088": {"tone": "serious", "speed": 1.0},
    "ch02-p0089": {"tone": "serious", "speed": 1.03},
    "ch02-p0090": {"tone": "neutral", "speed": 1.0},
    "ch02-p0091": {"tone": "serious", "speed": 1.04},
    "ch02-p0092": {"tone": "neutral", "speed": 1.0},
    "ch02-p0093": {"tone": "neutral"},
    "ch02-p0094": {"tone": "serious"},
    "ch02-p0095": {"tone": "worried", "speed": 1.0},
    "ch02-p0096": {"tone": "serious"},
    "ch02-p0097": {"tone": "neutral", "speed": 1.0},
    "ch02-p0098": {"tone": "serious", "speed": 1.05},
    "ch02-p0099": {"tone": "neutral"},
    "ch02-p0100": {"tone": "serious", "speed": 1.0},
    "ch02-p0101": {"tone": "neutral"},
    "ch02-p0102": {"tone": "worried", "speed": 1.0},
    "ch02-p0103": {"tone": "neutral"},
    # --- scene 3: the second summoning ------------------------------------
    "ch02-p0109": {"tone": "serious"},
    "ch02-p0111": {"tone": "playful"},
    "ch02-p0112": {"tone": "excited", "speed": 1.02},
    "ch02-p0113": {"tone": "serious"},
    "ch02-p0114": {"tone": "excited"},
    "ch02-p0115": {"tone": "neutral"},
    "ch02-p0116": {"tone": "serious"},
    "ch02-p0117": {"tone": "serious"},
    "ch02-p0118": {"tone": "excited"},
    "ch02-p0119": {"tone": "excited"},
    "ch02-p0120": {"tone": "excited", "speed": 1.05},
    "ch02-p0121": {"tone": "surprised"},
    "ch02-p0122": {"tone": "playful", "speed": 0.98},
    "ch02-p0123": {"tone": "surprised"},
    "ch02-p0124": {"tone": "playful"},
    "ch02-p0125": {"tone": "surprised"},
    "ch02-p0126": {"tone": "surprised"},
    "ch02-p0128": {"tone": "playful"},
    "ch02-p0129": {"tone": "excited", "speed": 1.02},
    "ch02-p0130": {"tone": "worried", "speed": 1.0},
    "ch02-p0131": {"tone": "playful", "speed": 1.0},
    "ch02-p0132": {"tone": "neutral", "speed": 1.0},
    "ch02-p0134": {"tone": "neutral", "speed": 1.0},
    "ch02-p0136": {"tone": "happy"},
    "ch02-p0137": {"tone": "surprised"},
    "ch02-p0138": {"tone": "surprised", "speed": 1.02},
    "ch02-p0139": {"tone": "playful"},
    "ch02-p0140": {"tone": "neutral", "speed": 1.0},
    "ch02-p0141": {"tone": "playful", "speed": 1.0},
    "ch02-p0142": {"tone": "annoyed"},
    "ch02-p0144": {"tone": "neutral", "speed": 1.0},
    "ch02-p0145": {"tone": "neutral"},
    "ch02-p0146": {"tone": "worried"},
    "ch02-p0147": {"tone": "annoyed"},
    "ch02-p0148": {"tone": "worried"},
    "ch02-p0149": {"tone": "worried"},
    "ch02-p0150": {"tone": "serious", "speed": 0.98},
    "ch02-p0151": {"tone": "happy", "speed": 1.02},
    "ch02-p0152": {"tone": "neutral"},
    "ch02-p0153": {"tone": "surprised", "speed": 1.02},
    "ch02-p0154": {"tone": "neutral"},
    "ch02-p0155": {"tone": "affectionate"},
    "ch02-p0156": {"tone": "playful", "speed": 1.0},
    "ch02-p0157": {"tone": "playful"},
    "ch02-p0158": {"tone": "playful"},
    "ch02-p0159": {"tone": "playful"},
    "ch02-p0161": {"tone": "excited", "speed": 1.04},
    "ch02-p0162": {"tone": "neutral"},
    "ch02-p0163": {"tone": "surprised", "speed": 1.04},
    "ch02-p0164": {"tone": "playful"},
    "ch02-p0165": {"tone": "worried", "speed": 1.0},
    "ch02-p0166": {"tone": "affectionate"},
    "ch02-p0167": {"tone": "serious", "speed": 0.98},
    "ch02-p0168": {"tone": "happy", "speed": 1.02},
    "ch02-p0170": {"tone": "affectionate"},
    "ch02-p0171": {"tone": "serious", "speed": 0.98},
    "ch02-p0172": {"tone": "happy", "speed": 1.02},
    "ch02-p0173": {"tone": "playful"},
    "ch02-p0174": {"tone": "serious", "speed": 0.98},
    "ch02-p0175": {"tone": "sad", "speed": 0.95},
    "ch02-p0176": {"tone": "happy", "speed": 1.0},
    "ch02-p0177": {"tone": "affectionate"},
}

QUOTE_RE = re.compile(r"[“\"]([^“”\"]+)[”\"]")


def split_block(text: str) -> list[tuple[str, str]]:
    """Split into (role, text) pieces: quoted speech and surrounding narration."""
    pieces: list[tuple[str, str]] = []
    cursor = 0
    for match in QUOTE_RE.finditer(text):
        before = text[cursor : match.start()].strip()
        if before and re.search(r"[A-Za-z0-9]", before):
            pieces.append(("narration", before))
        spoken = match.group(1).strip()
        if spoken and re.search(r"[A-Za-z0-9]", spoken):
            pieces.append(("speech", spoken))
        cursor = match.end()
    tail = text[cursor:].strip()
    if tail and re.search(r"[A-Za-z0-9]", tail):
        pieces.append(("narration", tail))
    if not pieces:
        pieces.append(("narration", text.strip()))
    return pieces


def available_tones(dataset: Path) -> dict[str, set[str]]:
    """tone folders that actually contain a combined clip with a transcript."""
    import csv

    tones: dict[str, set[str]] = {}
    with (dataset / "combined_clips.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["text"].strip():
                tones.setdefault(row["character"], set()).add(row["tone"])
    return tones


def resolve_tone(voice: str, tone: str, tones: dict[str, set[str]]) -> str:
    have = tones.get(voice, set())
    if tone in have:
        return tone
    if "neutral" in have:
        return "neutral"
    return sorted(have)[0] if have else "neutral"


def build(volume: int, chapter_id: str, dataset: Path) -> dict:
    source = DATA / f"volume{volume}.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    chapter = next(c for c in data["chapters"] if c["id"] == chapter_id)
    tones = available_tones(dataset)

    segments: list[dict] = []
    blocks: list[dict] = []
    for scene in chapter["scenes"]:
        for block in scene["blocks"]:
            if block["type"] in ("spacer", "image"):
                continue
            override = OVERRIDES.get(block["id"], {})
            block_tone = override.get("tone", NARRATION_TONE)
            block_speed = override.get("speed", NARRATION_SPEED)
            block_voice = CAST.get(block.get("speaker") or "Rudeus", "Rudeus Greyrat")
            narrator_voice = CAST["Rudeus"]

            first = len(segments)
            for index, (role, text) in enumerate(split_block(block["text"])):
                if role == "speech" and block.get("speaker"):
                    novel_speaker = block["speaker"]
                    voice = CAST.get(novel_speaker, block_voice)
                    tone = block_tone
                    speed = 1.0 if "speed" not in override else block_speed
                    if novel_speaker in NARRATED:
                        voice = narrator_voice
                else:
                    novel_speaker = "Rudeus"
                    voice = narrator_voice
                    tone = NARRATION_TONE if block["type"] != "narration" else block_tone
                    speed = NARRATION_SPEED
                    if block["type"] == "narration":
                        speed = block_speed
                if role == "narration" and block["type"] == "speech":
                    # "she said", "Eris declared in excitement" etc.
                    tone = NARRATION_TONE
                    speed = NARRATION_SPEED
                segments.append(
                    {
                        "id": f"{block['id']}-s{index + 1:02d}",
                        "blockId": block["id"],
                        "scene": scene["id"],
                        "role": role,
                        "speaker": novel_speaker,
                        "voice": voice,
                        "tone": resolve_tone(voice, tone, tones),
                        "requestedTone": tone,
                        "speed": round(speed, 3),
                        "text": text,
                        "tags": [],
                    }
                )
            blocks.append(
                {
                    "id": block["id"],
                    "scene": scene["id"],
                    "type": block["type"],
                    "speaker": block.get("speaker"),
                    "segments": list(range(first, len(segments))),
                }
            )

    return {
        "volume": volume,
        "chapter": chapter_id,
        "title": chapter["title"],
        "pov": chapter["pov"],
        "dataset": str(dataset),
        "blocks": blocks,
        "segments": segments,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=16)
    parser.add_argument("--chapter", default="ch02")
    parser.add_argument("--dataset", type=Path, default=DATASET_DEFAULT)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    plan = build(args.volume, args.chapter, args.dataset)
    out = args.out or (DATA / f"voice{args.volume}" / f"{args.chapter}.segments.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")

    from collections import Counter

    segs = plan["segments"]
    words = sum(len(s["text"].split()) for s in segs)
    print(f"{len(plan['blocks'])} blocks -> {len(segs)} segments, {words} words")
    print("roles:", dict(Counter(s["role"] for s in segs)))
    print("voices:", dict(Counter(s["voice"] for s in segs)))
    print("tones:", dict(Counter(s["tone"] for s in segs)))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
