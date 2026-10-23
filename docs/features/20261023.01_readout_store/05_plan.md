# Plan: readout store and delete

PRD: [03_prd.md](03_prd.md). Architecture: [04_architecture.md](04_architecture.md).

## Builder's reading list

[ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md) ("The stack", "Folder layout"), the readout-store and outside-in slices in [ROADMAP.md](../../ongoing/ROADMAP.md), `schema/claim.py` (`Readout`, `ScanResult`, `Source`), `scans/base.py` (`out_dir`), `server/app.py` (`room_dir`).

## Slices

1. **Disk store.** `store/base.py`, `store/models.py`, `store/files.py`, `store/tests/test_store.py`; `.gitignore` line `store_data/`; `store` in `testpaths`. Built test first (commit 4a43838).
2. **CLI and routes.** `store/cli.py`, `store/__main__.py`, `server/store_routes.py`, one include in `server/app.py`, `store/tests/test_cli.py`, `server/tests/test_store_routes.py`; `.env.example` gains the two variables. Built test first (commit 4828abf).
3. **Verification map and drive.** `.claude/skills/verify-tricorder/features/readout-store.md`, one index line, evidence in [evidence/](evidence/), note in [06_verification.md](06_verification.md).
4. **Later, not in this branch.** A store panel on the readout page (list and delete), and callers in steering, founder requests, the memo and contract terms.

## Throughput checkpoint

One owner. The only shared files are `server/app.py` (two lines), `pyproject.toml` (one word), `.gitignore` and `.env.example` (appended lines). No prerequisite is blocked.

## Verification

Test command for every row: `python3 -m pytest store server/tests/test_store_routes.py` (2026-10-23: 52 passed after the S9 fix). Full suite: `python3 -m pytest`, 234 passed, 18 skipped.

| Requirement | Acceptance/failure case | Command/observation | Owner | Evidence/status |
|---|---|---|---|---|
| Done when 1 | A stored Hollis Voice readout comes back with its sources and files. | `test_saved_readout_comes_back_with_sources_and_files`; drive: `GET /api/store/demo/hollis_voice/readout`, `GET .../files/02_financials/expense_ledger.csv` | builder | Pass. Drive: 10 claims with sources, 16 inputs, the ledger's bytes equal the room file (`evidence/api_20261023T015225Z_3811_19598.json`, `api_20261023T015215Z_3719_20601.json`). |
| Done when 2 | The list for the company shows everything held. | `test_the_list_for_a_company_shows_everything_held`; drive: `GET /api/store/demo/hollis_voice` | builder | Pass. 1 version, 16 files by room path, `redflags`, 1 cache file, 510165 bytes (`evidence/api_20261023T015225Z_3795_11123.json`). |
| Done when 3 | One delete leaves nothing for that company in the store or in `cache/`. | `test_one_delete_leaves_nothing_for_that_company`; drive: `POST .../delete` then `GET` and `find` | builder | Pass. `"left": []`, then an empty listing; `find` shows only the shared `signals/` page (`evidence/api_20261023T015233Z_3839_18855.json`, `api_20261023T015233Z_3853_10733.json`, `cli_20261023T015233Z_3867_1012.txt`). |
| STORE-R1 | Save stores readout, results and files as a version. | `test_saved_readout_comes_back_with_sources_and_files` | builder | Pass. |
| STORE-R2 | Only files read are stored; a source outside the room is never read; URL sources come from their cache copy. | `test_only_the_files_it_read_are_stored`, `test_a_source_outside_the_room_is_never_read`, `test_a_url_source_is_copied_from_its_cache_copy` | builder | Pass. Drive: 16 of the room's 17 files stored; `06_product/product_one_pager.pdf` is not, because nothing read it. |
| STORE-R3 | Same readout twice is one version; a change is a new one; all kept; A, B, A is three. | `test_saving_the_same_readout_twice_adds_no_version`, `test_a_changed_readout_is_a_new_version_and_every_version_is_kept` | builder | Pass. Drive: second save `"new": false` (`cli_20261023T015204Z_3644_26410.txt`). |
| STORE-R4 | Get latest or named; unknown is not held; files only by manifest path. | `test_get_an_unknown_company_or_version_is_not_held`, `test_read_file_serves_only_the_manifest` | builder | Pass. |
| STORE-R5 | Listing names files by room path with versions; total bytes equal the disk. | `test_the_list_for_a_company_shows_everything_held` | builder | Pass. |
| STORE-R6 | 13 bad ids refused in every call, nothing created. | `test_a_bad_fund_or_company_id_is_refused_before_any_path`; CLI `test_a_bad_id_exits_2`; route `test_bad_ids_and_paths_are_refused` | builder | Pass. Drive: `a.b` is 422, `Hollis_Voice` exits 2. |
| STORE-R7 | Delete removes the store folder; removes the cache folder and index entries only when this fund held the company and no other fund does; a fund that never stored it removes nothing (review S9); others stay; symlinked folder refused. | `test_one_delete_leaves_nothing_for_that_company`, `test_a_fund_that_never_stored_the_company_removes_nothing`, `test_the_cache_stays_while_another_fund_still_holds_the_company`, `test_deleting_a_company_with_nothing_held_removes_nothing`, `test_delete_refuses_a_symlinked_company_folder`, `test_delete_names_out_folders_it_leaves_alone`; route `test_a_delete_under_a_fund_that_never_stored_the_company_touches_no_cache` | builder | Pass after the S9 fix, 2026-10-23: the three new tests failed first (`KeyError`/attribute errors on `nothing_held` and `kept`), then 52 passed. |
| STORE-R8 | CLI asks; a wrong answer removes nothing; `--yes` skips; route needs `confirm`. | `test_save_list_get_delete_from_the_terminal`, `test_delete_with_yes_needs_no_answer`, `test_save_list_get_and_delete_through_the_routes` | builder | Pass. Drive: `echo no` exits 1 (`cli_20261023T015216Z_3780_10708.txt`); wrong confirm is 400 (`api_20261023T015216Z_3765_28554.json`). |
| STORE-R9 | Env vars and defaults; `store_data/` ignored by git. | `test_open_store_reads_the_environment`, `test_store_data_is_ignored_by_git` | builder | Pass. |
| STORE-R10 | Nothing written in `out/` or the room. | `test_the_store_writes_nothing_in_out_or_the_room` | builder | Pass. |
| STORE-R11 | A half-written version is ignored. | `test_a_half_written_version_is_ignored` | builder | Pass. Concurrent saves are not tested. |
| STORE-R12 | `open_store()` returns the configured store behind the protocol. | `test_open_store_reads_the_environment` | builder | Pass. No second implementation exists to swap in. |
| STORE-R13 | CLI commands and exit codes. | `store/tests/test_cli.py` (runs `python -m store` as a subprocess) | builder | Pass. |
| STORE-R14 | Routes, 404s for unknown room or no readout. | `server/tests/test_store_routes.py` | builder | Pass. |
