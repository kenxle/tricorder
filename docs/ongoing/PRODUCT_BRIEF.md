# Product brief

## Charter

**What belongs:** What the product is, who it is for, and why. Sections, in this order: Charter, What it is, Who it is for, The problem, The jobs to be done, What it does, What it is not, The principles for choosing methods, Commitments, How we know it works. The principles and commitments that hold for every feature.

**What does not:** How anything works (ARCHITECTURE.md and diagrams). How it looks (STYLE_GUIDE.md). A feature's own reasoning (its folder under docs/features/).

**Level of detail:** A reader finishes knowing what the product is for. That guides every other doc.

**Sources:**

- [The writers' brief for the hackathon plan](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), with every "Added" block
- [The organisers' problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)
- [The voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md)
- [The landscape research](../reports/20261022.02_research/research_landscape.md)
- [The feasibility research](../reports/20261022.02_research/research_feasibility.md)
- [The data-room research](../reports/20261022.02_research/research_data_room.md)
- [PERSONAS.md](PERSONAS.md), written from [the voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md) alongside this file

## What it is

Point it at a startup, get a readout. Tricorder reads everything about a startup, from its pitch deck and video to its financials to its online presence. It runs a set of scans and analyses, creating a readout that gives the operator a detailed understanding of what's great about the business, and where the red flags are. The readout is not a read-only document, but something that the operator can actively dig through, drill down, and even steer, updating areas that need to be rewritten or need more info.

By identifying gaps, highlighting strengths, rigorously showing its work, and adjusting on the fly, the Tricorder is the best tool for the partner deploying capital.

## Who it is for

Deployers of capital who need to know if they're making the best possible investment. The personas are grouped by the stage they invest at, because the stage decides what is available about the company ([PERSONAS.md](PERSONAS.md)). Venture funds at seed and Series A come first. Full personas, ranked by evidence, are in [PERSONAS.md](PERSONAS.md).

- **Buyer and user.** The fund buys: a partner or principal decides and pays. The operator uses it: usually the associate who does the first pass today, and at some funds the partner, since one seed fund writes that its partners run diligence themselves (the voice-of-the-customer research, row 11). Angels would use and pay for it themselves. Accelerators' screening staff would use it and the program would pay.

The problems these people have, ranked by how strongly they act on them (say, do, pay), are in [PERSONAS.md](PERSONAS.md). In short: partners and principals pay to solve the first-pass problem today (inferred from a vendor case study and a pricing roundup); angels want diligence but lack the time, and pay to get it by proxy from YC, a lead or a fund; accelerator screeners and associates work around it by hand; corporate VCs only describe it, and too thinly to design for.

## The problem

The organisers' statement, from VCs they spoke to: a first pass "still takes an associate days of pulling data, rebuilding numbers from a messy data room and spotting what does not add up" ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). The voice-of-the-customer research's public sources say the same thing four ways.

- **The red flags investors name most are ARR that is not really recurring, then numbers that disagree.** In the voice-of-the-customer research's quotes, ARR comes up in 9 rows from 6 sources, and disagreeing numbers in 5 rows from 3 sources ([red_flag_counts.py](../reports/20261022.02_research/red_flag_counts.py)). The two overlap: padded ARR usually shows as a deck that disagrees with the billing. On disagreement, a seed and Series A fund's guide: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)).
- **What makes ARR not recurring.** Pilots, one-time deals and contracts the customer can cancel are counted as recurring (the voice-of-the-customer research, question 2).
- **The slow part is gathering and checking, not writing.** A junior VC: "It took us weeks to sift through the data, ultimately which led to us losing momentum and conviction in the founders ability to execute (amongst other things)." ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture)).
- **Volume makes it worse.** "As an associate at a VC fund, I review about 500 decks a year, speak with around 100 founders, go deep on maybe 15, and invest in only a few." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).

The market leaves a gap. The landscape research checked 24 tools: 12 that funds use today and 12 AI diligence entrants and fund-operations tools. Its script ([landscape_counts.py](../reports/20261022.02_research/landscape_counts.py)) found that none of the 24 shows market signals, comps and red flags in financials together. The incumbents describe a company from the outside. The entrants read data rooms and write memos.

