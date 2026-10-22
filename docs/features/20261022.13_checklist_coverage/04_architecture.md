# Architecture: checklist coverage

Requirements: [03_prd.md](03_prd.md) (CC-R1 to CC-R20). Verification: [05_plan.md](05_plan.md), "Verification". Product questions: [03_prd.md](03_prd.md), "Questions".

## Summary

Checklist coverage is one merge step, `scans/memo/coverage.py`, plus one small scan for the cap table's notes. The step is a pure script. It reads the checklist, the room's file list, the readout so far and the stage, and returns the readout with two Panels added and checklist ask lines appended. The ask-list step after it adds the gap and weak-piece lines and keeps the list free of repeats. The page shows the panel. Nothing in this slice calls a model, and nothing changes the frozen schema before Saturday.

## Existing structure (reconnaissance)

Read from branch `claude/project-thread-ce34ga` with `git show` on 2026-10-22, after the skeleton builder pushed it. These are the real names, not assumptions.

- **Schema.** `schema/claim.py`: Pydantic v2 models `Source`, `Value`, `Check`, `Claim`, `Gap`, `Panel`, `Piece`, `TopFlag`, `AskItem`, `ScanResult`, `Readout`, field for field the FRAMEWORKS JSON Schema. Frozen before Saturday; on Saturday only the captain changes it (its docstring).
  - `Gap(what, why, would_need, piece: PieceName | None = None)`.
  - `Panel(name: str, columns: list[str], rows: list[list[str]])`.
  - `AskItem(what, why, piece: PieceName, from_kind: "gap" | "weak_piece" | "checklist", claim_ids, checklist_id: str | None, if_you_have_it: bool)`. `piece` is required and must be one of the nine pieces.
  - `Readout(room, built_at, synthetic_notice, top_flags, pieces, claims, unverified, gaps, asks, panels, scans_run, scans_missing, revisions, connecting, scores)`. There is no stage field and no coverage field.
- **Merge.** `scans/memo/merge.py`: `build_readout(room_dir)` loads every `out/<room>/<scan>.json`, re-runs the quote checker, turns each missing scan into a gap, then runs `STEPS` in order: `link`, `pieces`, `top_flags`, `coverage`, `asks`, `connecting`. Each step is `scans/memo/<name>.py` with `def apply(readout: Readout, room_dir: Path) -> Readout`. A step whose module does not exist is skipped. Its docstring: "verdicts, flags and asks never come from a model".
- **Scan base.** `scans/base.py`: `INPUT_KINDS` (kind to glob patterns, for example `"customers": ("*/customer_mrr_by_month.csv", "*/revenue_by_customer.csv")`), `find(room, kind)`, `room_inputs(room)`, `gap(what, why, would_need, piece)`, `now_iso()`, `out_dir(room)`, `synthetic_notice(room)`.
- **Scans.** `scans/__init__.py` lists `SCANS` (redflags, comps, signals, video, claims, readings, model, frameworks, founders, presence, outside, bank). Contract: `NAME`, `NEEDS`, `run(room_dir) -> ScanResult`; `python -m scans.<name> <room_dir>` writes `out/<room>/<name>.json`. No scan reads another's output.
- **Readers.** `schema/readers.py`: `pdf_page`, `pdf_pages`, `xlsx_cell`, `xlsx_sheet`, `xlsx_defined_name`, `csv_rows`, `csv_row_text`, `md_line`, `transcript_segment`, `text_at(source, room_dir)`. A bad locator raises `schema.readers.LocatorError`.
- **Gate.** `bin/ci-py` runs `python -m schema.export --check`, then `pytest` over `schema`, `scans`, `server`, `eval`.
- **Checklist.** `docs/ongoing/checklist.csv`, 109 rows, columns `id, piece, kind, item, pre_seed, seed, series_a, stage_basis, comes_from, where, checked_by, check_status, check_exists, named_by, named_by_urls, hollis_voice_file` ([checklist_counts.py](../../ongoing/checklist_counts.py)).
- **Guides.** `docs/reports/20261022.03_document_guides/*.md`, 33 guides, each with an "If it is missing" section holding a quoted one-line request.

