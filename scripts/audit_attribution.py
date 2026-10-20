#!/usr/bin/env python3
"""Flag attribution entries that look inconsistent with their own text.

Usage:
    python3 scripts/audit_attribution.py --volume 16
    python3 scripts/audit_attribution.py --volume 16 --chapter ch03

Heuristics:
  * a quote followed by "said NAME" / "NAME said" that names somebody else
  * "I said" / "I asked" / "I replied" spoken by somebody other than the POV
  * "NAME," NAME said - a speech tag naming a different speaker
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIRST_PERSON = re.compile(
    r"\bI (said|asked|replied|answered|murmured|muttered|whispered|shouted|"
    r"cried|exclaimed|added|continued|began|laughed|sighed|agreed|protested|"
    r"interjected|prompted|observed|remarked|responded|retorted|declared|"
    r"announced|insisted|admitted|wondered|repeated|corrected|teased|joked|"
    r"warned|pleaded|begged|urged|suggested|explained|informed|noted)\b"
)

SAID_TAG = re.compile(
    r"[“\"](?P<quote>.+?)[”\"]\s*,?\s*(?:said|asked|replied|answered|muttered|"
    r"murmured|whispered|shouted|yelled|cried|added|continued|began|exclaimed|"
    r"snapped|hissed|growled|laughed|sighed|agreed|protested|interjected|"
    r"prompted|observed|remarked|responded|retorted|declared|announced|insisted|"
    r"admitted|wondered|repeated|corrected|teased|joked|warned|pleaded|begged|"
    r"urged|suggested|explained|informed|noted)\s+(?P<name>[A-Z][\w'’\-]*)"
)

NAMED_TAG = re.compile(
    r"\b(?P<name>[A-Z][\w'’\-]{1,})\s+(said|asked|replied|answered|muttered|"
    r"murmured|whispered|shouted|yelled|cried|added|continued|began|exclaimed|"
    r"snapped|hissed|growled|laughed|sighed|agreed|protested|interjected|"
    r"prompted|observed|remarked|responded|retorted|declared|announced|insisted|"
    r"admitted|wondered|repeated|corrected|teased|joked|warned|pleaded|begged|"
    r"urged|suggested|explained|informed|noted)\b"
)

NARRATOR_TAGS = {"narrator", "author", "unknown"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, required=True)
    parser.add_argument("--chapter")
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "data" / f"volume{args.volume}.classified.json").read_text(
            encoding="utf-8"
        )
    )
    attribution: dict = {}
    for path in sorted(
        (ROOT / "data" / f"attribution{args.volume}").glob("ch*.json")
    ):
        attribution.update(json.loads(path.read_text(encoding="utf-8")))

    flagged = 0
    for chapter in data["chapters"]:
        if args.chapter and chapter["id"] != args.chapter:
            continue
        for scene in chapter["scenes"]:
            for block in scene["blocks"]:
                if block["type"] != "speech":
                    continue
                entry = attribution.get(block["id"])
                if not entry or not entry.get("speaker"):
                    continue
                speaker = entry["speaker"]
                text = block["text"]
                problems = []

                match = SAID_TAG.search(text)
                if match:
                    name = match.group("name")
                    if name not in {speaker, "he", "she", "it"} and name != speaker:
                        problems.append(f"tag says {name}")

                match = NAMED_TAG.search(text)
                if match:
                    name = match.group("name")
                    if name != speaker and name not in NARRATOR_TAGS:
                        problems.append(f"named {name}")

                if FIRST_PERSON.search(text) and speaker != scene["pov"]:
                    problems.append("first-person line not by POV")

                if problems:
                    flagged += 1
                    print(
                        f"{block['id']} | {speaker} | {', '.join(problems)}\n"
                        f"    {text[:220]}"
                    )

    print(f"\nFlagged {flagged} suspicious blocks")


if __name__ == "__main__":
    main()
