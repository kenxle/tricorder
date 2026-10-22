# Voice of the customer: first-pass diligence

Written 2026-10-22 for the Tricorder hackathon plan. It answers the organisers' three questions from public sources. It is the primary source for the plan, and [the research gaps](research_gaps.md) fill its gaps.

## What this means for Tricorder

- **The red flag named most is ARR that is not really recurring; numbers that disagree come second.** Of the 67 rows in the quotes table, 19 name a red flag. ARR comes up in 9 rows from 6 different sources. Numbers that disagree come up in 5 rows from 3 sources. Then faked documents (4 rows, 4 sources), burn out of line with plans (3, 3), cap table problems (2, 2), a founder who cannot explain the numbers (1) and hidden churn (1). The tags are keyword matches; [red_flag_labels.csv](red_flag_labels.csv) shows the tags on every row and [red_flag_counts.py](red_flag_counts.py) does the counting. The two leaders overlap: an ARR that is not recurring usually shows up as a deck that disagrees with the billing. On disagreement, a seed and Series A fund's guide says "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)). An associate says the same about the deck against the P&L. A readout that leads with disagreements matches how investors already think.
- **What makes ARR not recurring.** Investors name pilots, one-time deals, cancellable contracts and odd labels such as quarterly MRR. Hidden churn in cohort charts is on every checklist, but no one in this sample told a regret story about it.
- **The worst misses were faked documents.** An angel lost her money to a founder who kept two sets of books. A 2026 fraud case put forged bank statements in a data room. Only a check with the bank catches this, and a SaaS investor says that check usually waits until after the term sheet. Tricorder cannot tell that a set of books is fake. What it can find is where the reporting differs: the deck against the model, the model against the ledger and the revenue rows, any of them against a bank export when the room has one, and the company's story against the outside world. A fake has to stay consistent across every file to get past that, and the readout shows each place it does not.
- **What they check first depends on who is reading and at what stage.** The sources do not agree on one order, because they describe different readers. Details and links are in question 1 below.
  - **An associate at a seed-focused fund** looks outside first. She is Victoria Korytska, an associate at Flyer One Ventures, which invests "at Pre-Seed, Seed, and Series A stages" and says "The majority of F1V's portfolio companies are at the Seed stage" ([Flyer One Ventures](https://flyerone.vc/post/how-does-f1v-work), page saved in [raw/voc/](raw/voc/INDEX.md)). She opens ten browser tabs on traffic, reviews, investors and the founders before opening the data room.
  - **A fund's deal team at seed and Series A** starts inside the room with four documents: the cap table, the financial model, the incorporation papers and the IP assignments.
  - **Pre-seed investors** say there is almost no data at that stage, so they judge the founder.
  - For Tricorder this means the first screen cannot assume one reader or one stage. A thin pre-seed room needs the founder and outside-world pieces up front; a Series A room needs the financial pieces. The answer is simple: the operator can change the order of the pieces.
- **The slowest part is gathering and checking, not writing.** A partner who built his own tool says so, and a junior VC lost weeks to a messy data room. No independent source gives hours for a first-pass memo. [The research gaps](research_gaps.md) look for that number. So Tricorder has to make checking and cross-checking fast and easy: every number one click from its source, and one more from every other source that agrees or disagrees.
- **Funds already pay for this, which validates the idea.** A $600M fund runs its diligence on a commercial AI tool that turns a whole data room into a memo, with every claim linked to its source. Tricorder does not need to be very different from that. It does the same core job and adds to it: the readout that opens on the best green flags and worst red flags, the red-flag engine with accounting mislabels, fast cross-checking of any number, and the scans beyond the room (the pitch video, comps, market signals).
- **Angels want diligence and lack the time, so they buy it by proxy.** One angel puts almost every check into YC companies because he has no time or skills for diligence and YC has done it; he gives up upside for that. Others wait for a lead investor or split the work with co-investors. Each is diligence done by someone else that the angel trusts and cannot check. For Tricorder, that is a gap: angels might pay for diligence if it were accessible and easy to run in the time they have. They may also not be the first target market. The [research gaps](research_gaps.md) track looks at what angels pay for diligence today.
- **Accelerators have a volume problem and build their own triage.** One program needs about four minutes per application, 24 working days in all, and built its own ChatGPT screener. No evidence here that accelerators pay for a tool.

## How this was gathered

- Hacker News through the Algolia API, plus fetched pages from fund blogs, investor columns, accelerators, one interview, vendor case studies and two news stories. Everything read is saved in [raw/voc/](raw/voc/INDEX.md). The script counts the files below.
- Each quote or paraphrase is one row of [voc_quotes.csv](voc_quotes.csv). [voc_counts.py](voc_counts.py) does the counting. [voc_table.py](voc_table.py) renders the table. [hn_fetch.py](hn_fetch.py), [hn_digest.py](hn_digest.py) and [web_fetch.py](web_fetch.py) did the fetching.
- Quotes come only from a person's or firm's own post, column, comment or interview page. News stories, podcast summaries and vendor case studies are paraphrased and marked.
- Hacker News roles are self-described and cannot be checked. G2, Capterra and TrustRadius blocked fetches, so no tool reviews are quoted. Reddit was not fetched; the list for Ken is at the end.

**How old is it?** Per the script, 49% of rows are from 2025 or 2026. 21% are from before 2020, and 13 of those 14 are Hacker News comments. The Hacker News material skews old. The fund and accelerator pages are mostly recent.

## 1. What do you check first when you open a data room?

**Associates look outside the room first.** "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). That is Tricorder's market-signal and presence scans, done by hand.

**Then the legal and financial core.** "The initial pass concentrates on a short list of corporate and legal records: the cap table, the financial model, the articles of incorporation and the intellectual property (IP) assignment agreements." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)). The same guide: "Your annual recurring revenue (ARR) in the deck should reconcile to the underlying billing, contract and revenue schedules." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room)).

