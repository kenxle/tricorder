# Personas

## Charter

**What belongs:** One persona per problem, each with the problem in the person's own words, what they have tried, why it failed them, the moment Tricorder solves it, the proof we can show, the objection to answer first, and say, do, pay evidence with a rating. Personas are ordered by rating. Who is the user and who is the buyer.

**What does not:** What the product does (PRODUCT_BRIEF.md). How it talks (BRAND.md). New quotes without a primary link. Interview notes before they are written up.

**Level of detail:** A builder or a pitch writer can pick up one persona and know whose problem they are solving and what evidence backs it. Quotes come only from the voice-of-customer research, with the link it gives.

**Sources:**

- [R1, voice of the customer](../reports/20261022.02_research/research_voice_of_customer.md), its quotes table and its counts from [voc_counts.py](../reports/20261022.02_research/voc_counts.py)
- [R2, the landscape](../reports/20261022.02_research/research_landscape.md), for what each persona has tried and what it costs
- [R4, the data room](../reports/20261022.02_research/research_data_room.md), for the proof on the demo room
- [The writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), for the personas-and-problems method

## How to read this

Each persona is a problem, not a job title. Say, do and pay are the three layers of evidence, from weakest to strongest. Say is what people write or tell. Do is what they already do about it. Pay is what they spend to solve it. A persona's rating is the highest layer with evidence. What people pay to solve is what goes in the value proposition.

The order is R1's: highest layer first, then the persona with more rows. R1's evidence does not change the order, with two notes. The partner's pay rating is inferred, because both pay rows come from a vendor case study and a third-party roundup, not from the buyers' own posts. The angel's pay rating is first-hand, but what the angel pays for is avoiding diligence. Row numbers point to R1's quotes table. Row counts come from [voc_counts.py](../reports/20261022.02_research/voc_counts.py).

**User and buyer.** The fund is the buyer: a partner or principal decides and pays. The associate is the user. At some funds the partner is the user too (persona 1, Do). For angels the user and the buyer are the same person. For accelerators the screening staff are the users and the program would be the buyer, with no evidence yet that programs pay.

| Rank | Persona | The problem | Rating | Role |
|---|---|---|---|---|
| 1 | Partner or principal at a seed or Series A fund | Numbers that disagree, found too late | Pay (inferred) | Buyer |
| 2 | Solo angel | No time or team to do diligence at all | Pay (to avoid diligence) | User and buyer; a pricing warning |
| 3 | Accelerator screener | Too many applications to read | Do | User; no buyer evidence |
| 4 | Associate at a seed fund | Days of gathering before any thinking | Do | User |
| 5 | Corporate VC | Strategic overlap on top of standard diligence | Say | Too thin to design for |

---

## 1. The partner who finds the disagreement too late

**Who they are.** A partner or principal at a seed or Series A fund who decides whether a deal goes to a second meeting and signs for the fund's tools.

**The problem in their own words.**

