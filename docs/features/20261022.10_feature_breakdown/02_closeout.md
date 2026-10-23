# Wave 2 closeout: readout store, founder requests, memo export, contract terms, steering, claim support

Written 2026-10-23 at the Feature Forge closeout of wave 2. The plan for the wave is [00_breakdown.md](00_breakdown.md), with its "Wave 2 status" section. The review is [review_wave2a.md](review_wave2a.md). Each feature's progress page holds its own record, and now opens with a "Landed" line.

## What landed

| PR | What | Merged to `main` |
|---|---|---|
| #5 | pstack's `create-verification-skill` and `maintain-verification-skill`, installed unchanged in `.claude/skills/` (MIT, with `UPSTREAM.md` naming the revision) | 2026-10-23 |
| #8 | Wave 2: the six features below, the review fix round and the integration fixes | 2026-10-23, merge commit `60c45d5` |

- `bin/ci-py` on `main` after PR #8: 648 passed, 0 failed. `bin/ci-web` passes. GitHub CI was green on PR #8.
- Ken saw real output from the merged code on his Mac: the Hollis Voice memo in Lahe and its PDF, built from `main` at `60c45d5` in a separate worktree, `~/Documents/workspace/tricorder-wave2`. The readout page itself (steering and founder requests) is not built there yet: its `npm ci` waits on Ken's approval on the Mac.

| Feature | Code | Acceptance | Progress page |
|---|---|---|---|
| Readout store and delete | `store/`, `python -m store`, `server/store_routes.py` | All three Done when lines, on Hollis Voice through `control.sh` | [00_progress.md](../20261023.01_readout_store/00_progress.md) |
| Requests to the founder | `founder_requests/`, `server/founder_requests_routes.py`, `readout/src/FounderRequests.tsx`, `server/local_guard.py` | All three Done when lines on Brasswick, in Chromium and from the command line | [00_progress.md](../20261023.02_founder_requests/00_progress.md) |
| The memo and its PDF | `memo/`, `server/memo_routes.py` | All four Done when lines on Hollis Voice: every section filled or one gap line, two clicks to a source, every PDF claim footnoted, the quote checker passes | [00_progress.md](../20261023.03_memo_export/00_progress.md) |
| Contract terms in full | `scans/redflags/contract_reader.py`, `contract_terms_full.py` | All six Done when lines. The Marlow pilot is flagged with eight plan months past its term; Cedar & Pine and Brookline Row are cleared | [00_progress.md](../20261023.04_contract_terms/00_progress.md) |
| Steering in one sentence | `steering/`, `server/steering_routes.py`, `readout/src/Steering.tsx` | All five Done when lines, through `control.sh` and in Chromium | [00_progress.md](../20261023.05_steering/00_progress.md) |
| Claim support | `scans/claims/`, `scans/memo/claim_support.py` | Every figure labelled and quote-checked in all four rooms. Open: Hollis Voice GF2 and GF3's 17 staff read unsupported, because only the financial model states them (board row TRI-wave2-defaults) | [00_progress.md](../20261023.06_claim_support/00_progress.md) |

Test functions per feature, counted with `grep -c "def test_"` over each feature's test files at closeout: store 28, founder requests 57, memo 44, steering 40, claims scan 53, contract terms 29, the claim-support merge step 17, and the new route and guard tests 30.

### Docs changed at closeout

- [ROADMAP.md](../../ongoing/ROADMAP.md): a Status line on each of the six slices, naming the code, the PR and what is still open.
- [ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md): the store and server rows of "The stack" (the store folder and the local guard); the folder table gains `founder_requests/` and `steering/`, and says which of `memo/`, `inbox/` and `store/` are built; the merge steps gain `claim_support` after `link`, as `scans/memo/merge.py` runs them; the steering, founder-request and memo sections name their routes; the environment table gains the seven new variables. `.env.example` gains the same seven.
- [diagrams/system.md](../../ongoing/diagrams/system.md): steering, founder requests, the memo, the store and the guard drawn in.
- [BULLETIN.md](../../BULLETIN.md): TRI-forge-wave2 marked done, and one row per open item below.

### Check scripts at closeout

Run after the doc changes, all on 2026-10-23:

