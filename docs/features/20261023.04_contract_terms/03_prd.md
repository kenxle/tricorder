# PRD: contract-terms

Context and users are in the [short brief](01_brief.md) and [product_thinking.md](product_thinking.md). The agreed behaviour is the output in [02_interface_example.md](02_interface_example.md). The rules are FRAMEWORKS.md entry 1.13; this page says which parts this slice builds and how.

## Scope

In scope:

- One shared contract reader for entry 1.13, used by this slice and by Saturday's module.
- Checks 1, 3, 4 and 6 of entry 1.13.
- The clause notes: exclusivity, most-favoured-customer, change of control, and other clauses that change what a customer pays or when it can leave.
- Contracts in a room, or in a folder of only contracts, under any file names.
- Gaps for missing contracts, worded so the memo's coverage step turns them into ask lines.

Not in scope:

- The model reading with entry 1.13's prompt, and checks 2 (`pilot_without_duty_to_convert_vs_recurring`) and 5 (`contract_price_vs_counted_price`). Saturday's `contract_terms.py` builds them.
- A judged claim quoting "contracted" or "locked in" language in the deck past a term end (check 3's model add-on). It needs the model reading.
- The readout page's display of the two Panels. The page shows claims and gaps already.

## Requirements

Each requirement has a stable id. The Plan's verification table names the test for each.

- **CT-R1. Find every contract.** Every PDF in the folder, at any depth, that matches the room's contract file patterns (`scans.base.INPUT_KINDS["contracts"]`) or whose first page names a party "(the Customer)" or similar under a title naming an order form, agreement or statement of work. A folder of only contracts is a valid input and produces the terms, the clause notes and one gap for the missing counting files.
- **CT-R2. Missing and unreadable inputs are gaps.** No contract: the gap "Not in the room: customer contracts" and nothing else. A PDF that cannot be opened: "Not in the room: a readable copy of <file>", and the other contracts still run. No customer file: "Not in the room: the ARR build or the customer file to compare with". A contract whose customer has no row: "Not in the room: a customer row for <name>".
- **CT-R3. Check 3, plan revenue past a term end.** For each customer contract with a term end, the plan months after it, from the P&L plan columns of the recurring revenue row. `plan_share` is the customer's as-of MRR over the plan's starting figure (Assumptions, else the row's last actual month). Flag when the contract has no renewal clause; watch when it renews by itself and the Assumptions tab states no non-renewal rate; clear with an info claim when the share is at or below `match_tolerance` or no plan month comes after. A clear that leaves the last day to give notice inside the plan window says so. The claim states the months, the plan revenue resting on the contract and its first month's part, and cites the term, the starting cell, the customer rows and every plan cell summed.
- **CT-R4. Check 4, signed but not live.** Flag when the customer file's first month with MRR is earlier than the contract's effective month, or when a fee change from a later date (an amendment, a fee step) is already in an earlier month's MRR. Otherwise an info claim with the tie-out.
- **CT-R5. Check 6, counted lines without a contract.** One gap per `ARR_Build` line (cohort and named lines, not subtotals or zero-ARR lines) whose customer count exceeds the contracts the room holds for it, worded "Not in the room: the contract for <line> (<n> customers)". Without an ARR build, one gap naming every counted customer without a contract. One info claim gives the counted MRR the contracts cover, and its share of the as-of MRR.
- **CT-R6. Missing contracts reach the ask list.** Each check-6 gap's `would_need` is a sentence the operator can paste, asking for "the current customer contract language" for those customers, and the memo's coverage step turns it into an ask line under checklist row C34.
- **CT-R7. The three clause fields.** For each contract, a stated exclusivity, most-favoured-customer or change-of-control clause is an info claim (confidence `quoted`) whose quote is the whole numbered clause. The fields not stated share one info claim that names them and cites every page of the contract as read. The Panel "contract terms" holds each field's status.
- **CT-R8. Other clauses.** A fee freeze, a price increase right, a minimum commitment, a refund or credit, and a usage-based fee are each an info claim quoting its clause, one per kind per contract.
- **CT-R9. Check 1, notice against ARR.** Earliest exit per FRAMEWORKS 1.13 (a right to end for any reason, else the term end, else the renewal term once the notice day has passed). Flag when the customer is counted and the exit is within `short_notice_days`, or the term has ended with no renewal. Watch when the term is under `min_contract_months`. A right to end only after an event (a breach, a change of control) is not a right to end for any reason.
- **CT-R10. Supplier contracts.** A contract whose other party is a contractor, supplier or vendor gets its terms and clause notes and no customer check or customer-row gap.
- **CT-R11. One reading.** `contract_reader.read_room(room)` reads each contract once per folder and file version. A model reader registered by Saturday's module is used instead of the script; if it fails, the script reading is used and the failure is a gap.
- **CT-R12. Every quote passes the quote checker.** Every term's quote is confirmed at its page before any check uses it; a term whose quote is not found is marked `quote_not_found` and not used.
- **CT-R13. In the engine, offline, no decoy.** Listed in `scan.CHECKS` as `contract_terms_full`, leaving `contract_terms` for Saturday. No network call. On Hollis Voice no flag cites the Brookline Row order form or the onboarding cells (decoys DC1 and DC2).

## Failure cases

| Case | Behaviour |
|---|---|
| No contract in the folder | One gap, "Not in the room: customer contracts" (CT-R2) |
| A PDF that will not open | A gap for that file; the rest run |
| Contracts with no room | Terms, clause notes, one counting gap; no comparison |
| A term the contract does not state | `not_stated`; the check that needs it is `cannot_check` in the "contract checks" Panel, not a gap |
| A quote not found at its page | The term is `quote_not_found` and unused |
| A cell that breaks a check | A gap naming the check and the contract; the other checks run |

## Questions

- **Q1 (Ken).** Check 4 flags a long-time customer whose only contract in the room is a later renewal order form, because the effective date is after the first MRR month. FRAMEWORKS' rule does that. Should a contract that says it renews or replaces an earlier one be read as live from the earlier date?
- **Q2 (Ken).** A month-to-month contract has no term end, so check 3 returns `cannot_check` for it. Should such a contract count as renewing every month (a watch when the plan carries it)?
- **Q3 (Saturday owner).** Check 1 is built here. Saturday's module should not write it again (see the architecture's "Check 1 is here").
- **Q4 (coverage owner).** Seven check-6 gaps make seven ask lines on Hollis Voice. The SAFE gaps are folded into one line by default; the same could be done for contract gaps.
