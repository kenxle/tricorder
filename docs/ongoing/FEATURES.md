# Features

## Charter

**What belongs:** Each feature in detail. What it does for the associate and the partner. Its inputs and outputs. The roadmap slice that builds it.

**What does not:** Why the product exists ([PRODUCT_BRIEF.md](PRODUCT_BRIEF.md)). How it is built ([ARCHITECTURE.md](ARCHITECTURE.md)). The checks themselves ([FRAMEWORKS.md](FRAMEWORKS.md)). The build order ([ROADMAP.md](ROADMAP.md)).

**Level of detail:** A section per feature, with short lists. A builder finishes a section knowing what the feature does, what it takes in, what it gives back, and which slice builds it.

**Sources:** moved from the product brief on 2026-10-22, so the brief stays short. The sources behind each section are linked where they are used: the [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), the research under [docs/reports/20261022.02_research/](../reports/20261022.02_research/), [ROADMAP.md](ROADMAP.md) and [FRAMEWORKS.md](FRAMEWORKS.md).

## Inputs

Everything about a startup, from its pitch deck and video to its financials to its online presence.

- **The company's name.** Enough to start the outside-world checks before any file arrives.
- **An uploaded data room.** The deck, the financial model, the cap table, a metrics export, customer contracts, the hiring plan, founder bios and the website copy. A deck alone is enough to start.
- **Customer contracts, on their own or in the room.** Every order form, pilot agreement and master agreement is read for its terms: length, notice and cancellation period, auto-renewal, pilot terms and any duty to convert, price and payment terms. Each is compared with how it is counted, so a contract the customer can leave in 30 days is not counted as a year of revenue without a flag.
- **A pitch video.** Transcribed with timestamps so every spoken claim keeps its second.
- **The startup's online presence.** Its website, public filings, hiring, traffic, reviews and pricing, read by the comps, market signals and online presence scans.
- **The inbox.** A forwarding address first (such as deals@), because it needs no OAuth review. Then Gmail and Outlook through their official APIs. Tricorder pulls decks out of inbound mail: PDF attachments, and DocSend, Google Drive, Dropbox and Notion links. Investors who write about it prefer a PDF in the inbox, which suits a forwarding address ([the research gaps](../reports/20261022.02_research/research_gaps.md), section 3). [ARCHITECTURE.md](ARCHITECTURE.md) covers how each path connects: the forwarding address through an inbound mail service, and the Gmail and Outlook permissions each API needs.
- **The company's bank account.** With the founder's consent, through a banking connector. Plaid offers a free sandbox with test accounts and custom test transactions ([Plaid docs](https://plaid.com/docs/sandbox/user-custom/)), so it can be tried before any real connection. If the connector is not ready, the demo shows a sample bank statement in the room, labelled as a sample, and says this is where the connected account would plug in. The bank check itself is under [Later checks](#later-checks).

**Diligence starts on the inbound, before anyone asks.** When a deck arrives, the scans run. By the time the investor opens the email, there is already info on the company. As the data room is filled, more of the memo is created.

**Every scan starts as soon as its input exists.** The outside-world checks start on the company's name, the deck scan on the deck, and the model checks when the model lands. Nobody waits for the whole room. The readout fills in as results arrive. Each piece shows whether it is running, done, or waiting on an input, and the operator sees the first green and red flags early. Speed matters because slow diligence costs momentum: a junior VC lost weeks just sifting the data ([learnings from year 2 in venture](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture)).

While compiling the data room, there are quick ways to send messages to the company asking them for information, with guidance on what they should submit. Each message draws on the [ask list](#the-readout): what to send, and the claim it would settle.

**Built by:** [readers](ROADMAP.md#readers), [pitch-video](ROADMAP.md#pitch-video) and [contract-terms](ROADMAP.md#contract-terms) on Saturday; [inbox-forward](ROADMAP.md#inbox-forward), [inbox-apis](ROADMAP.md#inbox-apis), [inbound-unasked](ROADMAP.md#inbound-unasked) and [bank-check](ROADMAP.md#bank-check) after Saturday.

## What Tricorder gathers before the data room is opened

An associate describes her routine: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([associate at a seed fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). Tricorder opens those tabs for her, automatically, the moment a company comes in. This matters most at seed. A seed room is thin by design: a deck, a model, a cap table, a few metrics and founder bios. Y Combinator's seed guide calls an executive summary and a deck enough. So the outside world carries much of a seed first pass, and that is why Tricorder pulls signals from the internet ([the data-room research](../reports/20261022.02_research/research_data_room.md), Part 1). Sources and their terms are in [the feasibility research](../reports/20261022.02_research/research_feasibility.md), Part 2.

| What she checks | What Tricorder gathers | Where from | Piece it feeds |
|---|---|---|---|
| Traffic | Web traffic and its trend for the company and its competitors | Akta's web traffic signal (its paid plan) | Traction, market |
| Reviews | Ratings and review counts, and what reviewers complain about | App store pages through Apple's Search API and Google Play's public pages, plus review sites found through Tavily or You.com search | Customers, the pitch itself |
| Investors | Who has invested, how much and when | Crunchbase, SEC Form D filings, press found by search, checked against the cap table in the room | The pitch itself, comps |
| Co-founder issues | How long the founders have worked together, who left and when, public disputes | Founder bios in the room, founders' GitHub, personal sites, talks and press; never LinkedIn scraping | Team |
| Whether the story matches what's online | Each claim in the deck checked against the website, press, Hacker News and Product Hunt, with dates | The website, Hacker News through the Algolia API, Product Hunt's API, search | Every piece the claim belongs to |

On Saturday, Hollis Voice is invented and has no online footprint, so for it these show as cached competitor readings and as gaps ("not found online"). For a real YC company paired with a synthetic room, part of this runs live on stage: its website, Hacker News, the App Store and SEC filings (see [The demo](#the-demo)). The full set of tabs, and the online-presence and founder-profile scans, come after Saturday.

**Built by:** [cached-data](ROADMAP.md#cached-data) and [yc-rooms](ROADMAP.md#yc-rooms) this week; [market-signals](ROADMAP.md#market-signals) on Saturday; [outside-in](ROADMAP.md#outside-in) after Saturday.

## The sponsor tools

The hackathon's sponsors offer the data Tricorder reads: Akta for company signals, data and news, Crunchbase for comps and funding, and the Nicrron gateway for model access through one key ([the landscape research](../reports/20261022.02_research/research_landscape.md), Part 2). Each has an adapter that turns its responses into sourced claims. Keys arrive on the day, so each adapter is built and tested this week against its published docs with sample responses, and switches to live on Saturday morning. Every scan still works with no sponsor key, from the free sources and this week's cache.

**Built by:** [sponsor-adapters](ROADMAP.md#sponsor-adapters), this week.

## The scans

Each scan is one piece of first-pass diligence. Each returns a list of claims, and each claim carries at least one source. The order below is [the feasibility research's](../reports/20261022.02_research/research_feasibility.md) demo order, ranked by demo value for the build effort.

| Order | Scan | What it returns | When |
|---|---|---|---|
| 1 | **Red-flag engine** | A ranked table of flags in the financials and metrics, including accounting mislabels: a number filed under a label it does not earn, such as non-recurring revenue counted as ARR, billings shown as revenue, or cost of revenue filed as operating expense. Each row: what is wrong, the number the company claims, the number Tricorder computed, the severity, and links to both places. | Saturday, script checks only; the model readings and the other mislabel kinds after |
| 2 | **The readout** | The best green flags and the worst red flags, then the overview of the company in pieces, assembled from the scans' claims. Each piece is marked looking strong, looking weak, mixed or not enough in the room, with a one-line reason. Each piece drills down to its claims, and each claim to its sources. | Saturday |
| 3 | **Pitch video** | The video's claims with timestamps. Claims that disagree with the deck are marked. | Saturday |
| 4 | **Comps** | Comparable companies and recent rounds, each with the reason it is a fair comp and a source. Public filings from SEC EDGAR; private rounds from Form D. | Saturday, from filings cached this week |
| 5 | **Market signals** | Hiring, web traffic, reviews, news and pricing for the company's real competitors, each number linked. | Saturday as a panel of this week's cached readings; live after |
| 6 | **Business frameworks** | Lean canvas, jobs to be done and the other standard frameworks, each box quoting the sentence it came from. | After Saturday |
| 7 | **Founder profiles** | A card per founder from GitHub, personal sites and public talks. This is the founder scan from Track 1, built as one scan inside Tricorder. | After Saturday |
| 8 | **Online presence** | The company's footprint on the web, Hacker News, Product Hunt and app stores. A missing footprint is a finding. | After Saturday |

Each scan's checks, with their inputs, tolerances and output shape, are written as entries in [FRAMEWORKS.md](FRAMEWORKS.md).

**Contract terms, on Saturday.** Every contract in the room is read for its terms (length, notice and cancellation period, auto-renewal, pilot terms and any duty to convert, price and payment terms) and compared with how it is counted. A contract the customer can leave in 30 days, counted as a year of revenue, becomes a flag ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.13). Slices: [redflag-readings](ROADMAP.md#redflag-readings) and [contract-terms](ROADMAP.md#contract-terms).

**The claims workflow.** The deck and the pitch video make the claims. Every other document and the outside world either support each claim, contradict it, or say nothing. Tricorder extracts each claim, normalises it, finds the evidence, compares by script, and labels it supported, contradicted or unsupported. The labels feed the pieces ([diagrams/claims_workflow.md](diagrams/claims_workflow.md)). Saturday runs it for the planted flags in the deck and the video. The roadmap's claim-support slice runs it on every claim.

**Built by:** [redflag-engine](ROADMAP.md#redflag-engine), [readout](ROADMAP.md#readout), [pitch-video](ROADMAP.md#pitch-video), [comps](ROADMAP.md#comps) and [market-signals](ROADMAP.md#market-signals) on Saturday; [frameworks-scan](ROADMAP.md#frameworks-scan), [founder-profiles](ROADMAP.md#founder-profiles), [online-presence](ROADMAP.md#online-presence) and [claim-support](ROADMAP.md#claim-support) after Saturday.

## Later checks

These checks come after Saturday.

- **Deck against the books.** Each deck revenue figure is checked against the P&L for the same period, and a deck chart that starts late, skips months or hides a dip is flagged. The associate's rule: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). Slice: [deck-vs-books](ROADMAP.md#deck-vs-books).
- **Tricorder's own version of the model.** Tricorder rebuilds a monthly table of revenue, cost, headcount, burn, cash and runway from the room's raw rows, sets each line beside the company's model, and turns each difference into a disagreement claim. Slice: [financial-model](ROADMAP.md#financial-model).
- **The rest of the accounting mislabels.** On Saturday the red-flag engine checks two kinds: non-recurring revenue counted as ARR, and cost of revenue filed as operating expense. After Saturday it adds six more: billings or bookings shown as revenue, pass-through money shown as revenue, contractors left out of burn, capitalised costs kept off the P&L, deferred revenue counted as earned, and one-time fees counted in recurring numbers ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.12). Slice: [accounting-mislabels](ROADMAP.md#accounting-mislabels).
- **The bank check.** With the founder's consent, Tricorder reads the company's bank account through a banking connector (Plaid first, shown on a synthetic feed in Plaid's Sandbox, [Plaid docs](https://plaid.com/docs/sandbox/user-custom/)) and compares deposits with the revenue rows and outflows with the model's burn. It finds differences in reporting, not fraud. Slice: [bank-check](ROADMAP.md#bank-check).
- **Reference-call prep, low priority.** A list of people the operator could call, each with the source that names them, and questions drawn from the weak pieces; Tricorder never contacts anyone, and Ken is not sure it should take this on. Slice: [reference-checks](ROADMAP.md#reference-checks).

## The readout

The readout is the product. Everything else feeds it.

The readout starts with the best green flags and the worst red flags. Then it breaks into the detail.

- **The best green flags and the worst red flags first.** The first screen is a short headline list: the strongest corroborated positives and the most serious problems, each with its number and source. A script picks them from the piece verdicts and the flags by a stated rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Top green and red flags"). A green flag is as much the product as a red flag.
- **Then the overview.** Under the headline list is the company in pieces: traction and revenue, retention, burn and runway, unit economics, customers, market, comps, team, the pitch itself. Each piece is marked looking strong, looking weak, mixed or not enough in the room. Each shows its reason in one line and how many sources corroborate and contradict it. A script sets each mark by a stated rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts"). Strong pieces get the same space as weak ones.
- **Two clicks to any source.** One click opens the claims behind a piece. One more opens a claim's source in place (the cell, the slide, the clause, the video second), with every other source that corroborates or contradicts it.
- **Disagreements and flags sit one level down.** They are the reasons a piece reads weak. On the demo room, revenue reads weak, and its drill-down shows four ARR figures side by side: the true recurring $2,060,868 (answer key only), the model's $2,240,868, the deck's $2,500,000 and the founder's spoken figure of about $3,000,000 ([the data-room research](../reports/20261022.02_research/research_data_room.md), from [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)).
- **Gaps shown as gaps.** A fact the room does not hold is labelled "not in the data room". A missing document is a question for the operator, not a flag by default (the data-room research, Part 1.5).
- **Every claim links to its source.** A footnote opens the deck page, the spreadsheet cell, the URL with the date it was read, or the video second.
- **A "could not verify" box.** A script checks that each claim's quote appears in its source. A claim that fails drops out of the memo and is listed here.
- **Views that suit the stage, and the operator's own order.** The stage decides what exists about a company. So the default order of the pieces suits the stage: at pre-seed the team, the pitch itself and the outside world come first, and at Series A the financial pieces. The operator can reorder the pieces, and their order comes back on their next company at that stage. The verdicts never change with the order.
- **The checklist and coverage.** Tricorder keeps one diligence checklist ([CHECKLIST.md](CHECKLIST.md)): every document, check and outside item a first pass looks for, with the stage it is expected at, built from published checklists, DocSend's two checklist pages among them. The readout shows coverage for the company's stage: each item found, checked or missing.
- **A reference guide for every data-room document.** Each document a seed or Series A room can hold gets its own guide: what it is, what changes between seed and Series A, what a first pass checks, its green flags, red flags and pitfalls with sources, how Tricorder checks it, and the ask-list line if it is missing. Research agents are writing them now in `docs/reports/20261022.03_document_guides/`. The checklist and the scans draw on them.
- **The ask list.** The readout ends with what to request from the founder. A script builds it from three things: every gap, every weak piece that more information could settle, and every checklist item expected at the company's stage that the room lacks. Each line says what to ask for (for example current monthly burn, or the current contract language for the largest customers) and the claim it would settle. The operator can copy it into an email. It is the "get more info" steer in reverse: what Tricorder cannot fetch, it asks the operator to request.
- **An interactive memo for the partners.** Tricorder helps the operator write the memo for the partners' meeting. Its sections follow [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md), which is built from real published memos and templates. The memo is interactive: it reads top to bottom like a normal memo, and any partner can drill from a line to its claims and from a claim to its sources, so a reader who wants the raw numbers gets them in two clicks. The recommendation and the judgement lines stay the operator's; Tricorder never says invest or pass. A static PDF, with every claim footnoted, stays available.
- **Each reader steers their own copy, and can run what-ifs.** The operator's memo is the shared version. Each partner can steer a personal copy without changing anyone else's, and can tweak a few assumptions in the financial model (churn, price, hiring pace, whether the pilot counts) to see what the numbers become. Scripts recompute from the company's own files, which never change, and every tweaked number is marked as that reader's scenario beside the company's figure and Tricorder's rebuilt one.
- **Several people on one readout (uncertain).** A lead, teammates or co-investors the lead invites could build one readout at once and split the checklist, with each person's work carrying their name. Ken is not sure this works. Before it is built, an online check of how syndicate leads and angel groups split diligence today decides whether it goes ahead.

**Built by:** [readout](ROADMAP.md#readout) and [readout-page](ROADMAP.md#readout-page) on Saturday (the headline list, the overview, the drill-downs, the gaps, the quote check and the ask list); [checklist](ROADMAP.md#checklist) this week; [stage-views](ROADMAP.md#stage-views), [checklist-coverage](ROADMAP.md#checklist-coverage), [memo-export](ROADMAP.md#memo-export), [reader-scenarios](ROADMAP.md#reader-scenarios) and [multiplayer](ROADMAP.md#multiplayer) after Saturday.

## Steering the readout

The readout is a working surface, not a read-only document. On any piece, the operator leaves a comment or a short instruction. A steer is one of two kinds.

- **Rewrite a section.** For example, "rewrite the market piece using only the competitor filings" or "treat the pilot as non-recurring". The scans behind the piece run again on that piece's inputs, and the piece is reworded.
- **Get more info for a section.** For example, "read the full room, not the seed drop", "pull the competitor's pricing pages" or "find their latest filing". Tricorder fetches or reads the new sources for that piece, runs its scans on them, and adds the new claims, marked as new.
- **The change shows.** Either way, the new piece replaces the old one with a visible diff. If the verdict moves, the claim that moved it is named.
- **Easy enough for a partner.** Some partners run diligence themselves: "our partners run diligence themselves without handing it to junior staff." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)). Accurate sourcing and interpretation matter most to them, so a steer is one plain sentence on the line that looks wrong, with no setup and no menus, and the answer comes back on that line.
- **A steer changes the reading, not the numbers.** It can change what is read, how claims are grouped and how they are worded. A script's number stays as the script computed it.

Steering is built after Saturday. One steer may be shown on stage on Saturday if Ken chooses that on the overview page's "Steering on stage" card ([00_overview.md](../features/20261022.01_hackathon_plan/00_overview.md)).

**Built by:** [steering](ROADMAP.md#steering), after Saturday.

## Where it sits among similar tools

The closest competitors validate the idea. Several AI entrants already turn a data room into a memo with every claim linked to its source, and the voice-of-the-customer research's strongest pay signal is a $600M fund using one of them ([vendor case study, paraphrased in the voice-of-the-customer research](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go)). A fund partner built one for his own work, Startup Due Dil, and now sells it to funds and angels ([the landscape research](../reports/20261022.02_research/research_landscape.md), Part 5). Tricorder does not need to be very different from them. It does the same core job and adds to it. What it adds is the top green and red flags, the overview under them, and the corroboration trail. The operator sees first the best green flags and the worst red flags, then which pieces of the company look strong and which look weak. Any number is two clicks from its source and from every source that corroborates or contradicts it. The red-flag engine proves each flag with a script, and its flags feed the overview.

**Built by:** [product](ROADMAP.md#product), after Saturday, which turns this into the product sold to funds.

## The demo

The demo shows two kinds of room: invented companies whose planted flags are known, and real YC companies paired with fake data rooms.

**The controlled rooms.** Every room is synthetic. The organisers require it: "Bring a synthetic data room; never upload a real company's confidential data." ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). Two invented companies have rooms whose planted flags are known ([what a data room is](../reports/20261022.02_research/what_is_a_data_room.md)).

- **Hollis Voice**, an invented phone agent for independent veterinary clinics, raising a $9,000,000 Series A. The room has 17 files, eight planted red flags (seven kinds, one of them also stated on video), three clean decoys and three green flags. The counts are the lengths of the `full_room_files`, `flags`, `decoys` and `green_flags` lists in [answer_key.json](../../data_room/answer_key.json). Four of the planted kinds are the organisers' four examples. The other three are customer concentration, gross margin that leaves out delivery costs, and cumulative sign-ups shown as active customers. The generator also writes a clean room with nothing planted and a variant room whose flags someone outside the build picks and seals ([SEALING.md](../../data_room/SEALING.md)).
- **Brasswick**, an invented seed-stage company. Its room is one thin tier and carries different kinds of planted flags, with its own answer key (`data_room/answer_key_brasswick.json`).

**Real companies, live.** Real YC companies from the spring 2026 batch, from a list Ken approves, are each paired with a fake data room. On stage, the outside-world scan reads one real company's public footprint live: its website, Hacker News, the App Store and SEC filings. The room's documents are invented. One safeguard holds throughout: an invented room under a real company's name must never read as a claim about that company.

- Every page of those rooms carries "Synthetic test document. Not this company's data."
- The numbers are invented and plausible, anchored only to what the company has published.
- Planted problems are named test plants in the answer key and on screen, and the demo says so out loud.
- The company's public facts (name, product, the founders' public bios, any announced round) come only from public pages, saved with links.
- Ken picks the companies. A research agent proposes candidates with their public footprint, and the rooms are generated only after Ken chooses.

**The order on stage.** The demo opens on Hollis Voice's readout, already waiting because the run finished before the captain walked up: the top green and red flags, then the overview. It drills into the weakest piece (revenue, with its four ARR numbers) and then into one strong piece, showing the sources that agree in both directions. Then it switches to the approved real company, whose outside-world scan runs live while the judges watch. If a live call fails, the panel shows the copy saved this week, with its date.

**Built by:** [data-room](ROADMAP.md#data-room), [blind-room](ROADMAP.md#blind-room), [yc-rooms](ROADMAP.md#yc-rooms) and [demo-script](ROADMAP.md#demo-script) this week (the demo-script slice holds the beats); [demo-freeze](ROADMAP.md#demo-freeze) on Saturday; [room-templates](ROADMAP.md#room-templates) after Saturday.

## The rules every feature follows, in detail

The product brief states each rule in one line. This is the longer reasoning behind each.

**What Tricorder is not.**

- **Not a sourcing database.** It does not find companies. Affinity, Harmonic, PitchBook and the rest do that (the landscape research, Part 1).
- **Not a CRM or a fund operations tool.**
- **Not a replacement for the partner's judgment.** It does the gathering and the checking. The partner decides.
- **Not confirmatory diligence.** Reference calls, bank statements and legal review come after the term sheet (the voice-of-the-customer research, "What they do instead"). Tricorder may later prepare reference calls, at low priority, but it never makes them.

**The principles for choosing methods.**

1. **Every claim links to its source.** A claim without a source a person can open does not reach the readout.
2. **Green flags and red flags first, then the overview, strong and weak alike, gaps shown as gaps.** The readout opens on the best green flags and the worst red flags, then every piece of the company. A piece that looks strong counts as much as one that looks weak. A number two independent sources agree on is corroborated, and that is what makes a piece look strong. Disagreements and flags are reasons a piece looks weak, one click down. The readout never fills a missing fact with a plausible one.
3. **A check a script can run beats a model's reading.** The script decides that a number is wrong. The model reads only what a script cannot: a deck's claims page, a contract clause, a tab note, a spoken number, a messy ledger line. The feasibility research found three of the planted flags are pure script checks, and the rest need a model only to read text before a script compares ([the feasibility research](../reports/20261022.02_research/research_feasibility.md), Part 3.2).
4. **No real company's confidential data.** Every demo room is synthetic. Public filings and public pages are fine. A synthetic room under a real company's name never reads as a claim about that company: it is labelled on every page, and its planted problems are named test plants.
5. **Nothing is scraped against a site's terms.** LinkedIn's terms prohibit scraping, so the founder scan uses official APIs, consented exports, GitHub, personal sites and public talks. Reddit is read only from pages a person saved by hand. Where a source has an official API, Tricorder uses it.
6. **Personas and problems, with say, do, pay.** Every persona is a specific problem in that person's own words. Say, do and pay are the three layers of evidence, weakest to strongest. What people pay to solve goes in the value proposition. See [PERSONAS.md](PERSONAS.md).
7. **The data stays with the investor, and they can see and delete what was pulled.** The mailbox is read for decks only. Nothing is stored beyond the readout and its sources. The investor can see and delete everything Tricorder pulled. [BRAND.md](BRAND.md) gives the sentence that says this on the page. Built by [readout-store](ROADMAP.md#readout-store).

**Commitments.**

- **Every claim links to the exact page, cell, URL or video second it came from.** One click opens it, and the quote checker runs over the final page.
- **Every missing fact shows as a gap instead of a guess.**
- **A steer never changes a script's number because someone asked.** Every rewrite keeps its sources and shows what changed.
- **Tricorder reports its own misses.** On the demo room it shows how many planted flags it found and how many decoys it wrongly flagged, scored against the data-room research's answer key.
- **The data rule above holds for every input.** The inbox makes it sharpest, so it is stated on the page where the inbox is connected. A bank connection is read only with the founder's consent and deleted when the consent is withdrawn.
- **Tricorder never claims to detect fraud.** It finds differences in reporting and says so.
- **A what-if never replaces a fact.** A reader's scenario number sits beside the company's figure and Tricorder's rebuilt one. The room's files never change.
- **No scan logic before Saturday.** The organisers say Saturday is for building. This week holds everything else ([ROADMAP.md](ROADMAP.md#this-week-no-scan-logic)):
  - the research, including [the research gaps](../reports/20261022.02_research/research_gaps.md), all done online
  - the one-page founder brief for the judges
  - the synthetic data rooms (Hollis Voice and Brasswick), their answer keys, the clean room and the sealed variant room
  - the synthetic rooms for the real YC companies Ken approves, each page labelled "Synthetic test document. Not this company's data.", and each company's outside calls saved as the live demo's fallback
  - the API keys (the feasibility research, Part 5)
  - the prompts and schemas, written as entries in [FRAMEWORKS.md](FRAMEWORKS.md)
  - the diligence checklist and the memo template
  - the empty repo skeleton, written by an agent: folders, packages, the CI commands, `.env.example`, the Claim schema and the shared file-reader stub, with no scan logic

  The skeleton is option B on the overview page's skeleton card, as the buildability critic recommends. Its condition: Ken asks the organisers at the mixer and tells the judges plainly what was written before the day ([skeleton-card](ROADMAP.md#skeleton-card)).

## How we measure it

Tricorder is a product after Saturday, so these measures are written for a product. Numbers below are targets to set after the first pilot, not predictions.

**First measure: the hackathon result.** A live demo on the synthetic rooms, with the outside-world scan running live on a real company, judged by a panel of investors and agent builders. The organisers describe one judge as wanting both good code and a real business (the landscape research, Part 3). The demo shows the readout catching planted flags live, and says who would buy it (the fund, per seat). There is no paying customer yet, and the demo does not claim one; this is a demo.

**On the demo room, the score against the answer key.** Planted flags found out of the eight entries, and decoys wrongly flagged out of three (the data-room research, Part 3.6). The seed drop alone should catch five of the eight; the full room the other three (the data-room research, Part 3.4). The same run on the sealed variant room and on the clean room shows the checks are not fitted to our own key.

**What the online research found.** No trustworthy public number exists for how long a first-pass memo takes ([the research gaps](../reports/20261022.02_research/research_gaps.md), section 1). The best number covers all the diligence on a deal: 118 hours on average in a survey of 885 VCs, and 81 hours at early-stage firms ([academic survey of VCs, 2016](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf)). The slowest part is getting the information. So Tricorder states no time saving as a number until a pilot measures one.

**With a pilot fund, the measures a fund would judge it on:**

- **Time to first-pass memo.** From the deck arriving to a readout the operator would hand a partner. No public baseline exists, so the pilot times the fund's own first pass on its first deals and uses that.
- **Flags a partner agrees with.** Of the flags Tricorder raises, how many the partner calls real. Of the problems the partner finds, how many Tricorder raised first.
- **Disagreements found.** How many places per deal the deck, model, video and outside world disagree, and how many of those the partner did not already know.
- **Whether the fund pays.** Say and do are not enough. The pilot ends with a price. Price is the top reason funds turn a tool down: 39% of rejections in a 2026 survey of 250+ venture professionals ([survey, May 2026](https://ewvc.beehiiv.com/p/vc-tech-stack-pulse-2026), via the research gaps).

**Built by:** [blind-room](ROADMAP.md#blind-room) this week and [demo-freeze](ROADMAP.md#demo-freeze) on Saturday for the score; [pilot](ROADMAP.md#pilot) after Saturday for the fund's measures.
