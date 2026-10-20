#!/usr/bin/env python3
"""Extract a Mushoku Tensei volume from EPUB into a structured JSON skeleton.

Usage:
    python3 scripts/extract.py --volume 16

This script only extracts and normalizes content. Speaker attribution is done in a
separate data pass so that decisions can be reviewed independently.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

from volumes import POV_NAMES, get_volume

ROOT = Path(__file__).resolve().parents[1]
NS = {"xhtml": "http://www.w3.org/1999/xhtml"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def inline_html(el: ET.Element) -> str:
    """Serialize an element's children, preserving only useful inline emphasis."""
    parts: list[str] = []
    if el.text:
        parts.append(escape(el.text, quote=False))
    for child in el:
        tag = local_name(child.tag)
        style = child.get("style", "") or ""
        if tag == "br":
            parts.append("<br/>")
        elif tag == "img":
            src = child.get("src", "")
            parts.append(f'<img src="{escape(src, quote=True)}" alt=""/>')
        elif tag == "span":
            inner = inline_html(child)
            if "font-style: italic" in style:
                inner = f"<em>{inner}</em>"
            if "font-weight: bold" in style:
                inner = f"<strong>{inner}</strong>"
            parts.append(inner)
        else:
            parts.append(inline_html(child))
        if child.tail:
            parts.append(escape(child.tail, quote=False))
    return "".join(parts)


def plain_text(el: ET.Element) -> str:
    text = "".join(el.itertext())
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    return text.strip()


def split_scenes(
    paragraphs: list[dict],
    default_pov: str,
    chapter_id: str,
) -> list[dict]:
    scenes: list[dict] = []
    current: dict | None = None
    pov = default_pov

    def new_scene(header: str | None = None, scene_header: str | None = None) -> dict:
        scene = {
            "id": f"{chapter_id}-s{len(scenes) + 1:02d}",
            "pov": pov,
            "povHeader": header,
            "sceneHeader": scene_header,
            "location": "",
            "cast": [],
            "blocks": [],
        }
        scenes.append(scene)
        return scene

    for paragraph in paragraphs:
        text = paragraph["text"]
        class_name = paragraph.get("className", "")
        is_star = class_name == "P__STAR__STAR__STAR__page_break"
        is_header = class_name == "P_Chapter_Header"
        if is_star:
            if text in POV_NAMES:
                pov = text
                current = new_scene(header=text)
                continue
            if text and text.strip("* ") == "":
                current = new_scene()
                continue
            if text:
                current = new_scene(scene_header=text)
                continue
        if is_header:
            # Volume 26 uses P_Chapter_Header for both the chapter title and
            # the name that introduces a section. The title is dropped during
            # extraction, so anything left here marks a new section.
            current = new_scene(scene_header=text)
            continue
        if current is None:
            current = new_scene()
        current["blocks"].append(paragraph)
    return scenes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=15)
    args = parser.parse_args()
    config = get_volume(args.volume)

    chapters: list[dict] = []

    with zipfile.ZipFile(config["epub"]) as zf:
        for ch_id, number, title, filename, default_pov, kind in config["chapters"]:
            raw = zf.read(f"OEBPS/Text/{filename}")
            root = ET.fromstring(raw)
            body = root.find(".//xhtml:body", NS)
            if body is None:
                raise RuntimeError(f"No body in {filename}")

            paragraphs: list[dict] = []
            images: list[dict] = []
            source_index = 0
            chapter_title_seen = False

            for el in body.iter():
                if local_name(el.tag) != "p":
                    continue
                cls = el.get("class", "") or ""
                text = plain_text(el)
                html = inline_html(el)
                imgs = el.findall(".//xhtml:img", NS)

                if imgs:
                    for img in imgs:
                        src = img.get("src", "")
                        images.append({
                            "id": f"{ch_id}-img{len(images) + 1:02d}",
                            "type": "image",
                            "src": Path(src).name,
                            "alt": "",
                        })
                    continue

                if not text:
                    if paragraphs and paragraphs[-1]["type"] != "spacer":
                        paragraphs.append({
                            "id": f"{ch_id}-p{source_index:04d}",
                            "sourceIndex": source_index,
                            "type": "spacer",
                            "text": "",
                            "html": "",
                            "className": cls,
                        })
                    source_index += 1
                    continue

                if cls == "P__STAR__STAR__STAR__page_break" and not chapter_title_seen:
                    chapter_title_seen = True
                    source_index += 1
                    continue

                if cls == "P_Chapter_Header" and not chapter_title_seen:
                    # Volume 26 style: the chapter title is a header paragraph.
                    chapter_title_seen = True
                    source_index += 1
                    continue

                is_italic = "font-style: italic" in html or any(
                    "font-style: italic" in (span.get("style", "") or "")
                    for span in el.findall(".//xhtml:span", NS)
                )
                is_bold = "font-weight: bold" in html or any(
                    "font-weight: bold" in (span.get("style", "") or "")
                    for span in el.findall(".//xhtml:span", NS)
                )
                drop_cap = any(
                    re.search(r"font-size:\s*(?:2\.40|2\.\d+)em", span.get("style", "") or "")
                    for span in el.findall(".//xhtml:span", NS)
                )

                paragraphs.append({
                    "id": f"{ch_id}-p{source_index:04d}",
                    "sourceIndex": source_index,
                    "type": "text",
                    "text": text,
                    "html": html,
                    "className": cls,
                    "italic": is_italic,
                    "bold": is_bold,
                    "dropCap": drop_cap,
                })
                source_index += 1

            while paragraphs and paragraphs[-1]["type"] == "spacer":
                paragraphs.pop()

            scenes = split_scenes(paragraphs, default_pov, ch_id)
            scenes = [scene for scene in scenes if scene["blocks"]]

            word_count = sum(
                len(paragraph["text"].split())
                for paragraph in paragraphs
                if paragraph["type"] != "spacer"
            )
            chapters.append({
                "id": ch_id,
                "number": number,
                "title": title,
                "pov": default_pov,
                "kind": kind,
                "wordCount": word_count,
                "scenes": scenes,
                "images": images,
            })

    data = {
        "meta": {
            "series": "Mushoku Tensei: Jobless Reincarnation",
            "volume": config["number"],
            "title": config["title"],
            "blurb": config["blurb"],
            "slug": config["slug"],
            "author": "Rifujin na Magonote",
            "illustrator": "Shirotaka",
            "publisher": "Seven Seas Entertainment",
            "language": "en",
            "source": config["epub"].name,
            "schemaVersion": 1,
            "notes": "Extracted from the user's EPUB for a personal reading edition.",
        },
        "stats": {
            "chapters": len(chapters),
            "words": sum(chapter["wordCount"] for chapter in chapters),
            "paragraphs": sum(
                1
                for chapter in chapters
                for scene in chapter["scenes"]
                for block in scene["blocks"]
                if block["type"] != "spacer"
            ),
        },
        "chapters": chapters,
    }

    output = ROOT / "data" / f"volume{config['number']}.source.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output}")
    print(
        f"Chapters: {data['stats']['chapters']}, words: {data['stats']['words']}, "
        f"paragraphs: {data['stats']['paragraphs']}"
    )


if __name__ == "__main__":
    main()
