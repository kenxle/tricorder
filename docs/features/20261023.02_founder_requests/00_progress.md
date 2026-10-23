# Feature progress: requests to the founder

**Now (2026-10-23 02:15 UTC).** Built, tested and driven once by the verify-tricorder recipe on branch `forge/founder-requests` (`origin/main` merged in). Every roadmap "Done when" line passes on Brasswick: [06_verification.md](06_verification.md). `python3 -m pytest`: 244 passed, 18 skipped (matplotlib, pre-existing), 0 failed; `bin/ci-py` and `bin/ci-web` pass. **Next:** the orchestrator's independent review and integration; a rerun of the persona review with real persona agents.

Roadmap slice: [founder-requests](../../ongoing/ROADMAP.md#founder-requests). Route: prototype first.

## Attention needed

- **Orchestrator: the persona review was run by the builder, not by independent agents.** This session had no tool to start a subagent. The findings in [02_prototype_decision.md](02_prototype_decision.md) are labelled so. Rerun `persona-associate` and `persona-partner` on `evidence/page_draft_light.png`, `page_reply_added_light.png` and `02_prototype/proto_*`.
- **Orchestrator: shared files touched.** `server/app.py` (one import and one `include_router` line, placed above the page mount: a mount at `/` placed first answers every path, so a router below it is never reached; keep this order at merge). `readout/src/App.tsx` (one import and one `<FounderRequests room={readout.room} />` under the ask-list section). `pyproject.toml` (`founder_requests` added to `testpaths`, or its 48 tests never run in `bin/ci-py`). `.claude/skills/verify-tricorder/features/` (my map file and one README line, as asked).
- **Coverage owner: two Brasswick ask lines ask for a file the room already holds.** Line 3 (C14, the cohort guide's text: "Send monthly revenue by customer so we can rebuild retention...") and line 1 (a red-flag gap's `would_need`: "monthly revenue by customer with a product type column") both ask for monthly revenue by customer, and `03_metrics/revenue_by_customer.csv` is in the room. A founder reading that may think the fund did not open the room. The draft sends the line's words as they are.
- **Red-flag owner: gap `would_need` text is still a fragment** ("monthly balance sheets"). `founder_requests.draft.founder_text` turns it into "Please send monthly balance sheets." and strips cell references (review U8), so the founder never sees the raw text; the readout's own ask list still does.
- **Captain: no built red-flag check reads a hiring plan** (entry 1.4 is not built). The hiring-plan reply reruns `redflags` and changes the readout through coverage, but adds no claim yet.
- **Ken: two defaults set.** The working copy of a synthetic room is `rooms/<room>_live` (`founder_requests.intake.COPY_SUFFIX`); the upload limit is 25 MB (`TRICORDER_UPLOAD_MAX_MB`).
- **ARCHITECTURE.md (not edited, ongoing docs are off limits):** the folder table could name `founder_requests/` beside `memo/`, `inbox/` and `store/`, and the environment table could add `TRICORDER_ROOMS_DIR` and `TRICORDER_UPLOAD_MAX_MB`.

## Documents

- [product_thinking.md](product_thinking.md): the job, evidence, assumptions, priority
- [01_brief.md](01_brief.md): short brief
- [02_prototype/prototype.html](02_prototype/prototype.html) and [02_prototype_decision.md](02_prototype_decision.md): prototype, screenshots, builder-run persona review
- [03_prd.md](03_prd.md): requirements FR-R1 to FR-R21
- [04_architecture.md](04_architecture.md): package, data shapes, flows, security
- [05_plan.md](05_plan.md): slices and the verification table
- [06_verification.md](06_verification.md): the driven recipe, Done when line by line, test results
- [evidence/](evidence/): transcripts, API responses, screenshots (light, dark, phone)
- Verification map: `.claude/skills/verify-tricorder/features/founder-requests.md`
- `spike/`: `build_prototype.py`, `prototype_template.html`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Product note, brief | this thread | done | linked above | none |
| Prototype from real output, screenshots | this thread | done | `02_prototype/proto_*.png` | Ken clicks through |
| Persona review | this thread | done, builder-run | 02_prototype_decision.md | orchestrator reruns with agents |
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
- No human approval was asked for or needed; the orchestrator integrates.

## To delete at cleanup

- `rooms/brasswick_live/` in this worktree: the working copy made by the verification run (git-ignored).
- `/tmp/tricorder-verify/founder-requests/`: the run folder (out, evidence copy, server log).
- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/founder-requests/`: scratch readouts, Playwright scripts, the 409A stub.
- `readout/dist/` and `readout/node_modules/` in this worktree: built by `bin/ci-web` (git-ignored).
