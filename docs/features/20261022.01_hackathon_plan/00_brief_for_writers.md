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
