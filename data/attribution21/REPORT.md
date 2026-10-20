# Volume 21 — Speaker Attribution Report

*Playing Dumb* (ch01–ch08) and three extra chapters (ch09 Eris, ch10 Therese, ch11 Geese).
Reader data set: `data/volume21.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 11 (ch01–ch08 main, ch09–ch11 extra) |
| Scenes | 35 |
| Blocks total | 2,113 (1,114 narration, 941 speech, 58 spacer) |
| Speech blocks in the classified data | 950 |
| Attributed speech blocks | 950 (100.0%) |
| Speech blocks after nine re-typed narration blocks | 941 |
| Attributed after re-typing | 941 (100.0%) |
| Distinct speakers | 29 |
| `mixed` blocks | 144 |
| `embeddedDialogue` blocks | 28 |
| `recollection` blocks | 36 |
| `imagined` blocks | 2 |
| `type` overrides | 9 (all of them re-type a `speech` block as `narration`) |
| Blocks carrying a `note` | 57 |
| Medium / low confidence | 14 / 0 |

Validation status:

```
python3 scripts/check_attribution.py --volume 21   -> Attributed: 950 (100%)
python3 scripts/make_scene_metadata.py --volume 21 --file /tmp/opencode/spec21-scenes.json
                                                     -> 35 scenes
