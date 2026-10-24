# Style guide

## Charter

**What belongs:** How the product looks: color, type, spacing and the reusable components. Tokens and the rules for using them. Each component and when to use it.

**What does not:** Voice and word choice (BRAND.md). How a screen works.

**Level of detail:** Rules a builder can apply without asking, with the reason for each.

**Describes:** the stylesheet and component folders

**Sources:** the stylesheets and the live UI

## The style: Black Card, in Archivo

Ken chose this direction on 2026-10-24 at 12:28 PM. The source is [direction E in Archivo](../features/20261022.05_style_directions/round_2/direction_e_archivo/style_guide.html), and every value below comes from its CSS.

**The idea.** Tricorder should feel like a premium charge card crossed with a trading terminal. A warm graphite ground, off-white type, and one pale champagne metal kept to thin lines, so the product carries quiet wealth and then gets out of the way.

### Files

| File | What it is |
|---|---|
| [style/tricorder.css](style/tricorder.css) | The shared stylesheet. Tokens for dark and light, the fonts, base element styles, and every component class below. No Bootstrap. |
| [style/fonts/](style/fonts/) | Archivo and IBM Plex Mono as woff2, with each font's OFL licence. [SOURCES.md](style/fonts/SOURCES.md) records where each file came from. |
| [style/check_contrast.py](style/check_contrast.py) | Reads the tokens from tricorder.css and checks every text pairing. Run it after any colour change. |

To use the style, link `tricorder.css` and keep the `fonts/` folder beside it. The fonts load by relative URL, so nothing needs the network. Every class starts with `tc-` and every token with `--tc-`, so the file can sit beside an app's own CSS without clashing.

## Tokens

### Colour

Dark is the default. The light theme turns on when the system prefers light. `data-theme="light"` or `data-theme="dark"` on the `<html>` element overrides the system. The class `tc-dark` keeps one band dark inside the light theme; the homepage hero and closing band use it.

| Token | Dark | Light | Role |
|---|---|---|---|
| `--tc-ground` | `#131210` | `#ffffff` | Page ground. Warm near-black in dark, plain white in light. |
| `--tc-surface` | `#1a1916` | `#ffffff` | Panels and cards. In light a panel is held by its hairline, not a fill. |
| `--tc-surface-2` | `#211f1b` | `#f6f4ef` | Hover fill only. |
| `--tc-lit-top` | `#201e1a` | `#ffffff` | Top of the raised hero panel's gradient. |
| `--tc-lit-bottom` | `#171614` | `#ffffff` | Bottom of the raised hero panel's gradient. |
| `--tc-ink` | `#eeebe4` | `#1c1b18` | Headings, figures, primary text. |
| `--tc-ink-2` | `#bdb7ab` | `#47443d` | Body copy. |
| `--tc-ink-3` | `#9a9488` | `#6b675e` | Labels, axes, help text. |
| `--tc-rule` | `#2e2b26` | `#e6e2da` | Hairlines between rows and around panels. |
| `--tc-rule-2` | `#45413a` | `#cdc7ba` | Stronger hairline: inputs, chips, the range strip's track, a table's head row. |
| `--tc-accent` | `#d3bf8e` | `#85692f` | The metal. Champagne in dark, deeper brass in light so it reads on paper. Focus, metal labels, hover borders. |
| `--tc-accent-2` | `#e5d6ae` | `#6a5323` | The metal, one step further from the ground. |
| `--tc-btn-bg` | `#d3bf8e` | `#1c1b18` | Primary button fill. Champagne in dark, graphite in light. |
| `--tc-btn-bg-hover` | `#e5d6ae` | `#3a3731` | Primary button hover fill. |
| `--tc-btn-fg` | `#16140f` | `#eadbb4` | Primary button text. It does not change on hover. |
| `--tc-band` | `rgba(211, 191, 142, 0.20)` | `rgba(133, 105, 47, 0.14)` | A flat wash of the metal, for small demos and the source-panel highlight. |
| `--tc-band-edge` | `#b9a574` | `#8a6c2e` | The band's edge, and the outline of Ask the founder and a steered piece. |
| `--tc-band-fill` | `rgba(211, 191, 142, 0.20)` | `linear-gradient(180deg, #f4e8c4 0%, #dcc286 48%, #b99850 100%)` | The range strip's band. In light it is brushed brass so it reads as metal, not beige. |
| `--tc-glow` | `rgba(211, 191, 142, 0.55)` | `rgba(133, 105, 47, 0.35)` | The bright corner of the raised hero panel's edge. |
| `--tc-strong` | `#7dc4a0` | `#1e7550` | Looking strong, green flag, clean check. |
| `--tc-strong-bg` | `rgba(125, 196, 160, 0.12)` | `rgba(30, 117, 80, 0.08)` | Fill behind a looking-strong mark. |
| `--tc-weak` | `#f08c78` | `#b3402e` | Looking weak, red flag, a figure outside the band. |
| `--tc-weak-bg` | `rgba(240, 140, 120, 0.12)` | `rgba(179, 64, 46, 0.08)` | Fill behind a looking-weak mark. |
| `--tc-mixed` | `#93b2e6` | `#2d5c9c` | Mixed. A cool blue, so it never reads as the metal. |
| `--tc-mixed-bg` | `rgba(147, 178, 230, 0.12)` | `rgba(45, 92, 156, 0.08)` | Fill behind a mixed mark. |
| `--tc-thin` | `#aaa498` | `#6b675e` | Not enough in the room, and gaps. |
| `--tc-thin-bg` | `rgba(170, 164, 152, 0.10)` | `rgba(107, 103, 94, 0.08)` | Fill behind a not-enough mark. |

