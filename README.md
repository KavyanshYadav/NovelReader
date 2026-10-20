# Mushoku Tensei Reader

A reader-friendly, offline edition of *Mushoku Tensei: Jobless Reincarnation* Volumes 15–26, built from the supplied EPUBs. The project ships a home page for the library and, behind it, a scrolling edition and a fullscreen, scene-at-a-time reader with a timeline.

> The project folder is still named `Volume 15 Reader` from when it covered a single book, but it now ships twelve volumes behind a volume switcher.

## Open it

| Page | File | What it is |
| --- | --- | --- |
| Home | `web/index.html` | The library front page: every volume, its cover, and a link into the reader |
| Reader | `web/reader.html` | The scrolling edition and the fullscreen scene reader |

Open `web/index.html` directly in a modern browser — no server, build step, or network connection is required. Keep `web/data.js`, `web/volumes/`, and `web/images/` beside it.

The original EPUBs are left untouched.

## Host it on the web

The whole site is static: plain HTML, CSS and JavaScript with no dependencies, no build step and no runtime API calls, so any static host works.

| Host | How |
| --- | --- |
| **GitHub Pages** | The `Deploy to GitHub Pages` workflow publishes `web/` on every push to `main`. `.nojekyll` is included so the `volumes/` folder is not filtered out. |
| **Vercel** | `vercel.json` publishes `web/` as the output directory, and the `Deploy to Vercel` workflow redeploys it on every push. It needs the `VERCEL_TOKEN` secret plus the `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` repository variables. |
| **Netlify / Cloudflare Pages** | Set the publish directory to `web`. The included `_headers` file sets long-lived caching for the volume data and artwork and revalidates the HTML. |
| **Any static host** | Copy `web/` to the web root. |

```bash
# Build a publishable copy (adds sitemap.xml and absolute metadata)
python3 scripts/deploy.py --out dist --base-url https://reader.example.com

# Preview it exactly as a host would serve it
python3 -m http.server --directory dist 8000
```

`web/` is the publish root. The artwork is re-encoded for the web (85.8 MB down to 24.8 MB) by `scripts/optimize_images.py`, which the export step runs for you.

Deep links work: `reader.html?volume=21` opens volume 21 directly, and the reader keeps the volume in the address bar as you switch, so links can be shared.

`scripts/deploy.py --base-url` rewrites the canonical link, the social preview tags and the sitemap to absolute URLs; leave it out and the relative URLs still resolve on any host.

## Choosing a volume

The sidebar (or the mobile contents drawer) has a **Volume** switcher. Switching volumes reloads the chapters, table of contents, cover art, statistics, and the scene timeline, and remembers where you were in each volume separately. Each volume is a separate file, so only the book you are reading is loaded.

| Volume | Chapters | Words | Scenes | Dialogue lines | Speakers |
| --- | --- | --- | --- | --- | --- |
| 15 | 14 | 74,846 | 38 | 1,274 | 30 |
| 16 | 10 | 71,000 | 24 | 1,382 | 24 |
| 17 | 15 | 73,808 | 32 | 1,249 | 33 |
| 18 | 13 | 74,109 | 29 | 1,188 | 44 |
| 19 | 14 | 78,784 | 31 | 1,285 | 29 |
| 20 | 12 | 68,178 | 41 | 1,145 | 44 |
| 21 | 11 | 64,594 | 35 | 941 | 29 |
| 22 | 14 | 62,258 | 35 | 1,337 | 46 |
| 23 | 11 | 68,792 | 51 | 1,153 | 38 |
| 24 | 12 | 59,404 | 31 | 1,185 | 49 |
| 25 | 11 | 54,277 | 41 | 842 | 22 |
| 26 | 10 | 48,538 | 35 | 615 | 29 |
| **Total** | **147** | **798,588** | **423** | **13,596** | — |

## Reader features

