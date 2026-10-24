# redflag-engine

The red flags in the financials and metrics: the organisers' first direction, and first in the feasibility research's ranking.

- **Status today:** partly built. Left: the deck claims page, ARR definition, burn against hiring plan, deck against model, customer concentration, gross margin, vanity metric, cap table and green-flag cells.
- **Who builds it:** design-and-finance.
- **Waits on:** skeleton (the schema, frozen this week), readers (merged at 11:30), data-room, saturday-specs (the check list). The pure checks that compute numbers start at 10:30.
- **Horizon:** Saturday
- **Checked against:** scans/redflags/ has cohorts, mislabels, deck_vs_books, contract terms, scan.py lists the missing checks.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The red flags in the financials and metrics: the organisers' first direction, and first in the feasibility research's ranking.

**Waits on:** skeleton (the schema, frozen this week), readers (merged at 11:30), data-room, saturday-specs (the check list). The pure checks that compute numbers start at 10:30.

**Includes:**

- Scripts only on Saturday. A junior Python-and-Excel builder has 3.0 hours for 7 checks, so this slice makes no model call ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), finding 2). Every planted flag already has a script check (feasibility Part 3.2).
- One pandas check per planted flag in the data room research's Part 3.4, over the CSVs and the model: pilot booked as ARR, deck ARR against the model (1 percent tolerance), churn hidden in the cohort tab, burn against the hiring plan, customer concentration, gross margin without delivery costs, cumulative sign-ups shown as active clinics. The video-against-deck variant is found by the readout slice, because it needs the video scan's output.
- Deck claims read from the deck's claims page (slide 14) by regex, with `01_overview/claims.json` as the fallback (feasibility 1.1 and 1.9). The buildability critic's regex read 14 of 14 rows; three rows need a better label split.
- Files are read through `schema/readers.py`. The scan writes no reader of its own.
- The script decides that a number is wrong (feasibility Part 3.2). The model reading that gives a flag its clause quotes (the pilot contract) is the [contract-terms-saturday](contract-terms-saturday.md) slice, owned by backend-and-data after the video slice. The model's reading of the cohort note is built before Saturday by an agent, in [financial-model](financial-model.md).
- Each flag is a Claim with the claimed number, the computed number, a severity, and sources pointing at both places.
- The cells behind the green flags, read by script with no judgement: the round from the cap table (new money, pre-money, Series A ownership) and the model (`SERIES_A_RAISE`), the market size (`MARKET_TAM_USD`), staff today (`STAFF_NOW`) and staff after hiring (the last row of `hiring_plan.csv`). The cap table's sum check (`cap_table_reconcile`, [FRAMEWORKS.md](../FRAMEWORKS.md) entry 1.10) runs here, so the clean cap table (DC3) reads clear. The readout's strong pieces rest on these claims, and no other Saturday slice writes them.
- `python -m scans.redflags <room>` writes `out/<room>/redflags.json`.
- A test in `scans/redflags/tests/` that compares the output to the answer key by check name.
- Accounting mislabels, the Saturday part ([FRAMEWORKS.md](../FRAMEWORKS.md), entry 1.12; [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:32 PM block). The two kinds this slice already checks carry their mislabel kind on the claim: the pilot booked as ARR is kind a, and gross margin without delivery costs is kind d. Entry 1.12 marks six more sub-checks as runnable on this room. They sit outside this slice's 3.0 hours: an agent builds them before Saturday in the [accounting-mislabels](accounting-mislabels.md) slice, and they join this slice's output on Saturday.

**Done when:**

- On the seed drop, the test finds the four flags the research says the seed drop can show from this scan: deck ARR against the model, burn against the hiring plan, gross margin, and the clinic count.
- On the full room it also finds the pilot as ARR, the cohort churn and the customer concentration.
- None of the three decoys (the onboarding fee, the annual prepay, the clean cap table) is flagged.
- The round, market size and staff claims match the answer key's `green_flags` values within 1 percent.
- On the clean room from [blind-room](blind-room.md), no planted-flag check fires.
- The pilot-as-ARR flag and the gross-margin flag each name their mislabel kind from entry 1.12.
- The scan runs with no network, so it can run live on the demo laptop.
- Every claim passes the quote checker.

**Who:** design-and-finance.

**Hours:** 3.0 (10:30 AM to 2:00 PM, less lunch).

**Judgment:** yes.
