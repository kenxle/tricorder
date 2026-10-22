# Hollis Voice synthetic data room

**Every name, number, company and person in this folder is fictional.** Hollis Voice does not exist. Its clinics, founders, investors, vendors and figures are invented for the Tricorder demo at Deal Flow NYC 2026. Any match with a real company or person is by chance. Do not treat anything here as real.

## What this is

A fake startup data room for the Tricorder demo. The organisers ask teams to bring a synthetic room and never a real company's confidential data. The main room has eight planted red flags and three clean decoys. It also has three green flags: numbers that two different files state the same way. Tricorder should find the red flags, leave the decoys alone, and report the green flags as strengths.

The generator can also write two other rooms: a clean room with no flags, and a sealed variant room with a different seed and a flag list that only an outside person knows. They let the demo show Tricorder on a room the build team did not write the checks against. See `SEALING.md`.

## The fictional company

Hollis Voice, Inc. is a Brooklyn startup, founded in 2024, that sells an AI phone agent to independent veterinary clinics. The agent answers calls, books appointments and sends refill requests to staff. Data is as of 2026-09-30, with 21 months of history. The company is raising a $9,000,000 Series A at $45,000,000 pre-money. It earlier raised $5,500,000 in two SAFE rounds: $2,000,000 in 2024 on a $12,000,000 post-money cap and $3,500,000 in 2025 on a $28,000,000 post-money cap. It has 17 staff and plans 24 hires. Under a good-looking deck it has real churn, one very large customer, and a gross margin that leaves out delivery costs.

The cash reconciles. Money raised, less the net loss before 2025 and the 21 monthly operating results, equals the $1,800,000 in the bank, to within a dollar. The `Cash_Bridge` sheet of the model shows the sum.

## How to regenerate

```
python3 -m venv data_room/.venv
data_room/.venv/bin/pip install -r data_room/requirements.txt
data_room/.venv/bin/python data_room/generate.py
```

The seed is fixed (20261024). Each run writes the same CSV, PDF and Markdown bytes, and the same workbook bytes too. This was checked by hashing every output file after two runs of each room. Files are overwritten in place and nothing is deleted. The script stops with an error if a key number drifts from the research (`docs/reports/20261022.02_research/data_room_design_numbers.py`).

The price, cost and pay noise uses its own random streams, so the research's simulation is untouched. The script tries noise streams in order until the research's rounded retention and concentration numbers hold, and it nudges a few clinics' prices so September 2026 MRR is exactly $171,739.

## The three rooms

| Command | Writes | Key |
|---|---|---|
| `generate.py` | `hollis_voice/` and `hollis_voice_seed_drop/`, all eight flags | `answer_key.json` |
| `generate.py --plants off` | `hollis_voice_clean/` and `hollis_voice_clean_seed_drop/`, no flags | `answer_key_clean.json` |
| `generate.py --seed N --plants PF1,PF3,...` | `hollis_voice_variant/` and `hollis_voice_variant_seed_drop/`, a new seed and only the named flags | `answer_key_variant.json`, or the path given to `--key-out` |

Flag ids: PF1 (pilot counted as ARR), PF2 (deck ARR above the model), PF2b (spoken ARR above the deck), PF3 (churn hidden in cohorts), PF4 (burn and runway ignore the hiring plan), PF5 (customer concentration), PF6 (gross margin leaves out delivery costs), PF7 (sign-ups shown as active clinics).

- A flag that is off means the room is honest on that point. For example, with PF6 off the P&L puts hosting, model usage and support in cost of revenue, and the deck shows the true margin.
- The clean room keeps the three decoys. A correct scan reports no flags and does not flag the decoys.
- A variant seed can make a flag too small to count. The script then stops and says to try another seed. Of the first 24 whole numbers, 16 gave a valid room with all eight flags.
- The variant folders and `answer_key_variant.json` are in `.gitignore`. The variant folders currently in the repo came from a smoke test with seed 77. Do not use them for the blind demo, because the person who ran the smoke test knows the flags.

## How to check

