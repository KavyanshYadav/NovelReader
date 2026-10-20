# Volume 22 — Speaker Attribution Report

*Coming Home and Making Reports* (ch01–ch05), the *Blue and Red* interlude (ch06),
*Infiltrating Fort Necross* (ch07–ch11), the *We Got Married* interlude (ch12),
*Number Four* (ch13) and the Geese extra chapter (ch14).
Reader data set: `data/volume22.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 14 (ch01–ch13 main/interlude, ch14 extra) |
| Scenes | 35 |
| Blocks total | 2,374 (988 narration, 1,337 speech, 49 spacer) |
| Speech blocks in the classified data | 1,342 |
| Attributed speech blocks | 1,342 (100.0%) |
| Speech blocks after seven re-typed narration blocks | 1,337 |
| Attributed after re-typing | 1,337 (100.0%) |
| Distinct speakers | 46 |
| `mixed` blocks | 222 |
| `embeddedDialogue` blocks | 34 |
| `recollection` blocks | 2 |
| `imagined` blocks | 1 |
| `type` overrides | 5 (all of them re-type a `speech` block as `narration`) |
| Blocks carrying a `note` | 47 |
| Medium / low confidence | 3 / 0 |

Validation status:

```
python3 scripts/check_attribution.py --volume 22   -> Attributed: 1342 (100%)
python3 scripts/make_scene_metadata.py --volume 22 --file /tmp/opencode/spec22-scenes.json
                                                     -> 35 scenes
