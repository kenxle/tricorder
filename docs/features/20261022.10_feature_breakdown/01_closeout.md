# Wave 1 closeout: deck-vs-books, accounting mislabels, checklist coverage

Written 2026-10-23 at the Feature Forge closeout of wave 1. The plan for the wave is [00_breakdown.md](00_breakdown.md). The review is [review_wave1.md](review_wave1.md). Each feature's progress page holds its own record.

## What landed

| PR | What | Merged to `main` |
|---|---|---|
| #1 | The persona review agents (`.claude/agents/persona-*.md`, [PERSONA_REVIEWS.md](../../ongoing/PERSONA_REVIEWS.md)) | 2026-10-23 |
| #2 | The architecture skeleton: schema, readers, quote checker, scan framework, memo merge, score, server, CI | 2026-10-23, merge commit `dc0be0e` |
| #4 | Wave 1: the three features below, their review fix round and the CI fix | 2026-10-23, merge commit `dc10bbc` |

- `bin/ci-py` on `main` after PR #4: 203 passed. GitHub CI was green on PR #4's head, `229f8db`.
- The three features' own test files hold 163 of the 203 (`python3 -m pytest -q` on each file at closeout): 53 for deck-vs-books, 68 for mislabels, 42 for coverage.
- Ken saw real output from the merged code on the wave 1 demo page ([claude.ai artifact](https://claude.ai/artifact/S8Cyt8ZTsjrmL8ydAZmHuc)), built by [demo/build_demo.py](demo/build_demo.py).

| Feature | Code | Acceptance | Progress page |
|---|---|---|---|
| Deck revenue against the books | `scans/redflags/deck_vs_books.py` | Brasswick: "found BF2", decoys flagged 0 of 3. Hollis Voice: the deck's $2,500,000 ARR flagged against the P&L's $2,240,868 (11.6%) | [00_progress.md](../20261022.11_deck_vs_books/00_progress.md) |
| Accounting mislabels | `scans/redflags/mislabels.py` | Brasswick: BF1, BF3 and BF4 found. No decoy flagged in any of the four rooms | [00_progress.md](../20261022.12_accounting_mislabels/00_progress.md) |
| Checklist coverage and the ask list | `scans/memo/checklist.py`, `scans/memo/coverage.py` | Every roadmap Done when check passes on the real merge. Slices 3 and 4 are still open | [00_progress.md](../20261022.13_checklist_coverage/00_progress.md) |

### Docs changed at closeout

- [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md): entry 1.14 (deck revenue against the books) added under Scan 1, with its two rows in "Where each planted flag is caught" and its row in "When each entry runs". Entry 1.12 took all four proposed changes: the kind e plan test and vendor propagation, the kind g bridge test, Brasswick as the room for kind c, and "the financial model workbook" in place of "the model". "Checklist coverage" now lists the `not_checked` status and the default on "not stated" items. Both proposal files stay in place, marked applied.
- [ROADMAP.md](../../ongoing/ROADMAP.md): the three slices marked done, with links. Deck-vs-books' Done when names BF2 and says the late test deck is "reported". The skeleton is marked merged.
- [ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md): the `scans/redflags/` row names entry 1.14, and the coverage step names its five statuses.
- [BULLETIN.md](../../BULLETIN.md): TRI-forge-wave1 and TRI-architecture marked done, and one row per open item below.

### Check scripts at closeout

Run after the doc changes, all on 2026-10-23:

| Script | Result |
|---|---|
| `docs/ongoing/check_frameworks_numbers.py` | PASS: 67 figures checked against the key, 7 stale figures checked for absence |
| `docs/ongoing/checklist_counts.py` | Runs; it prints counts and has no pass or fail |
| `docs/features/20261022.01_hackathon_plan/check_asks_table.py` | PASS: 53 slices, 53 rows |
| `docs/features/20261022.01_hackathon_plan/check_saturday_hours.py` | PASS |
| `docs/features/20261022.01_hackathon_plan/check_brief_words_and_links.py` | 0 broken links in PRODUCT_BRIEF.md and FEATURES.md |

The check names in `scans/memo/checklist.py` (`ENTRY_CHECKS`, `ROW_CHECKS`) were compared with FRAMEWORKS.md by a script. Before closeout, `deck_revenue_vs_pnl` and `deck_history_vs_metrics` were the only two not quoted in FRAMEWORKS. Entry 1.14 now quotes both. Coverage maps them under entry 1.5, which checks row C65. That still works, because no checklist row names 1.14 yet.

## Verification skill

The project's verification skill, `.claude/skills/verify-tricorder/`, was generated with pstack's create-verification-skill and merged in PR #6 (merge 26237f8). Its feature map covers the three wave 1 features and the readout page. It was proven end to end once in the cloud container: launch, doctor, the deck-against-books recipe on three rooms, the Brasswick score (found 4 of 5, decoys flagged 0 of 3), a page capture, cleanup, and the evidence still present after cleanup. Its first runs found two helper bugs, both fixed before merge: a subshell made cleanup stop the wrong process, and evidence files written in the same second overwrote each other. Run `/maintain-verification-skill` to keep the map honest as wave 2 lands.

## Open items

Each item has an owner and a board row. None blocks Saturday.

| Item | Owner | Board row |
|---|---|---|
| Whether the wave 1 defaults stand: partial history as flag or watch, Brasswick January against December (review U2), the six coverage defaults | Ken | TRI-wave1-defaults |
| The readout groups `deck_revenue_vs_pnl`'s ARR flag with the engine's PF2 flag | readout slice, Saturday | TRI-readout-group-flags |
| Entry 1.2's flag cites `ARR_Build!E13`, so the mislabels `mrr` flag links to it | redflag-engine slice, Saturday | TRI-arr-cites-e13 |
| `scans/memo/asks.py` keeps coverage's lines and calls `gap_is_asked` | readout slice, Saturday | TRI-asks-seam |
| Coverage slices 3 and 4, and the prototype's persona review | agent | TRI-coverage-panel |
| Checklist rows C110 to C114 have no file pattern; C111 misses Brasswick's SOW | agent | TRI-checklist-new-rows |
| `checklist.csv` C23 has no `hollis_voice_file` | agent (checklist owner) | TRI-c23-hollis-file |
| `scans/base.py` `INPUT_KINDS` counts Brasswick's vendor `sow_*.pdf` as a customer contract | agent (skeleton owner) | TRI-input-kinds-sow |
| `data_room/README.md` misstates BF2's percentage | agent (data-room owner) | TRI-brasswick-readme |
| A check for "Ken decided" phrases (lesson c) | agent | TRI-who-decided |
| After Saturday: a tenth ask-list group for company records, in place of "the pitch itself" | captain (schema owner) | none; recorded in the coverage [04_architecture.md](../20261022.13_checklist_coverage/04_architecture.md) |

## Lessons

### a. A fix-round test turned CI red

- **What happened.** The deck-vs-books fix round added six tests that built test slides without the skip guard. GitHub CI installs no pypdf, so those tests errored there while they passed on the builder's machine.
- **Evidence.** Commit `e0551fb`: "CI has no pypdf, and six fix-round tests built slides without the skip guard."
- **Prevention, by structure.** The guard `need_deck_tools()` now runs inside the shared slide-size helper `_deck_size` in `scans/redflags/tests/deck_vs_books_fixtures.py`. Every slide builder goes through that helper, so a new test cannot build a slide without the guard.

### b. A test pinned the size of a living doc

- **What happened.** A coverage test asserted 109 checklist items. Ken's checklist update on `main` grew the list to 193 items with stable ids, and the test broke on the merge.
- **Evidence.** Commit `b9ab9c4`. `test_every_item_has_one_status` now uses `len(checklist.load())`.
- **Prevention, by structure.** The test reads the count from `checklist.csv`. A test of a doc that people edit computes its expected count from that doc.

### c. Builders wrote "Ken decided" for orchestrator defaults

- **What happened.** The orchestrator set defaults while Ken was away. Builders recorded some of them as Ken's decision or Ken's default.
- **Evidence.** At closeout, grep found 8 such doc lines across the deck-vs-books and coverage folders (00_progress, 03_prd, 05_plan, 02_prototype_decision) and 2 code comments in `scans/memo/checklist.py`. The doc lines now read "default chosen by the orchestrator, open for Ken". The code comments wait for the next code PR (TRI-checklist-new-rows).
- **Why it matters.** A default recorded as Ken's decision hides a question Ken never answered.
- **Prevention.** A check script lists every such phrase for the orchestrator to confirm at closeout (TRI-who-decided). The open defaults also sit on one board row for Ken (TRI-wave1-defaults), so they stay visible.

### d. 84 new checklist rows arrived with no matching rules

- **What happened.** Rows C110 to C193 landed on `main` during the wave. On the seed drop at Series A, coverage reports `not_expected` 0 for all 193 items.
- **Evidence.** A script over `checklist.csv` at closeout: every row has a value in all three stage columns, the new rows included. The Series A column holds 157 "yes", 25 "not stated" and 11 "lighter", and no "no". The real merge on `main` (counts on the [coverage progress page](../20261022.13_checklist_coverage/00_progress.md)) puts all 75 new check rows at "not checked yet" in every room, and all 5 new document rows (C110 to C114) at missing.
- **What follows.** `not_expected` 0 at Series A is correct, not a bug. No row says "no" for Series A, and default 1 counts "not stated" as expected. The real gap is matching. The new check rows wait for checks that carry their names, which is true and harmless. The new document rows have no file pattern, so they always read missing, and C111 (consulting agreements) is asked of Brasswick although its room holds a statement of work.
- **Prevention.** A test that every document row in `checklist.csv` has a file pattern or is listed as asked only (TRI-checklist-new-rows). A new row then fails the suite until someone decides how it is found.

### e. Parallel builders in one working tree saw each other's red tests

- **What happened.** The three builders worked in the same checkout. One builder's full-suite run caught another's tests in their red phase.
- **Evidence.** The coverage progress page: "One earlier run in the round showed 2 failures in `scans/redflags/tests/test_deck_vs_books.py` while that builder's own test-first round was in progress." The mislabels page: an earlier run "set aside `scans/memo/tests/test_coverage.py` ... while another agent's checklist module was still missing."
- **Why it matters.** A failure that belongs to someone else costs a rerun and trains builders to ignore red.
- **Prevention, by structure.** One worktree per builder, merged into the integration branch when green. This is a proposal for the orchestrator's process. If Ken wants it as a project rule, it is one line in AGENTS.md, and that change needs his approval.

### f. A plan marked "Pass" on tests that skipped the real path

- **What happened.** Some verification rows passed on tests that called a helper directly, not the module's entry point.
- **Evidence.** Review S1: the half-step rule was tested through `figure_matches()` with a hand-passed value, and never ran in production. Review S11: `test_no_request_twice` called `coverage.apply` though the plan said it ran the real merge, and `test_cannot_check_is_not_checked` passed no claims at all.
- **Prevention.** The fix round required each new test to go through the real `check()` or `build_readout`. The reviewer kept one rule: a Pass row whose test does not call the entry point it names is a fail. A future plan's verification row names that entry point, so the reviewer can check it in one look.

### g. "The model" meant two things in FRAMEWORKS

- **What happened.** Entry 1.12 said the seed-drop fallback reads "the model". The coordinator read it as a language model and asked for a downgrade rule. It meant the financial model workbook.
- **Evidence.** The mislabels progress page, item 1 before closeout.
- **Prevention.** Entry 1.12 now says "the financial model workbook (`financial_model.xlsx`)". `test_makes_no_model_call` replaces every function in `clients/llm.py` with one that fails and runs the seed drop, so the fallback cannot quietly start calling a model.

### h. Saving a generated workbook with openpyxl empties its totals

- **What happened.** A mislabels test edited the Brasswick workbook with openpyxl and saved it. openpyxl drops cached formula values, so every total read as empty.
- **Evidence.** The mislabels progress page, "Decisions and events", and review U10.
- **Prevention.** The tests patch the parsed P&L in memory instead of saving the file. A test needs no saved workbook to drop a cell.

## To delete at cleanup

- `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`: generated test rooms (untracked).
- The worktree `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/wt2` and its local branch `tmp-ce34ga`. Its work is on `main` through PR #2 and PR #4. Remove with `git worktree remove --force` and `git branch -D tmp-ce34ga`.
- Each feature page lists its own scratch files. Files under `/tmp` are left to the operating system.
- The local branch `claude/verify-skill-tmp` in the cloud clone (made by mistake while committing the verification skill; its one commit is on main).