- **Home page** listing all twelve volumes with their covers, chapter and scene counts, a one-line summary, and a direct link into each book.
- **Scrolling edition** with a sidebar table of contents, chapter illustrations, scene headers, reading progress, saved scroll position, and a mobile contents drawer.
- **Speaker-attributed dialogue** with color-coded inline labels. Mixed narration/quotation paragraphs are marked `quoted` rather than attributed as fully spoken lines.
- **Document styling** for diary entries, letters, inscriptions, remembered quotations, imagined speech, and silence. Volume 18 opens with Rudeus's diary as a full document panel.
- **Fullscreen scene reader** that shows only the currently selected scene. The bottom timeline maps every scene in the volume; tick marks, chapter segments, and the progress rail are clickable.
- **Immersive fullscreen chrome** — entering native fullscreen automatically hides the scene-reader header and timeline so they do not obstruct the prose. Use `C`, the small chevron button, or the focus-mode controls to bring them back.
- **Keyboard-first navigation** for moving between scenes, chapters, and reading modes.
- **Reading settings** for theme, typeface, text size, line height, reading width, and narration alignment. Settings are saved in `localStorage` and shared across volumes.
- **Responsive layout** with a mobile contents drawer, a bottom-sheet settings panel, and a fixed-width reading column on larger screens.
- **Light and dark paper themes**, reduced-motion support, print styles, and accessible focus handling.

## Hotkeys

| Key | Action |
| --- | --- |
| `F` | Open the focus reader from the scrolling edition; toggle native fullscreen inside the focus reader |
| `←` / `→` | Previous / next scene in the focus reader |
| `H` / `L` | Previous / next scene in the focus reader |
| `Home` / `End` | First / last scene in the focus reader |
| `C` | Hide / show the focus-reader header and timeline |
| `S` or `?` | Open reading settings |
| `T` | Toggle light / dark theme |
| `+` / `−` | Increase / decrease text size |
| `[` / `]` | Previous / next chapter in the scrolling edition |
| `Esc` | Close settings, then the focus reader, then the mobile drawer |

## Reading settings

Open settings with the gear button, `S`, or `?`.

| Setting | Options |
| --- | --- |
| Theme | Light, Dark |
| Typeface | Serif, Sans, Mono |
| Text size | 17–24 px |
| Line height | Compact, Cozy, Airy |
| Reading width | Narrow, Standard, Wide |
| Narration alignment | Justified, Left |

The current scene and reading position are stored per volume. Use **Reset to defaults** to restore the original paper theme and typography.

## Data

`data/volume15.json` … `data/volume26.json` are the sources of truth for the reader. `web/data.js` and `web/volumes/` are generated from them.

- Every live dialogue block has a speaker name
- Narration that contains quoted dialogue is annotated with the speaker and flagged as embedded dialogue
- Diary entries, letters, inscriptions, remembered quotations, imagined speech, and silence are kept distinct from live dialogue
- Every scene carries a location and a cast list

### Structure

```
meta
stats
speakers[]
chapters[]
  scenes[]
    location
    cast[]
    speakers[]
    wordCount
    speechCount
    blocks[]
```

Each block has:

| Field | Meaning |
| --- | --- |
| `id` | Stable block ID, e.g. `ch03-p0124` |
| `type` | `narration`, `speech`, `diary`, `letter`, `silence`, `inscription`, `quotation`, `thought`, `spacer`, or `image` |
| `text` | Plain text |
| `html` | Original inline HTML where available |
| `speaker` | Canonical speaker name for live dialogue |
| `speakerConfidence` | `high`, `medium`, or `low` |
| `mixed` | The block mixes narration and quoted speech |
| `recollection` | A remembered quotation rather than speech happening now |
| `imagined` | An imagined or unspoken line |
| `embeddedDialogue` | A narration block that contains quoted live dialogue |
| `attributionNote` | Short note explaining a non-obvious label |

Scene `cast` lists characters who are present, not only those who speak. `speakers` lists the characters who actually speak in that scene.

## Attribution

Speaker labels were assigned by reading the dialogue in context, chapter by chapter, using scene POV, turn-taking, vocatives, action beats, and explicit speech tags. Canonical names are used (`Rudy` → `Rudeus`, `Sylphie` → `Sylphiette`).

Volume 15 has nine lines marked `medium` confidence that can be reviewed individually:

- `ch05-p0090`
- `ch07-p0017`, `ch07-p0018`, `ch07-p0019`
- `ch07-p0287`, `ch07-p0291`, `ch07-p0293`, `ch07-p0297`
- `ch08-p0079`

