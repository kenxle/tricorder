# contract-terms

The rest of customer contracts ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:53 PM block).

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** saturday-specs (entry 1.13's prompt and schema, which the Saturday reading uses too); data-room; [readout-store](readout-store.md).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #8, scans/redflags/contract_terms_full.py exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The rest of customer contracts ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:53 PM block). The rules are entry 1.13, "Contract terms", in [FRAMEWORKS.md](../FRAMEWORKS.md). Saturday's [contract-terms-saturday](contract-terms-saturday.md) already reads every contract in both demo rooms and runs three comparisons (the notice check, the pilot check and the price check). This slice adds the rest.

**Waits on:** saturday-specs (entry 1.13's prompt and schema, which the Saturday reading uses too); data-room; [readout-store](readout-store.md).

**Joins on Saturday:** [contract-terms-saturday](contract-terms-saturday.md), whose readings of both demo rooms it extends.

**Includes:**

- Contracts upload with the room or on their own. A folder that holds only contracts is a valid input, and the contracts of rooms beyond the two demo rooms are read the same way.
- The clauses Saturday leaves unread: exclusivity, most-favoured-customer, change of control, and any other clause that changes what the customer pays or when it can leave. Each is a claim that quotes its clause.
- The three comparisons Saturday leaves out: `plan_revenue_past_term_end` (the plan keeps a contract's revenue after its term ends, or treats an automatic renewal as certain), `signed_not_live_vs_revenue` (a signed contract or amendment that has not started is counted as revenue) and `counted_line_without_contract` (a counted line has no contract in the room).
- The ARR and concentration entries keep their own checks and point to this one.
- A contract the room lacks becomes an ask-list line: the current contract language for that customer.

**Done when:**

- On the full Hollis Voice room, the plan check flags the Marlow pilot with its eight plan months after the term ends, and clears Cedar & Pine and Brookline Row.
- The exclusivity, most-favoured-customer and change-of-control fields return "not stated" for the Hollis Voice contracts, each read from the contract and not assumed.
- A test contract with a change-of-control clause returns that clause with its quote.
- A folder that holds only contracts produces a result with no crash.
- A test contract with a 30-day cancellation counted as a year of ARR produces a gap. The same contract with a one-year commitment does not.
- Every quote passes the quote checker.

**Who:** agent.

**Judgment:** yes.

**Status:** done for every Done when check. Merged in PR #8 on 2026-10-23. The code is `scans/redflags/contract_reader.py` (the one contract reader for entry 1.13) and `scans/redflags/contract_terms_full.py` (checks 1, 3, 4 and 6 and the clause notes). The 30-day line is met as a flag under check 1, which is entry 1.13's sense of a gap, not a missing input. Checks 2 and 5 stay with [contract-terms-saturday](contract-terms-saturday.md), on the seam in the feature's architecture. Feature folder: [20261023.04_contract_terms](../../features/20261023.04_contract_terms/00_progress.md).
