#!/usr/bin/env python3
"""Validate a finished volume JSON before it is consumed by the renderer.

Usage:
    python3 scripts/validate.py --volume 16
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=15)
    args = parser.parse_args()
    data_path = ROOT / "data" / f"volume{args.volume}.json"

    with data_path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    errors: list[str] = []
    warnings: list[str] = []

    required_meta = {"series", "volume", "title", "author", "schemaVersion"}
    for key in required_meta:
        if not data.get("meta", {}).get(key):
            errors.append(f"meta.{key} is missing")

    speaker_names = {speaker["name"] for speaker in data.get("speakers", [])}
    block_ids: set[str] = set()
    type_counts: Counter[str] = Counter()
    speech_count = 0
    attributed_count = 0
    embedded_count = 0
    speaker_counts: Counter[str] = Counter()

    for chapter in data.get("chapters", []):
        for key in ("id", "number", "title", "pov", "scenes"):
            if key not in chapter:
                errors.append(f"chapter missing {key}: {chapter.get('id')}")

        seen_source_indices: dict[int, str] = {}

        for scene in chapter.get("scenes", []):
            if not scene.get("location"):
                errors.append(f"{scene.get('id')}: missing location")
            if not scene.get("cast"):
                errors.append(f"{scene.get('id')}: missing cast")
            if scene.get("pov") not in scene.get("cast", []):
                errors.append(f"{scene.get('id')}: POV is not in cast")

            for block in scene.get("blocks", []):
                block_id = block.get("id")
                if not block_id:
                    errors.append(f"{scene.get('id')}: block without id")
                    continue
                if block_id in block_ids:
                    errors.append(f"duplicate block id: {block_id}")
                block_ids.add(block_id)

                source_index = block.get("sourceIndex")
                if source_index in seen_source_indices:
                    warnings.append(
                        f"duplicate sourceIndex {source_index}: "
                        f"{seen_source_indices[source_index]} and {block_id}"
                    )
                elif isinstance(source_index, int):
                    seen_source_indices[source_index] = block_id

                block_type = block.get("type")
                type_counts[block_type] += 1

                if block_type not in {"spacer", "image"} and not block.get("text"):
                    errors.append(f"{block_id}: empty text")

                if block.get("embeddedDialogue"):
                    embedded_count += 1

                if block_type == "speech":
                    speech_count += 1
                    speaker = block.get("speaker")
                    if not speaker:
                        errors.append(f"{block_id}: speech without speaker")
                    else:
                        attributed_count += 1
                        speaker_counts[speaker] += 1
                        if speaker not in speaker_names:
                            errors.append(
                                f"{block_id}: speaker not in speaker index: {speaker}"
                            )
                        if (
                            speaker not in scene.get("cast", [])
                            and not block.get("recollection")
                            and not block.get("imagined")
                        ):
                            errors.append(
                                f"{block_id}: speaker {speaker} not in cast "
                                f"for {scene.get('id')}"
                            )
                        if block.get("speakerConfidence") not in {
                            "high",
                            "medium",
                            "low",
                        }:
                            errors.append(
                                f"{block_id}: invalid speakerConfidence"
                            )

                if block_type in {"quotation", "thought", "narration"} and block.get(
                    "speaker"
                ):
                    if block.get("speaker") not in speaker_names:
                        warnings.append(
                            f"{block_id}: mixed-block speaker not indexed: "
                            f"{block.get('speaker')}"
                        )
                    if block.get("embeddedDialogue"):
                        if (
                            block["speaker"] not in scene.get("cast", [])
                            and not block.get("recollection")
                            and not block.get("imagined")
                        ):
                            errors.append(
                                f"{block_id}: embedded speaker "
                                f"{block['speaker']} not in cast for "
                                f"{scene.get('id')}"
                            )

        chapter_speech = sum(
            1
            for scene in chapter["scenes"]
            for block in scene["blocks"]
            if block["type"] == "speech"
        )
        if chapter.get("speechCount") != chapter_speech:
            errors.append(f"{chapter.get('id')}: speechCount mismatch")

        chapter_speakers = {
            block["speaker"]
            for scene in chapter["scenes"]
            for block in scene["blocks"]
            if block["type"] == "speech"
            and block.get("speaker")
            and not block.get("recollection")
            and not block.get("imagined")
        }
        if set(chapter.get("speakers", [])) != chapter_speakers:
            errors.append(f"{chapter.get('id')}: chapter speakers mismatch")
        missing_cast = chapter_speakers - set(chapter.get("cast", []))
        if missing_cast:
            errors.append(
                f"{chapter.get('id')}: speakers missing from chapter cast: "
                f"{sorted(missing_cast)}"
            )

    if data.get("stats", {}).get("blockTypes") != dict(sorted(type_counts.items())):
        errors.append("stats.blockTypes does not match actual block counts")
    if data.get("stats", {}).get("speechBlocks") != speech_count:
        errors.append("stats.speechBlocks mismatch")
    if data.get("stats", {}).get("attributedSpeech") != attributed_count:
        errors.append("stats.attributedSpeech mismatch")
    if data.get("stats", {}).get("embeddedDialogueBlocks") != embedded_count:
        errors.append("stats.embeddedDialogueBlocks mismatch")

    indexed_counts = {
        speaker["name"]: speaker["lines"] for speaker in data.get("speakers", [])
    }
    if indexed_counts != dict(speaker_counts):
        errors.append("speaker index line counts do not match actual dialogue")

    print(f"Blocks: {len(block_ids)}")
    print(f"Speech: {speech_count} | attributed: {attributed_count}")
    print(f"Embedded dialogue annotations: {embedded_count}")
    print(f"Speakers: {len(speaker_names)}")
    print(f"Types: {dict(sorted(type_counts.items()))}")
    if warnings:
        print(f"Warnings: {len(warnings)}")
        for warning in warnings[:20]:
            print("  -", warning)
    if errors:
        print(f"ERRORS: {len(errors)}")
        for error in errors[:80]:
            print("  -", error)
        raise SystemExit(1)
    print("Validation passed.")


if __name__ == "__main__":
    main()
