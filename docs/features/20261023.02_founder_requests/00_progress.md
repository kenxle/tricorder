# Feature progress: requests to the founder

**Now (2026-10-23 02:45 UTC).** Fix round done on branch `forge/founder-requests`, after the orchestrator's independent persona review (both "workable", email not sendable as drafted). All seven fixes taken, test-first ([02_prototype_decision.md](02_prototype_decision.md), FR-R22 to FR-R28 in [03_prd.md](03_prd.md)), driven again on port 8812 ([06_verification.md](06_verification.md), fix-round section). `python3 -m pytest`: 276 passed, 0 failed; `bin/ci-py` and `bin/ci-web` pass. **Next:** the orchestrator's code review and integration.

Roadmap slice: [founder-requests](../../ongoing/ROADMAP.md#founder-requests). Route: prototype first.

## Attention needed

- **Claim support owner: the claims scan crashes on a hiring plan without a `headcount_after_hire` column** (`scans/claims/evidence.py`, `_hiring`, `KeyError`). A founder's own hiring plan will rarely have that column. The add still finishes and the receipt says "One check could not read the new file, so its part of the readout is from before." (test `test_a_plan_in_the_founders_own_columns_still_lands`, fixture `synthetic_brasswick_hiring_plan_own_columns.csv`). The main fixture now uses the repo's hiring plan columns.

- **Orchestrator: the independent persona reports are recorded from your relay.** Their full text was not in a shared folder; 02_prototype_decision.md says so. If you kept them, a link there would help.
- **Orchestrator: shared files touched.** `server/app.py` (one import and one `include_router` line, placed above the page mount: a mount at `/` placed first answers every path, so a router below it is never reached; keep this order at merge). `readout/src/App.tsx` (one import and one `<FounderRequests room={readout.room} />` under the ask-list section). `pyproject.toml` (`founder_requests` added to `testpaths`, or its 48 tests never run in `bin/ci-py`). `.claude/skills/verify-tricorder/features/` (my map file and one README line, as asked).
- **Coverage owner: the readout's own ask list still repeats itself and asks for files the room holds.** On Brasswick, line 3 (C14's guide text, "Send monthly revenue by customer so we can rebuild retention...") and line 1 (a red-flag gap's `would_need`) ask for monthly revenue by customer while `03_metrics/revenue_by_customer.csv` is in the room; material agreements (23) repeats 24, 25, 28 to 32; equity (13, 17) repeats the 409A and grants; line 29 asks for consulting agreements beside a contractor SOW. The founder email now fixes this on its own side (FR-R22, FR-R23, using `match_document` with pattern-only matching, unedited), but the ask list on the readout page does not. Also: with `room_dir` set, `match_document`'s contained-text rules count C20 as held (the model's P&L sheet) and C75 as held (cap table text), so this feature calls it with `room_dir=None`.
- **Coverage owner: closing paperwork in the ask list at seed.** Coverage stages C74, C76 and C77 "before the second meeting"; this feature moves them after the term sheet at pre-seed and seed (FR-R24). The ask list's own `ask_stage` could do the same.
- **Red-flag owner: gap `would_need` text is still a fragment** ("monthly balance sheets"). `founder_requests.draft.founder_text` turns it into "Please send monthly balance sheets." and strips cell references (review U8), so the founder never sees the raw text; the readout's own ask list still does.
- **Captain: no built red-flag check reads a hiring plan** (entry 1.4 is not built). The hiring-plan reply reruns `redflags` and changes the readout through coverage, but adds no claim yet.
- **Ken: defaults set.** The working copy of a synthetic room is `rooms/<room>_live` (`founder_requests.intake.COPY_SUFFIX`); the upload limit is 25 MB a file (`TRICORDER_UPLOAD_MAX_MB`), four times that for one add; the reply date defaults to a week from today with the reason "before our partner meeting"; the sign-off reads `TRICORDER_OPERATOR_NAME` and `TRICORDER_FUND_NAME`, and the page remembers the two fields in the browser.
- **ARCHITECTURE.md (not edited, ongoing docs are off limits):** the folder table could name `founder_requests/` beside `memo/`, `inbox/` and `store/`, and the environment table could add `TRICORDER_ROOMS_DIR`, `TRICORDER_UPLOAD_MAX_MB`, `TRICORDER_OPERATOR_NAME` and `TRICORDER_FUND_NAME`.

## Documents

- [product_thinking.md](product_thinking.md): the job, evidence, assumptions, priority
- [01_brief.md](01_brief.md): short brief
- [02_prototype/prototype.html](02_prototype/prototype.html) and [02_prototype_decision.md](02_prototype_decision.md): prototype, screenshots, independent persona review and what was taken
- [03_prd.md](03_prd.md): requirements FR-R1 to FR-R28
- [04_architecture.md](04_architecture.md): package, data shapes, flows, security
- [05_plan.md](05_plan.md): slices and the verification table
- [06_verification.md](06_verification.md): the driven recipe, Done when line by line, test results
- [evidence/](evidence/): first run; [evidence/fix_round/](evidence/fix_round/): the fix-round drive, with its Playwright script
- Verification map: `.claude/skills/verify-tricorder/features/founder-requests.md`
- `spike/`: `build_prototype.py`, `prototype_template.html`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Product note, brief | this thread | done | linked above | none |
| Prototype from real output, screenshots | this thread | done | `02_prototype/proto_*.png` | Ken clicks through |
| Persona review | orchestrator | done, independent | 02_prototype_decision.md | none |
| Fix round (7 items) | this thread | done | FR-R22 to FR-R28; `evidence/fix_round/` | code review |
| PRD, architecture, plan | this thread | done | linked above | none |
| Guidance and draft | this thread | done | `founder_requests/tests/test_guidance.py`, `test_draft.py` | none |
| Intake | this thread | done | `founder_requests/tests/test_intake.py` | none |
| CLI and routes | this thread | done | `test_cli.py`, `server/tests/test_founder_requests_routes.py` | none |
| Panel on the page | this thread | done | `bin/ci-web`; `evidence/page_*.png` | mount line kept at merge |
| Verification run | this thread | done | [06_verification.md](06_verification.md) | independent review |

## Decisions and events

- 2026-10-23 01:45 UTC: worktree made from `origin/main` at `cc86536`.
- 2026-10-23 01:50 UTC: guidance written by hand from each guide, one entry per guide (33), tied to the guide's sections by a test. Reading the guides live was rejected: their words are for investors.
- 2026-10-23 01:52 UTC: raw-body upload instead of multipart, so no new dependency.
- 2026-10-23 02:00 UTC: merged `origin/main` (verify-tricorder skill, accounting mislabels). Full suite green after.
- 2026-10-23 02:05 UTC: recipe driven on run `founder-requests`, port 8812; instance stopped by `control.sh cleanup`.
- 2026-10-23 02:20 UTC: independent persona review relayed by the orchestrator; fix round started.
- 2026-10-23 02:25 UTC: held files are found with coverage's patterns only (`room_dir=None`); its contained-text rules marked the balance sheets and prior financing as held when they are not.
- 2026-10-23 02:30 UTC: several files go up as one JSON batch with base64 bodies, so still no multipart dependency.
- 2026-10-23 02:40 UTC: fix-round drive on run `founder-requests-r2`, port 8812; two defects found and fixed test-first; instance stopped by `control.sh cleanup`.
- 2026-10-23 03:00 UTC: merged `claude/project-thread-ea11in` (claim support). Tests now derive the expected scans from each scan's NEEDS (`conftest.ready_scans`). A scan now waits only for input files written since its last run, since the claims scan leaves some kinds out on purpose and would otherwise rerun on every add. The receipt says a relabelled claim in its new words: on Brasswick the hiring plan turns three deck hiring claims from Supported to Contradicted.
- No human approval was asked for or needed; the orchestrator integrates.

## To delete at cleanup

- `rooms/brasswick_live/` in this worktree: the working copy made by the verification run (git-ignored).
- `rooms/brasswick_r2/` and `rooms/brasswick_r3/` in this worktree: the fix-round working copies (git-ignored).
- `/tmp/tricorder-verify/founder-requests/` and `/tmp/tricorder-verify/founder-requests-r2/`: the run folders (out, evidence copy, server log).
- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/founder-requests/`: scratch readouts, Playwright scripts, the 409A stub.
- `readout/dist/` and `readout/node_modules/` in this worktree: built by `bin/ci-web` (git-ignored).
