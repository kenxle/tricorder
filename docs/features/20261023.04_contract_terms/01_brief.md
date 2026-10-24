# Short brief: contract-terms

Roadmap slice: [contract-terms](../../ongoing/roadmap/contract-terms.md). Rules: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) entry 1.13, "Contract terms". Reasoning: [product_thinking.md](product_thinking.md).

## Who it is for

The associate who prepares the memo, first. The partner who reads it, second ([PERSONAS.md](../../ongoing/PERSONAS.md)).

## The problem

The books count each customer as ARR, MRR and plan revenue. Nothing compares that counting with what the contracts say: when each one ends, whether it renews, when it started, and who has no contract in the room at all. The clauses that change what a customer pays or when it can leave go unread.

## Desired outcome

- Checks 3, 4 and 6 of entry 1.13 run on every room: `plan_revenue_past_term_end`, `signed_not_live_vs_revenue`, `counted_line_without_contract`.
- Exclusivity, most-favoured-customer, change of control and the other pay-or-leave clauses are each a claim that quotes the clause, or a "not stated" result read from every page of the contract.
- A folder of only contracts is a valid input.
- A counted line with no contract becomes an ask line: the current contract language for those customers.
- Check 1 (`cancellable_within_notice_vs_arr`) also runs here, because the slice's Done when asks for the 30-day test (see [04_architecture.md](04_architecture.md), "Check 1 is here").

## Known constraints

- Inside the red-flag engine: `check(room, ids) -> (claims, gaps, panels)`, listed in `scans/redflags/scan.py`.
- Saturday's module `contract_terms.py` owns the model reading and checks 2 and 5. Both share one contract reader and never read a contract twice.
- Scripts only here, no key in the container. Every number is this script's. Every quote passes `schema/check_quotes.py`.
- `data_room/` and `schema/` are not edited. Test contracts are built in the tests.

## The prototype and what it settled

No screen. The prototype is [02_interface_example.md](02_interface_example.md), printed from the real module's output by [spike/contract_terms_spike.py](spike/contract_terms_spike.py) and [spike/render_interface_example.py](spike/render_interface_example.py). It settled: the script reading finds every term the checks need on all seven contracts in the two rooms; the Marlow plan figures match FRAMEWORKS' worked example to the dollar; the "not stated" result can cite each page it read; Brasswick's renewals give three watches. The spike called the module directly, so the prototype became the implementation.
