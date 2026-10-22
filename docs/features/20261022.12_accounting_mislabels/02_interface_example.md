# Interface example: what accounting mislabels emits

This feature has no screen, so its prototype is its output. Everything below was written by [spike/render_example.py](spike/render_example.py) from the JSON that [spike/mislabels_spike.py](spike/mislabels_spike.py) wrote to `spike/out/`. Nothing here was typed by hand. The raw run log is [spike/spike_run.txt](spike/spike_run.txt) and the answer-key score is [spike/score_run.txt](spike/score_run.txt).

The claims use the shared Claim from [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), "The shared Claim". The spike checked each one three ways: against the JSON Schema in entry 1.12's output shape, against the skeleton's Pydantic models (`schema.claim`), and with the skeleton's quote checker (`schema.check_quotes.check_claim`). All six rooms passed all three. Claim ids here use a spike prefix (`redflags-mislabels-NNN`); the real module takes ids from `scans.base.Ids`, so they become `redflags-NNN`.

## Full room: data_room/hollis_voice

Entry label: **flag**. Worst sub-check label is flag: mrr_column_vs_subscription_rows.

| Sub-check | Label | Really is | File read | Claim ids |
|---|---|---|---|---|
| `mrr_column_vs_subscription_rows` | flag | pilot | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-001 |
| `billings_vs_recognised_revenue` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-002 |
| `gross_vs_net_revenue` | not_run | not_checked | `03_metrics/customer_mrr_by_month.csv` | none |
| `contractor_spend_vs_headcount_and_burn` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-003 |
| `capitalised_spend_vs_pnl_and_cash` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-004 |
| `deferred_revenue_vs_earned` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-005 |
| `one_time_fees_in_recurring_metrics` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-006 |

### The one flag: the pilot in the `mrr` column

This is the claim the roadmap's first Done when asks for. It cites the metrics row and the pilot's own row in the customer file.

```json
[
  {
    "id": "redflags-mislabels-001",
    "scan": "redflags",
    "text": "monthly_metrics.csv shows MRR of $186,739 for 2026-09. The subscription rows add to $171,739. The $15,000 difference is 8.7% of subscription MRR and equals the non-subscription lines: Marlow Veterinary Group (Pilot, $15,000). Months over tolerance: 2026-08, 2026-09.",
    "value": {
      "number": 171739.0,
      "unit": "USD_per_month",
      "label": "mrr",
      "period": "2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "mrr_column_vs_subscription_rows",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "03_metrics/monthly_metrics.csv",
        "locator": "row 22",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,186739,2240868,212,357,72149",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "03_metrics/customer_mrr_by_month.csv",
        "locator": "row 2101",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,C0219,Marlow Veterinary Group,20,Pilot,Pilot,15000,0,15000",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!A13",
        "start_s": null,
        "end_s": null,
        "quote": "Marlow Veterinary Group (pilot)",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!E13",
        "start_s": null,
        "end_s": null,
        "quote": "180000",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  }
]
```

The link to entry 1.2's pilot-as-ARR flag. The Claim has no field for it, so the spike writes it beside the result. [04_architecture.md](04_architecture.md) proposes carrying it as a Panel.

```json
[
  {
    "claim_id": "redflags-mislabels-001",
    "same_cause_as_check": "arr_from_subscription_rows",
    "shared_sources": [
      "03_metrics/customer_mrr_by_month.csv row 2101",
      "02_financials/financial_model.xlsx ARR_Build!A13",
      "02_financials/financial_model.xlsx ARR_Build!E13"
    ],
    "pilot_arr_counted_cell": "ARR_TOTAL"
  }
]
```

The lines panel: places where a label claims recurring money and the line holds a pilot.

```json
[
  {
    "locator": "03_metrics/monthly_metrics.csv row 22",
    "label_shown": "mrr",
    "kind": "pilot",
    "claim_id": "redflags-mislabels-001"
  },
  {
    "locator": "P&L!W10",
    "label_shown": "Recurring revenue (subscription plus pilot)",
    "kind": "pilot",
    "claim_id": "redflags-mislabels-001"
  }
]
```

### The clear sub-checks

Each clear sub-check writes one info claim with the tie-out it ran, so the readout can show that the check ran and on what. None of them cites a Brookline Row (C0193) row, a June 2026 billings row or an Onboarding row.

