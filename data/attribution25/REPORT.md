# Volume 25 — Speaker Attribution Report

Scope: `data/attribution25/ch01.json` … `ch11.json` plus `data/scene_metadata25.json`
(Volume 25 of the English edition: the last battle of the war — Alexander against
Rudeus — and the two interludes).

## Coverage

| Item | Count |
| --- | --- |
| Classified speech blocks | 845 |
| Attributed speech blocks | 845 (100%) |
| Missing attributions | 0 |
| Blocks with no `speaker` | 0 |
| Scenes with location + cast | 41 |
| Distinct speakers in the built volume | 22 |
| Blocks mixing narration and dialogue (`mixed`) | 263 |
| Narration blocks flagged with `embeddedDialogue` | 22 |
| Blocks re-typed away from `speech` | 3 |

Checks:

```
python3 scripts/check_attribution.py --volume 25   # "Attributed: 845", no missing
python3 scripts/make_scene_metadata.py --volume 25 --file /tmp/vol25-scenes.json
python3 scripts/build.py --volume 25                # 11 chapters | speech 842 | attributed 842
python3 scripts/validate.py --volume 25             # "Validation passed."
```

`check_attribution.py` lists 22 “extra” keys: those are the narration blocks that
carry quoted dialogue and are annotated with `embeddedDialogue` (see below), which
the script counts as unknown because the classifier did not type them as speech.

The built volume reports 842 speech blocks because three blocks that the classifier
marked as `speech` were re-typed (see *Type corrections*). All 845 originally
classified speech blocks still carry a speaker in the attribution files.

## Top speakers

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 200 | Dohga | 20 |
| Sandor | 153 | Ogre God Marta | 16 |
| Alexander | 95 | Zanoba | 9 |
| Badigadi | 86 | Informant | 7 |
| Geese | 60 | Orsted | 5 |
| Eris | 50 | Norn | 4 |
| Gall Falion | 35 | Superd Warrior | 4 |
| Atofe | 32 | Elinalise | 3 |
| Ruijerd | 32 | Knight | 2 |
| Perugius | 25 | Laplace | 2 |
| | | Cliff | 1 |
| | | Labyrinth Guardian | 1 |

## Conventions

* **Canonical names** are used throughout: `Rudeus` (never Rudy), `Sylphiette`
  (never Sylphie). In-world names are kept as the book spells them — `Ruijerd`,
  `Badigadi`, `Atofe`, `Gall Falion`, `Kalman`, `Geese`, `Dohga`, `Zanoba`, `Norn`.
* **Two North Gods, two labels.** The book calls the son `Alexander Rybak`
  (North God Kalman III) and the father `Alex Rybak` (North God Kalman II), who
  goes by the cover name `Sandor von Grandour`. The son is labelled **Alexander**
  (the text also calls him “Alec”), the father **Sandor**, so that the reader sees
  one consistent name for each man across both final volumes.
* **The Man-God is `Perugius`** (25 lines: his taunts in Rudeus’s white space in
  ch02 and the dream conversation with Badigadi in ch10).
* **Generic labels** are used only where the text does not name the speaker, and
  they stay consistent across the volume:
  * `Informant` — the boy in the tavern in ch01 who is Geese's paid source.
  * `Knight` — the two Biheiril Kingdom knights held in the Superd village (ch09).
  * `Superd Warrior` — the unnamed Superd warriors who report and carry messages
    (ch03, ch05).
  * `Labyrinth Guardian` — the headless Dullahan who guards the Devil’s Cave
    (ch10); the text refuses to name him.
  * `Laplace` — appears only in the two lines of the recollection inside Ruijerd's
    account of the Laplace War (ch08); both are flagged `recollection`.
* **Battle cries and vocalisations** belong to the fighter who shouts them
  (“Gaaaah!”, “Tch-hah.”, “Rroooaaaah!”). Where the text does not make the
  speaker certain — mostly a scream during a crowded fight — the line is marked
  `medium` confidence and explained in the note.
* **`mixed: true`** marks a block that contains narration/action around the
  quoted line (263 blocks). The speaker is still the one who speaks.
* **`embeddedDialogue: true`** marks a *narration* block that contains a quoted
  live line (22 blocks), so that no line of dialogue is left unattributed.
* **`recollection: true`** marks remembered or recounted speech (ch03 `ch03-p0052`,
  ch08 `ch08-p0003`/`ch08-p0005`, ch11 `ch11-p0002`/`ch11-p0004`).
* **Point of view.** Four chapters are not narrated by Rudeus, and the scene
  metadata corrects them: ch01 is **Sandor** (he receives the rumours, goes to the
  Superd village and organises the search party), ch04 is **Eris** (her duel with
  Gall Falion), ch10 is **Badigadi** (the interlude about the armor, narrated by
  the Wise Demon King himself), ch11 is **Alexander** (the Third North God Kalman
  reflecting while buried). ch10's narrator is identified as Badigadi from the
  text itself: Atofe is “my older sister”, Kishirika is the woman he was engaged
  to, and he is the one who killed Laplace in the Fighting God Armor.
* **Names in the text that are not the label.** The text calls the son “Alec” and
  the father “Alex”; both keep their own label. The reader still sees the book's
  wording inside the line itself.

## Type corrections

Three blocks were misclassified by the automated classifier; each carries a `type`
override and an explanatory `note`:

