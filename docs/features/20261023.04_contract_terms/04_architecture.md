# Architecture: contract-terms

Requirements are in the [PRD](03_prd.md). Acceptance is in the [Plan](05_plan.md#verification).

## Summary

Two modules in `scans/redflags/`:

- `contract_reader.py`: the one contract reader for entry 1.13. It finds the contracts in a folder, reads each one into a `ContractTerms` record in the shape of entry 1.13's "contracts" item, confirms every quote with the quote checker, and caches the reading per folder. It writes no claims.
- `contract_terms_full.py`: `check(room, ids) -> (claims, gaps, panels)`. Checks 1, 3, 4 and 6, the clause notes, and two Panels ("contract terms", "contract checks"). Listed in `scan.CHECKS` as `contract_terms_full`, one line under Saturday's `contract_terms`.

Tests: `scans/redflags/tests/test_contract_terms_full.py`, with test contracts written by `tests/contract_fixtures.py` (a small PDF writer with no dependency, so the tests never skip).

## Inputs, read through `schema/readers.py`

| Input | Read with | Used for |
|---|---|---|
| Every contract PDF | `pdf_pages` | the terms, clauses and quotes |
| `03_metrics/customer_mrr_by_month.csv` (or Brasswick's `revenue_by_customer.csv`, column `subscription_revenue`) | `csv_rows`, `csv_row_text` | counted MRR by customer and month, first MRR month |
| `02_financials/financial_model.xlsx` `Assumptions` | `xlsx_sheet` | the data date (as-of), the plan's starting figure, any non-renewal rate |
| `P&L` | `xlsx_sheet` | the plan columns of "Recurring revenue (subscription plus pilot)", else "Subscription revenue" |
| `ARR_Build` | `xlsx_sheet` | the counted lines and their customer counts (check 6), the cohort line a customer sits in (check 1's source) |
| `03_metrics/monthly_metrics.csv` | `csv_rows` | the as-of MRR for the coverage share |
| Settings | `schema.settings.load()` | `short_notice_days`, `min_contract_months`, `match_tolerance` |

## The reader: script now, model on Saturday

Decision: the reading is a script that locates each term by its heading and wording in the PDF text. Why:

- There is no model key in this container, so a model path could be tested only on hand-built responses, never end to end.
- The script reading is deterministic and offline, and its quotes are exact spans of the page text, so the quote checker always finds them.
- Saturday's slice is the model reading with entry 1.13's prompt. Building it here would take Saturday's work and leave two prompts to keep in step.

What the script reads: parties and counterparty role, effective date, term and dates, auto-renewal with its notice and length, a right to end for any reason with its notice, a breach cure period, "has no other right to end", pilot or trial wording and any duty to convert, fee lines (monthly, annual, total, with their from and until dates, and an amendment's new fee from the amendment's date), discount and list price, payment terms, one-time fee, the three clause fields, the other pay-or-leave clauses, and amendments. Patterns are in `contract_reader.read_contract`. A contract whose wording the patterns miss returns `not_stated` for that term, which is honest but may under-read a real room; that is the risk the model reading covers.

The "not stated" result cites every page of the contract, quoting each page's first line, so the reader can open each page the script searched. The claim says the script read all pages for the wording; it does not claim more.

## The seam with Saturday's module

```
contract_reader.read_room(room) -> RoomContracts(contracts: list[ContractTerms], gaps, read_by)
contract_reader.set_model_reader(fn)      # fn(room, paths) -> list[ContractTerms]
TRICORDER_CONTRACT_READER=script          # forces the script reading even when a model reader is set
```

- Saturday's `contract_terms.py` calls `set_model_reader` at import with a function that calls `clients.llm.read` with entry 1.13's prompt and returns `ContractTerms` (its "contracts" items map field for field; `title`, `counterparty`, `pages` and `page_heads` are ours and can be filled from `pdf_pages`). `scan.CHECKS` lists `contract_terms` before `contract_terms_full`, so the reader is set before either module reads.
- Both modules call `read_room`. The first call reads; the second gets the cached reading. A test proves three contracts are read three times in all, not six.
- If the model reader raises (no key, a refusal), `read_room` writes the gap "Not in the room: a model reading of the contracts" with the reason and falls back to the script reading. The scan never crashes for want of a key.
- Each term's quote is confirmed by `schema.check_quotes.source_holds_quote` at its page in `_confirm`, whichever reader produced it.

### Check 1 is here

The roadmap's Done when for this slice includes "a test contract with a 30-day cancellation counted as a year of ARR produces a gap; the same contract with a one-year commitment does not". That is check 1. So `contract_terms_full.check_1` writes `cancellable_within_notice_vs_arr`, and Saturday's module must write only checks 2 and 5. If the team prefers check 1 in Saturday's module, it moves by deleting one line from `check()`'s loop and importing `check_1` there.

## Outputs

- Claims, all `check.kind` "script", severity set by the script, confidence `computed` (arithmetic, or the "not stated" reading) or `quoted` (a clause shown as written). Amounts use `value.label` "other", as entry 1.13 says. Check names: the entry's names, plus `clause_notes` for the clauses (checklist row C172's check name).
- Gaps with `piece` set: "customers" for missing contracts, "traction_and_revenue" for missing counting files.
- Panels: "contract terms" (contract, field, status, value, page, quote) and "contract checks" (contract, label, check, result, reason).

## Alternatives considered

- **Model reading now, tested on hand-built responses.** Rejected for the reasons above; the seam keeps it one function away.
- **One module for all of entry 1.13.** Rejected: Saturday's team owns `contract_terms.py`, and two builders in one file the same day conflict.
- **Gaps per customer for check 6.** FRAMEWORKS asks for one per `ARR_Build` line; per customer would be 210 lines on Hollis Voice. Kept per line, with a per-customer list only when there is no ARR build.

## Proposed schema changes

None needed. Two notes for the captain after Saturday:

- Entry 1.13's `Term` has no status for a quote the checker could not find. `ContractTerms` adds `quote_not_found`.
- The `ContractTerms` extras (`title`, `counterparty`, `pages`, `page_heads`, `read_by`, `term_start_date`) are this package's own model, not `schema/`.

## Risks

- The script patterns are tuned on the two synthetic rooms' wording. A third room with other wording reads `not_stated` more often. Saturday's model reading is the answer; until then, the "contract terms" Panel shows exactly what was and was not read.
- Brasswick's plan starting figure is the P&L's last actual subscription revenue ($84,810), which includes Ostley's annual fee booked in one month (BF4). The shares on Brasswick are therefore lower than a clean start would give.