python3 scripts/build.py --volume 22                -> Chapters: 14 | speech: 1337 | attributed: 1337 | speakers: 46
python3 scripts/validate.py --volume 22            -> Validation passed.
```

`check_attribution.py` also lists 28 "extra" keys. Those are the narration blocks
that carry quoted speech (and the blocks re-typed as narration); they are
deliberate entries, not mistakes.

`validate.py` prints one warning:

```
ch12-p0180: mixed-block speaker not indexed: Lara
```

Lara has no spoken line anywhere else in the volume, so she cannot appear in the
automatic speaker index; the warning is informational and the validation still
passes.

## Top speakers

Counts below are the line counts in the built reader
(`data/volume22.json` → `speakers`), i.e. speech blocks only.

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 377 | Dohga | 9 |
| Roxy | 119 | Sylvester Ifrit | 9 |
| Eris | 95 | Elinalise | 8 |
| Atofe | 83 | Lucie | 8 |
| Geese | 68 | Benedikte | 7 |
| Moore | 60 | Calina | 7 |
| Guard | 45 | Arcantos | 7 |
| Young Adventurer | 43 | Shagall Gargantis | 6 |
| Ariel | 38 | Norn | 5 |
| Randolph | 35 | Chandle | 5 |
| Vio Pompadour | 34 | Desert Warrior | 5 |
| Zanoba | 30 | Lady-in-Waiting | 4 |
| Kirkland von Kingdragon | 30 | Doctor | 4 |
| Sylphiette | 27 | Villager | 4 |
| Aisha | 24 | Leo | 2 |
| Rokari | 22 | Shirone Noble | 1 |
| Orsted | 21 | Herald | 1 |
| Lilia | 19 | Legend | 1 |
| Man-God | 17 | Demon King | 1 |
| Rowin | 15 | Lara | 1 |
| Secretary | 14 | Baby | 1 |
| Stelvio von Kingdragon | 12 | Arumanfi | 1 |
| Ghislaine | 10 | Child | 1 |
| Benebene | 10 | | |

(The attribution files hold a few extra lines that the reader no longer counts
as dialogue, because those blocks were re-typed as narration — see the
re-typing section below.)

## Scene map

| Scene | Location | Cast |
| --- | --- | --- |
| ch01-s01 | Orsted Corporation headquarters on the outskirts of Sharia | Rudeus, Orsted, Eris |
| ch01-s02 | The reception room of the Orsted Corporation, Sharia | Rudeus, Secretary |
| ch01-s03 | The Greyrat house in Sharia | Lilia, Elinalise, Rudeus, Eris, Roxy, Sylphiette, Aisha, Zenith, Norn, Leo, Lara, Lucie |
| ch01-s04 | The Zanoba Store in Sharia | Rudeus, Zanoba, Roxy, Eris, Sylphiette |
| ch01-s05 | The Mercenary Band carriage on the way home | Rudeus, Eris, Roxy, Sylphiette |
| ch02-s01 | The palace of the King Dragon Realm, Wyvern | Rudeus, Eris, Zanoba, Randolph, Benedikte, Aisha, Julie |
| ch02-s02 | The audience chamber of the King Dragon Realm palace | Rudeus, Eris, Zanoba, Randolph, Benedikte |
| ch03-s01 | The military training grounds of the King Dragon Realm | Rudeus, Zanoba, Vio Pompadour, Shagall Gargantis |
| ch03-s02 | A restaurant near the King Dragon Realm palace | Rudeus, Vio Pompadour, Zanoba, Aisha, Eris, Julie |
| ch04-s01 | The Asuran palace, outside and inside Ariel's chambers | Rudeus, Ariel, Dohga, Lady-in-Waiting, Ghislaine, Sylvester Ifrit, Chandle |
| ch05-s01 | The Asuran Embassy in Wyvern | Rudeus, Aisha, Eris |
| ch05-s02 | The audience chamber of the King Dragon Realm palace | Rudeus, Kirkland von Kingdragon, Shagall Gargantis, Stelvio von Kingdragon, Herald |
| ch05-s03 | The King Dragon Realm palace, Benedikte's quarters | Rudeus, Randolph, Benedikte, Zanoba, Julie |
| ch06-s01 | The kitchen of the Greyrat house in Sharia | Roxy, Eris |
| ch06-s02 | The dining room of the Greyrat house in Sharia | Roxy, Eris |
| ch07-s01 | The road to the Gaslow Territory, Demon Continent | Rudeus, Eris, Roxy |
| ch07-s02 | The back gate of Fort Necross | Rudeus, Eris, Roxy, Guard |
| ch07-s03 | The arena of Fort Necross | Rudeus, Eris, Roxy, Atofe, Moore, Guard |
| ch08-s01 | The arena of Fort Necross | Rudeus, Eris, Roxy, Guard |
| ch08-s02 | The arena of Fort Necross | Rudeus, Eris, Roxy, Calina, Guard |
| ch08-s03 | The arena of Fort Necross | Rudeus, Eris, Roxy, Benebene, Guard |
| ch09-s01 | The princess's room in Fort Necross | Rudeus, Atofe, Moore |
| ch10-s01 | The arena of Fort Necross | Rudeus, Eris, Roxy, Moore, Arcantos, Atofe |
| ch11-s01 | The arena of Fort Necross | Rudeus, Eris, Roxy, Atofe, Guard |
| ch11-s02 | The arena of Fort Necross | Rudeus, Eris, Roxy, Atofe, Moore |
| ch11-s03 | Fort Necross: banquet hall, training ground, Moore's room | Rudeus, Eris, Roxy, Atofe, Moore, Guard |
| ch12-s01 | The road to and arrival at the Migurd Village | Rudeus, Roxy, Lara |
| ch12-s02 | The Rokari family home, Migurd Village | Rudeus, Roxy, Rokari, Lara |
| ch12-s03 | The Rokari family home, Migurd Village | Rudeus, Roxy, Rowin, Rokari, Lara |
| ch12-s04 | An empty house near the Migurd Village | Rudeus, Roxy, Lara |
| ch12-s05 | The entrance to the Migurd Village | Rudeus, Roxy, Lara, Rowin, Rokari |
| ch13-s01 | The Greyrat house in Sharia | Rudeus, Sylphiette, Norn, Aisha, Lucie, Leo, Lilia |
| ch13-s02 | The Greyrat house in Sharia, the childbirth room | Rudeus, Sylphiette, Lucie, Doctor, Roxy, Eris, Aisha, Lilia, Leo, Arumanfi |
| ch14-s01 | The Man-God's white room | Geese, Man-God |
| ch14-s02 | The Begaritt Continent: a desert boulder, a village, and the village beacon | Geese, Young Adventurer, Desert Warrior, Villager, Child |

## Uncertainty ledger

No `low`-confidence labels are used. All three flagged entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch03-p0011 | Shagall Gargantis | Comment on the drilling soldiers; read as the general himself. |
| ch08-p0097 | Guard | "That was too fast…" — muttered by Calina or one of the watching guards; not identified. |
| ch12-p0105 | Rudeus | "Oh…" — Roxy and Rudeus exclaim at the same time; Rudeus is listed first. |

## Conventions used

* **Canonical names.** "Rudeus" and "Sylphiette" are used as speaker labels
  throughout. The book's own text writes "Rudy", "Miss Sylphie", "Master
  Rudeus" and so on; those stay inside the quotes, but the label is always the
  canonical form.
* **Title vs. name.** `Atofe` is the Immortal Demon King Atoferatofe Rybak;
  `Stelvio von Kingdragon` is the king; `Kirkland von Kingdragon` is the first
  prince; `Vio Pompadour` is the same man in disguise (the book reveals this
  in ch05: "Vio… I mean Stelvio"), so the two labels follow the name in use in
  each scene. `Shagall` and `Shagall Gargantis` are the same general, and the
  full name is used throughout.
* **Demon King Atofe's guard.** Atofe's personal guard are unnamed knights in
  black armour; their lines carry the generic label `Guard`. The four elites are
  named by the book: `Calina` (wind), `Benebene` (water), `Peridot` (earth, who
  does not speak in this volume) and `Arcantos` (flame). `Moore` is Atofe's
  retainer and speaks constantly.
* **The unnamed youth in ch14.** The "dreaming youth" who waits on the boulder
  in the Begaritt Continent is never named in the volume; he is labelled
  `Young Adventurer`. The people around him are `Desert Warrior`, `Villager`
  and `Child`.
* **Other generic labels.** `Secretary` (Orsted's unnamed secretary — the
  narration cannot even remember her name), `Lady-in-Waiting` (Ariel's
  attendant in ch04), `Herald` (the announcer in the King Dragon Realm audience
  chamber), `Doctor` (the midwife in ch13), `Legend` (the inscribed verse at
  Fort Necross), `Demon King` (the chorus of demon kings in ch12) and
  `Shirone Noble` (the hypothetical conspirators in ch02).
* **Point of view.** Chapter 1 opens in Lilia's voice (she writes down Rudeus's
  report and hosts the family meeting); from ch01-s04 the chapter moves to
  Rudeus. The scene metadata records the scene POV exactly as the classified
  data has it — Lilia for ch01-s01 … ch01-s03 and Rudeus for ch01-s04 and
  ch01-s05 — and the scene cast always contains it. Chapter 6 is the Roxy
  interlude and chapter 14 is the Geese extra chapter; their first-person "I"
  lines are attributed to those two.
* **Re-typed blocks (5).** Five blocks that the first-pass classifier typed as
  `speech` are really narration and were re-typed as `narration`, each with a
  note: ch06-p0018 (narration carrying Roxy's question about the burnt lump),
  ch07-p0174 (Rudeus's inner aside quoting Eris's word "Okay!"), ch07-p0197
  (Rudeus's monologue quoting his own earlier phrasing), ch11-p0127 (the word
  "Strength" in quotation marks) and ch12-p0116 (Rudeus imagining a phrase
  Lara might say). Two further narration blocks that the classifier got right —
  ch10-p0072 (Rudeus replaying Roxy's offer in his head) and ch14-p0034 (Geese
  quoting the Man-God inside his own head) — are annotated with
  `embeddedDialogue` so the reader still knows whose words they carry.
* **Narration that carries live dialogue (34 `embeddedDialogue` blocks).**
  Examples: ch01-p0126 (Lilia's question to Elinalise), ch02-p0046 (Eris's
  stammered introduction), ch04-p0040 (the lady-in-waiting's rebuke),
  ch07-p0048 (the gate guard's reply), ch10-p0094 (Atofe's voice across the
  arena), ch12-p0180 (Lara's first spoken words).
* **Recollection and imagination (2 + 1).** ch13-p0080 (Sylphiette's answer,
  repeated in Rudeus's narration) and ch14-p0034 (Geese quoting the Man-God)
  are flagged `recollection`; ch02-p0098 — the conspirators' imagined reply
  about killing the baby — is flagged `imagined`.
* **Mixed blocks (222).** A speech block is flagged `mixed` when it also carries
  narration or an action beat, for example ch01-p0004 ("Th-that's all I have to
  report for this time," I said, wrapping up my report…), ch04-p0046
  ("Very well," Roxy said, stepping forwards to address the guards…) or
  ch11-p0112 ("Under these circumstances, I have no choice but to use my
  authority as deputy captain of the Keepers of Anastasia to dismiss you," she
  continued).
* **Two speakers in one block.** Where two characters answer in the same
  paragraph (ch01-p0196 Eris and Aisha, ch07-p0215 Roxy and Eris, ch12-p0094 and
  ch12-p0105 Roxy and Rudeus) the first speaker is used and the block is
  flagged `mixed` with a note.
