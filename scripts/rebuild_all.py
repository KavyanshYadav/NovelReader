#!/usr/bin/env python3
"""Run the whole reader pipeline for every configured volume.

Usage:
    python3 scripts/rebuild_all.py            # all volumes
    python3 scripts/rebuild_all.py 19 20 21  # only these volumes
    python3 scripts/rebuild_all.py --skip-extract 19

Each stage runs the same script the reader uses, with a --volume argument, so
a single volume can also be rebuilt on its own.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from volumes import VOLUMES

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(args: list[str]) -> None:
    print(f"\n$ python3 {' '.join(args)}")
    result = subprocess.run([sys.executable, *args], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"Step failed: {' '.join(args)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("volumes", nargs="*", type=int)
    parser.add_argument("--skip-extract", action="store_true")
    parser.add_argument("--skip-classify", action="store_true")
    args = parser.parse_args()

    numbers = args.volumes or sorted(VOLUMES)
    for number in numbers:
        if number not in VOLUMES:
            raise SystemExit(f"Unknown volume: {number}")

    for number in numbers:
        print(f"\n=== Volume {number} ===")
        if not args.skip_extract:
            run(["scripts/extract.py", "--volume", str(number)])
        if not args.skip_classify:
            run(["scripts/classify.py", "--volume", str(number)])
        run(["scripts/build.py", "--volume", str(number)])
        run(["scripts/validate.py", "--volume", str(number)])

    run(["scripts/export_web.py", "--volumes", ",".join(str(n) for n in numbers)])
    print("\nAll done.")


if __name__ == "__main__":
    main()