```
data_room/.venv/bin/python data_room/check.py
data_room/.venv/bin/python data_room/check.py --room data_room/hollis_voice_clean --key data_room/answer_key_clean.json
data_room/.venv/bin/python data_room/check.py --room data_room/hollis_voice_variant --key <path to the sealed key>
```

`check.py` takes a room folder and a key. It reads the generated files back and checks each planted flag is where the key says it is, then rebuilds the true numbers from the raw files. For a flag the key does not list, it checks the room is honest on that point. It also checks that the cash reconciles and that the room does not look built to be caught. It exits with a non-zero status on any miss. Last run: 276 checks passed on the main room, 171 on the clean room and 211 on the seed 77 smoke-test variant (`--seed 77 --plants PF1,PF3,PF6`). It also checks the green flags and that the main room's eight red flags still show and mean the same numbers.

## What is written

- `hollis_voice/` is the full Series A room, 17 files in seven folders.
- `hollis_voice_seed_drop/` holds copies of the 12 files of the thin first tier (the 11 first-tier files plus `claims.json`). This is what a founder sends before a first meeting.
- `answer_key.json` lists every flag and decoy with its file and location, the shown value, the true value, the check that catches it, and which files a check needs. It also lists the green flags (`green_flags`). Do not point Tricorder at it.

## The files

| File | What it is | Seed drop |
|---|---|---|
| `00_welcome/cover_note_and_index.pdf` | Cover note and a numbered index of the room, with the tier of each file. The second tier is shared on request after a first meeting | yes |
| `01_overview/pitch_deck.pdf` | 14 slides. Slide 14 is an appendix of key metrics | yes |
| `01_overview/company_overview.pdf` | One-page overview: what, who, traction, ask | yes |
| `01_overview/pitch_video_script.md` | Two-minute script to read on a phone. It states a third ARR figure | yes |
| `01_overview/claims.json` | The 14 rows of slide 14 as data (label, value, slide), written from the same list. The fallback when PDF text extraction fails | yes |
| `02_financials/financial_model.xlsx` | Assumptions, P&L, ARR build, cohorts, hiring plan, cash and runway, the cash bridge, and the company's market estimate, with named cells | yes |
| `02_financials/cap_table.xlsx` | Fully diluted cap table, three SAFE conversions and the Series A. Clean | yes |
| `02_financials/expense_ledger.csv` | 408 dated expense lines from 13 vendors, with category and how each is booked | no |
| `03_metrics/monthly_metrics.csv` | MRR, ARR, paying accounts, accounts created (cumulative), calls | yes |
| `03_metrics/customer_mrr_by_month.csv` | 2,132 rows: one per customer per month with plan, product type, locations, revenue (`mrr`), one-time fee and cash invoiced (`billings`) | no |
| `04_customers/order_form_cedar_pine.pdf` | Largest customer, 40 locations, 24-month term | no |
| `04_customers/pilot_agreement_marlow.pdf` | Six-month pilot at 20 locations, 30 days notice, no duty to convert | no |
| `04_customers/order_form_brookline_row.pdf` | Annual prepaid plan at 10% off list. Clean | no |
| `05_team/founder_bios.pdf` | Two founders and the senior team | yes |
| `05_team/hiring_plan.csv` | 24 planned hires with start dates, base pay, and the staff count after each hire | yes |
| `06_product/product_one_pager.pdf` | What it does, pricing, integrations | yes |
| `06_product/website_copy.md` | Home page and pricing copy | yes |

## How the room avoids looking built

The demo critic listed tells that make a fake room look fake. The generator now handles these.