## Affected components

| Component | Change | Owner |
|---|---|---|
| `scans/memo/coverage.py` | New. The merge step. | this slice |
| `scans/memo/checklist.py` | New. Loads and validates checklist.csv; the pattern, input and same-request tables; guide ask lines. Pure functions the step and the ask-list step both import. | this slice |
| `scans/memo/asks.py` | The ask-list step (readout slice, Saturday). Must keep coverage's lines and call `checklist.items_for_gap()` for dedupe. A seam, not owned here. | captain |
| `scans/cap_notes/` | New scan for 1.10's model question 4 (cap table notes naming a grant with no row). Optional; see Plan slice 4. | this slice |
| `scans/memo/tests/test_coverage.py`, `test_checklist.py` | New tests. | this slice |
| `readout/` coverage panel | New component reading the two Panels. | readout-page (frontend), built by this slice before Saturday against `sample_out/` |
| `server/app.py` | A route to set the operator's stage, writing `out/<room>/operator.json`. | this slice, with the skeleton owner's review |
| `docs/features/20261022.13_checklist_coverage/proposed_checks.csv` | New. The guides' proposed-check register (CC-R17). | this slice |

## Data shapes

Named before logic. All three live in `scans/memo/checklist.py` as plain dataclasses, internal to the merge. What reaches `readout.json` is only schema types: `Panel`, `AskItem` and `Gap`.

### ChecklistRow

One row of checklist.csv, validated on load: `id`, `piece`, `kind` (document, check, outside, ask), `item`, `stage: dict[str, Level]` with `Level` in yes, lighter, no, not stated, `checked_by_entries: list[str]` (entry numbers parsed from `checked_by`, for example `["1.2", "1.13"]`), `check_exists: bool`, `hollis_voice_file: str`. An unknown level fails the load (CC-R4).

### StageReading

```
stage: "pre_seed" | "seed" | "series_a" | None
source: Source | None        # the deck line, e.g. kind file, uri 01_overview/pitch_deck.pdf, locator "slide 1", quote "Series A  |  $9,000,000 ..."
deck_stage: same type as stage   # what the deck said, kept when the operator overrides
set_by: "deck" | "operator" | None
word: str | None             # the raw word found, for the stage_unknown reason ("Series B")
```

The operator's choice lives in `out/<room>/operator.json` as `{"stage": "seed", "set_at": "<iso>"}`. Coverage reads it if present. The stage-views slice reuses the same file for the operator's piece order.

### CoverageRecord (one per checklist item)

Extends FRAMEWORKS' `coverage` item (`item_id`, `status`, `claim_ids`, `ask`) with what the panel needs:

```
item_id: "C03"
status: "checked" | "found" | "missing" | "not_checked" | "not_expected"
expected: "yes" | "lighter" | "no" | "not stated"      # the row's mark at this stage
piece: PieceName | None          # readout piece; None for legal, AI governance, outside world
found_in: list[str]              # room-relative paths
note: str | None                 # qualifier, or why not_checked
claim_ids: list[str]             # claims whose check.name belongs to the row's entries
missing_inputs: list[str]        # checklist ids of absent input documents (check rows)
ask: int | None                  # index of the AskItem that covers this row
```

### Ask-list line

The schema's `AskItem`, unchanged. Coverage sets `from_kind="checklist"`, `checklist_id` to the requested document or ask row, `if_you_have_it` from the stage marks, `what` from the guide, `why` as "Not in the room: <item>." plus "Also needed for <check ids>" when checks fold in. Two things the schema has no field for travel in the coverage Panel instead: the full list of checklist ids a line covers, and the ask stage (before the second meeting or after the term sheet). The after-term-sheet mark is also written as the first words of `why` ("After the term sheet. ...") so the ask-list text carries it without a schema change.

### What reaches readout.json

