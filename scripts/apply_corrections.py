#!/usr/bin/env python3
"""Apply review corrections to a volume's speaker attribution files.

Usage:
    python3 scripts/apply_corrections.py --volume 16 --file data/corrections16.json

The correction file is a JSON object keyed by block ID. Each value is either a
speaker name (string) or an object of fields to set, for example:

    {
      "ch01-p0279": "Orsted",
      "ch09-p0123": { "speaker": "Ariel", "mixed": true, "note": "..." },
      "ch09-p0999": null
    }

A null value removes the entry. Blocks that are not present yet are created.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def attribution_dir(volume: int) -> Path:
    return ROOT / "data" / ("attribution" if volume == 15 else f"attribution{volume}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, required=True)
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    corrections = json.loads(Path(args.file).read_text(encoding="utf-8"))
    target = attribution_dir(args.volume)
    target.mkdir(parents=True, exist_ok=True)

    files: dict[str, dict] = {}
    for path in sorted(target.glob("ch*.json")):
        files[path.stem] = json.loads(path.read_text(encoding="utf-8"))

    applied = 0
    for block_id, value in corrections.items():
        chapter = block_id.split("-")[0]
        if chapter not in files:
            files[chapter] = {}
        if value is None:
            files[chapter].pop(block_id, None)
        elif isinstance(value, str):
            entry = files[chapter].get(block_id, {})
            entry["speaker"] = value
            files[chapter][block_id] = entry
        else:
            entry = files[chapter].get(block_id, {})
            entry.update(value)
            files[chapter][block_id] = entry
        applied += 1

    for chapter, entries in files.items():
        ordered = {key: entries[key] for key in sorted(entries)}
        path = target / f"{chapter}.json"
        path.write_text(
            json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"Applied {applied} corrections across {len(files)} chapter files")


if __name__ == "__main__":
    main()
