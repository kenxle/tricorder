# Brief for the writers: the Tricorder hackathon plan

Written 2026-10-22 by the orchestrating session. Every research agent, writer and critic on this plan reads this file first. It holds what Ken asked for, the hackathon's own problem statement, the decisions already made, the sources in order of authority, and the rules every file must follow.

## What Ken asked for, in his words

Dictated 2026-10-22 at about 10:10 AM (speech-to-text, lightly punctuated, nothing else changed):

> You can look at the other agent session here that has come up with the basis for tri-corder, the name of the team and product that that we're gonna be having on the Saturday hackathon and I need to get started on this I wanna go ahead and set the whole factory up. so I want to do this like we did for my text reminders essentially. you know use the Seneschal to set up project we need to write a product brief based on the hackathon prompt which I'm giving you the URL for and then the the document that we put together Together coming up with the name So here's what I'm thinking. I'm gonna give you some roadmap ideas. And you can help me think through them or write them down. We can get them red mapped out. We can build the brand document. We need to run online voice of the customer research. We can do that on Reddit, we can do that on Hacker News, anywhere else that you can find info from VCs talking about this kind of stuff I want us to have you know a section that essentially runs basic business modeling so do a lean canvas figure out jobs to be done, you know, essentially run a few different standard MBA kind of things and do that automatically. We'll want things for competitive analysis. We'll want things for financial modeling. I also think we're gonna want a module that Can understand a video pitch. So it's gonna need to break down a video using whisper and FFmpeg to get the key points out of a video and potentially maybe lead you to the key interesting parts of the video. What else could we analyze? We may want to search for their presence online. So we may want to come up with all of them the things that they have posted online, anything that they're putting on Reddit, we can do a version of our Reddit thing where we let people click on Reddit links. And sort of maybe we make our own little mini browser so that when you're clicking on Reddit links, you can immediately save that info. And what else does a VC look for? You know, they're looking for people, so you also want to look at maybe like the person's socials or the person's GitHub and sort of rate their passion for what they're working on, whether or not they're actually from the industry. So we may want to to be doing sort of personal profiles on these people. So now we've got like personal profiles and the research there. We've got company presence online including Reddit. and Facebook, we've got the basic MBA business viability, and we've got video breakdowns

Added 2026-10-22 at 10:15 AM, when Ken found the organisers' full problem statement:

> oh wait there's a full problem statement here!

He pasted Track 2 (below). The whole document, all four tracks, is saved as [problem_tracks.txt](../../reports/20261022.01_hackathon_sources/problem_tracks.txt).

## The hackathon