python3 scripts/build.py --volume 21                -> Chapters: 11 | speech: 941 | attributed: 941 | speakers: 29
python3 scripts/validate.py --volume 21            -> Validation passed.
```

`check_attribution.py` also lists 21 "extra" keys. Those are the narration blocks
that carry quoted speech (and the blocks re-typed as narration); they are
deliberate entries, not mistakes.

## Top speakers (volume)

Counts below are the line counts in the built reader
(`data/volume21.json` → `speakers`), i.e. speech blocks only.

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 277 | Carlisle Latria | 16 |
| Blessed Child | 123 | Zenith | 16 |
| Therese | 101 | Cardinal Leblanc | 9 |
| Temple Knight | 78 | Orsted | 7 |
| Claire Latria | 69 | Sir Bellemond | 5 |
| Geese | 54 | Guard | 4 |
| Pope | 39 | Barkeep | 3 |
| Cliff | 37 | Council Member | 3 |
| Eris | 29 | Knight | 3 |
| Aisha | 21 | Wendy | 3 |
| Sword God | 18 | Funeral Procession | 2 |
| Dusklight Morchite | 17 | Morchite Mother | 2 |

Smaller labels: Dust Bin (1), Geese's Father (1), Man-God (1), Meredy Latria (1),
Passerby (1).

(The attribution files hold a few extra lines that the reader no longer counts
as dialogue, because those blocks were re-typed as narration — see the
re-typing section below.)

## Scene map

| Scene | Location | Cast |
| --- | --- | --- |
| ch01-s01 | The Adventurers' District, Millishion | Rudeus, Aisha |
| ch01-s02 | The Dappled Light Tavern in the pleasure district | Rudeus, Aisha, Geese |
| ch01-s03 | The gate of the Latria estate | Rudeus, Aisha, Geese, Claire Latria, Guard, Butler |
| ch01-s04 | The streets of the Divine District | Rudeus, Aisha, Geese |
| ch02-s01 | The pope's audience chamber, church headquarters | Rudeus, Pope, Cliff |
| ch02-s02 | The inner garden of the church headquarters | Rudeus, Blessed Child, Therese |
| ch02-s03 | The mercenary band office, Merchant District | Rudeus, Orsted, Therese, Blessed Child, Guard |
| ch02-s04 | The inner garden of the church headquarters | Rudeus, Therese, Blessed Child |
| ch03-s01 | Inner garden — the inquisition | Rudeus, Therese, Temple Knight, Dust Bin |
| ch03-s02 | Inner garden — the fight | Rudeus, Therese, Temple Knight |
| ch03-s03 | Inner garden — Therese's viewpoint | Therese, Rudeus, Temple Knight, Funeral Procession |
| ch03-s04 | Inner garden — the duel | Rudeus, Therese, Blessed Child, Temple Knight |
| ch04-s01 | The mercenary band office | Rudeus, Blessed Child |
| ch04-s02 | Church headquarters and its labyrinthine passages | Rudeus, Blessed Child, Temple Knight, Therese, Carlisle Latria |
| ch05-s01 | The meeting room of the church headquarters | Rudeus, Pope, Cliff, Cardinal Leblanc, Sir Bellemond, Carlisle Latria, Claire Latria, Zenith, Blessed Child |
| ch05-s02 | The meeting room of the church headquarters | as above plus Therese, Temple Knight |
| ch06-s01–s03 | The meeting room (the Latria family history) | Rudeus, Claire Latria, Meredy Latria, Carlisle Latria, Ralkan Latria, Therese, Zenith, Norn, Aisha |
| ch06-s04 | The Latria estate (recounted history) | Rudeus, Claire Latria, Aisha, Zenith, Ander |
| ch06-s05 | The meeting room of the church headquarters | Rudeus, Carlisle Latria, Claire Latria, Cliff, Blessed Child, Therese, Zenith, Pope, Cardinal Leblanc |
| ch07-s01 | Cliff's house and the Blessed Child's quarters | Rudeus, Cliff, Wendy, Aisha, Geese, Zenith, Carlisle Latria, Claire Latria, Blessed Child, Temple Knight |
| ch07-s02 | The side room of the church headquarters and Cliff's house | Rudeus, Claire Latria, Aisha, Zenith, Wendy |
| ch08-s01 | The mercenary band office (Orsted's messages) | Rudeus, Orsted |
| ch08-s02 | The mercenary band office | Rudeus, Aisha |
| ch08-s03 | The mercenary band office | Rudeus, Aisha, Eris |
| ch08-s04 | The mercenary band office | Rudeus |
| ch08-s05 | Latria estate, church headquarters, Cliff's house | Rudeus, Claire Latria, Aisha, Eris, Zenith, Blessed Child, Therese, Cliff, Temple Knight |
| ch09-s01 | The inner garden of the church headquarters | Eris, Therese, Blessed Child, Temple Knight, Rudeus |
| ch10-s01 | The Latria estate | Therese, Claire Latria |
| ch10-s02 | The Morchite family estate | Therese, Claire Latria, Dusklight Morchite, Morchite Mother |
| ch10-s03 | The Latria estate | Therese, Claire Latria |
| ch11-s01 | A roadside camp on the road west, Central Continent | Geese, Geese's Father |
| ch11-s02 | A ravine in a snowy monster forest beyond the Asura Kingdom | Geese, Sword God |
| ch11-s03 | The same ravine | Geese |

## Uncertainty ledger

No `low`-confidence labels are used. All 14 flagged entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch01-p0032 | Passerby | Unnamed man in the pleasure district who approaches Rudeus. |
| ch01-p0212 | Geese | One of two short replies to Rudeus ("Okay." / "I understand."); read as Geese's. |
| ch01-p0213 | Aisha | The second of those two replies; read as Aisha's. |
| ch02-p0138 | Guard | One of the Blessed Child's otaku knight guards. |
| ch02-p0139 | Guard | One of the Blessed Child's otaku knight guards. |
| ch02-p0140 | Guard | One of the otaku knight guards — the "fan brigade" whose attitude softened. |
| ch03-p0020 | Dust Bin | The knight who objects; the next paragraph says Dust was disappointed that his motion was overruled. |
| ch03-p0078 | Temple Knight | One of the Keepers of Anastasia jokes in the middle of the vote; not named. |
| ch04-p0210 | Blessed Child | Read as the Blessed Child asking how far the labyrinth still goes. |
| ch05-p0013 | Pope | Someone at the table repeats Rudeus's slang; read as the pope. |
| ch05-p0133 | Zenith | The cry as Zenith rams into Sir Bellemond. |
| ch08-p0117 | Knight | One of the Millis rumors about Cliff, credited to the Temple Knight commander and the Cathedral Knight vice-captain. |
| ch08-p0118 | Knight | Same rumor set. |
| ch08-p0119 | Knight | Same rumor set. |

## Conventions used

* **Canonical names.** "Rudeus" and "Sylphiette" are used throughout, never
  "Rudy" or "Sylphie" as the speaker label (the characters still say "Rudy"
  inside quotes, which is the book's wording). Full in-world names are kept as
  the book gives them: Claire Latria, Carlisle Latria, Therese Latria,
  Cardinal Leblanc, Pope, Sir Bellemond, Dusklight Morchite, Meredy Latria.
* **The pope and the cardinal.** The volume names them "Pope Harry Grimor" and
  "Cardinal Leblanc McFarlane" once each, but the book itself calls them
  "the pope" and "the cardinal" (and "Cardinal Leblanc") everywhere else, so
  the labels are `Pope` and `Cardinal Leblanc`.
* **The Blessed Child** never has a name in this volume, so the label is
  `Blessed Child`. (Volume 22 names her Nurse; the two volumes are consistent
  with each other only in the sense that the book is — the name does not exist
  yet in volume 21.)
* **Keepers of Anastasia.** The eight elite Temple Knights are introduced by
  code name: Skull Ash, Dust Bin, Grave Keeper, Trash Sweeper, Black Coffin,
  Burial Shroud, Funeral Procession. Where the text names the speaker, that
  name is used (`Dust Bin`, `Funeral Procession`). The many collective shouts
  ("Liar!", "No objections!", "The accused is lying!") are not attributable to
  one knight, so they carry the generic label `Temple Knight`.
* **Dust Bin / Dusklight Morchite.** The same person. Chapter 3 only knows his
  code name (`Dust Bin`); chapter 10 reveals his real name, and the text itself
  links the two ("Yes, he had another name. Dust Bin, of the Keepers of
  Anastasia."). The label follows the name in use in each chapter.
* **The unnamed swordsman in ch11** is never named in this volume. He is
  labelled `Sword God` (the title he holds elsewhere in the series; volume 22
  names him Gall Falion).
* **Generic labels** used across the volume: `Temple Knight` (the Millis
  knight orders and the Keepers), `Knight` (the Millis rumours in ch08),
  `Guard` (the city guard and the Blessed Child's attendants), `Council Member`
  (the assembly at the negotiating table in ch05), `Barkeep` (two tavern
  keepers), `Passerby` (the man in the pleasure district in ch01), `Morchite
  Mother` (Dusklight's unnamed mother), `Geese's Father`.