**The first pass is thin on purpose.** A SaaS investor lists the pre-term-sheet checks: "A couple of customer calls. Often just 2 or 3. But quickly confirm they love the product." ([SaaS investor, Feb 2025](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)) and "Basic financials and model review. But often only a cursory one." ([SaaS investor, Feb 2025](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)).

**Founders who cannot explain their numbers fail early.** "In one founder call handled by our Hustle Fund team, the concern was not that the metrics were weak. The founder could not explain monthly traffic, conversion rate, returning-customer percentage, or customer acquisition cost (CAC)." ([pre-seed fund, Sep 2026](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).

**At pre-seed there is little data to check.** "As a VC who invests in Pre-Seed startups, often the data that we get from startups has pretty much nothing." ([pre-seed partner, early 2021, inferred](https://sacra.com/p/elizabeth-yin-hustlefund-interview/)). So a pre-seed first pass leans on the founders and the outside world, not on a data room.

**References are routine but weak.** "Most VCs do reference calls. From my conversations, few feel like they do them very well." ([seed investor, Jun 2025](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls)).

**Corporate VCs add a strategic check**, and accelerators look at the founder. Both quotes are in the table (rows 38 and 58).

## 2. Which red flag did you once miss and regret?

First-person regret stories are rare in public. Investors write the lesson more often than the miss. What exists falls into four groups.

**Fake books and fake bank records.** "Along with many wins there are some investments I wish I’d turned down. I missed the red flags." ([angel, May 2023](https://techcrunch.com/?p=2539424)). Her co-investors found the cause: "They discovered two sets of books: a made-up one for investors; the other with the real numbers." ([angel, May 2023](https://techcrunch.com/?p=2539424)). A June 2026 thread discussed a founder jailed for putting forged bank documents in a data room. One commenter asked "Wait, when they're doing due diligence, nobody actually checks anything with the bank? I think it might be harder to fake eligibility for a mortgage than $107 million ARR." ([observer, Jun 2026](https://news.ycombinator.com/item?id=48606618)). A SaaS investor lists the bank check as post-term-sheet work: "Bank statements & deep financial review. To make sure whatever you have is true." ([SaaS investor, Feb 2025](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)).

**ARR that is not recurring.** A secondary fund's managing partner, writing after a 2023 fraud: "Beware of ARR - one of the indicators most prone to disasters and favored by entrepreneurs is the ARR (Annual Recurring Revenue)." ([secondary fund partner, Jul 2023](https://calcalistech.com/ctechnews/article/b1jfcymt3)). Her reason: there is no standard definition, so "In fact, today, every company calculates its own ARR in the absence of a uniform standard," and a padded number "is not considered cheating because it falls within the realm of acceptable interpretation within the industry" (same article). In 2025, six VCs told a business magazine that founders count pilots, one-time deals and unactivated contracts as recurring revenue. One described "booked ARR" on contracts the customer can cancel within three months ([paraphrased from journalism, Sep 2025](https://finance.yahoo.com/news/much-pressure-company-went-zero-100000468.html)). A SaaS investor flags the labels: "Weird metrics like “Quarterly MRR” or odd ways to describe revenue are immediate flags." ([SaaS investor, Dec 2021](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately)).

**Burn out of line with progress.** "If you have burnt, say, more than $3m-$4m on the way to $1m ARR, it starts to get tough to invest (at least for me), unless you are truly a rocketship." ([SaaS investor, Dec 2021](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately)). No one here checked burn against a hiring plan. That organiser direction has no public voice behind it yet.

**Speed that skipped the checks.** "Term-sheets that were signed within 24-48 hours were not considered an unusual occurrence during those times (though not a widespread practice either, it is important to emphasize)." ([secondary fund partner, Jul 2023](https://calcalistech.com/ctechnews/article/b1jfcymt3)). A corporate VC made the same point a year later (table row 39). What it means for Tricorder: when a round moves fast, the checks are the first thing dropped. A first pass that runs in minutes, and starts on the inbound before anyone asks, means a fast round no longer forces a choice between speed and checking. The readout's gaps and ask list also show what was not checked, so speed cannot hide it.

**A gap left open.** The seed fund guide asks founders for cohort retention curves, and every checklist does. No public regret story about hidden churn turned up. [The research gaps](research_gaps.md) look for one.

## 3. How long does your first-pass memo take, and which part is slowest?

**Who the memo is for.** The partners who decide whether to go further. The associate writes it so she can "walk into a partners' meeting, and convince people who've never met you that we should do this deal" ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)). a16z describes the data room's job the same way: giving investors what they need for diligence, to "eventually write an investment memo to discuss with the rest of their team" ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)). So the operator works in the readout, and what leaves it is a memo for the partners' meeting.

**No trustworthy public number exists.** The only hour counts come from vendors. One says a private equity firm spent 12 to 15 hours of senior associate time per committee memo ([vendor claim, Mar 2026](https://agentman.ai/blog/ic-memo-that-wrote-itself)). Another's customer says work went from weeks to a day ([vendor case study, Jul 2026](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go)). Treat both as sales copy.

**Volume sets the clock.** "As an associate at a VC fund, I review about 500 decks a year, speak with around 100 founders, go deep on maybe 15, and invest in only a few." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).

**The slowest part is the data, not the prose.** A junior VC recalls a deal his team loved: "It took us weeks to sift through the data, ultimately which led to us losing momentum and conviction in the founders ability to execute (amongst other things)." ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture)). A fund partner who built his own tool said the slowest part is finding, verifying and structuring information ([paraphrased from journalism, Aug 2026](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/)). A growth investor described skipping the polished memo for the raw numbers: "As a VC/private equity guy, the presentations and investment memos that were no doubt largely written between 2 and 5 AM were mostly discarded; I extracted the few numbers I needed and tossed them, as I wanted the raw data from management and not the bankers' glossy sales pitch." ([growth investor, Sep 2013](https://news.ycombinator.com/item?id=6379145)).

**Angels have no team, so time is the wall.** "What started as a few hours a month quickly grew into a full-time (unpaid) job." ([angel, Apr 2025](https://halletecco.substack.com/p/why-i-stopped-angel-investing-after)).

**Accelerators count minutes per application.** "A human takes around four minutes to screen each application. That’s 24 full working days for one person–a huge time investment for a lean, non-profit team, even when the work is split between several staff members." ([challenge program, mid-2025, inferred](https://solve.mit.edu/articles/how-ai-helped-us-screen-applications-in-half-the-time)). Years earlier, YC's founder wrote "If we get 1000 applications and have 10 days to read them, we have to read about 100 a day." ([accelerator, 2011 or earlier](https://www.ycombinator.com/howtoapply.html)).

## What they pay for

- **AI diligence tools.** A $600M fund's managing partner says her team drops a whole data room into a commercial AI tool and gets a memo in the firm's template. She clicks each citation to check it. She frames it as buying rather than building. The vendor wrote the case study, calls the fund a user and an investor, and does not say what the fund pays ([paraphrased from a vendor case study, Jul 2026](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go)). This is the strongest pay signal found, and it is a direct competitor.
- **Data subscriptions.** A startup site collected eight PitchBook customers' prices, such as $13,500 a year for one seat. Reviewers it cites call it very expensive for small funds ([paraphrased from a third-party roundup, Jan 2024](https://www.failory.com/blog/pitchbook-pricing)).
- **Someone else's diligence.** "Yes, I give up some upside because of how much YC already owns, but to me it's worth every penny for the service that YC provides to me as an investor and to the startup." ([angel, Jan 2022](https://news.ycombinator.com/item?id=30130146)). "Lastly, I became a Limited Partner (LP) in a handful of VC funds, basically paying professionals to do the investing on our behalf." ([angel, Apr 2025](https://halletecco.substack.com/p/why-i-stopped-angel-investing-after)).
- **Outsourced teams.** A former Big 4 diligence worker, launching his own product, says offshore teams rebuild each data room by hand before anyone can analyse it (table row 40). A technical diligence consultant priced a full diligence at about $100K, which is why angels skip it (table row 41).

## What they do instead

- **Browser tabs and manual checks.** The associate's ten tabs (question 1).
- **Generic chatbots.** In early 2023 a fund partner told a reporter he uses ChatGPT to get past writer's block on memos. Another investor said chatbots are poor at memos because early-stage numbers are not public ([paraphrased from journalism, Jan 2023](https://techcrunch.com/2023/01/10/some-investors-are-cautiously-implementing-chatgpt-in-their-workflows/)).
- **Home-built tools.** A fund partner built a ten-agent diligence tool for under 1,000 euros ([paraphrased from journalism, Aug 2026](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/)). A challenge program built a ChatGPT screener and cut screening from 24 working days to 10 ([paraphrased from the program's own post, mid-2025](https://solve.mit.edu/articles/how-ai-helped-us-screen-applications-in-half-the-time)).
- **Notion as a CRM.** "In my personal Notion CRM where I track relationships and people I meet, I interacted with over 1500 people as of December 5th, 2022." ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture)).
- **Borrowing a lead's diligence.** "As an angel, I would use this condition because I wouldn't invest without a lead institutional investor." ([angel, Mar 2013](https://news.ycombinator.com/item?id=5376620)). "I do it so we can share the task of due diligence." ([angel, Aug 2013](https://news.ycombinator.com/item?id=6202816)).
- **Volunteer readers.** In 2009 YC announced that alumni founders would help read applications ([paraphrased from the founder's thread comment, Oct 2009](https://news.ycombinator.com/item?id=908577)).
- **Deferring checks.** Bank statements, background checks and formal references move after the term sheet ([SaaS investor, Feb 2025](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)).

## Personas

Ordered by the highest layer with evidence (pay, then do, then say), per [voc_counts.py](voc_counts.py). Within a layer, the persona with more rows comes first. Row numbers point to the quotes table.

**1. Partner or principal at a seed or Series A fund. Highest layer: pay, inferred.**
- Problem, in their words: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([seed fund guide, Aug 2026](https://www.crv.com/content/what-is-a-data-room))
- Say: ARR is the riskiest metric (row 31). Founders cannot explain their own metrics (row 23).
- Do: two or three customer calls and a cursory model review before the term sheet (rows 12, 13). One partner built his own AI tool (row 27).
- Pay: a commercial data-room-to-memo tool (row 25) and data seats (row 67). Both come from a vendor or a roundup, not the buyers' own posts, so the pay rating is inferred.

**2. Solo angel. Highest layer: pay.**
- Problem, in their words: "I don't have the time nor skills to do proper due diligence, but with YC I don't have to." ([angel, Jan 2022](https://news.ycombinator.com/item?id=30130146))
- Say: missed red flags and fake books (rows 50, 51).
- Do: waits for a lead, splits diligence with co-investors, sizes diligence to the check (rows 45 to 47).
- Pay: gives up upside to YC (row 44), becomes an LP instead (row 53). This is paying to avoid diligence. It is a warning for pricing.

**3. Accelerator screener. Highest layer: do.**
- Problem, in their words: "A human takes around four minutes to screen each application. That’s 24 full working days for one person–a huge time investment for a lean, non-profit team, even when the work is split between several staff members." ([challenge program, mid-2025, inferred](https://solve.mit.edu/articles/how-ai-helped-us-screen-applications-in-half-the-time))
- Say: partners read about 100 applications a day (row 56).
- Do: built a ChatGPT triage tool (row 61), recruited alumni readers (row 59).
- Pay: no evidence found.

**4. Associate at a seed fund. Highest layer: do.**
- Problem, in their words: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([associate, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal))
- Say: a messy room cost weeks (row 5).
- Do: manual web checks, Notion as a CRM, phone calls (rows 1, 6, 7).
- Pay: none. The associate is Tricorder's user; the partner is its buyer.

**5. Corporate VC. Highest layer: say.**
- Problem, in their words: "In addition to the standard diligence items, CVCs will spend more time validating areas of strategic overlap between the startup and the CVC’s corporate parent." ([corporate VC, Apr 2024](https://tdk-ventures.com/?p=2035))
- Two rows, both from one firm's report. Too thin to design for.

## Quotes table

Layer is say, do or pay. "context" marks observers and vendor claims, which are not customers. Rendered from [voc_quotes.csv](voc_quotes.csv).

<!-- TABLE START -->
| # | Persona | Layer | Date | Quote or paraphrase | Link |
|---|---|---|---|---|---|
| 1 | Associate | do | 2026-01 | "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." | [source](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| 2 | Associate | say | 2026-01 | "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." | [source](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| 3 | Associate | say | 2026-01 | "As an associate at a VC fund, I review about 500 decks a year, speak with around 100 founders, go deep on maybe 15, and invest in only a few." | [source](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| 4 | Associate | say | 2026-01 | "I still need to write a memo, walk into a partners’ meeting, and convince people who’ve never met you that we should do this deal." | [source](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| 5 | Associate | say | 2022-12 | "It took us weeks to sift through the data, ultimately which led to us losing momentum and conviction in the founders ability to execute (amongst other things)." | [source](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture) |
| 6 | Associate | do | 2022-12 | "In my personal Notion CRM where I track relationships and people I meet, I interacted with over 1500 people as of December 5th, 2022." | [source](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture) |
| 7 | Associate | do | 2012-07 | "I did that kind of stuff as a lowly associate at a university-affiliate VC fund, so I don't see how a firm being paid millions of dollars can't find someone to make a few phone calls." | [source](https://news.ycombinator.com/item?id=4246323) |
| 8 | Partner or principal | say | 2026-08 | "The initial pass concentrates on a short list of corporate and legal records: the cap table, the financial model, the articles of incorporation and the intellectual property (IP) assignment agreements." | [source](https://www.crv.com/content/what-is-a-data-room) |
| 9 | Partner or principal | say | 2026-08 | "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." | [source](https://www.crv.com/content/what-is-a-data-room) |
| 10 | Partner or principal | say | 2026-08 | "Your annual recurring revenue (ARR) in the deck should reconcile to the underlying billing, contract and revenue schedules." | [source](https://www.crv.com/content/what-is-a-data-room) |
| 11 | Partner or principal | do | 2026-08 | "our partners run diligence themselves without handing it to junior staff." | [source](https://www.crv.com/content/what-is-a-data-room) |
| 12 | Partner or principal | do | 2025-02 | "A couple of customer calls. Often just 2 or 3. But quickly confirm they love the product." | [source](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) |
| 13 | Partner or principal | do | 2025-02 | "Basic financials and model review. But often only a cursory one." | [source](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) |
| 14 | Partner or principal | do | 2025-02 | "Bank statements & deep financial review. To make sure whatever you have is true." | [source](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) |
| 15 | Partner or principal | say | 2021-12 | "Weird metrics like “Quarterly MRR” or odd ways to describe revenue are immediate flags." | [source](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately) |
| 16 | Partner or principal | say | 2021-12 | "If you have burnt, say, more than $3m-$4m on the way to $1m ARR, it starts to get tough to invest (at least for me), unless you are truly a rocketship." | [source](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately) |
| 17 | Partner or principal | say | 2024-06 | Paraphrase (podcast summary): On a podcast, a SaaS fund founder said investors should always check the bank account, and that his most stressful investments all had made-up claims in them. | [source](https://20vc.substack.com/p/20vc-newsletter-june-2nd-2024) |
| 18 | Partner or principal | say | 2023-09 | Paraphrase (podcast summary): The same investor's podcast episode was billed as arguing that VC diligence is weak and that every VC has fraud in its portfolio. Only the episode description was read. | [source](https://cloud.substack.com/p/jason-back-on-20vc-every-vc-has-a) |
| 19 | Partner or principal | say | 2018-02 | "If someone is investing $15k or $50k as an angel, they might make a decision after a single meeting because that meeting is often their sole shot to meaningfully interact with a founder. But if a fund is writing a $400k or $1m check, more diligence will be required." | [source](https://news.ycombinator.com/item?id=16425967) |
| 20 | Partner or principal | do | 2018-02 | "Generally we do 2 smaller meetings (maybe associate the first time and partner the second time, maybe partner the first time and partner+associate the second time, etc), then a full partnership meeting." | [source](https://news.ycombinator.com/item?id=16426678) |
| 21 | Partner or principal | say | 2025-06 | "Most VCs do reference calls. From my conversations, few feel like they do them very well." | [source](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls) |
| 22 | Partner or principal | do | 2025-06 | "Most funds I spoke with only do reference calls at the end of the process, as part of confirmatory diligence." | [source](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls) |
| 23 | Partner or principal | say | 2026-09 | "In one founder call handled by our Hustle Fund team, the concern was not that the metrics were weak. The founder could not explain monthly traffic, conversion rate, returning-customer percentage, or customer acquisition cost (CAC)." | [source](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore) |
| 24 | Partner or principal | say | 2021-02 (inferred) | "As a VC who invests in Pre-Seed startups, often the data that we get from startups has pretty much nothing." | [source](https://sacra.com/p/elizabeth-yin-hustlefund-interview/) |
| 25 | Partner or principal | pay | 2026-07 | Paraphrase (vendor case study): A managing partner at a $600M fund says her team drops a whole data room into a commercial AI tool and gets back a memo in the firm's own template. She says the work went from weeks to a day, and she clicks into each citation to check it. She frames it as buying rather than building. The vendor wrote the case study, calls the fund a user and an investor, and does not say what the fund pays. | [source](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go) |
| 26 | Partner or principal | pay | 2026-07 | Paraphrase (vendor case study): An investor at the same fund says they use the tool for market research, pulling comps, evaluating companies and analyzing financials. | [source](https://www.v7labs.com/news/moderne-ventures-accelerates-due-diligence-with-v7-go) |
| 27 | Partner or principal | do | 2026-08 | Paraphrase (journalism): A fund partner built his own ten-agent diligence tool for under 1000 euros. He says the slowest part of analysing a startup is finding, verifying and structuring information. The finding it surfaces most often is founders overestimating market size. When it misses a nuance he retunes the agent and reruns it. | [source](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/) |
| 28 | Partner or principal | do | 2023-01 | Paraphrase (journalism): A fund partner told a reporter he uses ChatGPT to help write investment memos when he is stuck on phrasing, and noted its data was stale. | [source](https://techcrunch.com/2023/01/10/some-investors-are-cautiously-implementing-chatgpt-in-their-workflows/) |
| 29 | Partner or principal | say | 2023-01 | Paraphrase (journalism): Another investor said ChatGPT would be poor at writing memos because the numbers that matter for early startups (revenue, growth, retention) are not public. | [source](https://techcrunch.com/2023/01/10/some-investors-are-cautiously-implementing-chatgpt-in-their-workflows/) |
| 30 | Angel | say | 2023-08 | Paraphrase (journalism): The founder of an angel network told a reporter that founders show the four flattering metrics out of a hundred, and the investor's job is to ask about the other 96. | [source](https://techcrunch.com/2023/08/08/how-vcs-spot-liars-venture-debt-basics-getting-legal-help-without-going-broke/) |
| 31 | Partner or principal | say | 2023-07 | "Beware of ARR - one of the indicators most prone to disasters and favored by entrepreneurs is the ARR (Annual Recurring Revenue)." | [source](https://calcalistech.com/ctechnews/article/b1jfcymt3) |
| 32 | Partner or principal | say | 2023-07 | "In fact, today, every company calculates its own ARR in the absence of a uniform standard." | [source](https://calcalistech.com/ctechnews/article/b1jfcymt3) |
| 33 | Partner or principal | say | 2023-07 | "Term-sheets that were signed within 24-48 hours were not considered an unusual occurrence during those times (though not a widespread practice either, it is important to emphasize)." | [source](https://calcalistech.com/ctechnews/article/b1jfcymt3) |
| 34 | Partner or principal | say | 2025-09 | Paraphrase (journalism): Six VCs told a business magazine that founders count pilots, one-time deals and unactivated contracts as recurring revenue. One said startups claim booked ARR on contracts the customer can cancel within three months. | [source](https://finance.yahoo.com/news/much-pressure-company-went-zero-100000468.html) |
| 35 | Partner or principal | say | 2025-09 | Paraphrase (journalism): A fund managing partner said investors forced AI revenue into SaaS-style recurring metrics, and should build new metrics instead. | [source](https://finance.yahoo.com/news/much-pressure-company-went-zero-100000468.html) |
| 36 | Partner or principal | do | 2013-09 | "As a VC/private equity guy, the presentations and investment memos that were no doubt largely written between 2 and 5 AM were mostly discarded; I extracted the few numbers I needed and tossed them, as I wanted the raw data from management and not the bankers' glossy sales pitch." | [source](https://news.ycombinator.com/item?id=6379145) |
| 37 | Fund staff, role unstated | say | 2025-01 | "I work in private equity and venture capital, and we recently had an internal discussion about whether AI could eventually replace analysts and deal sourcing employees for investment screening and due diligence. It would obviously save firms a ton of money and time, but there's concern about the accuracy." | [source](https://news.ycombinator.com/item?id=42612506) |
| 38 | Corporate VC | say | 2024-04 | "In addition to the standard diligence items, CVCs will spend more time validating areas of strategic overlap between the startup and the CVC’s corporate parent." | [source](https://tdk-ventures.com/?p=2035) |
| 39 | Corporate VC | say | 2024-04 | "VCs began prioritizing speed and cutting corners on diligence, only to find – after interest rates rose and capital contracted – valuations falling in a reversion to the norm." | [source](https://tdk-ventures.com/?p=2035) |
| 40 | Outsourced diligence | pay | 2026-07 | "Every deal starts with a data room: Ledgers. Accounting records. Contracts. Financial statements & Endless spreadsheets. And before anyone can operate on top of it, a loot of offshore teams in India have to reconstruct it by hand and inject it into a dashboard." | [source](https://news.ycombinator.com/item?id=49111296) |
| 41 | Outsourced diligence | pay | 2016-01 | "To make an extreme example: a full legal/commercial/technical/financial dd would cost approximately 100K or so." | [source](https://news.ycombinator.com/item?id=10952145) |
| 42 | Outsourced diligence | say | 2016-01 | "For angels the situation is worse here because they don't have the funds or the organization to do this properly." | [source](https://news.ycombinator.com/item?id=10952145) |
| 43 | Angel | say | 2022-01 | "I don't have the time nor skills to do proper due diligence, but with YC I don't have to." | [source](https://news.ycombinator.com/item?id=30130146) |
| 44 | Angel | pay | 2022-01 | "Yes, I give up some upside because of how much YC already owns, but to me it's worth every penny for the service that YC provides to me as an investor and to the startup." | [source](https://news.ycombinator.com/item?id=30130146) |
| 45 | Angel | do | 2013-03 | "As an angel, I would use this condition because I wouldn't invest without a lead institutional investor." | [source](https://news.ycombinator.com/item?id=5376620) |
| 46 | Angel | do | 2013-08 | "I do it so we can share the task of due diligence." | [source](https://news.ycombinator.com/item?id=6202816) |
| 47 | Angel | do | 2013-08 | "Note that I'm an angel investor, so I try to make sure the cost of due diligence is proportional to the amount I'm investing." | [source](https://news.ycombinator.com/item?id=6202816) |
| 48 | Angel | do | 2019-02 | "I mean I did this even when I invested just $15K as an angel investor in a company long time ago." | [source](https://news.ycombinator.com/item?id=19218335) |
| 49 | Angel | say | 2025-05 | "As an angel, you don’t have that level of access or time." | [source](https://news.ycombinator.com/item?id=43880555) |
| 50 | Angel | say | 2023-05 | "Along with many wins there are some investments I wish I’d turned down. I missed the red flags." | [source](https://techcrunch.com/?p=2539424) |
| 51 | Angel | say | 2023-05 | "They discovered two sets of books: a made-up one for investors; the other with the real numbers." | [source](https://techcrunch.com/?p=2539424) |
| 52 | Angel | say | 2025-04 | "What started as a few hours a month quickly grew into a full-time (unpaid) job." | [source](https://halletecco.substack.com/p/why-i-stopped-angel-investing-after) |
| 53 | Angel | pay | 2025-04 | "Lastly, I became a Limited Partner (LP) in a handful of VC funds, basically paying professionals to do the investing on our behalf." | [source](https://halletecco.substack.com/p/why-i-stopped-angel-investing-after) |
| 54 | Angel | say | 2026-09 | "Ask: “I may be using a different definition. Can you walk me from the source data to this number?”" | [source](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore) |
| 55 | Angel | say | 2026-09 | "At minimum, reconcile founder histories, customer and revenue claims, cash and burn, prior financings, cap table, security, and material conflicts." | [source](https://www.hustlefund.vc/post/angel-squad-7-expensive-mistakes-angel-investing-communities-help-you-avoid) |
| 56 | Accelerator screener | say | 2011-03 (or earlier) | "If we get 1000 applications and have 10 days to read them, we have to read about 100 a day." | [source](https://www.ycombinator.com/howtoapply.html) |
| 57 | Accelerator screener | do | 2009-10 | "every cycle there are a few applications that say they won't tell us any details about what they're doing without an NDA.  We thereupon instantly hit "next."" | [source](https://news.ycombinator.com/item?id=908577) |
| 58 | Accelerator screener | say | 2014-03 | "When I was reading applications (odd yet delightful to use the past tense) the main thing I looked for was energetic founders working on an idea that grew organically out of their own experience." | [source](https://news.ycombinator.com/item?id=7481618) |
| 59 | Accelerator screener | do | 2009-10 | Paraphrase (community comment): The accelerator announced that its alumni founders would help its partners read applications. | [source](https://news.ycombinator.com/item?id=908577) |
| 60 | Accelerator screener | say | 2025 (mid-year; inferred) | "A human takes around four minutes to screen each application. That’s 24 full working days for one person–a huge time investment for a lean, non-profit team, even when the work is split between several staff members." | [source](https://solve.mit.edu/articles/how-ai-helped-us-screen-applications-in-half-the-time) |
| 61 | Accelerator screener | do | 2025 (mid-year; inferred) | Paraphrase (own words): The program built a screening prototype on the ChatGPT API with university researchers. Staff then read only the 41% of applications it labelled for review, which cut screening from 24 working days to 10. | [source](https://solve.mit.edu/articles/how-ai-helped-us-screen-applications-in-half-the-time) |
| 62 | Accelerator screener | do | 2026-01 | "Thousands of companies apply to Techstars, and our staff personally review every application that comes in." | [source](https://www.techstars.com/blog/advice/inside-a-techstars-accelerator-the-application-and-interview-process) |
| 63 | Accelerator screener | say | 2026-01 | "We do our best to review all applications within four weeks of applications closing, and we will notify all applicants about the state of their application." | [source](https://www.techstars.com/blog/advice/inside-a-techstars-accelerator-the-application-and-interview-process) |
| 64 | Observer | context | 2026-06 | "Wait, when they're doing due diligence, nobody actually checks anything with the bank? I think it might be harder to fake eligibility for a mortgage than $107 million ARR." | [source](https://news.ycombinator.com/item?id=48606618) |
| 65 | Observer | context | 2025-12 | "Got pissed off with too many ARR manipulations and AI startups announcing revenue numbers manipulations(best day * 365 as ARR etc)." | [source](https://news.ycombinator.com/item?id=46429742) |
| 66 | Vendor claim | context | 2026-03 | Paraphrase (vendor case study): A memo-tool vendor says one mid-market private equity firm spent 12 to 15 hours of senior associate time on each investment committee memo, and that the pain is assembling the sources, not writing. | [source](https://agentman.ai/blog/ic-memo-that-wrote-itself) |
| 67 | Data buyers, mixed | pay | 2024-01 | Paraphrase (third party roundup): A startup-resources site collected eight PitchBook customers' quoted prices, such as 13500 dollars a year for one seat and 20000 dollars a year for three seats on a two-year term. Reviewers it cites call it very expensive and say small funds struggle to justify it. | [source](https://www.failory.com/blog/pitchbook-pricing) |
<!-- TABLE END -->

## Counts from the script

Output of `python3 -I voc_counts.py`, also saved at [raw/voc/voc_counts_output.txt](raw/voc/voc_counts_output.txt).

<!-- COUNTS START -->
```
saved HN query files: 48
saved web page text files: 35
total rows: 67
by kind: {'quote': 53, 'paraphrase': 14}
rows with a link: 67
verbatim quotes with a link: 53
verbatim quotes from the person's or firm's own publication or own comment: 53

persona x layer (rows):
persona                 say      do       pay      context  total
partner_principal       17       9        2        0        28
solo_angel              8        4        2        0        14
accelerator_screener    4        4        0        0        8
associate               4        3        0        0        7
outsourced_diligence    1        0        2        0        3
corporate_vc            2        0        0        0        2
observer                0        0        0        2        2
fund_staff_unstated     1        0        0        0        1
vendor_claim            0        0        0        1        1
fund_buyers_mixed       0        0        1        0        1

highest layer with evidence, customer personas (pay > do > say):
  partner_principal: highest=pay (2 rows at that layer, 28 rows in all)
  solo_angel: highest=pay (2 rows at that layer, 14 rows in all)
  accelerator_screener: highest=do (4 rows at that layer, 8 rows in all)
  associate: highest=do (3 rows at that layer, 7 rows in all)
  corporate_vc: highest=say (2 rows at that layer, 2 rows in all)

rows by question:
  q3_memo_time: 19
  q2_red_flag: 18
  q1_first_check: 16
  do_workaround: 7
  pay: 7

rows by year:
  2009: 2
  2011: 1
  2012: 1
  2013: 4
  2014: 1
  2016: 2
  2018: 2
  2019: 1
  2021: 3
  2022: 4
  2023: 9
  2024: 4
  2025: 14
  2026: 19
rows before 2020: 14 of 67 (21%)
source types of rows before 2020: {'community_comment': 13, 'own_words': 1}
rows from 2025 or later: 33 of 67 (49%)

source types: {'own_words': 34, 'community_comment': 20, 'podcast_summary': 2, 'interview': 1, 'vendor_case_study': 3, 'journalism': 6, 'third_party_roundup': 1}
```
<!-- COUNTS END -->

## Reddit URLs for Ken

Agents do not fetch reddit.com. Please open each URL in your browser and save the JSON into `docs/reports/20261022.02_research/reddit_corpus/raw/`. Each is a search inside one subreddit. Most cover the past year. A few use all time (`t=all`) because the topic is rare.

1. https://www.reddit.com/r/venturecapital/search.json?q=%22data+room%22&restrict_sr=1&sort=top&t=year
2. https://www.reddit.com/r/venturecapital/search.json?q=%22investment+memo%22&restrict_sr=1&sort=top&t=all
3. https://www.reddit.com/r/venturecapital/search.json?q=associate+diligence+hours&restrict_sr=1&sort=top&t=year
4. https://www.reddit.com/r/venturecapital/search.json?q=%22red+flag%22+missed&restrict_sr=1&sort=top&t=all
5. https://www.reddit.com/r/venturecapital/search.json?q=cohort+churn+diligence&restrict_sr=1&sort=top&t=all
6. https://www.reddit.com/r/venturecapital/search.json?q=ARR+inflated+OR+%22not+recurring%22&restrict_sr=1&sort=top&t=year
7. https://www.reddit.com/r/venturecapital/search.json?q=PitchBook+worth&restrict_sr=1&sort=top&t=year
8. https://www.reddit.com/r/venturecapital/search.json?q=AI+tools+diligence&restrict_sr=1&sort=top&t=year
9. https://www.reddit.com/r/venturecapital/search.json?q=%22first+pass%22+screening&restrict_sr=1&sort=top&t=year
10. https://www.reddit.com/r/venturecapital/search.json?q=Affinity+OR+Harmonic+CRM&restrict_sr=1&sort=top&t=year
11. https://www.reddit.com/r/angelinvestors/search.json?q=%22due+diligence%22&restrict_sr=1&sort=top&t=year
12. https://www.reddit.com/r/angelinvestors/search.json?q=%22red+flags%22+lost&restrict_sr=1&sort=top&t=all
13. https://www.reddit.com/r/angelinvestors/search.json?q=syndicate+diligence+lead&restrict_sr=1&sort=top&t=year
14. https://www.reddit.com/r/startups/search.json?q=%22data+room%22+investor&restrict_sr=1&sort=top&t=year
15. https://www.reddit.com/r/startups/search.json?q=%22due+diligence%22+%22term+sheet%22&restrict_sr=1&sort=top&t=year
16. https://www.reddit.com/r/ycombinator/search.json?q=application+reviewed+partners&restrict_sr=1&sort=top&t=year
17. https://www.reddit.com/r/SaaS/search.json?q=ARR+investors+diligence&restrict_sr=1&sort=top&t=year
18. https://www.reddit.com/r/SaaS/search.json?q=cohort+retention+investors&restrict_sr=1&sort=top&t=year
19. https://www.reddit.com/r/fintech/search.json?q=%22due+diligence%22+venture+automation&restrict_sr=1&sort=top&t=year
20. https://www.reddit.com/r/Entrepreneur/search.json?q=%22investor+due+diligence%22&restrict_sr=1&sort=top&t=year