### Type scale

| Role | Class | Font and weight | Size | Leading | Tracking |
|---|---|---|---|---|---|
| Display (homepage hero only) | `tc-display` | Archivo 800 | 46 to 112px, `clamp(46px, 7.6vw, 112px)` | 0.94 | -0.045em |
| Page title | `tc-h1` | Archivo 800 | 44 to 80px, `clamp(44px, 6vw, 80px)` | 0.96 | -0.04em |
| Section heading | `tc-h2` | Archivo 800 | 32 to 52px, `clamp(32px, 4vw, 52px)` | 1.02 | -0.035em |
| Panel heading | `tc-h3` | Archivo 700 | 24px | 1.2 | -0.015em |
| Card title | `tc-h4` | Archivo 700 | 20px | 1.2 | -0.01em |
| Wordmark | `tc-brand` | Archivo 800 | 20px | 1 | -0.03em |
| Lede | `tc-lede` | Archivo 400 | 21px, 19px on phones | 1.45 | 0 |
| Ask the founder question | `tc-ask-question` | Archivo 500 | 18px | 1.4 | 0 |
| Body | (body) | Archivo 400 | 16px | 1.5 | 0 |
| Card body | `tc-body-2` | Archivo 400 | 15px | 1.5 | 0 |
| Table and small text | `tc-small` | Archivo 400 | 14px | 1.5 | 0 |
| Help | `tc-help` | Archivo 400 | 13px | 1.5 | 0 |
| Button | `tc-btn` | Archivo 600 | 15px, 14px small | 1 | 0.005em |
| Figure | `tc-pair-value` | IBM Plex Mono 500 | 26px, 20px small, 22px on phones | 1.1 | -0.02em |
| Data | `tc-mono`, `tc-meta` | IBM Plex Mono 400 | 12 to 13px | 1.3 to 1.45 | 0 |
| Label | `tc-eyebrow`, `tc-label` | IBM Plex Mono 400 or 500, capitals | 12px | 1 | 0.08em |
| Small label | table heads, strip labels | IBM Plex Mono 400, capitals for heads | 11px | 1 to 1.2 | 0.08em for heads |

### Spacing

One step scale. Use a token, never a raw number.

