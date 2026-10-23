# Review, wave 2a: readout store, founder requests, contract terms, claim support

Independent code-quality, completion and security review (Feature Forge, required before the pull request). The reviewer edited no code. This file is the only thing written to the repo, and it is left uncommitted.

## What was inspected

- Worktree `/home/claude/wt/review`, branch `review/wave2a` made from `claude/project-thread-ea11in`, HEAD `17fa2d20b6ad491f60dcf89ab3a2f616a1def48b`.
- Diff: `git diff e017a69...HEAD` on the four features' paths, plus `server/app.py`, `pyproject.toml`, `requirements.txt`, `scans/memo/merge.py`, `scans/redflags/scan.py`, `scans/redflags/__init__.py`. About 6,900 lines added in scope:
  - Readout store: `store/` (base, models, files, cli and tests), `server/store_routes.py`, `server/tests/test_store_routes.py`.
  - Founder requests: `founder_requests/` (guidance, draft, intake, CLI and tests), `server/founder_requests_routes.py`, `readout/src/FounderRequests.tsx`.
  - Contract terms: `scans/redflags/contract_reader.py`, `contract_terms_full.py`, `tests/test_contract_terms_full.py`, `tests/contract_fixtures.py`.
  - Claim support: `scans/claims/` (numbers, extract, kinds, evidence, label, read, scan, prompt and tests), `scans/memo/claim_support.py`, `scans/memo/tests/test_claim_support.py`.
- Authorities read: `CLAUDE.md`, `.claude/guardrails.md`, `docs/ongoing/ARCHITECTURE.md`, `docs/ongoing/PRODUCT_BRIEF.md`, the roadmap's Done when lines for `readout-store`, `founder-requests`, `contract-terms` and `claim-support`, each feature's `03_prd.md`, and the progress and plan pages where a finding turns on them. The wave 1 review was the model for this file.
- Out of scope, but read where they touch shared files: `memo/`, `steering/`, `scans/redflags/cohorts.py`.

## Commands run, with results

Every scan and merge below ran with `TRICORDER_OUT_DIR`, `TRICORDER_STORE_DIR`, `TRICORDER_CACHE_DIR` and `TRICORDER_ROOMS_DIR` pointed into the scratch folder, `TRICORDER_OFFLINE=1`, and no `ANTHROPIC_API_KEY`.

| Command | Result |
|---|---|
| `python3 -m pytest` | 9 failed, 511 passed in 128 s. The 3 founder-requests failures are the known ones (the claims scan now reruns too). The 6 memo failures are out of scope, but their cause is in a shared file (S10). |
| `bin/ci-py` | `schema.export --check` passed. Then pytest gave the same result: 9 failed, 511 passed. |
| `python3 -m scans.redflags <room>` | hollis_voice 27 claims and 11 gaps; seed_drop 7 and 8; clean 27 and 11; brasswick 32 and 7 |
| `python3 -m scans.claims <room>` | hollis_voice 64 claims and 8 gaps; seed_drop 64 and 13; clean 64 and 8; brasswick 53 and 9 |
| `python3 -m scans.memo <room>` | Exit 0 in all four rooms. 0 unverified claims. `claim_support` ran as a merge step. |
| `python3 -m schema.check_quotes <room> redflags.json claims.json` | Every claim checked in all four rooms, and none failed |
| `python3 -m eval.score data_room/hollis_voice` | found 2 of 8 (PF2b, PF3); decoys flagged 0 of 3 |
| `python3 -m eval.score data_room/hollis_voice_seed_drop` | found 1 of 8 (PF2b); decoys flagged 0 of 3 |
| `python3 -m eval.score data_room/hollis_voice_clean` | found 0 of 0; decoys flagged 0 of 3. **But the readout holds two flags (B1).** |
| `python3 -m eval.score data_room/brasswick` | found 5 of 5; decoys flagged 0 of 3 |
| Partial rooms in the scratch folder: empty, deck only, contracts only | redflags, claims and memo all exit 0 with gaps |
| Broken inputs in the scratch folder: a hiring plan with other columns, text in a metrics cell, a malformed `claims.json`, a blank month in the customer file | Crashes. See S5 and O8. |
| `uvicorn server.app:app --port 8820` (pid 10732), probed with curl, then stopped by its pid | Bound to 127.0.0.1. Results are quoted under each finding. `ps` confirmed it stopped and that port 8820 was closed. |
| Search of the in-scope diff for U+2014 and U+2013 | None found |
| Search for `requests`, `socket`, `httpx`, `anthropic`, `smtplib` imports | None in product code. `read.py` reaches the model only through `clients/llm.py`, and only with a key set. |