- "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room))
- "Beware of ARR - one of the indicators most prone to disasters and favored by entrepreneurs is the ARR (Annual Recurring Revenue)." ([secondary fund partner, Jul 2023](https://calcalistech.com/ctechnews/article/b1jfcymt3))
- "Weird metrics like “Quarterly MRR” or odd ways to describe revenue are immediate flags." ([SaaS investor, Dec 2021](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately))

**What they have tried.**

- A cursory review before the term sheet: "Basic financials and model review. But often only a cursory one." ([SaaS investor, Feb 2025](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet))
- Building their own tool. A fund partner built a ten-agent diligence tool and retunes it when it misses a nuance (paraphrased from journalism, R1 row 27).
- Generic chatbots, used to get past writer's block on memos (paraphrased from journalism, R1 row 28).
- Buying a commercial tool that turns a data room into a memo with linked citations (paraphrased from a vendor case study, R1 row 25).

**Why it failed them.**

- A cursory review is where disagreements hide, and the deep checks wait until after the term sheet (R1, "What they do instead").
- Chatbots cannot see the numbers that matter, because early-stage revenue, growth and retention are not public (paraphrased from journalism, R1 row 29).
- A home-built tool is a second job to maintain.
- The commercial tools R2 found are quote-only enterprise contracts, and V7 Go's own page claims memos in 2 to 4 hours, not minutes. None of the 24 tools R2 checked shows market signals, comps and red flags together ([landscape_counts.py](../reports/20261022.02_research/landscape_counts.py)). The partner in R1 row 25 still clicks into each citation to check it.

**The moment Tricorder solves it.** The partner opens the readout before the second meeting. The first thing on the page is the ARR the company reports in four places, side by side, each linked: the model, the deck and the founder's video disagree, and the pilot counted as ARR is named.

**The proof we can show.** On the demo room: the model's ARR is $2,240,868, the deck says $2,500,000 and the founder says about $3,000,000 on video, while the true recurring figure is $2,060,868 (R4, from [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). Tricorder finds the gap, finds the pilot that makes up part of it, and links the pilot agreement's notice clause.

**The objection to answer first.** Can I trust it, and where does my deal data go? The organisers' Track 3 names data leaving the firm as the biggest objection funds raise ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). The answer: every claim opens its source, Tricorder shows its own score on planted flags and decoys, and the investor can see and delete everything it pulled.

**Say, do, pay.** 28 rows in all (voc_counts.py).

- **Say (17 rows).** Numbers that disagree damage the deal (row 9). ARR is the riskiest metric (row 31). Founders cannot explain their own metrics (row 23).
- **Do (9 rows).** Two or three customer calls and a cursory model review before the term sheet (rows 12, 13). Some partners run diligence themselves: "our partners run diligence themselves without handing it to junior staff." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)). One partner built his own tool (row 27).
- **Pay (2 rows).** A $600M fund uses a commercial data-room-to-memo tool (row 25, vendor case study, price not stated). Funds pay for data seats, such as $13,500 a year for one PitchBook seat (row 67, a third-party roundup).
- **Rating: pay, inferred.** Both pay rows come from a vendor or a roundup, not the buyer's own words.

---

## 2. The solo angel with no time to do diligence

**Who they are.** An individual who writes small checks alone, with no analyst and no team.

**The problem in their own words.**

