# bank-check

**Compare the bank account with the books.** With the founder's consent, the investor connects the company's bank account through a banking connector.

- **Status today:** not started. Left: the Plaid sandbox bank check.
- **Who builds it:** agent with Ken for Plaid.
- **Waits on:** [readout-store](readout-store.md), so bank data is stored with the readout and deleted with it; a Plaid developer account, which is a board row for Ken.
- **Horizon:** Now to Friday night
- **Checked against:** no Plaid code, scans/__init__.py lists bank as planned.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

**Compare the bank account with the books.** With the founder's consent, the investor connects the company's bank account through a banking connector. Tricorder compares deposits with the revenue rows, and outflows with the model's burn, and shows each difference as a claim with its sources ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:52 PM block). It is a check for differences in reporting, never fraud detection (1:33 PM block). A set of books that is fake but consistent with the bank can still get through, and the readout says so.

**Waits on:** [readout-store](readout-store.md), so bank data is stored with the readout and deleted with it; a Plaid developer account, which is a board row for Ken.

**Joins on Saturday:** [readout](readout.md), which places the bank claims in their pieces.

**Includes:**

- **Try the connector first, fake it if needed** (Ken, 3:11 PM: "we can try this, we just need to see if one of these connectors has a trial account and test data. or we could rig it up and fake it, just say we'd connect this here, and here's a sample bank statement you might get"). Plaid's sandbox has free test accounts and custom test data. If it is not working in time, the room carries a sample bank statement (a CSV and a PDF from the generator, labelled as a sample), and the readout shows where the connected account would plug in.
- **The connector: Plaid first.** Its Sandbox offers custom test users whose data covers Balance, Identity and Transactions, among other products ([Plaid Sandbox custom users](https://plaid.com/docs/sandbox/user-custom/), [saved copy](../../reports/20261022.02_research/raw/feasibility/plaid/sandbox_user_custom.md)). No other connector is named here, because no other connector's sandbox docs have been read and saved. Plaid's production terms and pricing have not been read either; the builder reads them before any real account is connected.
- **The consent step.** The founder, not the investor, signs in to the bank through Plaid Link, Plaid's own sign-in flow, so the investor never sees the bank credentials. The page states what is read (balances and transactions, read only), for which accounts and for how long. Tricorder records the consent with its date. The founder can withdraw it, and withdrawing deletes the connection and every transaction pulled, under the data rule from the 11:20 AM block.
- **The checks.** Each is a script; a model only sorts messy transaction descriptions into categories.
  - Deposits against the revenue rows: deposits per month, matched to the revenue file's rows by customer and month, within `match_tolerance`.
  - Outflows against the model's burn: outflows per month against the model's net burn for the same months.
  - The bank balance at the as-of date against the model's cash. On Hollis Voice the model's cash rests on the model alone today, because no bank statement is in the room ([FRAMEWORKS.md](../FRAMEWORKS.md), "Piece verdicts", worked example).
  - New check names in [FRAMEWORKS.md](../FRAMEWORKS.md): `bank_deposits_vs_revenue_rows`, `bank_outflows_vs_model_burn`, `bank_balance_vs_model_cash`, written in the seven parts.
- **The pieces it feeds.** Deposits feed **traction and revenue**. Outflows and the balance feed **burn and runway**. The bank counts as a source independent of the narrative set and of the model, so a match corroborates and a difference contradicts.
- **The gap when no bank is connected.** "Not in the room: bank transactions (no bank connected)", with `would_need` "the founder connects the company's account". It is never a flag.
- **The demo path.** A Plaid Sandbox custom user with configured accounts, created in Sandbox Studio or with `/sandbox/public_token/create`. The limits from the saved page: a configuration larger than about 55 KB, or about 250 transactions, may make the sign-in fail, and more than ten accounts on one custom user fails. Use a non-OAuth test bank such as First Platypus Bank. `roll_dates_forward` keeps the dates current, and the generator leaves it off when a test needs exact dates.
- **The Hollis Voice bank feed.** The data-room generator writes a bank feed from the same simulation, within those limits. Its deposits disagree with the revenue file in one planted place. The plant goes in the answer key with its location, true value, shown value and check name. It is written only with a generator option and kept out of the Saturday rooms, so Saturday's score of found entries and decoys does not change.

**Done when:**

- On the Hollis Voice bank feed, `bank_deposits_vs_revenue_rows` finds the planted difference and nothing else.
- With the plant switched off, no bank check fires.
- On the Sandbox custom user, the bank's balance and transactions arrive through Plaid and match the generated feed.
- With no bank connected, the readout shows the gap and no flag.
- Withdrawing consent deletes the connection and every pulled transaction, and readout-store's list for the company shows none.
- Every claim passes the quote checker against the saved transaction data.
- Tests run on a recorded Sandbox response, so CI never calls Plaid.

**Who:** agent, with Ken for the Plaid account.

**Judgment:** yes.
