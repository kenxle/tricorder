# Direction E: Black Card

- **The idea:** the quiet wealth of a premium charge card, crossed with the precision of a trading terminal. Warm graphite ground (#131210), off-white ink (#eeebe4), and one pale champagne metal kept to hairlines, the primary button, focus and the range strip's band.
- **Type:** Hanken Grotesk 800 for display, set at 0.94 leading with -0.045em tracking; the same family for body. IBM Plex Mono for every figure, file name and label, with tabular numbers.
- **Light theme:** white ground with graphite ink, and the metal deepened to brass (#85692f) so it reads on paper. The primary button turns graphite with champagne text. The homepage hero and closing band stay dark in both themes, on purpose, so the drama survives.
- **Grid:** Bootstrap 5.3 columns only, 12 columns, one 24px gutter, 1200px of content. Corners are 4px (marks, chips), 8px (buttons, inputs), 14px (panels).
- **Range strip:** values go in as numbers and CSS places every tick and band with calc(), so nobody positions a tick by hand. The band is the agreed or rebuilt figure, within 1%.
- **Risk taken:** the hero panel is the only raised surface, with a metal edge that fades round the whole outline and a soft shadow. Everything else is flat hairline. Mixed is a cool blue instead of the usual amber, so it never reads as the metal.
- **Unsure:** whether Ken reads the champagne as wealth or as beige in the light theme's band. Whether the hero overview's band for ARR (the subscription-rows rebuild, $2,060,868) reads as picking a winner; the disagreement table itself does not pick one. The "Ask the founder" and steered-note outlines use the metal as a full outline, which the brief allows, but they are the only two.

## To delete at cleanup

- `style_guide.src.html` in this folder: the template I built `style_guide.html` from. `style_guide.html` is complete and standalone without it.
