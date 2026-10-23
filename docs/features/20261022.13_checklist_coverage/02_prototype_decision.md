# Prototype decision: coverage panel and ask list

Prototype: [02_prototype/prototype.html](02_prototype/prototype.html). One self-contained file: inline CSS and JS, no fetches, light and dark. Open it in any browser.

All data in it is synthetic. Hollis Voice is a made-up company. Since 2026-10-22 evening the data is the product step's output (`scans/memo/coverage.py`) on `data_room/hollis_voice_seed_drop` and `data_room/hollis_voice`, with the red-flag scan's real claims and gaps, inlined by `spike/build_prototype.py`. Rebuild: `TRICORDER_OUT_DIR=<dir> python3 -m scans.redflags <room>` for both rooms, then `TRICORDER_OUT_DIR=<dir> python3 docs/features/20261022.13_checklist_coverage/spike/build_prototype.py`.

Screenshots, from headless Chromium after the build: [desktop, light](02_prototype/screenshot.png) and [phone width, dark](02_prototype/screenshot_phone_dark.png). The phone shot is the page in a 390px iframe, because headless Chromium will not open a window narrower than 500px.

## What it shows

- **A synthetic-data banner** that also says "checked" is projected, because no scan has run.
- **Room switch:** the seed drop (12 files) and the full room (17 files).
- **Stage switch:** pre-seed, seed, Series A. The deck's stage is the default, with its source: "Series A", `01_overview/pitch_deck.pdf`, slide 1. Picking another stage marks it "Set by you. The deck says Series A", with a link back.
- **The stage-unknown state:** a link shows what the panel does when no stage can be read. It asks the operator to pick and shows nothing else. (Simulated with `--stage series_b`.)
- **Coverage panel:** counts by status as filter buttons, a bar over the expected items, then the items grouped by checklist piece. Each row says where the item was found, which entry would check it, which missing file blocks it, or that no check exists yet. A missing row links to the ask line that requests it. The default filter is "missing".
- **Ask list:** grouped by readout piece, in the overview's order. Each line is "Ask for: ..." in the guide's words, then "Why: ...", then tags: from a scan gap or from the checklist, "if you have it", "after the term sheet", and the checklist ids it covers.
- **Stage change feedback:** after a switch, a box says how many lines were added and removed, names the removed ones, and marks new lines "New at this stage". A second box names the gap requests held back because the stage does not expect them.
- **Copy as email text:** copies the lines, leaving out the after-term-sheet ones, and says how many it copied. If the browser blocks the clipboard, it says so instead of claiming success.

## The numbers it shows

Product step with the red-flag scan's real output (from `spike/build_prototype.py`'s printout, 2026-10-22):

| Room and stage | Expected | Checked | Found | Missing | Not checked yet | Not expected | Ask lines | If you have it | After term sheet | Gap asks held back |
|---|---|---|---|---|---|---|---|---|---|---|
| Seed drop, Series A | 109 | 3 | 15 | 65 | 26 | 0 | 25 | 7 | 3 | 0 |
| Seed drop, seed | 107 | 3 | 15 | 63 | 26 | 2 | 24 | 17 | 2 | 0 |
| Seed drop, pre-seed | 82 | 3 | 15 | 38 | 26 | 27 | 17 | 13 | 1 | 1 |
| Full room, Series A | 109 | 11 | 16 | 40 | 42 | 0 | 21 | 7 | 3 | 0 |

