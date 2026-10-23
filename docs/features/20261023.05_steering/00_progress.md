# Feature progress: steering in one sentence

**Now.** Built and verified on branch `forge/steering` (cut from `forge/readout-store`). Every Done when line passes on the wording-rule path, driven through `control.sh` and in Chromium ([06_verification.md](06_verification.md)). Full suite 319 passed; `bin/ci-py` and `bin/ci-web` green. **Next:** the orchestrator merges, mounts the page component, and Ken answers the three PRD questions.

Roadmap slice: [steering](../../ongoing/ROADMAP.md#steering). Route: prototype first.

## Attention needed

1. **Ken: may a definition steer make a new figure?** "Treat the pilot as non-recurring" adds ARR $2,060,868 computed from two P&L cells, beside the check's $2,240,868. [03_prd.md](03_prd.md), Questions 1 to 3.
2. **Readout slice owner (captain): `scans/memo/pieces.py` and `top_flags.py` do not exist.** Steering carries a copy of the FRAMEWORKS rules in `steering/verdicts.py` and uses the merge's steps as soon as they exist. The copy can move into `scans/memo/` as is. Until then the readout page (`App.tsx`) shows no pieces; only `/steer.html` does.
3. **Entry 1.3 owner (design-and-finance): `scans/redflags/cohorts.py` is new**, the script half of the cohort rebuild (PF3), written so "read the full room" on retention has a check to rerun. It adds 3 claims on Hollis Voice; the model half is still yours.
4. **Store owner: `store/tests/test_cli.py` edited.** It asserted 10 Hollis Voice claims; with cohorts there are 13. It now reads the count from the readout its fixture built. Any new redflags check (contract terms too) would have broken it.
5. **Orchestrator: mount the page.** Put `<SteerableOverview readout={readout} onReadout={setReadout} />` from `readout/src/Steering.tsx` in `App.tsx` in place of the Overview section (ReadoutView needs the readout from `getSteerable`, or `steering.engine.steerable`'s pieces). `readout/vite.config.ts` gained a second input (`steer.html`); drop it once mounted, if wanted.
6. **Shared files touched:** one import and one `include_router` line at the bottom of `server/app.py` (above the static mount); `pyproject.toml` `testpaths` gains `steering`; `readout/vite.config.ts`.
7. **Schema proposals** (captain, after Saturday): [04_architecture.md](04_architecture.md), "Proposed schema changes" (wording changes, read-by and rebuilt-by, source room, the revision that added a claim).
8. **Persona review ran inline**, not as subagents (no subagent tool in this session). Rerun the two persona agents on `/steer.html` screenshots.
9. **Demo:** with no key the demo runs fully offline on the wording rules. The overview card's "live steer needs the network" is not true for these three sentences.

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
| Persona review | builder | done, inline | [02_prototype_decision.md](02_prototype_decision.md) | rerun as agents |
| Slice 1: entry 1.3 script half | builder | done | `scans/redflags/tests/test_cohorts.py` | owner adds the model half |
| Slice 2: reading and verdicts | builder | done | `steering/tests/test_classify.py`, `test_verdicts.py` | none |
| Slice 3: engine and CLI | builder | done | `steering/tests/test_engine.py` | none |
| Slice 4: routes | builder | done | `server/tests/test_steering_routes.py` | none |
| Slice 5: page | builder | done | `bin/ci-web`; `evidence/steer_*.png` | mount in App.tsx |
| Slice 6: verification | builder | done | [06_verification.md](06_verification.md) | none |

## Decisions and events

- 2026-10-23 02:02 UTC: worktree on `forge/steering` from `forge/readout-store` (4aa2cc8).
- Wrote the 1.3 script half and a verdict stand-in, because no built check fed retention and no verdict step existed (see Attention needed 2 and 3).
- A definition steer adds a computed line rather than changing the check's line (PRD question 1, open for Ken).
- During the drive: a more-info store save copied full-room files nothing cited; fixed to keep the readout's own results (commit 5185dc7).
- No human approval was needed or given.

## To delete at cleanup

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/steering/` (scratch out folders and the Node Playwright install)
- `/tmp/tricorder-verify/steering-trial/` (a trial run before the real one)
- `/tmp/tricorder-verify/steering/` (the run folder; its evidence is copied into `evidence/`)
- `readout/node_modules/` and `readout/dist/` in this worktree (git-ignored, built by `bin/ci-web`)