- `ch03-p0080` → `narration` (Rudeus narrating Zanoba's snort; no dialogue).
- `ch05-p0071` → `narration` (Rudeus narrating Alexander's loss of patience; no
  dialogue).
- `ch08-p0178` → `thought` (Rudeus's inner aside, “Sorry, I shouldn't have laughed…”).

First-person inner monologue that the classifier typed as speech is re-typed
`thought` so the reader still knows whose thought it is; third-person narration
without any dialogue is re-typed `narration`. Both keep their speaker.

## Narration blocks with quoted dialogue (22)

`ch01-p0031`, `ch01-p0054`, `ch02-p0168`, `ch03-p0052`, `ch03-p0065`, `ch03-p0094`,
`ch03-p0158`, `ch03-p0166`, `ch04-p0019`, `ch05-p0030`, `ch05-p0034`, `ch05-p0057`,
`ch06-p0116`, `ch08-p0003`, `ch08-p0005`, `ch08-p0088`, `ch09-p0173`, `ch10-p0037`,
`ch10-p0112`, `ch10-p0154`, `ch11-p0002`, `ch11-p0004`.

## Medium- and low-confidence labels

22 blocks are marked `medium`; none are `low`. Each one is a line whose speaker is
not named in the text.

- `ch03-p0021` — “…By the way, what's with the arm?” Eris and Roxy are both
  candidates; Eris is the likelier (she is staring at his arm a few lines later).
- `ch03-p0133` — “Aaahh!” as the bridge falls; attributed to Alexander, who is
  plunged into the ravine.
- `ch03-p0171` — “Ruooaaaah!!!”; the charge cry of the battle that starts the
  next paragraph, attributed to Alexander.
- `ch04-p0059` — “Gyaaaaah!” as Gall Falion's strike is blocked from behind.
- `ch05-p0107` — “…Hmph.” after Sandor shoulders Alexander aside.
- `ch05-p0123` — “Uuah!” and `ch05-p0124` — “Grrryaah!”, the two cries of the
  renewed exchange between Sandor and Alexander; split between the two fighters.
- `ch05-p0134` — “Gaaagh!” just before Eris and Ruijerd arrive.
- `ch05-p0212` — “Rudeus…!” as Rudeus reaches the magic circle; Elinalise.
- `ch06-p0042`, `ch06-p0057`, `ch06-p0178` — “Ngh…!”, “Ouf!” and “Gah!” in the
  four-on-one fight; attributed to Alexander.
- `ch06-p0121` — “Right, our enemy is alone!” after the Ogre God withdraws; given
  to Rudeus, the tactical voice of the scene.
- `ch06-p0145` — “That's right! Now accept your death quietly!”; given to Sandor
  continuing his own demand, though Rudeus could be backing him up.
- `ch07-p0007`, `ch07-p0011`, `ch07-p0084` — “Whooooooa!”, “Graaah!” and
  “Gr…raaaaah!” during the fall; given to Rudeus, who is doing the shouting and
  the punching.
- `ch08-p0032` — “Ah!” when Eris's sword is caught at the hilt; given to Sandor.
- `ch08-p0086` — “Gaaaah!” during the mock fight; given to Eris.
- `ch08-p0218` — “Nngh…uhh…” as Sandor talks his mother down; given to Atofe.
- `ch09-p0003` — the envoy's report of the king's answer; given to Cliff, who led
  the mission to the Second City.
- `ch09-p0039` — “…Hey, Rudeus. Can you see them?” on the lighthouse; given to
  Eris, who is keeping watch with him.

## Notes per chapter

- **ch01** — Sandor, not Rudeus. The whole chapter is Sandor's errand: the
  informant's rumours about the “monkey-faced demon” (Rudeus), the broken
  communication tablet, the empty teleportation circle, the search party with
  Ruijerd and Norn.
- **ch02** — Rudeus's soul wakes in the Man-God's white space. Perugius is the
  one who says “Go die in a hole” (ch02-p0012); Rudeus's reply, “Already did,” is
  narration and is not attributed. The rest is Rudeus and Dohga in the ravine.
- **ch03** — the great hall and the bridge. `ch03-p0033` is the boy in the tavern
  (Geese's source), `ch03-p0110` is the Superd warrior who reports the hunting
  party. The Sword God is `Gall Falion`, the third North God is `Alexander`.
- **ch04** — Eris's chapter, entirely from her point of view. The only other
  voices are Gall Falion and, at the very end, Ruijerd.
- **ch05** — Rudeus against Alexander, with Sandor. `ch05-p0033` is Rudeus
  mimicking Badigadi's laugh; the man who answers with “Fwahahaha! Futile, all
  futile!” is Badigadi.
- **ch06** — the second round against Alexander, then Atofe's arrival. The Ogre
  God speaks in halting human tongue; Atofe speaks in demon tongue.
- **ch07** — the fall into the ravine and the end of Alexander. `ch07-p0131`
  carries Sandor's shouted “Now!”; `ch07-p0157` and `ch07-p0164` are Alexander's
  cries.
- **ch08** — the quiet after the battle. `ch08-p0088` holds Eris's remark after
  the mock duel; `ch08-p0163`/`ch08-p0164` are Laplace's dying words inside
  Ruijerd's recollection and are flagged `recollection`.
- **ch09** — the peace with the Ogre God. The Ogre God is `Ogre God Marta`
  throughout; the knights captured at the bridge are `Knight`.
- **ch10** — the interlude, narrated by Badigadi (the Wise Demon King) with
  Geese on his shoulder, from the mouth of the Devil's Cave to the throne room
  where the Fighting God Armor waits, and finally Perugius's visit to his dreams.
- **ch11** — the interlude is Alexander's, buried under the rubble of the ravine
  and reflecting on what a hero is. `ch11-p0002` and `ch11-p0004` are Paul
  Greyrat's recounted words.
