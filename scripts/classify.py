#!/usr/bin/env python3
"""First-pass block classification for a Mushoku Tensei volume.

Usage:
    python3 scripts/classify.py --volume 16

This marks diary, letter, inscription, silence and speech blocks. Speaker names are
left empty; attribution is applied in a later pass.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from volumes import get_volume

ROOT = Path(__file__).resolve().parents[1]

SPEECH_VERBS = re.compile(
    r"\b(said|says|asked|asks|replied|replies|answered|answers|muttered|murmured|"
    r"shouted|yelled|called|cried|whispered|added|continued|began|exclaimed|snapped|"
    r"hissed|growled|laughed|sighed|agreed|protested|interjected|prompted|observed|"
    r"remarked|responded|retorted|spat|barked|screamed|wailed|groaned|mumbled|"
    r"stammered|declared|announced|insisted|admitted|wondered|repeated|corrected|"
    r"teased|joked|warned|pleaded|begged|urged|suggested|explained|informed|noted|"
    r"snorted|huffed|puffed|whisper|mutter|murmur|reply|answer)\b",
    re.I,
)

NAME_PATTERN = re.compile(
    r"\b(Rudeus|Rudy|Sylphie|Sylphiette|Roxy|Eris|Nanahoshi|Orsted|Ghislaine|"
    r"Nina|Isolde|Reida|Ariel|Zanoba|Cliff|Elinalise|Aisha|Norn|Lilia|Zenith|"
    r"Lucie|Perugius|Arumanfi|Luke|Man-God|Hitogami|Gall|Gino|Georg|Sara|"
    r"Pilemon|Atofe|Moore|Sylvaril|Ariel|Grabel|Darius|Cleane|Lienhard|"
    r"Gertrude|Ruquag|Tal-Chi)\b",
    re.I,
)


def in_ranges(pid: str, ranges: list[tuple[str, str]]) -> bool:
    for start, end in ranges:
        if start <= pid <= end:
            return True
    return False


def strip_quotes(text: str) -> str:
    return text.strip().strip("“”\"").strip()


def is_silence(text: str) -> bool:
    inner = strip_quotes(text)
    return inner in {"…", "...", "……", "..", "…!", "…?"}


def has_dialogue_quote(text: str) -> bool:
    return bool(re.search(r"“[^”]+”", text))


def classify(text: str, starts_quote: bool) -> str:
    if is_silence(text):
        return "silence"
    if starts_quote:
        return "speech"
    if has_dialogue_quote(text):
        outside = re.sub(r"“[^”]*”", "", text)
        if SPEECH_VERBS.search(outside) or NAME_PATTERN.search(outside):
            if len(outside.split()) <= 35:
                return "speech"
    return "narration"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=15)
    args = parser.parse_args()
    config = get_volume(args.volume)

    source_path = ROOT / "data" / f"volume{config['number']}.source.json"
    output_path = ROOT / "data" / f"volume{config['number']}.classified.json"
    data = json.loads(source_path.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}

    for chapter in data["chapters"]:
        cid = chapter["id"]
        diary_ranges = config.get("diary_ranges", {}).get(cid, [])
        letter_ranges = config.get("letter_ranges", {}).get(cid, [])
        chapter_kind = chapter.get("kind", "main")
        for scene in chapter["scenes"]:
            for block in scene["blocks"]:
                if block["type"] == "spacer":
                    continue
                pid = block["id"]
                text = block["text"]
                block["type"] = "narration"
                block.pop("speaker", None)

                if chapter_kind == "diary":
                    block["type"] = "diary"
                    block["author"] = "Rudeus"
                    block.pop("italic", None)
                    counts["diary"] = counts.get("diary", 0) + 1
                    continue

                if in_ranges(pid, diary_ranges) and block.get("italic"):
                    block["type"] = "diary"
                    block["author"] = "Future Rudeus"
                    block.pop("italic", None)
                    counts["diary"] = counts.get("diary", 0) + 1
                    continue

                letter_hit = None
                for start, end, author, recipient, part in letter_ranges:
                    if start <= pid <= end:
                        letter_hit = (author, recipient, part)
                        break
                if letter_hit:
                    block["type"] = "letter"
                    block["author"], block["recipient"], block["letterPart"] = letter_hit
                    counts["letter"] = counts.get("letter", 0) + 1
                    continue

                if pid in config.get("inscriptions", set()):
                    block["type"] = "inscription"
                    counts["inscription"] = counts.get("inscription", 0) + 1
                    continue

                kind = classify(text, text.startswith(("“", '"')))
                block["type"] = kind
                counts[kind] = counts.get(kind, 0) + 1

    data["stats"]["blockTypes"] = counts
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
