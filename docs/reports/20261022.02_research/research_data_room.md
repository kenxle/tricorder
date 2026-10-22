# R4: The data room, the red flags in it, and the one we will build

Written 2026-10-22 by the data-room researcher (R4) for the Tricorder hackathon plan. Counts in this file come from [data_room_tables.py](data_room_tables.py). The demo company's numbers come from [data_room_design_numbers.py](data_room_design_numbers.py) (seed 20261024). Pages I relied on are saved under `raw/data_room/`; the first line of each saved file is its URL.

## Summary

- **A data room is the shared folder a startup opens to investors after a good first meeting.** The deck sells; the room proves. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)
- **A seed room is thin.** Deck, one-pager, model, cap table, a few metrics, founder bios, incorporation papers and SAFEs. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups)
- **A Series A room adds the proof layer.** Monthly financial statements, cohort and retention exports, unit economics, top customer contracts, IP assignments, a 409A, board minutes and employment records. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Peony A](https://www.peony.ink/blog/series-a-data-room), [CRV](https://www.crv.com/content/what-is-a-data-room)
- **A first-pass reader goes to the cap table, the financial model, incorporation papers and IP assignments first.** With revenue in play, the monthly P&L and revenue by customer come next. [CRV](https://www.crv.com/content/what-is-a-data-room), [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/) The deck is read for its claims; that ordering is mine, and a16z lists the deck first. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)
- **Published lists back all seven red flags we plan to plant.** The one soft spot is burn against the hiring plan: nobody publishes it as a named flag, only the method to build the test. [Kruze cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/)
- **Proposed company: Hollis Voice** (placeholder name), an AI phone agent for independent veterinary clinics, raising a $9,000,000 Series A. Two alternates are in Part 3.
- **The room has 16 files.** 11 of them form a thin "seed drop" that the demo opens first. The other 5 are the Series A extras.
- **8 planted entries (7 flags plus one variant) and 3 clean decoys.** The seed drop alone can catch 5 entries; the full room catches the other 3.
- **A generator script in `data_room/` makes every file from one seeded simulation and writes an answer key.** Tests check each plant is found and each decoy is left alone.
- **Two tools are missing here.** `python-pptx` and LibreOffice are not installed, so the deck is built as a PDF directly and spreadsheet formulas need `xlsxwriter` to carry values. Details in Part 3.

---

## Part 1. What a data room is in practice

### 1.1 The definition

A data room is a collection of documents that helps investors get up to speed on a company. Its goal is to give them what they need to do diligence and, later, to write an investment memo for their partners. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)

It used to be a locked physical room of binders. Today it is a link to a folder with access controls and a log of who opened what. [CRV](https://www.crv.com/content/what-is-a-data-room)

The deck and the room do different jobs. The deck is a sales tool that gets the meeting. The room is a verification tool that gets the wire. [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)

Founders usually stage access in two tiers. The first tier holds the deck, metrics, a financial summary and a cap table summary, shared before a term sheet. The second tier holds full financials, contracts, IP assignments and minutes, shared after one. [Peony A](https://www.peony.ink/blog/series-a-data-room) [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)

Three places I looked had less than I hoped:

- **Carta.** Its data room documentation covers rooms that fund managers run for their own investors (access control, NDA gating, watermarks, view tracking). It does not list what a startup should put in a room. [Carta](https://support.carta.com/kb/guide/en/how-to-manage-vc-fundraising-data-rooms-MHvOEzfZwJ/Steps/3724875)
- **DocSend.** Its checklist posts were blocked when I fetched them (HTTP 403). The one DocSend page I read lists the features of a room and a short content checklist: P&L, balance sheet and cash flow, business model, incorporation papers, executive bios. [DocSend](https://www.docsend.com/blog/virtual-data-room-for-startups/)
- **Y Combinator.** YC's seed guide says not to spend long on diligence documents at seed. It names an executive summary and a deck as enough, and calls an investor who asks for heavy diligence or financials at seed a warning sign. [YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/) The "YC data room" lists I found are written by data room vendors, not by YC.

### 1.2 The documents, by stage

30 documents. Stage letters: **Y** put it in, **L** a lighter version or only if you have it, **N** leave it out at that stage, **-** my sources do not say. Most letters come from one vendor's checklist, [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/). A star on a letter means it comes from another source in the row. Where one row merges two of Visible's rows, I took the first row's letters. A dagger on the last column means part of that reading step is my inference, not something a source states.

Counts of Y: pre-seed 11, seed 17, Series A 28. Counts of N: pre-seed 10, seed 1, Series A 0.

| # | Document | Pre-seed | Seed | Series A | Who asks | What a first-pass reader does | Sources |
|---|---|---|---|---|---|---|---|
| 1 | Cover note and document index | Y | Y | Y | The founder volunteers it; investors reward it | Uses the index to find the cap table and model in seconds | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room) |
| 2 | Pitch deck | Y | Y | Y | Every investor; a16z lists it first | Treats each number as a claim and looks for the file that proves it | [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Peony A](https://www.peony.ink/blog/series-a-data-room), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 3 | One-page summary | Y | Y | Y | Every investor; YC says one or two pages is enough at seed | Reads stage, ask and traction | [YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 4 | Founder video or recorded intro | L | L | L | Partner, optional | Hears the founder state the numbers in their own voice (our use: compare with the deck) † | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 5 | Cap table, fully diluted | Y | Y | Y | Deal team and investor counsel; a16z lists it right after the deck; first on CRV's first-pass list | Checks that holders add to 100 percent, SAFEs are converted, and the option pool is shown | [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony A](https://www.peony.ink/blog/series-a-data-room) |
| 6 | Financial model, 3 to 5 years | Y | Y | Y | Deal team; a16z says detailed projections can wait for consumer seed; NFX says 24 months monthly plus 3 years annual | Reads it against the deck; at Series A an associate rebuilds it | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony A](https://www.peony.ink/blog/series-a-data-room), [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising) |
| 7 | Historical P&L, balance sheet, cash flow (monthly) | L | Y | Y | Deal team; Kruze lists three years of statements | Reads revenue lines, cost of revenue lines, payroll, and computes burn | [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 8 | Audited or reviewed financials | N | N | L | Series A lead, accountants | Compares reviewed numbers with management numbers | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 9 | KPI dashboard or metrics export (MRR, ARR, customers, churn) | L | Y | Y | Deal team | Compares each headline number with the deck and the definition used | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| 10 | Monthly revenue by customer | - | L* | Y* | BCV names it as one of two key items; Hustle and First Round also ask | Builds customer cohorts and concentration, and sets them against sales and marketing spend | [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/), [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) |
| 11 | Cohort or retention export | N | L | Y | Deal team; CRV lists cohort retention curves as proof | Rebuilds retention from raw data and checks the retention claim in the deck | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony A](https://www.peony.ink/blog/series-a-data-room) |
| 12 | Unit economics (CAC, LTV, payback) | N | L | Y | Deal team; a16z lists LTV/CAC and payback last of its five | Recomputes from spend and customer counts | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| 13 | Bank statements (3 to 12 months) | N | L | Y | Deal team before wiring; Papermark puts them at the pre-wire step of a seed | Checks that revenue in the deck reaches the bank | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups) |
| 14 | 409A valuation | N | L | Y | Investor counsel and Kruze's tax list | Files it; checks the date | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) |
| 15 | Customer contracts and order forms (top ten) | N | L | Y | Series A lead; Kruze asks for top ten invoices and contracts; Peony A adds anything above about $20,000 | Checks term, renewal and termination, and whether ARR rests on the paper † | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Peony A](https://www.peony.ink/blog/series-a-data-room), [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/) |
| 16 | Customer references and letters of intent | N | L | Y | Series A lead; First Round runs 5 to 15 diligence conversations | Calls them | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Peony A](https://www.peony.ink/blog/series-a-data-room), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) |
| 17 | Sales pipeline snapshot | N | L | Y | Deal team | Compares stage counts with the growth plan | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) |
| 18 | Incorporation documents and bylaws | Y | Y | Y | Investor counsel; Cooley section B | Confirms they exist and match the cap table | [Cooley](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room) |
| 19 | Prior financing: SAFEs, notes, term sheets | Y | Y | Y | Investor counsel; Cooley section C | Matches each instrument to a cap table row | [Cooley](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| 20 | IP and invention assignment agreements | L | Y | Y | Investor counsel; on CRV's first-pass list | Checks every founder and contractor signed | [CRV](https://www.crv.com/content/what-is-a-data-room), [Cooley](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 21 | Board and stockholder minutes | L | Y | Y | Investor counsel; Cooley section A; a16z does not pore over them unless it has a question | Skims for financing approvals | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| 22 | Founder bios | Y | Y | Y | Partner; a16z says it uses LinkedIn instead | Reads for founder-market fit | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| 23 | Key team bios and org chart | L | Y | Y | Partner | Checks that the people in the plan exist | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 24 | Hiring plan and future org | L | Y | Y | Deal team; Kruze asks for a three-year hiring plan | Multiplies hires by loaded cost and compares the result with the burn in the model † | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Kruze cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/) |
| 25 | Employment, advisory and option grant records | N | L | Y | Investor counsel; SeedLegals lists founder service agreements and key employment agreements | Matches grants to the cap table | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [SeedLegals](https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round) |
| 26 | Investor update archive | N | L | Y | Deal team; CRV recommends including them at seed | Reads the trend and compares earlier numbers with today's † | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room) |
| 27 | Product roadmap and demo | Y | Y | Y | Partner | Watches the demo; reads the roadmap against the use of funds | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| 28 | Market sizing and competitive landscape | Y | Y | Y | Partner; a16z says it does its own sizing | Skims; investors build their own | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| 29 | Tax returns (three years) | - | - | Y* | Investor accountants; Kruze says a professional investor will ask | Checks they were filed | [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) |
| 30 | Disclosure of claims, disputes and regulatory inquiries | Y* | Y* | Y* | Investor counsel; Cooley section D, Hustle's pre-seed baseline | Reads the list | [Cooley](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |

Cooley GO's request list is the lawyers' view. It runs by section: shareholder and board actions, charter documents, capital stock, legal and regulatory, intellectual property, management and employees, debt, other agreements, and miscellaneous (which holds audited and monthly financials and the business plan). [Cooley](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) Cooley also publishes a sample cap table in simple and pro forma form on the same page, which is a good model for ours.

### 1.3 What an associate opens first, and why

- **The first pass is short and goes through four things.** CRV says the deal team starts with the cap table, the financial model, the articles of incorporation and the IP assignment agreements. A hole in any one shows up before anyone opens the rest. [CRV](https://www.crv.com/content/what-is-a-data-room)
- **For a company with revenue, two files do most of the work.** The Bain Capital Ventures author says that when a company is pulled into a process earlier than planned, investors often cut the request down to the monthly P&L and monthly revenue by customer. From those two files the fund builds customer and revenue cohorts, then sets them against sales and marketing spend to read LTV/CAC. [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/)
- **The financials folder is the most opened.** Visible says the numbers either match the pitch or they do not, and any gap becomes the main topic of the diligence call. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) Visible sells investor-update software, so this is a vendor's observation from its own platform.
- **a16z's five items for a consumer-leaning room** are the deck, the cap table, the historical P&L and burn, usage data, and LTV/CAC with payback. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)
- **At Series A the associate rebuilds the numbers.** Peony says a lead builds their own model from your raw data, calls your top customers, and ties every claim in the deck to a source in the room. [Peony A](https://www.peony.ink/blog/series-a-data-room) Peony sells data rooms, so read it as a vendor's account.
- **At seed, much of diligence is conversation.** First Round says it runs 5 to 15 diligence conversations with people who can speak about the business or the founders. [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) Hustle Fund's angel guide says early-stage diligence rarely benefits from a five-year forecast treated as a promise or a perfectly polished room. [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)
- **The room is also read as a sign of how the founder runs the company.** The Bain Capital Ventures author says the quality of the financial materials tells you a lot about the team before you read a number. [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/) Ellty says an investor who cannot find the cap table in 30 seconds counts that as a red flag. [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)

What this means for the Tricorder scan order. Read the deck first and pull out its claims, because the claims are the list of things to check. Then go to the cap table, the model, the P&L and metrics, then revenue by customer and cohorts, then contracts and legal. Every claim gets tied to a file or flagged as unsupported.

### 1.4 Seed room versus Series A room

- **Seed is thin.** Papermark describes about 24 files in six folders (overview, team, product, traction, financials, legal) and says the checks that matter are metrics, cap table cleanliness and IP assignment. [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups) It is a vendor, and the list is its own, not YC's.
- **Seed asks for little proof.** Hustle Fund's seed additions are board and stockholder consents, an equity plan, monthly statements and revenue detail that reconcile to the traction claims, and cohort, retention, pipeline, unit economics and customer-concentration support. [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)
- **Series A changes the kind of room.** CRV says Series A scrutiny falls on monthly management accounts, actuals against plan, expense breakdowns by function, and about two years of detailed financials. It adds that cohort retention gets a hard look and customer reference calls turn formal. [CRV](https://www.crv.com/content/what-is-a-data-room)
- **The Series A list of new items**, drawing on Kruze's checklist: three years of monthly GAAP financials, three-year projections tied to a real model, a 409A, cohort and retention analysis, unit economics, top ten customer contracts and anything above about $20,000, IP chain of title, employment agreements, minutes and bank statements. [Peony A](https://www.peony.ink/blog/series-a-data-room) [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)
- **The bar for proof moves from presenting to verifying.** Peony's framing is that a seed room presents and a Series A room proves. [Peony A](https://www.peony.ink/blog/series-a-data-room)

### 1.5 Where the sources disagree

- **a16z says several common documents can wait**: org charts and bios (it uses LinkedIn), detailed three to five year projections, tax returns, legal documents, board minutes and market sizing, unless an investor asks. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) Visible and Kruze list many of the same items as expected. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) Tricorder should treat a missing document as a question for the partner, not as a flag by default.
- **Room size.** Papermark says about 24 files at accelerator seed. [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups) Ellty says 40 to 60 focused documents is better than 200, and that a bloated room makes investors suspicious. [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room)
- **Projection length.** Visible says three to five years. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) NFX says 24 months by month plus three years by year. [NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising)
- **Gross margin bands.** Covered under the gross margin flag in Part 2.

---

## Part 2. Red flags a first pass finds

The organisers name four: churn hidden in cohort charts, revenue counted as ARR when it is not recurring, burn that does not match the hiring plan, and numbers that disagree between the deck and the model. I add three that published lists treat as standard: customer concentration, gross margin that leaves out delivery costs, and a vanity metric shown as a real one. That is 7 flags in all.

The sources are venture firm posts, accountants and a few vendors. Where a source sells something I say so. Thresholds are folk numbers unless a source defines them, so a script should take them as settings.

### RF1. Churn hidden in cohort charts

What the published lists say:

- a16z separates gross churn from net churn and says net churn understates the loss because it blends in upsells. It also says cohort retention should start at 100 percent of the installed base. [a16z 16 metrics](https://a16z.com/16-startup-metrics/)
- a16z wants two trends in a cohort table: retention that levels off after 6 or 12 months, and newer cohorts doing better than older ones. [a16z 16 more](https://a16z.com/16-more-startup-metrics/)
- a16z's data room guide lists selectively presented metrics as a red flag and asks for the full data, not the best cohorts. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)
- The Bain Capital Ventures author says an artificially low base for net dollar retention never works, because investors take the raw customer file and rerun the numbers. [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/)
- Jason Lemkin says to split churn by customer segment, use case and contract size, and calls 88 percent gross retention at $13M ARR a red flag. [SaaStr GRR](https://www.saastr.com/dear-saastr-were-at-13m-arr-and-growing-but-our-grr-is-slipping-what-should-we-do/) He says below 80 percent signals churn that needs fixing before scaling. [SaaStr top 10](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)
- Christoph Janz (Point Nine) notes that in a cohort table churn is usually high in the first months and then settles, because people who never adopted the product are gone. [Janz on Chen](https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/) My reading: a cohort that drops the first-month leavers removes the steepest part of the curve.

How it shows up in the documents: The cohort chart shows net dollar retention, so upgrades cover lost customers; customers who leave in the first weeks are dropped from the cohort size; the newest cohorts are missing or the best cohorts are shown alone.

How a script catches it: Rebuild cohorts from the revenue-by-customer export. Compare each cohort's starting count with the count in the model's cohort tab. Compute gross retention (each customer's later MRR capped at its starting MRR) beside net retention. Compare both with the deck's number. Check the a16z test that newer cohorts do better than older ones.

What needs a model reading instead: Reading a footnote such as 'active after onboarding' and judging whether the exclusion is fair; reading a chart that exists only as an image in the deck.

### RF2. Revenue counted as ARR when it is not recurring

What the published lists say:

- a16z says ARR should exclude one-time fees, professional service fees and variable usage fees. Multiplying one month of all-in bookings by 12 is a common mistake. [a16z 16 metrics](https://a16z.com/16-startup-metrics/) [a16z 16 more](https://a16z.com/16-more-startup-metrics/)
- a16z says letters of intent and verbal agreements are neither revenue nor bookings. [a16z 16 metrics](https://a16z.com/16-startup-metrics/)
- Bessemer says ARR gives full credit for the annualized recurring contract and nets out non-recurring revenue. [Bessemer](https://www.bvp.com/atlas/scaling-to-100-million)
- Fortune reports that six VCs said founders count pilots, one-time deals or unactivated contracts as recurring, and that some 'booked ARR' sits on contracts the customer can leave at any time. One VC described a defense-tech startup claiming $325,000 of ARR that came from a two-week pilot. [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)
- Hustle Fund's angel checklist says to separate contracted revenue, recognized revenue, pipeline, pilots, letters of intent and verbal interest. [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)
- Lighter Capital defines MRR as revenue reliably earned each month from ongoing contracts and subscriptions. [Lighter MRR](https://www.lightercapital.com/blog/four-metrics-to-track-when-raising-capital-for-your-saas-company) It treats signed contracts that are not yet live as a separate metric, committed MRR. [Lighter CMRR](https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr)

How it shows up in the documents: ARR includes a pilot, one-time fees, professional services, or a signed contract that has not gone live; MRR is multiplied by 12 from an all-in month.

How a script catches it: Tag each line of the ARR build by product type using the revenue export (subscription, pilot, onboarding, services). Recompute ARR from subscription lines only. Flag any ARR line whose contract is under 12 months or can end on short notice.

What needs a model reading instead: Reading the contract: is a pilot, an evaluation or an opt-out clause present, and does the customer owe anything after the first term.

### RF3. Burn does not match the hiring plan

What the published lists say:

- I found no published list that names 'burn does not match the hiring plan' as a red flag. What exists is method, and our check is built from it. The organisers named this flag, so a partner clearly cares; the test below is ours.
- Kruze says headcount is often 60 to 80 percent of burn, so a forecast that does not model hiring clearly is a guess. It says to build a headcount grid, use fully loaded cost (a rule of thumb of 1.25 to 1.4 times base pay), and assume hires start a month or two later than hoped. [Kruze cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/)
- a16z defines net burn and gross burn. [a16z 16 metrics](https://a16z.com/16-startup-metrics/) Lemkin calls a burn multiple of 1 to 2 healthy. [SaaStr top 10](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)
- NFX says the raise should give at least 18 to 24 months of runway. [NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising)

How it shows up in the documents: The model's payroll line grows by a few hires while the hiring plan lists many more, or the plan's start dates are earlier than the model uses. The deck's runway comes from the lighter model.

How a script catches it: Build monthly payroll from the hiring plan: base pay times a loaded-cost factor, from each start month. Compare it with the model's payroll line and the cash tab. Recompute runway from cash and net burn. Compare it with the deck.

What needs a model reading instead: Reading start dates or comp notes that sit in text (offer letters, assumptions notes); judging whether the loaded-cost factor is fair.

### RF4. Numbers disagree between the deck and the model

What the published lists say:

- a16z's data room guide gives this example of a red flag: the deck says $2M in ARR and the model shows $1.5M. It also flags numbers that differ across tabs and suggests one linked model. [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)
- CRV says burn or revenue that differs between the deck, the model and the accounting records reads as carelessness or something worse, and that deck ARR should reconcile to billing, contract and revenue schedules. [CRV](https://www.crv.com/content/what-is-a-data-room)
- Visible says a mismatch between dashboard numbers and deck numbers is one of the fastest ways to lose credibility. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)

How it shows up in the documents: The same ARR, customer count or margin appears with different values in the deck, the model, the metrics export and what the founder says on video.

How a script catches it: Pull labeled numbers from the deck's claims page and from named cells in the model and exports. Match by label and period. Flag any pair that differs by more than a set tolerance.

What needs a model reading instead: Matching 'customers' on a slide to 'logos' or 'paying accounts' in the model; spotting a different date or definition behind the same label; reading a number spoken on video.

### RF5. Customer concentration

What the published lists say:

- a16z defines customer concentration as the largest customers' revenue over total revenue for the same period, and names three risks: pricing power, roadmap pressure and below-market terms. [a16z 16 more](https://a16z.com/16-more-startup-metrics/) It gives no threshold.
- MicroVentures calls 20 percent a common rule of thumb and says 30 to 40 percent can change valuation or deal structure. It also says early concentration is not a red flag if the founders have a plan to spread it. [MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many) It is a crowdfunding platform, so treat the number as folk wisdom.
- Hustle Fund's checklist puts customer-concentration support in the seed-stage additions. [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)

How it shows up in the documents: One customer or one group of locations makes up a large share of MRR while the deck says the base is spread out.

How a script catches it: From revenue by customer: top-one and top-three share of MRR. Compare with the deck's claim. Flag when the computed share is above the deck claim, or above a set line (MicroVentures calls 20 percent a common rule of thumb; a16z gives the definition and no line, so the line is a setting).

What needs a model reading instead: Reading the big customer's contract for renewal date and termination rights, which decide how risky the share is.

### RF6. Gross margin leaves out hosting or support cost

What the published lists say:

- a16z says gross profit should include all costs of manufacturing, delivery and support, and founders should be ready to say what is in and out. [a16z 16 metrics](https://a16z.com/16-startup-metrics/)
- Tomasz Tunguz says cost of revenue includes web hosting, software licences embedded in the product, customer success work to onboard and retain customers, and professional services salaries. [Tunguz](https://tomtunguz.com/not-all-revenue-dollars-are-created-equal/)
- Stripe's guide lists hosting and infrastructure and customer support salaries and tools as cost of goods sold. [Stripe](https://stripe.com/en-se/resources/more/saas-gross-margin-explained-what-it-is-and-why-it-is-important)
- Benchmarks disagree. Bessemer reports an average of 65 to 70 percent with a middle half of 60 to 80. [Bessemer](https://www.bvp.com/atlas/scaling-to-100-million) a16z says software should sit at 80 to 90 percent. [a16z 16 more](https://a16z.com/16-more-startup-metrics/) So a benchmark is context for a reader, not a test for a script.

How it shows up in the documents: Cost of revenue holds only some delivery costs. Hosting, model inference and support staff sit under R&D or sales.

How a script catches it: Recompute gross margin with every ledger line tagged as hosting, inference, telephony, or support included. Compare with the deck. Use benchmarks as context only: Bessemer's average is 65 to 70 percent with a middle half of 60 to 80, while a16z says software should sit at 80 to 90.

What needs a model reading instead: Classifying ambiguous ledger lines such as 'platform costs' or 'customer experience salaries'.

### RF7. Vanity metric: cumulative sign-ups shown as active users

What the published lists say:

- a16z calls registered users a cumulative metric that can rise while a business shrinks, and prefers active users with a clear definition. [a16z 16 more](https://a16z.com/16-more-startup-metrics/)
- a16z calls downloads a vanity metric and says cumulative charts are not a valid measure of growth. [a16z 16 metrics](https://a16z.com/16-startup-metrics/)
- In a business-to-business product the equivalent is 'accounts created' or 'clinics signed up' shown as 'customers'.

How it shows up in the documents: A count that can only rise (accounts created, downloads, total users ever) is shown as active customers.

How a script catches it: Test whether the deck's number equals the last value of a cumulative column. Test the column for never decreasing. Compare with the active or paying count in the metrics export.

What needs a model reading instead: Reading a chart or label that does not say what 'users' means.

### Other published flags we will not plant

Each of these is real and in the sources, but we leave them out to keep the room small enough to demo. 9 in all.

- Cap table that does not reconcile (unconverted SAFE, undocumented grants) ([CRV](https://www.crv.com/content/what-is-a-data-room), [Peony A](https://www.peony.ink/blog/series-a-data-room))
- Missing IP assignments from founders or contractors ([CRV](https://www.crv.com/content/what-is-a-data-room), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups))
- Bookings counted as revenue; letters of intent counted as bookings ([a16z 16 metrics](https://a16z.com/16-startup-metrics/), [Hustle](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- Cherry-picked cohorts or periods; only a few months of history ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/))
- Blended CAC that hides weak paid channels ([a16z 16 metrics](https://a16z.com/16-startup-metrics/))
- Stale documents that disagree with current numbers ([CRV](https://www.crv.com/content/what-is-a-data-room), [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room))
- Customers who keep paying but use the product far less (stealth churn) ([SaaStr stealth churn](https://www.saastr.com/stealth-ai-churn-are-your-customers-starting-to-leave-already/))
- Tax returns not filed ([Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/))
- Truncated y-axis or cumulative chart used for a metric that should not be cumulative ([a16z 16 more](https://a16z.com/16-more-startup-metrics/), [a16z 16 metrics](https://a16z.com/16-startup-metrics/))

---

## Part 3. Our synthetic data room

### 3.1 Fictional company: three options

The organisers require a synthetic room: "Bring a synthetic data room; never upload a real company's confidential data." [Deal Flow problem tracks](https://docs.google.com/document/d/1S0ytTC-k1zLTvcoUjkRJy0JYuaNgYOWW9EQ04xN8SDA/edit) The judges' sectors come from [research_landscape.md](research_landscape.md), Part 3. One judge invests in enterprise and AI B2B software from pre-seed to Series A. Another sits at a pre-seed fund. Two build AI agents. One is a security engineer. B2B software with an AI core is the shared ground, so the options below sit there. The generator takes a different config if Ken prefers another space.

| Option | The company | Why the panel gets it in ten seconds | What it makes easy to plant | Watch out for |
|---|---|---|---|---|
| **A. Brasswick** | AI that matches freight invoices to loads for brokers and carriers | Plain B2B software with a clear return story | Concentration (one big broker), cohort churn, deck against model | Dry; less topical for an AI-agent panel |
| **B. Hollis Voice (recommended)** | AI phone agent for independent veterinary clinics | Most people know what a vet clinic is, and a voice agent is a product an AI panel knows | The pilot booked as ARR (a very current AI habit, per Fortune), gross margin that leaves out model inference, cumulative sign-ups as customers | A web search for the name shows vendors already selling voice AI to vet clinics; invented numbers must not look like theirs |
| **C. Stoopline** | Compliance software for New York building owners under the city's emissions law | Local to the room; real regulation | Pilots with building managers, concentration in one large management company | A web search shows vendors already selling software for the city's emissions law, and the judges may know them |

I searched the web for each name and found no company by that name. That does not prove none exists, so run a fresh search before the name appears on a slide. The AI-pilot habit that makes option B useful is described by Fortune. [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)

I recommend B because the pilot-as-ARR flag and the inference-cost margin flag are the two things an AI-literate panel will recognize at once. A is the safer fallback if Ken wants a plainer story.

### 3.2 Hollis Voice in numbers

Every figure below comes from [data_room_design_numbers.py](data_room_design_numbers.py), a design check that simulates the company once with a fixed seed. It is not the generator. The generator reuses its logic.

- **What it is.** An AI phone agent that answers calls for independent veterinary clinics, books appointments and sends refill requests to staff. Founded in 2024, based in Brooklyn. All names, clinics and people are invented.
- **Stage.** Series A. Data as of 2026-09-30, with 21 months of history (2025-01 to 2026-09).
- **The ask.** $9,000,000 at $45,000,000 pre-money ($54,000,000 post, so 16.67% to the new investors).
- **Earlier money.** $2,000,000 of SAFEs on a $12,000,000 post-money cap, which converts to 16.67% before the Series A.
- **Customers.** 250 accounts have ever paid; 212 pay now. Plans run from a few hundred to about a thousand dollars a month. One account, the largest, covers 17 locations.
- **Revenue.** True subscription MRR is $171,739 and true recurring ARR is $2,060,868.
- **People.** 17 staff today. The hiring plan adds 24, which takes it to 41.
- **Cash.** $1,800,000 at the data date.
- **Retention (true).** Twelve-month gross retention 73.4% and net retention 87.3% across the nine cohorts old enough to measure.

The company has a real churn problem, a real concentration problem and a real margin problem under a good-looking deck. That is the point of the room.

### 3.3 The files

16 files, in six folders that follow the stage-by-stage layouts the sources recommend. [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room) The "seed drop" is the thin first tier: the files a founder would send before a term sheet. The demo opens the seed drop first and the full room second.

| Path under `data_room/out/hollis_series_a/` | Format | What it is | In the seed drop |
|---|---|---|---|
| `00_welcome/cover_note_and_index.pdf` | PDF, 1 page | Cover note and a numbered index of the room. | yes |
| `01_overview/pitch_deck.pdf` | PDF, 14 slides | Deck with a claims page (slide 14) listing every number with its slide. | yes |
| `01_overview/company_overview.pdf` | PDF, 1 page | One-page company overview: what, who, traction, ask. | yes |
| `01_overview/pitch_video_script.md` | Markdown, about 300 words | Two-minute script for Ken to record on his phone; says an ARR figure that differs from the deck. | yes |
| `02_financials/financial_model.xlsx` | Excel | Tabs: README, Assumptions, P&L, ARR_Build, Cohorts, Hiring_Plan, Cash_Runway. | yes |
| `02_financials/cap_table.xlsx` | Excel | Fully diluted cap table with two SAFEs and an option pool; clean (decoy). | yes |
| `02_financials/expense_ledger.csv` | CSV | Expense lines by month with vendor and category; lets a checker recompute gross margin. | no |
| `03_metrics/monthly_metrics.csv` | CSV, 21 months | MRR, ARR, paying accounts, accounts created (cumulative), calls handled. | yes |
| `03_metrics/customer_mrr_by_month.csv` | CSV | One row per customer per month with plan, MRR and product_type. | no |
| `04_customers/order_form_cedar_pine.pdf` | PDF, 3 pages | Largest customer: 17 locations, 24-month term. | no |
| `04_customers/pilot_agreement_marlow.pdf` | PDF, 3 pages | Six-month pilot, 30 days notice to end, no duty to convert. | no |
| `04_customers/order_form_brookline_row.pdf` | PDF, 2 pages | Ordinary annual prepaid subscription (decoy). | no |
| `05_team/founder_bios.pdf` | PDF, 2 pages | Two invented founders and the senior team. | yes |
| `05_team/hiring_plan.csv` | CSV, 24 rows | Role, department, start month, base pay. | yes |
| `06_product/product_one_pager.pdf` | PDF, 1 page | What the product does, pricing tiers, integrations. | yes |
| `06_product/website_copy.md` | Markdown | Home page and pricing copy for the web scan. | yes |

Notes on the list:

- **The deck** is 14 slides: title, problem and product, where we are (ARR, clinics), customers, unit economics (margin, retention), cohort chart, pricing, market, competition, team, plan and use of funds (runway), hiring, the ask, and a claims page. Slide 14 is a table of every number with the slide where it first appears, so the memo can cite "deck, slide 3". The cohort chart is an image, so reading it needs vision; the same numbers sit on the claims page as text.
- **The model** has seven tabs and no checks tab. Named cells (`ARR_TOTAL`, `GM_PCT`, `RUNWAY_MONTHS`) let a checker find the number it needs and let the answer key point at them.
- **Two files are my additions** to the brief's list: `customer_mrr_by_month.csv` and `expense_ledger.csv`. Without them a script cannot rebuild cohorts, concentration or gross margin from raw data, and BCV's two key files include revenue by customer. [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/) Cut them if time is short; the flags that need them then rely on the model tabs alone and are weaker.
- **Contracts.** Three PDFs: the largest customer (17 locations, 24-month term), the pilot (six months, 30 days notice, no duty to convert), and an ordinary annual prepaid order form that is correct (a decoy).
- **No real people, companies or contact details.** Names come from word lists and a seeded Faker. Emails use `example.com`. Every page and sheet carries the footer "Synthetic data room for Deal Flow NYC 2026. Not a real company."
- **A board deck** appears in the full growth-stage request. [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/) I left it out; if added, it should carry a third version of the ARR figure.

### 3.4 What is planted

8 entries. Locations name the file, sheet, row label and named cell. The generator records exact cell addresses when it writes the cells (see 3.6).

**PF1. Pilot booked as ARR** (organiser direction: revenue counted as ARR when not recurring)

- Where: financial_model.xlsx / ARR_Build / row 'Marlow Veterinary Group (pilot)' and cell ARR_TOTAL; monthly_metrics.csv column arr (2026-09); pilot_agreement_marlow.pdf clauses 2, 7, 8
- True: Recurring ARR $2,060,868; the pilot contracts $90,000 of fees in total and can end on 30 days notice
- Shown: Model ARR $2,240,868, which counts the pilot as $180,000 a year
- Check that catches it: Recompute ARR from rows with product_type = Subscription in customer_mrr_by_month.csv and compare with ARR_TOTAL

**PF2. Deck ARR disagrees with the model** (organiser direction: numbers that disagree between the deck and the model)

- Where: pitch_deck.pdf slide 3 and claims slide 14; financial_model.xlsx cell ARR_TOTAL
- True: Model $2,240,868 (true recurring $2,060,868)
- Shown: Deck $2,500,000, a gap of $259,132 to the model
- Check that catches it: Match the deck claim labeled ARR to the named cell ARR_TOTAL; tolerance 1 percent

**PF2b. Video ARR disagrees with the deck** (organiser direction: numbers that disagree between the deck and the model)

- Where: pitch_video_script.md line at about 0:35 (and the recorded video, once Ken records it)
- True: Deck $2,500,000
- Shown: Spoken: about $3,000,000
- Check that catches it: Transcribe the video, extract the ARR sentence, compare with the claims page

**PF3. Churn hidden in the cohort tab** (organiser direction: churn hidden in cohort charts)

- Where: financial_model.xlsx / Cohorts (month-0 counts and the NRR row); pitch_deck.pdf slide 6 chart and claims row 'Net revenue retention'; note on the Cohorts tab: 'Cohort = customers still active after onboarding'
- True: 12-month net retention 87.3%, gross retention 73.4%, 68 customers in the nine cohorts
- Shown: Net retention 102.6%, 57 customers (the 11 who left within two months are dropped)
- Check that catches it: Rebuild cohorts from customer_mrr_by_month.csv; compare month-0 counts and NRR; compute GRR

**PF4. Burn and runway do not match the hiring plan** (organiser direction: burn that does not match the hiring plan)

- Where: hiring_plan.csv (24 rows); financial_model.xlsx / P&L forecast row 'Payroll' and Cash_Runway; pitch_deck.pdf slide 11 and claims row 'Runway'
- True: 24 hires in the plan; runway 19 months; average net burn over the next 12 months $480,062 a month
- Shown: The model counts 8 hires; runway 37 months in the model; average burn $374,462 a month
- Check that catches it: Payroll from hiring_plan.csv times the load factor in Assumptions; rerun cash; compare with Cash_Runway and the deck

**PF5. Customer concentration** (organiser direction: an additional published flag)

- Where: customer_mrr_by_month.csv (customer C-BIG); order_form_cedar_pine.pdf; pitch_deck.pdf slide 4 and claims row 'Largest customer'
- True: Largest customer 21.0% of MRR; top three 22.2%
- Shown: Deck: no customer above 9% of ARR
- Check that catches it: Top-one and top-three share from customer_mrr_by_month.csv; compare with the deck claim

**PF6. Gross margin excludes hosting, inference and support** (organiser direction: an additional published flag)

- Where: financial_model.xlsx / P&L rows 'Cloud hosting and model inference' (under R&D) and 'Customer support specialists' (under S&M); expense_ledger.csv categories; pitch_deck.pdf slide 5 and claims row 'Gross margin'
- True: Gross margin 58.1% when delivery costs are included
- Shown: Deck and model: 80%
- Check that catches it: Sum ledger lines tagged hosting, inference, telephony, support into cost of revenue; recompute

**PF7. Cumulative sign-ups shown as active clinics** (organiser direction: an additional published flag)

- Where: monthly_metrics.csv column accounts_created_cumulative; pitch_deck.pdf slide 3 and claims row 'Clinics on Hollis'
- True: 212 paying accounts (column paying_accounts)
- Shown: Deck: 357 clinics, which is the last value of a column that never decreases
- Check that catches it: Monotonic test on each metrics column; match the deck number to the column's last value

The four ARR numbers a partner would see side by side:

| Source | ARR it states | Why it differs |
|---|---|---|
| True recurring ARR (answer key only) | $2,060,868 | Subscription clinics only |
| Financial model, `ARR_Build` | $2,240,868 | Adds the pilot, annualized |
| Deck, slides 3 and 14 | $2,500,000 | Nothing in the room explains the extra $259,132 |
| Founder video | about $3,000,000 | A rounded, hopeful spoken figure |

Clean decoys. A checker that flags these is wrong, and the tests count that.

| ID | Clean item | Where | Why it is here |
|---|---|---|---|
| DC1 | Onboarding fee excluded from ARR correctly | financial_model.xlsx / ARR_Build row 'Onboarding fees (one-time, excluded)' | A checker must not flag the $500 fee as ARR |
| DC2 | Annual prepay counted as recurring correctly | order_form_brookline_row.pdf and customer row for Brookline Row Veterinary | Cash arrives up front, revenue is spread monthly, ARR counts it once; must not be flagged |
| DC3 | Clean cap table | cap_table.xlsx | Holders add to 100.00 percent and the SAFE conversion at the stated cap is right; must not be flagged |

Which entries each file set can catch:

| Planted entry | Files its check needs | Catchable from the seed drop |
|---|---|---|
| PF1 Pilot booked as ARR | `financial_model.xlsx`, `customer_mrr_by_month.csv`, `pilot_agreement_marlow.pdf` | no, needs the full room |
| PF2 Deck ARR disagrees with the model | `pitch_deck.pdf`, `financial_model.xlsx` | yes |
| PF2b Video ARR disagrees with the deck | `pitch_video_script.md`, `pitch_deck.pdf` | yes |
| PF3 Churn hidden in the cohort tab | `financial_model.xlsx`, `customer_mrr_by_month.csv`, `pitch_deck.pdf` | no, needs the full room |
| PF4 Burn and runway do not match the hiring plan | `hiring_plan.csv`, `financial_model.xlsx`, `pitch_deck.pdf` | yes |
| PF5 Customer concentration | `customer_mrr_by_month.csv`, `pitch_deck.pdf` | no, needs the full room |
| PF6 Gross margin excludes hosting, inference and support | `financial_model.xlsx`, `pitch_deck.pdf` | yes |
| PF7 Cumulative sign-ups shown as active clinics | `monthly_metrics.csv`, `pitch_deck.pdf` | yes |

### 3.5 Keeping it consistent

- **One simulation, one set of facts.** `facts.py` simulates customers, revenue, cohorts, costs and cash once. Every file reads from it. No file invents its own number.
- **Plants are explicit.** Each plant is one function. It takes a true fact, returns the shown value, and registers where it wrote it. Everything not planted is the true fact.
- **A clean room must pass.** With plants turned off (`--no-plants`) every reference check must report nothing. That test proves the room reconciles except where we choose.
- **Rounded claims are rounded on purpose.** The deck says "$2.5M", the model holds the exact figure, and the check uses a tolerance that the plant exceeds by a stated margin.
- **Dates and definitions.** All files use the as-of date 2026-09-30 and the same definition of ARR in the README tab of the model, so a difference is a plant, not a typo.

### 3.6 Generating it with scripts

What I found in this environment:

- **Installed:** `openpyxl`, `reportlab`, `faker`, `pandas`, `matplotlib`, `pdftotext`, `ffmpeg`, Python 3.13.
- **Not installed:** `python-pptx`, `xlsxwriter`, LibreOffice (`soffice`), WeasyPrint's native libraries.
- **So the deck is built straight to PDF with `reportlab`**, charts drawn with `matplotlib`. A PDF is what the scan reads anyway.
- **Formulas.** I tested it: `openpyxl` writes a formula with no stored result, so a reader that asks for values (`data_only=True`) gets `None`. Nothing here can recalculate without LibreOffice. `xlsxwriter` lets you write a formula together with its result (its `write_formula` takes a value argument, per its documentation; I have not run it here). Recommendation: `pip install xlsxwriter` for the model, and reload each workbook with `openpyxl` (`data_only=True`) in a test to prove the values are there. Fallback: write plain values and keep formulas in a documented column.
- **Reruns.** I tested both writers. `reportlab` with `invariant=1` gave identical PDF bytes on two runs two seconds apart. `openpyxl` workbooks differed in bytes even with fixed properties, because the zip entries carry the write time. So the determinism test compares CSV and PDF bytes, and compares workbook cell values.
- **The generator overwrites files in place and never deletes.** Files left over from an older run are listed for Ken's cleanup.

Proposed layout, at the repo root. The generator is data preparation the organisers ask for, not product code.

```
data_room/
  README.md              what this is, the synthetic notice, how to rerun
  generate.py            python3 data_room/generate.py [--seed 20261024] [--no-plants]
  requirements.txt       openpyxl, xlsxwriter, reportlab, matplotlib, faker, pandas
  src/
    facts.py             the one simulation; every number starts here
    plants.py            one function per planted flag; each registers its location
    tables.py            the CSV files
    workbook.py          financial model and cap table
    pdfs.py              deck, contracts, bios, overview, one-pager, cover note
    names.py             word lists and the Faker seed for invented people and clinics
    answer_key.py        collects locations, writes planted_flags.json
  tests/
    test_reconciles.py   plants off: the reference checks find nothing
    test_plants.py       plants on: each check finds its flag, and none finds a decoy
    test_determinism.py  same seed: same CSV and PDF bytes, same workbook cell values
  out/
    hollis_series_a/     the full room, in the folder tree of 3.3
    hollis_seed_drop/    copies of the thin first tier
  answer_key/
    planted_flags.json   never inside out/
```

**The answer key.** `answer_key/planted_flags.json` lives outside `out/` so Tricorder is never pointed at it. One entry per planted flag and decoy. The helper that writes a cell also registers its address, so a recorded address cannot drift from the file. The shape:

```json
{
  "seed": 20261024,
  "as_of": "2026-09-30",
  "flags": [
    {
      "id": "PF1",
      "name": "Pilot booked as ARR",
      "organiser_direction": "revenue counted as ARR when not recurring",
      "locations": [
        {"file": "02_financials/financial_model.xlsx", "sheet": "ARR_Build", "cell": "recorded at write time"},
        {"file": "04_customers/pilot_agreement_marlow.pdf", "page": 1, "clauses": [2, 7, 8]}
      ],
      "true": {"value": 2060868, "unit": "USD", "label": "recurring ARR"},
      "shown": {"value": 2240868, "unit": "USD", "label": "model ARR_TOTAL"},
      "check": "arr_from_subscription_rows",
      "tolerance": 0.01,
      "decoy": false
    }
  ],
  "decoys": [{"id": "DC1", "locations": [], "must_not_flag": true}]
}
```

The demo can score itself against the key: how many planted flags the readout found, and how many decoys it wrongly flagged. That score can go on a slide.

**Order of work.** No time estimates here; each step names what it waits on.

1. **Reference checks and tests first.** Write the plain-Python check for each entry in 3.4 and a failing test for it. Waits on: nothing. These checks double as the specification for the real scans.
2. **`facts.py`.** Promote [data_room_design_numbers.py](data_room_design_numbers.py) into the generator's source of truth. Waits on: step 1 only for the target values.
3. **Tables.** The three CSV files and the hiring plan. Waits on: facts.
4. **Workbooks.** Model and cap table. Waits on: tables, and Ken's call on `xlsxwriter`.
5. **PDFs.** Contracts, bios, overview, one-pager, cover note. Waits on: facts and the name lists.
6. **Deck.** Charts, then slides, then the claims page last. Waits on: workbooks, because the shown numbers come from the plants.
7. **Video script.** Beats below. Waits on: the deck's claims page.
8. **Answer key, determinism and clean-room tests.** Waits on: all of the above.
9. **Ken records the video** on his phone from the script. Waits on: step 7. Then the video scan transcribes it and the planted spoken figure is checked.

The video script, two minutes, about 300 words. The beats (times in seconds of video):

| At | Beat |
|---|---|
| 0:00 | Who we are and the problem: clinics miss calls |
| 0:20 | What the product does |
| 0:35 | Traction. Includes the planted sentence: "we're at about three million dollars in annual recurring revenue" |
| 0:50 | Clinics, retention, and the largest customer, all matching the deck |
| 1:10 | Why we win |
| 1:30 | Team |
| 1:45 | The ask and how long the money lasts |
| 1:55 | Close |

### 3.7 How the demo uses it

- **Open with the seed drop.** The panel's funds work at pre-seed to Series A, so the thin room is their home ground. The readout should catch the deck against model gap, the vanity clinic count, the gross margin problem and the runway against the hiring plan. That is 5 of the 8 entries. The script file stands in for the video until Ken records it.
- **Then add the rest of the room.** Pointing Tricorder at the full room should add the pilot as ARR, the hidden cohort churn and the customer concentration. That is the other 3, and it shows the "weeks of rebuilding numbers from a messy data room" claim from the organisers' problem statement in a few minutes.
- **The video line lands last.** The video scan compares the spoken figure with the deck.
- **Other tools claim these checks.** [research_landscape.md](research_landscape.md) lists Keye (cohort and margin checks on raw deal files), Termina (retention, churn, growth and top-customer share) and askRIA (data room analysis and red flags) on their own pages. The answer key lets Tricorder show a score instead of a claim.

---

## Open points

- **Pick the company.** I recommend Hollis Voice (option B). If Ken agrees, the name needs one fresh web search before it appears anywhere public.
- **`xlsxwriter`.** Installing it is a `pip install`. Without it, model formulas have no stored values. Say yes or no.
- **The video.** Ken records it. The script is written once the deck's claims page exists.
- **Whether the answer-key score goes on the demo.** I think it should; it turns "trust us" into a check the judges can see.
- **Is `data_room/` at the repo root "code before Saturday"?** The brief says no product code before Saturday and tells critics to weigh a repo skeleton. This is data preparation the organisers ask teams to do, so I treat it as allowed, but the overview page should say it.
- **Room stage.** The commission asked for a Series A room because it is the richest for diligence. The panel's funds mostly work at pre-seed to Series A, so the seed drop alone could carry the demo if five minutes is tight. The overview page can decide.

## Cleanup needed

I deleted nothing. Files that are empty, partial or duplicate, for Ken's cleanup pass:

- `raw/data_room/vccafe_com_p_9727.txt` (page text came back empty)
- `raw/data_room/adamantventures_substack_com_p_data_rooms_why_when_and_how_alsowhat.txt` (empty)
- `raw/data_room/community_carta_com_education_customer_journey_guides_fundraising_essentials.txt` (106 bytes, blocked)
- `raw/data_room/hustlefund_vc_post_angel_squad_due_diligence_what_actually_matters_and_what_doesnt.txt` (same page as the checklist file, different URL)
- `raw/data_room/bakertilly_com_insights_your_arr_is_probably_wrong_and_could_be_costing_you.txt` (partial; not relied on)

## Files written

- `research_data_room.md` (this file)
- `data_room_tables.py`, `data_room_design_numbers.py` and the outputs `data_room_documents.csv`, `data_room_flags.csv`, `data_room_planted.csv`, `data_room_files.csv`, `data_room_design_numbers.json`
- `raw/data_room/` with the saved pages and `fetch_pages.py`
