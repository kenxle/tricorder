# Proposed changes to FRAMEWORKS.md entry 1.12

This is a proposal for whoever keeps [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md). This agent does not edit `docs/ongoing/`. `scans/redflags/mislabels.py` already runs these tests, and `scans/redflags/tests/test_mislabels.py` pins them. Every figure below comes from that module's output on the rooms (see [00_progress.md](00_progress.md), "Work and evidence").

## 1. Kind e: a plan test, and vendor propagation

**Why.** Brasswick's BF3 contractors are inside the actual P&L. They are booked under "Professional services", so entry 1.12's tie test is clear in every month. They drop out only in the plan: the row is $36,149.98 in 2026-09 and $2,800 from 2026-10. Entry 1.12's keyword list also misses the studio. Its lines say "Contract engineering, SOW 1" or "Additional engineering hours", and none of them contains "contractor".

**Proposed text, added to the kind e formula block:**

```
contractor_vendors  = vendors with at least one ledger line whose vendor, description or category contains
                      "contractor", "consultant", "consulting", "freelance", "agency", "staffing",
                      "contract engineering", "statement of work" or "SOW"
contractor_lines    = every ledger line from a contractor vendor
holding_row         = the P&L row whose as-of actual equals the ledger sum of the contractor lines' categories
covered             = holding_row(first plan month) − ( holding_row(as-of) − contractor_spend(as-of) )
flag if covered < contractor_spend(as-of) × (1 − match_tolerance)         (contractors cut from the plan)
```

**Worked example to add, Brasswick:** the contractor lines add to $34,708.97 in 2026-09 (Norrgate Software Studio and Fernway Contractor Payments). They sit in "Professional services" at $36,149.98. The plan puts $2,800 on that row. Result: `flag`. The fractional controller's line (Abbotsford Finance Partners, DC2) has no contractor keyword. The plan also keeps its $2,950, so it stays clear either way.

**Change to "Inputs":** Brasswick's `02_financials/expense_ledger.csv` and its `P&L` plan columns.

## 2. Kind g: a bridge test

**Why.** Brasswick's model names a deferred revenue cell (`DEFERRED_REVENUE_USD`, `Cash_Bridge!B10`). The room's billings and revenue columns let a script rebuild the balance and compare the two.

**Proposed text, added to the kind g formula block:**

```
if the model names a deferred revenue cell:
    flag if | deferred(as-of) − that cell | ÷ deferred(as-of) > match_tolerance
    write it as severity "info" when a P&L test in this sub-check already flagged
```

**Why the info rule:** `Cash_Bridge!B10` is a location of Brasswick decoy DC1 (Tessmore Freight's prepay, booked correctly). `eval/score.py` counts any flag claim that cites a decoy location as a wrongly flagged decoy. The bridge comparison is right. The cause it points to, Ostley Freight's invoice, is already flagged by the P&L test.

**Worked example to add, Brasswick:** the rebuilt deferred balance is $33,885 across 2 customers at 2026-09. The bridge carries $8,640. The P&L test flags the $25,245 excess in September as Ostley Freight's unearned invoice. The bridge claim is info.

## 3. Kind c: Brasswick is the room to run it on

**Why.** Entry 1.12 says kind c "has nothing in the room to run on". That is true of Hollis Voice. Brasswick's BF1 is kind c, keyed to `gross_vs_net_revenue` in `data_room/answer_key_brasswick.json`.

**Proposed text, replacing the kind c Hollis Voice paragraph's last sentence:** "Brasswick is built around a pass-through: `revenue_by_customer.csv` has a `remitted_to_customer` column and the P&L counts recoveries gross. Over the 12 months to 2026-09, $264,214.66 of pass-through money sits inside $943,339.50 of P&L total revenue, 28.0%. Result: `flag`."

**Change to "How the readout scores it":** "Kind c is `not_run` on Hollis Voice and `flag` on Brasswick."

## 4. Kind a on the seed drop: say "the financial model"

**Why.** Entry 1.12's fallback says to read "the `Product type` column of `ARR_Build` in the model". Its scoring section says kinds a, d and h "still run from the model and the metrics file". A reader can take "the model" to mean a language model. It means the company's financial model workbook. The fallback reads cells, so its claims are `computed`, not `judged`, and it needs no API key.

**Proposed text:** in both places, replace "the model" with "the financial model workbook (`financial_model.xlsx`)".
