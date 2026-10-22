# Research gaps: what the interviews were meant to find, done online

Written 2026-10-22 for the Tricorder hackathon plan. There are no interviews before Saturday, so this file answers the five questions the interviews were meant to fill, from what people wrote online. It adds to [the voice-of-the-customer research](research_voice_of_customer.md) and does not repeat it.

Each quote is marked with its layer. **Say** is what people say about the problem. **Do** is what they do about it today. **Pay** is money or upside they give up to get diligence done. **Context** marks vendors, guides and journalism, which are not people solving the problem. The layers rate how people deal with the problem; they say nothing about who would use or buy Tricorder.

## The five answers

1. **How long a first pass takes.** No trustworthy public number exists for a first-pass memo alone. The best numbers cover all the diligence on a deal: 118 hours on average in a survey of 885 VCs (81 hours at early-stage firms), two to three weeks at one seed fund, and a median of 20 hours for angels in groups. The slowest part is getting the information: chasing documents that have not arrived and researching the market. No source names the writing as the slow part.
2. **Would angels pay for a first pass.** They already pay for diligence, by proxy: group dues of $3,000 to $4,000 a year, 20% carry to syndicate leads, per-deal fees, and about $600 a deal for outside financial diligence in one network. No one in the sample buys a first pass of their own as a product; what they pay per deal for someone else's vetting runs from about $58 to $600.
3. **How decks and rooms reach investors.** No published number says what share of decks or rooms arrive as links. Investors who write about it prefer a PDF in the inbox and open DocSend links reluctantly, or not at all on cold pitches; early data rooms are mostly Google Drive folders.
4. **Regret stories about hidden churn and burn against hiring.** No first-person regret story turned up for churn hidden in a cohort chart, or for burn that did not match a hiring plan. The nearest are a SaaS investor naming high burn as one of his own top mistakes, a collapsed startup whose burn doubled as headcount roughly quadrupled, and an investor watching retention cohorts fall after six months.
5. **What funds pay for diligence.** Funds pay for data subscriptions, financial-diligence tools and AI diligence tools out of the management fee, but no fund published what it pays for a first pass. In a 2026 survey of 250+ venture professionals, spreadsheets were still the most used diligence tool (84%), and price was the top reason for turning a tool down (39%).

## What this means for Tricorder

- **Do not claim a first-pass time saving with a number.** No independent source gives one. A defensible line is the survey's 118 hours of diligence per deal, and the sources' view that gathering, not writing, eats the time.
- **The inbox idea fits how decks arrive.** Decks come as PDF attachments and DocSend links, and investors prefer the PDF. A forwarding address that reads the attachment works with that habit. A DocSend link still needs the viewer's email, as [what a data room is](what_is_a_data_room.md) already notes. The funds' own wishlist in the 2026 survey starts with automation, and inbound parsing is the first item named.
- **Angel pricing has anchors.** Angels pay $3,000 to $4,000 a year to a group that runs diligence with them, or a per-deal fee to a syndicate lead. Per deal, what they give up for someone else's vetting sits between tens and a few hundred dollars, plus carry. A solo-angel price above that range needs a reason.
- **Fund pricing has a ceiling worry and a privacy worry.** Price is the top reason funds reject a tool, and data privacy is the top concern in every category of the same survey. The where-the-data-goes rule in the product brief answers the second.
- **Two planted flags have the best support.** Burn against progress, and a cumulative chart that hides a slowing month, are things investors say they check. Churn hidden in a cohort chart is on every checklist but has no regret story behind it.

## How this was gathered