"Expected" now includes "not stated" items (Ken's default 1). "Checked" counts only rows a real red-flag claim checked: C02, C19 and C20 on the seed drop; eleven rows on the full room.

The first version, from the spike, `spike/print_counts.py` after `spike/run_all.sh` ("checked" projected, "not stated" not expected):

| Room and stage | Expected | Checked (projected) | Found | Missing | Not checked yet | Ask lines | Of which "if you have it" | After term sheet | Gap requests held back |
|---|---|---|---|---|---|---|---|---|---|
| Seed drop, Series A | 96 | 20 | 18 | 53 | 5 | 23 | 2 | 3 | 0 |
| Seed drop, seed | 91 | 20 | 18 | 45 | 8 | 20 | 10 | 1 | 1 |
| Seed drop, pre-seed | 55 | 20 | 18 | 11 | 8 | 11 | 4 | 0 | 5 |
| Full room, Series A | 96 | 41 | 21 | 28 | 6 | 19 | 2 | 3 | 0 |

"Found" counts every document row the room holds, whatever its stage mark. The other statuses count expected rows only. Every run has 0 repeated requests and 0 missing items without an ask line.

## What trying it settled

- **The stage switch is worth its place.** Moving the seed drop from Series A to pre-seed drops the list from 23 lines to 11 and holds back 5 gap requests (`spike/print_counts.py`). The diff box makes that legible. Without it, lines just vanish.
- **Missing checks must fold into their file's request.** On the seed drop at Series A, 33 missing items are checks that cannot run because a file is absent. Asking for each check would be 33 more lines. Folded, monthly revenue by customer covers 19 checklist ids in one line (`spike/out/seed_drop_series_a.json`, the line whose `checklist_id` is C03).
- **"Missing" as the default filter.** With "all", the panel is 109 rows. With "missing", it is the list an associate acts on.
- **Two kinds of missing need different words.** A missing document says "Not in the room". A missing check says "Cannot run: needs C03, not in the room". Both link to the same ask line.

## Defaults set 2026-10-22 (Ken can override each)

The coordinator recorded these defaults while Ken was away. The code and the prototype follow them.

1. "Not stated" items are asked "if you have it" (`EXPECTED` in `scans/memo/checklist.py`).
2. Legal and cap table asks go under "the pitch itself" (`PIECES` in `scans/memo/checklist.py`). AI governance rows go there too.
3. One line for all SAFEs, naming each holder (`_ask_lines` in `scans/memo/coverage.py`). The gaps stay one per SAFE.
4. After-term-sheet asks are kept, tagged, and collapsed under their own heading on the page.
5. The full list, grouped by piece, with the top five pinned at the top. Top five: required lines for before the second meeting, ranked by how many checklist items each settles.
6. Build only the guide checks that run on the demo rooms; mark the rest as left to the operator (Plan slice 4).

## Open design questions for Ken (as first asked; superseded by the defaults above)

1. **Items marked "not stated" for a stage.** FRAMEWORKS treats them as not expected, so they are never asked. At Series A that is 13 items, including all 8 AI and data governance rows (`docs/ongoing/checklist_counts.py`). Ask them "if you have it" instead? Recommendation: keep them out of the ask list and show them in the panel as "not expected", because the research names no stage for them.
2. **Ask lines with no readout piece.** The schema's `AskItem.piece` must be one of the nine readout pieces. The checklist's "legal and cap table" and "AI and data governance" rows have no piece. On the seed drop at Series A, 11 of the 23 lines are company records like these (`spike/out/seed_drop_series_a.json`, lines whose `piece` is null). Options: put them under "the pitch itself", which already holds the cap table (FRAMEWORKS 1.10); or add a tenth group, "company records", which changes the frozen schema. Recommendation: "the pitch itself" for Saturday, a proper group after.
3. **One line per SAFE, or one line for all three.** Entry 1.10's reading writes a gap per instrument, so the list asks for three signed SAFEs on three lines. BRAND says "one request per item". Recommendation: one line per instrument, because each is a separate document the founder must find.
4. **Lines for after the term sheet.** Bank statements, accountant-prepared statements and tax returns are asked "after the term sheet" (FRAMEWORKS 1.11). The prototype shows them tagged and leaves them out of the copied email. Keep them on screen, or hide them until the operator asks? Recommendation: keep them on screen, tagged.
5. **Length.** 23 lines at Series A on the seed drop. Show all, or the five most blocking first? Recommendation: show all, ordered by piece, because the associate pastes it into an email and edits it there.

Design questions the prototype could not settle without the style guide: color and type for the status pills, and whether the coverage panel sits beside the ask list or under it. The prototype uses neutral CSS variables so the chosen style can replace them.

## Persona review

**Pending.** The persona-review agents are being built in a parallel thread. When they exist, run the associate and the partner personas on this prototype at the seed drop, Series A, and record findings and dispositions here.

## Fixes after the first screenshots

- The "covers C03, C05, ..." chip overflowed the ask panel. Chips now wrap (`.ask .meta` is a wrapping flex row; the covers chip wraps inside).
- At phone width a long code span in the banner pushed the page wider than the screen; long text now wraps. Measured in headless Chromium: page width 485px in a 500px window, no element past the edge.
- Links were default blue on the dark background; they now use the accent token.
- The red-flag scan's real output has two gaps both named "Not in the room: an expense ledger". They made two ask lines. They now make one (`test_two_gaps_for_one_document_ask_once`).

## Prototype status

Throwaway. The product panel is a React component in `readout/` (the readout-page slice). The prototype is the UI acceptance baseline for its behavior, not its look: the stage control and its source line, the default filter, the fold of missing checks into one request, the diff box after a stage change, the copy button's honest message.

Screenshots are linked at the top.