### Security probes that passed

These are recorded so the next reviewer does not repeat them.

- **Store ids.** `demo/Hollis` and `demo/a%0A` give 422. `..%2F..%2Fetc` gives 404, because the router refuses the path.
- **Store files.** `files/..%2F..%2F..%2Fanswer_key.json` and `files/%2Fetc%2Fpasswd` give 404, because the path is only compared with the manifest. A held PDF gives 200 as `application/octet-stream`.
- **Store versions.** `readout?version=99` and `version=-1` give 404.
- **Store save.** `{"room": "../data_room/hollis_voice"}` and `{"room": "answer_key.json"}` give 404. A direct `FileStore.save` probe was also refused. It used a room symlink to a file outside the room, a `../secret.txt` source, an input of `/etc/passwd`, and a cache index entry of `../secret.txt`. All four were recorded as not copied and none was read.
- **Store delete.** A delete sent with a `text/plain` body is refused (422), so the JSON routes cannot be reached by a simple cross-site request.
- **Upload refusals.**
  - An upload to `data_room/brasswick` gives 409 with the copy command.
  - A hidden name gives 400, a control character gives 400, and an empty file gives 400.
  - `.exe` gives 415. A `.pdf` whose bytes are a zip gives 415. A CSV with a NUL byte gives 415.
  - An unknown request id gives 422, and so does a check-row id.
  - A 26 MB upload gives 413, both with a Content-Length and when chunked.
  - A second file with the same name gives 409.
  - A numbered folder that is a symlink out of the room gives 400 ("The room's folder is a link"), and nothing is written.
  - A room that is a symlink gives 404.
- **Upload file names.** `../../../etc/evil.csv` was saved as `04_contracts/pipeline_evil.csv`, inside the room. Nothing named `evil.csv` exists anywhere else on the disk.
- **Founder-facing text.** On all four rooms, a draft of every line has no leaks. Every numbered line starts "Please", "Send" or "If" and ends with a full stop. The default mailto link fits: 1,692 characters on Brasswick and 1,677 on Hollis Voice. The greeting and company come from the deck and the cover note.

## Findings, by severity

One blocker, ten should-fix items, nine optional items.

### Blocker

**B1. Contract terms: the clean room gets two false flags, and the claim text states something the script never checked.**

- **Where:**
  - `scans/redflags/contract_terms_full.py:110-114`. `counted()` takes the customer file's MRR for every product type except Onboarding.
  - `:306-311`. Check 1 says "the customer is counted as a year of ARR" from 12 times that MRR.
  - `:296-297`. The ARR build cell is only added as a source when a line is found. A missing line never stops the flag.
  - `:368-371`. Check 3 flags "the plan keeps its revenue" from the customer's share of the plan's starting figure. It never checks that the plan holds this customer.
- **Requirement:**
  - CT-R9 says to flag "when the customer is counted". The roadmap's 1.13 Done when wants the flag "beside the ARR row (`ARR_Build!E13`)".
  - PRODUCT_BRIEF and ARCHITECTURE say a claim says no more than its script checked.
  - The clean room is the control that proves Tricorder raises no false flags.
- **Observed:** on `hollis_voice_clean`, `redflags-020` is a `flag`: "Marlow Veterinary Group pilot agreement: either party may end it on 30 days notice ... but the customer is counted as a year of ARR: $180,000 (12 x $15,000 MRR in 2026-09)."
  - In the clean room the pilot is not counted. `monthly_metrics.csv` row 22 has MRR 171,739, not 186,739. ARR is 2,060,868. The ARR build has no Marlow line, and the claim cites no `ARR_Build` cell.
  - `redflags-021` is also a flag: "the plan keeps its revenue for 8 plan months after it ... at its 8.7% share of the plan's starting $171,739". That starting figure already leaves the pilot out.
  - Both flags reach the clean room's readout. `eval.score` reports "decoys flagged 0 of 3" only because the clean key has no decoy on that file.
