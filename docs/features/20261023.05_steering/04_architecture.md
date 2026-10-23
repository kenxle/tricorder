# Architecture: steering in one sentence

PRD: [03_prd.md](03_prd.md). System: [ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md), "Steering" and "How the readout is built". Store interface: [readout store, 04_architecture.md](../20261023.01_readout_store/04_architecture.md).

## Summary

A steer is one call: `steering.engine.steer(room_dir, piece, sentence, claim_id=None, author=None)`. It loads the room's readout, reads the sentence, reruns the piece's scans on the right room, applies the one script reread the sentence asks for, quote-checks what changed, rebuilds verdicts by the FRAMEWORKS rules, writes a `PieceRevision` and a "what changed" Panel, writes the readout back and saves it to the store. The server route and the page are thin layers over it.

## What exists (reconnaissance, 2026-10-23)

- `scans/memo/merge.py`: `build_readout(room_dir)` and `STEPS`. Of the steps, only `coverage` exists. `pieces` and `top_flags` are not built on any branch.
- `scans/redflags/`: entries 1.12 (`mislabels`) and 1.14 (`deck_vs_books`). Entry 1.3 (`cohorts`) is listed in `CHECKS` but has no module, so nothing feeds the retention piece.
- No scan has a model reading yet, so a rewrite has no model prompt to pass the sentence to.
- `schema/claim.py` has `Steer`, `PieceRevision` and `Readout.revisions`.
- The store (`store/`, branch `forge/readout-store`): `open_store().save(fund, company, readout, room_dir, results)` copies the files the sources name from `room_dir`.

## Components

| Part | File | Job |
|---|---|---|
| Sentence reading | `steering/classify.py` | `read_sentence(sentence, llm=None) -> Reading`. Model path through `clients.llm.read` (route `bulk`) when `ANTHROPIC_API_KEY` is set and `TRICORDER_OFFLINE` is not; wording rules otherwise. The model's answer is checked against the sentence (STEER-R3). |
| Rereads | `steering/rereads.py` | `exclude_from_recurring(term, claims, room_dir, new_id, author)`: the one definition reread (STEER-R6). Reads P&L cells through `schema.readers.xlsx_sheet`; uses `figure_matches` from `scans.redflags.deck_vs_books` for the flag rule; finds the agreement's notice clause with `scans.redflags.contract_reader.read_room` (read-only). Returns the scenario claims, notes, the check line each replaces, and the check's own figure. |
| Rewording | `steering/reword.py` | The model's rewording of a piece's lines and its `guard` (STEER-R9): the same figures in the same order with the same units, each stated against the same source word, and the same agree, differ, up, down and negation words. Never used without a key. |
| Verdicts | `steering/verdicts.py` | `rebuild(readout, room_dir)`: runs the merge's `pieces` and `top_flags` steps when they exist; otherwise steering's copy of FRAMEWORKS "Piece verdicts" steps 1, 3, 4, 5 and "Top green and red flags". `piece_of(claim)` is the step 1 table plus a check-name table for claims with no value or the label `other`. |
| Engine | `steering/engine.py` | `steer(...)` and the diff. `operator(author)` (request, else `TRICORDER_OPERATOR`). `claim_room`: the room a line's source opens from (`scans.memo.merge.reads_room`). `scenario_reasons`: a piece the operator steered reads its scenario line as its reason. `carry(before, fresh, room)`: what a rebuild keeps from a steered readout. |
| Source room and rebuilds | `scans/memo/merge.py` | `READS_PANEL`, `reads_panel`, `reads_room(readout, room_dir)`, `readout_room(room_dir)`: the room a readout's sources resolve in. `build_readout(room_dir, keep_steers=True)` keeps a steered readout's record through `steering.engine.carry`; `python -m scans.memo <room> --fresh` starts over. |
| CLI | `steering/__main__.py` | `python -m steering <room_dir> <piece> "<sentence>" [--line <claim id>]`, for the terminal and the verification map. |
| Entry 1.3, script half | `scans/redflags/cohorts.py` | The Cohorts tab's stated NRR as a claim; with the customer file, the rebuilt NRR and GRR and the cohort counts (FRAMEWORKS 1.3, mechanical check), and the Panel "cohort retention rebuild" listing every customer-file row each cohort sums. The NRR and GRR lines cite the file's header row and name the script and the panel. No model reading. |
| Routes | `server/steering_routes.py` | `POST /api/rooms/{room}/steer`, `GET /api/rooms/{room}/steerable`, `GET /api/rooms/{room}/revisions`, `GET /api/rooms/{room}/claims/{claim_id}/sources/{i}` (the source text from `engine.claim_room`). One `include_router` line in `server/app.py`, above the static mount. |
| Page | `readout/src/Steering.tsx`, `readout/src/steerApi.ts`, `readout/src/steer_main.tsx`, `readout/steer.html` | `SteerableSection` (loads `/steerable`) and `SteerableOverview`: the overview with a box on the overview, per piece and per line. Mounted in `App.tsx` in place of the Overview section; `/steer.html` serves it alone. `vite.config.ts` has a second build input. |

## Data shapes

`steering/models.py`, owned by steering, not by `schema/`:

- `Reading`: `kind` (`rewrite` or `more_info`), `path` (`model`, `rules`), `term` and `treat_as` for a definition, `number_text` for a number request, `source` (`full_room`, `named`, or none) and `source_named`, `fallback_why` (why the model path was not used).
- `SteerReading`: what the model returns (strict, structured output). Same facts, no path.
- `RewordReading`: `lines: [{claim_id, text}]`.
- `SteerOutcome`: `readout`, `revision` (`PieceRevision`), `changes` (the Panel), `reading`, `source_room`, `store` (`{version, new}` or the reason it did not save).

