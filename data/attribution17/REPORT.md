# Volume 17 — Speaker Attribution Report

Scope: `data/attribution17/ch01.json` … `ch15.json` plus `data/scene_metadata17.json`
(chapters 7–15 and the scene metadata were produced in this pass; ch01–ch06 were already
complete and were used as the style reference).

## Coverage

| Item | Count |
| --- | --- |
| Classified speech blocks | 1,256 |
| Attributed speech blocks | 1,256 (100%) |
| Missing attributions | 0 |
| Blocks with no `speaker` | 0 |
| Scenes with location + cast | 32 |
| Distinct speakers | 33 |
| Blocks mixing narration and dialogue (`mixed`) | 251 |
| Blocks re-typed away from `speech` | 7 |

Checks:

```
python3 scripts/check_attribution.py --volume 17   # "Attribution coverage complete."
python3 scripts/build.py --volume 17                # 15 chapters | speech 1249 | attributed 1249
python3 scripts/validate.py --volume 17             # "Validation passed."
```

The built volume reports 1,249 speech blocks because seven blocks that the classifier
marked as `speech` were re-typed (see *Type corrections*). All 1,256 originally classified
speech blocks still carry a speaker in the attribution files.

## Top speakers

| Speaker | Lines | Speaker | Lines |
| --- | --- | --- | --- |
| Rudeus | 259 | Darius | 38 |
| Ariel | 219 | Reida | 32 |
| Orsted | 104 | Drunkard | 28 |
| Eris | 102 | Triss | 27 |
| Sylphiette | 93 | Roxy | 25 |
| Luke | 65 | Perugius | 13 |
| Ghislaine | 60 | Grabel | 11 |
| Auber | 51 | Pilemon | 10 |
| Isolde | 42 | Noble | 10 |

Remaining speakers: Nucklegard 9, Aisha 9, Crowd 8, Invisible Stranger 8, Gard 7,
Wi Taa 6, Sylvaril 4, Bandit 3, Freitus 3, Guard 3, Ellemoi 2, Lilia 2, Cleane 1,
Matsukaze 1, Bartender 1.

## Generic speaker labels

Unnamed speakers use the same labels across the whole volume:

- `Crowd` — the Ars street crowds cheering Ariel, Luke and Sylphiette (ch07).
- `Noble` — unidentified guests in the Silver Palace reception hall (ch09, ch10).
- `Guard` — palace guards and the silver-armored knights who burst into the hall (ch10).
- `Bandit` — the smugglers' gang in the Red Wyrm's Whiskers (ch05, ch06).
- `Drunkard` / `Invisible Stranger` — the two voices in the extra chapter (ch15).
- `Bartender` — the POV narrator of the extra chapter (ch15).
- `Matsukaze` — Rudeus' horse, which neighs once in ch07.

Canonical names are used throughout (`Rudeus`, never Rudy; `Sylphiette`, never Sylphie).
Louise-style nicknames spoken by characters (`Fitz`, `Mad Dog`, `Mad Dog`) were normalized
to the canonical name of the person being addressed.

## Type corrections

Seven blocks were misclassified by the automated classifier; each carries a `type`
override and an explanatory `note`:

- `ch05-p0010` → `narration` (no dialogue present).
- `ch06-p0100`, `ch06-p0146` → `thought` (Rudeus's internal asides).
- `ch09-p0173` → `narration` with `embeddedDialogue` (a noble's murmured aside).
- `ch10-p0075` → `thought` (Rudeus's aside that also quotes Perugius's imagined line).
- `ch12-p0109`, `ch12-p0138` → `thought` (Rudeus's internal asides).

## Medium- and low-confidence labels

39 blocks are marked `medium`, 2 are marked `low`. They are listed here so they can be
reviewed individually.

Low confidence:

- `ch02-p0050` — the objector at the war council is not named; context points to Luke.
- `ch06-p0006` — unattributed exclamation at first sight of the lake (Rudeus).

Medium confidence:

- `ch02-p0077`, `ch02-p0078` — battle cries as Eris and Ghislaine charge the ambush.
- `ch07-p0013` — "Whoa." is shared by Rudeus and Eris; given as Rudeus's reaction.
- `ch07-p0071` — "Hm?!" when the novice knight breaks from the patrol.
- `ch07-p0073` — "Oh my!" as the armored novice halts; given as Isolde.
- `ch08-p0093` … `ch08-p0101` — the Nucklegard twins trade taunts; which twin speaks
  which line is not certain.
- `ch08-p0145` — "Tch!" while Auber deflects the spell; could be Rudeus.
- `ch08-p0180`, `ch08-p0183` — the end-of-battle banter; speakers are not named.
- `ch10-p0082` — "Hm?!" as Rudeus braces to act.
- `ch10-p0084` — "Good lord, is that…?" when the hall starts to tremble.
- `ch10-p0119` — the terror scream when Orsted enters the hall.
- `ch10-p0155` — "…I see them!" when the fleeing pair is spotted.
- `ch10-p0218`, `ch10-p0219` — the paired grunts when the glue trap springs.
- `ch10-p0268` — two clipped reactions in one block, both read as Auber's.
- `ch10-p0275` — "Hm?!" after Darius is blinded.
- `ch10-p0287` — "…Splendidly done." as Auber collapses.
- `ch10-p0311` — "…Huh?" at the poisoned wound.
- `ch13-p0008` — "We're ready." is spoken by Rudeus and Eris together.
- `ch13-p0125` — the soft sound as Sylphie leaves the bed.
- `ch14-p0007` — "We're hooome." on arriving home.
- `ch14-p0015`, `ch14-p0018` — the short exchange about Aisha's hand mirror.
- `ch15-p0021`, `ch15-p0022`, `ch15-p0025`, `ch15-p0026`, `ch15-p0027`, `ch15-p0029`,
  `ch15-p0036`, `ch15-p0042` — which half of the extra chapter's two-sided conversation
  each line belongs to (see notes below).

## Notes

- **ch07** — Isolde Cluel is the Water King who recognizes Eris in the streets of Ars;
  "Isolde" is used everywhere. The horse's neigh in `ch07-p0117` is credited to
  Matsukaze, who pushes Eris in the next paragraph.
- **ch08** — the two North King twins introduce themselves as "Nucklegard" and answer to
  "Nuckle" and "Gard"; the labels follow the text ("Hey, Nuckle…" / "You're so smart,
  Gard."). The rest of the chapter's action beats are clear from the narration.
- **ch09** — Pilemon Notos Greyrat, Freitus Purplehorse (head of House Purplehorse),
  Grabel Zafin Asura, High Minister Darius and Perugius Dola are all named in the
  scene, so they carry their own labels; the unidentified guests at the table are
  `Noble`.
- **ch10** — the Water God is "Reida" (Reida Lia, "the Water God Reida" in ch09–ch10).
  Auber is the North Emperor; Wi Taa is the halfling North King; the princess and
  Eris/Ghislaine trade blows with the assassins Darius sent.
- **ch11** — the chapter is narrated by Luke, so every "I" is Luke. Luke's hostage
  scene with Ariel, and Sylphiette's answer, are the emotional core of the chapter.
- **ch12** — Orsted explains his time loop to Rudeus in a servants' cemetery catacomb;
  Isolde visits the mansion and sizes Rudeus up; the figurine business is negotiated
  with Ariel in her chambers.
- **ch13** — Ghislaine's last training session with Eris, then Luke's farewell to
  Sylphiette, then Sylphiette's night-time confession in Perugius' castle.
- **ch14** — the homecoming in Sharia, Rudeus's talk at Paul's grave.
- **ch15** — the extra chapter is deliberately unnamed. The visible drunkard is
  `Drunkard`; the other half of the conversation, the unseen man in the empty chair, is
  `Invisible Stranger`. The two voices were separated by register (slurred and
  colloquial versus measured and formal), by turn-taking, and by the content of the
  exchange (the drunkard asks for help; the stranger is the one being hunted and is
  assembling a team). Both halves remain `medium` where the split is not certain.
