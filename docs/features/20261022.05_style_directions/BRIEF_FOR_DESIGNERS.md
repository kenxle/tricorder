# Brief for the three style directions

Ken asked for at least three style guides, each with a sample homepage, for Tricorder. Each direction is seeded: `seed_directions.py` hashed the datetime the request arrived (2026-10-22T19:51:56Z) and picked a motif, an accent hue, a type pairing, a density, a ground and a shape for each direction. The picks are in `seed_directions.json`. The seed is inspiration, not a cage: honour every pick, and interpret the motif with taste. A motif shows up in materials, structure and detail, never as clip art or a costume.

## Read first

- `docs/ongoing/BRAND.md`: the voice, the line, the words to use and avoid, the readout's voice with real Hollis Voice examples. Copy on your pages follows it exactly.
- `docs/ongoing/PRODUCT_BRIEF.md`: what Tricorder is and who it is for.
- `docs/ongoing/PERSONAS.md`, the two primary personas only: the associate who prepares the memo and the partner who reads it and decides.

## What each direction delivers

Write into `docs/features/20261022.05_style_directions/direction_<x>/` only:

1. `style_guide.html`: the style guide, as a page. Sections: the direction in two sentences and how the seed shaped it; colour tokens (light and dark, with hex and the role of each); type (the three faces, the scale, where each is used); spacing, corners, lines; the readout components drawn for real: a green flag, a red flag, a verdict line for each of the four marks (looking strong, looking weak, mixed, not enough in the room), a corroboration table, a disagreement table, a gap, a clean check, a source chip, a steered-piece note, buttons and a text input; then rules a builder can apply without asking, each with its reason. Semantic colours for strong, weak, mixed and not-enough are separate from the accent, work in both themes, and are never colour alone (each mark also has a shape or a word).
2. `home.html`: Tricorder's sample homepage. It sells to the two personas. Suggested sections, change the order if the direction calls for it: hero with the line, verbatim ("Point it at a startup, get a readout. Tricorder takes any data: decks, videos, spreadsheets, data rooms. It reveals insight you can trust, every claim sourced."); a live-looking readout excerpt from the Hollis Voice room using the exact figures in BRAND.md (the green flag "the round adds up", the red flag "runway leaves out most of the hiring plan", and the ARR disagreement), labelled "Synthetic data room for Deal Flow NYC 2026. Not a real company."; one block for the associate and one for the partner, using the promises in BRAND.md "How we describe Tricorder"; what Tricorder adds; what it is not; a call to action that claims nothing false (for example "See the Hollis Voice readout" or "Bring a data room to the pilot"). No customer logos, no testimonials, no speed or accuracy claims, no "AI-powered", no "insights" outside the line, never "verified" or "confirmed" for a number, never "invest", "pass" or "fraud".
3. `notes.md`: five to ten lines. The direction's name, what it borrows from the motif and where, the risk you took, and anything you are unsure of.

## Page rules

- Each file is a complete standalone HTML document: `<!doctype html>`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`, a `<title>` of two to four words (for example "Tricorder, Direction A"), and all CSS and JS inline. The two files link to each other by relative path (`home.html`, `style_guide.html`) and to `../index.html` ("All directions").
- Fonts from Google Fonts only (`fonts.googleapis.com`), each with a real fallback stack. No other external resource of any kind: no images from the web, no scripts from anywhere. Draw what you need in inline SVG or CSS.
- Light and dark themes, token-driven: every colour defined on bare `:root`, redefined under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }` and again under `:root[data-theme="dark"]`, with `color-scheme: dark` in both. A dark-first direction mirrors the pattern. `body` sets an explicit background from a token.
- Works at 400px wide with no horizontal page scroll. Side gutter `padding-left: max(16px, env(safe-area-inset-left, 0px))` and the same on the right. Tables scroll inside their own `overflow-x: auto` box.
- Visible keyboard focus, `prefers-reduced-motion` respected, `font-variant-numeric: tabular-nums` where figures line up.
- Avoid the stock AI looks: cream with serif and terracotta, black with one acid-green pop, purple-to-blue gradient heroes, Inter or Space Grotesk, emoji as markers, everything centred, the same rounded card and shadow on every block.
- Plain words, one idea per sentence, no em dashes anywhere (copy, comments, notes).

## Check your work

Screenshot both pages with `node /tmp/claude-0/-home-claude/03513b6c-0caf-53e4-b2b9-686a5a421283/scratchpad/shoot.js <page.html> <outprefix>`. It writes desktop and 400px phone shots in light and dark and prints any horizontal overflow or script error. Write the screenshots to `direction_<x>/screens/`. Look at them, fix what is broken, shoot once more. Then grep your files for em dashes (`—`) and for the avoid-list words in BRAND.md.

## Do not

- Do not delete any file, ever, including your own drafts. List anything you would remove in `notes.md` under "To delete at cleanup".
- Do not edit anything outside your own `direction_<x>/` folder. Do not commit or push; the thread that briefed you does that.
