#!/usr/bin/env python3
"""Shrink the extracted artwork for the web.

The EPUB artwork is 1403x2000 JPEG straight out of the book, which is far more
than the reader ever draws. Re-encoding it once keeps the site fast and the
repository small without touching the original EPUBs.

Usage:
    python3 scripts/optimize_images.py                 # optimize web/images
    python3 scripts/optimize_images.py --width 1200
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "web" / "images"

COVER_WIDTH = 900
ART_WIDTH = 1200
QUALITY = 82


def have_imagemagick() -> bool:
    return shutil.which("magick") is not None or shutil.which("convert") is not None


def image_tool() -> list[str]:
    if shutil.which("magick"):
        return ["magick"]
    if shutil.which("convert"):
        return ["convert"]
    raise SystemExit("ImageMagick is required to optimize the artwork")


def dimensions(path: Path) -> tuple[int, int]:
    tool = image_tool()
    result = subprocess.run(
        [*tool, "identify", "-format", "%w %h", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    width, height = result.stdout.split()[:2]
    return int(width), int(height)


def optimize(path: Path, max_width: int) -> tuple[int, int]:
    before = path.stat().st_size
    width, height = dimensions(path)
    if width <= max_width:
        return before, before

    temporary = path.with_suffix(".tmp.jpg")
    subprocess.run(
        [
            *image_tool(),
            str(path),
            "-resize",
            f"{max_width}x",
            "-strip",
            "-interlace",
            "Plane",
            "-sampling-factor",
            "4:2:0",
            "-quality",
            str(QUALITY),
            str(temporary),
        ],
        check=True,
        capture_output=True,
    )
    temporary.replace(path)
    return before, path.stat().st_size


def optimize_images(root: Path, width: int = ART_WIDTH) -> tuple[int, int, int]:
    """Re-encode every JPEG under root. Returns (before, after, changed)."""
    if not have_imagemagick():
        raise SystemExit("ImageMagick is required to optimize the artwork")
    if not root.exists():
        return 0, 0, 0

    before_total = 0
    after_total = 0
    changed = 0
    for path in sorted(root.rglob("*.jpg")):
        limit = COVER_WIDTH if path.name.startswith("Cover") else width
        before, after = optimize(path, limit)
        before_total += before
        after_total += after
        if after < before:
            changed += 1
    return before_total, after_total, changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default=str(IMAGES))
    parser.add_argument("--width", type=int, default=ART_WIDTH)
    args = parser.parse_args()

    if not have_imagemagick():
        print("ImageMagick not found, leaving the artwork as it is.")
        return

    before_total, after_total, changed = optimize_images(
        Path(args.images), args.width
    )
    if not changed and before_total == 0:
        print(f"No artwork folder at {args.images}")
        return

    saved = (before_total - after_total) / 1_048_576
    print(
        f"Optimized {changed} images: "
        f"{before_total / 1_048_576:.1f} MB -> {after_total / 1_048_576:.1f} MB "
        f"({saved:.1f} MB saved)"
    )


if __name__ == "__main__":
    main()
