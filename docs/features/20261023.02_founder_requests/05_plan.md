# Plan: requests to the founder

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). Progress: [00_progress.md](00_progress.md).

## Slices

1. **Guidance and draft.** `founder_requests/guidance.py`, `draft.py`, tests in `founder_requests/tests/test_guidance.py` and `test_draft.py`. Began as the prototype spike; its tests were written after the spike, then the module was changed test-first (FR-R6 leaks, FR-R7 sentences).
2. **Intake.** `founder_requests/intake.py` and `test_intake.py`, test-first: names, kinds, sizes, paths, folders, canonical names, the waiting-scan rule, the rerun and merge.
3. **CLI and routes.** `founder_requests/__main__.py`, `server/founder_requests_routes.py`, `test_cli.py` and `server/tests/test_founder_requests_routes.py`, test-first through the real command and the real endpoints.
4. **Panel.** `readout/src/FounderRequests.tsx`, type check and build through `bin/ci-web`, screenshots in light and dark.
5. **Fix round after the independent persona review (2026-10-23).** Test-first: the draft rules (FR-R22 to FR-R26) in `test_draft.py`, then the batch intake and receipt (FR-R27, FR-R28) in `test_intake.py`, `test_cli.py` and the route tests, then the panel.

## Throughput checkpoint

One owner. The slices share one package and build on each other; the only shared files are one line each in `server/app.py` and `pyproject.toml`. No blocking prerequisite: checklist coverage is merged.

## Verification

| Requirement | Acceptance or failure case | Command or observation | Owner | Evidence or status |
|---|---|---|---|---|
| FR-R1, FR-R2 | Brasswick lists 32 lines; default is the top five | `test_draft.py::test_brasswick_lines_and_default` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R3 | Every checklist guide has guidance; each entry's sections exist in its guide | `test_guidance.py` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R4, FR-R5 | Shared guide grouped once; optional lines after required | `test_draft.py::test_grouping_and_optional_section` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R6, FR-R7 | No leak on any line of Brasswick or Hollis Voice; full sentences | `test_draft.py::test_no_internal_reference_reaches_the_founder` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R8 | "Hi Celia," and "Brasswick" read from the room | `test_draft.py::test_greeting_and_company_from_the_room` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R9, FR-R10 | mailto encodes CRLF and %20; length flag | `test_draft.py::test_mailto_encoding` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R11 to FR-R15 | Hiring plan reply on a Brasswick copy reruns redflags and C22 goes missing to found | `test_intake.py::test_hiring_plan_reply_reruns_and_rebuilds` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R16 to FR-R20 | Synthetic room refused; bad names, kinds, sizes, links, overwrite refused | `test_intake.py`, `server/tests/test_founder_requests_routes.py` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R21 | Panel renders, drafts, adds a file | `bin/ci-web`; screenshots in `evidence/` | builder | Pass, 2026-10-23, [06_verification.md](06_verification.md) |
| FR-R22, FR-R23 | No line asks for a held file; families merge; SOW named | `test_draft.py::test_never_ask_for_a_file_the_room_holds`, `test_lines_for_the_same_papers_become_one`, `test_a_document_the_room_holds_by_name_is_not_asked`, `test_a_merged_item_lists_each_request_a_reply_can_answer` | builder | Pass, 2026-10-23, fix round |
| FR-R24, FR-R25 | Closing paperwork after the term sheet at seed; top five by piece weight and flags | `test_draft.py::test_top_five_puts_what_settles_the_decision_first`, `test_closing_paperwork_waits_for_the_term_sheet_at_seed` | builder | Pass, 2026-10-23, fix round |
| FR-R26 | Short email, date, sign-off, fits a mail link | `test_draft.py::test_the_email_is_short_and_warm`, `test_one_item_and_the_default_date`, `test_operator_view_has_no_check_codes`; route and CLI tests | builder | Pass, 2026-10-23, fix round |
| FR-R27, FR-R28 | Plain-words receipt; several files, one rerun; one bad file writes nothing | `test_intake.py::test_changes_are_said_in_plain_words`, `test_several_files_in_one_add_rerun_once`, `test_a_batch_with_one_bad_file_writes_nothing`; `test_add_several_files_each_with_its_requests`; `test_several_files_in_one_add` | builder | Pass, 2026-10-23, fix round |
| Done when | Brasswick request with guidance; copy and mailto; reply starts waiting scans | the verify-tricorder recipe, driven once | builder | Pass, [06_verification.md](06_verification.md), `evidence/` |

## Testing findings and dispositions

Recorded in [06_verification.md](06_verification.md).

## Rollout and final verification

`python3 -m pytest` and `bin/ci-py` must end with 0 failed; `bin/ci-web` must exit 0. Release authority is the orchestrator's: this branch is not pushed by the builder.
