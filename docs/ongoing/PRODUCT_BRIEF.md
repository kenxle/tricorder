# Product brief

## Charter

**What belongs:** What the product is, who it is for, and why. Sections, in this order: Charter, What it is, Who it is for, The problem, The jobs to be done, What it does, What it is not, The principles for choosing methods, Commitments, How we know it works. The principles and commitments that hold for every feature.

**What does not:** How anything works (ARCHITECTURE.md and diagrams). How it looks (STYLE_GUIDE.md). Each feature in detail ([FEATURES.md](FEATURES.md)). A feature's own reasoning (its folder under docs/features/).

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
- [FEATURES.md](FEATURES.md), for each feature in detail, the reasons behind each principle and commitment, and the measures in full
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

- [Reads everything about a startup](FEATURES.md#inputs) as it arrives: the deck, video, financials, contracts, inbox and online presence.
- [Asks the company for what is missing](FEATURES.md#inputs), with guidance on what to submit.
- [Opens the associate's usual tabs](FEATURES.md#what-tricorder-gathers-before-the-data-room-is-opened): traffic, reviews, investors, founders, and whether the story matches what's online.
- [Runs scans](FEATURES.md#the-scans) that flag problems in the numbers and the contract terms, and check every deck and video claim against the other sources.
- [Builds a readout](FEATURES.md#the-readout): the best green and worst red flags, then which pieces look strong or weak, with every number two clicks from its source.
- [Helps write an interactive memo](FEATURES.md#the-readout) that partners can drill into and run what-ifs on.
- [Lets the operator steer](FEATURES.md#steering-the-readout) any piece in one plain sentence.
- [More checks come after Saturday](FEATURES.md#later-checks).

## What it is not

- Not a sourcing database or a CRM.
- Not a replacement for the partner's judgment.
- Not confirmatory diligence.

## The principles for choosing methods

1. **We use deterministic checks for math, not model judgment.** A script decides that a number is wrong. The model reads only what a script cannot, such as a contract clause or a spoken number. Decisions are routed to Jev or decision models. Judgment is sent to LLMs.
2. **No real company's confidential data.** Every room is synthetic. A room under a real company's name is labelled synthetic on every page, and its planted problems are named test plants.
3. **Nothing is scraped against a site's terms.** No LinkedIn scraping. Reddit only from pages a person saved by hand. Official APIs wherever they exist.
4. **Personas and problems, with say, do, pay.** Every persona is a specific problem in that person's own words, and what people already pay to solve is what goes in the value proposition ([PERSONAS.md](PERSONAS.md)).
5. **The data stays with the investor.** Tricorder reads only what it is given, keeps only the readout and its sources, and the investor can see and delete everything it pulled.
6. **Always defer to operator steering and judgment.** When the operator says a section is wrong, thin or framed badly, Tricorder follows the steer and shows what changed. The scripts' own figures stay on screen beside any change, so the operator decides with both in view.

## Commitments

- **Every claim links to its source.** A claim without a source a person can open does not reach the readout.
- **Identify strengths, weaknesses, and gaps and call them out.** A piece looks strong when two independent sources agree on its number. A missing fact shows as a gap, never a guess.
- A steer or a what-if never changes a script's number.
- Tricorder reports its own misses against the answer key.
- A bank account is read only with the founder's consent.
- No scan logic before Saturday.

## How we know it works

On Saturday, investors and agent builders judge a live demo. Tricorder is scored against the answer key. After Saturday, a pilot fund [judges it on speed, flags the partner agrees with, and whether it pays](FEATURES.md#how-we-measure-it). No time saving is claimed until a pilot measures one.