- `Panel(name="checklist coverage", columns=["id", "item", "piece", "kind", "expected", "status", "detail", "ask", "covers"], rows=[...])`, one row per item, every cell a string.
- `Panel(name="checklist coverage counts", columns=["key", "value"], rows=[["stage", "series_a"], ["stage_set_by", "deck"], ["stage_source", "01_overview/pitch_deck.pdf, slide 1: Series A | $9,000,000"], ["label", "built"], ["checked", "20"], ...])`.
- `AskItem`s appended to `readout.asks`.
- `Gap`s from the 1.10 instrument reading appended to `readout.gaps` with `piece="the_pitch_itself"`. These are written by coverage because the merge, not a scan, holds the room file list and the cap table reading is a script. See "Alternatives" for the scan option.

### Proposed schema additions (after Saturday, captain's call)

1. `Readout.coverage: Coverage | None` with `Coverage(stage, stage_source: Source | None, set_by, label: "built" | "stage_unknown", records: list[CoverageRecord])`, replacing the two Panels.
2. `AskItem.covers: list[str]` (every checklist id the line settles) and `AskItem.ask_stage: "before_second_meeting" | "after_term_sheet"`.
3. `AskItem.piece` nullable, or a tenth group for company records, depending on Ken's answer to question 2 in the PRD.

Until then, legal and cap table lines use `piece="the_pitch_itself"` (FRAMEWORKS 1.10 already scores cap table claims there), and AI governance lines do the same. No AI governance row is expected at any stage today, so none is asked.

## Flows

### The coverage step, inside `build_readout`

```
apply(readout, room_dir):
    rows   = checklist.load(CHECKLIST_CSV)                       # fails on an unknown level
    stage  = read_stage(room_dir)                                # operator.json, else deck slide line, else claims.json
    if stage.stage not in STAGES:
        readout.panels += [counts panel with label stage_unknown and the reason]
        return readout                                           # no records, no asks (CC-R3)
    files  = room file list (relative paths)
    found  = {doc row: match(row, files)}                        # patterns, then the cover note index (CC-R6)
    checks = {entry: claims whose check.name maps to the entry}  # via a CHECK_NAMES table: "1.2" -> "arr_definition", ...
    records = [status(row, stage, found, checks) for row in rows]   # CC-R4, CC-R5
    inst_gaps = cap_table_instruments(room_dir, files)           # 1.10 script reading, CC-R13
    readout.gaps += inst_gaps
    lines = checklist_lines(records, stage, readout.gaps + inst_gaps)   # CC-R8 to CC-R12, CC-R15, CC-R16
    readout.asks += lines
    readout.panels += [coverage panel, counts panel]
    return readout
```

### The seam with the ask-list step

The ask-list step runs next. It owns the gap and weak-piece lines and the final order. Its contract with coverage:

1. It keeps every line with `from_kind == "checklist"`.
2. For each gap, it calls `checklist.items_for_gap(gap)` to get the checklist ids the gap's `would_need` names. If a checklist line for one of those ids exists, the gap line replaces it: the gap's words stay, the checklist id moves onto the gap line (`checklist_id`), and the checklist line is dropped (CC-R15). Coverage already skips ids named by gaps present at its run, so this is only needed for gaps written after it, which do not exist today. The rule lives in one function both steps call, so it cannot drift.
3. It skips a gap line whose ids are all not expected at the stage (CC-R10), using `checklist.expected(id, stage)`.
4. It drops the C71 line when it writes any per-flag walk-through line (CC-R12).
5. Its existing merge rule (same `what` after lowercasing) still runs last (CC-R14).
6. Order: pieces in `PIECE_ORDER`; inside a piece, gap lines, then weak-piece lines, then checklist lines.

If the ask-list step is not built when this lands, coverage's lines still reach the readout: the merge skips the missing step.

### Mapping a claim to a checklist row

