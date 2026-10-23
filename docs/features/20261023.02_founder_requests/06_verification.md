# Verification: requests to the founder

Driven once by the project recipe, `.claude/skills/verify-tricorder/features/founder-requests.md`, on 2026-10-23 at revision `8ac8ec2` (branch `forge/founder-requests`, with `origin/main` merged), in a Linux cloud container. Run `founder-requests`, port 8812, `TRICORDER_OFFLINE=1`. Every room is synthetic. Every artifact is in [evidence/](evidence/), copied from the run's evidence folder after `control.sh cleanup` (which reported "stopped pid 9343" and "26 files" kept).

## Done when, line by line

| Roadmap "Done when" | Result | Evidence |
|---|---|---|
| On the Brasswick room, the ask list produces a request for its missing documents with guidance for each | Pass. 32 ask lines; the top-five draft greets "Hi Celia," and gives each document "What it is", "Best form" and "A good one shows". Every document line on Brasswick carries guidance (test `test_every_document_line_on_brasswick_carries_guidance`); three Brasswick lines carry none by design: current burn (C29) and founder references (C58), which only the founder can answer, and patents (C101), whose guide covers another document. | `cli_20261023T020332Z_*` (list), `cli_20261023T020341Z_*` (draft), `api_20261023T020341Z_9524_*` (one-line draft, `leaks: []`) |
| The operator can copy it or open it in their email client | Pass. On the page, "Copy text" put the subject and message on the clipboard ("Copied." shown); "Open in mail app" carries a `mailto:celia@example.com?subject=Brasswick%3A%20documents%20for%20our%20review&body=Hi%20Celia%2C...` link, 4,479 characters, so the page shows the long-link warning. | `page_copied_text.txt`, `page_mailto.txt`, `page_draft_light.png`, `page_draft_dark.png`, `page_draft_phone_dark.png` |
| A reply's attachment added to the room starts the waiting scans | Pass. Upload to `data_room/brasswick` refused (409, names the copy command; `git status --short data_room` empty). After the copy, the page added `synthetic_brasswick_hiring_plan.csv` for "6. Hiring plan": saved as `rooms/brasswick_live/05_team/hiring_plan.csv`; `redflags` ran again (its `inputs` now list the file, new `ran_at` 2026-10-23T02:05:08Z); the readout was rebuilt: C22 "missing before, found now", ask list 32 to 31, C24 now "not_checked" (no payroll check is built yet), and no `C22` ask remains. | `upload_to_synthetic_refused.txt`, `page_receipt.txt`, `page_reply_added_light.png`, `page_reply_added_dark.png`, `page_after_light.png`, `page_after_dark.png`, `api_20261023T020553Z_*` (redflags result and readout read back) |

Second entry point: `python3 -m founder_requests add rooms/brasswick_live "<synthetic 409A>.pdf" --for C73` saved `06_legal/brasswick_409a_report_2026.pdf`, C73 missing to found, asks 31 to 30, `scans_rerun: []` because no scan's input kinds name a 409A report (`cli_20261023T020527Z_*`). A bad kind (`..%2F..%2Fescape.exe`) was refused with 415 (`upload_bad_kind_refused.txt`).

The hiring plan and the 409A file are synthetic, written by the builder: `founder_requests/tests/fixtures/synthetic_brasswick_hiring_plan.csv` (with a README saying so) and a two-line PDF stub.

## What the rerun does and does not show

The red-flag scan reran because its last result had not seen `05_team/hiring_plan.csv`. No built red-flag check reads a hiring plan yet (entry 1.4, burn against the hiring plan, is not built), so the rerun adds no claim. The readout change comes from the merge's checklist coverage, which now finds the file. When 1.4 lands, the same upload will produce its claims with no change here.

## Test results

- `python3 -m pytest`: 244 passed, 18 skipped, 0 failed (2026-10-23, after the merge of `origin/main`). The 18 skips are the deck-vs-books fixture tests that need matplotlib (`data_room/requirements.txt`), not installed in this container; they skip the same way on `main`.
- `bin/ci-py`: `python -m schema.export --check` passed, then 244 passed, 18 skipped.
- `bin/ci-web`: type check and build passed (`dist/assets/index-*.js` 207.64 kB).
- Tests for this feature: `founder_requests/tests/` (guidance 4, draft 9, intake 31, CLI 4) and `server/tests/test_founder_requests_routes.py` (11).

## Testing findings and dispositions

| Finding | Disposition |
|---|---|
| The draft module began as the prototype spike, so its first tests were written after it | Recorded. Later draft behaviour (empty list refused, default fallback) went red then green. Intake, CLI and routes were test-first: the intake tests failed at import before `intake.py` existed; the CLI and route tests ran 14 red before the code. |
| `test_folders_and_names_on_brasswick` expected `monthly_metrics.csv` for a new metrics file, but Brasswick already holds one | The test was wrong; never overwriting is the rule. It now expects the file beside the old one. |
| A route test expected 404 for an encoded-slash path; with `readout/dist` built the page mount answers 405 | The test checks the request is refused and nothing is written. |
| The persona review was run by the builder, not independent agents | Open; see 00_progress.md, Attention needed. |
| No independent code review yet | Open; the orchestrator's review of the integrated branch. |
