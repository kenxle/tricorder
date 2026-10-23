# PRD: the memo and its PDF

Roadmap slice: [memo-export](../../ongoing/ROADMAP.md#memo-export). Brief: [01_brief.md](01_brief.md). Prototype and persona review: [02_prototype_decision.md](02_prototype_decision.md). Template: [MEMO_TEMPLATE.md](../../ongoing/MEMO_TEMPLATE.md).

## Problem, users, context

The associate prepares the memo for the partners' meeting; the partner reads it and decides. The readout already holds every claim with its sources, the gaps, the coverage and the ask list. The memo puts them in the order partners know, keeps the readout's two clicks behind every line, and leaves the decision to the operator.

## Scope

In: the export from a readout, the interactive page, the PDF, operator edits with numbered versions, the quote check on export, the CLI and the server routes.

Not in: reader copies and scenarios ([reader-scenarios](../../ongoing/ROADMAP.md#reader-scenarios)); steering a section (the [steering](../../ongoing/ROADMAP.md#steering) slice); the connecting sentences (the merge's model pass); a mount point in the readout page (`readout/src/App.tsx` is avoided; Attention needed).

## Requirements

| ID | Requirement |
|---|---|
| ME-R1 | `python -m memo <room_dir \| readout.json>` writes a new version `out/<room>/memo/memo_v<N>.json`, `memo.html` and `memo.pdf`, and prints a JSON summary with the version, the claim count, the "could not verify" count and every empty section with its gap. |
| ME-R2 | The memo has the template's 16 sections, in its order, with its titles and its "who writes it". |
| ME-R3 | Each claim goes to one body section: its piece's section when the pieces step placed it, else its value label's section, else its FRAMEWORKS entry's section (the template's "Filled from" column), else the section of its room folder. |
| ME-R4 | Every section either holds a sourced line (claim, reading, pieces, ask, source) or names the gap that leaves it empty: "Not in the room: ..." for a document, "Not in the readout yet: ..." for a scan or a merge step that has not run or is not built. The operator's sections (13, 15) hold a blank slot instead. |
| ME-R5 | Sections 4 to 11 open with their pieces (verdict and source counts), or a gap line when the pieces step has not run, and close with their checklist coverage at the company's stage. |
| ME-R6 | Section 2 holds: what the company does (deck claims) or its gap; the operator's recommendation slot; a line naming the scans not run; the top green flags then the top red flags, or, until that step exists, its gap and every claim with severity "flag"; the nine pieces or their gap. |
| ME-R7 | Section 12 lists every claim with severity "flag", then the reasons of weak and mixed pieces, then the room gaps, then the operator's ranking slot. A flag with no ask line says what would settle it. |
| ME-R8 | Section 14 holds the coverage counts, the checked, found and missing items, every ask item with why and the section it feeds, and the "could not verify" box. Section 16 lists every cited source once and the change log. |
| ME-R9 | Tricorder never writes the recommendation, the outcome cases, the operator's view of the founders, whether the price is right, or the risk ranking. It never says invest or pass. |
| ME-R10 | On export the quote checker runs on every claim. A claim that fails moves to the "could not verify" box with the reason, and no line cites it; a claim line left with no claim is dropped. |
| ME-R11 | The page works offline: one file, no outside script, style or font. The memo's data is embedded. |
| ME-R12 | On the page, one click on any line with something behind it opens its claims; for a gap, its checklist items and ask line; for an operator line, who wrote it and in which version; for a coverage line, its items. |
| ME-R13 | One more click on a claim opens each source's text at its locator with the quote marked, and the claims that agree and disagree (corroborated_by, conflicts_with) with their sources. Until the link step exists, the page says agreement is not checked yet. |
| ME-R14 | The PDF has the same sections in the same order. Every claim cited by a line has a numbered note naming its file, locator, what it reads as (the quoted text, or for a CSV row or a cell its columns, ME-R24) and the date read: a web source's retrieved_at, or for a file the date the export read it. The claim id is in the page's operator view, not the PDF (ME-R20). Amended in the wave 2b review round (O3). Gap lines, operator lines and blanks are marked. |
| ME-R15 | An operator edit (add, replace, remove) makes the next version and a change-log line with the author and time. Versions are never overwritten. |
| ME-R16 | An operator line is marked as theirs (author, version). Claims are attached only when the operator names them and they are in the memo. A number in an operator line with no claim is shown as "operator's figure, no source". |
| ME-R17 | A new export after edits redrafts from the current readout and keeps the operator's lines in place; a line the operator removed or replaced stays so. |
| ME-R18 | The server routes: `POST/GET /api/rooms/{room}/memo`, `GET .../memo/versions`, `POST .../memo/edits` (refused with 409 when based on an old version or when another save made that version first, 400 for a bad edit, 422 for an edit over the size limits: a line of 2,000 characters, an author of 80, 100 edits a batch, 500 operator lines a memo), `GET .../memo.html` (editing on), `GET .../memo.pdf` (each version's PDF built once and served as saved). |
| ME-R19 | Words follow [BRAND.md](../../ongoing/BRAND.md): no "likely", "probably", "fraud", no em or en dashes. |
| ME-R20 | Two views of one memo. The partner view is the default for the page and the only view in the PDF: no claim ids, check names, checklist numbers, "Who writes it", operator blanks, commands or sentences about scripts. The operator view (the toggle) shows all of it. |
| ME-R21 | The first screen is the answer: the head line, the round, the red and green flags, one line for the pieces, then the rest of the summary. |
| ME-R22 | A section with nothing in it is one line naming the scans it needs. "Not assessed yet" for the pieces is said once. A flag is in full once, in section 2; other sections refer to it. A gap is not repeated within a section. |
| ME-R23 | The operator's recommendation in section 15 opens section 2, on the page and in the PDF. No blank prints in the PDF. |
| ME-R24 | The PDF leaves out the ask list. Its notes name each source's file and place and what it reads as: a CSV row with its column names, a cell with its line and column, numbers formatted as the claims state them. |
| ME-R25 | When the room holds two or more ARR figures, red flag 1 puts them side by side, each copied from a claim or a cited source and linked to the claims. The memo computes no figure. |
| ME-R26 | Editing in place: many changes, one save, one version, a name typed in the edit bar as the author. On a 409 the page keeps the changes and offers to reapply them on the newer version. A claim line rewritten with a figure its claims do not state becomes the operator's, with no claims behind it. |
| ME-R27 | Many claims read in a few lines: the pitch's figures are one line per section with every claim behind it; red flags on the same subject share a line; the source list is the operator's, with one line for partners. |
| ME-R28 | A source opens only inside the readout's room, or, after a "read the full room" steer on a seed drop, the full room it names (scans.memo.merge.reads_room). The quote check, the page's source text, the PDF notes, `POST /api/rooms/{room}/source` and `GET .../files/...` all resolve it there. No absolute path, no `..`, no other room, no repo file, no answer key. Added in the wave 2b review round (B1, S2). |
| ME-R28 | A claim an operator's steer replaced is not a live line; it is the new line's "before", shown in its drill with its sources. |
| ME-R29 | Tests find claims by the check that wrote them or by severity and take counts from the readout, so a new check or a renumbering never breaks them. |

## Failure cases

| Case | Behaviour |
|---|---|
| No readout yet | CLI exits 2 and names `python -m scans.memo <room>`; `POST .../memo` answers 409. |
| A readout with nothing in it | Every section still renders, each naming its gap (`test_a_bare_readout_still_builds`). |
| A source cannot be opened at export | The claim fails the quote check and moves to the box. |
| An edit names a missing line, section or claim, or has no text or author | Refused, nothing written (`EditError`; CLI exit 2; HTTP 400). |
| Two people edit the same version | The second save gets 409 and reloads. |
| The pieces, top_flags or link step not built | Gap lines name the step; the page says agreement is not checked yet. |

## Logging and rollout

No flag: the export runs only when asked. The change log in section 16 is the record of edits.

## Questions for Ken

1. **Section notes or page footnotes in the PDF?** Built: numbered notes at the end of each section. Page-bottom footnotes need a different PDF engine.
2. **Routing when pieces are missing.** Built: label first, then entry, so the MRR mislabel lands in traction (7), not business model (6) as entry 1.12's row in the template would put it. Once the pieces step runs, the piece decides.
3. **Who signs.** The "From" line is a blank the operator fills; there is no sign-in to name them.
