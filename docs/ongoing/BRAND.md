# Brand

## Charter

**What belongs:** How the product talks: tone, word choice and positioning. How we describe the product. Words we use and words we avoid. Key claims and where each came from.

**What does not:** Anything visual (STYLE_GUIDE.md). What the product does (PRODUCT_BRIEF.md).

**Level of detail:** Rules a writer can apply without asking. No history of past decisions.

**Sources:**

- [The writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)
- [The team-name workshop page](../reports/20261022.01_hackathon_sources/team_name_workshop.txt)
- [The organisers' problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)
- [Voice of the customer research](../reports/20261022.02_research/research_voice_of_customer.md)
- [Landscape research](../reports/20261022.02_research/research_landscape.md)
- [Data room research](../reports/20261022.02_research/research_data_room.md)
- [Ken's communication style guide](../../../personal/context/personal/communication_style.md)
- USPTO trademark records, linked in "The name's origin and the trademark risk" below
- The judge's and the demo critic's critiques ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), [critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md)), for the pitch's length, the margin's revenue base and the answer on a room we didn't make

## The name and the line

**The name is Tricorder.** It is settled and posted. This doc does not reopen it.

**The posted pitch** (on the Team Match Network since 10:04 AM on 2026-10-22, per the [workshop page](../reports/20261022.01_hackathon_sources/team_name_workshop.txt)):

> Point it at a startup, get a readout. Thesis-driven sourcing plus a first-pass diligence memo with every claim sourced.

**Proposed line for Saturday:**

> Point it at a startup's data room, get a readout. Red flags first, then comps and market signals, every claim sourced.

Why the change:

- Track 2 asks for three things: market signals, comps and red flags ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). The new line names all three.
- Sourcing is Track 1. The posted line spends its first words on it. The new line drops it.
- Red flags lead because a readout that puts what doesn't add up first is where Tricorder can differ. Five AI tools already claim to link every claim to a source ([landscape](../reports/20261022.02_research/research_landscape.md)), so "every claim sourced" stays but cannot carry the line alone.
- The first sentence keeps the posted rhythm, so the team card and the demo still sound like the same product.

**Decision for the overview page.** Recommendation: use the proposed line on the demo's first screen and in the founder brief. Leave the posted line on the network card; it does not need editing.

### The name's origin and the trademark risk

