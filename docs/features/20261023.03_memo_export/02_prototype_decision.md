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
- **One claim per line.** Each claim keeps its own sentence. Grouping claims into one sentence is the connecting step's job (the merge's model pass), not the export's.
- **Gap lines open their checklist item and ask line,** and a second click on the item opens the published checklists that name it, with links.

## Persona review

Run by the builder in this session, following `.claude/agents/persona-partner.md` and `persona-associate.md` and the rules in [PERSONA_REVIEWS.md](../../ongoing/PERSONA_REVIEWS.md). This session had no subagent tool, so the review was **not** a cold, independent read: the reviewer knew the design. Treat it as the builder's best reading of the two personas, and run the agents properly at the checkpoint (Attention needed in [00_progress.md](00_progress.md)). Simulated judgment, not customer evidence.

| Persona | Finding | Grounded or inferred | Taken or left |
|---|---|---|---|
| Partner | The drill-down repeated the line's sentence word for word under the line, so the first thing under a click was text already read. | Inferred | Taken: the claim card hides its text when it is the line's text, and opens on the number, the label, the check and the source button. |
| Partner | "Sources that agree (0)" reads as "nothing agrees", when the truth is that the linking step is not built. On the real readout every claim shows 0 and 0. A partner who reads disagreement as a warning ("the gap suggests carelessness or something worse", PERSONAS.md, partner) would misread a missing step as a clean bill. | Grounded | Taken: the page says "Not checked yet: the merge step that links agreeing and disagreeing claims is not built" until `scans/memo/link.py` exists. |
| Partner | The ARR red flag is the moment that matters (PERSONAS.md, partner, "The moment Tricorder solves it"). On the real readout it sits in section 2 as "Flag: ARR", with the deck slide one click and two clicks away. | Grounded | Kept as built. |
| Partner | Too many "Not in the readout yet" lines on the real readout: about twenty. They are honest, but a partner skimming would stop. | Inferred | Left: the Done when requires each empty section to name its gap. Fewer lines come from more scans, not from hiding them. The section 2 status line names the missing scans once, at the top. |
| Associate | The ask list is where they act, and they want it in an email ([MEMO_TEMPLATE.md](../../ongoing/MEMO_TEMPLATE.md), "The operator can copy the list into an email"). | Grounded | Taken: a "Copy the ask list" button in section 14. |
| Associate | The scan sentences are long and technical ("Mislabel kind a: non-recurring revenue in MRR"). | Inferred | Left for the scan owners: the memo shows the claim's own text and never rewrites it. Attention needed. |
| Associate | Editing must be quick: rewrite a line where it stands. | Inferred | Taken: served by the server, every line has "Rewrite" and "Remove", each section "Write a line", each blank "Write this". Each save is a new version. |

## Decisions

- **Notes at the end of each section in the PDF, not at the foot of each page.** True page-bottom footnotes need a layout engine none of our tools has (reportlab's platypus has no footnote flowable; Chromium's print does not support CSS footnotes). The notes are numbered across the memo, so a reader reads "[12]" and finds note 12 under the same section. Question for Ken in the PRD.
- **Editing in the page only when the server serves it.** A file opened from disk is read only, because there is nowhere to save a version.
- **Default theme follows the system; a button switches it,** as the readout page does.
