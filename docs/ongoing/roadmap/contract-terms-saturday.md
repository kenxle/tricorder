# contract-terms-saturday

Every contract in the room, read for its terms and checked against how each customer is counted, on both demo rooms.

- **Status today:** not started. Left: the model reading of contracts and checks 2 and 5.
- **Who builds it:** backend-and-data.
- **Waits on:** redflag-engine (the pilot flag these claims sit beside), pitch-video (backend-and-data starts this after the video slice), readers, claim-result (the quote checker).
- **Horizon:** Saturday
- **Checked against:** scans/redflags/contract_terms.py does not exist, the shared contract_reader.py does.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Every contract in the room, read for its terms and checked against how each customer is counted, on both demo rooms. It is the Saturday part of entry 1.13, "Contract terms", in [FRAMEWORKS.md](../FRAMEWORKS.md) ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:53 PM block).

**Waits on:** redflag-engine (the pilot flag these claims sit beside), pitch-video (backend-and-data starts this after the video slice), readers, claim-result (the quote checker).

**Includes:**

- One model request per room reads every contract in it, with entry 1.13's prompt and schema, one schema per request. Hollis Voice has three contracts in `04_customers/`: the Cedar & Pine order form, the Marlow pilot agreement and the Brookline Row order form. Brasswick has four in `04_contracts/`: the Corvane agreement, the Ostley and Tessmore order forms, and the Norrgate statement of work.
- The terms read: start, end and length; the notice that ends a running contract, kept apart from the notice not to renew; auto-renewal; pilot or trial terms and any duty to convert; the price, any discount and the list price; payment terms. Each stated term is a claim that quotes its clause. The request also returns the clause fields (exclusivity, most-favoured-customer, change of control), but nothing reads them until [contract-terms](contract-terms.md).
- Brasswick's Norrgate statement of work is a supplier contract. It is read for its terms and shown as info claims. It is not matched to a customer row, so it produces no check and no missing-customer gap.
- Three of entry 1.13's script comparisons, run on both rooms: `cancellable_within_notice_vs_arr`, `pilot_without_duty_to_convert_vs_recurring` and `contract_price_vs_counted_price`. They compare each contract with the ARR build (Hollis Voice) or the model's `Revenue_Build` tab (Brasswick), the MRR column (`mrr` in `customer_mrr_by_month.csv`, or `subscription_revenue` in Brasswick's metrics and customer files), and the largest customer's share. The price check also confirms the fee behind that share.
- The model reads clauses. The script decides that a number is wrong. Each comparison cites the flag it explains and sits beside the claim from entries 1.2, 1.6 and, where it applies, 1.12.
- If the hour runs short, Hollis Voice is finished before Brasswick is started.
- `python -m scans.readings <room>` writes `out/<room>/readings.json`.

**Not in this slice:** checks 3, 4 and 6 (plan revenue past a contract's end, a signed contract not yet live, a counted line with no contract), the exclusivity, most-favoured-customer and change-of-control clauses, and contracts beyond the room's. An agent builds those before Saturday in [contract-terms](contract-terms.md). The cohort note reading is in [financial-model](financial-model.md), also built before Saturday.

**Done when:**

- On Hollis Voice, the Marlow pilot agreement's 30-day notice and its "nothing requires the Customer to buy a subscription" clause are read with quotes. The notice check and the pilot check both flag it, with the clause beside the ARR row (`ARR_Build!E13`) and the `mrr` rows.
- On Hollis Voice, Cedar & Pine's 90 days and Brookline Row's 30 days are read as notice not to renew, and both contracts return clear on all three checks. Brookline Row's 10 percent discount is read and matches the counted price.
- On Brasswick, the three customer contracts return their terms. Corvane and Tessmore return clear. The price check finds Ostley Freight's $27,540 in `Revenue_Build` against the order form's $2,295 a month, and reports it as one cause with the annual prepayment flag from entry 1.12 (BF4).
- The Norrgate statement of work returns its term, its notice and its fee as info claims, and no comparison.
- On the Hollis Voice seed drop, which holds no contracts, the entry returns `cannot_check` with the gap "Not in the room: customer contracts".
- Every quote passes the quote checker. On the demo laptop the readings show as frozen output, saved for both rooms under `demo/frozen/` before the freeze.

**Who:** backend-and-data.

**Hours:** 1.0 (2:30 to 3:30 PM). Fourth in the [demo fallback order](saturday.md#demo-fallback-order): if it is not working at the freeze, the pilot flag still shows from the engine's script check, without clause quotes.

**Judgment:** no.
