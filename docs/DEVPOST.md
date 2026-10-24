# Tricorder

Point it at a startup, get a readout.

## Inspiration

Due diligence on startups can take weeks, and this creates a slow down in momentum that can damage the relationship with the startups. But with millions of dollars on the line, it's important to know where your money is going and whether you're making a good investment.

An associate at a seed fund described the first pass: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([Startups Magazine, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). And a survey of 885 VCs found the average firm spends 118 hours of diligence on a deal ([NBER working paper](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf)).

Tricorder makes this process faster, more accurate, and facilitates decision making.

## What it does

Tricorder automates research and helps associates build the memo that will be the artifact used to decide whether to invest in a company or not.

**Tricorder's features:**

- Public research. Scrape the web to get public signals on a company.
- Data room analysis: the deck, the financial model, the cap table, the ledgers and the contracts. Expert knowledge is encoded to analyze existing documents.
- Request additional info: Send automated requests to founders for more info.
- Surfacing red flags: specific red flags are automatically bubbled up to speed up the due diligence process.
- Fully sourced. All claims are linked to documentation that can be examined.
- Builds the memo: collaborate with the associate to build a memo.
- Allow Principals to review and ask questions of the memo.


## How we built it

**The team.** Ken St. Clair (captain, product), Benjamin (TypeScript port, web and React Native apps), Kimmy (domain expert, expert knowledge) and Tirth.

**Research first.** Before code, we researched what investors say about diligence, the competing tools, and what a seed or Series A data room holds. That gave us the two personas, a 193-item diligence checklist, and a catalog of every check the scans run.

**Synthetic rooms with answer keys.** A generator creates fake data rooms. Hollis Voice, an invented Series A company, has 17 files with 8 planted red flags, 3 decoys and 3 green flags. Brasswick, an invented seed company, has 14 files and 5 red flags. A clean copy of Hollis Voice has none. The answer keys sit outside the rooms, and only the scorer reads them.

**The stack.** A React web app and a React Native (Expo) app share TypeScript types generated from the Python models. Both talk through a typed tRPC gateway, checked with Zod, to a Python API (FastAPI) that runs the scans and builds the readout. The workspace runs on pnpm and Turbo.

**Expert knowledge.** Kimmy wrote how an investor reads traction and revenue, and burn and runway: what to check first, how traction differs for B2B and games, and what to ask the founder. Her files go into the model's prompts for the deck slide reader and for steering.

## Challenges we ran into

- **Real data rooms are confidential.** We wrote our own, with planted problems and decoys. For real YC companies we pair real public data with a room we wrote.
- **Keeping the model honest.** The model API would not return citations together with structured output. So every claim carries its quote, and a script checks the quote against the file.
- **Scoring ourselves.** On a fresh run today, the engine finds 5 of 5 planted flags in Brasswick but only 2 of 8 in Hollis Voice. It misses a pilot counted as ARR, the deck's ARR against the model, burn against the hiring plan, customer concentration, gross margin, and cumulative sign-ups shown as active clinics. The checks for those are on the roadmap and not built yet.
- **Scope.** The roadmap has 57 slices. 13 are done and 10 are partly built.

## Accomplishments that we're proud of

- **No false alarms.** In today's fresh run, neither scored room had a decoy flagged, and the clean room raised no flags at all.
- **Every claim opens its source.** A claim either carries a quote a script found in the file, or it is set aside as unverified.
- **Steering that keeps the math intact.** The associate can reword, regroup or ask for more on any piece. The script's numbers stay on screen beside the change.
- **A clear workflow.** Eight steps, from a list of real companies to the partner's memo, and each slice of the roadmap serves one of them.

## What we learned

- **Disagreement is the signal.** Two sources that agree earn a small green flag. Two that disagree earn a big red flag.
- **Scripts should do the math.** A model that reads a number can misread it. A script that recomputes it can be checked.
- **The first pass starts before the data room.** The slow part is gathering, so Tricorder has to research the company from public sources and draft the request for documents.
- **The partner's memo has to stay live.** We built a PDF export early. On Saturday we decided the partner's memo cannot be a PDF, because the partner needs to drill in and steer it.
- **Traction means different things by business model.** Kimmy showed us that a B2B company proves demand with paying customers, while a game company may show wishlists and trailer views.

## What's next for Tricorder

- **Build the prototype's first steps into the app:** set up a company from its URL, research it live from public sources, and fill each section as its data arrives.
- **Finish the red-flag checks** that Hollis Voice still slips past.
- **Write Kimmy's knowledge for the other pieces,** and use it in the checks still to be built and in Tricorder's own financial model.
- **Give each partner their own copy of the memo,** with what-ifs on the growth model and a chat that points to the evidence.
- **Read the pitch video,** with each claim tied to its timestamp.
- **Check the bank account,** with the founder's consent, through Plaid's sandbox first.
- **Run a pilot with one fund** on real inbound deals. It will judge Tricorder on speed, on the flags the partner agrees with, and on whether it is worth paying for. We claim no time saving until that pilot measures one.
