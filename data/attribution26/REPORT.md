# Volume 26 — Speaker Attribution Report

Scope: `data/attribution26/ch01.json` … `ch10.json` plus `data/scene_metadata26.json`
(Volume 26 of the English edition: the threat of the Fighting God, the last battle,
the three closing stories, the Asuran dossier, the afterword and the epilogue).

## Coverage

| Item | Count |
| --- | --- |
| Classified speech blocks | 623 |
| Attributed speech blocks | 623 (100%) |
| Missing attributions | 0 |
| Blocks with no `speaker` | 0 |
| Scenes with location + cast | 35 |
| Distinct speakers in the built volume | 29 (+2 in quoted documents) |
| Blocks mixing narration and dialogue (`mixed`) | 194 |
| Narration blocks flagged with `embeddedDialogue` | 9 |
| Blocks re-typed away from `speech` | 8 |

Checks:

```
python3 scripts/check_attribution.py --volume 26   # "Attributed: 623", no missing
python3 scripts/make_scene_metadata.py --volume 26 --file /tmp/vol26-scenes.json
python3 scripts/build.py --volume 26                # 10 chapters | speech 615 | attributed 615
python3 scripts/validate.py --volume 26             # "Validation passed."
```

`check_attribution.py` lists 8 “extra” keys: the narration blocks that contain
quoted dialogue and are annotated with `embeddedDialogue`.

The built volume reports 615 speech blocks because eight blocks that the
classifier marked as `speech` were re-typed (see *Type corrections*). All 623
originally classified speech blocks still carry a speaker in the attribution files.

## Top speakers

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 258 | Dohga | 3 |
| Badigadi | 55 | Feris | 3 |
| Orsted | 54 | Lucie | 3 |
| Perugius | 32 | Norn | 3 |
| Alexander | 28 | Priest | 3 |
| Sylphiette | 24 | Isolde | 2 |
| Geese | 23 | Zanoba | 2 |
| Sandor | 23 | Julie | 1 |
| Eris | 19 | Leo | 1 |
| Ruijerd | 19 | Mage Knight | 1 |
| Cliff | 9 | | |
| Ghislaine | 8 | | |
| Lilia | 8 | | |
| Shinohara Akito | 8 | | |
| Atofe | 6 | | |
| Aisha | 5 | | |
| Lyria | 5 | | |
| Roxy | 5 | | |
| Lara | 4 | | |

Two further names appear only in quoted documents and therefore carry no line
count: `Archivist` (the three anecdotes in the Asuran dossier) and `Ariel` (the
sentence she said to Luke, quoted in the same dossier).

## Conventions

* **Canonical names** are used throughout: `Rudeus` (never Rudy), `Sylphiette`
  (never Sylphie). In-world names are kept as the book spells them — `Ariel`,
  `Orsted`, `Perugius`, `Badigadi`, `Geese`, `Ruijerd`, `Atofe`, `Alexander`,
  `Ghislaine`, `Isolde`, `Dohga`, `Zanoba`, `Aisha`, `Norn`, `Cliff`, `Elinalise`.
* **North God Kalman II is `Sandor`.** The volume config calls him “Alex Rybak”
  and the chapter is headed “Sandor”; he is the same man as the `Sandor` of
  volume 25 (the text: “Sandor von Grandour, the cover name of Alex Rybak”), so
  one label is used for him in both volumes. The scene cast list of ch01 also
  contains the alias “Alex Rybak”, because the scene-metadata helper always adds
  the classifier's own scene-POV string.
* **North God Kalman III is `Alexander`** (“Alec” in the text).
* **The Man-God is `Perugius`** (32 lines: the white-space scenes in ch05 and ch07).
* **Generic labels** are used only where the text does not name the speaker:
  * `Priest` — the hooded magicians who run the summoning ritual in the
    epilogue (ch10).
  * `Mage Knight` — the bodyguard knight who explains the world to the girl in
    the epilogue; the text never names him.
  * `Archivist` — the Asuran dossier that frames the three anecdotes of ch08.
  * `Shinohara Akito` and `Lyria` are named by the characters themselves, so they
    are not generic labels; the girl is called “Lilia” in the text after the boy
    mishears her name, and `ch10-p0052` carries a note about that.
* **Battle cries and vocalisations** belong to the fighter who shouts them
  (“Gyaaaah!”, “Shotgun Trigger!”, “Gaaaah!”).
* **`mixed: true`** marks a block that contains narration/action around the
  quoted line (194 blocks). The speaker is still the one who speaks.
* **`embeddedDialogue: true`** marks a *narration* block that contains a quoted
  live line (9 blocks), so that no line of dialogue is left unattributed.
* **`recollection: true`** marks recounted speech: the Aisha/Perugius story
  Rudeus retells in ch04 (`ch04-p0015`, `ch04-p0019`, `ch04-p0020`).
* **Point of view.** ch01 is narrated by **Sandor** (North God Kalman II), not by
  Rudeus, and the scene metadata says so for the whole chapter. `ch01-s04` opens
  in Sandor's voice and switches to Rudeus at the “Rudeus” header halfway
  through; because most of the scene is Rudeus's, that single scene is marked
  `pov: Rudeus` while the chapter keeps `chapterPov: Sandor`. The remaining
  chapters are Rudeus's, including the three closing stories, the dossier, the
  afterword and the epilogue.
