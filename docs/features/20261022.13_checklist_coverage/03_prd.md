# PRD: checklist coverage

Context: [01_brief.md](01_brief.md) and [product_thinking.md](product_thinking.md). Agreed experience: [02_prototype_decision.md](02_prototype_decision.md). Rules this builds: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), "Checklist coverage", "Ask list", "1.10 Cap table reconciliation" (model reading only) and "1.11 What the room cannot settle". Roadmap slice: [checklist-coverage](../../ongoing/ROADMAP.md#checklist-coverage).

## Problem, user, context

The associate needs to know what a room lacks for the company's stage, and needs the requests written. The Saturday ask list sees only what the scans needed. This slice adds the checklist's view. The full reasoning is in the brief.

## Scope

In:

- Coverage of all 109 checklist items for one room at one stage.
- The stage, read from the deck and changeable by the operator.
- Ask-list lines for missing items, merged with the gap and weak-piece lines without repeats.
- Entry 1.11's asks (bank statements, accountant-prepared statements, tax returns, IP assignments, customer references, one walk-through per flag), as checklist lines with their ask stage.
- Entry 1.10's instrument reading: each SAFE, note and grant on the cap table matched to a document in the room (row C82).
- A register of the document guides' proposed checks, each marked as built here, left to a later slice, or left to the operator.
- The coverage counts and rows as Panels in `readout.json`, and the coverage panel on the readout page.

Out (non-goals):

- Building the 176 proposed checks the guides list (`spike/count_proposed_checks.py`). This slice builds the register and the few that run on the demo rooms; see the Plan.
- The bank tie-out (the bank-check slice).
- Drafting messages to the founder (the founder-requests slice).
- The default piece order per stage (the stage-views slice). This slice only provides the stage.
- Any model call.

## Solution outline

A merge step, `scans/memo/coverage.py`, runs after piece verdicts and top flags and before the ask list. It reads `docs/ongoing/checklist.csv`, the room's file list, the readout's claims and gaps, and the stage. It writes coverage records as a Panel and appends checklist ask lines to `readout.asks`. The ask-list step that follows adds gap and weak-piece lines and skips any request coverage already made. Details in [04_architecture.md](04_architecture.md).

## Requirements

Statuses use FRAMEWORKS' words plus one addition, `not_checked` (CC-R5). A requirement's acceptance row is in [05_plan.md](05_plan.md), "Verification".

### Stage

- **CC-R1. Stage from the deck.** The stage is read from the deck's cover or round slide: a line that starts "Pre-seed", "Seed" or "Series A" followed by "|" (Hollis Voice: "Series A | $9,000,000", slide 1; Brasswick: "Seed | $3,000,000", slide 1). If the deck text cannot be read, the round label in `01_overview/claims.json` is the fallback ("Series A raise" on Hollis Voice). The stage carries its source: file, slide and the quoted line.
- **CC-R2. The operator can change the stage.** An operator's choice wins over the deck. The readout keeps both: the operator's stage, and what the deck said. Changing the stage changes coverage and the ask list on the next build, and never changes a claim, a verdict or a flag.
- **CC-R3. Unknown stage.** If no stage is readable and the operator has set none, or the stage read or set is not pre-seed, seed or Series A (for example "Series B"), the label is `stage_unknown`. Coverage writes no statuses and no ask lines. The panel asks the operator to pick a stage. Tricorder never guesses a stage.

### Coverage

- **CC-R4. Every item gets one status.** For a known stage, each of the 109 items gets exactly one of: `checked`, `found`, `missing`, `not_checked`, `not_expected`. The counts by status come from the script and add up to the item count.
- **CC-R5. Status rules.**
  - A document row is `found` when a room file matches it. Found does not depend on stage.
  - A check row is `checked` when a readout claim's `check.name` belongs to an entry the row's `checked_by` names, and that entry did not return `cannot_check`.
  - A check row whose entry exists but whose input documents are not in the room is `missing`.
  - A check row with no entry yet, or whose missing input is not expected at this stage, is `not_checked`. This is the one status FRAMEWORKS does not list; it keeps "missing" meaning "something to ask for".
  - An outside row is `checked` when its scan wrote a claim for it, and `not_checked` otherwise. An outside row is never `missing`, because Tricorder fetches it itself.
  - An ask row (kind "ask") the stage expects is `missing` until the founder answers.
  - Any other row not expected at the stage is `not_expected`.
- **CC-R6. Matching a file to a document.** First the file-name patterns in a table in the module, kept in line with `scans.base.INPUT_KINDS`. Then, for a file no pattern matches, the room's own index (the cover note's "What it is" column). The `hollis_voice_file` column is a test oracle for the Hollis Voice rooms, not the matcher, because its locations are wrong for other rooms (on Brasswick the spike, using that column, marks C30 found at "slide 5" and C96 at "slide 13", Hollis Voice's slides; `spike/out/brasswick_auto.json`). A match qualified in the column, such as C75's "terms stated there; no SAFE documents", is `found` with the qualifier as a note.
- **CC-R7. Each row says why.** Found rows name the file. Checked rows name the claim ids. Missing check rows name the missing input rows. Not-checked rows say whether no check exists or its input is not expected.

### Ask list

- **CC-R8. Missing items become requests.** Every `missing` document or ask row that the stage marks "yes" becomes a request. Marked "lighter", it is asked "if you have it" (`if_you_have_it: true`).
- **CC-R9. Missing checks fold into their file's request.** A `missing` check row adds no line of its own. Its id is added to the request for each missing input document. One line can cover many ids: on the seed drop at Series A, the request for monthly revenue by customer covers 19 (`spike/out/seed_drop_series_a.json`).
- **CC-R10. Nothing a later stage expects is asked for.** No line asks for an item whose stage mark is "no" or "not stated" at the company's stage. This holds for gap lines too: a gap whose document the stage does not expect stays a gap in the readout and gets no ask line. On the seed drop at pre-seed, 5 gap requests are held back this way (`spike/print_counts.py`).
- **CC-R11. Request text comes from the document guide.** The line's `what` is the guide's one-line request from its "If it is missing" section. A row with no guide (C23, C97, C99, C100, C101) gets "Please send: <item>." until a guide exists. The text names no flag and no motive ([BRAND.md](../../ongoing/BRAND.md), "Writing to the founder").
- **CC-R12. Entry 1.11's asks.** Bank statements (C21), accountant-prepared statements (C01), tax returns (C79), IP assignments (C76) and customer references (C35) are asked through CC-R8 when missing. Bank statements, accountant-prepared statements and tax returns are marked for after the term sheet. When any claim carries severity "flag", the generic walk-through line (C71) is replaced by the ask-list step's one walk-through line per flag, and C71 is marked covered by them.
- **CC-R13. Entry 1.10's instrument reading.** Each SAFE, note and option grant listed on the cap table with no matching document in the room becomes a gap ("Not in the room: the signed SAFE for <holder>"), and so an ask line. A script reads the instrument rows. A model reads only the cap table's notes for grants with no row (1.10, question 4), and that part runs as a scan, never in the merge.

### Dedupe

- **CC-R14. No request twice.** After the ask-list step, no two lines have the same `what` after lowercasing, and no checklist item has both a gap line and a checklist line.
- **CC-R15. A gap wins over the checklist.** When a scan's gap names a document a checklist item covers, the gap's line stays (its words are more specific, for example "the Marlow pilot agreement") and the checklist adds no line. The checklist item's id is attached to that gap line. Two gaps that name two documents of one item (the Marlow pilot agreement and the Cedar & Pine order form, both under C34) stay two lines, because they are two documents. This keeps the readout slice's four seed-drop lines intact ([ROADMAP.md](../../ongoing/ROADMAP.md), "readout", Done when).
- **CC-R16. Rows that make the same request.** Two checklist rows that ask the founder for the same thing are folded into one line by a stated table. Today: C46 (customer reference calls) folds into C35 (customer references), whose guide line already asks for customers to call.

### Guides' proposed checks

- **CC-R17. A register of proposed checks.** Every proposed check in the 33 guides is listed once with its guide, its name, and a disposition: `built` (in this slice), `later` (named slice), or `operator` (Tricorder cannot check it). The spike counts 176 proposed checks, 128 model readings and 122 operator items (`spike/count_proposed_checks.py`, approximate).

### Output and page

- **CC-R18. Output fits the frozen schema.** Coverage writes two Panels into `readout.panels`: "checklist coverage" (one row per item) and "checklist coverage counts". It appends `AskItem`s with `from_kind: "checklist"` and `checklist_id` set. It needs no schema change before Saturday. Proposed additions for after Saturday are in the architecture.
- **CC-R19. The coverage panel on the readout page.** It shows the stage and its source, a way to change it, counts by status, the rows grouped by piece with "missing" as the default filter, and a link from each missing row to its ask line. It matches the prototype's behavior.
- **CC-R20. Runs offline and fast.** No network, no model. Runs in the merge on the demo laptop.

## Failure cases

| Case | Behavior | Requirement |
|---|---|---|
| Unknown stage: no deck, unreadable deck, or no stage line | Label `stage_unknown`, no statuses, no ask lines, the panel asks the operator to pick | CC-R3 |
| Stage outside the three (deck or operator says "Series B") | Same as unknown; the reason names the word found | CC-R3 |
| Item in two places: one file satisfies two rows (the cap table is C72, C75 and C95 on Hollis Voice) | Each row is found with the same file; no ask for any of them | CC-R5, CC-R6 |
| Item in two places: a check needs two missing files (C05 needs C03 and C34) | The check's id is attached to both requests; no line of its own | CC-R9 |
| Item in two places: a row is found by a qualified match but its signed documents are absent (C75) | C75 is found with its note; the 1.10 instrument gaps ask for each signed SAFE and carry C75 | CC-R6, CC-R13 |
| Dedupe between a gap and a checklist ask (the expense ledger gap and C23) | One line, the gap's words, with C23 attached | CC-R15 |
| Dedupe between two checklist rows (C46 and C35) | One line, C35's words, covering both | CC-R16 |
| Dedupe between the walk-through ask and the per-flag lines | C71's generic line is dropped once a flag exists | CC-R12 |
| A gap for a document the stage does not expect | The gap stays in the readout, no ask line | CC-R10 |
| A check returned `cannot_check` | The row is not `checked`; if its inputs are missing it is `missing`, otherwise `not_checked` | CC-R5 |
| checklist.csv has a stage value outside yes, lighter, no, not stated | The step fails loudly in tests; at run time the row is `not_expected` and a gap names the bad value | CC-R4 |
| A document row has no guide | Generic request text | CC-R11 |
| Brasswick or any non-Hollis room | Matching by index and patterns, not by `hollis_voice_file` | CC-R6 |

## UX

The prototype's behavior is the baseline ([02_prototype_decision.md](02_prototype_decision.md)). Copy follows [BRAND.md](../../ongoing/BRAND.md): "Ask for:", "Why:", "Not in the room:", and "if you have it". A missing document is never colored or worded as a red flag.

## Analytics and logging

None in the product. The step prints its counts to the merge's log line, so `bin/smoke` shows them.

## Rollout and flags

No flag. The merge skips a step whose module does not exist (`scans/memo/merge.py`, `_step`), so the step lands at any time without breaking the readout. The page hides the panel when the Panel is absent.

## Questions

Open, for Ken (from [02_prototype_decision.md](02_prototype_decision.md)):

1. "Not stated" items: never asked (recommended) or "if you have it".
2. Lines with no readout piece: under "the pitch itself" for Saturday (recommended), or a new group.
3. One line per SAFE (recommended) or one for all.
4. After-term-sheet lines on screen and tagged (recommended), or hidden.
5. Full list (recommended) or top five.
6. The guides' proposed checks: build only those that run on the demo rooms before Saturday (recommended), and leave the rest registered for later.

Open, for the captain (schema owner): whether to add a typed coverage field and two AskItem fields after Saturday ([04_architecture.md](04_architecture.md), "Proposed schema additions").

Resolved:

- **No model call.** FRAMEWORKS says so, and `scans/memo/merge.py` says asks never come from a model. The 1.11 ask text comes from the guides, not from 1.11's model prompt.
- **"Checked" is honest.** It needs a real claim. The spike's projection is a spike-only stand-in, labelled on every screen.
- **Gap words win over checklist words** (CC-R15), so the readout slice's four seed-drop lines survive.

## PM findings and dispositions

No separate PM reviewer was run. Findings from the spike and prototype, with dispositions:

| Finding | Disposition |
|---|---|
| `hollis_voice_file` is blank for C23 though `data_room/hollis_voice/02_financials/expense_ledger.csv` exists | Matcher uses patterns (CC-R6). The CSV fix is for the checklist owner; listed in Progress. |
| `hollis_voice_file` locations are room-specific and mislead on Brasswick | CC-R6 |
| `scans.base.INPUT_KINDS["contracts"]` includes `*/sow_*.pdf`; Brasswick's `04_contracts/sow_norrgate_software_studio.pdf` reads as a vendor's statement of work, not a customer contract | Coverage does not count SOWs as customer contracts. Flagged to the skeleton owner in Progress. |
| The roadmap's scope for the guides' proposed checks is larger than one slice | CC-R17 and question 6 |
