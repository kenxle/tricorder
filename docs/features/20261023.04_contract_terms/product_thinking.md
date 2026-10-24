# Product thinking: contract-terms

## User job

The associate who prepares the memo has a data room with a few customer contracts and a model that counts every customer as ARR and as plan revenue. Before she trusts the revenue line, she wants to know where the counting runs ahead of the paper: a pilot the plan keeps after it ends, a customer who can walk in 30 days but is counted for a year, revenue booked before a contract started, and how much of the counted revenue has any contract behind it at all. She also wants the clauses a partner asks about first, exclusivity, most-favoured-customer pricing and change of control, read and quoted, or plainly marked as absent. Ken asked for contracts as an input, "checked for gaps such as cancellation periods" ([ROADMAP.md](../../ongoing/roadmap/contract-terms.md), 1:53 PM block).

The partner who reads the memo needs one line per finding, with the clause and the cell side by side ([USER_STORIES.md](../../ongoing/USER_STORIES.md)).

## Evidence

Observed in the rooms (the spike, [spike/out/](spike/out/)):

- Hollis Voice holds three contracts. The Marlow pilot ends 2027-01-31 with no renewal clause, and the plan grows a starting figure that includes its $15,000 for every month to 2027-09. Eight plan months rest on it, $161,258 of plan revenue.
- No Hollis Voice contract has an exclusivity, most-favoured-customer or change-of-control clause. Cedar & Pine's fees are fixed for the initial term.
- The room holds contracts for 3 of the 213 counted customers: 27.6% of the counted MRR. The seven cohort lines in `ARR_Build` have no contract at all, which becomes seven ask lines.
- Brasswick's three customer contracts all renew by themselves, and its plan carries their revenue past each term end with no non-renewal rate: three watches.

## Assumptions

- A1. Contract wording in seed and Series A rooms is regular enough for a script to find terms by heading and wording. The two synthetic rooms are. A real room may not be, which is what Saturday's model reading is for.
- A2. A contract matches a customer by name, after the normalisation FRAMEWORKS 1.13 gives.
- A3. The plan's starting figure holds every counted contract at its counted MRR, so a contract's part of a plan month is its share of the start (FRAMEWORKS 1.13, "Mechanical check").

## Priority and the best next move

This is the Friday half of entry 1.13. Saturday's hour (contract-terms-saturday) reads the contracts with the model and runs checks 2 and 5. Building the shared reader, the clause notes and checks 3, 4 and 6 today means Saturday's hour is only the model call and two comparisons, and the demo has the pilot's plan flag even if the model reading falls back.
