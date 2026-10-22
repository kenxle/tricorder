# Product brief

## Charter

**What belongs:** What the product is, who it is for, and why. Sections, in this order: Charter, What it is, Who it is for, The problem, The jobs to be done, What it does, What it is not, The principles for choosing methods, Commitments, How we know it works. The principles and commitments that hold for every feature.

**What does not:** How anything works (ARCHITECTURE.md and diagrams). How it looks (STYLE_GUIDE.md). A feature's own reasoning (its folder under docs/features/).

**Level of detail:** A reader finishes knowing what the product is for. That guides every other doc.

**Sources:**

- [The writers' brief for the hackathon plan](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), with every "Added" block from 10:17 AM to 2:19 PM
- [The organisers' problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)
- [The voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md)
- [The research gaps](../reports/20261022.02_research/research_gaps.md): how long a first pass takes, what angels and funds pay, how decks arrive
- [The landscape research](../reports/20261022.02_research/research_landscape.md), including Part 5 on Startup Due Dil
- [The feasibility research](../reports/20261022.02_research/research_feasibility.md)
- [The data-room research](../reports/20261022.02_research/research_data_room.md), and the generated room ([data_room/README.md](../../data_room/README.md), [answer_key.json](../../data_room/answer_key.json))
- [PERSONAS.md](PERSONAS.md), [CHECKLIST.md](CHECKLIST.md) and [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md)
- [ROADMAP.md](ROADMAP.md), for the slice that builds each feature
- [The plan overview page](../features/20261022.01_hackathon_plan/00_overview.md), for the decision cards, and [the board](../BULLETIN.md), for the track change

## What it is

Point it at a startup, get a readout. Tricorder reads everything about a startup, from its pitch deck and video to its financials to its online presence. It runs a set of scans and analyses, creating a readout that gives the operator a detailed understanding of what's great about the business, and where the red flags are. An associate will review and steer the memo as needed, creating the deliverable memo.

The deliverable memo is shared with others within the firm, but rather than a fixed document, this is still interactive, allowing drilldowns, and even allowing partners to alter growth models and see how they could change, themselves.

By identifying gaps, highlighting strengths, rigorously showing its work, and adjusting on the fly, the Tricorder is the best tool for the partner deploying capital.

## Who it is for

Seed and Series A venture firms. At each firm, two people use Tricorder.

- **The associate who prepares the memo.** Their problem is days of gathering and checking before any thinking: "Before I even open your data room, I already have ten tabs up." ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). They work in the readout, check what it found, and steer it into the deliverable memo.
- **The partner who reads the memo and decides.** Their problem is a first pass that is thin where it matters: "Basic financials and model review. But often only a cursory one." ([SaaS investor, on pre-term-sheet diligence, Feb 2025](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)). They read the interactive memo, drill into any line they doubt, and change the growth model themselves to see what it takes.

The firm buys it, per seat. The evidence behind both personas is in [PERSONAS.md](PERSONAS.md).

## The problem

Investors have to check a startup before they put money in, and checking is slow. Three problems stand out in what investors say:

- **Diligence is how an investor learns whether it is a good investment, and stretching the truth is common because so much money is on the line.** Decks and models often say more than the accounts support. A fund guide puts the stakes plainly: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)). The kinds of stretching Tricorder looks for are in [FRAMEWORKS.md](FRAMEWORKS.md).
- **Accurately gathering and checking data is tedious and time consuming.** Sources put it at 12 to 15 hours of senior associate time per investment committee memo ([a memo-tool vendor's claim](https://agentman.ai/blog/ic-memo-that-wrote-itself)), two to three weeks of diligence at seed ([a seed fund](https://underscore.vc/?p=80)), 118 hours of diligence per deal on average ([a survey of VCs](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf)), and in one case weeks just to sift the data ([a junior VC](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture)).
- **Volume makes it worse.** "As an associate at a VC fund, I review about 500 decks a year, speak with around 100 founders, go deep on maybe 15, and invest in only a few." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).


## The jobs to be done

The high-level jobs an investor hires Tricorder for, in Ken's words:

- Deploy capital to trustworthy founders.
- Deploy capital to companies that will create ROI.
- Deploy capital to companies that will become extremely valuable.
- Understand the risk profile of a company.
- Understand the fundamentals of a company.
- Communicate the fundamentals and risk to a group for a group decision.

The user stories that turn these jobs into features are in [USER_STORIES.md](USER_STORIES.md).

## What it does

### Inputs

Everything about a startup, from its pitch deck and video to its financials to its online presence.

- **The company's name.** Enough to start the outside-world checks before any file arrives.
- **An uploaded data room.** The deck, the financial model, the cap table, a metrics export, customer contracts, the hiring plan, founder bios and the website copy. A deck alone is enough to start.
- **Customer contracts, on their own or in the room.** Every order form, pilot agreement and master agreement is read for its terms: length, notice and cancellation period, auto-renewal, pilot terms and any duty to convert, price and payment terms. Each is compared with how it is counted, so a contract the customer can leave in 30 days is not counted as a year of revenue without a flag.
- **A pitch video.** Transcribed with timestamps so every spoken claim keeps its second.
- **The startup's online presence.** Its website, public filings, hiring, traffic, reviews and pricing, read by the comps, market signals and online presence scans.
- **The inbox.** A forwarding address first (such as deals@), because it needs no OAuth review. Then Gmail and Outlook through their official APIs. Tricorder pulls decks out of inbound mail: PDF attachments, and DocSend, Google Drive, Dropbox and Notion links. Investors who write about it prefer a PDF in the inbox, which suits a forwarding address ([the research gaps](../reports/20261022.02_research/research_gaps.md), section 3). The feasibility of each path belongs to [ARCHITECTURE.md](ARCHITECTURE.md).
- **The company's bank account, after Saturday.** With the founder's consent, through a banking connector. See "More checks after Saturday" below.

**Diligence starts on the inbound, before anyone asks.** When a deck arrives, the scans run. By the time the investor opens the email, the readout is one click away, or the readout is the reply. This answers the voice-of-the-customer research's finding that the slow part is gathering: the gathering is done before the person looks.

**Every scan starts as soon as its input exists.** The outside-world checks start on the company's name, the deck scan on the deck, and the model checks when the model lands. Nobody waits for the whole room. The readout fills in as results arrive. Each piece shows whether it is running, done, or waiting on an input, and the operator sees the first green and red flags early. Speed matters because slow diligence costs momentum, as the junior VC above says. The roadmap's inbound-unasked slice builds it ([ROADMAP.md](ROADMAP.md)).

### What Tricorder gathers before the data room is opened

An associate describes her routine: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([associate at a seed fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). Tricorder opens those tabs for her, automatically, the moment a company comes in. This matters most at seed. A seed room is thin by design: a deck, a model, a cap table, a few metrics and founder bios. Y Combinator's seed guide calls an executive summary and a deck enough. So the outside world carries much of a seed first pass, and that is why Tricorder pulls signals from the internet ([the data-room research](../reports/20261022.02_research/research_data_room.md), Part 1). Sources and their terms are in [the feasibility research](../reports/20261022.02_research/research_feasibility.md), Part 2.

| What she checks | What Tricorder gathers | Where from | Piece it feeds |
|---|---|---|---|
| Traffic | Web traffic and its trend for the company and its competitors | Akta's web traffic signal (its paid plan) | Traction, market |
| Reviews | Ratings and review counts, and what reviewers complain about | App store pages through Apple's Search API and Google Play's public pages, plus review sites found through Tavily or You.com search | Customers, the pitch itself |
| Investors | Who has invested, how much and when | Crunchbase, SEC Form D filings, press found by search, checked against the cap table in the room | The pitch itself, comps |
| Co-founder issues | How long the founders have worked together, who left and when, public disputes | Founder bios in the room, founders' GitHub, personal sites, talks and press; never LinkedIn scraping | Team |
| Whether the story matches what's online | Each claim in the deck checked against the website, press, Hacker News and Product Hunt, with dates | The website, Hacker News through the Algolia API, Product Hunt's API, search | Every piece the claim belongs to |

On Saturday, Hollis Voice is invented and has no online footprint, so for it these show as cached competitor readings and as gaps ("not found online"). For a real YC company paired with a synthetic room, part of this runs live on stage: its website, Hacker News, the App Store and SEC filings (see "The demo" below). The full set of tabs, and the online-presence and founder-profile scans, come after Saturday ([ROADMAP.md](ROADMAP.md)).

### The sponsor tools

The hackathon's sponsors offer the data Tricorder reads: Akta for company signals, data and news, Crunchbase for comps and funding, and the Nicrron gateway for model access through one key ([the landscape research](../reports/20261022.02_research/research_landscape.md), Part 2). Each has an adapter that turns its responses into sourced claims. Keys arrive on the day, so each adapter is built and tested this week against its published docs with sample responses, and switches to live on Saturday morning ([ROADMAP.md](ROADMAP.md#sponsor-adapters)). Every scan still works with no sponsor key, from the free sources and this week's cache.

### The scans

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

The framework entries are written in [FRAMEWORKS.md](FRAMEWORKS.md). The roadmap ([ROADMAP.md](ROADMAP.md)) holds the slices and the run of show.

**The claims workflow.** The deck and the pitch video make the claims. Every other document and the outside world either support each claim, contradict it, or say nothing. Tricorder extracts each claim, normalises it, finds the evidence, compares by script, and labels it supported, contradicted or unsupported. The labels feed the pieces ([diagrams/claims_workflow.md](diagrams/claims_workflow.md); Ken at 2:41 PM: "extract claims from the pitch deck and video, and see if the other docs support"). Saturday runs it for the planted flags in the deck and the video. The roadmap's claim-support slice runs it on every claim.

### More checks after Saturday

- **Deck against the books.** Every revenue figure in the deck is checked against the P&L for the same period. A deck that shows only part of the company's history is flagged: a chart that starts after the first revenue month, skips months, or hides a dip. This is the associate's rule: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).
- **Tricorder's own version of the model.** A Series A lead builds its own model from the raw data. Tricorder does the same: the room's revenue, cost and headcount rows go into one monthly table with burn, cash and runway, each cell linked to its row. Every line of the company's model sits beside Tricorder's rebuilt line, and a difference becomes a disagreement claim. Ken at 2:40 PM: "i was already planning on building our own versions of models".
- **Contract terms.** Every contract is read for its terms and compared with how it is counted, as under Inputs above ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.13).
- **The rest of the accounting mislabels.** Saturday's engine runs the kinds it owns. The other kinds follow ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.12).
- **The bank check.** With the founder's consent, the investor connects the company's bank account through a banking connector, Plaid first. Tricorder compares deposits with the revenue rows and outflows with the model's burn. It finds differences in reporting, not fraud. Plaid's Sandbox supports custom test users with configured accounts, so it can be shown on a synthetic bank feed ([Plaid docs](https://plaid.com/docs/sandbox/user-custom/)).
- **Reference-call prep, low priority.** A list of people the operator could call, each with the source that names them, and questions drawn from the weak pieces. Tricorder never contacts anyone. Ken is not sure Tricorder should take this on.

Each has a slice in [ROADMAP.md](ROADMAP.md).

### The readout

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
- **A reference guide for every data-room document.** Each document a seed or Series A room can hold gets its own guide: what it is, what changes between seed and Series A, what a first pass checks, its green flags, red flags and pitfalls with sources, how Tricorder checks it, and the ask-list line if it is missing ([writers' brief, 2:38 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). Research agents are writing them now in `docs/reports/20261022.03_document_guides/`. The checklist and the scans draw on them.
- **The ask list.** The readout ends with what to request from the founder. A script builds it from three things: every gap, every weak piece that more information could settle, and every checklist item expected at the company's stage that the room lacks. Each line says what to ask for (for example current monthly burn, or the current contract language for the largest customers) and the claim it would settle. The operator can copy it into an email. It is the "get more info" steer in reverse: what Tricorder cannot fetch, it asks the operator to request.
- **An interactive memo for the partners.** Tricorder helps the operator write the memo for the partners' meeting. Its sections follow [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md), which is built from real published memos and templates. The memo is interactive: it reads top to bottom like a normal memo, and any partner can drill from a line to its claims and from a claim to its sources, so a reader who wants the raw numbers gets them in two clicks. The recommendation and the judgement lines stay the operator's; Tricorder never says invest or pass. A static PDF, with every claim footnoted, stays available.
- **Each reader steers their own copy, and can run what-ifs.** The operator's memo is the shared version. Each partner can steer a personal copy without changing anyone else's, and can tweak a few assumptions in the financial model (churn, price, hiring pace, whether the pilot counts) to see what the numbers become. Scripts recompute from the company's own files, which never change, and every tweaked number is marked as that reader's scenario beside the company's figure and Tricorder's rebuilt one.
- **Several people on one readout (uncertain).** A lead, teammates or co-investors the lead invites could build one readout at once and split the checklist, with each person's work carrying their name. Ken is not sure this works. Before it is built, an online check of how syndicate leads and angel groups split diligence today decides whether it goes ahead.

### Steering the readout

The readout is a working surface, not a read-only document ([writers' brief, 1:12 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). On any piece, the operator leaves a comment or a short instruction. A steer is one of two kinds.

- **Rewrite a section.** For example, "rewrite the market piece using only the competitor filings" or "treat the pilot as non-recurring". The scans behind the piece run again on that piece's inputs, and the piece is reworded.
- **Get more info for a section.** For example, "read the full room, not the seed drop", "pull the competitor's pricing pages" or "find their latest filing". Tricorder fetches or reads the new sources for that piece, runs its scans on them, and adds the new claims, marked as new.
- **The change shows.** Either way, the new piece replaces the old one with a visible diff. If the verdict moves, the claim that moved it is named.
- **Easy enough for a partner.** Some partners run diligence themselves: "our partners run diligence themselves without handing it to junior staff." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)). Accurate sourcing and interpretation matter most to them, so a steer is one plain sentence on the line that looks wrong, with no setup and no menus, and the answer comes back on that line.
- **A steer changes the reading, not the numbers.** It can change what is read, how claims are grouped and how they are worded. A script's number stays as the script computed it.

Saturday's demo may show one steer on stage, if the overview page's card says so. The roadmap carries steering as an after-Saturday slice ([ROADMAP.md](ROADMAP.md), "steering").

### Where it sits among similar tools

The closest competitors validate the idea. Several AI entrants already turn a data room into a memo with every claim linked to its source, and the voice-of-the-customer research's strongest pay signal is a $600M fund using one of them ([vendor case study, paraphrased in the voice-of-the-customer research](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go)). A fund partner built one for his own work, Startup Due Dil, and now sells it to funds and angels ([the landscape research](../reports/20261022.02_research/research_landscape.md), Part 5). Tricorder does not need to be very different from them. It does the same core job and adds to it. What it adds is the top green and red flags, the overview under them, and the corroboration trail. The operator sees first the best green flags and the worst red flags, then which pieces of the company look strong and which look weak. Any number is two clicks from its source and from every source that corroborates or contradicts it. The red-flag engine proves each flag with a script, and its flags feed the overview.

### The demo

Ken's direction at 2:49 PM: "we want to have a list of YC companies and we'll pair them with fake data rooms and run live demos on them" ([writers' brief, 2:44 PM to 2:49 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). So the demo shows two kinds of room.

**The controlled rooms.** Every room is synthetic. The organisers require it: "Bring a synthetic data room; never upload a real company's confidential data." ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). Two invented companies have rooms whose planted flags are known ([what a data room is](../reports/20261022.02_research/what_is_a_data_room.md)).

- **Hollis Voice**, an invented phone agent for independent veterinary clinics, raising a $9,000,000 Series A. The room has 17 files, eight planted red flags (seven kinds, one of them also stated on video), three clean decoys and three green flags. The counts are the lengths of the `full_room_files`, `flags`, `decoys` and `green_flags` lists in [answer_key.json](../../data_room/answer_key.json). Four of the planted kinds are the organisers' four examples. The other three are customer concentration, gross margin that leaves out delivery costs, and cumulative sign-ups shown as active customers. The generator also writes a clean room with nothing planted and a variant room whose flags someone outside the build picks and seals ([SEALING.md](../../data_room/SEALING.md)).
- **Brasswick**, an invented seed-stage company. Its room is one thin tier and carries different kinds of planted flags, with its own answer key (`data_room/answer_key_brasswick.json`).

**Real companies, live.** Real YC companies from the spring 2026 batch, from a list Ken approves, are each paired with a fake data room. On stage, the outside-world scan reads one real company's public footprint live: its website, Hacker News, the App Store and SEC filings. The room's documents are invented. One safeguard holds throughout: an invented room under a real company's name must never read as a claim about that company.

- Every page of those rooms carries "Synthetic test document. Not this company's data."
- The numbers are invented and plausible, anchored only to what the company has published.
- Planted problems are named test plants in the answer key and on screen, and the demo says so out loud.
- The company's public facts (name, product, the founders' public bios, any announced round) come only from public pages, saved with links.
- Ken picks the companies. A research agent proposes candidates with their public footprint, and the rooms are generated only after Ken chooses.

**The order on stage.** The demo opens on Hollis Voice's readout, already waiting because the run finished before the captain walked up: the top green and red flags, then the overview. It drills into the weakest piece (revenue, with its four ARR numbers) and then into one strong piece, showing the sources that agree in both directions ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). Then it switches to the approved real company, whose outside-world scan runs live while the judges watch. If a live call fails, the panel shows the copy saved this week, with its date. The roadmap's [demo-script](ROADMAP.md#demo-script) holds the beats.

## What it is not

- **Not a sourcing database.** It does not find companies. Affinity, Harmonic, PitchBook and the rest do that (the landscape research, Part 1).
- **Not a CRM or a fund operations tool.**
- **Not a chat window over documents.** A prior financial hackathon disqualified basic RAG apps (the landscape research, Part 4). Tricorder's checks are scripts with numbers and tolerances.
- **Not a replacement for the partner's judgment.** It does the gathering and the checking. The partner decides.
- **Not a fraud detector.** The voice-of-the-customer research's worst misses were faked books and forged bank statements. Tricorder cannot tell a faked document from a real one. It finds differences in reporting, between files and against the outside world, and shows each one. A fake that agrees across every file gets through. The bank check after Saturday compares the bank with the books, and it too finds differences in reporting, not fraud.
- **Not confirmatory diligence.** Reference calls, bank statements and legal review come after the term sheet (the voice-of-the-customer research, "What they do instead"). Tricorder may later prepare reference calls, at low priority, but it never makes them.
- **Not a Track 1 sourcing product.** The founder scan is one scan inside Tricorder, built after Saturday.

## The principles for choosing methods

1. **Every claim links to its source.** A claim without a source a person can open does not reach the readout.
2. **Green flags and red flags first, then the overview, strong and weak alike, gaps shown as gaps.** The readout opens on the best green flags and the worst red flags, then every piece of the company. A piece that looks strong counts as much as one that looks weak. A number two independent sources agree on is corroborated, and that is what makes a piece look strong. Disagreements and flags are reasons a piece looks weak, one click down. The readout never fills a missing fact with a plausible one.
3. **A check a script can run beats a model's reading.** The script decides that a number is wrong. The model reads only what a script cannot: a deck's claims page, a contract clause, a tab note, a spoken number, a messy ledger line. The feasibility research found three of the planted flags are pure script checks, and the rest need a model only to read text before a script compares (the feasibility research, Part 3.2).
4. **No real company's confidential data.** Every demo room is synthetic. Public filings and public pages are fine. A synthetic room under a real company's name never reads as a claim about that company: it is labelled on every page, and its planted problems are named test plants.
5. **Nothing is scraped against a site's terms.** LinkedIn's terms prohibit scraping, so the founder scan uses official APIs, consented exports, GitHub, personal sites and public talks. Reddit is read only from pages a person saved by hand. Where a source has an official API, Tricorder uses it.
6. **Personas and problems, with say, do, pay.** Every persona is a specific problem in that person's own words. Say, do and pay are the three layers of evidence, weakest to strongest. What people pay to solve goes in the value proposition. See [PERSONAS.md](PERSONAS.md).
7. **The data stays with the investor, and they can see and delete what was pulled.** The mailbox is read for decks only. Nothing is stored beyond the readout and its sources. The investor can see and delete everything Tricorder pulled. [BRAND.md](BRAND.md) gives the sentence that says this on the page.

## Commitments

- **Every claim links to the exact page, cell, URL or video second it came from.** One click opens it, and the quote checker runs over the final page.
- **Every missing fact shows as a gap instead of a guess.**
- **A steer never changes a script's number because someone asked.** Every rewrite keeps its sources and shows what changed.
- **Tricorder reports its own misses.** On the demo room it shows how many planted flags it found and how many decoys it wrongly flagged, scored against the data-room research's answer key.
- **The data rule above holds for every input.** The inbox makes it sharpest, so it is stated on the page where the inbox is connected. A bank connection is read only with the founder's consent and deleted when the consent is withdrawn.
- **Tricorder never claims to detect fraud.** It finds differences in reporting and says so.
- **A what-if never replaces a fact.** A reader's scenario number sits beside the company's figure and Tricorder's rebuilt one. The room's files never change.
- **No scan logic before Saturday.** The organisers say Saturday is for building ([writers' brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). This week holds everything else:
  - the research, including [the research gaps](../reports/20261022.02_research/research_gaps.md), all done online
  - the one-page founder brief for the judges
  - the synthetic data rooms (Hollis Voice and Brasswick), their answer keys, the clean room and the sealed variant room
  - the synthetic rooms for the real YC companies Ken approves, each page labelled "Synthetic test document. Not this company's data.", and each company's outside calls saved as the live demo's fallback
  - the API keys (the feasibility research, Part 5)
  - the prompts and schemas, written as entries in [FRAMEWORKS.md](FRAMEWORKS.md)
  - the diligence checklist and the memo template
  - the empty repo skeleton, written by an agent: folders, packages, the CI commands, `.env.example`, the Claim schema and the shared file-reader stub, with no scan logic

  The skeleton is option B on the overview page's skeleton card, as the buildability critic recommends. Its condition: Ken asks the organisers at the mixer and tells the judges plainly what was written before the day ([ROADMAP.md](ROADMAP.md), "skeleton-card").

## How we know it works

Tricorder is a product after Saturday, so this section is written for a product. Numbers below are targets to set after the first pilot, not predictions.

**First measure: the hackathon result.** A live demo on the synthetic rooms, with the outside-world scan running live on a real company, judged by a panel of investors and agent builders. The organisers describe one judge as wanting both good code and a real business (the landscape research, Part 3). The demo shows the readout catching planted flags live, and says who would buy it (the fund, per seat). There is no paying customer yet, and the demo does not claim one; this is a demo.

**On the demo room, the score against the answer key.** Planted flags found out of the eight entries, and decoys wrongly flagged out of three (the data-room research, Part 3.6). The seed drop alone should catch five of the eight; the full room the other three (the data-room research, Part 3.4). The same run on the sealed variant room and on the clean room shows the checks are not fitted to our own key.

**What the online research found.** No trustworthy public number exists for how long a first-pass memo takes ([the research gaps](../reports/20261022.02_research/research_gaps.md), section 1). The best number covers all the diligence on a deal: 118 hours on average in a survey of 885 VCs, and 81 hours at early-stage firms ([academic survey of VCs, 2016](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf)). The slowest part is getting the information. So Tricorder states no time saving as a number until a pilot measures one.

**With a pilot fund, the measures a fund would judge it on:**

- **Time to first-pass memo.** From the deck arriving to a readout the operator would hand a partner. No public baseline exists, so the pilot times the fund's own first pass on its first deals and uses that.
- **Flags a partner agrees with.** Of the flags Tricorder raises, how many the partner calls real. Of the problems the partner finds, how many Tricorder raised first.
- **Disagreements found.** How many places per deal the deck, model, video and outside world disagree, and how many of those the partner did not already know.
- **Whether the fund pays.** Say and do are not enough. The pilot ends with a price. Price is the top reason funds turn a tool down: 39% of rejections in a 2026 survey of 250+ venture professionals ([survey, May 2026](https://ewvc.beehiiv.com/p/vc-tech-stack-pulse-2026), via the research gaps).

## Decisions for Ken

**Settled by Ken.** Each is written into this brief.

- **Track 2, diligence.** Ken is asking the organiser to change the team's listing to diligence (the board row TRI-track-fix). The founder scan from Track 1 is one scan inside Tricorder, built after Saturday.
- **The edge and the readout's shape** ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). The best green flags and the worst red flags first, then which pieces look strong and which look weak, and every number two clicks from its sources. Disagreements and red flags stay, as reasons a piece looks weak.
- **The pitch line**: Ken chose "Point it at a startup, get a readout. Tricorder takes any data: decks, videos, spreadsheets, data rooms. It reveals insight you can trust, every claim sourced." at 10:34 AM (board row TRI-new-pitch). The 1:09 PM line, "Point it at a startup, get a readout: the best green flags, the worst red flags, and every number two clicks from its sources.", is a proposal for the readout's first screen only.
- **No interviews** (1:34 PM block). Online research only. [The research gaps](../reports/20261022.02_research/research_gaps.md) are done.
- **Angels are a market** (1:27 PM block). They want diligence, lack the time, and buy it by proxy.
- **Competitors validate the idea** (1:36 PM block). Tricorder does the same core job and adds to it.
- **Personas grouped by stage** (1:38 PM block), ranked by evidence within each stage.
- **Differences in reporting, never fraud** (1:33 PM block).
- **The primary personas** (2:35 PM block): the associate at a seed or Series A fund who prepares the memo, and the partner or principal who reads it and decides. Angels, accelerator screeners and corporate VCs are secondary.
- **Two data rooms** (Ken's answer on the overview page, 2:35 PM): Hollis Voice for Series A and Brasswick for seed.
- **A reference guide per data-room document** (2:38 PM block), being written now.
- **The claims workflow** (2:41 PM block), in [diagrams/claims_workflow.md](diagrams/claims_workflow.md).
- **Real YC companies paired with fake rooms, run live** (2:44 PM, 2:46 PM and 2:49 PM blocks). Hollis Voice and Brasswick stay as the controlled rooms. Rooms become templates with hidden issues after Saturday (the roadmap's room-templates slice).
- **The features asked for from 1:12 PM to 2:19 PM**: both kinds of steering, contracts as an input, accounting mislabels, the bank check, the ask list, the checklist and coverage, the interactive memo, per-reader copies and what-ifs, multiplayer (uncertain), deck against the books, and scans that start as soon as their input exists. [ROADMAP.md](ROADMAP.md), "Ken's asks and where they are built", gives the slice for each.

**Open, with the recommendation this brief is written to.** Each is a card on [the plan overview page](../features/20261022.01_hackathon_plan/00_overview.md).

1. **Saturday's scans.** Red-flag engine (scripts only), readout, pitch video, comps from cached filings, and market signals as a cached panel. Frameworks, founders and presence after Saturday. Alternative: add the frameworks scan.
2. **The demo opening.** The readout, already waiting: the top green and red flags, then the overview, then the weakest piece and one strong piece. The forwarded email is the closing "next" line. Alternative: open on the forwarded email.
3. **The skeleton.** Option B: an agent writes the empty skeleton this week, and Ken tells the organisers and the judges. Alternative: the team builds it on Saturday.
4. **What goes on stage.** Steering and the bank check after Saturday, each one line in the close. The checks proven on a sealed variant room and a clean room. The answer-key score in one line, as a test.
5. **Inbox input.** A forwarding address first, then Gmail and Outlook through their official APIs.
6. **Diligence on the inbound.** The scans start when a deck arrives, unasked.
7. **Where the data goes.** Mailbox read for decks only, nothing stored beyond the readout and its sources, the investor sees and deletes everything. Alternative: a self-hosted version.
8. **The real companies for the live demo.** A research agent proposes real YC companies from the spring 2026 batch, with their public footprint. Ken approves the list on the overview page, and rooms are generated only after he does.
9. **After Saturday.** A product sold to funds; the partner or principal buys, the operator uses. Alternative: skills Ken sells on stclair.ai, or a hackathon entry that ends Saturday.
10. **Who we price for first.** Funds first, angels next. Alternative: an angel plan from the start, as Startup Due Dil already sells.
11. **Measures.** Set numeric targets after the first pilot.
12. **The name.** Keep Tricorder for Saturday; rename before the first paid customer ([BRAND.md](BRAND.md)).
