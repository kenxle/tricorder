# Prototype decision: the memo and its PDF

Prototype: [prototype_real.html](02_prototype/prototype_real.html) (the Hollis Voice readout as `main` builds it today) and [prototype_simulated.html](02_prototype/prototype_simulated.html) (the same readout with pieces, top flags and links added by hand from its real claim ids, and two simulated operator lines; the banner says so), plus [prototype_simulated.pdf](02_prototype/prototype_simulated.pdf). Built by [spike/build_prototype.py](spike/build_prototype.py). Screenshots: `02_prototype/prototype_*_{light,dark}_{top,drill}.png` and `*_phone_dark.png`.

**The prototype is the implementation.** The page is `memo/html.py` rendering a real `Memo`; nothing in the prototype is hand-drawn. Only the pieces, top flags and links in the simulated page are made up, because the merge steps that write them are not built yet.

## What the prototype settled, by trying it

Driven in Chromium by [spike/drive_memo.js](spike/drive_memo.js), which clicks every line and every claim the way a partner would:

| Page | Lines | Lines with something behind them | Opened in one click | Claims shown | Source opened in the second click, quote marked |
|---|---|---|---|---|---|
| Real readout | 128 | 113 | 113 | 40 | 40 |
| Simulated pieces and flags | 129 | 114 | 114 | 62 | 62 |

From `02_prototype/prototype_real_drive.json` and `prototype_simulated_drive.json`. No horizontal scroll at phone width (390 px).

- **A thin readout still reads as a memo,** but a sparse one: on the real readout 9 of the 16 sections have nothing Tricorder could source, and each says why. The flags in section 2 and the claims in sections 6, 7 and 12 carry it.
- **One claim per line.** Each claim keeps its own sentence. Grouping claims into one sentence is the connecting step's job (the merge's model pass), not the export's. (Changed in the fix round: the pitch's figures share one line per section, and a red flag stated in several places is one line. See the persona review below.)
- **Gap lines open their checklist item and ask line,** and a second click on the item opens the published checklists that name it, with links.

## Persona review (independent)

The coordinator ran `persona-associate` and `persona-partner` cold on the built memo and the two prototype pages, following [PERSONA_REVIEWS.md](../../ongoing/PERSONA_REVIEWS.md). These replace the builder's own reading of the personas from the first round, which was not independent. Simulated judgment, not customer evidence.

**Verdict.** Both rated the built memo weak, and both ranked the simulated prototype first. Both said the memo reads like a checker's report: plumbing in every section (check names, claim ids, checklist numbers, "Who writes it", "not built", commands), the answer below the fold, empty sections that each took several lines, and the same flag printed word for word in sections 2, 7 and 12.

| Finding (both personas unless marked) | Taken or left | What changed |
|---|---|---|
| The first screen should be the answer. | Taken | The page opens on the head line, the round, the red flags and one line for the pieces. The contents list is folded, and a side rail on a wide screen. `evidence/fix_round/memo_drive.json`: `partner_first_screen` is the round and 6 red flags on a laptop; `phone_first_screen` starts with the round and the first flags. |
| A partner view with no plumbing, for the page and the PDF. | Taken | The partner view is the default. Check names, claim ids, checklist numbers, "Who writes it", blanks, commands and script sentences show only in the operator view, behind the toggle. The drive reads the partner view's visible text and finds none (`partner_plumbing: []`). |
| Empty sections take one line; say "not assessed yet" once; show a flag once. | Taken | An empty section is one line ("Market: not assessed yet. Needs the market signals and business frameworks scans."). The pieces with no verdict share one line. A flag is in full in section 2 once; sections 7 and 12 point to it. Gaps that differ only in their subject share a line. |
| The recommendation opens the summary; no placeholders in the partners' PDF. | Taken | Section 15's operator line becomes the first line of section 2 on the page and in the PDF. Blanks never print in the PDF. |
| The PDF is for partners. (Partner) | Taken | No ask list. Notes name the file, the place and what it reads as: a CSV row with its column names, a cell with its line and column, numbers formatted as the claims state them ("-$0.24", not -0.24000000022351742). |
| Say the ARR disagreement in plain words. (Partner) | Taken | Red flag 1 puts the room's ARR figures side by side, each with where it is, each copied from a claim or a cited source, with the claims behind the line. No figure is computed ([04_architecture.md](04_architecture.md), "Memo-local composition"). |
| Edit in one sitting. (Associate) | Taken | Changes are made in place and saved together as one version. On a 409 the page keeps the typed changes and offers to reapply them on the newer version. A claim line rewritten with a figure its claims do not state becomes the operator's line, with no claims behind it. |
| The edit's author is the person who typed it. (Associate) | Taken | A name field in the edit bar. The drive uses a plain operator name. |
| The clinic count (357 in the pitch against 212 in the books) is missing. (Partner) | Taken after the claims scan landed | The claims scan now writes it, and the memo shows it as its own red flag ("Paying accounts"). It was left for later in the coordinator's brief, while it needed an unbuilt check. |
| Empty sections need narrative, not a line. | Left | The narrative needs the scans that feed those sections (deck claims, market signals, comps, founder profiles). The memo names the missing scans. |
| The pitch's 60 figures should not be 60 lines. (Coordinator, with the claims scan) | Taken | Each section gives the pitch's figures as one line ("30 figures from the pitch: 16 match the room; 14 have nothing in the room to check against (...)"), with every claim behind it. A raise stated in three places is one line, "The round". |

## Decisions

- **Notes at the end of each section in the PDF, not at the foot of each page.** True page-bottom footnotes need a layout engine none of our tools has (reportlab's platypus has no footnote flowable; Chromium's print does not support CSS footnotes). The notes are numbered across the memo, so a reader reads "[12]" and finds note 12 under the same section. Question for Ken in the PRD.
- **Editing in the page only when the server serves it.** A file opened from disk is read only, because there is nowhere to save a version.
- **Default theme follows the system; a button switches it,** as the readout page does.