| Token | Value |
|---|---|
| `--tc-space-1` | 4px |
| `--tc-space-2` | 8px |
| `--tc-space-3` | 12px |
| `--tc-space-4` | 16px |
| `--tc-space-5` | 24px |
| `--tc-space-6` | 32px |
| `--tc-space-7` | 48px |
| `--tc-space-8` | 64px |
| `--tc-space-9` | 96px |

### Grid

| Token or class | Value | Use |
|---|---|---|
| `--tc-container`, `tc-container` | 1264px | 1200px of content plus 32px side padding on desktop. Padding drops to 16px under 992px. |
| `--tc-gutter`, `tc-grid` | 24px | One gutter on a 12-column grid. `tc-span-3` to `tc-span-9` set widths from 992px up; below that every column is full width. |

### Corners

| Token | Value | Use |
|---|---|---|
| `--tc-radius-s` | 4px | Marks and source chips. |
| `--tc-radius-m` | 8px | Buttons, inputs, stated-beside-found. |
| `--tc-radius-l` | 14px | Panels, cards, Ask the founder. |

Tables, rules and range strips stay square. The band and ticks inside a range strip round by 1 to 2px only to soften their ends.

### Lines

| Token | Value | Use |
|---|---|---|
| `--tc-hair` | 1px | Every line. |
| `--tc-rule` | colour | Between rows and around panels. |
| `--tc-rule-2` | colour | Inputs, chips, a table's head row, the strip's track. |
| `--tc-ink` as a line | colour | Opens a ruled list, full width. |
| `--tc-band-edge` | colour | The Ask the founder outline, a steered piece's outline, the band's edge. |
| `--tc-focus` | 2px | The focus ring, in `--tc-accent`, 2px off the element. |

### Shadows

| Token | Value | Use |
|---|---|---|
| `--tc-shadow-raised` | `0 1px 0 rgba(255,255,255,0.05) inset, 0 1px 2px rgba(0,0,0,0.35), 0 12px 32px -16px rgba(0,0,0,0.6)` | The homepage hero panel (`tc-lit`) only. |

Every other surface is flat, held by a hairline.

### Motion

`--tc-ease` is `.15s ease`, for colour and border changes on hover. Nothing moves when the reader asks for reduced motion.

## Type

**Archivo** carries the display, the headings and the body, at its normal width. Weights in use: 400 for body and ledes, 500 for the Ask the founder question, 600 for buttons and emphasis, 700 for card and panel headings, 800 for the display, page titles, section headings and the wordmark. Never use a wide or expanded cut, and never stretch a font with `font-stretch` or a transform. Ken reads them as stretched.

**IBM Plex Mono** carries every figure, file name, place and label. Weights in use: 400 for data and labels, 500 for figures and marks. Labels are capitals at 0.08em tracking.

**Tabular figures.** Numbers sit in Plex Mono, where every digit is the same width, so columns line up. The stylesheet also turns on `font-variant-numeric: tabular-nums` for tables, the range strip and stated-beside-found, so any Archivo number there lines up too.

**Tight headlines.** Large type uses negative tracking and leading under 1.05. Loose leading on a big headline looks unfinished.

## Components

