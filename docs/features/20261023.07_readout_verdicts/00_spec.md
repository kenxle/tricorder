# The readout gets verdicts and headline flags

The merge will fill the company overview and headline flags. Steering will use the same rules. No decision is waiting on Ken.

## Scope and behavior

This is the next open board item, TRI-pieces-top-flags (shared verdicts and headline flags), within the [readout roadmap slice](../../ongoing/ROADMAP.md#readout). It implements [the framework's piece and flag rules](../../ongoing/FRAMEWORKS.md#piece-verdicts).

- Assign verified claims to the fixed company pieces. Each piece gets a verdict, reason, claim links, and source counts.
- A flag makes its piece weak. Otherwise corroborated and contradicted claims determine the verdict. Empty pieces state what is missing.
- Rank green flags by independent sources, counting repeated pitch material as one source. Only strong pieces qualify.
- Rank red flags by the relative difference against a comparable computed figure or record. A flag without comparable figures stays inside its piece and does not get a headline rank.
- Keep one headline per piece. Settings limit the lists. Empty lists stay empty.
- Move steering to these modules. Retire the temporary implementation and its fallback wording.

The general `link` step, ask-list generation, connecting prose, and page styling remain separate work. The existing claim-support step and scan links provide the evidence for this slice. A missing link must not become invented corroboration. A green list may be empty when no supported claim qualifies.

## Approach

Move the useful rules from steering into `scans/memo/pieces.py` and `top_flags.py`. Both expose the merge's `apply(readout, room_dir)` interface. Steering calls these same functions directly. No schema or dependency change is needed.

Keep the old paths as retired notices pending Ken's cleanup, because repository rules prohibit agent file deletion. Move their tests to the merge package. Add behavior checks before implementing the changed rules.

## Verification

| Check | Owner | Evidence and state |
|---|---|---|
| Piece assignment, verdicts, source counts, reasons, missing data | Codex | Pending focused tests |
| Headline ranking, ties, limits, unrankable flags | Codex | Pending focused tests |
| Steering uses the merge rules and preserves revisions | Codex | Pending steering and route tests |
| Actual room scans, merge, memo export, and repeatability | Codex | Pending reproducible evidence script |
| Full Python suite and web build | Codex | Pending `bin/ci-py` and `bin/ci-web` |
| Independent integrated code and acceptance review | Independent reviewer | Pending after implementation |

## Readiness and progress

The base is `origin/main` at `dc3b0b0`. Work is isolated in `feat/readout-verdicts`. The Python environment is `/tmp/tricorder-readout-verdicts-venv`, installed from the root and data-room requirements, plus `pypdf` for the chart fixtures. The system Python lacked runtime dependencies.

The new steps pass their focused behavior tests. The actual room rebuilds and memo exports are captured by [verify_rooms.py](verify_rooms.py), with [one row per claim](evidence/claims.csv) and [the room summaries](evidence/summary.json). The current scans do not yet emit enough numeric peer claims and links for the framework's full headline example. This slice follows the available evidence rather than filling the missing flags by inference.

Integration exposed a memo bug: headline text bypassed the existing cleanup of script paths. The export now applies that same cleanup to headline text. Tests that assumed these merge steps did not exist now cover current results or explicitly cover a legacy readout without verdicts.

The completed change goes through a pull request with the full checks passing. The roadmap's whole readout slice stays open until linking, asks, and connecting prose are handled.

## Cleanup paths for Ken

- `steering/verdicts.py`, after its callers have moved.
- `steering/tests/test_verdicts.py`, after its behavior tests have moved.
