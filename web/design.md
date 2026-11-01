# Design system: Mushoku Tensei Reader

## Direction

Editorial library and long document reader. The volume index is the primary landing surface; the reader is a quiet, focused companion. Specimen theme with a cool ink-blue accent, oat paper in light mode, and high-contrast local serif typography. No remote assets or font requests are required.

## Tokens

`tokens.css` owns colors, typography, spacing, containers, motion, and stacking levels. Keep presentation values in those tokens. `base.css` owns shared document defaults and keyboard focus. `home.css` and `styles.css` own page and component layouts.

## Color and type

- Paper: warm off-white (`--color-paper`), with two stepped surfaces.
- Ink: near-black text and two quieter ink levels.
- Accent: cool blue for interactive emphasis and focus.
- Display and reading prose: system-supported book serif stack.
- Interface and controls: system sans-serif stack.
- Measured values and code: system monospace stack.
- Dark mode reassigns the same semantic tokens in `styles.css`.

## Layout

- Home: masthead, progress action, then a four-column index of real volume covers and summaries; responsive at tablet and phone widths.
- Reader: fixed contents rail on wide screens, sticky reading controls, cover and volume introduction, then a centered long-form chapter measure.
- Focus reader: scene text between a small control header and a chapter-aware timeline.
- Settings and audio remain available as existing reader interactions.

## Interaction

Square, hairline controls use visible keyboard focus. Theme, typeface, measure, alignment, and reading progress retain their existing storage behavior. Reduced motion disables transitions. Print hides app chrome and preserves chapter structure.

## Content and accessibility

Real volume covers and source copy remain in use. Existing IDs, links, manifests, script loading, encrypted content pipeline, settings, and reader navigation remain wired. Keep skip links, semantic headings, button names, scene labels, and responsive reflow.
