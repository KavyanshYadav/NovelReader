#!/usr/bin/env python3
"""Publish the reader as a static site.

Usage:
    python3 scripts/deploy.py                       # copy web/ to dist/
    python3 scripts/deploy.py --out /var/www/html
    python3 scripts/deploy.py --base-url https://reader.example.com

The reader is a plain static site, so the whole `web/` folder is the publish
root. The script copies it, optionally rewrites the canonical and social
metadata to absolute URLs, and writes a sitemap.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"


def absolute(base_url: str | None, path: str) -> str:
    if not base_url:
        return path
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def rewrite_html(text: str, base_url: str | None, page: str) -> str:
    if not base_url:
        return text

    page_url = absolute(base_url, page)
    text = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{page_url}">',
        text,
    )
    text = re.sub(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{absolute(base_url, "images/vol15/CoverDesign.jpg")}">',
        text,
    )
    if 'property="og:url"' in text:
        text = re.sub(
            r'<meta property="og:url" content="[^"]*">',
            f'<meta property="og:url" content="{page_url}">',
            text,
        )
    else:
        text = text.replace(
            '<meta property="og:type" content="website">',
            '<meta property="og:type" content="website">\n'
            f'  <meta property="og:url" content="{page_url}">',
            1,
        )
    return text


def build_sitemap(base_url: str | None) -> str:
    manifest_path = WEB / "data.js"
    volumes: list[int] = []
    if manifest_path.exists():
        match = re.search(r"window\.MUSOKU_MANIFEST = (\{.*?\});\n", manifest_path.read_text(encoding="utf-8"), re.S)
        if match:
            volumes = sorted(int(key) for key in json.loads(match.group(1)))

    entries = [("", "1.0"), ("reader.html", "0.9")]
    for number in volumes:
        entries.append((f"reader.html?volume={number}", "0.6"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority in entries:
        location = absolute(base_url, path) if path else (base_url or "")
        lines.append("  <url>")
        lines.append(f"    <loc>{location}</loc>")
        lines.append(f"    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "dist"), help="output folder")
    parser.add_argument(
        "--base-url",
        default=None,
        help="public base URL, for example https://reader.example.com",
    )
    args = parser.parse_args()

    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(WEB, out)

    for page in ("index.html", "reader.html", "404.html"):
        path = out / page
        if path.exists():
            path.write_text(
                rewrite_html(path.read_text(encoding="utf-8"), args.base_url, page),
                encoding="utf-8",
            )

    (out / "sitemap.xml").write_text(build_sitemap(args.base_url), encoding="utf-8")

    total = sum(1 for path in out.rglob("*") if path.is_file())
    size = sum(path.stat().st_size for path in out.rglob("*") if path.is_file())
    print(f"Published {total} files ({size / 1_048_576:.1f} MB) to {out}")
    if args.base_url:
        print(f"Base URL: {args.base_url}")
    print("Upload that folder to any static host, or run:")
    print(f"  python3 -m http.server --directory {out} 8000")


if __name__ == "__main__":
    main()
