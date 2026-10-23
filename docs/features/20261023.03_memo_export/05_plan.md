# Plan: the memo and its PDF

PRD: [03_prd.md](03_prd.md). Architecture: [04_architecture.md](04_architecture.md). UI baseline: [02_prototype_decision.md](02_prototype_decision.md).

## Throughput checkpoint

- Blocking prerequisites: none. The readout exists on main (red-flag scan, coverage, asks).
- Independent workstreams: none worth splitting. The builder, both renderers and the edits share one data shape; one owner.
- Shared writable state: `server/app.py` (one import and one include line, placed before the page mount), `requirements.txt` (reportlab), `pyproject.toml` (`memo` in testpaths), `.claude/skills/verify-tricorder/features/` (one file, one index line). Everything else is in `memo/`, `server/memo_routes.py` and this folder.

## Slices

| # | Slice | Outcome | State |
|---|---|---|---|
| 1 | Data shape, template table, builder | A `Memo` with 16 sections from any readout | Done, commit 312cebe |
| 2 | Edits, versions, store | Numbered versions, operator lines marked, rebuild keeps them | Done, 312cebe and 8ab2ea2 |
| 3 | Page and PDF | Offline page with two-click drill-down; PDF with section notes | Done, 312cebe, fe82a25, 8ab2ea2 |
| 4 | CLI and routes | `python -m memo`, `/api/rooms/{room}/memo*` | Done, 312cebe |
| 5 | Verification map and drive | `features/memo-export.md`, evidence | Done, 8ab2ea2; evidence in `evidence/` |

## Verification table

Inspected revision: 8ab2ea2 (branch `forge/memo-export`).

| Requirement | Acceptance or failure case | Command or observation | Owner | Evidence and status |
|---|---|---|---|---|
| ME-R1 | CLI writes version, page, PDF and a summary; refuses with no readout | `test_cli_writes_the_draft_the_page_and_the_pdf`, `test_cli_refuses_without_a_readout_or_with_a_bad_edit`; `control.sh cli python3 -m memo data_room/hollis_voice` | builder | Pass. `evidence/cli_*.txt` |
| ME-R2 | 16 sections in order | `test_sixteen_sections_in_the_template_order`; API read-back | builder | Pass |
| ME-R3 | Routing piece, label, entry, folder | `test_hollis_voice_claims_land_in_their_sections`, `test_routing_prefers_the_piece` | builder | Pass |
| ME-R4 | Every section filled or names its gap | `test_every_section_is_filled_or_names_its_gap`, `test_a_bare_readout_still_builds`; CLI `sections_empty` | builder | Pass. 7 sections empty on Hollis Voice, each with its gap text |
| ME-R5 | Openers and coverage closers | `test_sections_close_with_their_coverage`, `test_with_pieces_and_flags_the_summary_and_openers_fill` | builder | Pass (pieces simulated in the test, labelled) |
| ME-R6, ME-R7 | Summary and risks | `test_flags_open_the_summary_in_full_once_and_are_referred_to_elsewhere` | builder | Pass |
| ME-R8 | Section 14 and 16 | `test_section_14_holds_coverage_the_ask_list_and_the_box`, `test_section_16_lists_every_cited_source_once` | builder | Pass |
| ME-R9, ME-R19 | Operator's sections and banned words | `test_operator_sections_stay_the_operators`; `test_the_page_needs_no_network` (no dashes) | builder | Pass |
| ME-R10 | Quote check on export | `test_a_claim_that_fails_the_quote_checker_moves_to_the_box`, `test_every_claim_in_the_page_passes_the_quote_checker`; `evidence/pdf_check.txt` | builder | Pass. 0 could not verify on Hollis Voice |
| ME-R11 | Offline page | `test_the_page_needs_no_network`; the drive opens the page from a file and from the server | builder | Pass |
| ME-R12, ME-R13 | One click to claims, two to sources and agree/disagree | `spike/drive_memo.js` in Chromium on the served page | builder | Pass. `evidence/memo_drive.json`: 113 of 113 lines opened in one click; 40 of 40 claims opened their sources in the second, quote marked |
| ME-R14 | PDF footnotes | `test_every_claim_in_the_pdf_has_a_note_naming_its_file_and_locator`; `evidence/pdf_check.txt` | builder | Pass. 10 of 10 claims footnoted in v1 and v3; every source named |
| ME-R15, ME-R16 | Versions, operator marking | `memo/tests/test_edit.py`; `control.sh api POST .../memo/edits`; `spike/edit_in_page.js` | builder | Pass. `evidence/edit_in_page.json`, `memo_operator_line_*.png` |
| ME-R17 | Rebuild keeps operator lines | `test_a_rebuild_keeps_the_operators_lines`, `test_cli_takes_a_readout_json_and_a_second_run_makes_version_2` | builder | Pass |
| ME-R18 | Routes, 409 on stale, 400 on bad edit | `test_server_routes_build_edit_and_serve`; drive: HTTP 200 then 409 | builder | Pass |
| ME-R20 to ME-R22 | Partner view, first screen, one-line sections, flags once | `test_the_partner_view_holds_no_plumbing`, `test_a_section_with_nothing_in_it_is_one_line`, `test_flags_open_the_summary_in_full_once_and_are_referred_to_elsewhere`, `test_not_assessed_is_said_once_and_no_gap_repeats_in_a_section`; drive: `partner_plumbing`, `partner_first_screen` | builder | Pass. `evidence/fix_round/memo_drive.json` |
| ME-R23, ME-R24 | Recommendation first; partner PDF | `test_the_recommendation_opens_the_summary`, `test_cli_applies_an_edit_file`, `test_the_pdf_is_for_partners`, `test_sources_are_read_and_read_as_a_partner_reads_them` | builder | Pass. `evidence/fix_round/pdf_check.txt` |
| ME-R25 | ARR side by side from claims only | `test_the_arr_figures_sit_side_by_side_from_claims_only` | builder | Pass |
| ME-R26 | One save, 409 reapply, detach on a new figure | `test_many_changes_make_one_version`, `test_a_claim_line_rewritten_with_a_new_figure_is_the_operators`, `test_server_routes_build_edit_and_serve`; `spike/edit_in_page.js` | builder | Pass. `evidence/fix_round/edit_in_page.json`, `memo_edit_*.png` |
| ME-R27 | Many claims in few lines | `test_the_pitch_claims_read_as_one_line_per_section` | builder | Pass. 91 claims, 88 partner lines |
| ME-R28 | Steer's replaced claim as the before | `test_a_claim_the_steer_replaced_is_the_new_lines_before` | builder | Pass (unit only; no steered room in the drive) |
| ME-R29 | Tests robust to new checks | every memo test finds claims with `by_check` or severity | builder | Pass after three integration merges (cohorts, claim support, per-module ids) |
| All | Full suite and CI gate | `python3 -m pytest`; `bin/ci-py` | builder | 236 passed, 0 failed, 0 skipped at 60ce3a8 (earlier runs: 218 passed, 18 deck tests skipped while matplotlib was missing) |
| Independent review | Not done | the orchestrator's checkpoint review | orchestrator | Unverified |
