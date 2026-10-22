# Synthetic data rooms: Hollis Voice and Brasswick

**Every name, number, company and person in this folder is fictional.** Hollis Voice and Brasswick do not exist. Their customers, founders, investors, vendors and figures are invented for the Tricorder demo at Deal Flow NYC 2026. Any match with a real company or person is by chance. Do not treat anything here as real.

## What this is

Two fake startup data rooms for the Tricorder demo. The organisers ask teams to bring a synthetic room and never a real company's confidential data. Ken decided at 2:35 PM on 2026-10-22 to show two rooms, so the demo shows Tricorder on two different businesses at two stages.

| Company | Stage | Room | Red flags | Decoys | Green flags | Checks passed |
|---|---|---|---|---|---|---|
| Hollis Voice: an AI phone agent for vet clinics | Series A, raising $9,000,000 | `hollis_voice/` (17 files) and a 12-file seed drop | 8 | 3 | 3 | 276 |
| Brasswick: matches carrier invoices to loads for freight brokers | Seed, raising $3,000,000 | `brasswick/` (14 files, one tier) | 5 | 3 | 3 | 206 |

The two rooms plant different kinds of problems. Hollis Voice carries the organisers' four (a pilot counted as ARR, deck against model, churn hidden in cohorts, burn against the hiring plan) and three more. Brasswick carries four accounting mislabels Hollis Voice does not: recoveries counted at their gross amount, a deck chart that starts after a fall, contractors left out of burn, and an annual prepayment booked as one month's revenue. Its fifth is a spoken number in the pitch video, runway this time, where Hollis Voice's is ARR. The Brasswick section below has the details.

Tricorder should find the red flags, leave the decoys alone, and report the green flags as strengths.

For Hollis Voice the generator can also write two other rooms: a clean room with no flags, and a sealed variant room with a different seed and a flag list that only an outside person knows. They let the demo show Tricorder on a room the build team did not write the checks against. See `SEALING.md`.

# Hollis Voice, the Series A room

## The fictional company

Hollis Voice, Inc. is a Brooklyn startup, founded in 2024, that sells an AI phone agent to independent veterinary clinics. The agent answers calls, books appointments and sends refill requests to staff. Data is as of 2026-09-30, with 21 months of history. The company is raising a $9,000,000 Series A at $45,000,000 pre-money. It earlier raised $5,500,000 in two SAFE rounds: $2,000,000 in 2024 on a $12,000,000 post-money cap and $3,500,000 in 2025 on a $28,000,000 post-money cap. It has 17 staff and plans 24 hires. Under a good-looking deck it has real churn, one very large customer, and a gross margin that leaves out delivery costs.

The cash reconciles. Money raised, less the net loss before 2025 and the 21 monthly operating results, equals the $1,800,000 in the bank, to within a dollar. The `Cash_Bridge` sheet of the model shows the sum.

## How to regenerate