A tricorder is the handheld scanner from Star Trek, which is where the team-name workshop found it ([Wikipedia](https://en.wikipedia.org/wiki/Tricorder)); CBS Studios' own toy registration describes it as a device "used for sensor scanning, data analysis, and recording data" ([USPTO, Reg. 4194205](https://tsdr.uspto.gov/statusview/rn4194205)). CBS Studios Inc., which also owns the STAR TREK mark ([Reg. 1801165, via Gleanmark](https://gleanmark.com/trademark/uspto-74356106)), holds or has filed for TRICORDER in several fields. On the USPTO's own records, read 2026-10-22: a live registration for "educational services, namely, a competition to promote innovation and technology for health care" ([Reg. 5258520](https://tsdr.uspto.gov/statusview/rn5258520)); a live application for a model toy handheld scanning device, filed August 2023 ([Serial 98144748](https://tsdr.uspto.gov/statusview/sn98144748)); and a live application for handheld medical diagnostic devices, filed December 2024 ([Serial 98918659](https://tsdr.uspto.gov/statusview/sn98918659)). The earlier toy registration was cancelled in 2023 (Reg. 4194205 above), and a 2020 application for "downloadable software for healthcare monitoring" was abandoned ([Serial 90046204](https://tsdr.uspto.gov/statusview/sn90046204)). What I could not confirm: whether anyone holds TRICORDER for finance or investment software, because I read only the records a web search surfaced and did not run a full search of the register; and three more records (CBS's Serial 98937264 and two TRICORDER filings by other owners) returned an access error. This is a reading of public records, not legal advice. **Recommendation:** keep Tricorder for the hackathon, where it is a team name at a one-day event and nothing is sold. CBS is still filing for the word in new fields, so if Tricorder becomes a product, plan a rename before the first paid customer, and ask a trademark lawyer for a clearance search on the new name. The readout vocabulary in this doc (scan, readout, flag, gap) is generic and carries over to any name. The overview page carries this as a card.

## How Tricorder talks

The investors in the research talk in short sentences with numbers in them. They name the document. They expect the worst reading until the data says otherwise. A seed fund's guide puts it like this: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)).

The readout speaks like a careful associate writing to a partner. It states the number. It states the source. It states the disagreement. It does not soften a flag, and it does not guess at a reason.

These rules apply to the readout, the demo screens, the pitch and the posts.

**1. Lead with the number and where it came from.**

- Bad: Revenue looks strong and is growing quickly.
- Good: ARR is $2,240,868 in the model (financial_model.xlsx, ARR_Build, cell ARR_TOTAL).

**2. Two numbers beat one adjective.**

- Bad: Gross margin appears inflated.
- Good: The deck says 80% gross margin (slide 5). The ledger gives 58.1% once hosting, inference and support are counted (expense_ledger.csv).

**3. Say what the check did, not what it believes.**

- Bad: The founder may be hiding churn.
- Good: The Cohorts tab starts its nine cohorts with 57 customers. The revenue export shows 68 customers in the same cohorts.

**4. Don't soften a flag.**

- Bad: There may be a small discrepancy worth a closer look.
- Good: Flag: the deck's ARR is $259,132 above the model's.

**5. Don't invent a reason.** The readout reports what the documents show. Motive is the partner's call, after talking to the founder.

- Bad: The founder probably rounded up to impress investors.
- Good: Nothing in the room explains the $259,132 gap. Ask the founder.

**6. A missing document is a gap, not a guess.**

- Bad: Bank statements would likely confirm the revenue.
- Good: Not in the room: bank statements.

**7. Use the investors' words and say whose definition.** Finance terms (ARR, burn, runway, gross retention, comps) are fine. Software and AI vocabulary is not.

- Bad: Our AI-powered engine surfaced key revenue insights.
- Good: ARR here counts subscription contracts only, as a16z defines it ([a16z](https://a16z.com/16-startup-metrics/)). On that definition the room shows $2,060,868.

**8. Say it once, at the size it is.** No intensifiers, no urgency words. A flag is serious because of its numbers.

- Bad: Critical: runway is dramatically overstated.
- Good: Runway: 37 months in the model. 19 months with the full hiring plan.

## The readout's voice

Four shapes. Each is filled with the Hollis Voice numbers from the [data room research](../reports/20261022.02_research/research_data_room.md) (Part 3). Hollis Voice is the proposed synthetic demo company: an AI phone agent for vet clinics, raising a Series A. Its numbers come from that research's seeded design script. Differences below were computed with Python from those figures.

Order in the readout: disagreements first, then flags, then gaps, then clean checks. This follows the product brief's rule that claims which disagree are the first thing a partner sees.

**What each shape means:**

- **A disagreement** is two or more documents in the room stating different values for the same thing. The readout lists them side by side and does not pick a winner.
- **A flag** is a check that rebuilds a number from the raw files and finds the stated number does not hold.
- **A gap** is a document or fact the check needs that is not in the room.
- **A clean check** is a check that ran and found nothing. It is shown, so the partner knows it was done.

### A disagreement

Template:

> **Disagreement: [metric]**
>
> | Source | States | Where |
> |---|---|---|
> | [document] | [value] | [file, page or cell] |
> | [document] | [value] | [file, page or cell] |
>
> Largest gap: [value], between [source] and [source]. The room does not explain it.
>
> Ask the founder: [one question].

Filled:

> **Disagreement: ARR**
>
> | Source | States | Where |
> |---|---|---|
> | Pitch video | about $3,000,000 | pitch video, at about 0:35 |
> | Deck | $2,500,000 | pitch_deck.pdf, slides 3 and 14 |
> | Financial model | $2,240,868 | financial_model.xlsx, ARR_Build, ARR_TOTAL |
>
> Largest gap: about $760,000, between the video and the model. The deck is $259,132 above the model. The room does not explain either gap.
>
> Ask the founder: which of these is ARR as of 2026-09-30, and can you walk us from the billing data to it?

The last question is the one a pre-seed fund's angel guide recommends: ask the founder to walk from the source data to the number ([pre-seed fund, Sep 2026](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).

The gap is the video's rounded "about $3,000,000" minus the model's $2,240,868, which is $759,132, computed with Python. A gap that starts from a spoken figure is rounded too, here to the nearest $10,000, because "about" next to exact dollars reads as false precision ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 12). A gap between two written figures keeps its exact dollars.

### A flag

Template:

> **Flag: [what is wrong, in under ten words]**
>
> - The document shows: [value] ([file, location]).
> - The check found: [value] ([file, how it was rebuilt]).
> - Difference: [value].
> - Ask the founder: [one question].

Filled:

> **Flag: gross margin leaves out delivery costs**
>
> - The document shows: 80% gross margin (pitch_deck.pdf, slide 5; financial_model.xlsx, P&L).
> - The check found: 58.1% on the model's recurring revenue, which includes the Marlow pilot (expense_ledger.csv, with every line tagged hosting, inference, telephony or support moved into cost of revenue). On subscription revenue alone, without the pilot, it is 54.5% (financial_model.xlsx, P&L, W7, W13, W14, W20, W22).
> - Difference: 21.9 points on recurring revenue.
> - Ask the founder: why do cloud hosting and model inference sit under R&D, and support staff under sales and marketing, instead of cost of revenue?

A margin says which revenue it divides by. Once the pilot is out of recurring revenue, the two figures differ ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 12).

A second filled flag, because the pilot is the one an AI-literate panel will recognise:

> **Flag: a pilot is counted as ARR**
>
> - The document shows: ARR $2,240,868, including $180,000 a year from the Marlow Veterinary Group pilot (financial_model.xlsx, ARR_Build).
> - The check found: $2,060,868 from subscription rows only (customer_mrr_by_month.csv). The pilot is six months, $90,000 in fees in total, ends on 30 days notice, and carries no duty to convert (pilot_agreement_marlow.pdf, clauses 2, 7 and 8).
> - Difference: $180,000.
> - Ask the founder: has Marlow signed anything beyond the pilot?

### A gap

Template:

> **Not in the room: [document]**
>
> - Needed for: [the check it would allow].
> - Ask for: [the document, by name].

Filled:

> **Not in the room: IP assignment agreements**
>
> - Needed for: confirming the founders and any contractors assigned their work to the company. A seed fund's guide puts these on the first-pass list.
> - Ask for: signed invention assignment agreements for both founders and every contractor who wrote code.

The readout writes "not in the room". It does not write "likely", "probably" or "appears to", and it does not fill the gap from the web. A missing document is a question for the partner, not a flag on its own, because funds disagree on what a room should hold at each stage ([data room research](../reports/20261022.02_research/research_data_room.md), section 1.5).

### A clean check

Template:

> **Clean: [what was checked].** [How it was checked, in one sentence.] [The result, with its number.] ([file])

Filled:

> **Clean: cap table.** Holders were summed and the SAFEs converted at their stated cap. Holders add to 100.00%, and the $2,000,000 of SAFEs at a $12,000,000 post-money cap convert to 16.67%, which matches the table. (cap_table.xlsx)

## Words we use and words we avoid

**The metaphor in one line.** A tricorder scans and reads out what it finds; the person holding it decides.

**The product never says "invest" or "pass".** It does not recommend a decision, and it does not use any word that stands in for one ("strong buy", "avoid", "green light"). The readout's job ends at what the documents show and what to ask. The partner makes the call. This is the one absolute in this doc.

**Use:**

| Word | Means |
|---|---|
| readout | What Tricorder returns: the first-pass memo with its sources. |
| scan | One piece of first-pass diligence (red flags, comps, signals, video, founders). |
| flag | A number that does not hold up when a check rebuilds it. |
| disagreement | Two documents stating different values for the same thing. |
| source | The file and location, or the link, behind a claim. |
| gap | Something a check needs that is not in the room. |
| first pass | The work before a second meeting. Not full diligence. |
| memo | The written form of the readout, in the order a partner reads. |
| data room | The documents a startup shares with investors. |
| comps | Comparable companies and recent rounds, each with the reason it is fair. |
| signals | Outside evidence about a company and its competitors: hiring, traffic, reviews, pricing, customer wins. |

**Avoid:**

| Avoid | Why, or what to say instead |
|---|---|
| AI-first, "AI" in the lead | Say what it does. AI can come up when someone asks how. |
| leverage | use |
| robust | Say what it survives, with the test. |
| seamless | Say how many steps it takes. |
| revolutionary, game-changing | Cut. |
| insights | Say "flags", "disagreements" or the finding itself. |
| unlock, supercharge | Cut. Say what changes and by how much. |
| accurate, reliable, catches everything | Not without a score from a test run. See the claims table. |
| invest, pass, recommend | The partner decides. |
| likely, probably, appears to (in the readout) | State what the document shows, or write a gap. |

## The claims we make and where each came from

**Claims we can make:**

| Claim | What it rests on | Link |
|---|---|---|
| A first pass takes an associate days of pulling data and rebuilding numbers. | The organisers' Track 2 problem statement, from VCs they talked to. | [problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt) |
| The slow part is gathering and checking the data, not writing the memo. | A junior VC on weeks lost to a messy room; a fund partner who built his own tool, paraphrased by a reporter. | [junior VC](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture), [tech.eu](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/), [voice of the customer](../reports/20261022.02_research/research_voice_of_customer.md) |
| Investors treat numbers that disagree between the deck and the model as a red flag. | A seed fund's data room guide; a16z's data room guide gives a deck-against-model example. | [CRV](https://www.crv.com/content/what-is-a-data-room), [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| Founders count pilots and cancellable contracts as ARR. | Six VCs to a business magazine, paraphrased; a secondary fund partner's column. | [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/), [Calcalist](https://calcalistech.com/ctechnews/article/b1jfcymt3) |
| Every claim in the readout links to its source. | Track 2's fourth direction and the product rule. True of what we build. Not unique: five AI tools claim it. | [problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), [landscape](../reports/20261022.02_research/research_landscape.md) |
| On the pages we read, no tool shows market signals, comps and financial red flags together. | The landscape script's count over the tools mapped. Say "on the pages we read". | [landscape](../reports/20261022.02_research/research_landscape.md) |
| The buyer is a partner or principal at a seed or Series A fund; the associate uses it. | Persona ranking by say, do and pay. The pay evidence is inferred from a vendor case study. | [voice of the customer](../reports/20261022.02_research/research_voice_of_customer.md) |
| The demo room is synthetic and nothing in it belongs to a real company. | The organisers' rule and the data room design. | [problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), [data room](../reports/20261022.02_research/research_data_room.md) |
| The readout found [n] of the planted flags and wrongly flagged [n] of the decoys. | The answer key scored against Saturday's run. Use the numbers from that run, on that screen. | [data room](../reports/20261022.02_research/research_data_room.md), section 3.6 |

**Claims we do not make yet:**

| Claim | Why not | What would let us |
|---|---|---|
| Any speed in hours or minutes ("underwrite in an hour") | No independent source gives first-pass hours. The only figures are vendor claims. "In an hour" is the organisers' headline, not our measurement. | Timed runs on real rooms, and Ken's interview answers on how long a first pass takes. |
| Accuracy as a percentage, or "catches every red flag" | One synthetic room with planted flags is a test, not a measure. | A scored set of rooms, reported with how many there were. |
| "Trusted by funds", "used by investors" | No fund uses it. | A named fund that agrees to be named. |
| "The only tool that links claims to sources" | Five entrants claim it. | Nothing. Drop it. |
| "Detects fraud" | The worst misses in the research were faked books and bank records, which only a check with the bank catches. Tricorder reads what the room contains. | A bank or accounting data connection, and a test that shows it. |
| "Replaces an associate" | Untested, and it insults the user. | Nothing. Say it saves the associate the gathering. |
| Cheaper than a named competitor | Most enterprise tools quote on request. | Published prices for both. |

## Pitching to judges

Written for Ken to say. Plain, with contractions, no absolutes. "I" for what Ken decided, "we" for what the team built.

The spoken pitch fits the three-minute beat sheet in [ROADMAP.md, demo-script](ROADMAP.md#demo-script). The slot is likely three minutes or less, and VC judges already know the problem, so the pitch carries the open sentence, the beats and the close, and nothing else ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 11).

**Open (one sentence), said at 0:00 while the ARR ladder is on screen, before the beat sheet's first line:**

> When a startup sends a data room, an associate spends days rebuilding its numbers before a partner sees anything; Tricorder does that first pass and shows the partner what doesn't add up, with a source on every line.

**The problem, in investors' words (two quotes, for the page, not the spoken pitch):** the founder brief carries the first. Both are here for answers to questions.

> "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room))

> "It took us weeks to sift through the data, ultimately which led to us losing momentum and conviction in the founders ability to execute (amongst other things)." ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture))

Say who wrote each one by role: a seed and Series A fund's guide, and a junior VC. If Ken's own interviews this week produce a better line, and the person agrees to be quoted, use it in place of the second.

**The buyer, named, in one line at 2:30:** "The partner pays per seat." Behind it: the partner or principal at a seed to Series A fund pays. The associate uses it every day. Angels and accelerators come later; the research found angels tend to pay to avoid diligence rather than to do it better.

**The one workflow shown:** the readout for Hollis Voice's full room is already on screen, because it ran before Ken walked up. It opens on the ARR ladder: about $3.0M said on video, $2.5M in the deck, $2.24M in the model, $2.06M in the billing rows ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), verdict). Ken clicks the video figure, then the model figure and the pilot clause, each opening in the page. Then the flags, the gaps, and one line for the runs on the sealed variant room and the clean room. The forwarded pitch email is the closing "next" line.

**Where the data goes, only when asked:** say the sentence in "Where the data goes" below, then: "Today's room is synthetic."

**The close, at 2:30:**

> Next: forward the pitch email, and this is waiting before you open it. It doesn't tell you to invest or pass. It reads out what's in the room and what to ask the founder. If you do first-pass diligence and want to see it on your next deal, let's talk.

**If a judge asks:**

- *You built the company, planted the flags and wrote the answer key. What does it find in a data room you didn't make?* Answer with the two runs, not the room we planted ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 1). Someone outside the team planted a second room this week and sealed its key until our 3:30 freeze; here's what it found there, with the real numbers. On the same company with nothing planted, here's everything it flagged.
- *Isn't this a wrapper on a model?* The checks are code that rebuild each number from the raw files. The sealed variant room and the clean run are the test. The model reads contracts and labels where code can't.
- *Others already link claims to sources.* Yes, several do. Ours leads with what disagrees and writes a gap as a gap instead of filling it.
- *What happens when a scan fails?* The readout says which check didn't run and why. It doesn't leave the section blank.

## Posting voice

The hackathon gives $150 for the best social content posted during the day. Ken posts from his own accounts, under his name. An agent drafts; Ken edits and posts. The posts follow [Ken's style guide](../../../personal/context/personal/communication_style.md): plain, warm, specific, no emoji, no sign-off on the post itself.

**Show:**

- The readout catching a planted flag, with both numbers and the source file on screen.
- A disagreement on screen: the deck, the model and the video side by side.
- The team at work: hands, screens, whiteboards. Faces only with each person's yes.
- The answer key score, once a run produces one.

**Do not post:**

- Any judge's or teammate's words, or a teammate's name or face, without that person's consent. Ask first; tag them once they say yes.
- Any real company's data, deck or name in a way that suggests we scanned it.
- The answer key file itself, which would let anyone see where the flags are planted.
- A claim from the "do not make yet" table.

**Rules:**

- Say the room is synthetic in every post that shows numbers.
- Use the numbers from the screen in the photo. If Saturday's run shows different figures from the examples below, use Saturday's.
- One finding per post. Name the flag and give the two numbers.
- Before Hollis Voice appears in a public post, run the fresh web search on the name that the data room research asks for.

**Example post (under 280 characters):**

> At Deal Flow NYC we planted a pilot inside a synthetic startup's ARR. Tricorder caught it: the model says $2.24M, subscription revenue alone says $2.06M, and the pilot can end on 30 days notice. Both numbers on screen, each with its source file.

**Example LinkedIn post:**

> I'm at Deal Flow, NYC's first VC hackathon, at Betaworks today, building Tricorder on the diligence track.
>
> The organisers put the problem plainly: a first pass on a startup still takes an associate days of pulling data and rebuilding numbers from a messy data room.
>
> So we built a fake company with a real-looking data room and planted three problems in it:
>
> 1. A six-month pilot counted as recurring revenue.
> 2. A gross margin that leaves out hosting and model costs.
> 3. A runway that ignores most of the hiring plan.
>
> This afternoon Tricorder caught the pilot. The model says $2.24M ARR. Rebuilt from subscription revenue only, it's $2.06M, and the pilot can end on 30 days notice. The readout shows both numbers, the file each came from, and the question to ask the founder.
>
> It doesn't say invest or pass. It reads out what it found, and the partner decides.
>
> If you do first-pass diligence and want to see the readout, I'd love to talk!

## Where the data goes

> Tricorder reads only the documents you give it or the decks in mail you send it, keeps only the readout and its sources, and lets you see and delete everything it pulled.

Use this sentence on the product page and, when a judge asks, in the pitch, word for word. On Saturday, add one more: "Today's data room is synthetic."