* **Documents.** The appendix (ch08), the afterword (ch09) and the epilogue (ch10)
  are not scenes in the story sense; they are still given a location and a cast
  (the Royal Asuran Archive, Rudeus's diary, the kingdom's palace and the
  Citadel of Roa) so the reader can place them.

## Type corrections

Eight blocks were misclassified by the automated classifier; each carries a `type`
override and an explanatory `note`:

- `ch01-p0015` → `thought` (Sandor's inner narration; the quoted “No.” is not
  spoken aloud).
- `ch01-p0109` → `thought` (Sandor's inner narration; “Now!” and “On my word!”
  are words he did *not* say).
- `ch03-p0197` → `thought` (Rudeus recognising Alexander's voice; no dialogue).
- `ch08-p0126`, `ch08-p0127`, `ch08-p0128` → `quotation` (anecdotes quoted in the
  Asuran dossier, spoken by no one in the story).
- `ch08-p0161` → `quotation` (Ariel's words to Luke, quoted from the Chronicle).
- `ch09-p0036` → `quotation` (Rudeus's written diary line, not spoken aloud).

Inner monologue typed as speech is re-typed `thought`; written or quoted passages
typed as speech are re-typed `quotation`. Both keep their speaker, so the reader
still knows whose words they are.

## Narration blocks with quoted dialogue (9)

`ch01-p0128`, `ch02-p0153`, `ch03-p0151`, `ch03-p0250`, `ch04-p0094`, `ch04-p0118`,
`ch04-p0309`, `ch05-p0102`, `ch05-p0123`.

## Medium- and low-confidence labels

Six blocks are marked `medium`; none are `low`.

- `ch01-p0082` — “Sandor!” shouted by the arriving party; given to Eris, who
  calls out in the next chapter.
- `ch02-p0140` — “Hmph!” as the Fighting God's fist comes down; the speaker is the
  long-skirted rescuer straddling Rudeus, i.e. Isolde (Ghislaine is the wolf that
  cut the god's legs).
- `ch02-p0148` — “Big Brother!” and `ch02-p0150` — “Oh, Big Bro…”, the two calls
  from the girls Rudeus walks past; Norn and Julie both call him that, so the
  first is given to Norn and the second to Julie.
- `ch03-p0033` — “Fwahahaha! Payback time!”; Rudeus mimicking Badigadi's laugh
  after the shotgun blast.
- `ch03-p0181` — “Yeah.” answering Rudeus's “Let's go home.”; given to Ghislaine,
  who is the closest companion at that moment.

## Notes per chapter

- **ch01** — Sandor's point of view. The Fighting God is `Badigadi` (the book also
  calls him the Wise Demon King, and Atofe his “moron brother”); `Geese` rides on
  his shoulder. `ch01-p0068` is Atofe arriving with a roar, and the exchange
  between the two demon siblings runs `Badigadi` → `Atofe` → `Badigadi` →
  `Geese` → `Badigadi` → `Atofe`.
- **ch02** — the four days of buying time. The wall-watching, the bait of Geese's
  body and the duel with Badigadi are all Rudeus's. `ch02-p0140` aside, the
  rescuers are `Ghislaine` and `Isolde`; `ch02-p0149` (“Grand Master!”) is
  Aisha.
- **ch03** — the duel with the Fighting God, Geese's death in the burnt forest
  and Orsted's intervention. `ch03-p0163`–`ch03-p0171` are Geese and Ghislaine
  trading their last words, and `ch03-p0180`–`ch03-p0181` close the scene.
- **ch04** — the month after the battle: the rebuilt village, the farewells to
  Sandor, Ghislaine, Dohga and Isolde, the sealing of Badigadi at the bottom of
  the ravine, and the return home. `ch04-p0293` holds both Lilia's greeting and
  Rudeus's reply and is labelled Lilia with a note.
- **ch05** — Story 1: Rudeus's dream of the sealed Man-God and his death at
  seventy-four. `Feris` is the great-granddaughter who takes the Dragon God's
  bracelet; `Sylphiette` and `Roxy` are the white-haired women at his bedside.
- **ch06** — Story 2: Rudeus at thirty-four, at his own grave and at Paul's.
  `Lara` is the daughter with blue hair who takes the bracelet.
- **ch07** — Story 3: Rudeus's soul meets the Man-God again, forty years after the
  dream of ch05, and walks away.
- **ch08** — the Asuran dossier. It contains no live dialogue: the three anecdotes
  are `Archivist` quotations and Ariel's line to Luke is quoted from the Chronicle.
- **ch09** — the afterword from *The Book of Rudeus*. The single attributed line
  is Rudeus's written advice to whoever decodes his diary.
- **ch10** — the epilogue, “Prologue Zero”. The boy from another world names
  himself `Shinohara Akito`; the Blessed Child of Restoration names herself
  `Lyria` (the boy mishears it as “Lilia”). The hooded magicians are `Priest`
  and the bodyguard is `Mage Knight`.
