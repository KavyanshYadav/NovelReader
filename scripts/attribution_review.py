#!/usr/bin/env python3
"""Print a chapter's speech blocks with their assigned speaker for review.

Usage:
    python3 scripts/attribution_review.py --volume 16 --chapter ch09
    python3 scripts/attribution_review.py --volume 16 --chapter ch09 --missing-only
    python3 scripts/attribution_review.py --volume 16 --chapter ch09 --out /tmp/review.txt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def attribution_dir(volume: int) -> Path:
    return ROOT / "data" / ("attribution" if volume == 15 else f"attribution{volume}")


def load_attribution(volume: int) -> dict:
    attribution: dict = {}
    for path in sorted(attribution_dir(volume).glob("ch*.json")):
        attribution.update(json.loads(path.read_text(encoding="utf-8")))
    return attribution


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--missing-only", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "data" / f"volume{args.volume}.classified.json").read_text(
            encoding="utf-8"
        )
    )
    attribution = load_attribution(args.volume)
    chapter = next(
        (item for item in data["chapters"] if item["id"] == args.chapter), None
    )
    if chapter is None:
        raise SystemExit(f"Unknown chapter: {args.chapter}")

    lines: list[str] = []
    for scene in chapter["scenes"]:
        lines.append(f"--- {scene['id']} (pov {scene['pov']}) ---")
        for block in scene["blocks"]:
            if block["type"] != "speech":
                continue
            entry = attribution.get(block["id"])
            speaker = entry.get("speaker") if entry else None
            if args.missing_only and speaker:
                continue
            flags = []
            if entry:
                for key in ("mixed", "embeddedDialogue", "recollection", "imagined"):
                    if entry.get(key):
                        flags.append(key)
                if entry.get("confidence"):
                    flags.append(entry["confidence"])
                if entry.get("type"):
                    flags.append(f"type={entry['type']}")
            marker = f"[{','.join(flags)}]" if flags else ""
            text = block["text"].replace("\n", " ")
            lines.append(f"{block['id']} | {speaker or 'MISSING'}{marker} | {text}")
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