| Script | Result |
|---|---|
| `docs/ongoing/check_frameworks_numbers.py` | PASS: 67 figures checked against the key, 7 stale figures checked for absence |
| `docs/ongoing/checklist_counts.py` | Runs (exit 0); it prints counts and has no pass or fail |
| `docs/features/20261022.01_hackathon_plan/check_asks_table.py` | PASS: 53 slices, 53 rows |
| `docs/features/20261022.01_hackathon_plan/check_saturday_hours.py` | PASS |
| `docs/features/20261022.01_hackathon_plan/check_brief_words_and_links.py` | 0 broken links in PRODUCT_BRIEF.md and FEATURES.md |
| A relative-link check over every file this closeout changed | 3 broken links, none added here: ROADMAP.md links `../../../my-text-reminders/docs/ongoing/ROADMAP.md`, a folder outside the repo, and the contract-terms progress page links `spike/out/` and `spike/out/spike_run.txt`, which were never committed |

## Verification skill

Every feature has its map file in `.claude/skills/verify-tricorder/features/`, listed in that folder's README, and each was driven once by its own recipe through `control.sh`. The evidence is in each feature folder's `evidence/`. One gap in the skill: `control.sh shot` captures only `/`, so the memo page was driven by the memo's own `spike/drive_memo.js` (board row TRI-wave2-small-fixes).

## Open items

Each item has an owner and a board row. None blocks Saturday.

| Item | Owner | Board row |
|---|---|---|
| Whether the wave 2 defaults stand: a steer may add a figure, the model alone is not support, the loopback guard, store delete and `out/`, `rooms/<room>_live` and 25 MB, the memo's notes and section routing, contract terms Q1 and Q2 | Ken | TRI-wave2-defaults |
| `scans/memo/pieces.py` and `top_flags.py`, then retire `steering/verdicts.py` | readout slice, Saturday | TRI-pieces-top-flags |
| An independent code and security review of the memo and steering, and a persona re-read of the memo's fix round | agent | TRI-wave2-review-memo-steering |
| Coverage: C172 to `clause_notes`, the ask list's repeats, closing paperwork staging, the seven contract ask lines | agent (coverage owner) | TRI-coverage-wave2 |
| Claim sentences and gap requests written for people, not as checker output | agent (red-flag and claims owners) | TRI-claim-sentences |
| Claim support: comparable Values for BF1 and BF3, PF2's check name, decoys by locator, slide 9, extraction beyond the deck and script | agent | TRI-claim-support-followups |
| The readout page: Panels, a memo link, a store panel, the duplicate 357 clinics line | readout-page slice, Saturday | TRI-page-wave2 |
| One operator variable, contracts-only uploads through the API, the memo driver in the verify skill | agent | TRI-wave2-small-fixes |
| After Saturday: the schema proposals in the store, memo, steering and claim-support architecture docs | captain (schema owner) | none; each is in its feature's `04_architecture.md`, "Proposed schema changes" |
| Reader scenarios, stage views, video moments | blocked on the financial model, outside-in and the recorded pitch video | [00_breakdown.md](00_breakdown.md), "Wave 2 status" |

## Lessons

### a. Two features went to merge without an independent code review

- **What happened.** The code and security review ran on the four features ready first. Memo export and steering were still in their fix rounds, so the review read them only where they touch shared files. They merged with persona reviews and their own drives, but no independent code review.
- **Evidence.** [review_wave2a.md](review_wave2a.md), "What was inspected": "Out of scope, but read where they touch shared files: `memo/`, `steering/`, `scans/redflags/cohorts.py`."
- **Why it matters.** Both add server routes. The security findings the review did make (S1 cross-site writes, S2 a blocked event loop) were in routes.
- **Prevention.** The review brief lists every feature in the wave, and a feature left out is named in the closeout with a board row, as here (TRI-wave2-review-memo-steering). The local guard now covers every route, including theirs, because it is middleware and not per route.

### b. Tests that pinned another feature's output broke at integration, again

