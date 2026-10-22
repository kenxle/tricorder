# What a data room is

A data room is the folder of documents a startup shares with investors so they can check the pitch. The deck makes the claims; the data room holds the files that prove or disprove them. Tricorder reads one, so this page explains what is in it, who reads it and how, written from [the data-room research](research_data_room.md) with every claim linked to the page it came from.

## The short answer

- **It is a shared folder, not a room.** It used to be a locked physical room of binders. Today it is a link to a folder with access controls and a log of who opened what ([CRV](https://www.crv.com/content/what-is-a-data-room)).
- **The founder builds it; the investor reads it.** Its job is to get investors up to speed so they can do diligence and, later, write an investment memo for their partners ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)).
- **The deck gets the meeting; the room gets the wire.** The deck is a sales tool. The room is a verification tool ([Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)).

## When it shows up

A founder usually opens it in two tiers ([Peony](https://www.peony.ink/blog/series-a-data-room), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)):

1. **First tier, after the first meeting.** The deck, the key metrics, a financial summary and a cap table summary. This is what Track 2 means by "before a second meeting", and it is what Tricorder reads first.
2. **Second tier, closer to a term sheet.** The full financials, customer contracts, IP assignments and board minutes.

The size varies by stage. A vendor describes an accelerator seed room as about 24 files in six folders ([Papermark](https://www.papermark.com/blog/data-room-for-yc-startups)). Another says 40 to 60 focused documents beats 200, and that a bloated room makes investors suspicious ([Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)). Y Combinator's seed guide says an executive summary and a deck are enough at seed, and calls an investor who wants heavy financials at seed a warning sign ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/)).

## Where it lives

Mostly a shared Google Drive or Dropbox folder, or a link from a data-room product such as DocSend, Papermark or Peony, which add view tracking and access control. Carta's data rooms are a different thing: rooms fund managers run for their own investors ([Carta](https://support.carta.com/kb/guide/en/how-to-manage-vc-fundraising-data-rooms-MHvOEzfZwJ/Steps/3724875)). For Tricorder this matters for the inbox idea: a deck often arrives as a DocSend link that asks for the viewer's email, not as an attachment. The [architecture doc](../../ongoing/ARCHITECTURE.md) covers what that means.

## What is in it

The research built a table of 30 documents by stage from vendor checklists, fund guides and a law firm's request list ([research_data_room.md](research_data_room.md), section 1.2). By its count, 17 of the 30 are expected at seed and 28 at Series A. The ones that matter most for a first pass:

| Document | Seed | Series A | What a first-pass reader does with it |
|---|---|---|---|
| Pitch deck | yes | yes | Treats each number as a claim and looks for the file that proves it |
| Cap table | yes | yes | Checks holders add to 100 percent and every SAFE is on it |
| Financial model | yes | yes | Reads it against the deck; at Series A, rebuilds it |
| Monthly P&L, balance sheet, cash flow | yes | yes | Reads revenue, cost of revenue and payroll; computes burn |
| Metrics export (MRR, ARR, customers, churn) | yes | yes | Compares each headline number with the deck and its definition |
| Revenue by customer, by month | sometimes | yes | Builds cohorts and customer concentration |
| Cohort or retention export | sometimes | yes | Rebuilds retention from raw data |
| Customer contracts, top ten | sometimes | yes | Checks term and cancellation, and whether ARR rests on the paper |
| Hiring plan | yes | yes | Multiplies hires by cost and compares with the burn in the model |
| Incorporation papers, IP assignments | yes | yes | Confirms they exist and match the cap table |
| Founder and team bios | yes | yes | Reads for founder-market fit |

"Sometimes" is the research's "lighter version, or only if you have it". The full table, with sources on every row, is in [the research, section 1.2](research_data_room.md).

## How an associate reads it

- **The first pass is short.** CRV's deal team starts with four files: the cap table, the financial model, the articles of incorporation and the IP assignments. A hole in any one shows before anyone opens the rest ([CRV](https://www.crv.com/content/what-is-a-data-room)).
- **For a company with revenue, two files do most of the work.** A Bain Capital Ventures author says investors often cut the request to the monthly P&L and monthly revenue by customer, and build cohorts and unit economics from those two ([BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/)).
- **At Series A they rebuild the numbers.** A lead builds its own model from the raw data, calls top customers, and ties every deck claim to a file in the room ([Peony](https://www.peony.ink/blog/series-a-data-room)).
- **The room is read as a sign of how the founder runs the company.** An investor who cannot find the cap table in 30 seconds counts that against the founder ([Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)).

That reading order is what Tricorder automates: pull the deck's claims, tie each one to a file, rebuild the key numbers from the raw rows, and show which pieces of the company hold up.

## Our synthetic one

The organisers require a synthetic room ("Bring a synthetic data room; never upload a real company's confidential data", [the problem tracks](../20261022.01_hackathon_sources/problem_tracks.txt)). Ours is for Hollis Voice, an invented phone agent for vet clinics raising a Series A, laid out the way the research found real ones are ([data_room/README.md](../../../data_room/README.md)):

- `00_welcome`: the [cover note and index](../../../data_room/hollis_voice/00_welcome/cover_note_and_index.pdf)
- `01_overview`: the [pitch deck](../../../data_room/hollis_voice/01_overview/pitch_deck.pdf), the [company overview](../../../data_room/hollis_voice/01_overview/company_overview.pdf), the [pitch video script](../../../data_room/hollis_voice/01_overview/pitch_video_script.md)
- `02_financials`: the [financial model](../../../data_room/hollis_voice/02_financials/financial_model.xlsx), the [cap table](../../../data_room/hollis_voice/02_financials/cap_table.xlsx), the [expense ledger](../../../data_room/hollis_voice/02_financials/expense_ledger.csv)
- `03_metrics`: [monthly metrics](../../../data_room/hollis_voice/03_metrics/monthly_metrics.csv), [revenue by customer by month](../../../data_room/hollis_voice/03_metrics/customer_mrr_by_month.csv)
- `04_customers`: two order forms ([Cedar and Pine](../../../data_room/hollis_voice/04_customers/order_form_cedar_pine.pdf), [Brookline Row](../../../data_room/hollis_voice/04_customers/order_form_brookline_row.pdf)) and a [pilot agreement](../../../data_room/hollis_voice/04_customers/pilot_agreement_marlow.pdf)
- `05_team`: [founder bios](../../../data_room/hollis_voice/05_team/founder_bios.pdf), the [hiring plan](../../../data_room/hollis_voice/05_team/hiring_plan.csv)
- `06_product`: the [product one-pager](../../../data_room/hollis_voice/06_product/product_one_pager.pdf), the [website copy](../../../data_room/hollis_voice/06_product/website_copy.md)

The first tier (the seed drop) is the subset a founder would share after a first meeting. The second tier adds revenue by customer, the ledger and the contracts. Seven problems are planted across the files, each one a flag the research found investors look for, and three traps are planted that a careless check would wrongly flag.

## What to ask in your interviews

The public sources describe rooms from the vendor and fund side. Two things only an investor can tell you, added to [the interview sheet](interviews.md) as questions 6 and 7:

- How do rooms reach you today: a DocSend link, a Drive folder, attachments in the email?
- At what point in your process do you ask for one, and what do you open first?
