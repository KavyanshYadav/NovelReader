# Volume 20 — Speaker Attribution Report

Chapter: *Mushoku Tensei* Volume 20 (ch01–ch12), reader data set `data/volume20.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 12 (ch01–ch12; ch05 and ch06 are the two interludes) |
| Scenes | 41 |
| Blocks total | 2,441 (1,203 narration, 1,145 speech, 3 quotation, 25 silence, 65 spacer) |
| Speech blocks in the classified source | 1,158 |
| Speech blocks after re-typing | 1,145 (13 blocks were re-typed, see below) |
| Attributed speech blocks | 1,145 (100.0%) |
| Distinct speakers | 44 |
| `mixed` blocks | 117 |
| `recollection` blocks | 7 |
| `imagined` blocks | 0 |
| `type` overrides | 13 (3 → `quotation`, 10 → `narration`) |
| Blocks carrying a `note` | 145 |

Validation status:

```
python3 scripts/check_attribution.py --volume 20   -> Attribution coverage complete.
python3 scripts/build.py --volume 20                -> wrote data/volume20.json
python3 scripts/validate.py --volume 20            -> Validation passed.
```

## Top speakers (volume)

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 347 | Ariel | 9 |
| Cliff | 170 | Linia | 9 |
| Aisha | 90 | Roxy | 9 |
| Norn | 58 | Sylphiette | 9 |
| Zanoba | 44 | Merchant | 8 |
| Claire Latria | 40 | Wendy | 8 |
| Joseph | 31 | Ginger | 7 |
| Elinalise | 30 | Orsted | 7 |
| Student | 30 | Guard | 5 |
| Nina | 29 | Pursena | 5 |
| Therese Latria | 22 | Jenius | 4 |
| Blessed Child | 20 | Mercenary | 4 |
| Harry Grimor | 18 | Wraith | 4 |

Remaining speakers: Geese (17), Knight (17), Brooklyn von Elsass (16), Eris (15),
Lilia (15), Beastman (14), Sheila (11), Ander Berkeley (9), Butler (3), Lucie (3),
Julie (2), Clive (1), Dust (1), Gal Falion (1), Grave (1), Isolde Cluel (1),
Villager (1), Zenith (1).

## Chapters

| Chapter | Title | Speech | Main speakers |
| --- | --- | --- | --- |
| ch01 | Plans for the Future and Cliff's Concerns | 52 | Cliff 22, Rudeus 20, Orsted 7, Elinalise 3 |
| ch02 | The Zanoba Store | 127 | Rudeus 55, Joseph 31, Zanoba 30, Ginger 5, Linia 4, Julie 2 |
| ch03 | Cliff and the Institute of Magic Student Council | 211 | Cliff 81, Norn 50, Student 30, Elinalise 18, Beastman 14, Sheila 11 |
| ch04 | Cliff and Zanoba's Graduation Ceremony | 83 | Rudeus 29, Cliff 20, Brooklyn von Elsass 16, Zanoba 14, Jenius 2, Ginger 2 |
| ch05 | Interlude: A Country Bumpkin Visits the City | 67 | Nina 29, Eris 10, Merchant 8, Rudeus 8, Ariel 8, Gal Falion 1 |
| ch06 | Interlude: Coming-of-Age Ceremony | 58 | Rudeus 15, Aisha 9, Roxy 7, Norn 5, Pursena 5, Linia 5 |
| ch07 | Growth and New Horizons | 52 | Rudeus 20, Elinalise 9, Aisha 8, Lilia 4, Norn 3, Lucie 2 |
| ch08 | Onward, to Millishion… | 72 | Rudeus 26, Aisha 20, Cliff 10, Lilia 9, Sylphiette 5, Eris 1 |
| ch09 | Cliff's Homecoming | 79 | Rudeus 33, Aisha 17, Geese 16, Cliff 12, Zenith 1 |
| ch10 | The House of Latria | 108 | Rudeus 48, Claire Latria 40, Ander Berkeley 9, Aisha 8, Butler 3 |
| ch11 | Headquarters of the Millis Church | 152 | Rudeus 59, Therese Latria 22, Cliff 20, Blessed Child 20, Knight 17, Aisha 6 |
| ch12 | The Pope, and… | 84 | Rudeus 34, Aisha 22, Harry Grimor 18, Wendy 4, Cliff 3, Guard 2 |

## Scene map

| Scene | Location | Cast |
| --- | --- | --- |
| ch01-s01 | Orsted's office in Ranoa University, then Cliff's apartment in Sharia | Rudeus, Orsted, Cliff, Elinalise |
| ch02-s01 | Zanoba's house and workshop in Sharia | Rudeus, Zanoba, Julie |
| ch02-s02 | Zanoba's house and workshop in Sharia | Rudeus, Zanoba, Julie, Ginger, Joseph, Linia |
| ch02-s03 | The first-floor studio of Zanoba's house in Sharia | Rudeus, Zanoba, Joseph, Ginger, Julie, Linia |
| ch02-s04 | The Zanoba Store in the workshop district of Sharia | Rudeus |
| ch03-s01 | The teachers' office and the halls of the University of Magic | Cliff, Jenius, Norn, Sheila, Beastman, Student |
| ch03-s02 | The entrance and stairwell of the University of Magic's underground storehouse | Cliff, Norn, Sheila, Beastman, Student |
| ch03-s03 | The sealed chamber deep in the University of Magic's underground storehouse | Cliff, Norn, Sheila, Beastman, Student, Wraith |
| ch03-s04 | The University of Magic's underground storehouse, after the fight | Cliff, Norn, Sheila, Beastman, Student |
| ch03-s05 | Cliff and Elinalise's house in Sharia, in the bedroom | Cliff, Elinalise, Clive |
| ch04-s01 | The lecture hall of the University of Magic and the campus after the graduation ceremony | Rudeus, Cliff, Zanoba, Ginger, Julie, Norn, Aisha, Brooklyn von Elsass, Jenius |
| ch04-s02 | The rooftop of the University of Magic building | Rudeus, Cliff, Zanoba, Elinalise, Ginger |
| ch05-s01 | The training hall of the Sword Sanctum | Nina, Gal Falion, Apprentice, Isolde Cluel |
| ch05-s02 | The main street and Saalten Street in Ars, the capital of the Asura Kingdom | Nina, Merchant, Villager, Eris, Lucie, Rudeus, Sylphiette, Roxy, Zanoba, Julie |
| ch05-s03 | Isolde's training hall and the mansion near the royal castle in Ars | Nina, Isolde Cluel, Ariel, Rudeus, Eris |
| ch05-s04 | The mansion in Ars, then the road back to the Sword Sanctum | Nina, Eris, Isolde Cluel, Rudeus, Gino Britz |
| ch06-s01 | Rudeus's house in Sharia | Rudeus, Roxy |
| ch06-s02 | The basement of Rudeus's house in Sharia | Rudeus, Roxy, Lilia, Sylphiette, Eris |
| ch06-s03 | Rudeus's house in Sharia | Rudeus, Norn, Aisha |
| ch06-s04 | The living room of Rudeus's house in Sharia, during the party preparations | Rudeus, Aisha, Norn, Zenith, Lilia, Sylphiette, Lucie, Lara, Arus, Leo |
| ch06-s05 | The dining room of Rudeus's house in Sharia, at the birthday party | Rudeus, Norn, Aisha, Lilia, Sylphiette, Roxy, Eris, Zenith, Lucie, Lara, Arus |
| ch06-s06 | The front yard of Rudeus's house in Sharia | Rudeus, Aisha, Norn, Linia, Pursena, Mercenary, Eris |
| ch06-s07 | The front lawn of Rudeus's house in Sharia, at the cookout | Rudeus, Aisha, Norn, Linia, Pursena, Mercenary, Student, Eris |
| ch07-s01 | The graduation ceremony hall of the University of Magic | Rudeus, Jenius, Norn |
| ch07-s02 | Rudeus's house in Sharia, as Rudeus reviews the year | Rudeus |
| ch07-s03 | The pub in Sharia, at Cliff's sendoff party, and the street outside | Rudeus, Cliff, Elinalise, Roxy, Sylphiette, Eris, Aisha, Norn, Lilia |
| ch07-s04 | The living room of Rudeus's house in Sharia | Rudeus, Aisha, Norn, Lilia, Claire Latria |
| ch08-s01 | Rudeus's house and garden in Sharia | Rudeus, Sylphiette, Lilia, Roxy, Eris, Aisha, Zenith |
| ch08-s02 | The road from Sharia to Millishion | Rudeus, Aisha, Zenith, Cliff |
| ch09-s01 | The road to Millishion, outside the city | Rudeus, Aisha, Zenith, Cliff |
| ch09-s02 | The Adventurers' District of Millishion | Rudeus, Aisha, Zenith, Geese, Adventurer |
| ch09-s03 | The road to the Divine District of Millishion | Rudeus, Aisha, Zenith, Geese |
| ch09-s04 | Cliff's house in the Divine District of Millishion | Rudeus, Aisha, Zenith, Cliff, Wendy |
| ch10-s01 | The House of Latria in the Residential District of Millishion | Rudeus, Zenith, Aisha, Claire Latria, Ander Berkeley, Butler, Maid |
| ch10-s02 | The streets of Millishion, at the border of the Divine District | Rudeus, Zenith, Aisha |
| ch11-s01 | Cliff's house in the Divine District of Millishion | Rudeus, Cliff, Wendy, Aisha, Zenith |
| ch11-s02 | The Millis Church headquarters and the springtime garden | Rudeus, Cliff, Guard, Therese Latria, Blessed Child, Knight, Grave, Dust |
| ch12-s01 | The pope's office in the Millis Church headquarters | Rudeus, Cliff, Harry Grimor, Guard, Knight |
| ch12-s02 | The Millis Church headquarters and the streets of Millishion | Rudeus |
| ch12-s03 | Cliff's house in the Divine District of Millishion | Rudeus, Aisha, Wendy, Zenith |
| ch12-s04 | The streets of Millishion, in the search for Zenith | Rudeus, Aisha, Wendy |

## Uncertainty ledger

No `low`-confidence labels are used anywhere in the volume. All five flagged
entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch02-p0220 | Joseph | "Oh." is a flat reaction to the name "The Zanoba Store"; it could equally come from Zanoba, who is also in the room. |
| ch07-p0133 | Aisha | "Hahhh…" is a hollow laugh at the letter; it could come from Norn, who is described as exasperated. |
| ch07-p0134 | Norn | "Grandma… She never changes, huh?" is a resigned comment about their grandmother; it could come from Aisha instead. |
| ch11-p0112 | Blessed Child | "Look, the Sarakh Trees are in bloom!" is said by "someone"; it could be one of the knights rather than the Blessed Child herself. |
| ch12-p0140 | Aisha | "I'm sorry… But please, don't take it out on Wendy." is an apology for Wendy's scolding; it could be Rudeus pleading with Cliff instead. |

## Conventions

* **Only speech-typed blocks are listed.** Every block the first-pass classifier
  typed as `speech` appears in `data/attribution20/chNN.json` with a speaker, so
  `check_attribution.py` reports complete coverage with no unknown keys. Blocks
  the classifier typed as `narration` are left alone, even when they contain
  quoted dialogue inside the narration.
* **Names.** Canonical names are used throughout: "Rudeus" (never "Rudy"),
  "Sylphiette" (never "Sylphie"), "Cliff", "Aisha", "Norn", "Zanoba", "Elinalise",
  "Lilia", "Zenith", "Roxy", "Ginger", "Geese", "Wendy", "Isolde Cluel",
  "Gal Falion", "Gino Britz", "Ariel", "Therese Latria", "Claire Latria",
  "Ander Berkeley", "Brooklyn von Elsass", "Jenius", "Harry Grimor", "Nina",
  "Lucie", "Julie", "Clive", "Arus". The book itself calls Sylphiette "Sylphie"
  in other characters' speech; the label stays "Sylphiette". Nina is labelled
  "Nina" even though the book calls her Sword King/Sword Saint Nina Falion.
* **Generic labels.** Unnamed speakers get a descriptive label that is used
  consistently through the volume: `Student` (the unidentified members of the
  student council and the guests at the graduation party), `Knight` (the
  Temple Knights around the Blessed Child), `Guard` (the clerks at the Millis
  Church headquarters), `Mercenary` (the beastfolk who deliver the boar),
  `Merchant` (the salesman who sells Nina the picture book), `Villager` (the
  passerby who curses at Nina), `Butler` (the House of Latria's butler),
  `Blessed Child` (the unnamed young woman the Millis Church calls the
  "Blessed One"), `Apprentice` (the Sword Sanctum apprentice who reads
  Isolde's letter), `Wraith` (the monster in the storehouse). Two knights are
  named in the text and keep their names: `Grave` and `Dust`; the pigtailed
  student council member is `Sheila`, and the unnamed beastfolk council member
  is `Beastman` (the same label the neighbouring volumes use for unnamed
  beastfolk).
* **Vocalizations and battle cries** are attributed to the person making the
  sound: Zenith's "Ahh, aaahh…" as she points at the monkey (ch09-p0044),
  Aisha's "Mew!"-style interjections, the baby Clive's crying (ch03-p0398), and
  the Wraith's "WHY… WHY… WHY…" (ch03-p0185, p0187, p0189, p0228).
* **`mixed`** marks the 117 blocks where the classifier typed a line as speech
  but the paragraph also carries narration ("Zanoba smiled over at her
  reassuringly. …"). The speaker is the one whose words are quoted.
* **`recollection`** marks the seven blocks whose speaker is not in the scene:
  Isolde's letter read aloud in the Sword Sanctum (ch05-p0018), Ariel's
  suggestion and Lucie's two lines as Rudeus reviews the year (ch07-p0021,
  ch07-p0049, ch07-p0050), Claire Latria's order read from her letter
  (ch07-p0122), Geese's words repeated in Rudeus's retelling (ch12-p0121), and
  Cliff's advice to Norn from their school days (ch08-p0079).
* **Re-typed blocks.** Thirteen blocks were typed as speech by the classifier but
  are not spoken aloud, and were re-typed with a note:
  * → `quotation`: the phrase Rudeus considers but does not say (ch01-p0088),
    Isolde's closing message from her letter (ch05-p0018), the Countess of
    Latria's order (ch07-p0122);
  * → `narration`: a pause in Cliff's reply (ch01-p0094), narration that quotes
    Gal Falion's phrase (ch05-p0004), narration referring back to a quoted word
    (ch06-p0146), Rudeus's imagined joke about Ariel (ch07-p0042), narration
    repeating Norn's words (ch07-p0155), narration reporting what the sisters
    said about Claire (ch08-p0070), narration quoting the new branch director's
    answer (ch09-p0036), narration describing Aisha's shrug (ch10-p0127), and
    Rudeus's inner thought about a quoted term (ch10-p0159). The speaker is kept
    so the reader still knows whose thought it is.
* **POV changes.** ch03 ("Cliff and the Institute of Magic Student Council") is
  narrated entirely from Cliff's point of view, so `chapterPov` and the per-scene
  `pov` are overridden to "Cliff" in `data/scene_metadata20.json`; the volume
  configuration still lists Rudeus, so the metadata helper also keeps "Rudeus"
  in the cast of those five scenes. ch05 is Nina's interlude and ch06 is
  Rudeus's; both already match their scene headers.
* **Scene metadata.** `data/scene_metadata20.json` maps all 41 scene IDs to a
  location and a cast. The cast always includes the scene POV, every speaker
  attributed to that scene, and the other characters who are in the room but do
  not speak (for example Zenith and Leo at the birthday party in ch06, or the
  Temple Knights around the Blessed Child in ch11).
