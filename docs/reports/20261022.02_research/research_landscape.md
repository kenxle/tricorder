# The landscape for Tricorder

Written 2026-10-22 for the Deal Flow hackathon (Saturday 2026-10-24, Betaworks). Track 2, Diligence. Every page I relied on is saved under [raw/landscape/](raw/landscape/INDEX.md) so no one has to fetch it again. Every count and every computed price comes from a script beside this file: [landscape_counts.py](landscape_counts.py) (reads [landscape_labels.csv](landscape_labels.csv), writes [landscape_evidence.csv](landscape_evidence.csv)) and [landscape_price_math.py](landscape_price_math.py).

## Summary

- **The market gap.** The big data tools (Affinity, Harmonic, Specter, PitchBook, Crunchbase and the rest) tell you about a company from the outside. None of the 12 shows, on the pages I read, that it reads a startup's own deck, model or data room, hunts for red flags in the numbers, or drafts a memo. The new AI diligence tools do those things, but only 1 of the 12 shows market signals, and only 3 show comps. No tool I found puts the three things Track 2 names (market signals, comps, red flags in financials) in one readout.
- **"Every claim links to its source" is no longer empty ground.** Five of the 12 AI entrants say they do it (Wokelo, Keye, V7 Go, the Apify actor, the open source Diligent). These are vendor claims I could not test. A claim that "nobody links claims to sources" would be wrong. A claim that "the readout puts disagreements first and flags every gap instead of filling it" is narrower and has support (a hackathon entry, FirstSignal, already shows that approach, see Part 4).
- **Price is not an open gap at the low end.** Apify charges $12 per memo, Energent starts at $0 and $30 a month, two open source memo tools exist. The enterprise tools with data room reading (V7 Go, Keye, askRIA) all quote on request. What remains open is trust and completeness, which is my reading, not a finding.
- **Three sponsor tools most useful on Saturday.** Akta (signals, company data and news, one API key, and source metadata on every response). Crunchbase (comps and funding data through MCP, but see the terms warning below). The Nicrron gateway (one key for every model, with free repeat requests that make demo rehearsals cheap and repeatable). You.com and Tavily are close behind and both have free ways in.
- **What the judges will likely reward (my inference).** A working product on real inputs, claims with visible sources, and plain answers about where the data goes. A named buyer who pays was on this list, but Tricorder will not have one by Saturday; this is a demo (Ken, 2:57 PM). The demo says who would buy it, the fund, and how it would be priced, without claiming a customer. Details in Part 3.
- **Two judges I could not identify.** D. J. Patel and Arjun Padmajan have no public trace I could find. Roundtable (Padmajan's company, a sponsor) does not match any site I found. Ken or the orchestrator should ask the organisers.

### Needs action from Ken

These are things only a person can do (account sign-ups and questions). I did not create any account.

- [ ] Akta: the free sign-up at [playground.akta.pro/signup](https://playground.akta.pro/signup) says "Try for free", with a coupon field. The headcount, web traffic, job and review signals are not on the pay-as-you-go plan. They need the $50 a month Subscription or a coupon. Ask the sponsor for a hackathon coupon, or buy one month. (Details in Part 2.)
- [ ] Crunchbase: Pro has a free trial and includes MCP. Its own docs say apps built on the MCP server need a separate arrangement. Decide whether Tricorder uses it as a research aid only. (Part 2.)
- [ ] Ask the organisers on the Luma page: who is Roundtable and where are its docs; who is D. J. Patel (fund); is Abeera Saeed still at Plug and Play (her LinkedIn search title says another employer).
- [ ] Sign up for the free tiers the plan will use: Nicrron ($10 to start), You.com ($100 free credits), Tavily (1,000 free credits a month, or apply for 100,000 through its startup program).

One more thing I noticed: the Luma page says "9 hours of focused building", while its own schedule gives hacking from 10:30 AM to 4:30 PM. The brief says about six. Worth confirming on the day.

---

## Part 1: The market map

The columns use the organisers' own words from the week's instructions in the brief: "Who they sell to", "What they charge", "Where they fall short".

**How I wrote the "fall short" column.** I read each vendor's home, pricing and product pages. When I write that a page "shows no" feature, I mean the pages I saved do not mention it. That is weaker than "the product lacks it". The checks are in [landscape_evidence.csv](landscape_evidence.csv), one row per tool and capability.

### Whole-market summary

Counts below come from `python3 -I landscape_counts.py`.

| What the pages show | The 12 tools funds use today | The 12 AI entrants and fund-operations tools |
|---|---|---|
| Market signals (hiring, traffic, reviews, news) | 9 of 12 | 1 of 12 (Wokelo) |
| Comps (comparable companies or rounds) | 4 of 12 (Grata, Crunchbase, Tracxn, Carta data side) | 3 of 12 (V7 Go, Apify actor, Diligent) |
| Red flags in financials and metrics | 0 of 12 | 7 of 12 |
| Reads a deck, model or data room | 0 of 12 | 6 of 12 |
| Drafts a memo | 0 of 12 | 8 of 12 |
| Says output links to its source | 1 of 12 (CB Insights: cited chat answers) | 5 of 12 |

Two more results from the same script:

- No tool shows market signals, comps and financial red flags together. Zero of 24.
- Two tools show reading a data room, red flags, a memo and source links together: V7 Go (enterprise, quote on request) and the Apify "AI Dealflow Analysis" actor ($12 per analysis).

Where the whole market falls short on the three things Track 2 names:

- **Market signals.** The incumbents are strong here (hiring, headcount, traffic, news). The AI memo tools mostly are not. They write about the company from its documents plus a web search, and the pages do not show a competitor signal tracker.
- **Comps.** Only four incumbents show comps, and the pages describe them as competitor lists, public company multiples (Grata) or aggregate round benchmarks (Carta). None of the pages say why a comp is fair, which is what Track 2's second direction asks for.
- **Red flags in financials.** Only the new entrants show it, and they describe general checks (cohorts, margins, anomaly detection, cap table issues). None of the pages say the flag compares the deck against the model, which is the example Track 2 gives.
- **"Every claim links to its source."** Claimed by five entrants and by CB Insights for its chat answers. Not shown by the 11 other incumbents. Because these are marketing pages, treat it as "claimed", not "proven".

My reading (not a finding): the open ground is a single readout that joins signals, comps and flags, ranks claims that disagree first, and shows a gap as a gap. A buyer cares most about whether a partner can trust it on a first pass, and nothing on these pages lets me test that.

### A. Tools funds use for diligence and sourcing today

| Tool | What it does | Who they sell to | What they charge | Where they fall short |
|---|---|---|---|---|
| **Affinity** | Relationship CRM for deal teams. Captures email and calendar, scores warm paths, AI chat, notetaker, hosted MCP server. | VC, PE, private credit, corporate VC, banks, family offices, fund of funds, accelerators (its solutions menu). | $2,000, $2,300 or $2,700 per user per year on Essential, Scale and Advanced; Enterprise custom. [Pricing page](raw/landscape/affinity_pricing.txt). Vendr's median across firms is $49,758 a year, page last updated Feb 2026: [Vendr](raw/landscape/vendr_affinity.txt). | It manages relationships and pipeline. Data from PitchBook, Dealroom and Crunchbase comes only on Advanced. The pages show no reading of a startup's own documents, no comps and no red flags. The pricing page lists a "File Analyzer" without saying what it reads. |
| **Harmonic** | Startup and people database with an AI search agent (Scout), network mapping, API, MCP, bulk data. | VC, growth capital, corporate development, sales teams. | "Get pricing" only. [Pricing page](raw/landscape/harmonic_pricing.txt). Vendr's median is $36,000 a year from 3 purchases, range $25,500 to $92,200: [Vendr](raw/landscape/vendr_harmonic.txt). | Built to find companies. Vendr's description lists "AI diligence reports" in the console, but Harmonic's own pages show no data room reading, comps or memo. |
| **Specter** | Startup, people and investor database with live talent and interest signals, modeled revenue and valuation, agents, MCP, API. | Investors; its page cites 400+ firms. | "Get pricing". API has "200 free credits to start". [Pricing page](raw/landscape/specter_pricing.txt). | Revenue and valuation are modeled estimates, not what the company reports. Pages show no data room reading or memo. |
| **Grata** | Private company search with seller intent signals, deal data, public comps, Excel add-in, MCP. | PE, investment banks, corporate development, consulting, private credit. Venture is not on its solutions list. | Three tiers (Growth, Scale, Alpha), all "Book a demo". [Pricing page](raw/landscape/grata_pricing.txt). | Built for M&A and PE sourcing. Its comps feature compares multiples, and the page does not describe startup funding rounds. |
| **PitchBook** | Private markets data platform: screeners, profiles, market maps, research, AI search, plugins. API is a paid add-on (Direct Data). | Capital markets professionals broadly. | No price on its [products page](raw/landscape/chrome_pages_pricing.txt) (only "Request a free trial"). CostBench lists every plan as "contact sales", one source, limited confidence, verified Oct 11, 2026: [CostBench](raw/landscape/costbench_pitchbook.txt). Its pricing URL returns a 404 page. | No public price. API costs extra. The product page I could read shows no reading of a startup's own documents. |
| **Crunchbase** | Company and funding database with AI search, MCP, signals, valuation estimates, forecasts, competitor lists. | Individuals (Pro), teams (Business), organizations and apps (Custom). | Pro $49 a month billed annually or $99 monthly. Business from $199 a month. Custom is "Talk to sales". Annual equivalents: $588, $1,188 and $2,388. [Pricing page, read in a browser](raw/landscape/chrome_pages_pricing.txt). Vendr's median for firms is $20,000 a year, 71 purchases, updated Feb 2026: [Vendr](raw/landscape/vendr_crunchbase.txt). | Describes companies from outside. Pro exports are capped at 2,000 rows a month. The REST API is sold through the sales team. No data room reading or memo on the pages. |
| **Tracxn** | Startup database with taxonomy, instant competitor lists, valuation and cap tables, revenue and financials, deal CRM. | Investors, corporates; also a free personal tier. | Lite is free with usage limits. Premium is "Contact Sales". API and data packs are priced by specialist. [Pricing page](raw/landscape/tracxn_pricing.txt). | No public price for the paid plan. The pages show no reading of a startup's own documents. |
| **Dealroom** | Startup and funding data, signals on who is rising, MCP connection, API add-on. | Investment teams; qualified startups and nonprofits get special pricing. | Premium EUR 250 and Premium Plus EUR 325 per seat per month, billed annually, 3 seat minimum. At 3 seats that is EUR 9,000 and EUR 11,700 a year; at 10 seats EUR 30,000 and EUR 39,000 (matches the page). API priced on call volume on top. 3-day free trial. [Pricing page](raw/landscape/dealroom_pricing.txt). | Seat minimum and an API add-on. No data room reading, red flags or memo on the pages. |
| **CB Insights** | Market intelligence with predictive signals, company profiles, ChatCBI chat with citations. | Corporate strategy teams, analysts, data teams (CostBench's "best for" list). | No price on its [pricing page](raw/landscape/cbinsights_pricing.txt). Vendr's median is $46,984 a year, range $24,748 to $184,986, page headed 2025: [Vendr](raw/landscape/vendr_cbinsights.txt). CostBench says quote-only: [CostBench](raw/landscape/costbench_cbi.txt). | Strategy-team product at a quote price. Pages show no reading of a startup's own documents or memo. |
| **Carta (data side)** | Data Desk: a round benchmarking tool and reports built from Carta's customer data (50,000+ startups). | Founders, investors, employees. | No price shown on the [data page](raw/landscape/chrome_pages_pricing.txt); the tool is offered with "Try it out". Carta's pricing page returned 403, so the cost of its fund-side products is unknown to me. | The data is aggregated and anonymized by Carta's own statement, so it benchmarks rounds. It says nothing about one named startup's numbers. |
| **NFX Signal** | A directory of investors by stage and sector. | Founders, VCs, scouts and angels (its page text). | No price shown. You join by creating an investing profile. [Page](raw/landscape/nfx_signal.txt). | It finds investors. It does no diligence on a startup. Included because it is on the brief's list. |
| **Clay** | Sales data enrichment: waterfall enrichment across providers, an AI research agent, signal tracking. | Sales and marketing teams. Funds could point it at sourcing lists (my inference). | Free ($0, 100 data credits a month), Launch from $185 a month, Growth from $495 a month. [Pricing page](raw/landscape/clay_pricing.txt). | Not built for diligence. Pages show no comps, red flags or memo. |

### B. AI diligence and memo entrants

| Tool | What it does | Who they sell to | What they charge | Where they fall short |
|---|---|---|---|---|
| **Wokelo** | AI agents for investment research and diligence. Its blog describes memo generation with source attribution. Also the maker of Akta. | PE, banks, consulting, VC, corporates, asset managers (its nav menu). Blog says 35+ PE firms, VC funds and banks. | No price page found (the pricing URL is a 404). "Request a demo". [Blog](raw/landscape/wokelo_blog.txt), [home](raw/landscape/chrome_pages_pricing.txt). | Quote only. The pages I read are written mostly about PE. |
| **Keye** | Reads raw deal files, runs cohort and margin checks, flags anomalies, links every output to its raw source with audit trails (its claims). | PE funds ("built by private equity investors for private equity investors"). | "Request a Demo". The pricing URL is a 404. [Home](raw/landscape/keye.txt). | PE-shaped (CIMs, large funds), quote only. No memo, comps or market signals on the page. |
| **Termina** | On-demand diligence scans and metric benchmarks (retention, churn, growth, top-customer share). | VC firms, corporate development, founders. | "Get started". No price page (404). [Home](raw/landscape/termina.txt). | Metrics-focused. The page shows no deck reading, memo or source links. |
| **askRIA** | Data room analysis, red flag detection, a 0 to 100 diligence score, investment committee memo drafts, deal CRM. | VC and PE funds in the UK, US and UAE (its page). | Tiers from pay as you go to enterprise, each "Custom, priced to your fund". The VC tier ("Hawk") lists 5 AI diligence deals a month and IC memo generation. [Pricing page](raw/landscape/askria_pricing.txt), [product page](raw/landscape/askria.txt). | The closest product to Tricorder. No public price. It scores answers against evidence in the data room, but the page does not say each claim links to a page. No market signals or comps shown. |
| **V7 Go** | Document agents for private markets. Its VC memo page claims memos in 2 to 4 hours with citations linked to source pages. | Private markets, insurance, real estate firms. | "No public price list": an annual contract scoped on platform, users and documents. [Pricing page](raw/landscape/v7_pricing.txt), [VC memo page](raw/landscape/v7_vc.txt). | Enterprise sales motion, no self-serve price. Its own memo claim is 2 to 4 hours, not minutes. |
| **Energent** | General-purpose AI "teammates"; its VC diligence page lists data room ingestion, financial model analysis, red flag identification, automated memos. | Teams of many kinds. | Free $0, Standard $30 a month, Pro $240 a month (annual billing, credit based). Enterprise custom. [Pricing page](raw/landscape/energent_pricing.txt). | General agent platform. The page does not say claims link to sources. |
| **Apify "AI Dealflow Analysis"** | A pay-per-use actor that turns a pitch deck into an investment memo with a JSON summary. Covers unit economics, valuation, market size, red flags. | Developers and investors on Apify's marketplace. | $12 per completed analysis. [Actor page](raw/landscape/apify_dealflow.txt). | A single actor, not a workflow. The page describes cross-checking against live web sources, and I did not test it. |
| **Flybridge memo generator** | Open source tool that turns a pitch deck or transcript into a memo using research agents. Released by a VC firm for founders. | Founders. | Free, open source. [Post](raw/landscape/flybridge.txt). The post shows "Jan 8"; the year is not in the text I read. | Written for founders to test their pitch. No source-linking claim. |
| **Diligent** (open source, GitHub devyanshujadon/diligent) | Turns a startup name or URL into a one-page memo. A critic drops any finding without a real URL or quote. | Builders. | Free; needs your own model and search keys. [README](raw/landscape/diligent_readme.txt). | A demo project (seeded with one company). Not a hackathon winner as far as I can find. |
| **Decile Hub** | Fund operations suite: data rooms, CRM, LP portal, reporting, a deal memo builder, a legal and tax chat helper. | Emerging VC managers (900+ firms by its page). | No price shown. [Page](raw/landscape/decile.txt). | Runs the fund. It does not analyze a startup's numbers. |
| **Fundwave** | Fund operations: capital calls, IRR, deal pipeline, investor portal. | VC, PE, fund of funds. | "Schedule a demo". [Page](raw/landscape/fundwave.txt). | Fund administration. No diligence analysis. |
| **Visible** | Founder investor updates and fundraising data rooms; portfolio monitoring for investors. | Founders (plans), investors (portfolio monitoring). | Founder plans $0, $59, $129 and $199 a month (higher if billed monthly). [Pricing page](raw/landscape/visible_pricing.txt). | Hosts data rooms and updates. Does not analyze them. |

Looked at and left out:

- **Metal** ([metal.so](raw/landscape/metal.txt)) is an operating system for founders raising rounds. It is not a diligence tool for funds.
- **Vestberry** ([page](raw/landscape/vestberry_home2.txt)) is portfolio management (Track 3).
- **Flux** is a circuit board design tool (the name in the brief's list did not match).
- **Diligence Assist** did not load.
- **Hebbia, Rogo, AlphaSense and Brightwave** came up in search results as enterprise finance AI. I saved their pages but did not map them, since none sells to the small funds and angels Track 2 names. Add them if the critics want them.

---

## Part 2: The sponsors' and judges' products

Each entry: what it offers, the sign-up path, any free tier or credits a page states, and one line on a demo use. The demo company is synthetic, so any tool that looks up a real company has to run on the synthetic company's real named competitors or sector, not on the synthetic company itself.

### Akta (from Wokelo), akta.pro

- **Offers.** Company Data API (16 sections, 20M+ companies, 70+ to 75+ data points depending on the page), News Signals (entity-resolved, event-typed, sentiment), List Generation (by filters or plain English), and six "alternative signals": headcount trends, website traffic, job posts, social posts, employee reviews, product reviews. Also a hosted MCP server at `https://mcp.akta.pro/mcp` with 17 tools, and a CLI. Its home page says every response ships with source metadata ([home](raw/landscape/chrome_pages_pricing.txt), [overview](raw/landscape/akta_overview.txt), [MCP tools](raw/landscape/akta_mcp_tools.txt)).
- **Sign-up path.** [playground.akta.pro/signup](https://playground.akta.pro/signup): name, email, password or Google. The page says "Try for free! No credit card required". The API key is shown once and goes in an `x-api-key` header. In Claude Code: `claude mcp add --transport http akta-pro https://mcp.akta.pro/mcp --header "x-api-key: ..."` ([MCP setup](raw/landscape/akta_mcp_setup.txt)).
- **Free tier or credits.** The sign-up page offers a free start and a "Have a coupon code?" field. No page I read states how many free credits you get or says anything about hackathon credits. Docs contact: sales@akta.pro ([credits page](raw/landscape/akta_pricing.txt)).
- **The catch that matters.** Pay as you go is "personal use only", 25 requests a minute, 100 Company Data calls a month, and it does not include the alternative signals (headcount, traffic, jobs, reviews) or funding data ([rate limits](raw/landscape/akta_ratelimits.txt), [pricing page](raw/landscape/chrome_pages_pricing.txt)). The Subscription plan is $50 a month for 1,250 credits ($0.04 a credit) and adds them. The pricing page and the docs disagree on whether Subscription includes funding data (page: Enterprise only; docs: limited access on Subscription).
- **Cost of a pull** ([landscape_price_math.py](landscape_price_math.py)). One company's profile sections (8 credits), one news call of 20 articles, and the five alternative signals come to 19.3 credits, about $0.77 at $0.04. A target plus four competitors is 96.5 credits, about $3.86. One Subscription month covers about 65 companies pulled this way.
- **Demo use.** The market signal tracker (Track 2's third direction): hiring, traffic, reviews and news for the target's real competitors, each number carrying Akta's source metadata into the readout.

### Roundtable (sponsor; CEO Arjun Padmajan is a judge)

- **Offers.** The Luma page says "a data platform that lets your AI agents talk to each other". I could not find a matching site or docs. [roundtable.ai](raw/landscape/roundtable_home.txt) is a bot-detection product ("Proof of Human"). [roundtable.sh](raw/landscape/roundtable_sh.txt) is a CLI that convenes six AI models to deliberate. Neither matches the Luma description or a CEO named Padmajan. Searches for him returned nothing.
- **Sign-up path, free tier.** Unknown.
- **Demo use (a guess).** If it lets agents share data, it could carry facts from one scan to another (the financials scan hands a number to the memo writer). Do not plan on it until someone says what it is. Ask at the 10:00 intros.

### Wand AI (Radhika Khandelwal's employer), wand.ai

- **Offers.** Enterprise "AI workers" (Wand Agents) and a platform (Wand OS) with a registry, team coordination and governance. The pages talk about agents with an accountable owner, scoped access and oversight ([agents](raw/landscape/wand_agents.txt), [OS](raw/landscape/wand_os.txt)). I found no developer docs, API or free tier.
- **Sign-up path.** A [contact form](raw/landscape/wand_contact.txt).
- **Demo use.** No integration. A framing: present each scan as an agent with a stated job, a scope and a human owner, and show in the readout which agent found what. A judge who builds agents may find that familiar.

### Nicrron x Ninoo, nicrronninoo.ai

- **Offers.** The Nicrron API: one OpenAI-compatible endpoint (`https://api.nicrron.ai/v1`) for 110 models from 18 makers (the Luma page says 65+ models from 10 providers; the site is newer). Routing names (`nicrron/auto`, `reasoning`, `coding`, `fastest`, `cheapest`), automatic fallback, and an exact-match cache that returns repeat requests in about 12 ms at no cost when temperature is 0. Example list prices per million tokens: Claude Sonnet 5.5 at $2 input and $10 output. Chat prompts are not stored ([home](raw/landscape/nicrron_api.txt), [docs](raw/landscape/nicrron_docs.txt)).
- **Sign-up path.** "Get started" at nicrron.ai.
- **Free tier or credits.** "$10 to start, deposits matched up to $500 every 90 days". No hackathon credits stated.
- **A mismatch.** The Luma page says "no markup on model costs". The site says requests paid from credits add a 5% platform fee on top of list prices.
- **Demo use.** One key for the whole team, models swappable per scan, and the cache makes rehearsal runs on the fixed synthetic data room free and repeatable.

### Block Convey, blockconvey.com

- **Offers.** PRISM: traces of every agent step, evaluators, synthetic test scenarios (beta), alerts and failure diagnosis ([home](raw/landscape/blockconvey.txt)).
- **Sign-up path.** "Start free".
- **Free tier.** $0 a month with 100 credits a month. Builder is $20 a month for 400 credits, Growth $50 for 1,000 ([pricing](raw/landscape/blockconvey_pricing.txt)).
- **Demo use.** Trace each scan, and use an evaluator that fails any memo line without a source. That gives a reliability story for the judges. It costs integration effort on a day with little time, so it is optional.

### SeedLegals, seedlegals.com

- **Offers.** A legal platform for founders and investors: company formation, SAFEs, cap tables, funding rounds, a Data Room product, a portfolio view for investors ([home](raw/landscape/seedlegals.txt), [investors page](raw/landscape/seedlegals_investors.txt)). I found no API or developer docs and no hackathon credits.
- **Sign-up path.** "Book a demo" and a pricing page.
- **Demo use.** It is where a real startup's cap table, SAFEs and round documents live, which are the documents a data room contains. The synthetic data room's cap table and SAFE could follow those formats, and the pitch can name SeedLegals as the source of the document types we read (my suggestion).

### You.com search APIs, you.com

- **Offers.** Web Search API with news included, Contents (page extraction), cited Research, Answer, and a Finance Research API. A hosted MCP server ([API page](raw/landscape/youcom_api.txt), [docs](raw/landscape/youcom_docs.txt)).
- **Sign-up path.** None needed for the free MCP profile: `claude mcp add --transport http youdotcom "https://api.you.com/mcp?profile=free"`.
- **Free tier or credits.** 100 searches a day through the free MCP profile with no sign-up. New accounts get $100 in free credits (20,000 calls at $5 per 1,000), no card.
- **Demo use.** Customer wins and pricing changes for the competitor signal tracker, with timestamped citations. The Finance Research API is worth a test for the comps step.

### Tavily, tavily.com

- **Offers.** Search, Extract, Crawl, Map and Research endpoints, MCP, Python and JavaScript SDKs ([docs](raw/landscape/tavily_docs.txt)).
- **Sign-up path.** An API key from the docs page.
- **Free tier or credits.** Researcher plan: 1,000 credits a month, no card. Pay as you go $0.008 a credit. Project $30 a month for 4,000 credits. A startup program lists 100,000 free credits by application ([pricing](raw/landscape/tavily_pricing.txt), [startups](raw/landscape/tavily_startups.txt)).
- **Demo use.** Extract a competitor's pricing page and careers page for the signal tracker. FirstSignal (Part 4) used Tavily for evidence retrieval.

### Crunchbase API and MCP, data.crunchbase.com

- **Offers.** REST API in three packages (Fundamentals, Insights, Predictions). The docs list a starter playbook named "Surface Competitors and Reasoning for Diligence Workflows". An MCP server gives company, funding, investor, people and prediction data through Claude ([API packages](raw/landscape/cb_api_packages.txt), [MCP overview](raw/landscape/cb_mcp_overview.txt), [llms.txt](raw/landscape/cb_llms.txt)).
- **Sign-up path.** The REST API: "available through the Crunchbase sales team" ([first request](raw/landscape/cb_first_request.txt)). The MCP: a Crunchbase account with MCP access. The pricing page shows Pro, which includes MCP usage, with a "Try monthly free" option ([pricing](raw/landscape/chrome_pages_pricing.txt)).
- **Free tier.** A Pro trial. Nothing about hackathon credits.
- **Terms warning.** The MCP docs say data access for applications built on the MCP server differs from individual seat access and to contact the account team. Use it as a research aid, not as Tricorder's shipped data source, unless the organisers or Crunchbase say otherwise.
- **Demo use.** Comps (the organisers' second direction): similar companies and recent rounds for the target's category, with the reason each one is fair written by the model from the fields returned.

### Also worth a look: Carta's round benchmarks

Carta's round benchmarking tool (Part 1) gives deal-size and valuation benchmarks by stage, sector and geography. It is not a sponsor tool and I saw no API. It may help check a comp round by hand.

---

## Part 3: The judges

Source for who they are: the [Luma page](raw/landscape/luma_description.txt) (the judge list is in the page text, with the page's own links). I did not fetch or scrape LinkedIn. Where I cite a person's LinkedIn page, it is the URL from the Luma page, and I use only the title a search result showed.

### Who said "slick code and a real business"

The Luma page says of Radhika Khandelwal: "She'll want to see both slick code and a real business." ([luma.com/vc-hack-nyc](https://luma.com/vc-hack-nyc)). I confirmed this in the page's embedded data. It is the organisers' third-person bio, so it is how the organisers describe her, not something I can show she said herself.

### The eight

**Abeera Saeed, Plug and Play.**

- Who: Ventures Principal at Plug and Play, investing in Enterprise and AI B2B SaaS from pre-seed to Series A (Luma).
- Caution: a search result titled the LinkedIn page the Luma page links ([LinkedIn profile](https://www.linkedin.com/in/abeera-saeed-a608ba134/)) as "VP of Operations and Investments @ Propel". I cannot tell which is current. Ask.
- Public statements on diligence, sourcing, memos or AI tooling: none found. She is credited on one issue of the Plug and Play Enterprise and AI team newsletter, "Deep Dive: Permission, Not Power" (Oct 7, 2026), which argues that the bottleneck for data center power is community consent, not technology, and backs that with figures and named sources ([newsletter issue](https://pnpenterpriseai.substack.com/p/deep-dive-permission-not-power)). Another issue by the same team, which does not credit her, is titled "The Model Isn't the Moat" ([issue](https://pnpenterpriseai.substack.com/p/the-model-isnt-the-moat)).

**Michael Barone, Everywhere Ventures.**

- Who: Associate (Luma), investment analyst (the fund's podcast), early-stage investor (his own site), at a pre-seed fund that says it invests $250k into pre-seed rounds ([fund home](raw/landscape/everywhere_home.txt)).
- Public work: he runs a personal site with a series called "Signals and Startups" that connects research and open source to emerging themes, with a startup list per issue giving round size, date and backers ([site](https://www.michaeljbarone.com/signals), [example issue](https://www.michaeljbarone.com/signals/pacing-the-frontier)). He also writes on AI infrastructure ([Beyond the Token](https://www.michaeljbarone.com/ideas/beyond-the-token)) and hosted episode 110 of the fund's podcast, an interview with the founder of Zelt ([episode](https://podcasts.apple.com/us/podcast/all-in-one-zelt-solution-chris-priebe-with-michael-barone/id1683046904?i=1000754472655)).
- On diligence, memos or AI tooling: nothing directly. His writing is signal-driven and specific about sources.

**D. J. Patel.**

- Who: "VC | 3x exited founder" (Luma). Fund and stage not stated. His LinkedIn URL is [LinkedIn profile](https://www.linkedin.com/in/djpat/).
- Public statements: none found. Search results surface DJ Patil (a different person, former US chief data scientist). I have no evidence they are the same, and the Luma bio does not say so. Do not assume.

**Radhika Khandelwal, Wand AI.**

- Who: product leader at Wand AI who builds AI agents and has spent years in the VC world (Luma).
- A 2024 NYU Stern club article profiles a Radhika Khandelwal as a Summer and Fall 2023 associate at SenseAI Ventures, focused on AI across industries. She says the role gave her an eye for evaluating early-stage AI products ([article](https://medium.com/nyu-stern-private-equity-and-venture-capital-club/a-slice-of-nyu-sterns-vc-class-f5fff63c7558), [saved excerpt](raw/landscape/radhika_nyu_stern_article.txt)). The article does not mention Wand AI, so it is likely, not confirmed, that this is the same person.
- Nothing on diligence tooling or memos.

**Bettina Sosa, Yaven.**

- Who: co-founder and CEO of Yaven, with an engineering background including Head of Engineering in crypto, per her company's [about page](raw/landscape/yaven_about.txt).
- Yaven's product: agents for marketing and creative businesses that find clients, research each company, follow a client's market and competitors, and explain what each change means ([home](raw/landscape/yaven_home.txt)). That is close to Track 2's third direction, a signal tracker for a company and its competitors.
- Statements on diligence or memos: none found. Her company's [manifesto](raw/landscape/yaven_manifesto.txt) argues software should adapt to people.

**Arjun Padmajan, Roundtable.**

- Who: CEO of Roundtable, where AI agents connect and work together (Luma). [LinkedIn profile](https://www.linkedin.com/in/apadmajan/).
- Public statements: none found. See Part 2 on Roundtable.

**Erzsébet (Elisabeth) Ábrám, the residency.**

- Who: Community Architect at the residency (Luma). The residency describes itself as "college meets accelerator" with three-month cohorts and a demo day for investors ([site](raw/landscape/residency_home.txt)). She is not described as an investor.
- Public statements: none found.

**Akhil A. (Akhil Abraham), Collectors.**

- Who: Staff Security Engineer at Collectors, securing companies through AI adoption, M&A and IPO compliance (Luma). The handle in his Luma link matches his own site, [4khil4braham.com](https://4khil4braham.com/cyber-security).
- His site says he builds security programs that stand up to IPO scrutiny, regulation and M&A due diligence, and that he helps organisations with access to frontier AI models. That is diligence seen from the security side: the questions asked of a company, not of a startup's growth.

### What the panel will likely reward

This section is my inference, not a finding. The panel is three investors (one a principal, one an associate, one unidentified), two AI-agent builders, one security engineer and one community lead. They have not posted criteria.

- **A working product on real inputs, and a buyer.** The organisers' own bio line for Khandelwal says "slick code" and "a real business". The demo must run live on the synthetic data room, and the pitch must say who pays and why.
- **Sources you can see.** Barone's writing attaches round size, date and backers to every startup he mentions. The Plug and Play newsletter attaches figures and named sources. Track 2 itself asks for claims that link to sources. Show the link on screen.
- **Reliable agents.** Sosa and Khandelwal build agents for a living. Expect questions on what happens when a scan fails or a source is missing. A flagged gap in the readout is a good answer.
- **Where the data goes.** Abraham works on security and compliance. Say the data room is synthetic, what is sent to which model, and what is stored. Nicrron's no-storage stance and Akta's no-training statement are facts to cite (check each before claiming).
- **Not a thin wrapper.** The Plug and Play team's "The Model Isn't the Moat" title is a hint, and it is not Saeed's own statement. Be ready to say what is hard to copy: the checks, the planted-flag test set, and the readout format.
- **Using sponsors well.** Two judges run sponsor companies (Wand AI, Roundtable). Use a sponsor tool where it helps the readout, and say so. A bolted-on mention may look like a checkbox.

---

## Part 4: Prior art

I found few results. Deal Flow bills itself as NYC's first VC hackathon, and I found no list of winners from a VC-specific hackathon that built diligence tools. The closest cases:

- **FirstSignal** (GitHub, mjz620). Labelled by its own repo as a runner-up in the Hack-Nation Global AI Hackathon, Maschmeyer Group "VC Brain" challenge, built solo. I found no official results page, so the placing is self-reported ([repo](https://github.com/mjz620/FirstSignal), [README](raw/landscape/firstsignal_readme.txt)).
  - What it demoed: it scans GitHub, Hacker News, arXiv, Product Hunt and YC cohorts for founders, then produces a memo where every number carries a trust tier and a link, and a missing fact shows as a flagged gap. Contested claims go to prosecutor, defender and judge agents. Contradictions lead the memo.
  - Its headline example: a company with a polished deck and 92% coverage is a pass because its deck claims an acquisition with no public record. A less-covered company with checkable evidence is an invest. The README's takeaway is that verifiable evidence won, not coverage.
  - Why it matters: this is Tricorder's idea (disagreements first, gaps shown as gaps) already built. Tricorder's difference should be the Track 2 shape (financials against the data room, comps, signals) and a demo that makes the catch visible.
- **LandingAI Financial AI Hackathon Championship** (Luma page [jme15h1t](raw/landscape/financial_ai_hackathon.txt)). This is the 2025 edition (build started Monday Oct 27, finale Saturday Nov 15 in New York; I read the dates, not a year). The page lists earlier winning projects: first place "M&A Due Diligence Assistant", semantic search across complex documents in data rooms. It also lists projects that are disqualified, including "Basic RAG applications" and "Simple Streamlit only applications". A hackathon that bans basic RAG shows judges may mark down a thin document chat.
- **Open source memo tools** that are not hackathon entries: Flybridge's generator and Diligent (Part 1, table B).
- **Agentic Investment Bank hackathon** ([Partiful](raw/landscape/partiful_bank.txt)). Online, Oct 6, with a diligence pod. No winners posted that I found.

---

## What I could not confirm

- **Roundtable.** No matching company or docs.
- **D. J. Patel and Arjun Padmajan.** No public trace.
- **Abeera Saeed's current employer.** Luma and a LinkedIn search title disagree.
- **Radhika Khandelwal's earlier VC role.** A likely but unconfirmed match.
- **Free credits for any sponsor.** Only You.com, Tavily, Nicrron, Block Convey and Crunchbase's trial state something. Akta and SeedLegals state nothing about hackathon credits.
- **Prices behind blocked pages.** PitchBook, Carta's pricing page and Akta's own site returned 403 to plain fetches. I read PitchBook's products page, Carta's data page and Akta's pricing page in a browser. PitchBook shows no price. Carta's pricing page I could not read.
- **Third-party price figures** (Vendr, CostBench) come from small samples. Vendr's Harmonic figure rests on 3 purchases. CostBench's CB Insights and PitchBook pages are single-source and labelled limited confidence. Treat them as rough.
- **Wokelo's price.** A search summary mentioned a figure from a podcast page. I could not find that text on the page, so I left it out.

---

## Part 5: A closer look at Startup Due Dil

Added 2026-10-22 at Ken's request: take every feature we can from the fund partner's home-built tool and any other public information about it. The tool is Startup Due Dil, built by Vlad Tislenko, a partner at SMRK VC, a Ukrainian venture fund. Sources, all saved: the [Tech.eu article](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/) (Aug 2026, saved in [raw/voc/](raw/voc/INDEX.md)), the [dev.ua article](https://dev.ua/en/news/startup-due-dil-1787664994) and the [Kosht article](https://kosht.media/ukrainskyy-investor-zapustyv-shi-servis-dlia-perevirky-startapiv-pered-investytsiiamy/) (saved in [raw/landscape/](raw/landscape/INDEX.md)). Every quote below was checked word for word against the saved pages.

### Its features

| Feature | What the sources say |
|---|---|
| **Speed** | "Startup Due Dil is designed to produce an initial structured report in approximately 10 minutes." (Tech.eu) |
| **Ten agents** | Nine specialists, one per area: team and founders, market, competitors, technology and product, traction and financials, business model, regulatory compliance, ownership structure and cap table, legal considerations. (Tech.eu) |
| **An orchestrator that reruns weak work** | The tenth agent, Oracle, plans the work and checks completeness: "If the analysis of a particular area is insufficient, Oracle can rerun the relevant agent with additional context." (Tech.eu) |
| **Deck only, or more** | "To begin an analysis, a user only needs to upload the startup's pitch deck." For a deeper review the user adds financial statements, a cap table, legal documents, written comments and links. (Tech.eu) |
| **Claims checked against public sources** | "The platform compares claims made in the submitted materials with information from public sources." (Tech.eu) |
| **Cited report with three flag colours** | "The final report includes source citations, while key findings are organised into red, yellow, and green flags", from material risks and inconsistencies, to areas needing clarification, to verified positive signals. (Tech.eu) |
| **What it finds most** | Founders overestimating market size: "Quite often, Startup Due Dil cannot verify those numbers." (Tech.eu) |
| **Tuned by the partner** | When it misses a nuance, he updates that agent and reruns it to confirm the fix. (Tech.eu, paraphrased) |
| **A mode for founders** | "Startups can also run a one-off analysis before raising capital to assess their readiness for investor due diligence." (Tech.eu) |
| **Data handling** | "Administrative dashboards do not display private workspace content, and developers do not have access to user files or reports." Models are called through third-party APIs. (Tech.eu) |
| **Models** | "The current version of Startup Due Dil uses the OpenAI API, although its architecture also supports Anthropic." (Tech.eu) |
| **Cost to build** | "The platform cost less than €1,000 to build." (Tech.eu) |
| **Price** | "The cost of a single report is $49." "Monthly subscriptions are also available: $449 for business angels (up to 10 reports) and $999 for funds (up to 25 reports)." (dev.ua) Payments run through Paddle (dev.ua). |
| **Who uses it** | In use at SMRK's investment work and being tested by other investors; built for VC and private equity firms, especially early stage. (Tech.eu) |
| **Its framing** | "The goal is not to replace the investor, but to provide a more complete evidence base for decision-making and reduce the risk of overlooking an important signal" (Tech.eu). Reference checks and talking to the founder stay with the investor. |

### What it validates

- **The whole idea.** A partner built it for his own work because "the most time-consuming part is finding, verifying, and structuring information" (Tech.eu). That is the slow part the voice-of-the-customer research found.
- **Angels pay.** It sells a plan for business angels at $449 a month for up to 10 reports (dev.ua). That supports Ken's reading that angels want diligence and would pay for it if it were accessible.
- **The flag readout.** Red, yellow and green flags with citations is close to Tricorder's top green and red flags.
- **A price point.** $49 a report sits between the $12-a-memo tool and the enterprise tools in Part 1.

### What Tricorder takes from it

- **A yellow tier.** "Needs clarification" sits between red and green; in Tricorder it is a weak or mixed piece whose question goes on the ask list.
- **Rerun when thin.** Oracle reruns an agent when its area is insufficient. Tricorder's "get more info" steer does this on the operator's request; it could also do it on its own when a piece reads "not enough in the room" but more could be fetched.
- **Specialist areas.** Its nine areas map closely onto Tricorder's pieces. Regulatory compliance and legal are two Tricorder covers only through the checklist's legal and cap table items.
- **A founder mode.** Startups run it on themselves before raising. Tricorder could offer the same: a founder runs the readout on their own room and fixes what disagrees before an investor sees it.

### What Tricorder adds

- Numbers decided by scripts, not by a model's reading, with the readout's verdicts set by a stated rule.
- Corroboration shown both ways: every number two clicks from the sources that agree and the ones that disagree.
- Accounting mislabels and contract terms checked against how each contract is counted.
- An ask list for the founder, and coverage against a published-checklist list of what should be there.
- An interactive memo for the partners, which each reader can steer and run what-ifs on.
- The scans beyond the room: the pitch video, comps, and the associate's ten tabs.