* **Point of view.** Chapter 3 breaks twice: ch03-s03 is Therese's viewpoint
  during the fight (`povHeader: Therese`) and ch03-s04 returns to Rudeus
  (`povHeader: Rudeus`); the scene metadata records the scene POV exactly as
  the classified data has it, and the scene cast always contains it. Chapters
  9, 10 and 11 are extras in Eris's, Therese's and Geese's voices; their
  first-person "I" lines are attributed to those three.
* **Re-typed blocks (9).** Nine blocks that the first-pass classifier typed as
  `speech` are really narration and were re-typed as `narration` with an
  explanatory note: ch03-p0188 (the epithet "Quagmire" in quotes), ch03-p0232
  (Rudeus imagining Aisha), ch06-p0132 (Claire's earlier explanation), ch07-p0015
  (the cardinal's stock answer), ch09-p0022 (Rudeus's guarantee, recalled),
  ch09-p0030 and ch09-p0034 (the Blessed Child's squeak and reaction) and
  ch11-p0028 and ch11-p0122 (Geese recounting the Man-God's instructions, and
  the swordsman's threat). Two more narration blocks that the classifier got
  right — ch11-p0040 and ch11-p0151, both of the Man-God speaking inside
  Geese's account — are annotated with `embeddedDialogue` so the reader still
  knows whose words they carry.
* **Narration that carries live dialogue (28 `embeddedDialogue` blocks).**
  Where a narration paragraph quotes someone who is speaking in the present
  moment, the block is annotated with that speaker so the reader still knows
  whose words they are. Examples: ch01-p0058 (Rudeus, "Where's my mother?"),
  ch02-p0016 (the pope), ch05-p0058 / p0183 / p0199, ch07-p0157, ch10-p0008,
  ch11-p0076.
* **Recollection and imagination (36 + 2).** 36 blocks are remembered speech
  (Claire's childhood in ch06, Geese's letter in ch07, Zenith's memories
  recited by the Blessed Child in ch07, the Man-God's instructions in ch11).
  These keep their speaker but are flagged `recollection`, and they are
  deliberately kept out of the scene cast.
* **Zenith's memories in ch07 (ch07-p0076 – ch07-p0096).** The Blessed Child
  reads Zenith's memories aloud in Zenith's voice. These blocks are attributed
  to `Zenith` with `recollection`, because the words are Zenith's.
* **Mixed blocks (144).** A speech block is flagged `mixed` when it carries
  narration or an action beat in addition to the quoted line — for example
  ch01-p0008 ("Aisha replied. She sank to the ground…"), ch03-p0058
  ("When they were done, Therese announced…") or ch09-p0153.