- **What happened.** Wave 1's lesson b (a test pinned the size of a living doc) came back in a new form. As features merged, tests that pinned a claim count, a claim id or an engine's name broke on other features' claims. Adding the claims scan renumbered every red-flag id after it (review S10).
- **Evidence.** Commits `bc62a40` (memo tests derive every expectation from the readout the scans built), `a18af58` (founder-requests tests follow each scan's NEEDS), `bd60d89` (steering tests build readouts with every available scan), `d2378f5` (an engine name is looked for as code names it, so "2 claims changed" is not a leak), and `e000e77` (red-flag ids are numbered per module).
- **Prevention, by structure.** Ids are now `redflags-<module>-NNN`, so a new module cannot renumber another's claims. A test of the readout derives its counts from the readout the scans built. The second half is a habit, not a check, so the next review looks for literal counts of another feature's output.

### c. Parallel worktrees still share one stash and one object store

- **What happened.** Wave 1's lesson e (one worktree per builder) was applied and held: no builder saw another's red tests. But a stray `git checkout origin/main -- .` in the readout-store worktree staged main's files over the builder's, and the clean-up stash it made sits on the stack every worktree shares.
- **Evidence.** The [readout-store progress page](../20261023.01_readout_store/00_progress.md), "Process note". The stash is `stash@{0}` in the cloud clone.
- **Prevention.** The next wave's builder brief says never to run a bare `git stash` or `git stash pop`, because the stack is shared, and never to check out another ref's files over a worktree. A stash that must be made carries a message naming the feature, and it goes on the cleanup list, as this one did.

### d. Frequent commits made a container restart cheap

- **What happened.** The cloud container restarted mid-wave and stopped five running builders. Each was resumed where it stopped, because each had committed after every test-first step.
- **Evidence.** No builder redid a step. Each feature's commits from before and after the restart are both in PR #8.
- **Prevention.** Keep "commit by path, often" in the builder brief. It is the only thing that made the restart a non-event.

### e. Persona reports given only by message are lost

- **What happened.** The founder-requests persona reports were relayed to the builder in a message, and their full text was never saved in the feature folder.
- **Evidence.** The founder-requests progress page: "Their full text was not in a shared folder; 02_prototype_decision.md says so."
- **Prevention.** A persona subagent writes its report into the feature folder (`persona_<name>.md`) before it returns. The decision doc links the file.

### f. The cloud container's environment drifted

- **What happened.** `/dev/null` became a regular 48-byte file in the container during the wave. A copy of the downloaded pstack skills with `cp` was refused by the session's permission check, so the files were read and written one by one.
- **Evidence.** The claim-support progress page, item 11. The pstack files were compared with `cmp` against the download after writing (PR #5).
- **Prevention.** Nothing in the repo; neither touched the code. The verify skill's `doctor` could check that `/dev/null` is a device, if it happens again.

### g. No new "Ken decided" for an orchestrator default

- **What happened.** A grep at closeout for "Ken decided", "Ken's decision", "Ken's call" and "Ken's default" under the wave 2 folders and their code found one line, in the memo's progress page, and it named a question for Ken, not a decision. It now reads "Open for Ken".
- **Evidence.** `grep -rn -E "Ken decided|Ken's decision|Ken's call|Ken's default"` over `docs/features/20261023.0*`, `store`, `founder_requests`, `memo`, `steering`, `scans/claims` and `scans/redflags/contract*`.
- **Prevention.** TRI-who-decided, from wave 1, still stands as the check script.

## Unverified conditions

- The readout page with steering and founder requests has not run on Ken's Mac. It ran in Chromium in the cloud container, light and dark, for each feature's drive.
- No model reading ran live. There is no `ANTHROPIC_API_KEY` in the cloud container or on the Mac, so each model path was tested on hand-built responses, labelled as such, and every readout is the script readings alone.

## To delete at cleanup

Nothing was deleted by an agent. For Ken's cleanup:

- The builder and review worktrees under `/home/claude/wt/` in the cloud clone (`readout-store`, `founder-requests`, `memo-export`, `contract-terms`, `steering`, `claim-support`, `review`) and their local `forge/*` and `review/wave2a` branches. Their work is on `main` through PR #8.
- `stash@{0}` in the cloud clone: copies of main's files from the readout-store worktree's stray checkout, nothing of value.
- In the founder-requests worktree, git-ignored: `rooms/brasswick_live/`, `rooms/brasswick_r2/`, `rooms/brasswick_r3/`.
- `docs/features/20261023.06_claim_support/02_prototype/` in the claim-support worktree: an empty folder.
- On Ken's Mac: the worktree `~/Documents/workspace/tricorder-wave2`, once he is done looking at wave 2 there.
- Each feature page lists its own scratch files. Files under `/tmp` are left to the operating system.