- Fund and angel posts, angel group pages, price pages, a 2016 academic survey of VCs, a 2026 survey of venture professionals, Hacker News comments through the Algolia API, vendor data and a few news stories. Every page read is saved as text under [raw/gaps/](raw/gaps/), and each file starts with the address it came from.
- Each quote or paraphrase is one row of [gaps_quotes.csv](gaps_quotes.csv), with the same columns as [voc_quotes.csv](voc_quotes.csv). [gaps_counts.py](gaps_counts.py) checks every quote word for word against its saved page, then does all the counting and arithmetic below. Its output is saved at [raw/gaps/gaps_counts_output.txt](raw/gaps/gaps_counts_output.txt).
- Per the script: 82 rows from 52 distinct sources, 69 of them verbatim quotes and 13 paraphrases. All 69 quotes were found in their saved pages.
- Paraphrases are marked with what kind of source they come from. Hacker News roles are self-described. Reddit was not fetched; the list for Ken is at the end.
- Some pages would not give up their text: AngelList's and Odin's pricing pages load by script, and Medium and Inc. blocked the fetch. Those saved files hold only page boilerplate and nothing is quoted from them.

**How old is it?** Per the script, 36% of dated rows are from 2025 or later and 25% are from before 2020. Ten rows are undated, mostly price and membership pages read on 2026-10-22.

## 1. How long does a first-pass memo take, and which part is slowest?

**Answer.** No trustworthy public number exists for a first-pass memo alone; the best numbers cover all diligence on a deal, at 81 to 184 hours depending on stage. The slowest part is getting the information, not writing it up.

### The numbers people give

The one number with a real sample behind it is from a survey of 885 VCs at 681 firms:

- **do** · "The average deal takes 83 days to close; the average firm spends 118 hours on due diligence over that period and the average firm calls 10 references." ([academic survey of VCs, 2016](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf))
- **do** · "The deal period and time on due diligence are shorter for early-stage, IT, and California firms; and longer for late-stage, healthcare, and non-California firms." ([academic survey of VCs, 2016](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf))
- **do** · Paraphrase (survey table): early-stage firms report 81 hours and 73 days to close; late-stage firms report 184 hours and 106 days ([same survey](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf)).

Counted as 8-hour days, the script turns 118 hours into 14.8 working days and 81 hours into 10.1. One of the survey's authors, writing this year, adds the deals that never close:

- **say** · "An investor spends roughly 120 hours on the due diligence that eventually leads to an investment." ([Stanford finance professor, Aug 2026](https://ilyastrebulaev.substack.com/p/due-diligence-what-investors-actually))
- **say** · "Add up the hours burned on those, and the real figure is well north of 250 hours of diligence per completed investment." ([Stanford finance professor, Aug 2026](https://ilyastrebulaev.substack.com/p/due-diligence-what-investors-actually))

These are hours for full diligence, not for the first pass. Seed funds describe the first stretch in days and weeks:

- **do** · "Our diligence process, from the first meeting to the final decision, typically takes two to three weeks at the Pre-Seed and Seed stage." ([seed fund FAQ, undated](https://underscore.vc/?p=80))
- **say** · "if a first meeting doesn’t proceed to a second or some initial diligence within about a week or so, odds are you won’t ultimately end up with a commitment from that firm." ([seed fund partner, Oct 2015](https://nextview.vc/blog/reading-the-tea-leaves-where-am-i-in-my-seed-fundraise-really/))
- **do** · "In parallel, we talk to industry experts and write an investment memo that usually runs 20 to 30 pages." ([seed fund, Nov 2025](https://hsep.substack.com/p/what-we-fund-how-we-decide-and-how))

Angels give smaller numbers. The group study is in section 2. One angel, interviewed about his own process:

- **do** · "If I continue to due diligence, I spend 5-10 hours on that company." ([angel and syndicate co-founder, Aug 2020](https://alltheangels.substack.com/p/angel-interview-3-ali-altaf))

At the very first look, the numbers are minutes. An angel who ran a pitch event: "I can tell in two minutes if something is really bad." ([angel, Feb 2010](https://news.ycombinator.com/item?id=1156052)) **say**. DocSend, which sells deck-sharing links, says "our data shows that investors spend less than 3 minutes reviewing pitch decks these days." ([DocSend's own data, Apr 2025](https://www.dropbox.com/resources/docsend-pitch-deck-research)) **context**.

### Claims to treat as sales copy or practice

- **context** · A diligence-tool vendor says a growth fund's analysts spent days compiling data and drafting preliminary memos, that its tool now makes one in under 30 minutes, and that full diligence fell from 20 days to 7 ([vendor case study, Jan 2026](https://www.wokelo.ai/blog/how-wokelo-helped-a-growth-equity-vc-supercharge-diligence-with-a-crm-integration)).
- **context** · An interview-prep guide says a VC job candidate should be able to write a three-page practice memo in 4 to 6 hours after 2 to 3 hours of research ([third-party guide, undated](https://vcbeast.com/vc-case-study-guide)). That is an exercise, not a deal.

### Which part is slowest

Getting the information. Three investors describe it in their own words:

- **do** · "The 15 hours is very skewed typically towards one or two companies, where 2-3 hours are speaking to founders, and the rest of it is researching the market." ([angel and syndicate co-founder, Aug 2020](https://alltheangels.substack.com/p/angel-interview-3-ali-altaf))
- **do** · "As an investor now, I often jump from one company to another without dedicating half a day to each. The main reason? The information I need isn't usually there, leading to back-and-forth emails with founders." ([founder turned investor and syndicate lead, Aug 2024](https://elitegamedevelopers.substack.com/p/the-essential-startup-data-room-key))
- **say** · "What’s still missing after multiple requests is rarely benign." ([investor writing on how he builds a memo, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company))

A technical diligence consultant adds that at seed the financial and legal work is small: "Due diligence for a larger company can take several weeks, at the start-up level there is usually not a whole lot in terms of financial and legal, later those are actually the bigger portion of the time." ([diligence consultant, Oct 2009](https://news.ycombinator.com/item?id=866350)) **say**.

This matches the voice-of-the-customer research: the gathering is slow, and Tricorder's job is to have it done before the operator looks.

## 2. Would angels pay for a first pass of their own, and what is it worth per deal?

**Answer.** Angels already pay for diligence by proxy, in dues, carry and per-deal fees, because they want it and lack the time. No one in the sample buys a first pass of their own as a product, so the worth per deal comes from what they pay others: about $58 to $600 a deal, plus 20% carry when a lead does the work.

### Angels want diligence, and the study says it pays

- **do** · Paraphrase (association slides on the Wiltbank study of angels in groups): the median angel spent 20 hours on due diligence per deal, and 26% spent over 40 hours. The overall multiple for high-diligence investments was 5.9 times over 4.1 years, and for low-diligence investments 1.1 times over 3.4 years ([Angel Capital Education Foundation slides, Apr 2009](https://www.angelcapitalassociation.org/data/Documents/Resources/AngelGroupResarch/1d%20-%20Resources%20-%20Research/ACEF%20Angel%20Performance%20Project%2004.28.09.pdf)).
- **say** · "Some research indicates that a third of angel investments are made after less than 10 hours of due diligence." ([angel association blog, Aug 2015](https://angelcapitalassociation.org/?p=6582))
- **say** · "spending three to six months on a deal in a hyper-competitive environment can lead to a very different outcome than it did 15 years ago." ([venture fund newsletter, Feb 2025](https://vcunfiltered.beehiiv.com/p/how-extended-due-diligence-became-a-liability-for-angel-groups-in-today-s-rapid-fire-startup-world))

So angels know diligence matters and know it takes too long. That is the gap a cheaper first pass fills.

### What they pay today: group dues, with diligence built in

Both New York groups in the sample charge dues and have members do diligence together:

- **pay** · "What are the annual membership dues? $4,000" and "NYA members are expected to invest $50,000 per year." ([New York angel group FAQ, undated](https://www.newyorkangels.com/membership-benefits-criteria-faq))
- **do** · "Members get involved and dedicate time to attending screening sessions, taking an active role in due diligence and identifying investment opportunities." ([same FAQ](https://www.newyorkangels.com/membership-benefits-criteria-faq))
- **pay** · "Annual membership dues are $5000 in the first year (which includes cost of the startup investing training) and $3000 each subsequent year" ([New York angel network, undated](https://www.37angels.com/curriculum))
- **do** · Members must "Participate in at least one diligence team per year (writing a portion of a diligence memo)" ([same page](https://www.37angels.com/curriculum)).

Per the script, the first group's dues are 8% of the investing it expects each year. The second group's later-year dues are 12% of the one $25,000 investment it requires, and 20% in the first year.

Older groups charged the same way: "Keiretsu and CTEK both have “membership fees” paid by their angel investors that help to defray these costs" ([seed investor's blog, Mar 2007](https://davidgcohen.com/2007/03/18/say-hiya-to-the-keiretsu-forum/)) **pay**. A 2026 guide lists what dues pay for in one group: "Dues can support staff, member meetings, screening tools, education, travel, and group operations." ([angel community operator's guide, Sep 2026](https://www2.hustlefund.vc/post/angel-squad-angel-investor-network-fees-decoded-what-youre-really-paying-for)) **context**.

### What they pay today: cash for someone else's diligence

- **pay** · Paraphrase (business school case study): a Lagos angel network pays outside firms to do financial due diligence for its members, about $600 per deal; individual membership is about $600 a year ([case study, PDF dated Nov 2020](https://case.fuqua.duke.edu/wp-content/uploads/2025/03/Angel-Network-Spotlight_Lagos-Angel-Network.pdf)).
- **pay** · "www.Bioability.com lists a cost of $4,900 for their Investor Due Diligence Report Service, which takes 4 – 6 weeks." ([angel association best-practice guide, Sep 2007](https://www.angelcapitalassociation.org/data/Documents/Resources/AngelCapitalEducation/ACEF_BEST_PRACTICES_Due_Diligence.pdf))
- **say** · "Investors should also be ready to shoulder the cost of the due diligence process, which may prove to be considerable." ([same guide](https://www.angelcapitalassociation.org/data/Documents/Resources/AngelCapitalEducation/ACEF_BEST_PRACTICES_Due_Diligence.pdf))

### What they pay today: carry and fees to a syndicate lead

A syndicate lead picks the deal and does the checking; members pay in fees and in a share of any gain.

- **say** · "The syndicate leads take the carry and do most of the due diligence" ([observer of AngelList, Oct 2015](https://news.ycombinator.com/item?id=10373554))
- **pay** · "One of the terms grants me the lead status and 20% of carried interest." ([syndicate lead, Mar 2023](https://elitegamedevelopers.substack.com/p/egd-news-176-10-lessons-from-my-gaming-angel-syndicate))
- **pay** · "I charge a one-time fee, per deal, per participating member of 500 USD for operational costs." Later: "In 2023, I changed the fee policy to a 7% of the invested capital model" ([same syndicate lead](https://elitegamedevelopers.substack.com/p/egd-news-176-10-lessons-from-my-gaming-angel-syndicate)).
- **context** · "AngelList’s SPV carry guide says the manager sets carry and 20% is standard on its platform." ([angel community operator's guide, Sep 2026](https://www2.hustlefund.vc/post/angel-squad-angel-investor-network-fees-decoded-what-youre-really-paying-for))
- **context** · The vehicle itself also costs money: "Starts at $4,500 one time 2% of capital raised, between $2,500 and $12,500, plus a $2,000 regulatory fee." ([SPV provider's price page, undated](https://sydecar.io/pricing)). Per the script, that is $4,500 to $14,500 per deal, before any diligence.

The lead's $500 fee is 20% of that syndicate's $2,500 minimum check, per the script; the later 7% fee on the same check is $175.

### What they pay today: a membership that vets deals for them

- **pay** · "Fast Track (33% off) $875 per month (4 Payments) $3,500 total" ([angel community price page, undated](https://www.hustlefund.vc/trialpayment))
- **context** · What the money buys: "Every deal comes with the context: the company, the founders, the terms, and why Hustle Fund invested." The same page says the fund reviews over 1,000 deals a month and shares 3 to 5 ([angel community page, undated](https://www.hustlefund.vc/paymentpage)).

Spread over one year of shared deals, the script puts that at $58 to $97 per deal shown. The same seller tells members that "Active angel investing requires 3-5 hours weekly." ([angel community operator's guide, 2026](https://www.hustlefund.vc/post/angel-squad-how-to-become-an-angel-investor-in-2026-even-with-a-full-time-job)) **context**.

### What a first pass is worth per deal

Nobody quoted here prices a first pass as a separate product. What angels already give up per deal for someone else's vetting, from the figures above:

| What they pay | Per deal | Source |
|---|---|---|
| Membership that shares vetted deals | $58 to $97 per deal shown (script) | [price page](https://www.hustlefund.vc/trialpayment) |
| Syndicate lead's later percentage fee on a $2,500 check | $175 (script) | [syndicate lead](https://elitegamedevelopers.substack.com/p/egd-news-176-10-lessons-from-my-gaming-angel-syndicate) |
| Syndicate lead's flat fee | $500 | [syndicate lead](https://elitegamedevelopers.substack.com/p/egd-news-176-10-lessons-from-my-gaming-angel-syndicate) |
| Network-paid outside financial diligence | about $600 | [case study](https://case.fuqua.duke.edu/wp-content/uploads/2025/03/Angel-Network-Spotlight_Lagos-Angel-Network.pdf) |
| Third-party diligence report (2007 price) | $4,900 | [association guide](https://www.angelcapitalassociation.org/data/Documents/Resources/AngelCapitalEducation/ACEF_BEST_PRACTICES_Due_Diligence.pdf) |
| Lead's carry | 20% of any gain | [syndicate lead](https://elitegamedevelopers.substack.com/p/egd-news-176-10-lessons-from-my-gaming-angel-syndicate) |

The figures are from different years and places. They show the range of what angels already pay, not a price Tricorder can charge.

## 3. How do data rooms reach investors, and what do they open first?

**Answer.** No published number says what share of decks or data rooms arrive as DocSend links, Drive folders or attachments. Investors who write about it prefer a PDF in the inbox; early rooms are mostly Drive folders, with DocSend and Notion behind them.

### No share figure exists

DocSend publishes how long investors spend on decks and counts the links founders create on its own service. It does not say what share of all decks travel as links. Its own definition shows why: "A "link" refers to the unique URL a founder creates using DocSend to share their pitch deck with investors." ([DocSend press release, Jul 2023](https://www.nasdaq.com/press-release/docsend-mid-year-2023-pitch-deck-interest-analysis-indicates-growing-gap-in-founder)) **context**. Its time data: "in 2020, investors spent over four minutes looking at pitch decks that successfully raised money, but only one minute, 30 seconds on decks that didn’t manage to raise." ([DocSend's own data, Apr 2025](https://www.dropbox.com/resources/docsend-pitch-deck-research)) **context**. No investor survey of link against attachment turned up either. Carta's rooms serve fund managers and their own investors, as [what a data room is](what_is_a_data_room.md) covers; no source here describes a startup room arriving through Carta or Visible.

### What investors say about links and attachments

- **do** · "I rarely open docsend docs and never on cold pitches." ([angel investor, May 2018](https://news.ycombinator.com/item?id=17098497))
- **do** · "I do like having the deck in my inbox so that when the pitch changes I can see what they once did." ([same angel, May 2018](https://news.ycombinator.com/item?id=17098497))
- **say** · "I'm an investor and I don't love clicking on the docsend links, but I will." ([same angel, Aug 2020](https://news.ycombinator.com/item?id=24165769))
- **say** · "The worst part of docsend for me is I will get an email saying "check out our new thing" and then I click on it sometime later to look at it again and it's already expired." ([same angel, Aug 2020](https://news.ycombinator.com/item?id=24165769))
- **say** · "For what it's worth, many investors strongly dislike DocSend. It helps founders track views but adds friction." ([seed fund partner, May 2018](https://news.ycombinator.com/item?id=17096692))
- **say** · "Thing is, and a few investors agree, that it’s kind of annoying. Investors would prefer to just open an attachment in their mail client." ([investor and fundraising adviser, Dec 2019](https://www.alexanderjarvis.com/pitch-thinking-9-how-to-send-your-deck-to-investors/))
- **say** · "There's a lot of investor hate around docsend,etc." ([founder, Feb 2020](https://news.ycombinator.com/item?id=22430714)) and "It should be an attachment in the PDF format, not password-protected link like with DocSend or alike." ([commenter, Sep 2022](https://news.ycombinator.com/item?id=32837926)).
- **context** · A newsletter that talked to several VCs reports the same two complaints: tracking makes VCs read less, and an expired link loses the second look months later ([newsletter, May 2023](https://theventurecrew.substack.com/p/breaking-the-mold-why-founders-should)).

### How the room itself is shared

- **do** · "For added convenience, I prefer Google Drive folders containing all necessary documents under folders." ([founder turned investor, Aug 2024](https://elitegamedevelopers.substack.com/p/the-essential-startup-data-room-key))
- **say** · "Many use DocSend for its flexibility in tracking usage and investor interest in specific documents. Another favorite is Notion" ([same investor](https://elitegamedevelopers.substack.com/p/the-essential-startup-data-room-key))
- **context** · "Google Drive remains the most common "data room" used at the pre-seed stage" ([data-room vendor's blog, Mar 2026](https://www.ellty.com/blog/virtual-data-room-for-seed-round)). The vendor sells an alternative to Drive.

### What they open first

The voice-of-the-customer research already covers the reading order: an associate's ten browser tabs before the room, then the cap table, model, incorporation papers and IP assignments. One addition, from a fund partner describing his own process after a first meeting: "The first thing is to verify market size and whether it foots with the data the company presented." ([fund partner, Apr 2013](https://www.tomtunguz.com/breaking-down-a-typical-vcstartup-diligence-process/)) **do**.

The funds' own wishlist points the same way as Tricorder's inbox idea. Paraphrase (survey of 250+ venture professionals): the first theme on the wishlist for the next 12 months is automation, and inbound parsing is the first item named under it ([survey, May 2026](https://ewvc.beehiiv.com/p/vc-tech-stack-pulse-2026)) **say**.

## 4. Regret stories about hidden churn and about burn against the hiring plan

**Answer.** No first-person regret story turned up for churn hidden in a cohort chart, and none for burn that did not match a hiring plan. The nearest are investors naming high burn and lurking churn as mistakes, a startup whose burn doubled as headcount roughly quadrupled, and an investor watching retention cohorts fall.

### Burn

- **say** · A SaaS investor lists his own top seed investing mistakes, including "Investing when growth is strong but the burn rate is too high", and explains: "if the burn rate is too high, I find they tend to run out of money as they scale to $5m-$10m ARR." ([SaaS investor, Mar 2023](https://www.saastr.com/10-of-my-top-seed-investing-mistakes))
- **say** · "Almost every founder regrets using capital to keep a high-burn rate engine going that isn’t scaling rapidly." ([same investor, May 2024](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/))
- **do** · "I look at burn against progress: a team that did a lot on a little earns real trust, and a team that burned a lot to produce very little earns uncompromising scrutiny." ([investor writing on how he builds a memo, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company))
- **context** · Paraphrase (newsletter post-mortem citing podcasts and The Information): the checkout startup Fast burned about $10 million a month against about $600,000 of 2021 revenue. Its founder said burn doubled in the last two quarters of 2021, partly because headcount ballooned, from about 90 people to about 400 ([newsletter, Apr 2022](https://kjlabuz.substack.com/p/fast)). It shut down a year after a $102 million Series B ([journalism, Apr 2022](https://techcrunch.com/2022/04/05/fast-shuts-doors-after-slow-growth-high-burn-precluded-fundraising-options)).

Fast is the closest public case of burn running ahead of a business because of hiring. No investor in it has written that they missed it in diligence.

### Churn

- **say** · "Churn is a problem that lurks, especially in annual deals. If your churn is too high, a lot of that revenue isn’t even real." ([SaaS investor, May 2024](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/))
- **say** · "Cumulative charts are where founders hide a slowing month, because the line only ever goes up even when the pace underneath it is falling." ([investor writing on how he builds a memo, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company))
- **say** · An early investor in a social app, defending its founder's next company: "the company didn't invest deeply enough into moderation and the long term retention cohorts went down steeply past 6 months of use." ([early investor, Feb 2020](https://news.ycombinator.com/item?id=22362973)) The cohorts fell in plain view; this is not a hidden-churn story.
- **say** · "A thoughtful investor will be more interested in paid active users and cohort analysis of retention (in terms of actual usage) rather than subscription numbers/revenue in absolute terms." ([commenter, Feb 2025](https://news.ycombinator.com/item?id=42947897))

The voice-of-the-customer research found the same gap. Hidden churn is on every checklist, but people do not write about the time they missed it. The cumulative-chart point above is the nearest investor's-eye version, and it is easy to plant in the demo data room.

## 5. What do funds pay for first-pass diligence or diligence tooling?

**Answer.** Funds pay for data subscriptions, financial-diligence tools and AI diligence tools, out of the management fee; none published what it spends on a first pass. Spreadsheets are still the most used diligence tool, and price is the top reason funds turn a tool down.

### What a 2026 survey of funds found

Paraphrases of a survey of 250+ venture professionals across $80 billion of assets, half partners and half operations or investment staff ([survey, May 2026](https://ewvc.beehiiv.com/p/vc-tech-stack-pulse-2026)):

- **do** · Excel or Google Sheets is the most used due diligence tool, at 84%. Claude is the most loved diligence tool, and the tool most often named as the latest firm-wide adoption (22%).
- **say** · Pricing is the top reason funds reject a tool, at 39% of rejections, and it holds for funds of every size. Data privacy is the top concern in every category.
- **do** · "15%+ of funds rely on custom-built tools somewhere in their stack"

### What funds say they use and pay for

From a 2023 roundup in which 20 investors described their own tools ([fund stacks roundup, Aug 2023](https://signatureblock.co/articles/vc-fund-stacks)):

- **pay** · One fund's investor: "We use SaaSGrid to do financial diligence on all our B2B deals."
- **do** · The same investor: "If they don’t use SaaSGrid, we collect raw data from them (an MRR waterfall and P&L) and create our own SaaSGrid dashboard to analyze their numbers."
- **pay** · A seed fund partner on PitchBook: "Used for doing research on companies, market comps, competitive landscapes, etc. The data is not perfect, but it's pretty good."
- **pay** · A small fund's founder: "We often refer to Crunchbase to gather intel on prior rounds."
- **pay** · A solo fund manager on an AI diligence tool: "A powerful diligence tool, which we combine with our own AI analyst."

Funds also build their own. One seed fund released its memo tool: "we're open-sourcing our proprietary AI-powered memo generator" ([seed fund, Jan 2025](https://www.flybridge.com/ideas/the-bow/behind-the-curtain-unveiling-our-ai-powered-investment-memo-generator)) **do**. At small check sizes, diligence is often done as a favour: "When taken as a percentage of the value of the deal due diligence can cost quite a bit in early stage investments, so it can be a partner or the CFO/CTO of a company 'friendly' to the VC (or one they've already invested in) that will have a thorough look." ([diligence consultant, Oct 2009](https://news.ycombinator.com/item?id=866350)) **do**.

### Who pays inside a fund

Tools come out of the managers' own fee, not the fund's capital. A fund-administration vendor lists what management fees cover, including "Technology subscriptions for market data, research, and communication" ([fund admin vendor's guide, Sep 2025](https://carta.com/learn/private-funds/management/management-fees/)) **context**. A fund finance writer puts "General technology systems and software used across multiple funds" on the management company and "Broken deal expenses (transaction costs for deals that do not close)" on the fund ([fund finance newsletter, Jan 2026](https://dannybloomstine.beehiiv.com/p/fund-expenses-vs-management-company-expenses-what-gets-charged-where-and-why-it-matters)) **context**. So a first-pass tool competes for the same fee that pays salaries and data.

### Prices with some volume behind them

- **pay** · Paraphrase (price roundup from procurement data): the median PitchBook contract is $30,000 a year across 125 buyer-reported purchases; a count of 114 transactions ran from $20,000 to $124,000. The site says it could not re-check the underlying data in October 2026 ([third-party price roundup, Oct 2026](https://costbench.com/software/financial-data-terminals/pitchbook)).
- **say** · Asked whether a $25,000-a-year PitchBook subscription was worth it for finding investors in a small fund, a community member answered: "Don’t do this for your first fund. The ROI is not worth it." ([fund-manager community Q&A, May 2023](https://decilegroup.com/posts/is-subscribing-to-pitchbook-for-25k-year-worthwhile-to-access-potential-lps-for-a-small-fund)) The question was about finding investors, not diligence.
- **context** · "Bessemer Venture Partners reclaimed 234 hours per analyst after integrating AI into their workflows" ([CRM vendor's guide, Sep 2026](https://www.affinity.co/guides/vc-ai-tools)). Unverified and from a vendor.
- **context** · The diligence-tool vendor from section 1 says its fund client's analysts now screen up to 250 deals a month, up from 100; it names neither the fund nor the price ([vendor case study, Jan 2026](https://www.wokelo.ai/blog/how-wokelo-helped-a-growth-equity-vc-supercharge-diligence-with-a-crm-integration)).

The [landscape research](research_landscape.md) has the tool vendors' list prices. This section adds the funds' side: they pay, they mostly still use spreadsheets, and price and privacy decide what they keep.

## Counts from the script

Layer counts by question, per `python3 -I gaps_counts.py`. The full output, including the persona table and every figure used above, is in [raw/gaps/gaps_counts_output.txt](raw/gaps/gaps_counts_output.txt).

```
question                say      do       pay      context  total
q1_memo_time            6        8        0        3        17
q2_angel_pay            4        3        10       5        22
q3_data_room_delivery   8        4        0        4        16
q4_regret               7        1        0        2        10
q5_fund_pay             2        5        5        5        17
```

Pay-layer rows appear only in the angel and fund questions. Nobody pays anything in the regret stories, which is part of why they are hard to find.

## Reddit URLs for Ken

Agents do not fetch reddit.com. Please open each URL in your browser and save the JSON into `docs/reports/20261022.02_research/reddit_corpus/raw/`. These add to the list at the end of the voice-of-the-customer research and do not repeat it.

1. https://www.reddit.com/r/venturecapital/search.json?q=memo+hours+associate&restrict_sr=1&sort=top&t=all
2. https://www.reddit.com/r/venturecapital/search.json?q=%22how+long%22+diligence+seed&restrict_sr=1&sort=top&t=all
3. https://www.reddit.com/r/venturecapital/search.json?q=docsend+pdf&restrict_sr=1&sort=top&t=all
4. https://www.reddit.com/r/venturecapital/search.json?q=%22data+room%22+%22google+drive%22&restrict_sr=1&sort=top&t=all
5. https://www.reddit.com/r/venturecapital/search.json?q=%22hiring+plan%22+burn&restrict_sr=1&sort=top&t=all
6. https://www.reddit.com/r/venturecapital/search.json?q=cohort+churn+missed&restrict_sr=1&sort=top&t=all
7. https://www.reddit.com/r/venturecapital/search.json?q=%22tech+stack%22+fund+tools&restrict_sr=1&sort=top&t=year
8. https://www.reddit.com/r/venturecapital/search.json?q=pitchbook+harmonic+price&restrict_sr=1&sort=top&t=year
9. https://www.reddit.com/r/angelinvestors/search.json?q=%22angel+group%22+dues&restrict_sr=1&sort=top&t=all
10. https://www.reddit.com/r/angelinvestors/search.json?q=syndicate+carry+worth&restrict_sr=1&sort=top&t=all
11. https://www.reddit.com/r/angelinvestors/search.json?q=%22due+diligence%22+hours&restrict_sr=1&sort=top&t=all
12. https://www.reddit.com/r/angelinvestors/search.json?q=%22angel+squad%22&restrict_sr=1&sort=top&t=all
13. https://www.reddit.com/r/startups/search.json?q=docsend+investors+pdf&restrict_sr=1&sort=top&t=all
14. https://www.reddit.com/r/startups/search.json?q=%22burn+rate%22+hired+too+fast+shut+down&restrict_sr=1&sort=top&t=all
15. https://www.reddit.com/r/SaaS/search.json?q=%22net+revenue+retention%22+misleading&restrict_sr=1&sort=top&t=all
