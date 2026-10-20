#!/usr/bin/env python3
"""Apply compact speaker decisions to a volume's attribution files.

Usage:
    python3 scripts/apply_compact.py --volume 16 --file /tmp/opencode/attr16/ch09.txt

Each line of the input file is one decision:

    ch09-p0123 Orsted
    ch09-p0124 Rudeus mixed
    ch09-p0125 Ariel embeddedDialogue,medium
    ch09-p0126 Rudeus type=narration

The first token after the block ID is the speaker. The remaining tokens are
optional flags: mixed, embeddedDialogue, recollection, imagined, note=...,
type=narration|quotation|thought, confidence=medium|low.

Existing entries are updated; missing ones are created.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FLAG_FIELDS = {
    "mixed",
    "embeddedDialogue",
    "recollection",
    "imagined",
}


def attribution_dir(volume: int) -> Path:
    return ROOT / "data" / ("attribution" if volume == 15 else f"attribution{volume}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, required=True)
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    target = attribution_dir(args.volume)
    target.mkdir(parents=True, exist_ok=True)

    files: dict[str, dict] = {}
    for path in sorted(target.glob("ch*.json")):
        files[path.stem] = json.loads(path.read_text(encoding="utf-8"))

    applied = 0
    for raw_line in Path(args.file).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        block_id = parts[0]
        speaker = parts[1]
        chapter = block_id.split("-")[0]
        files.setdefault(chapter, {})
        entry = files[chapter].get(block_id, {})
        entry["speaker"] = speaker
        for token in parts[2:]:
            if token in FLAG_FIELDS:
                entry[token] = True
            elif token.startswith("type="):
                entry["type"] = token.split("=", 1)[1]
            elif token.startswith("confidence="):
                entry["confidence"] = token.split("=", 1)[1]
            elif token.startswith("note="):
                entry["note"] = token.split("=", 1)[1]
        files[chapter][block_id] = entry
        applied += 1

    for chapter, entries in files.items():
        ordered = {key: entries[key] for key in sorted(entries)}
        path = target / f"{chapter}.json"
        path.write_text(
            json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"Applied {applied} decisions across {len(files)} chapter files")


if __name__ == "__main__":
    main()
