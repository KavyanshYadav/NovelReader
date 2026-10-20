# Volume 24 — Speaker Attribution Report

*Mushoku Tensei: Jobless Reincarnation* Volume 24, "A Strategy Meeting / A Sought-After Item / …
/ Disappearance" (ch01–ch12, including the two interludes).
Reader data set: `data/volume24.json`.

## Coverage

| Metric | Value |
| --- | --- |
| Chapters | 12 (ch01–ch12) |
| Scenes | 31 |
| Blocks total | 2,108 (850 narration, 1,185 speech, 2 silence, 71 spacer) |
| Speech blocks in the classified data | 1,188 |
| Speech blocks after the `type` re-corrections | 1,185 |
| Attributed speech blocks | 1,185 (100.0%) |
| Distinct speakers | 49 |
| `mixed` blocks | 499 |
| `recollection` blocks | 13 |
| `embeddedDialogue` blocks | 35 (23 narration blocks + 12 speech blocks) |
| `type` overrides | 3 |
| Blocks carrying a `note` | 63 |
| Medium / low confidence blocks | 9 / 0 |

Validation status:

```
python3 scripts/check_attribution.py --volume 24   -> Attributed: 1188 / 1188 (coverage complete)
python3 scripts/make_scene_metadata.py --volume 24 --file /tmp/opencode/vol24-scenes.json
python3 scripts/build.py --volume 24                -> Wrote data/volume24.json
python3 scripts/validate.py --volume 24            -> Validation passed.
```

`check_attribution.py` also lists 30 "extra/unknown keys". These are **not** errors: they are
narration blocks that contain quoted live speech, listed in the attribution files with
`embeddedDialogue: true` so the reader can show the speaker of the quoted fragment (the same
approach already used for volume 16). Twelve further `embeddedDialogue` entries sit on
speech-typed blocks whose text mixes narration with a quoted line.

## Top speakers (volume)

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 461 | Chandle | 103 |
| Ruijerd | 62 | Cliff | 60 |
| Orsted | 57 | Norn | 56 |
| Paul | 26 | Roxy | 25 |
| Galixon | 23 | Sandor | 21 |
| Zanoba | 21 | Eris | 18 |
| Vita | 18 | Informant | 16 |
| Ariel | 12 | Chief | 12 |
| Dohga | 12 | Sara | 12 |
| Zenith | 12 | Elder | 11 |
| Faria | 11 | King | 11 |
| Lucie | 11 | Doctor | 10 |
| Gall Falion | 10 | Old Woman | 10 |
| Linia | 9 | Superd Warrior | 9 |
| Clerk | 7 | Server | 6 |
| Villager | 6 | Alexander Rybak | 5 |
| Receptionist | 5 | Child | 4 |
| Ginger | 4 | Man-God | 4 |
| Ogre | 4 | Sylphiette | 4 |
| Lilia | 3 | Aisha | 2 |
| Geese | 2 | Knight Captain | 2 |
| Mercenary | 2 | Official | 2 |
| Elinalise | 1 | Guard | 1 |
| Julie | 1 | Monster | 1 |
| Raxos's Friend | 1 | | |

## Chapter map

| Chapter | Title | Scenes | Speech | Distinct speakers |
| --- | --- | --- | --- | --- |
| ch01 | A Strategy Meeting | 3 | 101 | Chandle, Dohga, Eris, Orsted, Receptionist, Roxy, Rudeus, Sylphiette, Zanoba |
| ch02 | A Sought-After Item | 2 | 108 | Chandle, Dohga, Informant, Ogre, Rudeus, Server |
| ch03 | A Sought-After Person | 2 | 67 | Chandle, Dohga, Mercenary, Monster, Old Woman, Rudeus, Superd Warrior |
| ch04 | The Superd Village | 1 | 127 | Chandle, Chief, Dohga, Elder, Rudeus, Ruijerd, Superd Warrior |
| ch05 | Abyssal King Vita | 7 | 183 | Aisha, Ariel, Child, Knight Captain, Lilia, Linia, Paul, Rudeus, Ruijerd, Sara, Vita, Zenith |
| ch06 | The Plague | 2 | 122 | Chandle, Cliff, Doctor, Norn, Orsted, Receptionist, Rudeus |
| ch07 | The Genius | 2 | 155 | Child, Cliff, Doctor, Elder, Elinalise, Norn, Orsted, Rudeus, Ruijerd, Villager |
| ch08 | Interlude: Somebody to Someone | 3 | 36 | Cliff, Lucie, Norn |
| ch09 | Interlude: Vita and Raxos | 1 | 8 | (all remembered speech, see below) |
| ch10 | The Capital | 2 | 117 | Clerk, Dohga, Guard, King, Norn, Official, Orsted, Rudeus, Ruijerd, Zanoba |
| ch11 | Four-Day Educational Superd Village Tour | 3 | 103 | Alexander Rybak, Chief, Galixon, Gall Falion, Rudeus, Sandor, Superd Warrior |
| ch12 | Disappearance | 3 | 58 | Eris, Faria, Ginger, Julie, Ogre, Roxy, Zanoba |

## Uncertainty ledger

No `low`-confidence labels are used in this volume. All 8 flagged entries are `medium`:

| Block | Speaker | Reason |
| --- | --- | --- |
| ch01-p0057 | Roxy | Read as Roxy continuing her argument; Sylphie's next line agrees with Roxy. |
| ch03-p0061 | Old Woman | The village's original proclamation as retold by the old woman; the line is untagged. |
| ch03-p0116 | Rudeus | Read as Rudeus voicing the concern he has just been thinking; the line is untagged. |
| ch03-p0117 | Chandle | Chandle asking Rudeus whether he wants to turn back; the line is untagged. |
| ch05-p0187 | Vita | The figure in the dream drops the act and names Abyssal King Vita; read as Vita himself speaking. |
| ch11-p0011 | Galixon | Blunt interjection from one of the two envoys; the speaker is not named. |
| ch11-p0044 | Galixon | Short remark by one of the two envoys; the speaker is not named. |
| ch11-p0060 | Galixon | One of the two envoys remarks on the Millis priest; the speaker is not named. |
| ch11-p0061 | Sandor | One of the two envoys remarks on the elf; the speaker is not named. |

