# Volume 19 — Speaker Attribution Report

Chapter: *Mushoku Tensei* Volume 19 (ch01–ch14), reader data set `data/volume19.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 14 (ch01–ch14; ch14 is the extra chapter) |
| Scenes | 31 |
| Blocks total | 2,870 (1,516 narration, 1,285 speech, 1 quotation, 2 silence, 66 spacer) |
| Speech blocks in the classified source | 1,290 |
| Speech blocks after re-typing | 1,285 (5 blocks were re-typed, see below) |
| Attributed speech blocks | 1,285 (100.0%) |
| Distinct speakers | 29 |
| `mixed` blocks | 177 |
| `recollection` blocks | 4 |
| `imagined` blocks | 0 |
| `type` overrides | 5 (1 → `quotation`, 4 → `narration`) |
| Blocks carrying a `note` | 214 |

Validation status:

```
python3 scripts/check_attribution.py --volume 19   -> Attribution coverage complete.
python3 scripts/build.py --volume 19                -> wrote data/volume19.json
python3 scripts/validate.py --volume 19            -> Validation passed.
```

## Top speakers (volume)

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 342 | Benedikte | 12 |
| Zanoba | 301 | Cliff | 11 |
| Roxy | 129 | Squire | 10 |
| Pax | 120 | Aisha | 9 |
| Randolph Marianne | 100 | Billy | 9 |
| Orsted | 71 | Norn | 9 |
| Ginger | 36 | Sylphiette | 9 |
| Eris | 25 | Sylvaril | 9 |
| Perugius | 24 | Garrick Babriti | 8 |
| Soldier | 20 | Julie | 7 |

Remaining speakers: Lara (7), Nanahoshi (5), Elinalise (3), Leonardo Kingdragon (2),
Lilia (2), Lucie (2), Arus (1), Leo (1), Noble (1).

## Chapters

| Chapter | Title | Speech | Main speakers |
| --- | --- | --- | --- |
| ch01 | Zanoba's Decision | 93 | Rudeus 34, Orsted 27, Zanoba 26, Cliff 6 |
| ch02 | Bad Omens | 115 | Rudeus 24, Perugius 24, Zanoba 23, Roxy 15, Sylphiette 7, Eris 7 |
| ch03 | The Return to Shirone | 137 | Rudeus 47, Orsted 23, Roxy 16, Zanoba 14, Cliff 5, Nanahoshi 5 |
| ch04 | King Pax | 84 | Pax 40, Zanoba 32, Rudeus 9, Leonardo Kingdragon 2 |
| ch05 | Fort Karon | 121 | Zanoba 40, Roxy 32, Rudeus 31, Soldier 10, Garrick Babriti 8 |
| ch06 | Preparations for War | 81 | Rudeus 39, Roxy 23, Zanoba 16, Billy 3 |
| ch07 | The Battle | 46 | Rudeus 19, Zanoba 10, Roxy 6, Billy 6, Soldier 5 |
| ch08 | An Urgent Message, and Zanoba's True Feelings | 97 | Zanoba 42, Rudeus 30, Ginger 20, Soldier 5 |
| ch09 | To Pax's Side | 82 | Zanoba 31, Randolph Marianne 21, Rudeus 18, Roxy 12 |
| ch10 | Wasted Effort All Around | 120 | Rudeus 31, Randolph Marianne 28, Pax 26, Zanoba 25, Roxy 10 |
| ch11 | Aftermath | 85 | Rudeus 24, Zanoba 19, Randolph Marianne 18, Roxy 13, Ginger 11 |
| ch12 | Zanoba's Chosen Path | 55 | Orsted 21, Rudeus 18, Zanoba 15, Roxy 1 |
| ch13 | It's All Right to Be Happy | 60 | Rudeus 18, Eris 15, Zanoba 8, Norn 7, Aisha 6, Julie 4 |
| ch14 | Extra Chapter: The Death God and the Gluttonous Prince | 109 | Pax 54, Randolph Marianne 32, Benedikte 12, Squire 10, Noble 1 |

## Scene map

| Scene | Location | Cast |
| --- | --- | --- |
| ch01-s01 | Zanoba's laboratory, main research building, Ranoa University | Rudeus, Cliff, Zanoba, Elinalise, Ginger, Julie |
| ch01-s02 | The road outside Orsted's office, Ranoa University | Rudeus |
| ch02-s01 | Rudeus's house, Sharia | Rudeus, Eris, Sylphiette, Roxy, Aisha, Lilia, Lara, Lucie |
| ch02-s02 | Rudeus's house in Sharia, then the Principal's office at Ranoa University | Rudeus, Roxy, Sylphiette, Zanoba, Principal |
| ch02-s03 | Perugius's floating fortress (art gallery), then a warehouse near the Shirone capital | Rudeus, Zanoba, Perugius, Sylvaril, Ginger |
| ch03-s01 | Rudeus's house in Sharia, a vacant lot in the city, and the front gate of the household | Rudeus, Orsted, Eris, Sylphiette, Aisha, Norn, Lilia, Zenith, Lucie, Leo, Julie, Lara, Byt |
| ch03-s02 | The gates of Sharia, Perugius's floating fortress (teleportation chamber), and the ruined building near Shirone's eastern border | Rudeus, Zanoba, Roxy, Ginger, Cliff, Elinalise, Sylvaril, Nanahoshi, Arumanfi |
| ch03-s03 | The streets and the inn in Latakia, the capital of Shirone | Rudeus, Zanoba, Roxy, Ginger |
| ch04-s01 | The throne room of Shirone Castle, Latakia | Rudeus, Zanoba, Pax, Benedikte, Randolph Marianne, Knight |
| ch04-s02 | A guest room in Shirone Castle, Latakia | Rudeus, Zanoba |
| ch05-s01 | The inn in Latakia, the capital of Shirone | Rudeus, Roxy |
| ch05-s02 | The road to Fort Karon, then the fort's war room and ramparts | Rudeus, Zanoba, Roxy, Garrick Babriti, Billy, Soldier |
| ch06-s01 | The plain north of Fort Karon, then the ramparts of Fort Karon | Rudeus, Zanoba, Roxy |
| ch06-s02 | The ramparts of Fort Karon | Rudeus, Roxy, Billy |
| ch07-s01 | The ramparts of Fort Karon | Rudeus, Roxy, Billy, Soldier |
| ch07-s02 | Inside Fort Karon, after the battle | Rudeus, Zanoba, Roxy, Garrick Babriti, Soldier |
| ch07-s03 | A room inside Fort Karon, where the Bista prisoner is questioned | Rudeus, Zanoba, Bista Royal |
| ch08-s01 | The riverbank near Fort Karon, then a room inside the fort | Rudeus, Zanoba, Ginger, Soldier |
| ch09-s01 | Outside the sealed city of Latakia, then a watermill on the riverbank | Rudeus, Zanoba, Roxy |
| ch09-s02 | The secret passage beneath Latakia and the halls of Shirone Castle | Rudeus, Zanoba, Roxy, Randolph Marianne |
| ch10-s01 | The fifth-floor landing of Shirone Castle, Latakia | Rudeus, Zanoba, Roxy, Randolph Marianne |
| ch10-s02 | The king's chambers and balcony in Shirone Castle, then the palace gardens | Rudeus, Zanoba, Roxy, Pax, Benedikte, Randolph Marianne |
| ch11-s01 | The palace gardens, the secret passage, and the watermill outside Latakia | Rudeus, Zanoba, Roxy, Randolph Marianne, Benedikte |
| ch11-s02 | The main plaza of Latakia, where Pax's remains are displayed, and an inn in the city | Rudeus, Zanoba, Roxy, Ginger, Sylphiette, Aisha, Norn, Lara |
| ch12-s01 | Zanoba's room in Sharia, as he looks back on his life | Zanoba |
| ch12-s02 | Perugius's floating fortress, Nanahoshi's quarters, and Orsted's office in Ranoa University | Rudeus, Zanoba, Roxy, Orsted, Perugius, Nanahoshi |
| ch13-s01 | The garden and living room of Rudeus's house in Sharia | Rudeus, Zanoba, Eris, Julie, Aisha, Norn, Sylphiette, Lucie, Roxy, Lara, Lilia, Zenith, Arus |
| ch13-s02 | Rudeus's house in Sharia, as Rudeus reviews the plan | Rudeus |
| ch14-s01 | The gardens of the royal villa in the King Dragon Realm | Pax, Benedikte, Noble |
| ch14-s02 | The parade grounds of the royal villa in the King Dragon Realm | Pax, Benedikte, Randolph Marianne, Squire |
| ch14-s03 | A stairway landing in Shirone Castle, on the night of the rebellion | Pax, Randolph Marianne, Benedikte |

## Uncertainty ledger

No `low`-confidence labels are used anywhere in the volume. All three flagged
entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch01-p0165 | Rudeus | "…Hmmm." sits between Rudeus's own conclusion and Orsted's next point; it reads as Rudeus murmuring, but it could be Orsted thinking aloud. |
| ch07-p0052 | Rudeus | "Ah…looks like they're going for it." Either Rudeus or the mage squad captain Billy could be the one watching the enemy lines. |
| ch10-p0254 | Rudeus | The scream that follows Pax's jump from the balcony; it is either Rudeus's cry of horror or Zanoba's cry as he lunges after his brother. |

## Conventions

* **Only speech-typed blocks are listed.** Every block the first-pass classifier
  typed as `speech` appears in `data/attribution19/chNN.json` with a speaker, so
  `check_attribution.py` reports complete coverage with no unknown keys. Blocks
  the classifier typed as `narration` are left alone, even when they contain
  quoted dialogue inside the narration.
* **Names.** Canonical names are used throughout: "Rudeus" (never "Rudy"),
  "Sylphiette" (never "Sylphie"), "Zanoba", "Cliff", "Pax", "Randolph Marianne",
  "Orsted", "Roxy", "Ginger York", "Julie", "Norn", "Aisha", "Lilia", "Zenith",
  "Sylvaril", "Perugius", "Elinalise", "Nanahoshi", "Benedikte", "Arus",
  "Lucie", "Lara", "Garrick Babriti", "Billy". The book itself calls Sylphiette
  "Sylphie" in other characters' speech; the label stays "Sylphiette".
* **Generic labels.** Unnamed speakers get a descriptive label that is used
  consistently through the volume: `Soldier` (garrison soldiers, the messenger,
  the chanting combat mages, the archers' captain), `Squire` (the King Dragon
  Realm squires in ch14), `Noble` (the courtier who sneers at Pax and Benedikte
  in ch14). Named minor characters keep their names even when they only speak a
  line or two (`Billy`, the combat-mage squad captain; `Garrick Babriti`, the
  Fort Karon commander).
* **Vocalizations and battle cries** are attributed to the person making the
  sound: Zanoba's "Raaaaaah!" (ch10-p0003), Rudeus's "…Hooo." (ch07-p0005,
  ch07-p0007), Leo's "Raruff!" (ch03-p0121), the newborn Arus's crying
  (ch13-p0091).
* **`mixed`** marks the 177 blocks where the classifier typed a line as speech
  but the paragraph also carries narration ("Zanoba's response was prompt and
  firm: …"). The speaker is the one whose words are quoted.
* **`recollection`** marks four blocks whose speaker is not in the scene:
  King Pax's letter (ch01-p0018), the King Dragon Realm king's remarks as
  quoted in Pax's tale (ch04-p0108, ch04-p0110), and Zanoba's own words at
  Fort Karon as he recalls them (ch12-p0022).
* **Re-typed blocks.** Five blocks were typed as speech by the classifier but
  are not spoken aloud, and were re-typed with a note:
  * `ch01-p0018` → `quotation` (Pax's letter, quoted from the page);
  * `ch03-p0057`, `ch05-p0194`, `ch08-p0036`, `ch11-p0046` → `narration`
    (Rudeus's inner monologue). The speaker is kept so the reader still knows
    whose thought it is.
* **POV changes.** ch12 opens in Zanoba's point of view (the scene header is
  "Zanoba") and switches to Rudeus for the rest of the chapter; the scene-level
  POVs follow the in-story headers, and the chapter label follows the opening
  scene. ch14 (the extra chapter) is narrated entirely from Pax's point of
  view, so `chapterPov` and the per-scene `pov` are overridden to "Pax" in
  `data/scene_metadata19.json`; the volume configuration still lists Rudeus, so
  the metadata helper also keeps "Rudeus" in the cast of those three scenes.
* **Scene metadata.** `data/scene_metadata19.json` maps all 31 scene IDs to a
  location and a cast. The cast always includes the scene POV, every speaker
  attributed to that scene, and the other characters who are in the room but
  do not speak (for example Elinalise, Ginger and Julie in ch01-s01, or the
  captive "Bista Royal" in ch07-s03).
