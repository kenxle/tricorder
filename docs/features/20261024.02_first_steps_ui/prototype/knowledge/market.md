# Market: expert knowledge

Written by the Tricorder team from the [market sizing and competitive landscape guide](../docs/reports/20261022.03_document_guides/market-sizing-and-competitive-landscape.md), the [pitch deck guide](../docs/reports/20261022.03_document_guides/pitch-deck.md), and [FRAMEWORKS.md](../docs/ongoing/FRAMEWORKS.md) entries 5.6 (TAM, SAM and SOM, bottom-up), 1.5 (deck-against-model reconciliation) and "Piece verdicts". The public pages they quote are linked below. This is the team's reading of those sources, not an investor's own input.

This file gives the model an investor's lens on how big the market is and how the founder sized it. Scripts remain the source of computed figures. Do not invent a benchmark or a customer count that is not cited here.

## What an expert checks first

Investors size the market themselves. a16z: "Market sizing. We’ll do our own work sizing the market." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)) So the founder's figure is a test of how they think. Before reading it, establish:

- **How it was built.** A count of customers times a price, or a share of a large industry figure. CRV: "A top-down figure presented alone draws more skepticism than almost anything else on a market slide." ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size))
- **Who is counted, and from what source.** CRV: "Imprecision is fine, provided you can identify the customers counted and the price used." (same page)
- **Which price.** List price of one plan, an average across plans, or what paying customers pay today.
- **Whether the room's files agree.** The deck slide, the model's market tab and any memo should state the same count, price and total.

## Rules

- **Every market figure is a count times a price.** FRAMEWORKS.md 5.6 rebuilds TAM, SAM and SOM this way. A top-down figure is reported and labelled as top-down, and never used as the market size.
- **Use what a paying customer pays today.** FRAMEWORKS.md 5.6 sets the price as rebuilt recurring ARR divided by paying accounts. The guide's check `planning_acv_vs_observed_acv` compares the founder's price with that figure.
- **Treat the top plan's list price as a ceiling.** Most customers pay less than the top plan, and free users pay nothing. A count of every possible buyer times the top plan's price sizes the market as if every buyer chose the most expensive plan. Show that figure as the upper bound, then rebuild it with the price paying customers pay on average. This is the team's reading of CRV's rule on naming the price used.
- **Count only buyers the product can serve.** CRV: "Sizing the market as the entire industry when your product serves one segment of it." is one of its listed mistakes. And: "A tight market definition reads as research; a broad one reads as a guess." (same page) "Every team" or "every company" is the whole category. The reachable layer (SAM) is the buyers the product, channel and geography reach today.
- **Check the deck's own arithmetic and the model's.** Count times price should equal the stated total, and the deck and model should state the same count (FRAMEWORKS.md 1.5, `deck_claim_vs_named_cell`). a16z's standard example of a broken room: "Numbers that aren’t consistent with what’s in the deck. For example, your deck says $2M in ARR, but your model shows $1.5M." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)) The same holds for a market count. When the two differ, show both with their sources and give no reason.
- **The obtainable layer must fit the plan.** CRV: "Your obtainable market has to line up with the amount you're raising, the financial model and the hiring plan." ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size))
- **Two company files agreeing is still one estimate.** The deck and the model both come from the founder. Agreement shows consistency, not truth (FRAMEWORKS.md, "Piece verdicts" and 1.11).
- **Never use a count from memory.** With no cited count in the room, write the gap "Not in the room: a cited count of target customers" (FRAMEWORKS.md 5.6).

## Benchmarks, with their context

- **A billion dollars at seed is a fund's rule, not a test.** CRV: "The working threshold at most institutional funds moves into billion-dollar territory." ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size)) YC: "Total Available Market (TAM) >$1B if possible." ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/)) Whether a fund needs that size is the partner's call. It does not make a smaller figure wrong.
- **A defensible number beats a big one.** CRV: "At every one of these stages, we’ve seen a number you can defend do more for a founder than a big one." (same CRV page)
- **Overestimating is the common finding.** A fund partner who built his own diligence tool says the issue it raises most often is founders overestimating market size ([Tech.eu](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/), news, paraphrased).
- **No source gives a line for how far a deck may sit above the bottom-up figure.** Tricorder reports the ratio (`deck_gap`) and sets no pass mark.

## Stage expectations

- **Seed:** the logic is judged. CRV says seed funds look for billion-dollar territory, and that at pre-seed "Investors are buying your read on the market more than the market itself." ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size)) A missing market file is a gap, not a flag.
- **Series A:** the figure must square with revenue the company already earns. CRV: "The sizing also has to reconcile with recurring revenue you can already show". The price per customer in the market slide should match what paying customers pay in the customer file.

## What to ask

- The count of target customers, with its source and date.
- The price per customer used, and whether it is a list price, an average or what customers pay today.
- Revenue per paying account by plan, so the market can be rebuilt at the observed price.
- Why the deck and the model state different counts, when they do.
- The three nearest competitors by name.

## Sources and boundaries

- Every quote above was checked word for word against saved copies listed in the [market sizing guide](../docs/reports/20261022.03_document_guides/market-sizing-and-competitive-landscape.md) and the [pitch deck guide](../docs/reports/20261022.03_document_guides/pitch-deck.md).
- CRV is a fund writing for founders, so its rules are one fund's stated view. Tech.eu is news, paraphrased.
- The rule on the top plan's price is the team's reading, not a quoted rule.
- Whether the product wins in its market, and whether the market suits the fund, are for the operator and partner.