```json
[
  {
    "id": "redflags-mislabels-002",
    "scan": "redflags",
    "text": "The P&L row \"Subscription revenue\" matches subscription revenue in the customer file in all 21 actual months (largest difference $0). Billings differ from revenue by more than 1.0% in 18 of those months, which annual plans paid up front explain on their own.",
    "value": {
      "number": 171739.0,
      "unit": "USD",
      "label": "other",
      "period": "2026-09"
    },
    "severity": "info",
    "check": {
      "kind": "script",
      "name": "billings_vs_recognised_revenue",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!W7",
        "start_s": null,
        "end_s": null,
        "quote": "171739",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "03_metrics/customer_mrr_by_month.csv",
        "locator": "row 1",
        "start_s": null,
        "end_s": null,
        "quote": "month,customer_id,customer_name,locations,plan,product_type,mrr,one_time_fee,billings",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-003",
    "scan": "redflags",
    "text": "Ledger lines tie to P&L cost of revenue plus operating expenses in all 21 actual months (largest difference $0). No ledger line names a contractor, consultant, freelancer, agency or statement of work.",
    "value": {
      "number": 372919.22,
      "unit": "USD",
      "label": "other",
      "period": "2026-09"
    },
    "severity": "info",
    "check": {
      "kind": "script",
      "name": "contractor_spend_vs_headcount_and_burn",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!W26",
        "start_s": null,
        "end_s": null,
        "quote": "335571.42",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "Assumptions!B9",
        "start_s": null,
        "end_s": null,
        "quote": "17",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-004",
    "scan": "redflags",
    "text": "Every ledger line is booked as one of Cost of revenue, G&A, R&D, S&M; none names an asset. The cash bridge difference is -$0.24 against cash of $1,800,000.",
    "value": {
      "number": 1800000.0,
      "unit": "USD",
      "label": "cash",
      "period": "2026-09"
    },
    "severity": "info",
    "check": {
      "kind": "script",
      "name": "capitalised_spend_vs_pnl_and_cash",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/expense_ledger.csv",
        "locator": "row 1",
        "start_s": null,
        "end_s": null,
        "quote": "month,date,vendor,description,category,booked_as,amount_usd",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "Cash_Bridge!B12",
        "start_s": null,
        "end_s": null,
        "quote": "-0.24000000022351742",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "Assumptions!B6",
        "start_s": null,
        "end_s": null,
        "quote": "1800000",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-005",
    "scan": "redflags",
    "text": "Billed but not yet earned at 2026-09: $104,876 across 28 customers. The P&L row \"Subscription revenue\" does not exceed revenue earned in any month, and ARR_Build Subscription ARR ($2,060,868) is 12 times 2026-09 subscription revenue.",
    "value": {
      "number": 104876.0,
      "unit": "USD",
      "label": "other",
      "period": "2026-09"
    },
    "severity": "info",
    "check": {
      "kind": "script",
      "name": "deferred_revenue_vs_earned",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "03_metrics/customer_mrr_by_month.csv",
        "locator": "row 1",
        "start_s": null,
        "end_s": null,
        "quote": "month,customer_id,customer_name,locations,plan,product_type,mrr,one_time_fee,billings",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!E12",
        "start_s": null,
        "end_s": null,
        "quote": "2060868",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-006",
    "scan": "redflags",
    "text": "One-time fees of $9,500 in 2026-09 are not in the mrr column: the gap between mrr and subscription rows is $15,000, not the fee total, and the ARR_Build row \"Onboarding fees\" counts $0 of ARR.",
    "value": {
      "number": 9500.0,
      "unit": "USD",
      "label": "other",
      "period": "2026-09"
    },
    "severity": "info",
    "check": {
      "kind": "script",
      "name": "one_time_fees_in_recurring_metrics",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "03_metrics/monthly_metrics.csv",
        "locator": "row 22",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,186739,2240868,212,357,72149",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!A14",
        "start_s": null,
        "end_s": null,
        "quote": "Onboarding fees",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!E14",
        "start_s": null,
        "end_s": null,
        "quote": "0",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  }
]
```

### Gaps on the full room