Each component is a class in [tricorder.css](style/tricorder.css). The [direction's style guide page](../features/20261022.05_style_directions/round_2/direction_e_archivo/style_guide.html) draws them all with Hollis Voice content.

### Buttons

`tc-btn` is the primary button: the only filled control on a screen. `tc-btn--secondary` is an outline in `--tc-rule-2` for every other action. `tc-btn--small` (36px tall) sits inside cards and toolbars. `tc-link-btn` is a button that reads as a link. A disabled button drops to a `--tc-rule` outline with `--tc-ink-3` text.

**When to use it.** One primary button per view, for the step that moves the work forward (See the readout, Draft the data-room request). Everything else is secondary. Hover changes the fill or the border, never the text colour, so a control never fades when you point at it.

### Cards and panels

`tc-panel` is a surface with a 14px corner and a hairline. `tc-card` adds 24px padding and a column layout: `tc-card-head` for the mark and meta line, a title, the body, and `tc-card-foot` pinned to the bottom for chips or actions. `tc-lit` is the raised panel, with a metal edge that fades round the whole outline.

**When to use it.** A card holds one finding. Cards side by side share one structure and one height, with their chips or actions in the foot. Never nest boxes more than two deep. Use `tc-lit` only for the homepage hero panel.

### The range strip

`tc-strip` draws each figure against its normal band. Values go in as numbers through CSS custom properties: `--min` and `--max` on the strip set the scale, and `--v` on each piece places it. `tc-strip-band` is the agreed or rebuilt figure, within 1%. `tc-strip-tick` is a source's figure; add `is-out` for one outside the band (it gains a triangle) and `is-about` for a spoken figure (dotted). `tc-strip--labelled` adds room for `tc-strip-label` above or below the track. `tc-strip-axis` and `tc-strip-key` give the scale and the key.

**When to use it.** Whenever a number has a normal range or several sources disagree on it. Nobody positions a tick by hand. The overview uses the same strip without labels or axis.

### Flag and verdict labels

`tc-mark` is a glyph plus a word in a small box. The modifiers set both colour and glyph:

| Class | Glyph | Word |
|---|---|---|
| `tc-mark--strong` | filled dot | looking strong, Green flag, Corroborated |
| `tc-mark--weak` | triangle | looking weak, Red flag |
| `tc-mark--mixed` | half-filled dot | mixed |
| `tc-mark--thin` | dashed ring | not enough in the room |
| `tc-mark--running` | ringed dot | running |
| `tc-mark--disagreement` | three bars, in ink | Disagreement |

`tc-label` is the same idea without the box, for a card's head: `tc-label--weak` (Flag), `tc-label--gap` (Gap, dashed square), `tc-label--clean` (Clean check, tick), `tc-label--ask` and `tc-label--steered` (in the metal). `tc-verdict` lays out one verdict line: the piece, its mark, then the reason with `tc-verdict-count` under it.

**When to use it.** Every verdict and flag. The mark comes from the script's rule, and counts come from the run. A disagreement is not a verdict, so it takes ink, not a verdict colour. A plain `tc-mark` with no modifier is a neutral tag such as "The company says" or "First tier at Seed".

### Source chips

`tc-chip` shows a file and a place in mono, such as `pitch_deck.pdf, slide 3`. One click opens the source. `tc-chips` lays several out in a wrapping row.

**When to use it.** Under every claim that has a source. Chips go on their own row under the sentence they support, never inside it. A long chip wraps; it is never cut short.

### Tables

`tc-table` is one surface. Rows are split by hairlines. The head row is mono capitals with no fill, only a stronger rule under it. `tc-fig` right-aligns a figure column in mono. `tc-table--stack` turns each row into a small block on phones. Wrap a wide table in `tc-table-wrap`. `tc-facts` is a two-column label and value list for a card.

**When to use it.** Listing sources side by side, as in Corroboration and Disagreement. List them and do not pick a winner.

### Stated beside found

`tc-pair` shows two figures side by side at the same size and on the same baseline. Each half has a `tc-pair-key` (Stated, Found), a `tc-pair-value` and a `tc-pair-source`. `tc-pair--small` drops the figures to 20px for a three-across row.

**When to use it.** Any flag where the company's figure and the room's figure differ. Stated sits left of found. Only the stated figure takes the weak colour (`is-out`), and only when it is out of band.

### Ask the founder

`tc-ask` is a panel outlined in the metal all the way round. It holds a `tc-label--ask` label, the question in `tc-ask-question`, and its actions in `tc-ask-actions` (a small primary button and a small secondary one).

**When to use it.** Where a disagreement or a flag needs the founder to close it. It is an action for the operator, and its question can be pasted into an email. A steered piece (`tc-steered`) is the only other component outlined in the metal.

### Gaps

A gap is a question, drawn with a dashed glyph. In a card, use `tc-label--gap` in the head and `tc-facts` for "Needed for" and "Ask for". In a list, `tc-gap-list` is a ruled list with the dashed glyph on each item. A clean check uses `tc-label--clean` so the operator knows the check ran.

**When to use it.** For anything the room should hold and does not. Name it the way a gap is named: what is missing, why it matters, what to ask for.

### Inputs

`tc-input` is a 44px-tall field with a `--tc-rule-2` border and an 8px corner. It works on `input`, `select` and `textarea`; a textarea switches to mono for drafts. `tc-label` above it is a mono capital label. `tc-help` under it is 13px help text. `tc-check` gives a checkbox the metal and a 20px box; wrap it in a 44px label for the tap area.

**When to use it.** Every text field, such as the company URL, the steer input and the draft to the founder. Focus draws the metal ring and the metal border.

### The synthetic-data label

`tc-synthetic` is one line of small mono text in `--tc-ink-3`: "Synthetic data room for Deal Flow NYC 2026. Not a real company."

**When to use it.** Once per page, beside the readout excerpt or in the footer. Said once it is a fact. Said everywhere it is noise.

## Rules

**Where the metal may appear.** Champagne in dark and brass in light are for:

- thin lines: the band's edge, the Ask the founder outline, a steered piece's outline, link underlines, hover borders
- the primary button's fill in dark, and its text in light
- the focus ring
- the range strip's band
- small mono labels that mark an action: Ask the founder, Steered piece, a role label, the band's figure on a strip
- the faint light behind the homepage hero, and the raised hero panel's edge

**Where it may not.** Never as a large fill, a background, a heading colour, body text, or a verdict colour. A thin line of gold reads as precision. A field of it reads as decoration.

**Drama lives on the homepage.** Only the homepage hero and closing band stay dark in the light theme, and only the hero panel is raised. Product screens are for work. They stay quiet and get out of the way.

**Headings on column one.** Every section heading starts on the container's left edge, the same line as the content under it. No small label alone in a side column. One edge is easy to check by eye.

**Cards in a row match.** Side-by-side boxes share one structure and one height. Uneven boxes look like an error, and an error is the last thing a partner should see.

**Figures in mono.** Every number, file name and place is IBM Plex Mono. Stated sits beside found at the same size. The partner compares numbers down a column, so they must line up.

**Never colour alone.** Each mark pairs a glyph with a word. Out of band is a triangle as well as a colour. Some readers cannot tell red from green, and printouts lose colour.

**One radius scale.** 4px, 8px and 14px, and nothing else. Three sizes read as a system. More read as an accident.

**No one-sided stripes.** No coloured border on one edge of a box, and no short coloured bar above a heading. A full outline in a colour is fine.

**No textures or tilt.** No grid paper or texture behind the page. Nothing rotated, no sideways text.

**One table surface.** A table's head row is never filled differently from its body.

**No Bootstrap in the stylesheet.** Pages may use Bootstrap 5.3 for its grid, but tricorder.css works without it, and anything visible comes from our tokens.

## Accessibility floors

These are floors, not targets. A change that breaks one does not ship.

- **Text contrast of 4.5:1 or more**, for every text pairing in both themes, including marks on their tinted fills and button text in hover.
- **Visible focus.** Every interactive element shows a 2px ring in the metal, 2px off the element. Inputs also turn their border to the metal. The ring needs 3:1 against what it sits on.
- **Tap targets of 44px or more.** Buttons and inputs are 44px tall. Small buttons, chips, text buttons and the theme switch keep their look but extend their tap area to 44px with an invisible layer (`tc-hit` does the same for any other control).

### Contrast results

From `python3 docs/ongoing/style/check_contrast.py`, which reads the tokens from tricorder.css. Marks are measured on their tinted fill over a panel. Hairlines are listed for information; they are not text.

| Pairing | Theme | Text | On | Ratio | Floor | Result |
|---|---|---|---|---|---|---|
| Headings, figures | Dark | `tc-ink` #eeebe4 | `tc-ground` #131210 | 15.7:1 | 4.5:1 | pass |
| Body copy | Dark | `tc-ink-2` #bdb7ab | `tc-ground` #131210 | 9.4:1 | 4.5:1 | pass |
| Labels, axes, help | Dark | `tc-ink-3` #9a9488 | `tc-ground` #131210 | 6.2:1 | 4.5:1 | pass |
| Labels on a hover fill | Dark | `tc-ink-3` #9a9488 | `tc-surface-2` #211f1b | 5.5:1 | 4.5:1 | pass |
| Body copy on a panel | Dark | `tc-ink-2` #bdb7ab | `tc-surface` #1a1916 | 8.8:1 | 4.5:1 | pass |
| Metal label (Ask the founder, band label) | Dark | `tc-accent` #d3bf8e | `tc-ground` #131210 | 10.4:1 | 4.5:1 | pass |
| Metal label on a panel | Dark | `tc-accent` #d3bf8e | `tc-surface` #1a1916 | 9.7:1 | 4.5:1 | pass |
| Link hover | Dark | `tc-accent` #d3bf8e | `tc-ground` #131210 | 10.4:1 | 4.5:1 | pass |
| Primary button | Dark | `tc-btn-fg` #16140f | `tc-btn-bg` #d3bf8e | 10.2:1 | 4.5:1 | pass |
| Primary button, hover | Dark | `tc-btn-fg` #16140f | `tc-btn-bg-hover` #e5d6ae | 12.8:1 | 4.5:1 | pass |
| Secondary button, hover | Dark | `tc-ink` #eeebe4 | `tc-surface-2` #211f1b | 13.8:1 | 4.5:1 | pass |
| Disabled button | Dark | `tc-ink-3` #9a9488 | `tc-ground` #131210 | 6.2:1 | 4.5:1 | pass |
| Looking strong mark | Dark | `tc-strong` #7dc4a0 | `tc-surface` + `tc-strong-bg` #262e27 | 6.8:1 | 4.5:1 | pass |
| Looking weak mark | Dark | `tc-weak` #f08c78 | `tc-surface` + `tc-weak-bg` #342722 | 6.0:1 | 4.5:1 | pass |
| Mixed mark | Dark | `tc-mixed` #93b2e6 | `tc-surface` + `tc-mixed-bg` #292b2f | 6.6:1 | 4.5:1 | pass |
| Not enough in the room mark | Dark | `tc-thin` #aaa498 | `tc-surface` + `tc-thin-bg` #282723 | 6.0:1 | 4.5:1 | pass |
| Out-of-band figure | Dark | `tc-weak` #f08c78 | `tc-surface` #1a1916 | 7.3:1 | 4.5:1 | pass |
| Source chip | Dark | `tc-ink-2` #bdb7ab | `tc-surface` #1a1916 | 8.8:1 | 4.5:1 | pass |
| Source chip, hover | Dark | `tc-ink` #eeebe4 | `tc-surface-2` #211f1b | 13.8:1 | 4.5:1 | pass |
| Focus ring | Dark | `tc-accent` #d3bf8e | `tc-ground` #131210 | 10.4:1 | 3:1 | pass |
| Focus ring on a panel | Dark | `tc-accent` #d3bf8e | `tc-surface` #1a1916 | 9.7:1 | 3:1 | pass |
| Input and chip border (rule-2) | Dark | `tc-rule-2` #45413a | `tc-ground` #131210 | 1.8:1 | none | info |
| Hairline (rule) | Dark | `tc-rule` #2e2b26 | `tc-ground` #131210 | 1.3:1 | none | info |
| Band edge (Ask the founder outline) | Dark | `tc-band-edge` #b9a574 | `tc-ground` #131210 | 7.8:1 | none | info |
| Headings, figures | Light | `tc-ink` #1c1b18 | `tc-ground` #ffffff | 17.2:1 | 4.5:1 | pass |
| Body copy | Light | `tc-ink-2` #47443d | `tc-ground` #ffffff | 9.7:1 | 4.5:1 | pass |
| Labels, axes, help | Light | `tc-ink-3` #6b675e | `tc-ground` #ffffff | 5.6:1 | 4.5:1 | pass |
| Labels on a hover fill | Light | `tc-ink-3` #6b675e | `tc-surface-2` #f6f4ef | 5.1:1 | 4.5:1 | pass |
| Body copy on a panel | Light | `tc-ink-2` #47443d | `tc-surface` #ffffff | 9.7:1 | 4.5:1 | pass |
| Metal label (Ask the founder, band label) | Light | `tc-accent` #85692f | `tc-ground` #ffffff | 5.2:1 | 4.5:1 | pass |
| Metal label on a panel | Light | `tc-accent` #85692f | `tc-surface` #ffffff | 5.2:1 | 4.5:1 | pass |
| Link hover | Light | `tc-accent` #85692f | `tc-ground` #ffffff | 5.2:1 | 4.5:1 | pass |
| Primary button | Light | `tc-btn-fg` #eadbb4 | `tc-btn-bg` #1c1b18 | 12.5:1 | 4.5:1 | pass |
| Primary button, hover | Light | `tc-btn-fg` #eadbb4 | `tc-btn-bg-hover` #3a3731 | 8.6:1 | 4.5:1 | pass |
| Secondary button, hover | Light | `tc-ink` #1c1b18 | `tc-surface-2` #f6f4ef | 15.7:1 | 4.5:1 | pass |
| Disabled button | Light | `tc-ink-3` #6b675e | `tc-ground` #ffffff | 5.6:1 | 4.5:1 | pass |
| Looking strong mark | Light | `tc-strong` #1e7550 | `tc-surface` + `tc-strong-bg` #edf4f1 | 5.1:1 | 4.5:1 | pass |
| Looking weak mark | Light | `tc-weak` #b3402e | `tc-surface` + `tc-weak-bg` #f9f0ee | 5.1:1 | 4.5:1 | pass |
| Mixed mark | Light | `tc-mixed` #2d5c9c | `tc-surface` + `tc-mixed-bg` #eef2f7 | 6.0:1 | 4.5:1 | pass |
| Not enough in the room mark | Light | `tc-thin` #6b675e | `tc-surface` + `tc-thin-bg` #f3f3f2 | 5.1:1 | 4.5:1 | pass |
| Out-of-band figure | Light | `tc-weak` #b3402e | `tc-surface` #ffffff | 5.7:1 | 4.5:1 | pass |
| Source chip | Light | `tc-ink-2` #47443d | `tc-surface` #ffffff | 9.7:1 | 4.5:1 | pass |
| Source chip, hover | Light | `tc-ink` #1c1b18 | `tc-surface-2` #f6f4ef | 15.7:1 | 4.5:1 | pass |
| Focus ring | Light | `tc-accent` #85692f | `tc-ground` #ffffff | 5.2:1 | 3:1 | pass |
| Focus ring on a panel | Light | `tc-accent` #85692f | `tc-surface` #ffffff | 5.2:1 | 3:1 | pass |
| Input and chip border (rule-2) | Light | `tc-rule-2` #cdc7ba | `tc-ground` #ffffff | 1.7:1 | none | info |
| Hairline (rule) | Light | `tc-rule` #e6e2da | `tc-ground` #ffffff | 1.3:1 | none | info |
| Band edge (Ask the founder outline) | Light | `tc-band-edge` #8a6c2e | `tc-ground` #ffffff | 4.9:1 | none | info |

All text pairings meet 4.5:1 and the focus ring meets 3:1 in both themes.

**Not yet met: input borders.** The input and chip border (`--tc-rule-2`) is 1.8:1 in dark and 1.7:1 in light. WCAG asks 3:1 for the edge that shows where a field is. The floors above do not cover it, and the direction kept it quiet on purpose. If a field gets hard to find, raise `--tc-rule-2` and rerun the script.
