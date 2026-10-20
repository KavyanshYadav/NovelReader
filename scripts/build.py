#!/usr/bin/env python3
"""Merge a classified EPUB volume with contextual speaker attribution.

Usage:
    python3 scripts/build.py --volume 16

Reads:
  data/volumeN.classified.json
  data/attributionN/ch*.json        (data/attribution for volume 15)
  data/scene_metadataN.json          (data/scene_metadata.json for volume 15)

Writes:
  data/volumeN.json
"""

from __future__ import annotations

import argparse
import glob
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from volumes import get_volume

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def attribution_dir(volume: int) -> Path:
    return DATA / ("attribution" if volume == 15 else f"attribution{volume}")


def scene_metadata_path(volume: int) -> Path:
    return DATA / ("scene_metadata.json" if volume == 15 else f"scene_metadata{volume}.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=15)
    args = parser.parse_args()
    config = get_volume(args.volume)
    volume = config["number"]

    source = load_json(DATA / f"volume{volume}.classified.json")
    scene_metadata = load_json(scene_metadata_path(volume))

    attribution: dict[str, dict] = {}
    for path in sorted(glob.glob(str(attribution_dir(volume) / "ch*.json"))):
        chapter_attribution = load_json(Path(path))
        overlap = set(attribution) & set(chapter_attribution)
        if overlap:
            raise ValueError(f"Duplicate attribution IDs: {sorted(overlap)}")
        attribution.update(chapter_attribution)

    speaker_counts: Counter[str] = Counter()
    speaker_chapters: dict[str, set[str]] = defaultdict(set)
    speaker_scenes: dict[str, set[str]] = defaultdict(set)
    block_types: Counter[str] = Counter()
    total_blocks = 0
    speech_blocks = 0
    attributed_speech = 0
    embedded_dialogue = 0
    missing: list[str] = []

    for sequence, chapter in enumerate(source["chapters"], start=1):
        chapter["sequence"] = sequence
        chapter_speakers: set[str] = set()
        chapter_cast: set[str] = set()
        chapter_speech = 0
        for scene in chapter["scenes"]:
            meta = scene_metadata.get(scene["id"], {})
            scene["location"] = meta.get("location", "")
            scene["cast"] = meta.get("cast", [])
            if meta.get("pov"):
                scene["pov"] = meta["pov"]
            if meta.get("chapterPov"):
                chapter["pov"] = meta["chapterPov"]
            if not scene["location"] or not scene["cast"]:
                raise ValueError(f"Missing scene metadata for {scene['id']}")
            chapter_cast.update(scene["cast"])

            scene_speakers: set[str] = set()
            scene_speech = 0
            scene_words = 0

            for block in scene["blocks"]:
                total_blocks += 1
                block_id = block["id"]
                override = attribution.get(block_id)

                if override:
                    if "type" in override:
                        block["type"] = override["type"]
                    if override.get("speaker"):
                        block["speaker"] = override["speaker"]
                    for source_key, target_key in (
                        ("mixed", "mixed"),
                        ("recollection", "recollection"),
                        ("imagined", "imagined"),
                        ("embeddedDialogue", "embeddedDialogue"),
                        ("quoteSource", "quoteSource"),
                        ("note", "attributionNote"),
                    ):
                        if source_key in override:
                            block[target_key] = override[source_key]
                    if override.get("confidence"):
                        block["speakerConfidence"] = override["confidence"]
                    elif block.get("speaker"):
                        block["speakerConfidence"] = "high"

                block_type = block["type"]
                block_types[block_type] += 1
                if block.get("embeddedDialogue"):
                    embedded_dialogue += 1
                if block_type != "spacer":
                    scene_words += len(block.get("text", "").split())

                if block_type == "speech":
                    speech_blocks += 1
                    chapter_speech += 1
                    scene_speech += 1
                    if block.get("speaker"):
                        attributed_speech += 1
                        speaker = block["speaker"]
                        speaker_counts[speaker] += 1
                        speaker_chapters[speaker].add(chapter["id"])
                        speaker_scenes[speaker].add(scene["id"])
                        if not block.get("recollection") and not block.get("imagined"):
                            chapter_speakers.add(speaker)
                            scene_speakers.add(speaker)
                    else:
                        missing.append(block_id)
                elif block.get("speaker"):
                    block["speakerConfidence"] = block.get(
                        "speakerConfidence", "high"
                    )

            scene["wordCount"] = scene_words
            scene["speechCount"] = scene_speech
            scene["speakers"] = sorted(scene_speakers)

        chapter["cast"] = sorted(chapter_cast)
        chapter["sceneCount"] = len(chapter["scenes"])
        chapter["speechCount"] = chapter_speech
        chapter["speakers"] = sorted(chapter_speakers)
        if "kind" not in chapter:
            chapter["kind"] = (
                "extra" if chapter["title"].startswith("Extra Chapter") else "main"
            )

    source_ids = {
        block["id"]
        for chapter in source["chapters"]
        for scene in chapter["scenes"]
        for block in scene["blocks"]
    }
    unknown_ids = set(attribution) - source_ids

    if missing:
        raise ValueError(f"Speech blocks missing speakers: {missing}")
    if unknown_ids:
        print(
            "Note: attribution keys not present in the classified data: "
            f"{sorted(unknown_ids)}"
        )

    source["meta"]["schemaVersion"] = 2
    source["meta"]["generatedAt"] = datetime.now(timezone.utc).isoformat()
    source["meta"]["volume"] = volume
    source["meta"]["title"] = config["title"]
    source["meta"]["blurb"] = config["blurb"]
    source["meta"]["slug"] = config["slug"]
    source["meta"]["attribution"] = (
        "Speaker labels were assigned by contextual review, page by page. "
        "Diary excerpts, remembered quotations, imagined speech, and "
        "narration containing quoted fragments are distinguished from live "
        "dialogue."
    )
    source["meta"]["sceneMetadata"] = (
        "Each scene carries a location and cast. Cast lists include present "
        "characters, not only speaking characters."
    )

    source["stats"] = {
        "chapters": len(source["chapters"]),
        "scenes": sum(len(chapter["scenes"]) for chapter in source["chapters"]),
        "words": source["stats"].get("words", 0),
        "paragraphs": total_blocks,
        "blockTypes": dict(sorted(block_types.items())),
        "speechBlocks": speech_blocks,
        "attributedSpeech": attributed_speech,
        "speechCoverage": (
            round(attributed_speech / speech_blocks, 4) if speech_blocks else 1.0
        ),
        "embeddedDialogueBlocks": embedded_dialogue,
        "speakers": len(speaker_counts),
    }

    source["speakers"] = [
        {
            "name": name,
            "lines": count,
            "chapters": sorted(speaker_chapters[name]),
            "scenes": sorted(speaker_scenes[name]),
        }
        for name, count in sorted(
            speaker_counts.items(), key=lambda item: (-item[1], item[0])
        )
    ]

    output = DATA / f"volume{volume}.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(source, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"Wrote {output}")
    print(
        f"Chapters: {len(source['chapters'])} | speech: {speech_blocks} | "
        f"attributed: {attributed_speech} | speakers: {len(speaker_counts)}"
    )
    print("Top speakers:")
    for speaker in source["speakers"][:12]:
        print(f"  {speaker['name']}: {speaker['lines']}")


if __name__ == "__main__":
    main()
