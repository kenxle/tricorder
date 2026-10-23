# Contract terms

The red-flag engine reads every customer contract in a room, or in a folder that holds only contracts, and compares each one with how the customer is counted. The user sees a flag when the plan keeps a contract's revenue after its term ends, when a customer who can leave on short notice is counted as a year of ARR, or when revenue is counted before a contract starts. Each contract's exclusivity, most-favoured-customer and change-of-control clauses come back quoted or as "not stated", and every counted line with no contract in the room becomes an ask-list line for the current contract language.

## Sub-features

- `ct-plan` (`plan_revenue_past_term_end`) flags plan months that rest on a contract after its term ends, and watches an automatic renewal the plan treats as certain.
- `ct-notice` (`cancellable_within_notice_vs_arr`) flags a customer who can leave within 90 days but is counted as a year of ARR.
- `ct-live` (`signed_not_live_vs_revenue`) flags revenue counted before a contract or an amendment takes effect.
- `ct-missing` (`counted_line_without_contract`) writes one gap per ARR build line with no contract, and one coverage claim.
- `ct-clauses` (`clause_notes`) quotes exclusivity, most-favoured-customer, change-of-control and other pay-or-leave clauses, or says each is not stated.
- `ct-terms-panel` writes the Panels `contract terms` and `contract checks`.
- `ct-contracts-only` reads a folder of contracts with no room around it.
- `ct-asks` turns each missing-contract gap into an ask line after the memo runs.

## How to get to it (user POV)

- Run the red-flag scan on a room: `python3 -m scans.redflags <room>`.
- Run it on a folder that holds only contracts, under any file names: `python3 -m scans.redflags <folder>`.
- Run every scan and the memo: `bin/smoke <room>`; the ask lines are in the readout's `asks`.
- Through the API: `POST /api/rooms/<room>/scans/redflags`, then `GET /api/rooms/<room>/results/redflags`, then `POST /api/rooms/<room>/readout`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- For the contracts-only folder, a scratch folder outside the repo holding copies of the three PDFs in `data_room/hollis_voice/04_customers/`, renamed `contract_0.pdf` to `contract_2.pdf`.

- **Run the scan on Hollis Voice.** Run `control.sh api POST /api/rooms/hollis_voice/scans/redflags`. HTTP 200.
- **Read the plan flag.** Run `control.sh api GET /api/rooms/hollis_voice/results/redflags`. A claim with `check.name` `plan_revenue_past_term_end` and severity `flag` names the Marlow Veterinary Group pilot agreement, "8 plan months after it (2027-02 to 2027-09)" and "$161,258". The same check's claims for Cedar & Pine Animal Hospitals and Brookline Row Veterinary are severity `info`.
- **Read the clause results.** In the same response, each of the three contracts has a `clause_notes` claim reading "no exclusivity, most-favoured-customer or change-of-control clause", with one source per page of that contract. The Panel `contract terms` shows `not_stated` for `exclusivity`, `most_favoured_customer` and `change_of_control` on each contract.
- **Prove a quote.** Post the Marlow plan claim's first source to `control.sh api POST /api/rooms/hollis_voice/source '<source json>'`. The text returned contains "from 2026-08-01 to 2027-01-31".
- **Read the gaps.** The result's gaps include "Not in the room: the contract for Subscriptions signed 2025 Q1 (13 customers)", seven such lines in all. A `counted_line_without_contract` claim says "$51,584 of the $186,739 counted MRR in 2026-09 (27.6%)".
- **Ask lines.** Run `control.sh api POST /api/rooms/hollis_voice/readout`. The readout's `asks` include lines that start "Please send the current customer contract language" with `checklist_id` `C34`.
- **Contracts-only folder.** Run `control.sh cli python3 -m scans.redflags <folder>`. Exit code 0. The result file it names holds `clause_notes` claims for three contracts and the gap "Not in the room: the ARR build or the customer file to compare with".
- **Seed drop.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice_seed_drop`. Its result has the gap "Not in the room: customer contracts" and no contract claims.
- **Score.** After the readout was built in this run, run `control.sh cli python3 -m eval.score data_room/hollis_voice`. The transcript shows `decoys flagged 0 of 3`.

## Gotchas

- The test contracts (a 30-day cancellation, a one-year commitment, a change-of-control clause) exist only inside the unit tests, built in a temporary folder: `python3 -m pytest scans/redflags/tests/test_contract_terms_full.py`. No room in `data_room/` holds them.
- The API lists only folders that hold a `00_` to `09_` subfolder, so a contracts-only folder is driven through the CLI. A folder shaped `<name>/04_customers/*.pdf` under `rooms/` is listed.
- Checks 2 and 5 of entry 1.13 and the model reading are not here; they are built on Saturday in `contract_terms.py`. Until then the Marlow pilot's "no duty to convert" has no claim of its own.
- Brasswick returns `watch` on `plan_revenue_past_term_end` for three customers: their automatic renewals carry plan months and the plan states no non-renewal rate. That is the entry's rule, not a fault.
- Hollis Voice still scores `found 0 of 8` from these checks: the answer key credits PF1 to `arr_from_subscription_rows`, which is not built yet.