The newer volumes use the same scheme, with `medium` reserved for lines where the text does not make the speaker certain (unnamed voices in a crowd, duelling chants, a flashback whose speakers are never named, or a story inside a story). Per-volume notes are in `data/attributionNN/REPORT.md`:

| Volume | High | Medium | Low |
| --- | --- | --- | --- |
| 15 | 1,291 | 9 | 0 |
| 16 | 1,438 | 5 | 1 |
| 17 | 1,215 | 39 | 2 |
| 18 | 1,177 | 11 | 0 |
| 19 | 1,287 | 3 | 0 |
| 20 | 1,153 | 5 | 0 |
| 21 | 957 | 14 | 0 |
| 22 | 1,367 | 3 | 0 |
| 23 | 1,207 | 14 | 0 |
| 24 | 1,210 | 8 | 0 |
| 25 | 845 | 22 | 0 |
| 26 | 625 | 6 | 0 |

## Rebuilding and exporting

The pipeline is shared by every volume. Each stage takes a `--volume` argument (15–26).

```bash
python3 scripts/extract.py --volume 16      # EPUB -> data/volume16.source.json
python3 scripts/classify.py --volume 16     # block types -> data/volume16.classified.json
python3 scripts/build.py --volume 16        # + attribution + scene metadata -> data/volume16.json
python3 scripts/validate.py --volume 16     # schema, coverage and cast checks
python3 scripts/export_web.py               # web/data.js + web/volumes/*.js + web/images/vol*/
```

To run every stage for every volume at once:

```bash
python3 scripts/rebuild_all.py
python3 scripts/rebuild_all.py 19 20 21     # only these volumes
```

To publish the site:

```bash
python3 scripts/deploy.py --out dist --base-url https://reader.example.com
```

- `scripts/volumes.py` — volume configuration: EPUB path, chapter list, POV, special ranges
- `scripts/extract.py` — EPUB to a normalized block list, split into scenes
- `scripts/classify.py` — marks diary, letter, inscription, silence, speech, and quotation blocks
- `scripts/build.py` — merges the classified data, attribution files, and scene metadata
- `scripts/validate.py` — checks coverage, schema consistency, cast membership, and counts
- `scripts/export_web.py` — writes `web/data.js` and extracts cover/interior art to `web/images/<slug>/`

### Reviewing attribution

```bash
python3 scripts/chapter_report.py --volume 16 --chapter ch09 --out /tmp/ch09.txt
python3 scripts/attribution_review.py --volume 16 --chapter ch09 --out /tmp/review.txt
python3 scripts/audit_attribution.py --volume 16
```

- `chapter_report.py` prints a chapter with stable block IDs for contextual reading
- `attribution_review.py` prints the assigned speaker next to every line
- `audit_attribution.py` flags lines whose own text contradicts the label
- `apply_compact.py` / `apply_corrections.py` write reviewed changes back to the attribution files
- `make_scene_metadata.py` merges hand-written locations with the detected cast

### Data layout

```
data/
  volumeNN.source.json      extracted blocks
  volumeNN.classified.json  classified blocks
  volumeNN.json             finished volume
  attribution/              per-chapter speaker maps for volume 15
  attributionNN/            per-chapter speaker maps for volume NN
  scene_metadata.json       scene locations and casts for volume 15
  scene_metadataNN.json     scene locations and casts for volume NN
```

## Reader files

- `web/index.html` — the home page
- `web/home.css`, `web/home.js` — home page styling and the volume list
- `web/reader.html` — the reader shell, controls, and focus-reader markup
- `web/styles.css` — paper themes, typography, layout, timeline, settings, and responsive styles
- `web/app.js` — rendering, volume switching, speaker labels, timeline navigation, hotkeys, settings, theme/font controls, and scroll restore
- `web/data.js` — generated manifest that lists every bundled volume
- `web/volumes/volNN.js` — generated embedded data for one volume, loaded the first time you open it
- `web/images/volNN/` — extracted cover and interior images per volume
- `web/favicon.svg`, `web/manifest.webmanifest`, `web/robots.txt`, `web/404.html`, `web/_headers`, `web/.nojekyll` — the small extras a static host expects

The volume data is split into one file per volume so the reader only loads the
book you are reading. Opening a volume for the first time fetches
`web/volumes/volNN.js`; after that it is cached by the browser.
