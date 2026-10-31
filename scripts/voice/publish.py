#!/usr/bin/env python3
"""Publish rendered chapters into the reader as a JS manifest.

For every ``out/vol<volume>/<chapter>/chapter.json`` this copies the MP3 to
``web/audio/vol<volume>/<chapter>.mp3`` and rewrites ``web/audio/manifest.js``.
The manifest is a plain script so the reader still works from ``file://``.

Run:
    python3 scripts/voice/publish.py --volume 16 --chapter ch02
    python3 scripts/voice/publish.py --all
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
WEB = ROOT / "web"
WORK_DEFAULT = Path.home() / "projects/voiceClone"


def chapter_title(volume: int, chapter_id: str) -> str:
    path = DATA / f"volume{volume}.json"
    if not path.exists():
        return chapter_id
    data = json.loads(path.read_text(encoding="utf-8"))
    for chapter in data["chapters"]:
        if chapter["id"] == chapter_id:
            number = chapter.get("number") or chapter_id.replace("ch", "")
            return f"Ch. {number} — {chapter.get('title', '')}".strip()
    return chapter_id


def collect(work: Path) -> list[dict]:
    entries = []
    for manifest_path in sorted(work.glob("out/vol*/*/chapter.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        base = manifest_path.parent
        mp3 = base / manifest["file"]
        if not mp3.exists():
            continue
        entries.append(
            {
                "volume": int(manifest["volume"]),
                "chapter": manifest["chapter"],
                "title": manifest.get("title", ""),
                "duration": manifest["duration"],
                "mp3": mp3,
                "blocks": [
                    {"id": b["id"], "start": b["start"], "end": b["end"]}
                    for b in manifest["blocks"]
                ],
            }
        )
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=WORK_DEFAULT)
    parser.add_argument("--volume", type=int, default=None)
    parser.add_argument("--chapter", default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dest", type=Path, default=WEB / "audio")
    args = parser.parse_args()

    entries = collect(args.work)
    if args.volume is not None:
        entries = [e for e in entries if e["volume"] == args.volume]
    if args.chapter:
        entries = [e for e in entries if e["chapter"] == args.chapter]
    if not entries:
        raise SystemExit("no rendered chapters found")

    args.dest.mkdir(parents=True, exist_ok=True)
    lines = ["window.MUSOKU_AUDIO = window.MUSOKU_AUDIO || {};"]
    for entry in entries:
        volume, chapter = entry["volume"], entry["chapter"]
        target_dir = args.dest / f"vol{volume}"
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{chapter}.mp3"
        shutil.copyfile(entry["mp3"], target)
        record = {
            "volume": volume,
            "chapter": chapter,
            "label": chapter_title(volume, chapter),
            "file": f"audio/vol{volume}/{chapter}.mp3",
            "duration": entry["duration"],
            "blocks": entry["blocks"],
        }
        lines.append(
            f"window.MUSOKU_AUDIO[{json.dumps(f'{volume}:{chapter}')}] = "
            + json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            + ";"
        )
        print(f"{volume}:{chapter}  {entry['duration'] / 60:5.1f} min  "
              f"{target.stat().st_size / 1024**2:5.1f} MB  {len(entry['blocks'])} blocks")

    (args.dest / "manifest.js").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest -> {args.dest / 'manifest.js'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
