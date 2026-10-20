#!/usr/bin/env python3
"""Print a chapter with stable block IDs so attribution can be reviewed in context.

Usage:
    python3 scripts/chapter_report.py --volume 16 --chapter ch01
    python3 scripts/chapter_report.py --volume 16 --chapter ch01 --speech-only
    python3 scripts/chapter_report.py --volume 16 --chapter ch01 --out /tmp/ch01.txt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--speech-only", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "data" / f"volume{args.volume}.classified.json").read_text(
            encoding="utf-8"
        )
    )
    chapter = next(
        (item for item in data["chapters"] if item["id"] == args.chapter), None
    )
    if chapter is None:
        raise SystemExit(f"Unknown chapter: {args.chapter}")

    lines = [
        f"# {chapter['id']} · {chapter['title']}",
        f"POV: {chapter['pov']} | words: {chapter['wordCount']}",
        "",
    ]
    for scene in chapter["scenes"]:
        lines.append(
            f"## {scene['id']} | POV {scene['pov']}"
            + (f" | header {scene.get('povHeader')}" if scene.get("povHeader") else "")
            + (
                f" | scene header {scene.get('sceneHeader')}"
                if scene.get("sceneHeader")
                else ""
            )
        )
        for block in scene["blocks"]:
            if block["type"] == "spacer":
                continue
            if args.speech_only and block["type"] != "speech":
                continue
            lines.append(f"[{block['id']}] ({block['type']}) {block['text']}")
        lines.append("")

    output = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
