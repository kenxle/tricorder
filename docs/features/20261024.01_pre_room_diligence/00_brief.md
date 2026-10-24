# Brief: diligence before the data room

For Benjamin and his agents. Written 2026-10-24 at 11:34 AM, from Ken's comment on the roadmap: "let's make a brief for this so benjamin can work on it".

## What we are building

Steps 1 and 2 of the [demo workflow](../../ongoing/diagrams/demo_workflow.md), Ken's framework for the whole build. Ken, 11:15 AM: "we want to start with a real list of YC spring 26 companies and kick off our due diligence. we run our own models and do internet reserach."

Today Tricorder starts from a data room. This adds the part before it: the associate picks a real company, Tricorder researches it from public sources, and a first readout exists before anyone asks the founder for a file.

## What the associate sees

1. **Start from a URL.** The associate feeds in a company by its URL, its website or its YC company page, in the browser. There is no list screen (Ken, 12:02 PM).
2. **Tricorder sets the company up** from the URL: name, website, founders, batch, matched against the saved YC Spring 2026 list. The associate can correct any field.
3. **The research runs on its own.** Each part fills in as it lands, and each fails alone:
   - **The outside world:** the company's website, Hacker News, the App Store, and its SEC Form D filings (rounds raised, amount sold).
   - **The founders:** a card per founder from GitHub, personal sites and talks.
   - **Comparable companies:** recent private rounds and public companies, each with why it is a fair comp.
   - **Market signals:** competitors' hiring, traffic, reviews, news and pricing, where the keys allow.
4. **The first readout.** What the outside world says, every claim with its source, and the gaps only a data room can fill.
5. **The gaps become the first data-room request.** They feed [room-requests](../../ongoing/roadmap/room-requests.md), which you also own, so the associate's first ask is drafted already.

## Build order for today

The demo freezes at 3:30 PM. Build in this order, so each step is usable before the next starts. Pieces you hand to Tirth come from this list.

1. **Company setup from a URL** ([company-setup](../../ongoing/roadmap/company-setup.md)). Resolve the URL against the saved list; set up the company and save it in the store.
2. **The free outside sources, cached** ([outside-in](../../ongoing/roadmap/outside-in.md), [cached-data](../../ongoing/roadmap/cached-data.md)). The website, Hacker News (Algolia API), Apple's Lookup API and SEC EDGAR need no paid key. Save every call under `cache/` and run offline from it.
3. **Founder cards** ([founder-profiles](../../ongoing/roadmap/founder-profiles.md)). GitHub first.
4. **Comps** ([comps](../../ongoing/roadmap/comps.md)), from the Form D files.
5. **Market signals** ([signals-readings](../../ongoing/roadmap/signals-readings.md), [market-signals](../../ongoing/roadmap/market-signals.md)), as far as the keys on the laptop allow.

## What already exists

- **The list:** 193 companies in [yc_spring_2026_companies.csv](../../reports/20261022.02_research/raw/demo_companies/yc_spring_2026_companies.csv), from YC's public directory by [demo_yc_batch.py](../../reports/20261022.02_research/demo_yc_batch.py).
- **Six companies researched already,** with their raw calls saved in [raw/demo_companies/](../../reports/20261022.02_research/raw/demo_companies/): EDGAR Form D filings, GitHub users and orgs, Hacker News items and App Store lookups for Ploy, Tasklet, Sazabi, TesterArmy, Minicor and Expanse. The ranking and what each footprint shows: [research_demo_companies.md](../../reports/20261022.02_research/research_demo_companies.md). These can seed the cache.
- **The demo companies:** Ken has not picked yet. The research recommends Ploy and Sazabi; build for any company on the list and use those two until Ken says otherwise.
- **In the code:** the Claim schema (`schema/claim.py`), the quote checker that finds each quote again in its source, the readout store (`store/`), the server (`server/`), the readout page (`readout/`), and the scan interface every scan follows ([ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md)).
- **The detail for each piece:** the slice files linked above. Outside-in's is long: it covers resolving the right company, every tab's sources, limits, claims, gaps and what each must never do. Read it before building a tab.

## Rules that hold

- Every claim carries its source, and the quote checker finds it again in the saved copy, through `cache/index.json`.
- Official APIs only. LinkedIn is never fetched. reddit.com is never fetched. X is linked, not read.
- Keys come from the environment (`.env.example` lists them). A missing key makes that source a gap that names the variable, never a failure.
- A 403 or an empty answer is "no signal", never zero.
- `TRICORDER_OFFLINE=1` reads only `cache/`, so the demo runs with the wifi off.
- The real companies' data rooms are synthetic ([yc-rooms](../../ongoing/roadmap/yc-rooms.md)), and every page says so. Their outside research is real.

## Done when

- The associate feeds in Ploy's URL, and its first readout appears with outside-world claims and founder cards, each claim with a source the quote checker passes.
- The same run works with the network off.
- The readout's gaps show as checked items in room-requests.
- Comps and market signals show what the keys allow; anything else shows as a gap that says why.

## Yours to decide

- Whether this is built in the TypeScript port or in Python first, then ported. The TypeScript port is yours too ([typescript-port](../../ongoing/roadmap/typescript-port.md)).
- How the list and the setup screen look.
- Which pieces go to Tirth.

Post on the [board](../../BULLETIN.md) when a piece lands, and when you change a shape another part reads.
