# Brief for round two of the style directions

Ken reviewed round one (directions A, B and C, one folder up) in Lahe on 2026-10-22 and rejected all three as not professional enough. This round starts over. The seed from round one no longer applies.

## What Ken asked for, in his words

> none of these look professional enough. you need to try again, remember the audience and the product. look at the pages yourself and make sure they look like they were made by a world class designer that loves things being on the grid. you can use bootstrap if you want to make it easier to grid things. i'm also ok with rounded corners. they don't need to be everywhere, but the strict 90 corners are getting old already. make something that brings gravitas, expresses wealth, but is not overly flourishing, gets out of the way and lets you work. but the homepage of course will need a little bit of drama and wealth in it

## The audience and the product

Tricorder is first-pass diligence software for seed and Series A venture funds. Two people use it. The associate prepares the memo and wants the gathering done before they look. The partner reads the memo, decides, and wants to check any line in two clicks. They manage other people's money. The product has to look like it belongs next to a private bank, a top law firm or a serious financial terminal. It must not look like a developer tool, a startup template or a magazine.

Read before designing:

- `docs/ongoing/BRAND.md`: the line, how we describe Tricorder, the readout's voice with the Hollis Voice figures, and the words to avoid. Copy follows it exactly.
- `docs/ongoing/PERSONAS.md`, the associate and the partner only.
- `../BRIEF_FOR_DESIGNERS.md`: round one's brief. Its deliverables, page rules and copy rules still apply, except where this brief changes them.
- `../direction_a/home.html`: the round-one page Ken liked best. Reuse its copy and content as your starting material.

## What Ken's round-one comments taught us

These are hard rules for every page in this round.

Ken liked:

- The range strip in direction A: each number drawn against its normal band, with the out-of-range figure marked. Carry it in some form.
- The technical feel of A's ARR disagreement panel: the number line plus the source table.
- Stated beside found: two figures side by side, what the deck says and what the rest of the room shows.
- The "Ask the founder" prompt as a feature.

Ken rejected:

- No single coloured stripe on one edge of a box. That covers a left border, a right border on a tab, or an inset box-shadow that draws one. A full outline in a colour is fine.
- No short coloured bar above a heading or label. A top rule is allowed only when it lines up exactly with another vertical edge on the page and runs longer than the text under it.
- No graph paper, grids or textures as a background. Grey-tinted page grounds read as dull: use white, or a deliberate dark.
- Nothing tilted or rotated, and no sideways text.
- No overused or bookish display faces. Rejected: Bricolage Grotesque (everywhere), Libre Caslon Display (bookish, editorial). Also avoid Inter, Space Grotesk, Fraunces, Playfair and Cormorant.
- Headline line spacing has to be tight. Loose leading on a big headline looks amateur.
- Boxes that sit side by side share one structure and one height. A grid of cards has equal row heights.
- Section headings sit on the same grid line as the content under them. No small label floating alone in a narrow side column.
- A table is one surface. The head row is not a different fill from the body.
- Hover and focus states keep their contrast. Check every button's hover in both themes.
- The synthetic label ("Synthetic data room for Deal Flow NYC 2026. Not a real company.") appears once per page, near the readout excerpt or the footer. Do not repeat it.
- No decorative codes that mean nothing (round one had "Box 4", "L.01", "Bay 1").
- Source chips do not break sentences mid-line. Put them on their own row under the sentence.
- No boxes nested three deep.

## What changes from round one

- Bootstrap 5.3 is allowed for the grid and utilities, from `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css`. Use it for layout only. Override its look with your own tokens so nothing reads as default Bootstrap. No Bootstrap JavaScript.
- Rounded corners are allowed where they help: panels, buttons, inputs. Pick one radius scale and use it consistently. Not everything needs a radius.
- Everything sits on a 12-column grid with one gutter. Ken checks alignment by eye.
- The homepage needs some drama and a sense of wealth: a dark or deep-colour hero, generous scale, a product surface that looks expensive. The product screens and style guide stay quiet and get out of the way.

## Deliverables

Each direction writes into `round_2/direction_<x>/` only:

1. `home.html`: the homepage, sections as in round one's brief (hero with the line verbatim, a readout excerpt with the green flag, the red flag and the ARR disagreement, the associate and the partner, what Tricorder adds, what it is not, a call to action).
2. `style_guide.html`: tokens (light and dark), type, spacing, corners and lines, the readout components drawn for real, and rules a builder can apply, each with its reason. Same component list as round one.
3. `notes.md`: five to ten lines. The direction's name, the idea, the risk taken, anything unsure.

Both pages link to each other and to `../../index.html` ("All directions").

## Check your own work, with your own eyes

Screenshot both pages: `NODE_PATH=~/.claude/skills/playwright-skill/node_modules node <scratchpad>/shoot.js <page.html> <outprefix>`, writing into `round_2/direction_<x>/screens/`. It writes 1440px and 400px shots in light and dark, and prints horizontal overflow and script errors. Look at every shot. Check alignment to the grid, equal heights, tight headlines, contrast, and the rules above. Fix, shoot again, and repeat until you would show it to a design director. Then grep for em dashes and the avoid-list words in BRAND.md.

## Do not

- Do not delete any file. List anything to remove in `notes.md` under "To delete at cleanup".
- Do not edit outside your own folder. Do not commit or push.
