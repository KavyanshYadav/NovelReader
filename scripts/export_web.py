#!/usr/bin/env python3
"""Export the finished volumes to the offline web reader.

Writes:
  web/data.js            a small manifest that lists every bundled volume
  web/volumes/volNN.js  the embedded data for one volume, loaded on demand

The reader is dependency-free and works when opened directly from disk, so the
JSON is embedded in JavaScript files instead of being fetched over HTTP.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from volumes import VOLUMES, get_volume
from optimize_images import optimize_images as optimize_images_folder

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WEB = ROOT / "web"


def optimize_images(images_dir: Path) -> None:
    """Re-encode the extracted artwork for the web (no-op without ImageMagick)."""
    try:
        optimize_images_folder(images_dir)
    except SystemExit:
        print("ImageMagick not found, leaving the artwork as it is.")


def image_sources(data: dict) -> list[str]:
    sources = ["CoverDesign.jpg"]
    for chapter in data.get("chapters", []):
        for image in chapter.get("images", []):
            source = Path(image.get("src", "")).name
            if source and source not in sources:
                sources.append(source)
    return sources


def write_atomically(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--volumes",
        default=",".join(str(number) for number in sorted(VOLUMES)),
        help="Comma-separated volume numbers to export",
    )
    args = parser.parse_args()
    volume_numbers = [int(item) for item in args.volumes.split(",") if item.strip()]

    manifest: dict[str, dict] = {}
    volumes_dir = WEB / "volumes"
    volumes_dir.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(exist_ok=True)

    for number in volume_numbers:
        config = get_volume(number)
        data_path = DATA / f"volume{number}.json"
        if not data_path.exists():
            print(f"Skipping volume {number}: {data_path} does not exist")
            continue

        data = json.loads(data_path.read_text(encoding="utf-8"))
        slug = config["slug"]
        stats = data.get("stats", {})
        data.setdefault("meta", {})
        data["meta"]["slug"] = slug
        data["meta"]["blurb"] = config["blurb"]
        data["meta"]["assetBase"] = f"images/{slug}"

        images_dir = WEB / "images" / slug
        images_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(config["epub"]) as archive:
            available = {
                Path(name).name
                for name in archive.namelist()
                if name.startswith("OEBPS/Images/")
            }
            missing = []
            for filename in image_sources(data):
                if filename not in available:
                    missing.append(filename)
                    continue
                (images_dir / filename).write_bytes(
                    archive.read(f"OEBPS/Images/{filename}")
                )
            if missing:
                print(f"Volume {number}: missing images {missing}")

        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        volume_js = (
            f"window.MUSOKU_VOLUME_DATA = window.MUSOKU_VOLUME_DATA || {{}};\n"
            f"window.MUSOKU_VOLUME_DATA[{json.dumps(str(number))}] = {payload};\n"
        )
        write_atomically(volumes_dir / f"{slug}.js", volume_js)

        manifest[str(number)] = {
            "number": number,
            "title": config["title"],
            "label": config.get("label", f"Volume {number}"),
            "slug": slug,
            "blurb": config["blurb"],
            "file": f"volumes/{slug}.js",
            "chapters": stats.get("chapters", len(data.get("chapters", []))),
            "scenes": stats.get("scenes", 0),
            "words": stats.get("words", 0),
            "speakers": stats.get("speakers", 0),
            "speechBlocks": stats.get("speechBlocks", 0),
        }
        print(
            f"Volume {number}: {len(data.get('chapters', []))} chapters, "
            f"{stats.get('scenes', 0)} scenes -> {volumes_dir / (slug + '.js')}"
        )

    manifest_js = (
        "window.MUSOKU_MANIFEST = "
        + json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    )
    write_atomically(WEB / "data.js", manifest_js)
    print(f"Wrote {WEB / 'data.js'} with {len(manifest)} volumes")

    optimize_images(WEB / "images")


if __name__ == "__main__":
    main()
