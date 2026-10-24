# Tricorder

Point it at a startup, get a readout.

## Inspiration

Track 2 asked for better diligence. We started with the people who do it.

An associate at a seed fund described the first pass: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([Startups Magazine, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). The same associate reviews about 500 decks a year and goes deep on about 15.

The work is slow. A survey of 885 VCs found the average firm spends 118 hours of diligence on a deal ([NBER working paper](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf)). Investors say the slow part is getting the information, not writing the memo.

And the numbers often disagree. A fund's guide puts it plainly: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([CRV, Aug 2026](https://www.crv.com/content/what-is-a-data-room)).

So we built the first pass: gather everything, check every number against every other source, and show where each claim came from.

## What it does

Point it at a startup, get a readout. Tricorder does the first pass of diligence for seed and Series A funds. The associate runs it and steers it into a memo. The partner reads the memo and decides. Tricorder never says invest or pass.

**Working in the code today**, on synthetic data rooms:

- Reads the room: the deck, the financial model, the cap table, the ledgers and the contracts.
- Runs red-flag checks as scripts: deck revenue against the books, accounting mislabels, churn hidden in the cohort tab, and contract terms read against how each contract is counted as revenue.
- Ties every claim to its source with the exact quote. A script finds that quote again in the file. A claim whose quote is not found goes to a "could not verify" box.
- Builds the readout: the top green and red flags, nine pieces of the company each marked strong, weak, mixed or not enough in the room, the gaps, and an ask list for the founder.
- Lets the associate steer a piece in one plain sentence. The piece rebuilds and shows what changed. A steer never changes a script's number.
- Drafts the request to the founder. When the reply's files arrive, the scans that were waiting rerun.
- Exports a memo page and keeps every version of a readout in a per-fund store.
- Shows the readout in a React web app and an Expo (React Native) app.

**In the clickable prototype**, which is the reference the team is building to:

- Paste a company's URL. It matches against 193 saved YC Spring 2026 companies and sets itself up.
- A first readout from public sources before any data room: website, Hacker News, App Store, SEC filings, founders, comps and market signals. Ploy and Sazabi use real saved data; other sections are placeholders.
- The data-room request as a checklist the associate edits, with a live draft.
- The room arriving, with its flags merged into the working page.
- An interactive memo for the partner, with drill-downs, agree, disagree, what-if and a chat that points into the memo.

Every data room is synthetic, and every page says so. The real companies' public data is real.

## How we built it

**The team.** Ken St. Clair (captain, product), Benjamin (TypeScript port, web and React Native apps), Kimmy (domain expert, expert knowledge) and Tirth.

**Research first.** Before code, we wrote up what investors say about diligence, the competing tools, and what a seed or Series A data room holds. That gave us the two personas, a 193-item diligence checklist, and a catalog of every check the scans run.

**Synthetic rooms with answer keys.** A generator writes the test rooms. Hollis Voice, an invented Series A company, has 17 files with 8 planted red flags, 3 decoys and 3 green flags. Brasswick, an invented seed company, has 14 files and 5 red flags. A clean copy of Hollis Voice has none. The answer keys sit outside the rooms, and only the scorer reads them.

**Scripts for math, a model for words.** Each scan is Python and writes its claims as JSON. Scripts compute every number. Claude reads only what a script cannot, such as a contract clause, and returns structured output with the exact quote it relied on. A merge step turns the claims into the readout.

**The TypeScript port.** At 11:00 AM we decided to move to TypeScript, and Benjamin started the port the same morning. Today's commits brought:

- a pnpm and Turbo workspace;
- a typed tRPC gateway, checked with Zod, over the Python API;
- TypeScript types generated from the Python models;
- the readout ported to an Expo (React Native) app, with a company research workspace.

The scans and the merge are still Python, served by FastAPI to the React web app.

**Expert knowledge.** Kimmy wrote how an investor reads traction and revenue, and burn and runway: what to check first, how traction differs for B2B and games, and what to ask the founder. Her files now go into the model's prompts for the deck slide reader and for steering.

**Agents in parallel.** Ken and Benjamin each ran AI coding agents, which left notes for each other on a shared board in the repo. The repo has more than 500 commits since Thursday.

## Challenges we ran into

- **Real data rooms are confidential.** We wrote our own, with planted problems and decoys. For real YC companies we pair real public data with a synthetic room, and every page of the room says it is synthetic.
- **Keeping the model honest.** The model API would not return citations together with structured output. So every claim carries its quote, and a script checks the quote against the file.
- **Scoring ourselves.** On a fresh run today, the engine finds 5 of 5 planted flags in Brasswick but only 2 of 8 in Hollis Voice. It misses a pilot counted as ARR, the deck's ARR against the model, burn against the hiring plan, customer concentration, gross margin, and cumulative sign-ups shown as active clinics. The checks for those are on the roadmap and not built yet.
- **Changing stack mid-day.** We moved to TypeScript partway through the day, with web and mobile apps on one core. The Python engine keeps running the demo until the port scores the same on every answer key.
- **Scope.** The roadmap has 57 slices. 13 are done and 10 are partly built.

## Accomplishments that we're proud of

- **No false alarms.** In today's fresh run, neither scored room had a decoy flagged, and the clean room raised no flags at all.
- **Every claim opens its source.** A claim either carries a quote a script found in the file, or it is set aside as unverified.
- **Steering that keeps the math intact.** The associate can reword, regroup or ask for more on any piece. The script's numbers stay on screen beside the change.
- **One backend, two apps.** The web app and the Expo app read the same readout through typed contracts generated from the Python models.
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
