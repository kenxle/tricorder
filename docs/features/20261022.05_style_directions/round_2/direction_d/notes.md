# Direction D: Private Bank

- **The idea.** The quiet confidence of a private bank or a top law firm. White working surfaces, one deep navy band (#0b1a2e), and one accent: a deep spruce green (#1d5a47; #7cc4a4 in dark) for action only.
- **Type.** Source Serif 4 at its display optical size for headlines, set tight (1.02 to 1.15). IBM Plex Sans for every sentence and control. IBM Plex Mono for figures and file names, tabular.
- **The drama.** The homepage hero is a full-bleed navy band with the line in large serif, beside one lifted white readout card: green flag, red flag, stated beside found, and the range strip. That card is the only surface with a shadow.
- **The grid.** Bootstrap 5.3 grid only, 12 columns, one 24px gutter, 1248px of content. Every heading starts on the same column line as its content. Rows of boxes share one height. The two persona cards use a CSS subgrid, so their quotes, paragraphs and lists line up row by row.
- **Corners.** Two radii: 6px for chips, buttons, inputs, marks and the ask box; 12px for panels. Chart marks stay square.
- **The risk.** The accent is green and the strong verdict is also green. They are separate tokens (spruce #1d5a47 against leaf #17803d), and the accent never marks a verdict. A reviewer may still read a green button as "strong". Oxblood was the alternative; it would clash with the red flag instead.
- **Unsure.** In dark mode the hero band (#050d1a) and the page ground (#0a1526) are close, so the hero reads less dramatic than in light. The overview panel on the homepage shows 5 of 9 pieces so the two readout panels end at the same height.
- **Copy.** Taken from direction A and BRAND.md. The partner's quote is the full sentence. The synthetic label appears once per page.
- **Build note.** style_guide.html carries the same CSS block as home.html, copied in, so the two pages cannot drift apart while they are edited together.

## To delete at cleanup

- Nothing in this folder. Scratch files live in the session scratchpad: crop_d.py, sbs.py, build_sg.py, sg_src.html and the crop PNGs.
