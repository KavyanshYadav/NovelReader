# Volume 23 — Speaker Attribution Report

*Mushoku Tensei: Jobless Reincarnation* Volume 23, "The Green-Haired Baby / Path to the Divine
Continent / … / Extra Chapter: Geese and His Final Ally" (ch01–ch11).
Reader data set: `data/volume23.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 11 (ch01–ch11) |
| Scenes | 51 |
| Blocks total | 2,488 (1,234 narration, 1,153 speech, 16 silence, 85 spacer) |
| Speech blocks in the classified data | 1,162 |
| Speech blocks after the `type` re-corrections | 1,153 |
| Attributed speech blocks | 1,153 (100.0%) |
| Distinct speakers | 38 |
| `mixed` blocks | 352 |
| `recollection` blocks | 23 |
| `embeddedDialogue` blocks | 66 (59 narration blocks + 7 speech blocks) |
| `type` overrides | 9 |
| Blocks carrying a `note` | 123 |
| Medium / low confidence blocks | 14 / 0 |

Validation status:

```
python3 scripts/check_attribution.py --volume 23   -> Attributed: 1162 / 1162 (coverage complete)
python3 scripts/make_scene_metadata.py --volume 23 --file /tmp/opencode/vol23-scenes.json
python3 scripts/build.py --volume 23                -> Wrote data/volume23.json
python3 scripts/validate.py --volume 23            -> Validation passed.
```

`check_attribution.py` also lists 59 "extra/unknown keys". These are **not** errors: they are
narration blocks that contain quoted live speech, listed in the attribution files with
`embeddedDialogue: true` so the reader can show the speaker of the quoted fragment (the same
approach already used for volume 16). Seven further `embeddedDialogue` entries sit on
speech-typed blocks whose text mixes narration with a quoted line (`ch04-p0174`, `ch07-p0126`,
`ch07-p0178`, `ch07-p0217`, `ch08-p0135`, `ch10-p0035`, `ch10-p0040`).

## Top speakers (volume)

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 359 | Eris | 101 |
| Nanahoshi | 89 | Badigadi | 76 |
| Perugius | 69 | Kishirika | 65 |
| Sara | 55 | Soldat | 43 |
| Sylphiette | 42 | Geese | 37 |
| Man-God | 30 | Orsted | 28 |
| Nina | 27 | Roxy | 23 |
| Missionary Knight | 17 | Atofe | 15 |
| Sylvaril | 8 | Lucie | 7 |
| Adventurer | 6 | Soldier | 6 |
| Student | 6 | Swordsman | 6 |
| Crowd | 5 | Mercenary | 5 |
| Party Leader | 4 | Alisa | 3 |
| Black Knight | 3 | Linia | 3 |
| Pursena | 3 | Adviser | 2 |
| Glanze | 2 | Sieg | 2 |
| Aisha | 1 | Gigantic Jaw | 1 |
| Lilia | 1 | Receptionist | 1 |
| Skyfolk | 1 | Zanoba | 1 |

## Chapter map

| Chapter | Title | Scenes | Speech | Distinct speakers |
| --- | --- | --- | --- | --- |
| ch01 | The Green-Haired Baby | 4 | 78 | Nanahoshi, Orsted, Perugius, Rudeus, Sylphiette, Sylvaril |
| ch02 | Path to the Divine Continent | 7 | 65 | Aisha, Eris, Lilia, Lucie, Orsted, Roxy, Rudeus, Sieg, Sylphiette |
| ch03 | Aluce, City of the Divine Continent | 4 | 38 | Eris, Roxy, Rudeus, Skyfolk, Sylphiette |
| ch04 | Christening | 4 | 103 | Eris, Gigantic Jaw, Nanahoshi, Orsted, Perugius, Roxy, Rudeus, Sieg, Sylphiette, Sylvaril |
| ch05 | Teleportation Device to Another World | 4 | 110 | Eris, Lucie, Nanahoshi, Orsted, Perugius, Rudeus, Sylphiette, Sylvaril, Zanoba |
| ch06 | Nanahoshi's Fate | 4 | 89 | Nanahoshi, Orsted, Perugius, Receptionist, Rudeus |
| ch07 | The Mad Dog's Old Stomping Grounds | 5 | 120 | Crowd, Eris, Nina, Rudeus, Student, Swordsman |
| ch08 | A North God, an Adventurer, and More… | 7 | 153 | Adventurer, Alisa, Eris, Missionary Knight, Party Leader, Rudeus, Sara |
| ch09 | A North God, a Mercenary, and More… | 4 | 129 | Eris, Glanze, Mercenary, Missionary Knight, Orsted, Rudeus, Soldat |
| ch10 | The Second Eye | 3 | 111 | Atofe, Black Knight, Eris, Kishirika, Linia, Pursena, Rudeus |
| ch11 | Extra Chapter: Geese and His Final Ally | 5 | 157 | Adviser, Badigadi, Geese, Man-God, Soldier |

## Uncertainty ledger

No `low`-confidence labels are used in this volume. All 14 flagged entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch02-p0103 | Aisha | Farewell at the door; read as Aisha from the brisk "Gotcha!" and the three-way goodbye. |
| ch02-p0104 | Lilia | Farewell at the door; read as Lilia from the maternal "Take care, now." |
| ch02-p0105 | Lucie | Farewell at the door; read as Lucie, the hesitant child who was holding Aisha's hand. |
| ch02-p0127 | Sylphiette | Short squeal as the elevator starts; read as Sylphiette, who is uneasy about heights. |
| ch02-p0170 | Eris | Remark on Sieg's grip strength; read as Eris from the swordsmanship turn that follows. |
| ch03-p0069 | Rudeus | Question about how to enter Aluce; read as Rudeus, who leads the group, but the line is untagged. |
| ch04-p0017 | Rudeus | Reaction to the Gigantic Jaw; read as Rudeus from the POV narration, but the line is untagged. |
| ch04-p0051 | Roxy | First reaction to what Rudeus does not yet notice; read as Roxy, though the line is untagged. |
| ch04-p0053 | Sylphiette | Reaction that precedes the narration noting that Sylphie noticed the problem. |
| ch04-p0057 | Eris | Telling Rudeus to stop his dramatic monologue; read as Eris from the blunt, familiar tone. |
| ch11-p0096 | Geese | Toast before drinking; read as Geese, who is about to drink. |
| ch11-p0147 | Badigadi | Curious reaction as Geese gets up with his tankard; the line is untagged. |
| ch11-p0160 | Adviser | Unnamed attendant who warns Badigadi that Geese may die; the speaker is never named. |
| ch11-p0163 | Adviser | Unnamed attendant who suggests using magic on Geese; the speaker is never named. |

## Conventions used

* **Canonical names.** `Rudeus` (never Rudy), `Sylphiette` (never Sylphie). In-world names are
  kept as the book writes them: `Perugius`, `Sylvaril`, `Nanahoshi`, `Kishirika`, `Atofe`,
  `Badigadi`, `Geese`, `Soldat`, `Nina`, `Ghislaine` (referenced only), `Man-God`, `Ruijerd`.
* **Generic labels** for speakers the text never names. They are used consistently across the
  volume: `Adventurer` (unnamed Amazon party members and the North God fan in ch08),
  `Soldier` (the rough men in Badigadi's hall in ch11), `Swordsman` (the Sword Sanctum townsmen
  who duel and the practitioners in the training hall), `Crowd` (the murmuring townspeople in
  the Sword Sanctum), `Student` (the young man who shovels snow and spars with Eris),
  `Mercenary` (the Markien men who watch Eris in ch09), `Missionary Knight` (the knights of
  Millis in ch08–ch09), `Party Leader` (the unnamed woman leading the Amazons),
  `Adviser` (the unnamed attendant with Badigadi in ch11-s02), `Black Knight` (Atofe's
  armoured underlings in Necross Fortress), `Skyfolk` (the guard at the gate of Aluce),
  `Receptionist` (the Orsted Corporation receptionist), `Gigantic Jaw` (the A-rank monster on
  Aluce Hill) and `Sieg` (the baby, whose cries and gurgling are vocalizations).
* **Battle cries and vocalizations** belong to the fighter who shouts them: `Eris` shouts
  "Gaaaaaaaaah!" at the Gigantic Jaw, the `Gigantic Jaw` answers with its own bellow,
  `Sieg` cries "Owwwchgggh!" and "Mmahhh, waaaah!", and `Geese` groans "Urp…" and "Bleeeegh!"
  while he is being sick. Each of these carries a note marking it as a vocalization rather
  than speech.
* **Re-typed blocks (`type: "narration"`).** Nine blocks that the first-pass classifier typed as
  `speech` are pure narration or inner monologue and keep their speaker so the reader still
  knows whose thought it is: `ch01-p0033`, `ch02-p0180`, `ch05-p0088`, `ch06-p0052`,
  `ch06-p0054`, `ch07-p0067`, `ch09-p0050` (all Rudeus), `ch04-p0174` (Nanahoshi's announcement
  wrapped in narration) and `ch11-p0202` (Badigadi's retelling, where the quoted phrase is the
  hero's title "Golden Knight Aldebaran"). Each has a note explaining the correction.
* **`mixed` blocks.** 352 blocks interleave narration, action beats or speech tags with the
  quoted line. The speaker is always the person whose words are quoted.
* **Recollections.** The extra chapter is largely a story told by Badigadi, so the dialogue of
  ch11-s03 (the Second Great Human-Demon War: the Man-God, Badigadi as the "Demon King of
  Wisdom", and Kishirika) is flagged `recollection`, as is the unnamed stranger who relayed the
  Man-God's advice to Badigadi in ch11-s04 (`ch11-p0290`).
* **Point of view.** The scene-level POV in `data/volume23.classified.json` is correct for every
  scene (ch01-s01, ch02-s01 and ch02-s02 in Sylphiette's POV; ch07-s01 and ch07-s02 in Eris's
  POV; ch11-s01 and ch11-s02 in Geese's POV; ch11-s03 to ch11-s05 in Badigadi's POV), so no
  `pov`/`chapterPov` overrides were needed. The chapter-level POV in `scripts/volumes.py`
  (ch01/ch02 = Sylphiette, ch07 = Eris, ch11 = Geese) was left untouched.
* **Scene metadata.** `data/scene_metadata23.json` maps all 51 scene IDs to a real location
  (Rudeus's house in Sharia, the Chaos Breaker floating fortress, the Divine Continent, the city
  of Aluce, Aluce Hill, the Sword Sanctum, the town of Kide, Hammerpolka, the Thunderbolt clan
  room, Necross Fortress, the Superd village, the Biegoya Region estate) and a cast that includes
  every speaker of the scene, the scene POV, and the characters who are present but silent.
* **Known validator warning.** `ch11-p0290` carries the speaker `Stranger`, a figure who is
  never named in the volume; because that speaker never has a speech block of his own, the
  validator prints one informational warning ("mixed-block speaker not indexed: Stranger").
  Every other block validates cleanly.
