#!/usr/bin/env python3
"""Build a volume's scene metadata file from locations plus speaker data.

Usage:
    python3 scripts/make_scene_metadata.py --volume 16 --file /tmp/opencode/scene16.json

The input file maps scene IDs to {"location": "...", "present": ["..."]}.
"present" lists characters who are in the scene but may not speak.
Every speaker of a scene is added automatically, along with the scene POV, so
the resulting metadata always satisfies the validator.
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
    parser.add_argument("--out")
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "data" / f"volume{args.volume}.classified.json").read_text(
            encoding="utf-8"
        )
    )
    attribution: dict = {}
    for path in sorted(attribution_dir(args.volume).glob("ch*.json")):
        attribution.update(json.loads(path.read_text(encoding="utf-8")))

    source = json.loads(Path(args.file).read_text(encoding="utf-8"))
    result: dict[str, dict] = {}

    for chapter in data["chapters"]:
        for scene in chapter["scenes"]:
            scene_id = scene["id"]
            entry = source.get(scene_id)
            if not entry:
                raise SystemExit(f"Missing scene entry for {scene_id}")
            cast = set(entry.get("present", []))
            cast.add(scene["pov"])
            for block in scene["blocks"]:
                if block["type"] != "speech":
                    continue
                override = attribution.get(block["id"], {})
                speaker = override.get("speaker")
                if speaker and not override.get("recollection") and not override.get(
                    "imagined"
                ):
                    cast.add(speaker)
            record = {
                "location": entry["location"],
                "cast": sorted(cast),
            }
            if entry.get("pov"):
                record["pov"] = entry["pov"]
            if entry.get("chapterPov"):
                record["chapterPov"] = entry["chapterPov"]
            result[scene_id] = record

    missing = sorted(set(source) - set(result))
    if missing:
        raise SystemExit(f"Unknown scene IDs in source file: {missing}")

    out = Path(args.out) if args.out else (
        ROOT / "data" / f"scene_metadata{args.volume}.json"
    )
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {out} with {len(result)} scenes")


if __name__ == "__main__":
    main()