The Panel `steer N: what changed` has columns `Change`, `Claim`, `Before`, `After`. Rows, in order: `headline` (the diff's first line), `typed on` (a piece or `overview`), `read as`, `added`, `dropped`, `replaced` (the check line a scenario line replaces, and the scenario line's id), `wording`, `unverified`, `verdict`, `piece moved`, `reason`, `source` (seed drop to full room), `number`, `rebuilt by`. The page reads the headline, replacements, wording changes and the room switch from it, because `PieceRevision` has no field for them. It leaves `read as` and `rebuilt by` off the screen.

The full-room switch is also its own Panel, so every reader finds it without reading steer panels (review wave 2b, B1):

    {"name": "reads room", "columns": ["Room", "Since"], "rows": [["hollis_voice", "steer 1"]]}

It is written once, by the steer that switched, and kept by every later steer and every rebuild. `scans.memo.merge.reads_room` reads it (and, for readouts steered before it existed, the steer panel's `source` row). It counts only when the name is the seed drop's own sibling full room; any other name is ignored, so a readout cannot send a reader to another folder.

## Flow

1. Load `out/<room>/readout.json`, or build it with `build_readout` if only scan results exist. With no results, the route answers 404.
2. If the readout has no pieces, `verdicts.rebuild` adds them, so the before has a verdict.
3. `read_sentence`. Number request first (STEER-R4), then more info, then a rewrite.
4. Which scans to rerun: for a rewrite, every scan whose claims or gaps sit in that piece in the before readout (if none, every available scan); for "read the full room", every available scan.
5. Rerun them (`scan.run`, `write_result`) on the source room: the room the readout reads for a rewrite, the full room for "read the full room". Then `build_readout(source room)`.
6. Match fresh claims with the before claims by `(check name, label, unit, period, number)`, or by text when there is no value. Matched claims keep their ids. New ones get `.steerN`. A rewrite takes only the piece's claims; a full-room read takes the whole fresh readout (claims, gaps, asks, panels) and keeps the operator's scenario lines and steer panels.
7. Rewrite only: the definition reread, or the model rewording.
8. Quote-check each added or reworded claim against the source room.
9. A first `steer N` panel with only the `replaced` rows goes in, then `verdicts.rebuild` and `scenario_reasons` on the combined readout. The full panel replaces it.
10. The revision: `verdict_moved_by` is, when the verdict moved, the added or dropped claims whose mark (contradicted or corroborated) decides the new verdict by the rule; if none, the after piece's `reason_claim_ids`.
11. Append the revision and the Panel, write the readout to `out/<room>/readout.json`, and save to the store with `room_dir` set to the source room (the full room holds every seed-drop file, so every source resolves there).

## Alternatives

- **Pass the sentence into the scans.** The ARCHITECTURE wording. No scan has a model reading yet, so there is nothing to pass it to. The engine has the seam (step 5); when scans grow readings, a `steer` argument goes there.
- **Edit the deck-vs-books check to accept a definition.** Rejected: it is another feature's code, and a reread outside the scan keeps the check's own number untouched by construction.
- **Write `scans/memo/pieces.py` now.** Rejected for this slice: the step is the readout slice's and would change every readout on merge. `steering/verdicts.py` is ready to move there.
- **Point new claims' sources at `../hollis_voice/...`.** Rejected: paths leaving the room are refused by the readers and the store. The readout keeps its room; once switched it reads the full room, and the claim-source route reads every line's source there.
- **Rerun only the steered piece on "read the full room".** The first round did, and the page then mixed seed-drop and full-room pieces. Both persona reviews read that as the whole page having switched. Rejected in the fix round.

## Failure modes

- A rerun scan crashes: `ScanFailed` names the scan, the route answers 500 with it, and nothing is written: every scan runs before any result is written (review wave 2b, O2).
- A rebuild (`POST .../readout`, `python -m scans.memo`, a founder upload) of a steered readout keeps its revisions, steer panels, scenario lines and switch, and a switched seed drop rebuilds from the full room's results (review wave 2b, S7). A founder file added to the seed drop after a switch is saved there, but the rebuild reads the full room's results, so it shows only once the full room has it too.
- Steer fields are size limited at the route: `sentence` 1,000 raw (500 after spaces collapse, in the engine), `author` 80, `claim_id` 120, `piece` and `fund` 64. Over the limit is a 422 (review wave 2b, S3).
- The store refuses: the steer stands; `store` carries the reason.
- Two steers at once on one room: the second reads the readout the first wrote, or the one before it. Last write wins on `out/`; the store keeps both versions. Acceptable on one laptop.

## Security and data

- Room names come through the server's `room_dir` (its id pattern and room list). The full room is only ever the sibling folder named without `_seed_drop`, found under the same parents.
- No outside fetch. A named outside source is noted, never fetched.
- The model sees the sentence and the piece's claim texts only, never a file.

## Proposed schema changes

For the captain, after Saturday. Steering works without them.

1. `PieceRevision.wording_changed: list[{claim_id, before, after}]`, so the diff does not need a Panel.
2. `PieceRevision.read_by: Literal["model", "rules"]` and `rebuilt_by: Literal["merge", "steering"]`, instead of the note.
3. `PieceRevision.source_room: str | None`, so the page knows where a more-info claim's file lives.
4. `Claim.steer: int | None`, the revision that added it, instead of the `.steerN` id suffix.
