# Feature progress: steering in one sentence

**Now.** Fix round done on `forge/steering`, merged with `claude/project-thread-ea11in` (claims scan and claim support included). All eight items pass, driven through `control.sh` on port 8815 and in Chromium ([06_verification.md](06_verification.md)). Full suite after the last merge (320244e): 532 passed, 6 failed, the 6 known memo tests only. An earlier merge also showed 3 founder-requests failures; the integration branch has since fixed them. **Next:** the orchestrator merges.

Roadmap slice: [steering](../../ongoing/ROADMAP.md#steering). Route: prototype first.

## Attention needed

1. **Ken: a definition steer may add a new figure** beside the check's, labelled as the steer's. The coordinator made that call; Ken can reverse it ([03_prd.md](03_prd.md), question 1).
2. **Claims scan owner:** traction shows "gives paying customers as 357 clinics" twice (`evidence/fix_round/steer_traction_dark.png`).
3. **Readout slice owner (captain): `scans/memo/pieces.py` and `top_flags.py` still do not exist.** `steering/verdicts.py` is the stand-in; the readout page's overview now comes from `/steerable`, which uses it.
4. **Shared files touched:** `readout/src/App.tsx` (one import, the Overview section swapped for `SteerableSection`; the up and down buttons moved into it; a top flag now scrolls to its piece); `server/app.py` (one `include_router`); `pyproject.toml` testpaths; `readout/vite.config.ts`.
5. **Entry 1.3 owner:** `scans/redflags/cohorts.check()` now returns `(claims, gaps, panels)` and adds the panel "cohort retention rebuild".
6. **Setting:** `TRICORDER_OPERATOR` names who steers when the request does not. Unset, lines read "the operator's steer".
7. **Schema proposals** (captain, after Saturday): [04_architecture.md](04_architecture.md), "Proposed schema changes".

## Documents

- [product_thinking.md](product_thinking.md), [01_brief.md](01_brief.md)
- [02_prototype/prototype.html](02_prototype/prototype.html) and [02_prototype_decision.md](02_prototype_decision.md) (persona review inside)
- [03_prd.md](03_prd.md), [04_architecture.md](04_architecture.md), [05_plan.md](05_plan.md), [06_verification.md](06_verification.md)
- [verify_drive_page.mjs](verify_drive_page.mjs), the map at `.claude/skills/verify-tricorder/features/steering.md`, [evidence/](evidence/)
- `spike/`: `steer_spike.py`, `build_prototype.py`, `prototype_template.html`, `out/spike.json`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Spike and prototype | builder | done | `spike/out/spike.json`; `02_prototype/*.png` | none |
| Persona review | coordinator | done, both agents cold: workable, workable | [02_prototype_decision.md](02_prototype_decision.md) | none |
| Fix round, items 1 to 8 | builder | done | [06_verification.md](06_verification.md), `evidence/fix_round/` | none |
| Slice 1: entry 1.3 script half | builder | done | `scans/redflags/tests/test_cohorts.py` | owner adds the model half |
| Slice 2: reading and verdicts | builder | done | `steering/tests/test_classify.py`, `test_verdicts.py` | none |
| Slice 3: engine and CLI | builder | done | `steering/tests/test_engine.py` | none |
| Slice 4: routes | builder | done | `server/tests/test_steering_routes.py` | none |
| Slice 5: page | builder | done, mounted in App.tsx | `bin/ci-web`; `evidence/fix_round/steer_*.png` | none |
| Slice 6: verification | builder | done | [06_verification.md](06_verification.md) | none |

## Decisions and events

- 2026-10-23 02:02 UTC: worktree on `forge/steering` from `forge/readout-store` (4aa2cc8).
- Wrote the 1.3 script half and a verdict stand-in, because no built check fed retention and no verdict step existed (see Attention needed 2 and 3).
- A definition steer adds a computed line rather than changing the check's line (PRD question 1, open for Ken).
- During the drive: a more-info store save copied full-room files nothing cited; fixed to keep the readout's own results (commit 5185dc7).
- Fix round (coordinator, after both persona agents rated it workable): retention rows, the rewrite redoes the piece, headline first, author and time, full-room rerun of every piece, the pilot notice clause, the first-time example, the App.tsx mount. The coordinator answered PRD question 1.
- Merged `claude/project-thread-ea11in` twice; the second brought the claims scan, and the steering tests now build readouts with every available scan.
- Review wave 2a, O8: `cohorts.py` crashed on a blank month in the customer file. It now skips and counts unreadable rows and names them in a gap (commit 2360057; tests in `scans/redflags/tests/test_cohorts.py`).
- No human approval was needed or given.

## To delete at cleanup

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/steering/` (scratch out folders and the Node Playwright install)
- `/tmp/tricorder-verify/steering-trial/` (a trial run before the real one)
- `/tmp/tricorder-verify/steering/` (the run folder; its evidence is copied into `evidence/`)
- `readout/node_modules/` and `readout/dist/` in this worktree (git-ignored, built by `bin/ci-web`)