The four ch11 entries are the only places where the reader cannot tell which of the two
disguised envoys spoke. Where the text itself makes the turn clear (a "Sandor said" tag, a
question aimed at the other man) the two are separated; the flagged lines are the ones that
could belong to either man.

## Conventions used

* **Canonical names.** `Rudeus` (never Rudy), `Sylphiette` (never Sylphie). In-world names are
  kept as the book writes them: `Chandle`, `Dohga`, `Ruijerd`, `Norn`, `Cliff`, `Elinalise`,
  `Zenith`, `Ariel`, `Aisha`, `Lilia`, `Paul`, `Linia`, `Pursena`, `Ginger`, `Julie`,
  `Vita`, `Geese`, `Man-God`, `Nanahoshi`, `Faria`.
* **Generic labels** for speakers the text never names, used consistently across the volume:
  `Old Woman` (the villager who defends the People of the Forest in ch03), `Mercenary` (the
  bounty hunters in the village square), `Superd Warrior` (the Superd who guides Rudeus to the
  village and mans the gate), `Chief` (the head of the Superd village), `Elder` (the elder
  Superd who speaks in the chief's hall and in the medical centre), `Villager` (the unnamed
  Superd patients in the medical centre), `Child` (the Superd girl in ch07 and the beastfolk
  children in Rudeus's dream), `Doctor` (the Asuran medical team), `Clerk` (the mustachioed man
  at the palace reception desk), `Official` (the palace official who runs the audience),
  `Guard` (the Biheiril soldier sent with Rudeus), `King` (the King of the Biheiril Kingdom),
  `Knight Captain` (the Asuran knight captain in Rudeus's dream), `Informant` (the broker in
  the Irelil tavern), `Server` (the ogre waitress in the same tavern),
  `Receptionist` (the Orsted Corporation receptionist), `Monster` (the invisible wolf),
  `Ogre` (the unnamed ogres of Biheiril — the ogre townsman in Irelil in ch02 and the red ogre
  that storms the Orsted Corporation office in ch12, who may be acting for the Ogre God) and
  `Raxos's Friend` (the unnamed friend of the Death God whose bones became the Bone Ring).
* **The receptionist's name.** In ch01 and ch06 she is `Receptionist`, because Rudeus does not
  know her name ("Little Miss Elf from the reception desk… What's his name again?"). In ch12
  she is `Faria`, the name the narration gives her, and the chapter itself explains the change
  ("Unbeknownst to Rudeus, Fariastia was the real name of Little Miss Elf, the receptionist").
* **Battle cries and vocalizations** belong to the fighter who shouts them: `Rudeus` cries
  "Aaaggghhh!" when Gall Falion cuts off his arms on the bridge over the Earthwyrm Ravine;
  `Faria` squeals "Eep!" and screams "Aaaaagh!" when the ogre throws her out of the window;
  `Linia`'s "Hissss!" is a beastfolk hiss.
* **Re-typed blocks (`type: "narration"`).** Three blocks that the first-pass classifier typed as
  `speech` are pure narration or inner monologue and keep their speaker so the reader still
  knows whose thought it is: `ch01-p0122` (Rudeus's aside about the title "Chairman"),
  `ch03-p0041` (Rudeus's reasoning about the old woman's age) and `ch04-p0176` (Rudeus's aside
  about Abyssal King Vita and the labyrinth called "Hell"). Each has a note explaining the
  correction.
* **`mixed` blocks.** 499 blocks interleave narration, action beats or speech tags with the
  quoted line. The speaker is always the person whose words are quoted.
* **Recollections.** The Vita interlude (ch09) is a life story that Vita reviews in the Hell
  Labyrinth, so all of its dialogue — the Man-God, Geese and Raxos's friend — is flagged
  `recollection` and rendered as remembered speech. The same flag is used for Zenith's
  remembered line in Rudeus's flashback (ch05-p0019) and for the old woman's retelling of the
  village's history in ch03.
* **Dreams are not recollections.** ch05 is a sequence of five dream worlds built by Abyssal
  King Vita. The dialogue inside the dreams is live speech inside the dream, so it is not
  flagged `recollection`; the scene locations in `data/scene_metadata24.json` name each one as
  "A dream: …" so the reader can tell what is happening.
* **Disguises.** The two Biheiril envoys are labelled by the identities Rudeus knows them by
  at the time: `Galixon` and `Sandor` through ch11-s02 (the block in which they drop the
  disguise still carries the cover names, and the true names are spoken in the text), and
  `Gall Falion` and `Alexander Rybak` in ch11-s03, where the narration itself uses "Gall" and
  "Alexander".
* **Point of view.** The scene-level POV in `data/volume24.classified.json` is correct for every
  scene, including the two interludes (ch08 is Norn's, ch09 is Vita's), so no `pov`/`chapterPov`
  overrides were needed.
* **Scene metadata.** `data/scene_metadata24.json` maps all 31 scene IDs to a real location
  (the Orsted Corporation offices in Sharia, the Second City of Irelil, the Earthwyrm Ravine
  Village, the Superd village in the Forest of No Return, the Hell Labyrinth, the capital of the
  Biheiril Kingdom and its palace, the Third City of Heirulil) and a cast that includes every
  speaker of the scene, the scene POV, and the characters who are present but silent.
