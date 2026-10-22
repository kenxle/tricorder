# Hollis Voice synthetic data room

**Every name, number, company and person in this folder is fictional.** Hollis Voice does not exist. Its clinics, founders, investors, vendors and figures are invented for the Tricorder demo at Deal Flow NYC 2026. Any match with a real company or person is by chance. Do not treat anything here as real.

## What this is

A fake startup data room for the Tricorder demo. The organisers ask teams to bring a synthetic room and never a real company's confidential data. This room has seven planted red flags, one variant, and three clean decoys. Tricorder should find the flags and leave the decoys alone.

## The fictional company

Hollis Voice, Inc. is a Brooklyn startup, founded in 2024, that sells an AI phone agent to independent veterinary clinics. The agent answers calls, books appointments and sends refill requests to staff. Data is as of 2026-09-30, with 21 months of history. The company is raising a $9,000,000 Series A at $45,000,000 pre-money. It earlier raised $2,000,000 in SAFEs on a $12,000,000 post-money cap. It has 17 staff and plans 24 hires. Under a good-looking deck it has real churn, one very large customer, and a gross margin that leaves out delivery costs.

## How to regenerate

```
python3 -m venv data_room/.venv
data_room/.venv/bin/pip install -r data_room/requirements.txt
data_room/.venv/bin/python data_room/generate.py
```

The seed is fixed (20261024). Each run writes the same CSV, PDF and Markdown bytes, and the same workbook bytes too. Files are overwritten in place and nothing is deleted. The script stops with an error if a key number drifts from the research (`docs/reports/20261022.02_research/data_room_design_numbers.py`).

## How to check

```
data_room/.venv/bin/python data_room/check.py
```

`check.py` reads the generated files back and checks each planted flag is where `answer_key.json` says, then rebuilds the true numbers from the raw files. It exits with a non-zero status on any miss.

## What is written

- `hollis_voice/` is the full Series A room, 16 files in six folders.
- `hollis_voice_seed_drop/` holds copies of the 11 files of the thin first tier. This is what a founder sends before a term sheet.
- `answer_key.json` lists every flag and decoy with its file and location, the shown value, the true value, the check that catches it, and which files a check needs. Do not point Tricorder at it.

## The files

| File | What it is | Seed drop |
|---|---|---|
| `00_welcome/cover_note_and_index.pdf` | Cover note and a numbered index of the room, with the tier of each file | yes |
| `01_overview/pitch_deck.pdf` | 14 slides. Slide 14 lists every number with its slide | yes |
| `01_overview/company_overview.pdf` | One-page overview: what, who, traction, ask | yes |
| `01_overview/pitch_video_script.md` | Two-minute script to read on a phone. It states a third ARR figure | yes |
| `02_financials/financial_model.xlsx` | Assumptions, P&L, ARR build, cohorts, hiring plan, cash and runway, with named cells | yes |
| `02_financials/cap_table.xlsx` | Fully diluted cap table, SAFE conversion and Series A. Clean | yes |
| `02_financials/expense_ledger.csv` | Expense lines by month with vendor and category | no |
| `03_metrics/monthly_metrics.csv` | MRR, ARR, paying accounts, accounts created (cumulative), calls | yes |
| `03_metrics/customer_mrr_by_month.csv` | One row per customer per month with plan, product type and MRR | no |
| `04_customers/order_form_cedar_pine.pdf` | Largest customer, 17 locations, 24-month term | no |
| `04_customers/pilot_agreement_marlow.pdf` | Six-month pilot, 30 days notice, no duty to convert | no |
| `04_customers/order_form_brookline_row.pdf` | Ordinary annual prepaid plan. Clean | no |
| `05_team/founder_bios.pdf` | Two founders and the senior team | yes |
| `05_team/hiring_plan.csv` | 24 planned hires with start dates and base pay | yes |
| `06_product/product_one_pager.pdf` | What it does, pricing, integrations | yes |
| `06_product/website_copy.md` | Home page and pricing copy | yes |

## Notes for whoever runs the demo

- The video file does not exist yet. Ken records it from `pitch_video_script.md`. The planted spoken figure is "about three million dollars" at 0:35.
- Founder GitHub handles are placeholders (`FOUNDER_GITHUB` in `generate.py`). Swap in the demo organisation's handle and rerun.
- Run a fresh web search for the name "Hollis Voice" before it appears on a public slide. Vendors already sell voice AI to veterinary clinics.
- The room gives cash only at 2026-09-30. It does not give a cash history, so it does not try to reconcile cash since the company began.
- The deck's market figures are labelled company estimates and are not planted flags.

## Packages

Python 3.13 with `openpyxl`, `xlsxwriter`, `reportlab`, `matplotlib` and `pdfplumber`. They are pinned in `requirements.txt` and installed into `data_room/.venv`, which is not committed.
