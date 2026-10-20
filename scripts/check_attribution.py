#!/usr/bin/env python3
"""Check speaker attribution coverage for one volume.

Usage:
    python3 scripts/check_attribution.py --volume 16
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
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "data" / f"volume{args.volume}.classified.json").read_text(
            encoding="utf-8"
        )
    )
    speech_ids = {
        block["id"]
        for chapter in data["chapters"]
        for scene in chapter["scenes"]
        for block in scene["blocks"]
        if block["type"] == "speech"
    }

    attribution = {}
    for path in sorted(attribution_dir(args.volume).glob("ch*.json")):
        attribution.update(json.loads(path.read_text(encoding="utf-8")))

    missing = sorted(speech_ids - set(attribution))
    extra = sorted(set(attribution) - speech_ids)
    empty = sorted(
        block_id
        for block_id, value in attribution.items()
        if not value.get("speaker")
    )

    print(f"Volume {args.volume}: {len(speech_ids)} speech blocks")
    print(f"Attributed: {len(speech_ids) - len(missing)}")
    if missing:
        print(f"Missing ({len(missing)}):")
        for block_id in missing:
            print("  ", block_id)
    if extra:
        print(f"Extra/unknown keys ({len(extra)}):")
        for block_id in extra:
            print("  ", block_id)
    if empty:
        print(f"Entries without speaker ({len(empty)}): {empty}")
    if not missing and not extra and not empty:
        print("Attribution coverage complete.")


if __name__ == "__main__":
    main()
