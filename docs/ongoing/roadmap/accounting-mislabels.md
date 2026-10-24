# accounting-mislabels

The rest of the accounting mislabels family ([FRAMEWORKS.md](../FRAMEWORKS.md), entry 1.12; [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:32 PM block).

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** data-room; saturday-specs (entry 1.12's check names).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #4, scans/redflags/mislabels.py exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The rest of the accounting mislabels family ([FRAMEWORKS.md](../FRAMEWORKS.md), entry 1.12; [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:32 PM block). Saturday's [redflag-engine](redflag-engine.md) runs the two kinds it already owns. Entry 1.12 marks six more as runnable on Hollis Voice. An agent builds them here, before Saturday, outside the engine's 3.0 hours.

**Waits on:** data-room; saturday-specs (entry 1.12's check names).

**Joins on Saturday:** [redflag-engine](redflag-engine.md), whose pilot-as-ARR flag the `mrr` check links to.

**Includes:**

- The six sub-checks entry 1.12 marks Saturday that the engine does not run: `mrr_column_vs_subscription_rows`, `billings_vs_recognised_revenue`, `contractor_spend_vs_headcount_and_burn`, `capitalised_spend_vs_pnl_and_cash`, `deferred_revenue_vs_earned` and `one_time_fees_in_recurring_metrics`. Scripts only, as in the engine.
- Kind c, gross against net revenue (`gross_vs_net_revenue`), with a generator option that writes a resale line into a test room, because Hollis Voice has nothing to run it on.
- Each kind's gap when the room lacks its file, worded as entry 1.12 gives it.
- Each claim names its kind and feeds the piece entry 1.12 names.

**Done when:**

- On the full room, `mrr_column_vs_subscription_rows` finds the Marlow pilot's fee in the `mrr` column and links it to the pilot-as-ARR flag as one cause.
- The onboarding-fee decoy and the annual-prepay decoy stay clear.
- On the seed drop, each sub-check whose file is missing returns `cannot_check` with its gap.
- On the test room with a resale line, `gross_vs_net_revenue` fires. With the option off, it does not.
- Every claim passes the quote checker.

**Who:** agent.

**Judgment:** no.

**Status:** done. Merged in PR #4 on 2026-10-23. The code is `scans/redflags/mislabels.py`. On Brasswick it also finds BF1, BF3 and BF4. Feature folder: [20261022.12_accounting_mislabels](../../features/20261022.12_accounting_mislabels/00_progress.md).