`checked_by` holds entry names ("1.2 ARR definition check; 1.13 Contract terms"). Claims carry `check.name`, the entry's check name (for example `arr_from_subscription_rows` for 1.2, `cap_table_reconcile` for 1.10, `contract_price_vs_counted_price` for 1.13; a model claim adds `.read`). A table `ENTRY_CHECKS: dict[str, set[str]]` maps an entry number to its check names, copied from FRAMEWORKS' "Check name:" lines and kept in the module. A row is checked by any claim whose `check.name`, less a trailing `.read`, is in the set for one of the row's entries. Entries 1.12 and 1.13 hold several checks each, and each checklist row names one of them (C06 is 1.12 kind a, C42 is 1.13 check 5). For those rows a second table, `ROW_CHECKS`, names the exact check, so a claim from 1.12 kind b does not mark C06 checked. A test asserts every entry a checklist row names has at least one check name (TDD row CC-R5c in the Plan).

### Readout page

The panel reads the two Panels by name. It never recomputes a status. Changing the stage posts to the server route, which writes `operator.json` and reruns the merge (no scan reruns: coverage only reads their output). The page then reloads `readout.json`.

## Alternatives

| Option | Why not chosen |
|---|---|
| Coverage as a scan (`scans/coverage/`, writing `out/<room>/coverage.json`) | It must read the readout's claims to mark rows checked, and scans may not read other scans' output (`scans/__init__.py`). The skeleton reserved a merge step for it. |
| Coverage also writes the gap and weak-piece lines (owns the whole ask list) | Cleaner dedupe, but takes the readout slice's Saturday deliverable away from the captain and changes a slice that is already planned. The shared `items_for_gap` function gets the same result. |
| Use the `hollis_voice_file` column as the matcher | Wrong on any other room (Brasswick, the YC rooms). Kept as a test oracle. |
| Typed `Coverage` in the schema now | The schema is frozen; Panels carry everything the page needs. Proposed for after Saturday. |
| 1.10's instrument reading as a model call | The SAFE block is a table a script reads (`Cap_Table`, "SAFE conversion" rows, `spike/coverage_spike.py`, `cap_table_instrument_gaps`). Only the notes need a model, and that part is a small scan. |
| 1.11 as its own scan with its model prompt | Its `present()` test is coverage's found test for five rows, and its ask text is already in the guides. A model writing ask text would break "asks never come from a model". The tie-out half belongs to bank-check. |
| Treat "not stated" as "if you have it" | Waits on Ken (PRD question 1). One-line change in `checklist.expected()`. |

## Failure modes

- **Checklist edited with a new level or column.** Load fails in tests; at run time the row is `not_expected` and a gap names the value. The checklist owner reruns `checklist_counts.py` anyway.
- **Deck missing or unreadable.** `stage_unknown`, the panel asks. `readers.pdf_page` raising `LocatorError` is caught and treated as unreadable.
- **A scan crashes or is missing.** Its check rows read `missing` (inputs absent) or `not_checked` (inputs present, no claim). They never read `checked` on a projection.
- **The ask-list step ignores the seam contract.** A test on the merged readout asserts zero repeated requests (CC-R14), so the break shows in `bin/ci-py`.
- **Large rooms.** 109 rows, a file list and a claim scan: linear, well under a second.

## Security and privacy

Reads only the room folder, the checklist and the guides. Writes only `out/<room>/` through the merge, and `operator.json` through one server route that accepts one of three stage values and nothing else. No network. Request text is copied from repo files, never from room files, so a room cannot inject text into the ask list. Every room is synthetic.

## Selected findings

From the spike (`spike/coverage_spike.py`, run by `spike/run_all.sh`):

- The `hollis_voice_file` column misleads outside Hollis Voice, and is blank for C23 though the full room holds `02_financials/expense_ledger.csv`.
- `INPUT_KINDS["contracts"]` counts `sow_*.pdf`. Brasswick's SOW reads as a vendor contract. Coverage keeps SOWs out of C34.
- The seed drop at Series A has 33 missing check rows and 17 missing document rows; folding checks into documents is what keeps the list at 23 lines (`spike/print_counts.py`).