- Not in the room: a revenue export that separates pass-through money (why: not stated in the file; would need: a revenue export with a pass-through or resale column, and the ledger lines paid on at cost; piece: traction_and_revenue)
- Not in the room: a list of contractors, or an org chart that shows them (why: file missing; would need: a contractor list or contractor agreements; piece: burn_and_runway)
- Not in the room: a balance sheet (why: file missing; would need: monthly balance sheets; piece: burn_and_runway)
- Not in the room: a balance sheet with a deferred revenue line (why: file missing; would need: monthly balance sheets; piece: traction_and_revenue)

## Seed drop: data_room/hollis_voice_seed_drop

Entry label: **flag**. Worst sub-check label is flag: mrr_column_vs_subscription_rows.

| Sub-check | Label | Really is | File read | Claim ids |
|---|---|---|---|---|
| `mrr_column_vs_subscription_rows` | flag | pilot | `02_financials/financial_model.xlsx` | redflags-mislabels-001 |
| `billings_vs_recognised_revenue` | cannot_check | not_checked | `03_metrics/customer_mrr_by_month.csv` | none |
| `gross_vs_net_revenue` | cannot_check | not_checked | `03_metrics/customer_mrr_by_month.csv` | none |
| `contractor_spend_vs_headcount_and_burn` | cannot_check | not_checked | `02_financials/expense_ledger.csv` | none |
| `capitalised_spend_vs_pnl_and_cash` | cannot_check | not_checked | `02_financials/expense_ledger.csv` | none |
| `deferred_revenue_vs_earned` | cannot_check | not_checked | `03_metrics/customer_mrr_by_month.csv` | none |
| `one_time_fees_in_recurring_metrics` | clear | nothing_found | `02_financials/financial_model.xlsx` | redflags-mislabels-002 |

Kind a still runs here, through entry 1.12's fallback: the model's `ARR_Build` Product type column and its monthly history. Kind h runs from the P&L fee row and `ARR_Build`. The other five return `cannot_check` with their gaps:

- Not in the room: a revenue export by product type (why: file missing; would need: monthly revenue by customer with a product type column (customer_mrr_by_month.csv); piece: traction_and_revenue)
- Not in the room: an invoices or billings export (why: file missing; would need: monthly invoices or billings by customer; piece: traction_and_revenue)
- Not in the room: a revenue export that separates pass-through money (why: file missing; would need: a revenue export with a pass-through or resale column, and the ledger lines paid on at cost; piece: traction_and_revenue)
- Not in the room: an expense ledger (why: file missing; would need: the expense ledger with vendor, description and amount; piece: burn_and_runway)
- Not in the room: an expense ledger (why: file missing; would need: the expense ledger with booked_as and category; piece: burn_and_runway)
- Not in the room: a balance sheet with a deferred revenue line (why: file missing; would need: monthly balance sheets, or invoices and revenue by customer; piece: traction_and_revenue)

The seed drop's kind a claim:

```json
[
  {
    "id": "redflags-mislabels-001",
    "scan": "redflags",
    "text": "monthly_metrics.csv shows MRR of $186,739 for 2026-09. The model's ARR_Build shows subscription MRR of $171,739. The $15,000 difference is 8.7% of subscription MRR and equals the non-subscription lines: Marlow Veterinary Group (pilot) (Pilot, $15,000). Months over tolerance: 2026-08, 2026-09.",
    "value": {
      "number": 171739.0,
      "unit": "USD_per_month",
      "label": "mrr",
      "period": "2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "mrr_column_vs_subscription_rows",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "03_metrics/monthly_metrics.csv",
        "locator": "row 22",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,186739,2240868,212,357,72149",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!A13",
        "start_s": null,
        "end_s": null,
        "quote": "Marlow Veterinary Group (pilot)",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!B13",
        "start_s": null,
        "end_s": null,
        "quote": "Pilot",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "ARR_Build!C39",
        "start_s": null,
        "end_s": null,
        "quote": "171739",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  }
]
```

## Clean room: data_room/hollis_voice_clean

Entry label: **clear**. No sub-check fires.

| Sub-check | Label | Really is | File read | Claim ids |
|---|---|---|---|---|
| `mrr_column_vs_subscription_rows` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-001 |
| `billings_vs_recognised_revenue` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-002 |
| `gross_vs_net_revenue` | not_run | not_checked | `03_metrics/customer_mrr_by_month.csv` | none |
| `contractor_spend_vs_headcount_and_burn` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-003 |
| `capitalised_spend_vs_pnl_and_cash` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-004 |
| `deferred_revenue_vs_earned` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-005 |
| `one_time_fees_in_recurring_metrics` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-006 |

