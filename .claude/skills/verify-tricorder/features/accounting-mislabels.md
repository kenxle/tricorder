# Accounting mislabels

The red-flag engine runs entry 1.12's sub-checks on a room's model, metrics, customer rows and ledger. Each one either flags money counted under the wrong label, comes back clear with the figures it compared, or says why it cannot run. It also writes three panels: the entry, the checks table and the lines table.

## Sub-features

- `am-mrr` (kind a) flags non-recurring money in the `mrr` column, against the subscription rows.
- `am-billings` (kind b) flags billings shown as recognised revenue.
- `am-gross` (kind c) flags pass-through money shown as gross revenue.
- `am-contractors` (kind e) flags contractors left out of burn or cut from the plan.
- `am-capitalised`, `am-deferred`, `am-onetime` (kinds f, g, h) check capitalised spend, deferred revenue and one-time fees.
- `am-gaps` writes a gap for every sub-check whose file the room lacks.
- `am-decoys` keeps the planted decoys clear.

## How to get to it (user POV)

- Run the red-flag scan on a room: `python3 -m scans.redflags <room>`.
- Run every scan and the memo: `bin/smoke <room>`.
- Through the API: `POST /api/rooms/<room>/scans/redflags`, then `GET /api/rooms/<room>/results/redflags`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.

- **Run the scan on Hollis Voice.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`. Exit code 0.
- **Read the MRR flag.** Run `control.sh api GET /api/rooms/hollis_voice/results/redflags`. A claim with `check.name` `mrr_column_vs_subscription_rows` and severity `flag` says MRR of $186,739 for 2026-09 against $171,739 from subscription rows, the $15,000 Marlow pilot. Its sources include `ARR_Build!E13`.
- **Check the rest are clear.** In the same response, the claims for `billings_vs_recognised_revenue`, `contractor_spend_vs_headcount_and_burn`, `capitalised_spend_vs_pnl_and_cash`, `deferred_revenue_vs_earned` and `one_time_fees_in_recurring_metrics` are severity `info`. The panels include `accounting mislabels: checks`.
- **Seed drop gaps.** Run the scan on `data_room/hollis_voice_seed_drop` and read its result. The `mrr` flag still fires from the model's `ARR_Build` cells. Gaps include "Not in the room: an expense ledger".
- **Brasswick.** Run the scan on `data_room/brasswick` and read its result. Flags fire for `billings_vs_recognised_revenue`, `gross_vs_net_revenue`, `contractor_spend_vs_headcount_and_burn` and `deferred_revenue_vs_earned`.
- **Score.** Build the readouts first with `control.sh cli python3 -m scans.memo data_room/brasswick` (and the same for `hollis_voice`), then run `control.sh cli python3 -m eval.score data_room/brasswick`. The transcript has `found  BF1`, `found  BF3`, `found  BF4` and `decoys flagged 0 of 3`. Run the same on `data_room/hollis_voice`; it shows `decoys flagged 0 of 3`.
- **Clean room.** Run the scan on `data_room/hollis_voice_clean`. No mislabel claim is severity `flag`.

## Gotchas

- Hollis Voice scores `found 0 of 8` here. Its planted flags belong to checks not built yet (the ARR definition check 1.2 and the Saturday engine), so a 0 there is expected, not a regression of this feature.
- The resale room for kind c exists only inside the unit tests, built in a temporary folder. Hollis Voice has no pass-through money, so kind c does not run there.
- Duplicate gaps (two "an expense ledger" lines) come from two sub-checks needing the same file. The ask list folds them into one line.
