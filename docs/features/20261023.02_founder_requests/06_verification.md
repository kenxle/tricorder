# Verification: requests to the founder

## Fix round (2026-10-23, after the independent persona review)

Driven again by the recipe, run `founder-requests-r2`, port 8812, `TRICORDER_OFFLINE=1`, at revisions `477d06a` (command line and API drafts) and `e160691` (the page drive, the CLI add and the readback; the server was relaunched after each code change, and the branch head after it changes only docs). Evidence is in [evidence/fix_round/](evidence/fix_round/), copied after `control.sh cleanup` ("stopped pid 26804", 33 files kept). The working rooms are `rooms/brasswick_r2` and `rooms/brasswick_r3` (git-ignored), because `rooms/brasswick_live` from the first run still exists and is not deleted; the page drive's final pass used `brasswick_r3`. `cli_20261023T0234*` are from before the last two fixes; the current draft is `cli_20261023T023546Z_25458_3459.txt`.

| Check | Result | Evidence |
|---|---|---|
| Top five settles the decision first | Pass. Default: revenue by customer (reworded to what is missing), investor updates, the cohort export behind the deck's retention figure, monthly financial statements, the hiring plan. Incorporation, IP assignments and minutes read "After the term sheet". | `cli_20261023T023545Z_25447_14332.txt` (list), `r2_page_draft_light.png` |
| No ask for a held file, no ask twice | Pass. The revenue line asks only for the kind of revenue per row and an MRR column; the cohort line asks for the export behind the deck's figure; 32 readout lines become 22 items (material agreements, option grants and 409A, people we can call merged). | `cli_20261023T023545Z_25447_14332.txt`, `api_20261023T023546Z_25478_30135.json` |
| Short, warm, dated, signed email that fits a mail link | Pass. "Brasswick: a few things before our next meeting"; "by Friday 6 November ... before our partner meeting"; signed "Sam Ortiz / Example Ventures"; mailto 1,750 characters (CLI) and 1,744 (page), no long-link warning. | `cli_20261023T023546Z_25458_3459.txt`, `r2_page_copied_text.txt`, `r2_page_mailto.txt`, `r2_page_drive.json` |
| Trust line, plain sample-room line, no check codes | Pass. The drawer reads "Tricorder never sends this. Copy it, or open it in your own mail app and send it from there."; the add box reads "This is a sample room, so the files go into a working copy of it."; no `C<number>` in the panel's text (`codes_in_panel: []`). | `r2_page_drive.json`, `r2_page_draft_*.png` |
| Several files, one file for several lines, add box reachable | Pass. The add box is beside the list at its top on desktop (`intake_above_list_px: 0`) and above the list on a phone. Two files in one add: the hiring plan for "Hiring plan", the reference list PDF for "People we can call: Reference list ..." and "People we can call: Founder reference calls". | `r2_page_two_files_ready_*.png`, `r2_page_add_phone_*.png` |
| Receipt in plain words | Pass. "Coverage now finds Hiring plan and future org." "Coverage now finds Reference list: ..." "Founder reference calls is something only the founder can give, so no check reads the file. The line stays on the ask list." "No check reads these files yet, so no number changed." "The ask list is down from 32 to 30 lines." | `r2_page_receipt.txt`, `r2_page_reply_added_*.png` |
| Readback | Pass. The red-flag result's `inputs` list `05_team/hiring_plan.csv`; coverage rows C22, C97 and C73 read `found`; no C22 ask remains; the log lists all three files. | `api_20261023T023811Z_27045_25685.json`, `api_20261023T023811Z_27057_30540.json`, `r2_received.txt` |
| CLI add and refusals | Pass. `add rooms/brasswick_r3 <409A>.pdf --for C73`: "Coverage now finds 409A valuation." "No check reads this file yet, so no number changed." Upload to `brasswick` 409 with the copy command; `..%2F..%2Fescape.exe` 415; `git status --short data_room` empty. | `cli_20261023T023811Z_27033_8932.txt`, `r2_curl_refusals.txt` |
| Phone width | Pass. No horizontal scroll at 390 px (`phone_horizontal_scroll: false`). | `r2_page_draft_phone_*.png`, `r2_page_add_phone_*.png` |

The drive itself found two defects, each fixed test-first and driven again: the reworded revenue line still told the founder how to build the file they had sent ("Ideally it includes ..."), and the receipt said "this file" for two files and promised a way to take a line off the ask list that the page does not have.

Tests after the fix round: `python3 -m pytest` 276 passed, 0 failed; `bin/ci-py` passed (schema check, then 276 passed); `bin/ci-web` passed. Feature tests: guidance 4, draft 16, intake 36, CLI 5, routes 12.

## After the claim-support merge (2026-10-23)

Merged `claude/project-thread-ea11in`. Two scans now rerun on a hiring plan (`redflags`, `claims`). The receipt with both, on a Brasswick copy (`two_scan_receipt.txt` in the scratch folder, quoted here): "Coverage now finds Hiring plan and future org." "Coverage now finds Reference list: ..." "Customer reference calls is something only the founder can give, ..." "4 claims changed. Now: Contradicted: The deck (slide 10) gives planned hires as 7 hires, but hiring plan (row 6) says 5, 28.6% lower. Contradicted: The deck (slide 10) gives staff after hiring as 14, but hiring plan (row 6) says 19, 35.7% higher. ..." "The ask list is down from 36 to 34 lines." A 409A file still reads "No check reads this file yet, so no number changed." No scan name appears. The page was not driven again for this merge.

`bin/ci-py`: 518 passed, 6 failed, all six in `memo/tests/` (the known failures its builder is fixing). `bin/ci-web` passed.

## First run

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