## Kind c on a test room with a resale line

Hollis Voice has nothing for kind c. The spike writes two copies of the full room under `spike/test_rooms/`. With the option on, every paying subscription clinic gets a `Resale` row from 2026-04 (carrier minutes resold at cost, $25 a location a month, a spike choice), and the same money is added to the `mrr` column. With the option off, the copy is unchanged.

Option off:

| Sub-check | Label | Really is | File read | Claim ids |
|---|---|---|---|---|
| `mrr_column_vs_subscription_rows` | flag | pilot | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-001 |
| `billings_vs_recognised_revenue` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-002 |
| `gross_vs_net_revenue` | not_run | not_checked | `03_metrics/customer_mrr_by_month.csv` | none |
| `contractor_spend_vs_headcount_and_burn` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-003 |
| `capitalised_spend_vs_pnl_and_cash` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-004 |
| `deferred_revenue_vs_earned` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-005 |
| `one_time_fees_in_recurring_metrics` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-006 |

Option on:

| Sub-check | Label | Really is | File read | Claim ids |
|---|---|---|---|---|
| `mrr_column_vs_subscription_rows` | flag | pilot | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-001 |
| `billings_vs_recognised_revenue` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-002 |
| `gross_vs_net_revenue` | flag | pass_through | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-003 |
| `contractor_spend_vs_headcount_and_burn` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-004 |
| `capitalised_spend_vs_pnl_and_cash` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-005 |
| `deferred_revenue_vs_earned` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-006 |
| `one_time_fees_in_recurring_metrics` | clear | nothing_found | `03_metrics/customer_mrr_by_month.csv` | redflags-mislabels-007 |

```json
[
  {
    "id": "redflags-mislabels-003",
    "scan": "redflags",
    "text": "metrics \"mrr\" for 2026-09 equals the gross amount ($193,964), including $7,225 passed on (product type Resale). Over the 12 months to 2026-09, $36,825 of pass-through money sits inside $1,386,023 of monthly_metrics.csv mrr, 2.7%. Net of it: $1,349,198.",
    "value": {
      "number": 1349198.0,
      "unit": "USD",
      "label": "other",
      "period": "2025-10 to 2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "gross_vs_net_revenue",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "03_metrics/monthly_metrics.csv",
        "locator": "row 22",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,193964,2327568,212,357,72149",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "03_metrics/customer_mrr_by_month.csv",
        "locator": "row 2745",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,C0001,Pinecrest Corner Animal Hospital,1,Standard,Resale,25,0,25",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  }
]
```

## Brasswick: data_room/brasswick

Brasswick is the second demo room. Its answer key already names three 1.12 check names (BF1, BF3, BF4). The spike reads it through a column map (`subscription_revenue` for `mrr`, no product type).

Entry label: **flag**.

| Sub-check | Label | Really is | File read | Claim ids |
|---|---|---|---|---|
| `mrr_column_vs_subscription_rows` | not_run | not_checked | `03_metrics/monthly_metrics.csv` | none |
| `billings_vs_recognised_revenue` | flag | billings | `03_metrics/revenue_by_customer.csv` | redflags-mislabels-001 |
| `gross_vs_net_revenue` | flag | pass_through | `03_metrics/revenue_by_customer.csv` | redflags-mislabels-002 |
| `contractor_spend_vs_headcount_and_burn` | flag | contractor_spend | `02_financials/expense_ledger.csv` | redflags-mislabels-003 |
| `capitalised_spend_vs_pnl_and_cash` | clear | nothing_found | `02_financials/expense_ledger.csv` | redflags-mislabels-004 |
| `deferred_revenue_vs_earned` | flag | deferred_revenue | `03_metrics/revenue_by_customer.csv` | redflags-mislabels-005, redflags-mislabels-006 |
| `one_time_fees_in_recurring_metrics` | not_run | not_checked | `03_metrics/revenue_by_customer.csv` | none |

