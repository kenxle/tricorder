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
| Rereads | `steering/rereads.py` | `exclude_from_recurring(term, claims, room_dir, tag)`: the one definition reread (STEER-R6). Reads P&L cells through `schema.readers.xlsx_sheet`; uses `figure_matches` from `scans.redflags.deck_vs_books` for the flag rule. |
| Rewording | `steering/reword.py` | The model's rewording of a piece's lines and its number guard (STEER-R9). Never used without a key. |
| Verdicts | `steering/verdicts.py` | `rebuild(readout, room_dir)`: runs the merge's `pieces` and `top_flags` steps when they exist; otherwise steering's copy of FRAMEWORKS "Piece verdicts" steps 1, 3, 4, 5 and "Top green and red flags". `piece_of(claim)` is the step 1 table plus a check-name table for claims with no value or the label `other`. |
| Engine | `steering/engine.py` | `steer(...)` and the diff. |
| CLI | `steering/__main__.py` | `python -m steering <room_dir> <piece> "<sentence>" [--line <claim id>]`, for the terminal and the verification map. |
| Entry 1.3, script half | `scans/redflags/cohorts.py` | The Cohorts tab's stated NRR as a claim; with the customer file, the rebuilt NRR and GRR and the cohort counts (FRAMEWORKS 1.3, mechanical check). No model reading. |
| Routes | `server/steering_routes.py` | `POST /api/rooms/{room}/steer`, `GET /api/rooms/{room}/steerable`, `GET /api/rooms/{room}/revisions`. One `include_router` line in `server/app.py`, above the static mount. |
| Page | `readout/src/Steering.tsx`, `readout/src/steerApi.ts`, `readout/src/steer_main.tsx`, `readout/steer.html` | `SteerableOverview`: the overview with a box per piece and per line. Served at `/steer.html` until it is mounted in `App.tsx` in place of the Overview section. `vite.config.ts` gains a second build input. |

## Data shapes

`steering/models.py`, owned by steering, not by `schema/`:

- `Reading`: `kind` (`rewrite` or `more_info`), `path` (`model`, `rules`), `term` and `treat_as` for a definition, `number_text` for a number request, `source` (`full_room`, `named`, or none) and `source_named`, `fallback_why` (why the model path was not used).
- `SteerReading`: what the model returns (strict, structured output). Same facts, no path.
- `RewordReading`: `lines: [{claim_id, text}]`.
- `SteerOutcome`: `readout`, `revision` (`PieceRevision`), `changes` (the Panel), `reading`, `source_room`, `store` (`{version, new}` or the reason it did not save).

The Panel `steer N: what changed` has columns `Change`, `Claim`, `Before`, `After`. Rows: `added`, `dropped`, `wording`, `verdict`, `reason`, `source`, `read as`, `rebuilt by`. The page reads wording changes and the path from it, because `PieceRevision` has no field for them.

## Flow

1. Load `out/<room>/readout.json`, or build it with `build_readout` if only scan results exist. With no results, the route answers 404.
2. If the readout has no pieces, `verdicts.rebuild` adds them, so the before has a verdict.
3. `read_sentence`. Number request first (STEER-R4), then more info, then a rewrite.
4. Which scans feed the piece: every scan whose claims or gaps sit in that piece in the before readout; if none, every available scan.
5. Rerun those scans (`scan.run`, `write_result`) on the source room: the piece's own room for a rewrite, the full room for "read the full room". Then `build_readout(source room)`.
6. Match the fresh piece's claims with the before piece's by `(check name, label, unit, period, number)`, or by text when there is no value. Matched claims keep their ids. New ones get `.steerN`.
7. Rewrite only: the definition reread, or the model rewording.
8. Quote-check each added or reworded claim against the source room.
9. `verdicts.rebuild` on the combined readout.
10. The revision: `verdict_moved_by` is, when the verdict moved, the added or dropped claims whose mark (contradicted or corroborated) decides the new verdict by the rule; if none, the after piece's `reason_claim_ids`.
11. Append the revision and the Panel, write the readout to `out/<room>/readout.json`, and save to the store with `room_dir` set to the source room (the full room holds every seed-drop file, so every source resolves there).

## Alternatives

- **Pass the sentence into the scans.** The ARCHITECTURE wording. No scan has a model reading yet, so there is nothing to pass it to. The engine has the seam (step 5); when scans grow readings, a `steer` argument goes there.
- **Edit the deck-vs-books check to accept a definition.** Rejected: it is another feature's code, and a reread outside the scan keeps the check's own number untouched by construction.
- **Write `scans/memo/pieces.py` now.** Rejected for this slice: the step is the readout slice's and would change every readout on merge. `steering/verdicts.py` is ready to move there.
- **Point new claims' sources at `../hollis_voice/...`.** Rejected: paths leaving the room are refused by the readers and the store. The readout keeps its room; the page asks the source room for those claims' text.

## Failure modes

- A rerun scan crashes: the error propagates, nothing is written.
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
