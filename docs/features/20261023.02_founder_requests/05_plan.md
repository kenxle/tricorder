# Plan: requests to the founder

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). Progress: [00_progress.md](00_progress.md).

## Slices

1. **Guidance and draft.** `founder_requests/guidance.py`, `draft.py`, tests in `founder_requests/tests/test_guidance.py` and `test_draft.py`. Began as the prototype spike; its tests were written after the spike, then the module was changed test-first (FR-R6 leaks, FR-R7 sentences).
2. **Intake.** `founder_requests/intake.py` and `test_intake.py`, test-first: names, kinds, sizes, paths, folders, canonical names, the waiting-scan rule, the rerun and merge.
3. **CLI and routes.** `founder_requests/__main__.py`, `server/founder_requests_routes.py`, `test_cli.py` and `server/tests/test_founder_requests_routes.py`, test-first through the real command and the real endpoints.
4. **Panel.** `readout/src/FounderRequests.tsx`, type check and build through `bin/ci-web`, screenshots in light and dark.

## Throughput checkpoint

One owner. The slices share one package and build on each other; the only shared files are one line each in `server/app.py` and `pyproject.toml`. No blocking prerequisite: checklist coverage is merged.

## Verification

| Requirement | Acceptance or failure case | Command or observation | Owner | Evidence or status |
|---|---|---|---|---|
| FR-R1, FR-R2 | Brasswick lists 32 lines; default is the top five | `test_draft.py::test_brasswick_lines_and_default` | builder | see 06_verification.md |
| FR-R3 | Every checklist guide has guidance; each entry's sections exist in its guide | `test_guidance.py` | builder | see 06_verification.md |
| FR-R4, FR-R5 | Shared guide grouped once; optional lines after required | `test_draft.py::test_grouping_and_optional_section` | builder | see 06_verification.md |
| FR-R6, FR-R7 | No leak on any line of Brasswick or Hollis Voice; full sentences | `test_draft.py::test_no_internal_reference_reaches_the_founder` | builder | see 06_verification.md |
| FR-R8 | "Hi Celia," and "Brasswick" read from the room | `test_draft.py::test_greeting_and_company_from_the_room` | builder | see 06_verification.md |
| FR-R9, FR-R10 | mailto encodes CRLF and %20; length flag | `test_draft.py::test_mailto_encoding` | builder | see 06_verification.md |
| FR-R11 to FR-R15 | Hiring plan reply on a Brasswick copy reruns redflags and C22 goes missing to found | `test_intake.py::test_hiring_plan_reply_reruns_and_rebuilds` | builder | see 06_verification.md |
| FR-R16 to FR-R20 | Synthetic room refused; bad names, kinds, sizes, links, overwrite refused | `test_intake.py`, `server/tests/test_founder_requests_routes.py` | builder | see 06_verification.md |
| FR-R21 | Panel renders, drafts, adds a file | `bin/ci-web`; screenshots in `evidence/` | builder | see 06_verification.md |
| Done when | Brasswick request with guidance; copy and mailto; reply starts waiting scans | the verify-tricorder recipe, driven once | builder | `evidence/` |

## Testing findings and dispositions

Recorded in [06_verification.md](06_verification.md).

## Rollout and final verification

`python3 -m pytest` and `bin/ci-py` must end with 0 failed; `bin/ci-web` must exit 0. Release authority is the orchestrator's: this branch is not pushed by the builder.
