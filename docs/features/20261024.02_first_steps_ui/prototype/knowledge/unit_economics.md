# Unit economics: expert knowledge

Written by the Tricorder team from the [unit economics guide](../docs/reports/20261022.03_document_guides/unit-economics.md), the [historical financials guide](../docs/reports/20261022.03_document_guides/historical-financials.md), [research_data_room.md](../docs/reports/20261022.02_research/research_data_room.md) RF6 (gross margin leaves out hosting or support), and [FRAMEWORKS.md](../docs/ongoing/FRAMEWORKS.md) entries 1.7 (gross margin composition) and 1.9 (unit economics recompute). The public pages they quote are linked below. This is the team's reading of those sources, not an investor's own input.

This file gives the model an investor's lens on whether the company makes money on a customer after paying to win and serve them. Scripts remain the source of computed figures. Do not invent a benchmark that is not cited here.

## What an expert checks first

Gross margin feeds every other number here: payback, LTV and the ratio all multiply by it. Before reading any of them, establish:

- **What sits in cost of revenue.** a16z says "all costs associated with the manufacturing, delivery, and support of a product/service should be included" in gross profit ([16 Startup Metrics](https://a16z.com/16-startup-metrics/)). Tomasz Tunguz lists what that means for software: "This includes web hosting, software licensing fees for software embedded into the product like databases, and the customer success initiatives to on-board and retain customers." ([Tunguz](https://tomtunguz.com/not-all-revenue-dollars-are-created-equal/)) For an AI product, model inference is a delivery cost too (FRAMEWORKS.md 1.7).
- **Who pays the bills today.** Cloud credits, a free tier and support staff booked under sales can each make cost of revenue smaller than the real cost of serving customers.
- **What one customer pays.** Revenue per paying account from the customer file, beside the published plan prices. FRAMEWORKS.md 1.9 asks whether the two match.
- **How CAC, payback and LTV were built, if the deck states them.** A SaaStr write-up of a talk by Christoph Janz: "Make it clear how you’ve calculated your CACs." ([SaaStr write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)) These are the write-up's words, not Janz's own page.

## Rules

- **Rebuild gross margin with every delivery cost.** Hosting, model inference, telephony, licences built into the product and support staff go into cost of revenue, wherever the P&L placed them (FRAMEWORKS.md 1.7, `gross_margin_from_ledger`). Blake Koriath of High Alpha: "If your gross margins are this high for a SaaS company, you’re missing some costs that should be included in cost of goods sold (COGS)." ([High Alpha](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections)) A ledger line that could fit either way stays unclear, and the readout says how far it could move the margin.
- **Price cloud use as if no credits paid for it.** When cloud credits cover part of the bill, the P&L books less cost than serving customers really takes, and the margin drops when the credits run out. Show the margin twice: as booked, and with credit-covered usage at its full price. Say when the credits expire. This is the team's reading of the a16z definition above; no source in the repo speaks to credits directly. a16z heads its section on AI costs "Cloud infrastructure is a substantial – and sometimes hidden – cost for AI companies" ([The New Business of AI](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/)).
- **Find where the cost of free users sits.** Serving a free tier or free design partners costs money. A company may book it as cost of revenue or as marketing, and either can be fair if it says which. Booked in neither place, it flatters both the margin and CAC. This follows the guide's rule for support cost: counted once, never twice and never not at all (unit economics guide; FRAMEWORKS.md 1.9).
- **Count each cost once.** When support staff move into cost of revenue, take the same cost out of the sales and marketing spend used for CAC (FRAMEWORKS.md 1.9).
- **Measure payback on gross profit.** Tunguz: "It is amount of time a customer repays the cost of customer acquisition with gross profit dollars." ([Tunguz, 2020](https://www.tomtunguz.com/payback_period_2020/index.md))
- **Put every acquisition cost in CAC.** a16z: "One common problem with CAC metrics is failing to include all the costs incurred in user acquisition such as referral fees, credits, or discounts." ([16 Startup Metrics](https://a16z.com/16-startup-metrics/))
- **Prefer LTV from real months.** a16z: "Note, if you have only few months of data, the conservative way to measure LTV is to look at historical value to date." (same page)
- **Keep plans and usage apart.** Self-serve plans and enterprise contracts differ in price, cost to serve and payback, so split the numbers by plan. Keep usage overage out of the recurring base. a16z on ARR: "It should exclude one-time fees, professional service fees, and any variable usage fees." ([16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/))

## Benchmarks, with their context

- **Cloud software averages 65 to 70 percent gross margin in Bessemer's data**, with the middle half between about 60 and 80 percent ([Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million), paraphrased). Bessemer adds that Twilio ran near 50 percent for much of its life because it paid telecom carriers in cost of revenue.
- **a16z sets a higher line for pure software.** "Because of this magical property, software companies should have very high gross margins, in the 80%-90% range." ([16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/))
- **AI companies often run lower.** a16z: "Anecdotally, we have seen a surprisingly consistent pattern in the financial data of AI companies, with gross margins often in the 50-60% range – well below the 60-80%+ benchmark for comparable SaaS businesses." ([The New Business of AI](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/)) This is a 2020 observation. A margin far above it for an AI product is a reason to check what was left out.
- **Payback lines disagree.** Jason Lemkin: "Your customer acquisition cost (CAC) payback period should be 12 months or less." ([SaaStr](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)) That is one investor's line for SaaS at Series A. Bessemer sets targets by segment: under 12 months for SMB, under 18 for mid-market, under 24 for enterprise ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million)). The unit economics guide lists more, and none agree.
- **LTV to CAC of 3 or more.** Bessemer: "We recommend investing in customer acquisition when CLTV / CACs are 3x+" (same page). Tunguz warns: "But this figure is often meaningless for early stage startups." ([Tunguz, 2017](https://tomtunguz.com/challenge-of-cac-ltv/))

Tricorder shows all of these as context. The test is the deck's margin against the rebuilt one (FRAMEWORKS.md 1.7).

## Stage expectations

- **Seed:** lighter. Hustle Fund: "Compare customer acquisition cost (CAC), gross margin, payback, and lifetime value only when the data is mature enough to support them." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)) Tunguz: "In the early stages, payback period is a better metric to use." ([Tunguz, 2017](https://tomtunguz.com/challenge-of-cac-ltv/)) Gross margin is still checkable from the P&L, and credits matter most here, because a young company is most likely to be running on them.
- **Series A:** expected and rebuilt. Peony lists "A built financial/operating model with unit economics" with CAC, LTV and payback the associate can rebuild ([Peony](https://www.peony.ink/blog/series-a-data-room)). A ratio in the deck with no inputs in the room "invites investors to re-check everything else you’ve said." ([CRV](https://www.crv.com/content/what-is-a-data-room))

## What to ask

- The P&L and expense ledger with every hosting, inference, telephony, licence and support line, and the section each one sits in.
- The monthly cloud bill before credits, the credits applied, the balance left and the expiry date.
- How many free users and free design partners there are, what they cost to serve, and where that cost is booked.
- Monthly sales and marketing spend by line and channel, new paying customers by month and by source, and how the deck defines CAC, LTV and payback.
- Revenue per paying account by plan, with usage overage shown apart.

## Sources and boundaries

- Quotes from the guides were checked word for word against saved copies listed in the [unit economics guide](../docs/reports/20261022.03_document_guides/unit-economics.md) and [historical financials guide](../docs/reports/20261022.03_document_guides/historical-financials.md) ([raw copies](../docs/reports/20261022.03_document_guides/raw/unit-economics/)). The two a16z "New Business of AI" lines were checked against the live page on 2026-10-24; no saved copy is in the repo.
- The rules on credits and free users are the team's reading of the a16z cost definition, not a quoted rule.
- Vendors (Peony) and write-ups (SaaStr on Janz) are read as their views.
- The margin and payback lines are for SaaS and cloud software. Say so before applying them to a company outside that.
