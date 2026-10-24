# Real companies for the live demo

Written 2026-10-22 by the demo-company researcher, commissioned by the 2:44 PM Added block in [00_brief_for_writers.md](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md). Ken picks the companies. No data room has been made. Every page I relied on is saved under [raw/demo_companies/](raw/demo_companies/). Counts come from the scripts named next to them.

## Summary

- **The batch is real.** Y Combinator's own directory lists a "Spring 2026" batch with 193 companies. Its short code on YC's pages is P26.
- **Six candidates, ranked:** Ploy, Tasklet, Sazabi, TesterArmy, Minicor, Expanse. All six are B2B software with a live site, a Launch YC post, an announced round, and published prices or traction.
- **Top three:** Ploy, Tasklet, Sazabi. If Ken wants only two, take Ploy and Sazabi. Tasklet is the richest footprint, but its founder is well known and its valuation is public, so an invented room under its name carries more risk of being misread.
- **The best live moment:** Ploy has a Form D on EDGAR whose amount ($26,571,989 sold) matches its announced $27M seed. The investors tab can find that live, from a free government source, in front of the judges.
- **One rule for the plants:** every planted problem should sit between two invented room documents, never between the room and the real company's public facts. Where the company has published a number, the room repeats it. So the online check shows the real company's story as matching, and the contradictions the demo catches are visibly inside the invented room.
- **Gaps:** I did not check web traffic (Akta's traffic signal needs its Subscription tier) or Product Hunt (the site returns 403 to scripts; the API needs a token). None of the six has an App Store app, so the reviews tab will lean on review sites and HN comments.

## How I confirmed the batch

YC's directory page at [ycombinator.com/companies?batch=Spring 2026](https://www.ycombinator.com/companies?batch=Spring%202026) is a script-driven page. It carries a public, read-only search key for YC's own company index. I used that key to ask the index for the batch ([demo_yc_batch.py](demo_yc_batch.py)).

From [demo_batch_counts.py](demo_batch_counts.py) (output in [demo_batch_counts.txt](demo_batch_counts.txt)):

- Spring 2026 companies in YC's directory: 193. The directory's own batch count agrees.
- By industry: B2B 112, Industrials 26, Fintech 21, Healthcare 17, Consumer 12, Real Estate and Construction 4, Government 1.
- The directory also lists Winter 2026, Summer 2026 and Fall 2026 batches. The page's "current batch" field reads Fall 2026.
- Each company page names the batch "Spring 2026" and gives the code P26. Launch HN titles use the same code, for example "Launch HN: Minicor (YC P26)".

Saved: [yc_companies_spring2026.html](raw/demo_companies/yc_companies_spring2026.html), [yc_algolia_spring_2026.json](raw/demo_companies/yc_algolia_spring_2026.json), [yc_algolia_batch_facets.json](raw/demo_companies/yc_algolia_batch_facets.json), [yc_spring_2026_companies.csv](raw/demo_companies/yc_spring_2026_companies.csv).

## How I chose

1. I kept active B2B and Fintech companies and dropped Healthcare and Consumer outright. That left 131.
2. For each of the 131, [demo_hn_scan.py](demo_hn_scan.py) asked the HN Algolia API for stories linking the company's domain and for Launch HN posts naming it. Results are one row per company in [demo_hn_scan.csv](demo_hn_scan.csv). 27 had at least one HN story linking their domain. 15 are in New York City, but most of those have a thin footprint.
3. I read YC pages for 20 companies with the strongest footprint ([demo_yc_pages.py](demo_yc_pages.py) parses them).
4. For the leading nine I saved the website, Launch YC post, Launch HN thread, round announcements, pricing pages and founder GitHub profiles.
5. [demo_dispute_scan.py](demo_dispute_scan.py) searched HN stories and comments since June 2025 that name each company, and flagged dispute words (lawsuit, sued, terms of service, banned and similar). Output: [demo_dispute_scan.csv](demo_dispute_scan.csv). Only Chert was flagged. A web search for disputes about the six found nothing about them.
6. [demo_formd.py](demo_formd.py) and [demo_formd_lookup.py](demo_formd_lookup.py) looked for Form D filings. EDGAR full-text search returned nothing even for control names, so it does not index Form D content. The company-name lookup and the 2026 Q3 Form D data set did find filings.
7. I scored each company 0 to 2 on five things: the panel gets it in one sentence, the public footprint, natural data-room metrics, safety (nothing sensitive, no dispute), and a New York tie. The per-criterion scores and reasons are in [demo_fit_scores.csv](demo_fit_scores.csv). [demo_fit_totals.py](demo_fit_totals.py) totals them into [demo_fit_totals.csv](demo_fit_totals.csv). The scores are my judgment; the script only adds them.

## The six, ranked

| Rank | Company | What it does | Fit (of 10) | Why it ranks here |
|---|---|---|---|---|
| 1 | Ploy | AI platform that builds and runs a company's website and marketing | 10 | Form D matches the press; public prices; New York office |
| 2 | Tasklet | AI agents that do office work across a company's tools | 9 | Founder published ARR and the round; USV led; famous founder raises the stakes |
| 3 | Sazabi | Observability for engineering teams, pitched as "Datadog for the AI era" | 8 | Cleanest footprint, public prices and usage numbers; no New York tie |
| 4 | TesterArmy | AI agents that test web and mobile apps | 8 | Strong HN launch and founder GitHub; small round; no New York tie |
| 5 | Minicor | Lets AI products drive old Windows software with no API | 8 | New York lead investor; public story names medical-record systems |
| 6 | Expanse | Predicts what compute jobs need so GPUs are not wasted | 7 | Strong footprint; most technical for a seed panel; London |

Minicor, Sazabi and TesterArmy tie on total. I ranked Sazabi and TesterArmy above Minicor because both score full marks on safety.

The tabs below follow the associate's list in [PRODUCT_BRIEF.md](../../ongoing/PRODUCT_BRIEF.md): traffic, reviews, investors, co-founder issues, and whether the story matches what is online. Sources and their terms are in [research_feasibility.md](research_feasibility.md) Part 2.

The same three gaps apply to all six, so I state them once:

- **Traffic:** not checked. Akta's web-traffic signal is an "alternative signal", which Part 2 lists as unavailable on pay-as-you-go and available on the Subscription 50 tier.
- **Product Hunt:** direct fetches returned HTTP 403 for all six ([demo_fetch.py](demo_fetch.py) log). The official API needs a token and its terms bar commercial use. A web search restricted to producthunt.com found no listing for any of them.
- **App stores:** Apple's Search API found no app from any of the six ([demo_appstore_summary.py](demo_appstore_summary.py)). Searches for "Tasklet" and "Expanse" return other sellers' apps with the same names. So the reviews scan must match on seller name or domain, not on app name.

---

## 1. Ploy

- **Batch and YC page:** Spring 2026 (P26). [ycombinator.com/companies/ploy](https://www.ycombinator.com/companies/ploy)
- **One line:** Ploy builds, edits and runs a company's website and marketing channels with AI agents.
- **Founders and public profiles:** YC lists one founder, Bryant Chou, whose YC bio says he co-founded Webflow and was its CTO from 2013 to 2025. Public profile: [X](https://x.com/bryantchou). The Form D also lists a second director, Todd Jackson. A GitHub account named BryantChou exists, but it was created in 2026 and has no followers, so I could not confirm it is his ([github_user_bryantchou.json](raw/demo_companies/github_user_bryantchou.json)).

**Public footprint per tab**

| Tab | What the scan would find | Links | Source that works |
|---|---|---|---|
| Traffic | Not checked | [ploy.ai](https://ploy.ai) | Akta, Subscription tier |
| Reviews | No App Store app. Review sites not searched yet | | Tavily or You.com search |
| Investors | $27M seed led by First Round and YC, announced June 2026. Form D filed 2026-06-24 by Ploy, Inc. (Delaware, San Francisco address): $26,571,989 sold, 11 investors, first sale 2026-05-05, Bryant Chou as executive officer | [Pulse 2.0](https://pulse2.com/ploy-raises-27-million-seed-round-to-launch-ai-growth-platform/), [VCA Online](https://www.vcaonline.com/news/2026061715/ploy-raises-27m-to-turn-your-company-s-website-into-your-hardest-working-employee/), [EDGAR filing](https://www.sec.gov/Archives/edgar/data/2136625/000213662526000001/primary_doc.xml) | EDGAR (free, keyless), search |
| Co-founder issues | One listed founder; long public Webflow history; nothing found | [YC page](https://www.ycombinator.com/companies/ploy) | YC page, X, search |
| Story matches online | Launch YC (23 votes); a company blog post on migrating its agent to a new model drew 258 points and 131 comments on HN; press names customers Hex and Clay and agencies Tonik and TNT Growth; press says it is based in San Francisco and New York; pricing page shows Free $0, Starter $50, Pro $300 a month, and Enterprise | [Launch YC](https://www.ycombinator.com/launches/QuH-ploy-turns-your-website-into-your-company-s-growth-engine), [HN](https://news.ycombinator.com/item?id=48882716), [pricing](https://ploy.ai/pricing) | Website, HN Algolia, YC |

**A synthetic room for Ploy would hold:** a deck and overview built from the public pitch; a model with monthly subscription revenue by plan tier (the real tier prices) plus Enterprise contracts; customer MRR by month for invented customers; a credit-usage table per workspace; an expense ledger with model-inference costs; a cap table whose seed total matches the Form D amount; a hiring plan; founder bio taken only from the YC page.

**Planted test problems that fit:** an Enterprise pilot counted as recurring revenue; credits consumed shown as if they were paying usage; inference cost left out of gross margin; a hiring plan whose payroll does not fit the model's burn. All of these sit between invented documents. Avoid any plant in the cap table, because the real round is public.

**Fit: 10 of 10.** The panel gets it at once. The Form D match is the strongest live moment of the six. Public prices give the model real anchors. New York office. The one weak spot is the founders tab, which has a single listed founder and little writing found yet.

Saved: [yc_page_ploy.html](raw/demo_companies/yc_page_ploy.html), [launchyc_ploy.html](raw/demo_companies/launchyc_ploy.html), [site_ploy.html](raw/demo_companies/site_ploy.html), [site_ploy_pricing.html](raw/demo_companies/site_ploy_pricing.html), [blog_ploy_gpt56.html](raw/demo_companies/blog_ploy_gpt56.html), [news_ploy_pulse2.html](raw/demo_companies/news_ploy_pulse2.html), [news_ploy_vcaonline.html](raw/demo_companies/news_ploy_vcaonline.html), [edgar_company_ploy.xml](raw/demo_companies/edgar_company_ploy.xml), [edgar_submissions_ploy.json](raw/demo_companies/edgar_submissions_ploy.json), [edgar_formd_ploy_primary_doc.xml](raw/demo_companies/edgar_formd_ploy_primary_doc.xml), [hn/ploy.json](raw/demo_companies/hn/ploy.json), [hn_dispute_ploy.json](raw/demo_companies/hn_dispute_ploy.json), [appstore_ploy.json](raw/demo_companies/appstore_ploy.json).

---

## 2. Tasklet

- **Batch and YC page:** Spring 2026 (P26). [ycombinator.com/companies/tasklet-2](https://www.ycombinator.com/companies/tasklet-2)
- **One line:** Tasklet runs AI agents in the cloud that connect to a company's tools and do recurring office work on a schedule.
- **Founders and public profiles:** Andrew Lee, CEO, whose YC bio says he founded Firebase and Shortwave ([X](https://twitter.com/startupandrew)). Jonny Dimond ([X](https://x.com/jonnydimond)). Andrew Lee was interviewed for two hours on The Cognitive Revolution podcast on 2025-10-22 ([episode page](https://hopper.webdirections.org/share/0857315c584b9c1f/3dc11f22-af32-11f0-b7b4-337a6a84fe66)). A GitHub search for a Tasklet organisation found only unrelated accounts.

**Public footprint per tab**

| Tab | What the scan would find | Links | Source that works |
|---|---|---|---|
| Traffic | Not checked | [tasklet.ai](https://tasklet.ai) | Akta, Subscription tier |
| Reviews | No App Store app under its name; other sellers' apps share the name | | Search, matching on domain |
| Investors | The founder's own post: $20M from Union Square Ventures, Lightspeed, YC, Jeff Dean, and Patrick and John Collison, valuing it at $175M. Dealroom later reported a $13M pre-Series A bridge (July 2026). The Q3 2026 Form D data set holds "Gaingels Tasklet June 2026 LLC", an investment vehicle named for it | [Tasklet blog](https://tasklet.ai/blog/2026-04-07-20m-funding), [Dealroom](https://dealroom.co/news/142450-tasklet-raises-13m-bridge-round-for-ai-agents-backed-by-usv-and-lightspe/) | Company site, search, EDGAR Form D data set |
| Co-founder issues | Two founders with long, shared public history at Firebase; nothing found | [YC page](https://www.ycombinator.com/companies/tasklet-2) | YC page, X, podcasts |
| Story matches online | Show HN in October 2025; Launch YC (39 votes); public credit pricing from $25 a month upward; the founder's published traction numbers | [Launch YC](https://www.ycombinator.com/launches/PsX-tasklet-the-cloud-agent-os-for-knowledge-work), [pricing](https://tasklet.ai/pricing) | Website, HN Algolia, YC |

The founder wrote: "Tasklet has grown incredibly fast, with revenue increasing 1,200% already in 2026 and recently passing $5M in annualized run rate." ([Andrew Lee, Tasklet blog, 2026-04-07](https://tasklet.ai/blog/2026-04-07-20m-funding))

**A synthetic room for Tasklet would hold:** a deck that repeats the published $5M run rate and growth; a model with self-serve credit subscriptions and team plans; customer MRR by month across many small invented accounts; credit usage by workspace; an expense ledger heavy in model-inference cost; a cap table consistent with the published round and valuation; a hiring plan (the post says a team of nine with 11 open roles).

**Planted test problems that fit:** cumulative sign-ups shown as active customers; churn hidden by a cohort definition that drops small accounts; inference cost booked below gross margin; a hiring plan larger than the model's payroll. Keep the room's headline ARR equal to the published figure, so no plant reads as a claim that the real figure is wrong.

**Fit: 9 of 10.** The richest footprint of the six, with a founder-published revenue number to check against. USV, a New York fund, co-led. I took a point off safety: the founder is well known, the valuation is public, and judges may know the real numbers. Public round reports also disagree ($20M versus a $13M bridge), which is a good live finding but needs a careful script so it does not read as an accusation.

Saved: [yc_page_tasklet-2.html](raw/demo_companies/yc_page_tasklet-2.html), [launchyc_tasklet.html](raw/demo_companies/launchyc_tasklet.html), [site_tasklet.html](raw/demo_companies/site_tasklet.html), [site_tasklet_pricing.html](raw/demo_companies/site_tasklet_pricing.html), [blog_tasklet_20m.html](raw/demo_companies/blog_tasklet_20m.html), [news_tasklet_dealroom_bridge.html](raw/demo_companies/news_tasklet_dealroom_bridge.html), [podcast_tasklet_andrew_lee.html](raw/demo_companies/podcast_tasklet_andrew_lee.html), [edgar_submissions_gaingels_tasklet.json](raw/demo_companies/edgar_submissions_gaingels_tasklet.json), [github_search_tasklet.json](raw/demo_companies/github_search_tasklet.json), [hn/tasklet-2.json](raw/demo_companies/hn/tasklet-2.json), [hn_dispute_tasklet-2.json](raw/demo_companies/hn_dispute_tasklet-2.json), [appstore_tasklet.json](raw/demo_companies/appstore_tasklet.json), [appstore_tasklet_mac.json](raw/demo_companies/appstore_tasklet_mac.json).

---

## 3. Sazabi

- **Batch and YC page:** Spring 2026 (P26). [ycombinator.com/companies/sazabi](https://www.ycombinator.com/companies/sazabi)
- **One line:** Sazabi watches a team's production logs with AI, alerts on real problems, and opens fixes.
- **Founders and public profiles:** Sherwood Callaway, founder and CEO, a second-time YC founder who previously worked at Brex and Crunchbase. Public profiles: [X](https://twitter.com/shcallaway), [GitHub](https://github.com/shcallaway) (account since 2014). He gave a YC Library talk, "The End of Manual Debugging" ([video](https://www.youtube.com/watch?v=UGYnC9zqa-k), [YC Library](https://ycombinator.com/library/bp-the-end-of-manual-debugging)).

**Public footprint per tab**

| Tab | What the scan would find | Links | Source that works |
|---|---|---|---|
| Traffic | Not checked | [sazabi.com](https://www.sazabi.com) | Akta, Subscription tier |
| Reviews | No App Store app. Customer case studies on its site (Weave, Mastra, XMTP Labs) | [customers](https://www.sazabi.com/customers) | Website, search |
| Investors | $8M seed co-led by J2 Ventures, Village Global and YC, with Orange Collective and more than 60 named angels. No Form D found by name | [seed post](https://www.sazabi.com/blog/seed-round), [SiliconAngle](https://siliconangle.com/2026/04/08/startup-sazabi-bets-logs-ai-agents-replace-traditional-observability-stacks/) | Company site, search |
| Co-founder issues | One listed founder; public talk and writing; nothing found | [YC page](https://www.ycombinator.com/companies/sazabi) | YC page, GitHub, YC Library |
| Story matches online | Launch YC (44 votes) gives monthly usage numbers; the seed post gives design-partner counts; pricing shows Hobby $50, Startup $200, Growth $1,000 a month, and Enterprise | [Launch YC](https://www.ycombinator.com/launches/QdT-sazabi-datadog-for-the-ai-era), [pricing](https://www.sazabi.com/pricing) | Website, YC, HN Algolia |

The seed post says: "Since launching less than a month ago, we've signed up 50 design partners who now rely on Sazabi to monitor and debug their apps" ([Sazabi blog](https://www.sazabi.com/blog/seed-round)).

**A synthetic room for Sazabi would hold:** a deck built from the public "Datadog for the AI era" pitch; a model with plan-tier subscriptions at the real prices plus usage overage; a design-partner list of invented teams with conversion dates to paid; log volume ingested per customer; an expense ledger where storage and inference are the big cost lines; a cap table matching the $8M seed.

**Planted test problems that fit:** free design partners counted as paying customers; storage and inference cost left out of gross margin; one invented customer holding a large share of MRR; a deck ARR that differs from the model. Observability has clean usage metrics, so each plant has a number a judge can follow.

**Fit: 8 of 10.** The cleanest footprint for its size, and every panelist knows Datadog. No New York tie found.

Saved: [yc_page_sazabi.html](raw/demo_companies/yc_page_sazabi.html), [launchyc_sazabi.html](raw/demo_companies/launchyc_sazabi.html), [site_sazabi.html](raw/demo_companies/site_sazabi.html), [site_sazabi_pricing.html](raw/demo_companies/site_sazabi_pricing.html), [site_sazabi_customers.html](raw/demo_companies/site_sazabi_customers.html), [blog_sazabi_seed.html](raw/demo_companies/blog_sazabi_seed.html), [news_sazabi_siliconangle.html](raw/demo_companies/news_sazabi_siliconangle.html), [news_sazabi_letsdatascience.html](raw/demo_companies/news_sazabi_letsdatascience.html), [yc_library_sazabi_talk.html](raw/demo_companies/yc_library_sazabi_talk.html), [github_user_shcallaway.json](raw/demo_companies/github_user_shcallaway.json), [hn_item_sazabi_seed.json](raw/demo_companies/hn_item_sazabi_seed.json), [hn/sazabi.json](raw/demo_companies/hn/sazabi.json), [hn_dispute_sazabi.json](raw/demo_companies/hn_dispute_sazabi.json), [appstore_sazabi.json](raw/demo_companies/appstore_sazabi.json).

---

## 4. TesterArmy

- **Batch and YC page:** Spring 2026 (P26). [ycombinator.com/companies/testerarmy](https://www.ycombinator.com/companies/testerarmy)
- **One line:** TesterArmy's AI agents run plain-English tests on web and mobile apps on every pull request and in production.
- **Founders and public profiles:** Szymon Rybczak, CEO ([X](https://x.com/SzymonRybczak), [GitHub](https://github.com/szymonrybczak), [site](https://szymonrybczak.dev)). Oskar Kwaśniewski, CTO ([X](https://x.com/o_kwasniewski), [GitHub](https://github.com/okwasniewski), [site](https://kwasniew.ski)). Both YC bios describe years of React Native open-source work. Their GitHub accounts show 52 and 98 public repositories ([github_user_szymonrybczak.json](raw/demo_companies/github_user_szymonrybczak.json), [github_user_okwasniewski.json](raw/demo_companies/github_user_okwasniewski.json)).

**Public footprint per tab**

| Tab | What the scan would find | Links | Source that works |
|---|---|---|---|
| Traffic | Not checked | [tester.army](https://tester.army) | Akta, Subscription tier |
| Reviews | No App Store app. Expo's docs carry a TesterArmy integration guide | [Expo guide](https://docs.expo.dev/guides/using-testerarmy/) | Search |
| Investors | €1M pre-seed from YC, AIP Seed, Eight Capital, Script Capital and angels including Guillermo Rauch. No Form D found by name | [The Recursive](https://www.therecursive.com/yc-proven-testerarmy-raises-eur1m-for-ai-agents-that-test-software/) | Search |
| Co-founder issues | Two founders with long public GitHub records; nothing found | [YC page](https://www.ycombinator.com/companies/testerarmy) | YC page, GitHub, X, personal sites |
| Story matches online | Launch HN, 132 points and 69 comments; Launch YC, 95 votes (the highest of the 20 YC pages I read); pricing shows Free, $99, $299 a month and Enterprise; press lists more than 50 clients including Resend and bolt.new | [Launch HN](https://news.ycombinator.com/item?id=48586299), [Launch YC](https://www.ycombinator.com/launches/QWL-testerarmy-test-your-app-with-natural-language), [pricing](https://tester.army/pricing) | HN Algolia, YC, website |

The Launch HN post says: "Over the past few months, we scaled from 0 to 30+ teams using our product every day." ([Oskar Kwaśniewski, Launch HN](https://news.ycombinator.com/item?id=48586299))

**A synthetic room for TesterArmy would hold:** a deck repeating the public customer counts; a model with self-serve plans and a few Enterprise deals; customer MRR by month; test runs per customer; an expense ledger where cloud browsers, device time and inference are the cost lines; a cap table matching a €1M pre-seed.

**Planted test problems that fit:** free test-run credits counted as revenue; device and inference cost left out of gross margin; cohorts that hide churn among hobby accounts; a hiring plan that does not fit the burn.

**Fit: 8 of 10.** Strong launch and founder footprint, and the product is easy to grasp. The round is small for a room that looks like a seed raise, and there is no New York tie.

**A calibration note, not a finding.** The Launch HN post names three people, while YC lists two founders. That is normal for an early team, where the third person is often an early hire. It is exactly the kind of item the co-founder tab must not dress up as a concern, so it makes a good test of the scan's restraint. It should not appear in the demo.

Saved: [yc_page_testerarmy.html](raw/demo_companies/yc_page_testerarmy.html), [launchyc_testerarmy.html](raw/demo_companies/launchyc_testerarmy.html), [site_testerarmy.html](raw/demo_companies/site_testerarmy.html), [site_testerarmy_pricing.html](raw/demo_companies/site_testerarmy_pricing.html), [news_testerarmy_therecursive.html](raw/demo_companies/news_testerarmy_therecursive.html), [hn_item_testerarmy_launch.json](raw/demo_companies/hn_item_testerarmy_launch.json), [github_user_szymonrybczak.json](raw/demo_companies/github_user_szymonrybczak.json), [github_user_okwasniewski.json](raw/demo_companies/github_user_okwasniewski.json), [github_search_testerarmy.json](raw/demo_companies/github_search_testerarmy.json), [hn/testerarmy.json](raw/demo_companies/hn/testerarmy.json), [hn_dispute_testerarmy.json](raw/demo_companies/hn_dispute_testerarmy.json), [appstore_testerarmy.json](raw/demo_companies/appstore_testerarmy.json).

---

## 5. Minicor

- **Batch and YC page:** Spring 2026 (P26). [ycombinator.com/companies/minicor](https://www.ycombinator.com/companies/minicor)
- **One line:** Minicor turns a workflow in old Windows desktop software into an API call, so AI products can use systems that have no API.
- **Founders and public profiles:** Faizaan Chishtie, CEO ([X](https://x.com/faizchishtie), [GitHub](https://github.com/FaizChishtie), account since 2017, links minicor.com). Saheed Akinbile, CTO ([X](https://x.com/sahee_d)). A demo video is linked from the Launch HN post.

**Public footprint per tab**

| Tab | What the scan would find | Links | Source that works |
|---|---|---|---|
| Traffic | Not checked | [minicor.com](https://minicor.com) | Akta, Subscription tier |
| Reviews | No App Store app; HN launch comments discuss the product | | HN Algolia, search |
| Investors | $3.8M seed led by IA Ventures, with YC, Paul Graham, Pioneer Fund, Robinhood Ventures, 20VC and others (October 2026). No Form D found by name | [The SaaS News](https://www.thesaasnews.com/news/minicor-raises-3-8m-seed/) | Search |
| Co-founder issues | Two founders; nothing found | [YC page](https://www.ycombinator.com/companies/minicor) | YC page, GitHub, X |
| Story matches online | Launch HN, 105 points and 64 comments; Launch YC (27 votes); no public pricing page | [Launch HN](https://news.ycombinator.com/item?id=48280729), [Launch YC](https://www.ycombinator.com/launches/Pkq-minicor-windows-desktop-automations-at-scale) | HN Algolia, YC, website |

On HN the CEO describes the customer: "we support the AI companies who are selling to the legacy end users" ([Faizaan Chishtie, Launch HN](https://news.ycombinator.com/item?id=48282054)).

**A synthetic room for Minicor would hold:** a model priced per automation run plus platform fees; contracts with invented AI-software customers in accounting and logistics; runs and failure rates per customer; an expense ledger where virtual machines are the main cost; a cap table matching the $3.8M seed.

**Planted test problems that fit:** a paid pilot counted as recurring revenue; one customer holding most of the run volume; virtual-machine cost left out of gross margin; a run-success rate in the deck that differs from the usage table.

**Fit: 8 of 10.** A New York lead investor and a story the panel understands. Two points off: no public pricing to anchor a revenue table, and the public story names clinics' medical-record systems as a use case. A room for Minicor should use only invented accounting and logistics customers, and say nothing about healthcare.

Saved: [yc_page_minicor.html](raw/demo_companies/yc_page_minicor.html), [launchyc_minicor.html](raw/demo_companies/launchyc_minicor.html), [site_minicor.html](raw/demo_companies/site_minicor.html), [news_minicor_seed_thesaasnews.html](raw/demo_companies/news_minicor_seed_thesaasnews.html), [hn_item_minicor_launch.json](raw/demo_companies/hn_item_minicor_launch.json), [github_user_faizchishtie.json](raw/demo_companies/github_user_faizchishtie.json), [hn/minicor.json](raw/demo_companies/hn/minicor.json), [hn_dispute_minicor.json](raw/demo_companies/hn_dispute_minicor.json), [appstore_minicor.json](raw/demo_companies/appstore_minicor.json).

---

## 6. Expanse

- **Batch and YC page:** Spring 2026 (P26). [ycombinator.com/companies/expanse](https://www.ycombinator.com/companies/expanse)
- **One line:** Expanse predicts how much compute each job on a GPU cluster needs before it runs, so less capacity sits reserved and idle.
- **Founders and public profiles:** Ismaeel Bashir, CEO ([X](https://x.com/ismaeel_bashir_)); Nikodem Bieniek, CTO ([X](https://x.com/nkdem_b)); Yafet Melake, COO ([X](https://x.com/yafet_melake)); Eren Mendi, CPO ([X](https://x.com/erenzmendi03)). The company GitHub organisation [expanse-labs](https://github.com/expanse-labs) holds an open-source wastage scanner.

**Public footprint per tab**

| Tab | What the scan would find | Links | Source that works |
|---|---|---|---|
| Traffic | Not checked | [expanse.sh](https://expanse.sh) | Akta, Subscription tier |
| Reviews | No App Store app; a common name, so search must match on domain | | Search |
| Investors | $5.3M seed led by Crane Venture Partners, with PXN Ventures and angels (September 2026). No Form D found by name | [Expanse blog](https://expanse.sh/blog/expanse-raises-5-3m-seed) | Company site, search |
| Co-founder issues | Four co-founders "out of Edinburgh and Imperial", per their company page; nothing found | [company page](https://expanse.sh/company) | YC page, website, X, GitHub |
| Story matches online | Launch HN, 103 points; Launch YC (53 votes); a published waste figure from one cluster | [Launch HN](https://news.ycombinator.com/item?id=48356312), [Launch YC](https://www.ycombinator.com/launches/QCF-expanse-unlock-wasted-gpu-capacity) | HN Algolia, YC, GitHub |

The CEO wrote: "In one cluster, Expanse identified nearly $8 million of idle compute capacity in a single month." ([Ismaeel Bashir, Expanse blog](https://expanse.sh/blog/expanse-raises-5-3m-seed))

**A synthetic room for Expanse would hold:** annual contracts priced per cluster or per GPU node with invented AI labs and research centres; a pilot pipeline; GPU hours saved per customer; an expense ledger of engineers and cloud test clusters; a cap table matching the $5.3M seed.

**Planted test problems that fit:** a paid proof of concept booked as ARR; savings in the deck that are higher than the usage table supports; one customer as most of the revenue.

**Fit: 7 of 10.** A strong footprint and a crisp return story. But the product is the most technical of the six for a seed panel, and there is no New York tie.

Saved: [yc_page_expanse.html](raw/demo_companies/yc_page_expanse.html), [launchyc_expanse.html](raw/demo_companies/launchyc_expanse.html), [site_expanse.html](raw/demo_companies/site_expanse.html), [site_expanse_company.html](raw/demo_companies/site_expanse_company.html), [blog_expanse_seed.html](raw/demo_companies/blog_expanse_seed.html), [hn_item_expanse_launch.json](raw/demo_companies/hn_item_expanse_launch.json), [github_org_expanse-labs.json](raw/demo_companies/github_org_expanse-labs.json), [github_org_expanse-labs_repos.json](raw/demo_companies/github_org_expanse-labs_repos.json), [hn/expanse.json](raw/demo_companies/hn/expanse.json), [hn_dispute_expanse.json](raw/demo_companies/hn_dispute_expanse.json), [appstore_expanse.json](raw/demo_companies/appstore_expanse.json).

---

## Considered and set aside

- **Chert** (New York, "Twilio for iMessage"). The best New York footprint: a Launch HN with 200 comments. But much of that thread argues the product breaks Apple's iMessage terms, and the dispute scan flagged it. That is close enough to a public dispute to leave out. Saved: [hn_item_chert_launch.json](raw/demo_companies/hn_item_chert_launch.json), [yc_page_chert.html](raw/demo_companies/yc_page_chert.html), [site_chert.html](raw/demo_companies/site_chert.html).
- **Stage** (New York). YC describes a code-review platform, but the website now presents a different product, a voice-planning app called Luke. The online story is moving, so a room would not match it. Saved: [yc_page_stage.html](raw/demo_companies/yc_page_stage.html), [site_stage.html](raw/demo_companies/site_stage.html), [hn_item_stage_show.json](raw/demo_companies/hn_item_stage_show.json).
- **Cohesion** (New York, research tools for public-equity analysts). A panel would like it, but the footprint is thin: no HN posts, and the site renders only through scripts. Saved: [yc_page_cohesion.html](raw/demo_companies/yc_page_cohesion.html), [site_cohesion.html](raw/demo_companies/site_cohesion.html).
- **Interfaze** (a specialised AI model with an arXiv paper and many HN posts). A strong footprint, but it is a model company that sells API calls. That is harder for a seed panel to read from a data room. Saved: [yc_page_interfaze.html](raw/demo_companies/yc_page_interfaze.html), [hn/interfaze.json](raw/demo_companies/hn/interfaze.json).
- **Superlog** (Paris, self-installing observability). A good Show HN, but the round is unconfirmed and it overlaps Sazabi. It would make a fair comp for a Sazabi room. Saved: [yc_page_superlog.html](raw/demo_companies/yc_page_superlog.html), [site_superlog.html](raw/demo_companies/site_superlog.html), [hn_item_superlog_show.json](raw/demo_companies/hn_item_superlog_show.json).
- **All Healthcare and Consumer companies** in the batch were dropped before the scan, to keep health records and minors out.

## Top three, and why

1. **Ploy.** Every tab has something real to find. The investors tab can show a live SEC filing that matches the press, which no other candidate offers. It has a New York office and public prices, so the invented model can sit on real anchors.
2. **Tasklet.** The deepest public record: a founder-written ARR figure, two reported rounds, an investment-vehicle filing, a long podcast. USV gives the New York panel a familiar name. Choose it only if Ken is comfortable putting an invented room under a famous founder's company. The safeguard below matters most here.
3. **Sazabi.** The cleanest and safest. "Datadog for the AI era" lands in one sentence, the prices and usage numbers are public, and the founder has a YC talk the founders tab can find.

If Ken wants two, Ploy and Sazabi give one marketing product and one engineering product, both with full safety marks. Minicor is the best swap-in if a New York investor matters more than public prices.

## The safeguard

The room is invented, and three things keep that plain. First, the label: every page, sheet tab and file name in the room carries "Synthetic test document. Not this company's data." The readout repeats it at the top, and Tricorder shows it beside every finding that comes from the room. Second, the demo script: the presenter says out loud, before the scan starts, that the company is real, the outside scan reads only its public pages, and the data room was written by the team for the test. Each planted problem appears on screen as a named test plant ("Test plant 3: pilot counted as recurring revenue"), never as a finding about the company. Third, the answer key: it lists every plant, where it sits, and what should catch it, and it is shown to the judges. The plants follow one rule. They sit between two invented room documents and never between the room and the company's real public facts. Where the company has published a number (Tasklet's run rate, Ploy's round, Sazabi's prices), the room repeats it. So the online check shows the real story matching, and every contradiction on screen is visibly inside the invented room. The room also names no real customers, investors or people beyond what the public pages already say. The real company's public facts come only from the saved pages listed above.

## Files written

- This report: [research_demo_companies.md](research_demo_companies.md)
- Scripts: [demo_fetch.py](demo_fetch.py), [demo_yc_batch.py](demo_yc_batch.py), [demo_yc_pages.py](demo_yc_pages.py), [demo_hn_scan.py](demo_hn_scan.py), [demo_dispute_scan.py](demo_dispute_scan.py), [demo_formd.py](demo_formd.py), [demo_formd_lookup.py](demo_formd_lookup.py), [demo_github_summary.py](demo_github_summary.py), [demo_appstore_summary.py](demo_appstore_summary.py), [demo_text.py](demo_text.py), [demo_batch_counts.py](demo_batch_counts.py), [demo_fit_totals.py](demo_fit_totals.py)
- Data: [demo_hn_scan.csv](demo_hn_scan.csv), [demo_dispute_scan.csv](demo_dispute_scan.csv), [demo_fit_scores.csv](demo_fit_scores.csv), [demo_fit_totals.csv](demo_fit_totals.csv), [demo_batch_counts.txt](demo_batch_counts.txt)
- Raw pages: everything under [raw/demo_companies/](raw/demo_companies/), including one HN result file per scanned company in [raw/demo_companies/hn/](raw/demo_companies/hn/). The EDGAR full-text results with "control" in the name are the control queries that showed full-text search does not index Form D.