- Customer ids follow one pattern. The large customer and the pilot have ordinary ids in start-month order (the ids are in the key's `facts`).
- Clinics pay list price, a discount or an add-on price. In September 2026, 118 of the 211 ordinary subscription rows are at a price other than the plan's list price, there are 21 distinct prices, and some clinics have two or three locations. Annual payers get 10% off.
- The large customer pays $900 a location and the pilot $750, both below the Pro list price.
- Cost lines, pay and rent carry seeded noise. Gross margin runs from about 77% to 80% over the history. Pay is by person, with a raise in January 2026, so payroll does not rise by one fixed amount per hire. Rent moves in four lease steps.
- The ledger has dated lines from 13 vendors, with no "Various".
- Hiring plan salaries are not all multiples of 5,000, and start dates are not all the first of the month. Each pair of hires keeps its combined pay, so the planted runway and burn numbers hold.
- The cap table is not round. The share total is 14,424,000 and each SAFE converts at its own cap.
- Founder and senior team names are plainer, and only the CTO lists a GitHub handle.
- The deck has a logo and an example call.
- The cover note does not promise that every number ties.

Two tells are left as they are. Cohort retention still has 62 of 117 cells at exactly 100%, because that comes from the simulation the research numbers depend on. The hiring plan still has two hires a month, because the planted runway depends on the timing.

## The green flags

A green flag is a number two different files state the same way, within 1 percent, in a piece of the company that carries no planted red flag. The deck, overview, video and website count as one source, because they repeat each other. The answer key lists them under `green_flags`, each with its two or three file locations, and `check.py` reads every location back from the file.

| Piece | Number | Where it agrees |
|---|---|---|
| the pitch itself | Series A raise, $9,000,000 | deck slide 13, the cap table's "New money (USD)", the model's `SERIES_A_RAISE` (3 sources) |
| market | market size, $252,000,000 | deck slide 8 and the model's Market tab, `MARKET_TAM_USD` (2 sources). Both are the company's own estimate and say so |
| team | staff today, 17 | deck slide 10 and the model's `STAFF_NOW` (2 sources). Staff after hiring, 41, agrees between deck slide 12 and the last row of `hiring_plan.csv` |

Under the readout rule (`docs/ongoing/FRAMEWORKS.md`, "The readout") a piece with any planted flag reads weak. Five of the nine pieces hold a planted flag: traction and revenue (PF1, PF2, PF2b, PF7), retention (PF3), burn and runway (PF4), unit economics (PF6) and customers (PF5). Comps comes from outside the room. That leaves market as the only business piece that can read strong, so the room has one strong business piece, plus team and the pitch itself. Adding a corroborated number inside a flagged piece, such as CAC or calls handled per clinic, would not change its verdict, so none was added.

Why team reads strong, and what keeps it that way:

- The model states no staff total after the hires. It has no "Staff after these hires" row, and the P&L shows staff for actual months only. The model still pays for 8 of the 24 hires, which is the planted runway flag (PF4).
- Every name matches across the deck, bios, overview, video script and cap table, and each bio opens with the first name of the person it describes.
- No planned hire has the title of a person already on the team. The hire is "Director of Enterprise Sales", because Marguerite Dunleavy is the current Head of Sales.
- The cover note's index gives 40 locations for the Cedar & Pine order form, the same as the form.

## The decoys

- DC1: the $500 onboarding fee. The ARR_Build row is called "Onboarding fees", shows zero ARR, and the customer file carries Onboarding rows. A scan must not count the fee as ARR.
- DC2: Brookline Row pays $7,008 once a year, in advance, 10% under the $649 list price. The billings column shows the whole fee in 2026-06 and nothing after. Revenue is $584 a month, and ARR counts it once. A scan must not read the June billings as revenue.
- DC3: the cap table. The holders add to 100% and each SAFE converts correctly at its cap.

## Notes for whoever runs the demo

- The video file does not exist yet. Ken records it from `pitch_video_script.md`. The planted spoken figure is "about three million dollars" at 0:35.
- The CTO's GitHub handle is a placeholder (`FOUNDER_GITHUB` in `generate.py`). Swap in the demo organisation's handle and rerun.
- Run a fresh web search for the name "Hollis Voice" before it appears on a public slide. Vendors already sell voice AI to veterinary clinics.
- The deck's market figures are labelled company estimates and are not planted flags.
- The large customer and the pilot now have 40 and 20 locations. Earlier versions of the room said 17 and 4.

## Packages

Python 3.13 with `openpyxl`, `xlsxwriter`, `reportlab`, `matplotlib` and `pdfplumber`. They are pinned in `requirements.txt` and installed into `data_room/.venv`, which is not committed.
