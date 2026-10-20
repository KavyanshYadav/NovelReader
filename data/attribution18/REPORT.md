# Volume 18 — Speaker Attribution Report

Chapter: *Mushoku Tensei* Volume 18 (ch00–ch12), reader data set `data/volume18.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 13 (ch00–ch12) |
| Scenes | 29 |
| Blocks total | 2,461 (82 diary, 1,124 narration, 67 spacer, 1,188 speech) |
| Speech blocks | 1,188 |
| Attributed speech blocks | 1,188 (100.0%) |
| Distinct speakers | 44 |
| `mixed` blocks | 17 |
| `recollection` blocks | 7 |
| `imagined` blocks | 0 |
| `type` overrides | 0 (the classifier's typing was correct everywhere) |
| Blocks carrying a `note` | 51 |

Validation status:

```
python3 scripts/check_attribution.py --volume 18   -> Attribution coverage complete.
python3 scripts/build.py --volume 18                -> wrote data/volume18.json
python3 scripts/validate.py --volume 18            -> Validation passed.
```

## Top speakers (volume)

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 359 | Beastman | 25 |
| Linia | 111 | Lilia | 21 |
| Zanoba | 81 | Orsted | 21 |
| Aisha | 64 | Lienhard | 18 |
| Cliff | 36 | Roxy | 17 |
| Angie | 34 | Julie | 14 |
| Norn | 34 | Perugius | 14 |
| Eris | 33 | Pham | 13 |
| Student | 33 | Rayfort | 13 |
| Belfried | 30 | Leo | 12 |
| Gyes | 30 | Mi'nal | 11 |
| Kincho | 30 | Ruquag Mire | 11 |
| Sylphiette | 28 | Minitona | 8 |
| Pursena | 27 | Grannel | 6 |

## Chapter 08 — "Revisiting the Doldia Village" (this run)

| Metric | Value |
| --- | --- |
| Scenes | 4 (ch08-s01 … ch08-s04) |
| Speech blocks | 139 |
| Attributed | 139 (100%) |
| Distinct speakers | 11 |
| `mixed` blocks | 14 |
| `note` blocks | 25 |

Speakers in ch08: Rudeus 29, Linia 24, Gyes 24, Beastman 18, Perugius 14, Leo 11,
Minitona 8, Tersena 4, Pursena 3, Sylvaril 2, Nanahoshi 2.

Scene map:

| Scene | Location | Cast |
| --- | --- | --- |
| ch08-s01 | Rudeus's home in Sharia, before the trip to the Great Forest | Rudeus, Eris, Leo, Linia |
| ch08-s02 | Nanahoshi's floating fortress: Perugius's hall, guest room, and the basement teleportation room | Rudeus, Perugius, Sylvaril, Nanahoshi, Linia, Leo, Yuzuru |
| ch08-s03 | The flooded teleportation ruins and the Doldia Village in the Great Forest | Rudeus, Linia, Leo, Beastman, Minitona, Tersena, Gyes |
| ch08-s04 | The village jail, Doldia Village | Rudeus, Gyes, Pursena, Linia |

## Uncertainty ledger

No `low`-confidence labels are used anywhere in the volume. All 11 flagged
entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch01-p0093 | Rudeus | Rudeus speaks; the surrounding narration is in Angie's viewpoint. |
| ch02-p0031 | Sylphiette | Startled cry as Rudeus embraces her; speaker inferred. |
| ch03-p0135 | Mi'nal | Surprised reply to Rayfort. |
| ch03-p0137 | Mi'nal | Agreeing with Rayfort. |
| ch03-p0224 | Grannel | Response to Norn's welcome. |
| ch08-p0207 | Minitona | One of the two warriors chiming in; the speaker is not named. |
| ch08-p0211 | Rudeus | Stammered agreement to Gyes; read as Rudeus from the reaction that follows. |
| ch08-p0214 | Minitona | One of the two warriors questioning Gyes; the speaker is not named. |
| ch11-p0020 | Cliff | Remembered speech inside the Julie backstory. |
| ch11-p0022 | Zanoba | Remembered speech inside the Julie backstory. |
| ch11-p0032 | Zanoba | Remembered speech inside the Julie backstory. |

## Notes

* **Generic beastfolk = `Beastman`.** The Doldia villagers who heckle Linia at the
  village gate (ch08-p0120 … ch08-p0154, 18 blocks) are unnamed beastfolk and use
  the same generic label already used for the beastfolk in ch07-p0117–p0161, so the
  volume stays internally consistent. `Minitona` and `Tersena` are used for the two
  named warriors who appear in person; the text spells one of them "Tersuna" once
  (ch08-p0208) but "Tersena" everywhere else, and "Tersena" is used here.
* **Leo's barks.** Leo's "Woof!" lines are attributed to `Leo` with a note marking
  them as vocalizations rather than human speech. The five blocks where Linia
  supplies a translation in parentheses (ch08-p0184, p0186, p0191, p0193, p0195) are
  flagged `mixed`, with the translation attributed to Linia's interpretation.
* **Who answers Leo.** In the Gyes/Léo exchange (ch08-p0183–p0195), Leo asks the
  question in Woofenese and Gyes answers, matching the parallel structure of
  ch08-p0191→ch08-p0192. The translation parentheses are Linia's, not Leo's.
* **`ch08-p0185`** ("Our duty is to protect the Sacred Beast…") is Gyes answering
  Leo's question about the tribe's duty.
* **Unattributed warrior lines.** ch08-p0207 and ch08-p0214 are spoken by one of the
  two warriors behind Gyes; Minitona was chosen as the first-named of the pair and
  both are flagged `medium`. ch08-p0211 is read as Rudeus.
* **Narration that carries dialogue.** 14 ch08 blocks interleave narration and quoted
  speech (ch08-p0030, p0051, p0056, p0149, p0184, p0186, p0191, p0192, p0193, p0195,
  p0246, p0247, p0253, p0265) and are flagged `mixed` with a short note.
* **Scope of the attribution files.** Only blocks the classifier typed as `speech`
  are listed, matching the convention already used by ch00–ch07 and ch09–ch12 of this
  volume, so `check_attribution.py` reports complete coverage with no unknown keys.
* **Scene metadata.** `data/scene_metadata18.json` maps all 29 scene IDs to a
  `location` and a `cast`. Cast always includes the scene POV (Rudeus), every speaker
  attributed to that scene, and other characters present in it. The ch09 in-story
  headings are used as the location context for ch09-s02 ("First Witness Testimony"),
  ch09-s03 ("Second Witness Testimony") and ch09-s04 ("Watson's Input").