```json
[
  {
    "id": "redflags-mislabels-001",
    "scan": "redflags",
    "text": "The P&L row \"Subscription revenue\" for 2026-09 is $84,810. Subscription billings in revenue_by_customer.csv add to $82,650 and subscription revenue adds to $59,565. The P&L figure sits on the billings side.",
    "value": {
      "number": 59565.0,
      "unit": "USD",
      "label": "other",
      "period": "2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "billings_vs_recognised_revenue",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!S7",
        "start_s": null,
        "end_s": null,
        "quote": "84810",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-002",
    "scan": "redflags",
    "text": "P&L \"Recovery revenue\", metrics \"recovery_revenue\" for 2026-09 equals the gross amount ($35,387.73), including $24,771.41 passed on (column remitted_to_customer). Over the 12 months to 2026-09, $264,214.66 of pass-through money sits inside $943,339.50 of P&L Total revenue, 28.0%. Net of it: $679,124.84. The ledger shows $264,214.66 paid on in the same months.",
    "value": {
      "number": 679124.84,
      "unit": "USD",
      "label": "other",
      "period": "2025-10 to 2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "gross_vs_net_revenue",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!S8",
        "start_s": null,
        "end_s": null,
        "quote": "35387.73",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "03_metrics/monthly_metrics.csv",
        "locator": "row 18",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,120197.73,84810,35387.73,14,75337,799114",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "03_metrics/revenue_by_customer.csv",
        "locator": "row 128",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,C1001,Corvane Logistics,Network,11850,11850,16626,4916.02,1474.81,3441.21",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/expense_ledger.csv",
        "locator": "row 424",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,2026-09-12,Tessmore Freight,Remittance of carrier refunds recovered for the customer,recovery_remittance,Cost of revenue,898.85",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-003",
    "scan": "redflags",
    "text": "Contractor lines in the ledger add to $34,708.97 in 2026-09 (3 lines from Fernway Contractor Payments, Norrgate Software Studio). They sit in the P&L row \"Professional services\", $36,149.98 in 2026-09. The plan puts $2,800 on that row from 2026-10, which leaves $33,349.98 a month of the contractors out of the plan's burn. The staff count is 7 (Team!B12).",
    "value": {
      "number": 34708.97,
      "unit": "USD_per_month",
      "label": "payroll_monthly",
      "period": "2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "contractor_spend_vs_headcount_and_burn",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!S23",
        "start_s": null,
        "end_s": null,
        "quote": "36149.98",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!T23",
        "start_s": null,
        "end_s": null,
        "quote": "2800",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/expense_ledger.csv",
        "locator": "row 421",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,2026-09-05,Norrgate Software Studio,\"Contract engineering, SOW 2, September 2026\",professional_services,G&A,26500.00",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/expense_ledger.csv",
        "locator": "row 445",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,2026-09-27,Fernway Contractor Payments,\"Contractor payout: invoice labelling, T. Brennan\",professional_services,G&A,3875.71",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/expense_ledger.csv",
        "locator": "row 446",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,2026-09-30,Fernway Contractor Payments,\"Contractor payout: invoice labelling, A. Kirwan\",professional_services,G&A,4333.26",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "Team!B12",
        "start_s": null,
        "end_s": null,
        "quote": "7",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  },
  {
    "id": "redflags-mislabels-005",
    "scan": "redflags",
    "text": "The P&L row \"Subscription revenue\" for 2026-09 is $84,810. Revenue earned in the customer file is $59,565. The $25,245 excess equals the unearned part of the invoices billed that month to Ostley Freight.",
    "value": {
      "number": 59565.0,
      "unit": "USD_per_month",
      "label": "mrr",
      "period": "2026-09"
    },
    "severity": "flag",
    "check": {
      "kind": "script",
      "name": "deferred_revenue_vs_earned",
      "model": null
    },
    "confidence": "computed",
    "sources": [
      {
        "kind": "file",
        "uri": "02_financials/financial_model.xlsx",
        "locator": "P&L!S7",
        "start_s": null,
        "end_s": null,
        "quote": "84810",
        "retrieved_at": "2026-10-22"
      },
      {
        "kind": "file",
        "uri": "03_metrics/revenue_by_customer.csv",
        "locator": "row 141",
        "start_s": null,
        "end_s": null,
        "quote": "2026-09,C1015,Ostley Freight,Lane,2295,27540,1512,0.00,0.00,0.00",
        "retrieved_at": "2026-10-22"
      }
    ],
    "conflicts_with": [],
    "corroborated_by": []
  }
]
```

Contractor vendors that entry 1.12's keyword list would miss: Norrgate Software Studio.