The closest competitors validate the idea. Five of the 12 entrants turn a data room into a memo with every claim linked to its source (same script), and the voice-of-the-customer research's strongest pay signal is a $600M fund using one of them ([vendor case study, paraphrased in the voice-of-the-customer research](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go)). Tricorder does not need to be very different from them. It does the same core job and adds to it. What it adds is the top green and red flags, the overview under them, and the corroboration trail. The operator sees first the best green flags and the worst red flags, then which pieces of the company look strong and which look weak. Any number is two clicks from its source and from every source that corroborates or contradicts it. The red-flag engine proves each flag with a script, and its flags feed the overview.

## The jobs to be done

1. When a deck lands in my inbox, I want the first pass done before I open it, so I can decide in minutes whether to take the meeting.
2. When I open a readout, I want the best green flags and the worst red flags first, then an overview of which pieces of the company look strong and which look weak, with the disagreements one click down, so I know what to ask in the second meeting.
3. When a startup reports ARR, I want it rebuilt from the contracts and the revenue rows, so I know how much of it is truly recurring.
4. When a fact is missing from the room, I want to see it marked as missing, so I ask for it instead of trusting a guess.
5. When I compare the startup with others, I want comparable companies and rounds with the reason each one is fair.
6. When I watch the pitch video, I want to jump to each claim and see which ones disagree with the deck.
7. When I write the memo for the partners' meeting, I want every claim tied to its source, so I can defend it to people who never met the founder.
8. When I write a small check alone, I want a first pass whose cost fits the check (the angel's job; the voice-of-the-customer research, row 47).

## What it does

### Inputs

Everything about a startup, from its pitch deck and video to its financials to its online presence.

- **An uploaded data room.** The deck, the financial model, the cap table, a metrics export, customer contracts, the hiring plan, founder bios and the website copy.
- **Customer contracts, on their own or in the room.** Every order form, pilot agreement and master agreement is read for its terms: length, notice and cancellation period, auto-renewal, pilot terms and any duty to convert, price and payment terms. Each is compared with how it is counted, so a contract the customer can leave in 30 days is not counted as a year of revenue without a flag.
- **A pitch video.** Transcribed with timestamps so every spoken claim keeps its second.
- **The startup's online presence.** Its website, public filings, hiring, traffic, reviews and pricing, read by the comps, market signals and online presence scans.
- **The inbox.** A forwarding address first (such as deals@), because it needs no OAuth review. Then Gmail and Outlook through their official APIs. Tricorder pulls decks out of inbound mail: PDF attachments, and DocSend, Google Drive, Dropbox and Notion links. The feasibility of each path belongs to [ARCHITECTURE.md](ARCHITECTURE.md).

**Diligence starts on the inbound, before anyone asks.** When a deck arrives, the scans run. By the time the investor opens the email, the readout is one click away, or the readout is the reply. This answers the voice-of-the-customer research's finding that the slow part is gathering: the gathering is done before the person looks.

### What Tricorder gathers before the data room is opened

An associate describes her routine: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([associate at a seed fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). Tricorder opens those tabs for her, automatically, the moment a company comes in. Sources and their terms are in [the feasibility research](../reports/20261022.02_research/research_feasibility.md), Part 2.

| What she checks | What Tricorder gathers | Where from | Piece it feeds |
|---|---|---|---|
| Traffic | Web traffic and its trend for the company and its competitors | Akta's web traffic signal (its paid plan) | Traction, market |
| Reviews | Ratings and review counts, and what reviewers complain about | App store pages through Apple's Search API and Google Play's public pages, plus review sites found through Tavily or You.com search | Customers, the pitch itself |
| Investors | Who has invested, how much and when | Crunchbase, SEC Form D filings, press found by search, checked against the cap table in the room | The pitch itself, comps |
| Co-founder issues | How long the founders have worked together, who left and when, public disputes | Founder bios in the room, founders' GitHub, personal sites, talks and press; never LinkedIn scraping | Team |
| Whether the story matches what's online | Each claim in the deck checked against the website, press, Hacker News and Product Hunt, with dates | The website, Hacker News through the Algolia API, Product Hunt's API, search | Every piece the claim belongs to |

On Saturday the demo company is invented and has no online footprint, so these show as cached competitor readings and as gaps ("not found online"). The online-presence and founder-profile scans that run this for a real company come after Saturday ([ROADMAP.md](ROADMAP.md)).

### The scans

Each scan is one piece of first-pass diligence. Each returns a list of claims, and each claim carries at least one source. The order below is [the feasibility research's](../reports/20261022.02_research/research_feasibility.md) demo order, ranked by demo value for the build effort.

| Order | Scan | What it returns | When |
|---|---|---|---|
| 1 | **Red-flag engine** | A ranked table of flags in the financials and metrics, including accounting mislabels: a number filed under a label it does not earn, such as non-recurring revenue counted as ARR, billings shown as revenue, or cost of revenue filed as operating expense. Each row: what is wrong, the number the company claims, the number Tricorder computed, the severity, and links to both places. | Saturday |
| 2 | **The readout** | The best green flags and the worst red flags, then the overview of the company in pieces, assembled from the scans' claims. Each piece is marked looking strong, looking weak, mixed or not enough in the room, with a one-line reason. Each piece drills down to its claims, and each claim to its sources. | Saturday |
| 3 | **Pitch video** | The video's claims with timestamps. Claims that disagree with the deck are marked. | Saturday |
| 4 | **Comps** | Comparable companies and recent rounds, each with the reason it is a fair comp and a source. Public filings from SEC EDGAR; private rounds from Form D. | Saturday |
| 5 | **Market signals** | Hiring, web traffic, reviews, news and pricing for the company's real competitors, each number linked. | Saturday |
| 6 | **Business frameworks** | Lean canvas, jobs to be done and the other standard frameworks, each box quoting the sentence it came from. | After Saturday |
| 7 | **Founder profiles** | A card per founder from GitHub, personal sites and public talks. This is the founder scan from Track 1, built as one scan inside Tricorder. | After Saturday |
| 8 | **Online presence** | The company's footprint on the web, Hacker News, Product Hunt and app stores. A missing footprint is a finding. | After Saturday |

The framework entries are written in [FRAMEWORKS.md](FRAMEWORKS.md). The roadmap ([ROADMAP.md](ROADMAP.md)) holds the slices and the run of show.

### The readout

The readout is the product. Everything else feeds it.

The readout starts with the best green flags and the worst red flags. Then it breaks into the detail.

- **The best green flags and the worst red flags first.** The first screen is a short headline list: the strongest corroborated positives and the most serious problems, each with its number and source. A script picks them from the piece verdicts and the flags by a stated rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Top green and red flags"). A green flag is as much the product as a red flag.
- **Then the overview.** Under the headline list is the company in pieces: traction and revenue, retention, burn and runway, unit economics, customers, market, comps, team, the pitch itself. Each piece is marked looking strong, looking weak, mixed or not enough in the room. Each shows its reason in one line and how many sources corroborate and contradict it. A script sets each mark by a stated rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts"). Strong pieces get the same space as weak ones.
- **Two clicks to any source.** One click opens the claims behind a piece. One more opens a claim's source in place (the cell, the slide, the clause, the video second), with every other source that corroborates or contradicts it.
- **Disagreements and flags sit one level down.** They are the reasons a piece reads weak. On the demo room, revenue reads weak, and its drill-down shows four ARR figures side by side: the true recurring $2,060,868 (answer key only), the model's $2,240,868, the deck's $2,500,000 and the founder's spoken figure of about $3,000,000 ([the data-room research](../reports/20261022.02_research/research_data_room.md), from [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)).
- **Gaps shown as gaps.** A fact the room does not hold is labelled "not in the data room". A missing document is a question for the partner, not a flag by default (the data-room research, Part 1.5).
- **Every claim links to its source.** A footnote opens the deck page, the spreadsheet cell, the URL with the date it was read, or the video second.
- **A "could not verify" box.** A script checks that each claim's quote appears in its source. A claim that fails drops out of the memo and is listed here.
- **The operator sets the order.** The pieces show in an order the operator can change, so a pre-seed reader can put the founders and the outside world first and a Series A reader the financial pieces.

### Steering the readout

The readout is a working surface, not a read-only document ([writers' brief, 1:12 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). On any piece, the operator leaves a comment or a short instruction. A steer is one of two kinds.

- **Rewrite a section.** For example, "rewrite the market piece using only the competitor filings" or "treat the pilot as non-recurring". The scans behind the piece run again on that piece's inputs, and the piece is reworded.
- **Get more info for a section.** For example, "read the full room, not the seed drop", "pull the competitor's pricing pages" or "find their latest filing". Tricorder fetches or reads the new sources for that piece, runs its scans on them, and adds the new claims, marked as new.
- **The change shows.** Either way, the new piece replaces the old one with a visible diff. If the verdict moves, the claim that moved it is named.
- **A steer changes the reading, not the numbers.** It can change what is read, how claims are grouped and how they are worded. A script's number stays as the script computed it.

Saturday's demo may show one steer on stage, if the overview page's card says so. The roadmap carries steering as an after-Saturday slice ([ROADMAP.md](ROADMAP.md), "steering").

### The demo

The demo runs on the data-room research's synthetic data room ([what a data room is](../reports/20261022.02_research/what_is_a_data_room.md)). The organisers require it: "Bring a synthetic data room; never upload a real company's confidential data." ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). The company is **Hollis Voice**, an invented phone agent for independent veterinary clinics, raising a $9,000,000 Series A. The room has 16 files, seven planted flags plus one variant, and three clean decoys (the data-room research, counts from [data_room_tables.py](../reports/20261022.02_research/data_room_tables.py)). Four of the planted flags are the organisers' four examples. The other three are customer concentration, gross margin that leaves out delivery costs, and cumulative sign-ups shown as active customers. The demo opens on the top green and red flags, then the overview. It drills into the weakest piece (revenue, with its four ARR numbers) and then into one strong piece, showing the sources that agree in both directions ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

## What it is not

- **Not a sourcing database.** It does not find companies. Affinity, Harmonic, PitchBook and the rest do that (the landscape research, Part 1).
- **Not a CRM or a fund operations tool.**
- **Not a chat window over documents.** A prior financial hackathon disqualified basic RAG apps (the landscape research, Part 4). Tricorder's checks are scripts with numbers and tolerances.
- **Not a replacement for the partner's judgment.** It does the gathering and the checking. The partner decides.
- **Not a fraud detector for consistent fakes.** The voice-of-the-customer research's worst misses were faked books and forged bank statements. Tricorder catches documents that disagree with each other. A fully consistent fake needs a check with the bank, which stays with the investor.
- **Not confirmatory diligence.** Reference calls, bank statements and legal review come after the term sheet (the voice-of-the-customer research, "What they do instead").
- **Not a Track 1 sourcing product.** The founder scan is one scan inside Tricorder, built after Saturday.

## The principles for choosing methods

1. **Every claim links to its source.** A claim without a source a person can open does not reach the readout.
2. **Green flags and red flags first, then the overview, strong and weak alike, gaps shown as gaps.** The readout opens on the best green flags and the worst red flags, then every piece of the company. A piece that looks strong counts as much as one that looks weak. A number two independent sources agree on is corroborated, and that is what makes a piece look strong. Disagreements and flags are reasons a piece looks weak, one click down. The readout never fills a missing fact with a plausible one.
3. **A check a script can run beats a model's reading.** The script decides that a number is wrong. The model reads only what a script cannot: a deck's claims page, a contract clause, a tab note, a spoken number, a messy ledger line. The feasibility research found three of the planted flags are pure script checks, and the rest need a model only to read text before a script compares (the feasibility research, Part 3.2).
4. **No real company's confidential data.** The demo room is synthetic. Public filings and public pages are fine.
5. **Nothing is scraped against a site's terms.** LinkedIn's terms prohibit scraping, so the founder scan uses official APIs, consented exports, GitHub, personal sites and public talks. Reddit is read only from pages a person saved by hand. Where a source has an official API, Tricorder uses it.
6. **Personas and problems, with say, do, pay.** Every persona is a specific problem in that person's own words. Say, do and pay are the three layers of evidence, weakest to strongest. What people pay to solve goes in the value proposition. See [PERSONAS.md](PERSONAS.md).
7. **The data stays with the investor, and they can see and delete what was pulled.** The mailbox is read for decks only. Nothing is stored beyond the readout and its sources. The investor can see and delete everything Tricorder pulled. [BRAND.md](BRAND.md) gives the sentence that says this on the page.

## Commitments

- **Every claim links to the exact page, cell, URL or video second it came from.** One click opens it, and the quote checker runs over the final page.
- **Every missing fact shows as a gap instead of a guess.**
- **A steer never changes a script's number because someone asked.** Every rewrite keeps its sources and shows what changed.
- **Tricorder reports its own misses.** On the demo room it shows how many planted flags it found and how many decoys it wrongly flagged, scored against the data-room research's answer key.
- **The data rule above holds for every input.** The inbox makes it sharpest, so it is stated on the page where the inbox is connected.
- **Saturday is build-only.** The organisers' instructions for this week say Saturday is for building only ([writers' brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). This week is for everything else:
  - the research (done: The voice-of-the-customer research to the data-room research)
  - [the research gaps](../reports/20261022.02_research/research_gaps.md): online research on the questions the voice-of-the-customer research left open
  - the one-page founder brief for the judges
  - the synthetic data room and its answer key
  - the API keys (the feasibility research, Part 5)
  - the prompts and schemas, written as entries in [FRAMEWORKS.md](FRAMEWORKS.md)

  No product code before Saturday unless Ken overrules on the overview page.

## How we know it works

Tricorder is a product after Saturday, so this section is written for a product. Numbers below are targets to set after the first pilot, not predictions.

**First measure: the hackathon result.** A live demo on the synthetic room, judged by a panel of investors and agent builders. The organisers describe one judge as wanting both good code and a real business (the landscape research, Part 3). The demo shows both: the readout catching planted flags live, and a named buyer who pays.

**On the demo room, the score against the answer key.** Planted flags found out of the eight entries, and decoys wrongly flagged out of three (the data-room research, Part 3.6). The seed drop alone should catch five of the eight; the full room the other three (the data-room research, Part 3.4).

**In the online research this week.** The voice-of-the-customer research found no trustworthy public number for how long a first-pass memo takes. [The research gaps](../reports/20261022.02_research/research_gaps.md) need to find that number, because it is the baseline for the first pilot measure.

**With a pilot fund, the measures a fund would judge it on:**

- **Time to first-pass memo.** From the deck arriving to a readout the associate would hand a partner. The target is set against the baseline the research gaps find.
- **Flags a partner agrees with.** Of the flags Tricorder raises, how many the partner calls real. Of the problems the partner finds, how many Tricorder raised first.
- **Disagreements found.** How many places per deal the deck, model, video and outside world disagree, and how many of those the partner did not already know.
- **Whether the fund pays.** Say and do are not enough. The pilot ends with a price.

## Decisions for Ken

Each line is a recommendation this brief is written to, with the alternative.

1. **Track.** Track 2 only; the Track 1 founder scan is one scan inside Tricorder, built after Saturday. Alternative: put the founder scan in Saturday's demo.
2. **The edge.** Decided by Ken at 12:55 PM and refined at 1:09 PM ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). The edge is the readout's shape plus the corroboration trail: the best green flags and the worst red flags first, then which pieces look strong and which look weak, and every number two clicks from its sources. Disagreements and red flags stay, as reasons a piece looks weak. The competitors that already source every claim validate the idea; Tricorder does that job and adds these on top.
3. **Saturday's scans.** Red-flag engine, readout, pitch video, comps, market signals; frameworks, founders and presence after Saturday. Alternative: add the frameworks scan on Saturday, since it is the cheapest to build.
4. **Inbox input.** A forwarding address first, then Gmail and Outlook through their official APIs. Alternative: build the Gmail connection first.
5. **Diligence on the inbound.** The scans start when a deck arrives, unasked. Alternative: scans start only when the investor asks.
6. **Where the data goes.** Mailbox read for decks only, nothing stored beyond the readout and its sources, the investor sees and deletes everything. Alternative: a self-hosted version that keeps all data inside the fund.
7. **Demo company.** Hollis Voice, the data-room research's synthetic Series A room. Alternative: Brasswick, the data-room research's plainer freight-invoice company.
8. **After Saturday.** A product sold to funds; the partner or principal buys, the associate uses. Alternative: skills Ken sells on stclair.ai, or a hackathon entry that ends Saturday.
9. **Angels.** Angels already pay for diligence by proxy, which makes them a real market. Price for funds first only if [the research gaps](../reports/20261022.02_research/research_gaps.md) show funds pay more per first pass. Alternative: an angel tier from the start.
10. **Persona order.** Keep the ranking by strength of evidence (partner, angel, accelerator, associate, corporate VC). Who uses and who buys is a separate question and does not change it.
11. **Measures.** Set numeric targets after the first pilot. Alternative: state predicted numbers now.
12. **Self-score on stage.** Show the answer-key score (flags found, decoys wrongly flagged) in the demo. Alternative: show the readout only.
13. **This week.** No product code; research, the research gaps, founder brief, data room, keys and prompts. Alternative: pre-build module skeletons this week.