Facts from the Luma page ([luma.com/vc-hack-nyc](https://luma.com/vc-hack-nyc), read 2026-10-22) and the organisers' problem tracks document ([the Google Doc](https://docs.google.com/document/d/1S0ytTC-k1zLTvcoUjkRJy0JYuaNgYOWW9EQ04xN8SDA/edit), exported to [problem_tracks.txt](../../reports/20261022.01_hackathon_sources/problem_tracks.txt)).

- **Name.** Deal Flow: NYC's First VC Hackathon @ Betaworks. Hosted by localhost:nyc and VCLab.
- **When.** Saturday 2026-10-24, 9:00 AM to 6:00 PM Eastern (the page's `start_at` is 2026-10-24T13:00:00Z and `end_at` 2026-10-24T22:00:00Z, timezone America/New_York).
- **Where.** Betaworks, New York. The address shows after registration.
- **Schedule.** 9:00 to 10:00 breakfast, mixer and team formation. 10:00 to 10:20 intros and demos. 10:30 to 4:30 hacking, with lunch. 4:30 to 5:30 judging. 5:30 to 6:00 demos and the winner. So the team has about six hours in the room to build.
- **Teams of 4.** Deliverable: a working product, demoed live to a panel of VC judges.
- **Prizes.** $500 to the winning team. $150 for the best social media content posted during the hackathon.
- **Judges.** Abeera Saeed (Plug and Play), Michael Barone (Everywhere Ventures), D. J. Patel, Radhika Khandelwal (Wand AI), Bettina Sosa (Yaven), Arjun Padmajan (Roundtable), Erzsébet (Elisabeth) Ábrám (the residency), Akhil A. (Collectors). No formal criteria are posted. One judge's bio says they "want to see both slick code and a real business" (quoted by the Luma page; the research track confirms the wording and who said it).
- **Sponsors.** SeedLegals, Roundtable (a data platform for AI agents to communicate), Nicrron × Ninoo (model access through one API key). Community sponsors akta.pro (company data and signals via API or MCP for VC workflows) and Block Convey (AI agent reliability and observability).
- **The organisers' framing**, from the tracks document: "Pick one, talk to the people who have the problem before build day, and build a company, not a project."

### Track 2, the one Tricorder is in, verbatim

> Track 2: Diligence. Underwrite a startup in an hour, not two weeks
>
> Problem statement. VCs told us the three things that matter most in diligence: a startup's market signals, its comps, and the issues hiding in its financials and metrics. A first pass still takes an associate days of pulling data, rebuilding numbers from a messy data room and spotting what does not add up. Build a tool that takes a deck or data room and returns the market signals, the right comps and the red flags a partner needs before a second meeting.
>
> Who has this problem: associates and principals at VC funds, angels doing diligence alone, accelerators screening hundreds of applicants.
>
> Directions to explore
> - A red-flag engine for financials and metrics: churn hidden in cohort charts, revenue counted as ARR when it is not recurring, burn that does not match the hiring plan, numbers that disagree between the deck and the model
> - A comp builder that picks comparable companies and recent rounds, and explains why each one is a fair comp
> - A market signal tracker for a company and its competitors: hiring, web traffic, reviews, pricing changes, customer wins
> - A first-draft investment memo where every claim links back to its source
>
> Why it can be a company: diligence is expensive time for every fund, angel group and corporate VC. A tool a partner trusts on the first pass saves days on every deal.
>
> Data to start with: public company filings on SEC EDGAR for comps, the Akta API from Wokelo, Crunchbase, and web search APIs such as You.com and Tavily. Bring a synthetic data room; never upload a real company's confidential data.
>
> Ask in your interviews
> - What do you check first when you open a data room?
> - Which red flag did you once miss and regret?
> - How long does your first-pass memo take, and which part is the slowest?

Track 1 (Sourcing) is adjacent and its "founder-quality score built from public signals" direction is Ken's founder-profile idea. It names the GitHub API, arXiv, SEC EDGAR Form D and the Akta API as data, and says LinkedIn's terms prohibit scraping. The plan treats Track 2 as the track and the founder scan as one scan inside it, unless Ken decides otherwise on the overview page.

## The team and the name

From the team-name workshop page the earlier session ran ([team_name_workshop.txt](../../reports/20261022.01_hackathon_sources/team_name_workshop.txt), 2026-10-22):

- **Name: Tricorder.** Chosen from a seeded list (films, sci-fi). The angle: "Point it at a startup, get a readout. Instant first-pass diligence."
- **Posted to the Team Match Network at 10:04 AM** as team 2. Track: sourcing, diligence. Pitch as posted: "Point it at a startup, get a readout. Thesis-driven sourcing plus a first-pass diligence memo with every claim sourced." Ken's listed role: product. Needs: backend, frontend, data, design.
- **Three people recommended for invitation**, each filling a need: Benjamin Schachter (frontend; TypeScript, React Native, Postgres; senior), Sumit Kumar (backend and data; Python, ML, SQL, automation, data analytics; mid level), Alex Ly (design and finance; Python, valuation, R, Tableau, Power BI, Excel; junior). Whether they accepted is not known to this plan; the board carries a row for Ken to say.
- **Ken's profile on the network**: track sourcing and diligence, idea "good skills we could productize for reliable sourcing and diligence", roles fullstack, product, business. He builds in Rails and presents well.

## The product in one paragraph

Tricorder takes a startup (a deck or a synthetic data room, a pitch video, a website, founder names) and runs a set of scans. Each scan is one piece of first-pass diligence: the red flags in the financials and metrics, the comparable companies and rounds with the reason each is fair, the market signals for the company and its competitors, the business model through the standard frameworks (lean canvas, jobs to be done, and the rest), the pitch video broken into its claims with timestamps, the company's presence online, and a profile of each founder. The scans end in a readout: a first-draft investment memo where every claim links back to its source, and where the claims that disagree with each other (deck against model, video against deck) are the first thing a partner sees. The hackathon version demos on a synthetic data room with planted red flags. The product after the hackathon is the thing Ken's network profile named: good skills, productized, for reliable sourcing and diligence.

## Decisions already made

- **The name is Tricorder** and the one-line pitch is the posted one. The brand doc keeps both and does not reopen the name. The name is a Star Trek word and a CBS/Paramount trademark for merchandise; the brand writer notes the risk for a product after the hackathon and proposes what to do about it, in one paragraph, and the overview page carries a card.
- **Track 2, Diligence.** The product answers Track 2's problem statement, direction by direction. Ken's extra scans (video, presence, founders, business frameworks) are kept and placed where they serve the memo.
- **The demo runs on a synthetic data room.** The organisers require it. Building that data room, with planted red flags that the readout must catch, is a before-Saturday slice and the backbone of the demo.
- **Interviews happen before Saturday.** The organisers ask teams to talk to people with the problem before build day and give three questions. The plan carries a board row for Ken to run two or three short interviews (associates, principals, angels he knows), and the voice-of-the-customer research answers the same three questions from public sources as a stand-in.
- **Every claim in the readout links to its source.** This is the organisers' fourth direction and Ken's standing rule. It is a principle in the product brief and a rule in every scan's output shape.
- **The factory is the one that built My Text Reminders**: Seneschal scaffold, this brief, research tracks, ongoing docs written from them, critics, then one overview page with decision cards that Ken answers on Lahe. The board holds the rows; the roadmap holds the slices.

## Decisions for the overview page

Each of these gets a card with a recommendation. The writers build to the recommendation so nothing waits on the answer.

1. **The stack.** The team is two Python people (Sumit, Alex), one TypeScript person (Benjamin) and Ken (Rails). The scans are Python-shaped (whisper, ffmpeg, pandas, HTTP APIs). The architecture writer recommends and the card offers the alternatives.
2. **How much agents build before Saturday.** Groundwork (the synthetic data room, the module skeletons, each scan runnable alone from the command line with a sample output, the data-source clients) against building everything in the room. The critics weigh what judges will think and what the rules say (the Luma page posts no rule against prior work; the tracks document says to prepare synthetic data before the event).
3. **Which scans make the Saturday demo.** All of them cannot. The roadmap ranks them by what Track 2 asks for first.
4. **Track 2 only, or Track 2 with the founder scan from Track 1.**
5. **The name after the hackathon.** Keep Tricorder, or plan a rename when it productizes.
6. **What Tricorder is after Saturday.** A product, a set of skills Ken sells on stclair.ai, or a hackathon entry that ends on Saturday. The product brief writes "How we know it works" to the recommendation.
7. **The demo company.** A synthetic company in a space the judges know. The data room writer proposes one.

## Sources, in order of authority

1. Ken's words above, and any "Added" block that lands in this file later.
2. The organisers' tracks document and the Luma page, saved under `docs/reports/20261022.01_hackathon_sources/`.
3. The team-name workshop page (same folder).
4. The research tracks this plan commissions, under `docs/reports/20261022.02_research/`.
5. Ken's standing rules, carried from his other projects: the personas-and-problems method (every persona is a specific problem in that person's own words; say, do, pay as the three layers of evidence, weakest to strongest; what people pay to solve is what goes in the value proposition); quotes need a primary link; counts come from scripts; plain words.

## Rules every file must follow

- Plain words. One idea per sentence. No em dashes. No "leverage", no "robust", no "seamless".
- Every number comes from a script or a cited source, and the file names which. No counts by hand.
- A quote from a real person has a link to that person's own words immediately after it. No link, no quotation marks; paraphrase instead.
- Reddit: agents never fetch reddit.com. A research track that wants Reddit ends with a numbered list of `.json` URLs for Ken to save into `docs/reports/20261022.02_research/reddit_corpus/raw/`.
- Hacker News is reachable through the Algolia API (`https://hn.algolia.com/api/v1/search?query=...`). Save what you read under the research folder so the next agent does not refetch.
- LinkedIn is not scraped. The founder scan uses official APIs, consented exports, GitHub, personal sites, X, podcasts and talks.
- No real company's confidential data, ever. Public filings and public pages are fine. The demo data room is synthetic.
- Write into the file the brief names for you and nothing else in `docs/ongoing/`. The orchestrator commits.
- Each ongoing doc keeps its `## Charter` block and rewrites the charter's one `**Sources:**` line to name, as links, the files it drew on.
- Name people by role in copy meant for the public. Teammates are named on the board and in the roadmap's assignments only.

## The files this plan commissions

Research, in parallel, under `docs/reports/20261022.02_research/`:

- **R1, voice of the customer.** `research_voice_of_customer.md`. What associates, principals, solo angels and accelerator screeners say about first-pass diligence: what they check first, the red flags they missed, how long a first memo takes and which part is slowest (the organisers' three questions), and what they pay for today. Sources: Hacker News (Algolia), VC blogs and newsletters, X threads, podcast transcripts, public talks, Product Hunt and G2 reviews of diligence and sourcing tools. Say, do, pay per persona, with the layer marked on every quote. Ends with a Reddit URL list for Ken.
- **R2, the landscape.** `research_landscape.md`. The tools funds use for diligence and sourcing today (Affinity, Harmonic, Specter, Grata, PitchBook, Crunchbase, Tracxn, Dealroom, and the AI diligence entrants), what each does, what it costs, where it stops. The sponsors' and judges' products (Akta from Wokelo, Roundtable, Wand AI, Nicrron × Ninoo, Block Convey, SeedLegals) and what using each on Saturday would mean. Each judge: who they are, what they have said publicly about diligence, sourcing or AI tooling, with links. Prior hackathon winners in this space if findable.
- **R3, feasibility per scan.** `research_feasibility.md`. For each scan, what a team of four can get working in six hours, what an agent should pre-build, and the data sources with their access terms and free tiers: SEC EDGAR full-text search and XBRL frames for comps, Akta's API or MCP, Crunchbase's free tier, You.com and Tavily, GitHub's API, arXiv, the HN Algolia API, Product Hunt, app store listings, Whisper (local or API) and ffmpeg for the video scan, pdf and spreadsheet parsing for the data room. Which pieces have an official API and which do not. What a synthetic data room should contain and how to plant red flags in it.

Writers, after research, into `docs/ongoing/` unless named otherwise:

- **W1, product brief.** `PRODUCT_BRIEF.md`, in the charter's section order, and `PERSONAS.md` (one persona per problem, say, do, pay, ordered by rating). Written to the overview page's recommendations.
- **W2, brand.** `BRAND.md`: how Tricorder talks in the readout, the demo, the pitch to judges and any post. The name's origin and its one-paragraph trademark note. Words we use and avoid. The claims we make and where each came from. The $150 social content prize is a reason to write the posting voice too.
- **W3, roadmap and architecture.** `ROADMAP.md` with three horizons (before Saturday, Saturday, after), each slice with Waits on, Includes, Done when, Who (a teammate, an agent, or Ken), and Hours for a Saturday slice; a Saturday run of show, hour by hour, including when the demo is frozen and rehearsed. `ARCHITECTURE.md`: the stack recommendation, the module boundary (each scan is a function from inputs to a typed result with sources), the readout format, environment variables.
- **W4, frameworks.** `FRAMEWORKS.md`: every analysis the scans run (lean canvas, jobs to be done, business model canvas, Porter's five forces, SWOT, TAM/SAM/SOM, unit economics, cohort and churn checks, ARR definition checks, burn against hiring plan, deck-against-model reconciliation, comp selection rules, founder-market fit, a passion and commitment rubric from public signals), each with its inputs, its output shape, the questions it asks, and how the readout scores it. Written so a builder can turn one entry into one prompt and one schema.

Critics, after the writers, into `docs/features/20261022.01_hackathon_plan/`:

- **C1, the judge.** `critique_judge.md`. Reads everything as a VC judge would. Is this a company, not a project? Would a partner trust the first pass? What wins and what loses on the day.
- **C2, buildability.** `critique_buildability.md`. Can this team build the Saturday slices in six hours? Which slice breaks first, and what to cut.
- **C3, the data room and the demo.** `critique_demo.md`. Does the synthetic data room make the demo land? Are the planted flags the ones the organisers named? Is the readout the thing shown, and does the demo fit five minutes?

Then the orchestrator writes `00_overview.md`: the top of the plan, the decision cards, the Saturday run of show, and the board rows.

Added 2026-10-22 at 10:17 AM:

> and it suggested https://www.sec.gov/edgar/search/

So the comps data starts with EDGAR full-text search ([sec.gov/edgar/search](https://www.sec.gov/edgar/search/)) alongside the XBRL frames API. The feasibility research (R3) covers both: the full-text search for finding filings by business description, the frames and company-facts endpoints for pulling the numbers a comp table needs. EDGAR asks for a descriptive User-Agent header with contact details and limits requests to ten a second; R3 states the current rule with its link.

Added 2026-10-22 at 10:18 AM, the organisers' instructions for this week, which Ken pasted with "our basic setup does this, but this is a reminder in the prompt":

> Deal Flow works differently. On Saturday you only build. Everything a founder does before writing code happens this week:
>
> Pick a track and a team. Teams can be up to four people.
>
> Trying talk to a few people who have the problem: VCs, platform leads, LPs.
>
> Map the market: who already sells to them, what they charge, and where they fall short.
>
> Write a one-page founder brief: problem, customer, business model, and the one workflow you'll demo.

Settled, and it changes three things:

- **The founder brief is a deliverable.** One page: problem, customer, business model, and the one workflow we demo. A fifth writer (W5) writes it as `docs/features/20261022.01_hackathon_plan/founder_brief.md` from the product brief, the landscape research and the roadmap's demo slice, in the organisers' four headings and nothing more, and the orchestrator links it from the overview page. Ken edits it in his own words before Saturday; it is the thing he hands the judges.
- **Saturday is build-only, so this week is not.** The recommendation on the "how much agents build before Saturday" card becomes: no product code before Saturday. This week's work is the research, the interviews, the market map (R2 is exactly "who already sells to them, what they charge, and where they fall short"), the founder brief, the synthetic data room (the tracks document says to bring it), the API keys, and the frameworks doc, whose entries are the prompts and schemas the team types in on Saturday. The roadmap's before-Saturday horizon holds no code slice unless Ken overrules on the card. The critics weigh whether a repo skeleton (empty app, CI, folder layout) counts as code.
- **The landscape research answers the organisers' question in their words.** R2's table has the columns who they sell to, what they charge, where they fall short.

Added 2026-10-22 at 10:26 AM:

> we're going to need to simulate a "data room" whatever that is. we should look into that

Settled: the synthetic data room gets its own research track, R4, `research_data_room.md`, beside the others. A data room is the set of documents a startup shares with investors during diligence (the deck, the financial model, the cap table, customer contracts, metrics exports, team bios, legal documents), usually in a shared folder or a DocSend or Carta room. R4 finds out what a seed and Series A data room contains in practice (the folder structures funds and accelerators publish, what DocSend and Carta rooms look like, what founders are told to put in one), what an associate reads first in a first pass, and then designs ours: the file list, the fictional company, the planted red flags (the four the organisers name plus the ones R1 finds people regret missing), how each flag is planted so a script can find it, and how to generate the files this week with scripts (the spreadsheet with its cohort tab, the deck as a PDF, the hiring plan, a two-minute pitch video script Ken can record on his phone). The organisers say to bring the data room, so generating it before Saturday is allowed and expected. R3 keeps its short section and points to R4.

Added 2026-10-22 at 11:20 AM:

> we'll want to be able to connect to your email to automatically pull out emailed pitch decks. maybe we can even kick off the diligence process before you even ask, just from an inbound

Settled:

- **The inbox is an input.** Tricorder connects to the investor's mailbox (Gmail and Outlook through their official APIs, or a forwarding address such as deals@ for the first version) and pulls pitch decks out of inbound mail: PDF attachments, and DocSend, Google Drive, Dropbox and Notion links. The product brief (W1) adds it under What it does as an input alongside the uploaded data room. The feasibility of each path (Gmail API scopes and the verification Google requires for a restricted scope, Microsoft Graph, a plain forwarding address through a mail-receiving service, DocSend links that need the viewer's email and cannot be fetched blind) goes in the architecture doc (W3), with the forwarding address as the recommended first version because it needs no OAuth review.
- **Diligence starts on the inbound, unasked.** When a deck arrives, the scans run and the readout is ready before the investor asks for it. The investor opens the email and the readout is one click away, or the readout is the reply. This is the "before you even ask" moment, and it answers the voice-of-customer finding that the slow part is gathering, not writing: the gathering is done by the time the person looks. The roadmap (W3) carries it as a slice; the critics (C3) weigh whether "forward the pitch email, get the readout" should be the one workflow we demo on Saturday, against uploading the data room, and the overview page carries a card. The demo can show it with a forwarded email on stage even if the inbox connection itself is a later slice.
- **Where the data goes is part of the design.** The landscape research found judges reward plain answers on where the data goes, and the voice-of-customer research found funds will not let portfolio and deal data leave the firm. An inbox connection makes that question sharper. The product brief states the rule: the mailbox is read for decks only, nothing is stored beyond the readout and its sources, and the investor can see and delete everything pulled. The brand doc gives the sentence that says this on the page.

Added 2026-10-22 at 12:55 PM, as a comment on the product brief's "What it is" paragraph, which said the readout opens with the places the numbers disagree:

> no, that's not the starting point. we're looking to create an overview, show which pieces look strong, and which pieces look weak, and allow easy drill downs to verify and corroborate all data

Settled, and it replaces "disagreements first" as the shape of the readout and the edge:

- **The readout starts as an overview.** The first screen is the whole company in pieces (traction and revenue, retention, burn and runway, unit economics, customers, market, comps, team, the pitch itself), each marked looking strong, looking weak, mixed, or not enough in the room, with the reason in one line. It is a scorecard a partner reads in a minute, not a list of problems.
- **Strong pieces count as much as weak ones.** A first pass is a picture of the company, not a hunt for faults. A number two independent sources agree on is shown as corroborated, and that is what makes a piece look strong.
- **Easy drill-downs.** From a piece, one click opens the claims behind it. From a claim, one click opens its source in place (the cell, the slide, the clause, the video second) and every other source that corroborates or contradicts it. Verifying any number takes clicks, not a data-room hunt.
- **Disagreements and red flags stay, one level down.** A disagreement between sources, or a planted red flag, is one of the reasons a piece reads weak; it sits inside that piece's drill-down. The red-flag engine still runs; its output feeds the overview.
- **The edge** is the overview plus the corroboration trail: a partner sees at a glance what is strong and what is weak, and can check any number in two clicks. Sourcing alone is still table stakes.
- **The demo** opens on the overview for Hollis Voice, then drills into the weakest piece (revenue: the four ARR numbers from video, deck, model and billing rows) and one strong piece, showing corroboration both ways. The product brief, brand, roadmap, frameworks, founder brief and the overview page's cards follow this.

Added 2026-10-22 at 1:09 PM: Ken edited the product brief's "What it is" paragraph himself. His sentences, as applied:

> Tricorder reads everything about a startup, from its pitch deck and video to its financials to its online presence. It runs a set of scans, each a piece of first-pass diligence. It ends in a readout that gives a partner a detailed understanding of what's great about the business, and where the red flags are. The readout starts with the best green flags and the worst red flags. Then it breaks into the detail.

Settled, and it refines the 12:55 block:

- **The first screen is the best green flags and the worst red flags.** A short headline list: the strongest corroborated positives and the most serious problems. A green flag is as much the product as a red flag.
- **Then the detail**: the piece-by-piece overview (strong, weak, mixed, not enough in the room), then each piece's claims, then each claim's sources with what corroborates or contradicts it.
- **The inputs are everything about the startup**: the deck, the video, the financials and its online presence, not the data room alone.
- **The pitch line** becomes "Point it at a startup, get a readout: the best green flags, the worst red flags, and every number two clicks from its sources."

Added 2026-10-22 at 1:12 PM: Ken edited "What it is" again. His sentences, as applied:

> It runs a set of scans and analyses, creating a readout that gives the operator a detailed understanding of what's great about the business, and where the red flags are. This is not a final document, but something that the operator can actively dig through, drill down, and even steer, if they think areas need to be rewritten.

Settled:

- **The person using it is the operator.** Write "the operator" where the docs say "the partner" or "the associate" about the person working in the readout. The buyer (partner or principal) and the personas stay as they are.
- **The readout is a working surface, not a final document.** The operator digs through it and drills down, as before.
- **The operator can steer it.** When the operator thinks a section is wrong or thin, they say so on that section (a comment or a short instruction, such as "rewrite the market piece using only the competitor filings" or "treat the pilot as non-recurring"), and Tricorder reruns the analysis behind that section and rewrites it, keeping the sources and showing what changed. The scripts' numbers do not change because someone asked; a steer changes what is read, how it is grouped or how it is worded, and any change in a verdict shows the claim that moved it. This is the same live-review loop Ken uses on Lahe pages.
- **What it does** gains a "Steering the readout" feature. The roadmap carries it as an after-Saturday slice unless the critics think a single steer on stage (one section rewritten from one instruction) is worth a Saturday slot; the overview page gets a card. The architecture gets the shape: a steer is an instruction on a piece, the affected scans rerun on that piece's inputs, and the new piece replaces the old one with a visible diff.

Added 2026-10-22 at 1:21 PM, after Ken flagged "R1's" on the personas page ("we do not know what R1 is"):

- **The labels R1 to R4, W1 to W5 and C1 to C3 are for this brief only.** No document a person reads cites them. Name the research by what it is ("the voice-of-the-customer research") and link it the first time it appears in a file. A reference such as "row 11" says which table it points to. Every agent briefed from here on gets this rule.

Added 2026-10-22 at 1:24 PM, as a comment on the personas page:

> you're mixing concepts. User vs buyer is important when you're figuring out what marketing value props you need. but say/do/pay is about how people solve their problems, and identifying what evidence, what quotes, what behaviors, carry the most signal and therefor should make it into your value prop. say/do/pay is NOT about who is using your product vs paying for it

Settled, and it binds every writer:

- **Say, do, pay** rates how people deal with a problem today: what they say about it, what they do about it, what they spend (money or something given up) to solve it. It decides which problems and which quotes carry the most signal, and so what goes into the value proposition. It says nothing about who uses or buys Tricorder.
- **User and buyer** is a separate marketing question: whom each message speaks to. It lives in its own section and never sits in a rating, a persona's rank or a say, do, pay line.

Added 2026-10-22 at 1:27 PM, on the angel evidence:

> so effectively he IS doing due dilligence, just by proxy. he's letting yc do the diligence and then assuming their diligence is correct. what that means is that an angel still wants diligence, they just have less time for it. it's not that its thin evidence, i just disagree with your take

Settled: angels want diligence and lack the time. Giving up upside to YC, following a lead, splitting with co-investors and becoming an LP are diligence bought by proxy. That is pay-layer evidence for the problem Tricorder solves, not avoidance of it.

Added 2026-10-22 at 1:32 PM, as a comment on "ARR that is not recurring" in the voice-of-the-customer research:

> this is good. we should look for this specifically, but also any other accounting mislabeling

Settled: the red-flag engine checks ARR that is not recurring by name, and also a family of accounting mislabels, each a number filed under a label it does not earn. The frameworks doc gets an "Accounting mislabels" entry listing each kind with its mechanical check, starting with: non-recurring revenue counted as ARR or MRR; bookings or billings shown as revenue; gross merchandise value or pass-through money shown as revenue (gross against net); cost of revenue filed as operating expense, which inflates gross margin; contractors left out of headcount and burn; capitalised costs that keep spend off the P&L; deferred revenue counted as earned; and one-time fees counted in recurring metrics. Each kind names which data-room file and column a script reads, and what a gap looks like when the room does not hold that file.

Added 2026-10-22 at 1:33 PM, as a comment on faked documents in the voice-of-the-customer research:

> we can't identify faked books, but we can identify differences in reporting

Settled: no document claims Tricorder detects fraud or fake books. It finds differences in reporting between files and against the outside world, and shows each one. A fake that is consistent across every file gets through; say so where it matters (What it is not, the pitch's answer to "can it catch fraud").

Added 2026-10-22 at 1:34 PM, as a comment on "Ken's interviews need to get that number":

> we're only doing online research

Settled, and it replaces the interviews: there are no interviews before Saturday. Every place that says "the interviews should ask", "Ken's interviews", or waits on interviews changes to online research. The gaps the interviews were meant to fill become a fifth research track, `research_gaps.md`, done online: how long a first-pass memo takes and which part is slowest, whether angels would pay for a first pass of their own and what it is worth per deal, how data rooms reach investors and what they open first, regret stories about hidden churn and about burn against the hiring plan, and what funds pay for first-pass diligence in their own words. The interview sheet is retired. The board row for interviews closes with that reason.

Added 2026-10-22 at 1:36 PM, as a comment on the competitor that turns a data room into a sourced memo:

> this is validation of our idea. we do not need to make ourselves substantially different than this competitor, just add some extra stuff

Settled: the competitors that already turn a data room into a sourced memo validate the idea. Tricorder does that same core job and adds to it (the green-and-red-flags readout, the red-flag engine with accounting mislabels, fast cross-checking, and the scans beyond the room). No document frames sourcing as "no longer open ground" or calls the competitor something we must beat. Their strongest points plus ours is the method.

Added 2026-10-22 at 1:38 PM, as a comment on accelerators in the voice-of-the-customer research:

> accelerators are working at the earliest parts of the fundraising, like angels. funds are working at different stages. we should break our personas out by which stage they focus on, as that makes a difference in what is available about the company

Settled: the personas are grouped by the stage of company they focus on, because the stage decides what information exists. Earliest (pre-seed and accelerator applications): angels, accelerator screeners, pre-seed funds; little or no data room, so the deck, the founders, a video and the company's online presence carry the first pass. Seed: seed funds' partners and associates; a deck, a model, a cap table and some metrics. Series A: Series A funds and corporate VCs; a full room with monthly financials, cohorts and contracts. Each stage section says what is usually available (from the data-room research's stage table), which scans matter most at that stage, and which personas sit there. Say, do, pay stays per persona and is unchanged in meaning.

Added 2026-10-22 at 1:52 PM, as a comment on the faked bank records in the voice-of-the-customer research:

> we can maybe claim to do automated bank reviews with one of the banking-connector services that exists now, but we can't really demo that unless there's like a developer demo account

Settled: a bank check is a roadmap item. The investor, with the founder's consent, connects the company's bank account through a banking connector, and Tricorder compares deposits with the revenue rows and outflows with the burn in the model. It is a check for differences in reporting (the 1:33 PM rule), not fraud detection. A demo is possible: Plaid's Sandbox supports custom test users with configured accounts and up to about 250 transactions ([Plaid docs](https://plaid.com/docs/sandbox/user-custom/), saved under raw/feasibility/plaid/), so the data-room generator can write a Hollis Voice bank feed whose deposits disagree with the revenue file in one planted place. After Saturday by default; the overview page gets a card on whether it is worth a Saturday slot.

Added 2026-10-22 at 1:53 PM, as a comment on founders counting pilots, one-time deals and unactivated contracts as recurring revenue:

> allow contracts as an input and analyze for gaps like cancellation periods

Settled: customer contracts are a first-class input, uploaded with the room or on their own. A "Contract terms" entry reads every contract for its terms (start and end, length, notice and cancellation period, termination for convenience, auto-renewal, pilot or trial terms and any duty to convert, price, discounts, payment terms, and clauses such as exclusivity or change of control) and compares each with how the contract is counted (ARR, MRR, customer concentration, the model's revenue). A gap is any place the counting outruns the paper: a contract the customer can cancel in under 90 days counted as a year of ARR, a pilot with no duty to convert counted as recurring, an auto-renewal the founder treats as certain, a signed contract that has not gone live counted as revenue. The existing ARR and concentration entries keep their checks and point to this one.

Added 2026-10-22 at 1:54 PM, as a comment on burn out of line with progress:

> we can also have a list of things to ask for, like current burn, current contract language

Settled: the readout ends with an ask list, the documents and numbers the operator should request from the founder. Every gap ("not in the room") and every weak piece that more information could settle becomes one line: what to ask for, why (the claim or gap it would settle), and which piece it feeds. Examples: current monthly burn and the bank balance behind it; the current contract language for the largest customers and any pilot; the hiring plan with start dates; monthly revenue by customer. A script builds it from the gaps' `would_need` field and the weak pieces' reasons, so it costs little on Saturday. The operator can copy it into an email to the founder. This is also the "get more info" steer in reverse: what Tricorder cannot fetch, it asks the operator to request.

Added 2026-10-22 at 1:56 PM, as a comment on "and every checklist does" in the voice-of-the-customer research:

> another reference to a checklist. we need to have a checklist of info

Settled: Tricorder keeps one diligence checklist, `docs/ongoing/CHECKLIST.md`, built from the published checklists the research already read (the data-room research's 30-document table and its sources: Cooley GO, Kruze, Visible, Hustle Fund, CRV, a16z, Peony, Papermark, BCV) plus the outside-world items (the associate's ten tabs) and the red flags. Each item: what it is, the stage it is expected at (pre-seed, seed, Series A), where it comes from (a data-room document, an outside source, or the founder), which scan checks it, which readout piece it feeds, and which published checklists name it, with links. The checklist drives three things: what the scans look for, the readout's coverage (which items were found, checked, or missing), and the ask list (every missing item expected at the company's stage becomes a request). A script builds a CSV of the items and their counts, so the doc's counts come from it.

Added 2026-10-22 at 1:58 PM, as a comment on who the first-pass memo is for:

> great, so we are HELPING to write this memo. we need to get a sample memo or many of them, so we have a template for what this memo looks like

Settled: Tricorder helps the operator write the memo for the partners' meeting. A research track collects real investment memos that funds have published (for example the memos Bessemer Venture Partners publishes, and memos other funds or their partners have shared) and memo templates funds and accelerators publish, saves each, and finds the sections they share. From that, `docs/ongoing/MEMO_TEMPLATE.md` defines Tricorder's memo: its sections in order, what each holds, which readout pieces and checklist items fill it, and how the top green and red flags, the gaps and the ask list appear in it. The readout's export is a draft of that memo with every claim still linked to its source.

Added 2026-10-22 at 2:00 PM, as a comment on investors who discard the glossy memo and go to the raw numbers:

> this also means that we can deliver interactive memos that allow the readers to drill down as well

Settled: the memo Tricorder helps write is interactive, not a static document. The partners who read it can drill down from any line to the claims behind it and from any claim to its source and the sources that agree or disagree, the same two clicks the operator has in the readout. It still reads as a normal memo top to bottom; the drill-downs sit behind it. A static PDF export stays available for funds that need one, with every claim footnoted to its source.

Added 2026-10-22 at 2:01 PM, on the same paragraph:

> in some ways the person prepping the memo may do steering and creating their final product, but the person reading may also want to tweak the financial model a couple ways and see what they can get it to look like for their own udnerstanding. so even the "final" memo may need to be something that can be independent to each user, and then steered

Settled:

- **Every reader gets their own copy to steer.** The operator's memo is the shared version. Each partner who opens it can steer their own copy (rewrite a section, ask for more information) without changing anyone else's. Their copy says what they changed and from which version.
- **Readers can tweak the model.** A reader can change a few assumptions in the financial model (for example churn, price, hiring pace, the pilot counted or not) and see what the numbers become. Scripts recompute from the company's own model and rows; the source files never change. Every tweaked number is marked as the reader's scenario beside the company's figure and Tricorder's rebuilt figure, so nobody mistakes a what-if for a fact.
- The product brief's steering and memo features, the memo template and the roadmap carry this; the architecture gets the shape (a shared memo version, per-reader overlays of steers and scenario inputs, recomputation by the same scripts).

Added 2026-10-22 at 2:05 PM, as comments on angels borrowing a lead's diligence and on YC's volunteer readers:

> there's something interesting here. we can make this multiplayer while building, so that more than one person can accelerate the diligence process. i'm not sure that would work though

> another share the work example

Settled: a `multiplayer` slice on the roadmap, marked uncertain. Several people (a lead, teammates, co-investors the lead invites) build one readout at once and split the checklist; each person's work carries their name. Before building it, an online check of how syndicate leads and angel groups split diligence today decides whether it goes ahead.

Added 2026-10-22 at 2:19 PM, on the associate's quote "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable.":

> this becomes a roadmap feature

Settled: the `deck-vs-books` slice checks deck revenue against the P&L period by period, and flags a deck that shows only part of the company's history (a chart that starts after the first revenue month, skips months, or hides a dip).

Added 2026-10-22 at 2:19 PM, on the junior VC who lost momentum after weeks sifting data:

> speed is important. kick these off as early as possible

Settled: every scan starts the moment its input exists (the company name, the deck, the model), not after the whole room arrives. The readout fills in as results land, each piece shows running, done or waiting on an input, and the operator sees the first green and red flags early. The `inbound-unasked` slice carries it.

Added 2026-10-22 at 2:33 PM, correcting the 1:09 PM block's pitch line: Ken chose the pitch at 10:34 AM in the team-workshop session (board row TRI-new-pitch): "Point it at a startup, get a readout. Tricorder takes any data: decks, videos, spreadsheets, data rooms. It reveals insight you can trust, every claim sourced." That is the line. The 1:09 PM line was this session's proposal and Ken never chose it; it survives only as an optional line for the readout's first screen.

Added 2026-10-22 at 2:35 PM, as a comment on the personas table:

> ok, these are our two primary personas. the others are secondary. we're focusing on seed and series a funds, and the people who prep the memo and the people who read the memo

Settled: the primary personas are the associate at a seed or Series A fund who prepares the memo, and the partner or principal who reads it and decides. Angels, accelerator screeners and corporate VCs are secondary. Everything built first serves the two primary personas.

Added 2026-10-22 at 2:38 PM, as a comment on the 30-document table in the data-room research:

> ok this is a great list and we're focusing on seed and series a so we need to have custom reference documents written for every single one of these. we will need to send out research agents to uncover the pitfalls and red flags and green flags for each of these documents

Settled: one reference guide per data-room document a seed or Series A room can hold, 33 in all (the research table's 30 plus use of funds, non-customer material agreements, and AI and data governance from DocSend's checklist). Each covers what it is, what changes between seed and Series A, what a first pass checks, green flags, red flags and pitfalls with sources, how Tricorder checks it (script, model reading, or left to the operator), the pieces it feeds, the ask-list line if missing, and what the Hollis Voice room holds. Six research agents write them into `docs/reports/20261022.03_document_guides/` from the brief there. The checklist and FRAMEWORKS draw on them; the roadmap carries the work of turning their proposed checks into checks.

Added 2026-10-22 at 2:41 PM, as a comment on the research's scan order (read the deck first, its claims are the list to check):

> this is a feature workflow that needs to be documented. extract claims from the pitch deck and video, and see if the other docs support

Settled: the claims workflow is documented in `docs/ongoing/diagrams/claims_workflow.md` (extract, normalise, find evidence, compare by script, label supported, contradicted or unsupported, feed the pieces), linked from ARCHITECTURE.md, and built by Saturday's deck and video scans for the planted flags and by the `claim-support` roadmap slice in full.

Added 2026-10-22 at 2:44 PM, as a comment on the data-room research's company options:

> oh, but we should make up fake data room documents we can use for real startups. we need to be able to run our internet scrape live, and we should do it on, like 2-3 real YC companies from spring

Settled, with one safeguard:

- **Two or three real YC companies from the spring 2026 batch** get synthetic data rooms, so the outside-world scan (the associate's ten tabs) runs live on real public footprints during the demo, while the room documents are invented.
- **Safeguard.** An invented room under a real company's name must never read as a claim about that company. Every page of those rooms carries "Synthetic test document. Not this company's data." The numbers are invented and plausible, anchored only to what the company has published. Planted problems are named test plants in the answer key and on screen, and the demo says so out loud. The real company's public facts (name, product, founders' public bios, any announced round) come only from public pages, saved with links.
- **Ken picks the companies.** A research agent proposes candidates with their public footprint; the overview page carries a card; the rooms are generated only after Ken chooses.

Added 2026-10-22 at 2:46 PM, on the same comment:

> yes they say don't use real confidential data, but to do internet scraping we have to use real companies. we'll just fake the data room

> and we should actually set up a few different data rooms that will allow us to highlight different problems. the data rooms will need to be a little bit templated, so we can swap in new names on the fly, but we should make data rooms with hidden isseus in them, based on the problems we saw in the reserach. this can be on the roadmap

Settled: the generator becomes a template engine (`room-templates` on the roadmap): a company profile swapped in on the fly, a library of hidden issues drawn from the research's problems, green flags and decoys, and saved recipes, one per problem story. Real-company rooms are built from it with the 2:44 PM safeguard.

Added 2026-10-22 at 2:49 PM, Ken's closing note on the data-room research:

> ok i'm done here. make sure my feedback propagates to all the correct docs. we want to have a list of YC companies and we'll pair them with fake data rooms and run live demos on them

Settled: the demo pairs real YC companies (from a list Ken approves) with fake data rooms built from the room templates, and runs live: the outside-world scan reads each real company's public footprint during the demo, while the room's documents are invented and labelled synthetic. Hollis Voice and the second invented company stay as the controlled rooms whose planted flags are known. The product brief's demo section, the brand doc's pitch to judges, the founder brief's workflow, the roadmap's demo slices and the overview page's demo cards follow this.

Added 2026-10-22 at 2:51 PM, a note on the overview page:

> for the data room prep, we'll need to ask me to read a few scripts into a video. i'll just read them flatly, nothing crazy

Settled: Ken records the pitch videos himself, one flat reading per room's script (Hollis Voice, the second invented company, each approved real-company room). This replaces the demo critic's suggestion of an off-stage voice. On stage the clip plays as audio over the deck slides with captions. Each room's generator writes its script; the board row lists them.

Added 2026-10-22 at 2:56 PM, on the landscape research's three most useful sponsor tools:

> yeah let's make sure that these are in our roadmap and features. we won't get access to them until day of but we can do the other stuff ahead of time

Settled: Akta, Crunchbase and the Nicrron gateway are features (product brief, "The sponsor tools") and a this-week roadmap slice (`sponsor-adapters`): an adapter per sponsor built against its published docs with sample responses and an off, sample or live switch, so Saturday morning is pasting keys and flipping switches inside the existing 9:00 to 10:30 window.

Added 2026-10-22 at 2:57 PM, on "a named buyer who pays" in the landscape research's list of what judges reward:

> no we won't have that. this is about a demo

Settled: Tricorder will not have a paying customer or a named buyer by Saturday. The pitch says who would buy it (a fund, per seat) and never implies a customer.

Added 2026-10-22 at 3:00 PM: Ken rewrote the end of the product brief's "What it is". His words, as applied:

> An associate will review and steer the memo as needed, creating the deliverable memo.
>
> The deliverable memo is shared with others within the firm, but rather than a fixed document, this is still interactive, allowing drilldowns, and even allowing partners to alter growth models and see how they could change, themselves.

This matches the settled flow: the associate (the operator) steers the readout into the memo; the partners read an interactive memo and run their own what-ifs on the growth model.

Added 2026-10-22 at 3:01 PM, as a comment on the product brief's "Who it is for":

> completely delete and start this section over. i've narrowed in to seed and series A firms, associates preparing, and partners reading.

Settled: "Who it is for" is rewritten from scratch to seed and Series A firms and their two users, the associate who prepares the memo and the partner who reads it. Angels, accelerators and corporate VCs are no longer named in the product brief's audience; PERSONAS.md keeps them as secondary.

Added 2026-10-22 at 3:01 PM, on the product brief's "The problem":

> don't reference the organizers. write a very brief intro to the problems you're listing

Settled: product docs do not cite the organisers as a source for the problem; they speak from investors' own words. "The problem" opens with a one-sentence intro to the list.

Added 2026-10-22 at 3:02 PM, on the product brief's problem list: Ken renamed the first bullet "The red flags investors name most are financial sloppiness." and said:

> this is the brief. we can link to research, but counts like this do not belong in the brief

Settled: the product brief states findings and links to the research; research counts, row numbers and script names stay in the research files. This applies to every ongoing doc written for a reader (product brief, personas summary, brand), not to FRAMEWORKS or the checklist, whose numbers are working data.

Added 2026-10-22 at 3:07 PM, on the product brief's first problem:

> this is still more of a feature level detail. the problem is really that due diligence is required to understand if you've got a good investment, and lying or stretching the truth is very common because so much money is on the line

Settled: the product brief states problems at the level of the investor's situation, not the checks Tricorder runs. The first problem is that diligence is how an investor learns whether an investment is good, and stretching the truth is common because so much money is on the line. Specific red flags (padded ARR, numbers that disagree) belong in the feature and framework docs.

Added 2026-10-22 at 3:10 PM, on the product brief's jobs to be done:

> these are user stories, which belong in feature documentation. jobs to be done are the high level jobs
> - deploy capital to trustworthy founders
> - deploy capital to companies that will create ROI
> - deploy capital to companies that will become extremely valuable
> - understand the risk profile of a company
> - understand the fundamentals of a company
> - communicate the fundamentals and risk to a group for a group decision

Settled: the product brief's jobs to be done are Ken's six high-level jobs. The "when I ..., I want ..." lines are user stories and live in `docs/ongoing/USER_STORIES.md`, grouped by the associate, the partner and secondary personas.

Added 2026-10-22 at 3:11 PM, on the bank account input:

> we can try this, we just need to see if one of these connectors has a trial account and test data. or we could rig it up and fake it, just say we'd connect this here, and here's a sample bank statement you might get

Settled: try Plaid's sandbox first (free test accounts and custom test data); if it is not ready, the room carries a labelled sample bank statement and the readout shows where the connected account would plug in. The overview page's bank card gains that option.

Added 2026-10-22 at 3:13 PM, on the product brief's detailed feature sections:

> yo this is a BRIEF. put all this in roadmap and feature documentation, not in the brief. i need this document to be, you know. BRIEF

Settled: the product brief is short (target under about 900 words). It holds what it is, who it is for, the problem, the jobs to be done, a one-line list of what it does, and the essentials of what it is not, its principles, its commitments and how we know it works. Feature detail lives in `docs/ongoing/FEATURES.md`, user stories in `USER_STORIES.md`, build order in `ROADMAP.md`, open decisions on the overview page.

Added 2026-10-22 at 3:15 PM, a sentence Ken added to the product brief's Inputs:

> While compiling the data room, there are quick ways to send messages to the company asking them for information, with guidance on what they should submit.

Settled: a `founder-requests` roadmap slice drafts requests from the ask list, each with guidance from the document guides on what to submit; the operator sends them from their own email.