- **Why the tests miss it:** `test_notice_check_on_hollis_flags_marlow_only` and `test_plan_check_flags_marlow_with_its_eight_plan_months` run only on the planted room. The clean room appears in `test_contract_terms_full.py` only in the quote-checker test (`CLEAN`, line 28).
- **Fix:**
  - Check 1: flag only when the counting side counts the customer as recurring. That means an ARR build line for the customer or its cohort (`arr_line_for`), or a metrics MRR that includes the customer's non-subscription rows. Otherwise write an info claim worded as what was checked, for example "the customer file lists $15,000 MRR for it; the ARR build does not count it".
  - Check 3: work out the plan share against a starting figure that includes the customer, or skip the check when the starting figure leaves the customer out.
  - Add a clean-room test asserting no flag or watch from `contract_terms_full`.

### Should fix

**S1. Founder requests: any website the operator visits can write files into a room and start scans (cross-site request forgery).**

- **Where:**
  - `server/founder_requests_routes.py:114` (`/files`) reads the raw body whatever its Content-Type.
  - `:125` (`/batch`) passes the raw body to `model_validate_json`, also without checking the Content-Type.
  - There is no Origin or Host check, and no token.
- **Requirement:**
  - FR-R16 to FR-R20 treat the upload as attack surface.
  - Under the guardrails, a claim must keep its source honest. A planted file becomes an input the readout cites.
- **Observed:** with `content-type: text/plain` and `Origin: http://evil.example`, both of these gave 200 and rebuilt the readout:
  - `POST /api/rooms/brasswick_live/founder-requests/files?name=pipeline.csv&answers=C36` saved `04_contracts/pipeline.csv`.
  - `/batch`, with a JSON body sent as `text/plain`, saved a reference list.
  - A browser sends both of these cross-site without a preflight.
  - A request with `Host: attacker.example:8820` was also served, so DNS rebinding reaches every route, including store file reads.
  - The store and draft routes are safe from the cross-site form. FastAPI refuses a JSON body sent as `text/plain` with 422.
- **Why the tests miss it:** the route tests send well-formed requests from the test client only.
- **Fix:**
  - Require `Content-Type: application/octet-stream` on `/files` and `application/json` on `/batch`. Either type forces a preflight, and with no CORS middleware the preflight fails.
  - Refuse a request whose `Origin` is not the page's own origin.
  - Add a Host allowlist (`127.0.0.1`, `localhost`) in `server/app.py`, for example with `TrustedHostMiddleware`.

**S2. Founder requests: an upload freezes the whole server while the scans rerun.**

- **Where:** `server/founder_requests_routes.py:114` and `:125` are `async def`. They call `ik.receive` and `ik.receive_batch` directly, and those run `subprocess.run(..., timeout=900)` for each waiting scan, then the merge (`founder_requests/intake.py:318-322`), all on the event loop.
- **Requirement:** ARCHITECTURE says "The page ... never waits on Python." The page, the store and the steering routes share this one server.
- **Observed:** during a 1.77 s hiring-plan upload, a `GET /health` sent 0.5 s in took 1.26 s. It waited for the upload to finish. With the model reading on, each rerun can take minutes and every other request waits.
- **Why the tests miss it:** the test client sends one request at a time.
- **Fix:** make the two routes plain `def` (FastAPI runs those in its thread pool) after reading the body, or wrap the call in `run_in_threadpool`. Read the body asynchronously, then hand off.

**S3. Founder requests: the receipt says "no number changed" when a scan crashed on the founder's file.**

- **Where:** `founder_requests/intake.py:350-390` (`changes`). It never reads `scans_rerun`. The readout is then rebuilt on the stale result the crashed scan left behind.
- **Requirement:** FR-R27 says the receipt says what changed in plain words. The failure-case row says that when a scan crashes, "the answer lists it as failed".
- **Observed:** a hiring plan with columns `role,start_month,salary` was added for C22 to `brasswick_live`.
  - `scans_rerun` holds `{"scan": "claims", "ok": false, ... KeyError: 'hire_id'}`.
  - The summary the operator reads is "Coverage now finds Hiring plan and future org. No check reads this file yet, so no number changed."
  - The claims scan does read the hiring plan. It crashed, and the readout kept the old claims.
- **Why the tests miss it:** the fixture hiring plan has the columns the claims reader expects.
- **Fix:** when any rerun fails, put a plain line first in `summary`, for example "One check could not read the new files, so its results are from before they arrived." Do not say "no number changed" in that case. Then fix S5.

**S4. Founder requests: the received-file log does not record the scans rerun.**