- "I don't have the time nor skills to do proper due diligence, but with YC I don't have to." ([angel, Jan 2022](https://news.ycombinator.com/item?id=30130146))
- "What started as a few hours a month quickly grew into a full-time (unpaid) job." ([angel, Apr 2025](https://halletecco.substack.com/p/why-i-stopped-angel-investing-after))
- "Along with many wins there are some investments I wish I’d turned down. I missed the red flags." ([angel, May 2023](https://techcrunch.com/?p=2539424))

**What they have tried.**

- Waiting for a lead investor: "As an angel, I would use this condition because I wouldn't invest without a lead institutional investor." ([angel, Mar 2013](https://news.ycombinator.com/item?id=5376620))
- Splitting the work with co-investors: "I do it so we can share the task of due diligence." ([angel, Aug 2013](https://news.ycombinator.com/item?id=6202816))
- Investing alongside an accelerator, and giving up upside for it (row 44).
- Stopping, and becoming an LP in funds instead (row 53).

**Why it failed them.** Each workaround avoids diligence rather than doing it. One angel's co-investors found the cause of her loss: "They discovered two sets of books: a made-up one for investors; the other with the real numbers." ([angel, May 2023](https://techcrunch.com/?p=2539424)). A full outside diligence costs far more than an angel check (a consultant priced one at about 100K, R1 row 41).

**The moment Tricorder solves it.** Before writing the check, the angel forwards the founder's email. The readout comes back with the places the deck and the model disagree and the questions to ask the founder.

**The proof we can show.** The seed drop, the thin first tier a founder sends before a term sheet, catches five of the eight planted entries on its own (R4, Part 3.4).

**The objection to answer first.** Is this worth the cost for a check this size? In the angel's words: "Note that I'm an angel investor, so I try to make sure the cost of due diligence is proportional to the amount I'm investing." ([angel, Aug 2013](https://news.ycombinator.com/item?id=6202816)). Memo tools already sell at $12 a memo and $0 to $30 a month (R2, Part 1). Tricorder cannot win angels on price, and it cannot catch a consistent set of fake books; that needs a check with the bank.

**Say, do, pay.** 14 rows in all (voc_counts.py).

- **Say (8 rows).** Missed red flags and fake books (rows 50, 51). No time or skills (row 43). A full-time unpaid job (row 52).
- **Do (4 rows).** Waits for a lead, shares diligence, sizes diligence to the check (rows 45 to 47).
- **Pay (2 rows).** "Yes, I give up some upside because of how much YC already owns, but to me it's worth every penny for the service that YC provides to me as an investor and to the startup." ([angel, Jan 2022](https://news.ycombinator.com/item?id=30130146)). "Lastly, I became a Limited Partner (LP) in a handful of VC funds, basically paying professionals to do the investing on our behalf." ([angel, Apr 2025](https://halletecco.substack.com/p/why-i-stopped-angel-investing-after))
- **Rating: pay.** The angel pays to avoid diligence, not to do it better. That is a pricing warning, not a buying signal for Tricorder.

---

## 3. The accelerator screener with too many applications

**Who they are.** Staff at an accelerator or challenge program who read every application in a short window.

**The problem in their own words.**

- "A human takes around four minutes to screen each application. That’s 24 full working days for one person–a huge time investment for a lean, non-profit team, even when the work is split between several staff members." ([challenge program, mid-2025, inferred](https://solve.mit.edu/articles/how-ai-helped-us-screen-applications-in-half-the-time))
- "If we get 1000 applications and have 10 days to read them, we have to read about 100 a day." ([accelerator, 2011 or earlier](https://www.ycombinator.com/howtoapply.html))

**What they have tried.**

- Reading every one: "Thousands of companies apply to Techstars, and our staff personally review every application that comes in." ([accelerator, Jan 2026](https://www.techstars.com/blog/advice/inside-a-techstars-accelerator-the-application-and-interview-process))
- Volunteer readers. One accelerator had alumni founders help read applications (row 59).
- A home-built screener on the ChatGPT API, which cut screening from 24 working days to 10 (row 61, the program's own post).

**Why it failed them.** The home-built screener worked in part: staff still read the share it labelled for review (row 61). A screener sorts applications. It does not check whether an applicant's numbers agree with each other.

**The moment Tricorder solves it.** After Saturday. A batch of applications, each with a deck, comes back as a stack of short readouts, sorted so the ones whose numbers disagree are on top.

**The proof we can show.** None yet beyond the demo room. Early applicants send thin material. A pre-seed partner: "As a VC who invests in Pre-Seed startups, often the data that we get from startups has pretty much nothing." ([pre-seed partner, early 2021, inferred](https://sacra.com/p/elizabeth-yin-hustlefund-interview/)). So the readout's gap list matters as much as its flags.

**The objection to answer first.** We already built our own, cheaply. The program in row 61 did exactly that. There is no evidence in R1 that accelerators pay for a tool.

**Say, do, pay.** 8 rows in all (voc_counts.py).

- **Say (4 rows).** About 100 applications a day (row 56). Four minutes each (row 60).
- **Do (4 rows).** Built a ChatGPT triage tool (row 61). Recruited alumni readers (row 59). Staff read every application (row 62).
- **Pay (0 rows).** No evidence found.
- **Rating: do.**

---

## 4. The associate who spends days gathering

**Who they are.** An associate at a seed fund who does the first pass and writes the memo the partners read. **This is Tricorder's user.**

**The problem in their own words.**

- "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal))
- "It took us weeks to sift through the data, ultimately which led to us losing momentum and conviction in the founders ability to execute (amongst other things)." ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture))
- "I still need to write a memo, walk into a partners’ meeting, and convince people who’ve never met you that we should do this deal." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal))

**What they have tried.**

- Browser tabs and manual web checks (row 1).
- A personal Notion CRM: "In my personal Notion CRM where I track relationships and people I meet, I interacted with over 1500 people as of December 5th, 2022." ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture))
- Phone calls (row 7).

**Why it failed them.** It is all by hand, and it does not scale to the volume: "As an associate at a VC fund, I review about 500 decks a year, speak with around 100 founders, go deep on maybe 15, and invest in only a few." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). A messy room cost one team weeks and the deal's momentum (row 5).

**The moment Tricorder solves it.** A deck arrives in the fund's inbox. Before the associate opens it, the ten tabs are already done: the market signals, the comps, and the red flags sit in one readout. The associate starts at the disagreements and walks into the partners' meeting with every claim linked.

**The proof we can show.** On the demo room, the readout catches the deck's count of 357 clinics, which is the last value of a column that never decreases, against 212 paying accounts (R4, PF7). The associate sees both numbers and both files in one row.

**The objection to answer first.** If it is wrong, I am the one who looks bad in the partners' meeting. One fund worker wrote that their firm discussed whether software could replace analysts, and that accuracy was the worry ([fund staff, Jan 2025](https://news.ycombinator.com/item?id=42612506)). The answer: every claim opens its source, a claim whose quote cannot be found is dropped and listed, and a missing fact shows as a gap.

**Say, do, pay.** 7 rows in all (voc_counts.py).

- **Say (4 rows).** A messy room cost weeks (row 5). "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal))
- **Do (3 rows).** Ten tabs of manual checks, a Notion CRM, phone calls (rows 1, 6, 7).
- **Pay (0 rows).** None. The associate uses the tool; the partner buys it.
- **Rating: do.**

---

## 5. The corporate VC with a strategic check on top

**Who they are.** An investor at a corporation's venture arm, who runs standard diligence plus a check on fit with the parent company.

**The problem in their own words.**

- "In addition to the standard diligence items, CVCs will spend more time validating areas of strategic overlap between the startup and the CVC’s corporate parent." ([corporate VC, Apr 2024](https://tdk-ventures.com/?p=2035))
- "VCs began prioritizing speed and cutting corners on diligence, only to find – after interest rates rose and capital contracted – valuations falling in a reversion to the norm." ([corporate VC, Apr 2024](https://tdk-ventures.com/?p=2035))

**What they have tried.** Nothing in R1's sample.

**Why it failed them.** Not known from the research.

**The moment Tricorder solves it.** The standard first pass, done before the strategic review starts. Tricorder does not check strategic overlap with a parent company.

**The proof we can show.** The same demo-room readout as the partner. Nothing specific to corporate VCs.

**The objection to answer first.** The strategic check is our extra work, and Tricorder does not do it.

**Say, do, pay.** 2 rows in all, both from one firm's report (voc_counts.py).

- **Say (2 rows).** Rows 38 and 39.
- **Do (0 rows).** None found.
- **Pay (0 rows).** None found.
- **Rating: say.** Too thin to design for. Ken's interviews could change this.

---

## What the interviews need to fill

R1 is a stand-in for interviews. Ken's two or three interviews this week ask the organisers' three questions. These gaps matter most for the ranking:

- **How long a first-pass memo takes, in hours.** No trustworthy public number exists (R1, question 3).
- **Hidden churn.** Every checklist names it, but no one in R1 told a regret story about it.
- **Burn against the hiring plan.** The organisers name it; no public voice in R1 does.
- **What the fund pays today, in the buyer's own words.** This would move the partner's rating from pay, inferred, to pay.