```
python3 -m venv data_room/.venv
data_room/.venv/bin/pip install -r data_room/requirements.txt
data_room/.venv/bin/python data_room/generate.py
data_room/.venv/bin/python data_room/generate.py --company brasswick
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
data_room/.venv/bin/python data_room/check.py --company brasswick
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

# Brasswick, the seed room

## The fictional company

Brasswick, Inc. is a Long Island City startup, founded in 2025, that sells software to freight brokers. It reads each carrier invoice, matches it to the load's rate confirmation, bill of lading and proof of delivery, and holds the invoices that do not match. On invoices a broker paid before it joined, Brasswick chases overbilled money back from carriers and keeps 30% of what it recovers. Data is as of 2026-09-30, with 17 months of history from its first paying month, 2025-05. It is raising a $3,000,000 seed round at $16,000,000 pre-money. It earlier raised $1,700,000 in three SAFEs. It has 7 employees and plans 7 hires. Fifteen brokers have paid it and fourteen still do.

The research's alternate list (`docs/reports/20261022.02_research/research_data_room.md`, 3.1) offered Brasswick and Stoopline. Brasswick was chosen because a web search showed vendors already selling software for the city emissions law Stoopline would serve, and the judges may know them.

## How to regenerate and check

```
data_room/.venv/bin/python data_room/generate.py --company brasswick
data_room/.venv/bin/python data_room/check.py --company brasswick
```

`brasswick_room.py` builds the room and `check_brasswick.py` checks it. `generate.py` and `check.py` hand off to them. `check.py` also picks the Brasswick checker on its own when the key's company is Brasswick. The seed is fixed (20261025). Two runs give the same bytes in all 15 outputs (the 14 room files and the key). `--plants` and `--seed` do not apply: Brasswick has one room with all five flags.

The script retries its noise streams until the revenue history has the planted shape, then stops with an error if any planted gap is too small to count or the cash does not bridge.

Last run: 206 checks passed, 0 failed. A key with five numbers deliberately changed failed exactly those five checks.

## The files

Brasswick is a seed company, so its room is one thin tier, the kind a founder sends before a first meeting. There is no separate seed drop.

| File | What it is |
|---|---|
| `00_welcome/cover_note_and_index.pdf` | Cover note and an index of the room |
| `01_overview/pitch_deck.pdf` | 12 slides. Slide 12 is an appendix of key metrics |
| `01_overview/claims.json` | The 16 rows of slide 12 as data |
| `01_overview/pitch_video_script.md` | Two-minute script, 295 words, plain enough to read flatly. Its runway figure disagrees with the deck |
| `02_financials/financial_model.xlsx` | Assumptions, P&L, revenue by broker, team, cash and runway, and the cash bridge, with named cells |
| `02_financials/cap_table.xlsx` | Three SAFEs converted at their caps and the seed round. Clean |
| `02_financials/expense_ledger.csv` | 449 dated payments: 13 vendors, and the remittances to brokers |
| `03_metrics/monthly_metrics.csv` | Total, subscription and recovery revenue, paying brokers, invoices audited (monthly and since launch) |
| `03_metrics/revenue_by_customer.csv` | 140 rows, one per broker per month: subscription revenue, billings, invoices audited, money recovered, Brasswick's fee and the broker's share |
| `04_contracts/msa_corvane_logistics.pdf` | The largest customer's agreement, with the recovery clause |
| `04_contracts/order_form_ostley_freight.pdf` | Annual plan, invoiced 2026-09-01 |
| `04_contracts/order_form_tessmore_freight.pdf` | Annual plan, invoiced 2026-02-01 |
| `04_contracts/sow_norrgate_software_studio.pdf` | Statement of work with the contract engineering studio |
| `05_team/founder_bios.pdf` | Two founders and two senior people |

## The red flags

| Id | What is wrong | Shown | True | Where |
|---|---|---|---|---|
| BF1 | Recoveries counted at their gross amount. The broker's 70% passes through Brasswick and is booked as revenue, then as cost | Revenue, last 12 months: $943,340 | $679,125 with the brokers' share taken out | Deck slides 4 and 12; P&L rows "Recovery revenue" and "Recoveries paid to customers"; the customer file's fee and remittance columns; the ledger's remittance lines; the agreement's section 4 |
| BF2 | The deck's revenue chart starts in 2026-01. The 8 months before it hold a peak of $84,090 in 2025-09, 28% above January 2026, when the first brokers' back-audits ran out | Chart from 2026-01, "Revenue grew every month in 2026." | History from 2025-05 | Deck slide 4; `monthly_metrics.csv` |
| BF3 | Contractors left out of burn. A studio and two labellers cost $34,709 in 2026-09, booked as professional services. The plan cuts that line to $2,800 of legal fees | Runway 29 months, burn $113,684 a month | Runway 23 months, burn $148,393 a month | Deck slide 10; model `Assumptions`, `P&L`, `Cash_Runway`; ledger; the statement of work (to 2027-06-30, 90 days notice) |
| BF4 | Ostley Freight's $27,540 annual invoice is booked as September revenue | MRR, September 2026: $84,810 | $59,565 earned | Deck slides 4 and 12; P&L; `Revenue_Build`; metrics; Ostley's order form; the cash bridge has no deferred revenue for it |
| BF5 | The video says "close to three years of runway" | 36 months, spoken | 29 months in the deck | `pitch_video_script.md` at 1:35; deck slide 12 |

BF1 and BF4 both raise the deck's revenue. Each flag's true value removes only its own error. With both removed, revenue for the last 12 months is $653,880.

## The decoys

- DC1: Tessmore Freight paid $25,920 a year in advance in 2026-02, the same kind of contract as Ostley's. It is booked the right way: one twelfth a month, with the four undelivered months ($8,640) on the cash bridge as deferred revenue.
- DC2: the fractional controller is paid as a contractor, and the plan keeps the $2,950 retainer every month. Only the engineers and labellers are left out.
- DC3: the deck gives 799,114 carrier invoices audited since launch, says so, and gives the September count beside it. The metrics column is named `since_launch` and is the running sum of the monthly column.

## The green flags

Each sits in a piece of the readout with no planted flag, and three different files state it the same way.

| Piece | Number | Where it agrees |
|---|---|---|
| the pitch itself | seed raise, $3,000,000 | deck slide 11, the cap table's new money, the model's `SEED_RAISE` |
| retention | 14 of 15 brokers still pay | deck slide 5, the customer file's 2026-09 rows, the model's `PAYING_BROKERS` |
| customers | the largest customer pays $11,850 a month, fixed | the signed agreement, the customer file in all 17 months, the model's `Revenue_Build` |

The deck also states the largest customer's share honestly: 20% of subscription revenue.

## The cash

Money raised ($1,700,000), less the loss before 2025-05 ($134,609) and the 17 monthly operating results ($932,713), plus Tessmore's undelivered months ($8,640), equals the $641,318 in the bank, to within $0.21. The ledger agrees: total spend less billings and recoveries collected equals the P&L loss less the deferred revenue.

## How the room avoids looking built

- Customer ids are C1001 to C1015 in start order. Fourteen different fees are paid in September 2026.
- Revenue rises and falls with real causes: back-audits spike and fade, one broker stops paying after 2025-11, one upgrades and one takes a price rise at its anniversary.
- Pay is by person, with a rise in January 2026 and part months for mid-month starts. Rent moves in two lease steps. No vendor is called "Various".
- The deck says Brasswick keeps 30% of recoveries. The flag is that the revenue figure still counts all of it, which is how founders usually present it.
- The cover note does not promise that every number ties. No file names a flag or anything from the Hollis Voice room.

Run a fresh web search for the name "Brasswick" before it appears on a public slide. The research found no company by that name, which does not prove none exists.

## Packages

Python 3.13 with `openpyxl`, `xlsxwriter`, `reportlab`, `matplotlib` and `pdfplumber`. Both rooms use the same packages. They are pinned in `requirements.txt` and installed into `data_room/.venv`, which is not committed.