- **Where:** `founder_requests/intake.py:471`. Each log entry is the file entry plus `summary`. `scans_rerun` stays in the receipt only.
- **Requirement:** FR-R15 lists "when, the request, the original name, the saved path, its size and the scans rerun".
- **Observed:** the last entry in `out/brasswick_live/founder_requests.json` has the keys `answers, at, bytes, checklist_id, item, original_name, saved, summary`.
- **Why the tests miss it:** `test_hiring_plan_reply_reruns_and_rebuilds` (`test_intake.py:231-234`) asserts name, id, bytes and time only.
- **Fix:** add `"scans_rerun": reran` to each entry, and assert it in the test.

**S5. Claims scan: an ordinary file with other columns crashes the whole scan.**

- **Where:**
  - `scans/claims/evidence.py:306` and `:309` index `hire_id` and `headcount_after_hire`.
  - `:172`, `:201`, `:213` and `:241` call `float()` on a cell, which raises on text.
  - `_customers` (`:250` on) indexes `month` and `customer_id`.
  - `scans/claims/extract.py:304` indexes `c["value"]` in `claims.json`, and `:140` does the same in `_split_row`.
  - `label.label_all` calls every reader with no guard.
- **Requirement:**
  - CS-F6 says that when a named cell or column is missing, "the claim falls through ... Never a crash."
  - ARCHITECTURE "Failure" says a missing input is a gap.
  - Founder requests puts founder files into rooms under exactly these names (`CANONICAL` maps C22 to `hiring_plan`).
- **Observed:**
  - A deck plus `hiring_plan.csv` with `role,start_month` gives `claims exit 1: KeyError: 'hire_id'`.
  - With the hiring plan restored and `n/a` in the 2026-09 `mrr` cell, `metrics_mrr`, `metrics_revenue_ltm` and `metrics_grew` each raise `ValueError: could not convert string to float: 'n/a'`.
  - An unreadable deck beside `claims.json` holding `{"claims":[{"label":"ARR"}]}` gives `KeyError: 'value'`.
- **Why the tests miss it:** `test_inputs.py` covers missing files, not files with other columns or text cells.
- **Fix:** wrap each reader call in `label_all` so that an exception becomes an empty `Reading` with `missing` set to "a readable <document>", and the claim reads unsupported with a gap. Skip malformed `claims.json` rows. Add one test per case.

**S6. Claim support: a true pitch figure is relabelled "Contradicted" because a flag shares only a check name.**

- **Where:** `scans/memo/claim_support.py:127` (`settles(f, kind_name)`) and `:155-170` (`_contradict`). Any flag from a check in `CHECK_SETTLES` contradicts every claim of that kind. Values, periods and the subject are never compared.
- **Requirement:**
  - CS-R13 says to relabel when the flag "comes from a check that settles its kind".
  - The principle that a claim's text says no more than its script checked.
- **Observed:** a direct `apply()` probe used a supported claim, "largest customer share as at most 25%", and a `top_customer_share` flag, "The largest customer is 21.0% of MRR in 2026-09, over the 20% line". It produced severity `flag` with the text "Contradicted: The deck (slide 4) gives largest customer share as at most 25%, but the redflags scan's top_customer_share check flags it". The deck's ceiling is true.
  - On the demo rooms every relabel happened to be right: Hollis Voice NRR, and Brasswick BF1, BF2 and BF3. The rule is still not safe for a third room, or for a flag about another month or another customer.
- **Why the tests miss it:** `MEMO_CONTRADICTIONS` holds only cases where the flag does disprove the figure. No test has a flag that agrees with the claim's value.
- **Fix:** when the flag and the claim both carry a `Value` with the same unit, compare them, respecting the claim's bound, before contradicting. When they cannot be compared, use softer words, for example "the X check raises a problem with this figure: ...". Add the agreeing-flag case as a test.

**S7. Claim support: Hollis Voice's runway and burn read "supported" with no model-only note.**

- **Where:** `scans/memo/claim_support.py:113` and `:135-136`. `ran` counts any claim with a settling check name, including an info claim. The note is written only when every settling check has not run.
- **Requirement:**
  - CS-R14 says a row only the model backs names the rebuild check that would test it, while that check has not run.
  - `00_progress.md` item 2 says the 37 months of runway and the $374,462 burn have an ask column that "says so".
- **Observed:** on Hollis Voice, `claims-031` (runway 37) and `claims-032` (burn $374,462) are `supported`. Their ask columns are empty.
  - `payroll_from_hiring_plan_and_rerun_cash`, the check for planted PF4, has not run.
  - `contractor_spend_vs_headcount_and_burn` counts as run, because mislabels wrote an info claim under that name: "Ledger lines tie to P&L ...".
- **Why the tests miss it:** `test_model_only_support_is_said_out_loud` checks gross margin only. That kind has one settling check.
- **Fix:** write the note when no settling check has flagged and at least one has not run, and name the checks that have not run. Assert it for the runway and burn rows.

**S8. Claims scan: computed evidence cites one unrelated row, and the text does not say how the figure was made.**

- **Where:** `scans/claims/evidence.py:268-293`. A sum, a count or a share cites only the top row or the last row. `label._ev_words` (`:165`) and the claim texts (`label.py:243-249`) never use `Evidence.how`, although every reader fills it in.
- **Requirement:**
  - PRODUCT_BRIEF says every claim links to its source, a person can open it, and the number is two clicks away.
  - This is the same defect class as wave 1 S7 and U4.
- **Observed:**
  - Hollis `claims-004` says "revenue by customer (row 1984) says 2,060,868". Row 1984 is Cedar & Pine at $3,600. The figure is 12 times the sum of every 2026-09 subscription row.
  - Brasswick `claims-010` says "customers ever as 15 brokers ... revenue by customer (row 141, 15) agrees". Row 141 is one Ostley Freight row.
  - Brasswick `claims-014` cites the same row for 75,337 invoices.
- **Why the tests miss it:** the quote checker only confirms that the cited row's text is in the file, and it is.
- **Fix:** put `how` into the evidence words, for example "revenue by customer (sum of column mrr for 2026-09, rows 1915 to 2133, times 12): 2,060,868". Cite the first and last row of the range, as `_metrics_ltm` does.

**S9. Store: delete removes another fund's outside data, and deletes for a company that was never stored.**

- **Where:** `store/files.py:129` (`cache/outside/<company>`, keyed by company alone) and `:335-351` (`delete_company`). The route checks only the company id and the confirm text.
- **Requirement:** STORE-R7 says "Other companies, other funds and shared cache entries stay" and "Deleting a company with nothing held removes nothing and says so".
- **Observed:**
  - `POST /api/store/zzz/other/delete {"confirm":"other"}` returned `versions: 0, cache_files: 1, index_entries: 1`. It removed `cache/outside/other/` and its index entry. Fund `zzz` has never held anything.
  - The same happened for `demo/brasswick`, which was never saved.
  - On the laptop, the outside-in scans write `cache/outside/hollis_voice/`. Any fund's delete of that id wipes the offline cache the demo runs on.
- **Why the tests miss it:** the tests delete a company that the same fund saved.
- **Fix:** remove `cache/outside/<company>` only when the fund holds a version of the company, and no other fund holds the company. Otherwise leave it, and list it in `left` or `also_on_this_laptop` with the reason. This is Ken's call against the PRD's Questions entry on the cache key. The default should at least not cross funds.

**S10. Shared file: claim ids move when a module is added to `scans/redflags/scan.py`.**

- **Where:** `scans/redflags/scan.py:18-32` and `scans.base.Ids`. Ids are numbered in the order of `CHECKS`. `contract_terms_full` and `cohorts` were inserted ahead of `deck_vs_books`.
- **Requirement:** memo edits and steering revisions refer to claims by id. So does the store's version history, which compares readouts across versions.
- **Observed:**
  - The deck-against-P&L claim moved from `redflags-007` to `redflags-024` on Hollis Voice.
  - 6 memo tests fail on this branch for that reason, for example `memo/edit.py:73 EditError: no line 's07-redflags-007' in section 7` and `test_build.py:42 assert where["redflags-007"] == 7`.
  - An operator's memo edit made before this merge would be lost the same way on a rebuild.
- **Why the tests miss it:** each feature's tests run on its own branch.
- **Fix:** this is the captain's call. Either give each module its own id prefix (`redflags-ctf-001`), or derive the id from the check name and the claim's first source, so it stays the same across builds. At least, append new modules to the end of `CHECKS` until then.

### Optional

- **O1. Claim support: `corroborated_by` never fires.** No room sets it, and no test covers it (`grep corroborat scans/memo/tests/test_claim_support.py` finds nothing). CS-R13's second clause is unverified. The likely reason is that every other scan's claim carries `label="other"` or a period the claims scan does not use.
- **O2. Rooms folder.** `founder_requests/intake.py:83` reads `TRICORDER_ROOMS_DIR`, but `server/app.py:30` (`ROOM_PARENTS`) does not. In a verification run, a copied room is visible to founder requests but missing from `/api/rooms`. The store's save route uses the same list, so it cannot see the room either. Observed: `brasswick_live` was not in `/api/rooms`. Point `ROOM_PARENTS` at `rooms_root()`.
- **O3. Page.** After a reply is added to a working copy, the panel reloads the synthetic room's lines (`FounderRequests.tsx:198`). `App.tsx:146` passes no `onRebuilt`. The page keeps showing the unchanged synthetic readout. The receipt is right, and the page should switch to the copy.
- **O4. Duplicate count row.** `_recount` (`claim_support.py:185`) appends "relabelled by the memo step" each time it runs. The tests now run the merge (which runs the step) and then the command, so the row appears twice. The test reads it through a dict, so it passes.
- **O5. Loose matches.**
  - `bios_years` supports a claim from any "N years" anywhere in any bio.
  - `_contract_date` supports it from any date that starts with the month, on any page that names the customer (`evidence.py:367-384`, `:469`).
  - The text is true about what matched. A reader may take it as more than it is.
- **O6. Name length.** `target_for` (`intake.py`, `name_from_founder_stem`) allows up to 100 characters, but FR-R17 says 80.
- **O7. Room copy follows links.** `copy_room` uses `shutil.copytree(src, dest)`, which copies the target of any symlink in the source room. Pass `symlinks=True`, or refuse rooms that hold links.
- **O8. Crashes outside this scope, found on the same probes.**
  - `scans/redflags/cohorts.py:41` raises `ValueError` on a customer row with a blank month, and that kills the red-flag scan. `contract_terms_full` alone handles the same file.
  - A deck that is not a PDF crashes `deck_vs_books.py:256` and `scans/base.py:102` (`synthetic_notice`) in the merge.
  - `scans/redflags/scan.py:51` calls each module with no guard, so one module's crash loses every module's claims.
- **O9. No network test.** FR-R10 ("No route or command opens a network connection") has no test. The plan maps it to `test_mailto_encoding`.

## Verdicts by feature

| Feature | Code quality | Completion against the Plan and Done when |
|---|---|---|
| Readout store (.01) | **Pass**, with S9 to fix. The path handling is the strongest in the diff: ids by fullmatch, files only by manifest, resolve-and-contain on save, atomic versions. | **Pass** on all three Done when lines (Hollis Voice stored, listed and deleted on the live server). STORE-R7 **fails** narrowly on other funds (S9). |
| Founder requests (.02) | **Fail** until S1 and S2 are fixed. Name cleaning, the kind allowlist, byte checks, exclusive no-follow writes and size limits all held under probing. | Drafting (FR-R1 to R10, R22 to R26) verified on four rooms. Receiving **fails** FR-R15 (S4) and FR-R27 and its failure-case row (S3). The Done when is met on Brasswick. The 3 failing tests are known. |
| Contract terms (.04) | **Pass** on structure. Every quote is confirmed before use, and the cell-level guard per check is good. | **Fail** on CT-R9 and CT-R3 in the clean room (B1). The Hollis Voice Done when lines pass: Marlow flagged with 8 plan months, Cedar & Pine and Brookline Row cleared, clause fields read as not stated, the change-of-control test contract. |
| Claim support (.06) | **Fail** until S5 and S6 are fixed. | Every figure is labelled and the quote checker passes in all four rooms. The planted contradictions that the progress page names are contradicted. **Fails** CS-F6 (S5) and CS-R14 (S7). CS-R13 corroboration is unverified (O1). The source wording falls short of the principle (S8). |

## To delete at cleanup

- The worktree `/home/claude/wt/review` and its branch `review/wave2a`. This review file is the only change in it, and it is uncommitted.
- Ignored files in that worktree from the test run: `.pytest_cache/`, the `__pycache__/` folders, and any `out/` the pytest run wrote.
- Scratch files (under `/tmp`, so the OS owns them): `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/review/`. That includes the probe rooms, `out/`, `store/`, `store2/`, `cache/`, `cache2/`, `roomsdir/` (with `brasswick_live`, a `06_legal` symlink and an `hv_link` symlink), `outside_target/`, `big.csv`, and the server and pytest logs.
