# Research: published investment memos and memo templates

Written 2026-10-22 for the memo template ([MEMO_TEMPLATE.md](../../ongoing/MEMO_TEMPLATE.md)). Commissioned by the 1:58 PM block of [the writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), with the 2:00 PM block (interactive memos) and the 2:01 PM block (each reader's own copy and scenarios).

## Summary

- **What was saved.** 28 real investment memos and 6 memo templates. The memos come from three funds and one angel: Bessemer Venture Partners (19), Root Ventures (7), Blackbird Ventures (1) and one angel memo by a partner who later joined Root. By stage, 13 are seed, 5 Series A, 5 Series B and 5 other or not named. They are dated 2005 to 2020 where the memo states a year. The templates come from Hustle Fund, Point Nine, Compound (Michael Dempsey), NextView, an Angel Capital Association workshop deck, and Visible.
- **The shared spine.** Almost every memo has a product section, a team section, deal terms and a competition section. Most open with a summary and the ask, and most close with a conclusion. Risks sit near the end, after the deal.
- **The usual order.** Summary and the ask, company and problem, market, product, business model, traction, competition, financials, team, deal terms, risks, outcomes, then the conclusion. Diligence notes and appendices come last.
- **Length.** The median memo runs about 2,500 words in about 9 sections. Bessemer's run longer than Root's.
- **Risks** are a short labelled list near the end, rarely with mitigations. A few memos write them as questions to settle before the next round, which is the shape of Tricorder's ask list.
- **Evidence.** Bessemer memos are dense with numbers and cite almost nothing by link. Root's memos link out freely. Only the newest template asks for a source and a date on every important statement.
- **Nothing published is interactive in Tricorder's sense.** Some pages let a reader jump to a section, and some memos link out to sources. None lets a reader click a line and see the passage behind it, and none lets a reader change an assumption. Bessemer's fixed scenario tables are the closest thing to reader scenarios, and most of them are published as pictures.

Every number in this file comes from [memo_sections.py](memo_sections.py), which writes [memos.csv](memos.csv), [memo_section_labels.csv](memo_section_labels.csv), [memo_section_counts.csv](memo_section_counts.csv), [memo_stats.csv](memo_stats.csv) and [memo_summary.json](memo_summary.json). The pages were fetched with [memo_fetch.py](memo_fetch.py) and saved as text under [raw/memos](raw/memos/INDEX.md). Headings and quotes come only from those saved files.

## What was saved

[memos.csv](memos.csv) has one row per memo and template: title, company, fund, stage, year, URL, saved file, and the section headings as they appear.

**Bessemer Venture Partners.** Bessemer publishes its memos in an archive at [bvp.com/atlas?type=memo](https://www.bvp.com/atlas?type=memo). All 19 are saved: Yelp, LifeLock, LinkedIn, Wix, Dropcam, Twilio, Mindbody, Shopify, Medi Assist, Fiverr, Pinterest, SendGrid, Twitch, Auth0, PagerDuty, Rocket Lab, ServiceTitan, Velo3D and Toast. Each is a partner's recommendation to the partnership, from seed checks (Twilio's is a $125,000 extension) to Series B. Two fall outside seed to Series B and are kept for their structure: LinkedIn (Series C) and Medi Assist (a management buyout).

**Root Ventures.** Root keeps its memos as Markdown files on GitHub at [rootvc/investment-memos](https://github.com/rootvc/investment-memos). All seven are seed memos: Esper, Meroxa, Daily, Okteto, Privacy Dynamics, Superconductive and Zed. The repo's front page says some parts are edited out: "Some things have to be edited/redacted, particularly around personal references and diligence, pricing, and any information about the company or product that would be of competitive interest." ([Root Ventures, README](https://github.com/rootvc/investment-memos/blob/main/README.md)). The same repo links a partner's earlier angel memo on Esper ([Lee Edwards, Esper angel memo](https://github.com/ledwards/investment-memos/blob/main/esper.md)), which is saved too.

**Blackbird Ventures.** The Zoox seed memo Blackbird sent its investors in 2014, published on its blog in 2018 ([Blackbird, Investment Notes: Zoox](https://blackbird.vc/blog/zoox-memory-lane)).

**Templates.**

- Hustle Fund's copyable template for angels, with a worked example ([Hustle Fund, investment memo template](https://www.hustlefund.vc/post/investment-memo-template)).
- Point Nine's open-source deal memo template, a Google Doc ([Point Nine template](https://docs.google.com/document/d/1zLMTk_s_As7mjZwOAJwHc6-6H0JhEety8ZLEG2NtTN0/edit)).
- Michael Dempsey's seed memo template at Compound, a Google Doc ([Dempsey template](https://docs.google.com/document/d/1tlqi-nPgScyG78uwVX6BOwhukztvLaZbFgRh2bF-xog/edit)), with his notes on it ([Dempsey, On My Mind #7](https://mhdempsey.substack.com/p/on-my-mind-7)).
- NextView's description of its seed memo, section by section ([NextView, The Investment Memo](https://nextview.vc/blog/the-investment-memo/)).
- The topics an angel group's diligence report covers, from an Angel Capital Association board member's workshop deck ([ACA, The Basics of Due Diligence](https://angelcapitalassociation.org/data/Secure/Angel%20Insights%20Exchange%20Library/2016-Nashville/BasicsofDueDiligence-Presentation.pdf?rev=F688)).
- Visible's guide, written for founders who send investors a memo ([Visible, Investment Memo](https://visible.vc/blog/investment-memo/)).

**Saved but not counted.** Seven files were read and left out of the counts, each for the reason the script records. The DoorDash, Snapchat and YouTube pages hold commentary or audio, not the memo text. The Confluence.VC and LaTeX pages do not hold their templates' sections. Dempsey's post is his notes on his own template, used below for how risks are written. The Root repo's index page is not a memo. No Carta, HBS, Stanford GSB or NFX template with readable sections turned up in the search. Medium pages (Point Nine's post, Ali Tamaseb's template) refused the fetch.

## Which sections appear, and how often

[memo_sections.py](memo_sections.py) reads each memo's headings in order and sorts each heading into one of the canonical sections below, by a fixed list of rules in the script. A heading that names two things (for example "Traction/Financials") gets a main section and a second one. A memo "has" a section if any heading lands there. [memo_section_labels.csv](memo_section_labels.csv) has one row per heading with its assigned section, so any label can be checked. 316 headings were labelled. Two landed in "Other": Blackbird's "Full Story" (the whole memo under one heading) and the angel-group deck's "Legal & Regulatory Environment".

Ordered by where the section sits in the memos (0 is the first heading, 1 is the last; the median across memos):

| Section | Memos that have it | Templates that have it | Median position |
|---|---|---|---|
| Summary and the ask | 17 of 28 | 4 of 6 | 0.0 |
| Why invest (the merits) | 1 of 28 | 1 of 6 | 0.0 |
| Company and problem | 6 of 28 | 4 of 6 | 0.08 |
| Market | 17 of 28 | 6 of 6 | 0.12 |
| Product | 25 of 28 | 5 of 6 | 0.2 |
| Unit economics | 3 of 28 | 0 of 6 | 0.29 |
| Business model and sales | 11 of 28 | 6 of 6 | 0.31 |
| Traction and metrics | 13 of 28 | 3 of 6 | 0.33 |
| Competition | 21 of 28 | 5 of 6 | 0.5 |
| Financials | 10 of 28 | 4 of 6 | 0.5 |
| Team | 25 of 28 | 6 of 6 | 0.55 |
| Deal terms | 23 of 28 | 5 of 6 | 0.75 |
| Risks and open questions | 16 of 28 | 4 of 6 | 0.79 |
| Outcomes and returns | 11 of 28 | 3 of 6 | 0.86 |
| Sources and change log | 1 of 28 | 1 of 6 | 0.9 |
| Conclusion and recommendation | 17 of 28 | 1 of 6 | 1.0 |
| Diligence and reference calls | 8 of 28 | 2 of 6 | 1.0 |
| Appendix | 6 of 28 | 0 of 6 | 1.0 |

Three things the headings alone undercount:

- **The summary.** Every Bessemer memo opens with a To, From, Date and Re block (19 of 19), and many then go straight into an untitled opening paragraph with the ask. Counting an untitled opening of 100 words or more as a summary, 25 of 28 memos open with one.
- **The numbers.** Traction, unit economics and financials are split three ways. 18 of 28 memos have at least one of them.
- **The recommendation.** A phrase such as "we recommend" or "we have signed a term sheet" appears in 20 of 28 memos, and in the first 150 words of 13. The script's phrase list is in [memo_sections.py](memo_sections.py), so a memo that recommends in other words is missed.

Heading names vary more than the sections do. Bessemer writes "Deal", "The Deal", "Financing" and "Timeline/Financials/Fundraising" for the same job, and Toast heads its risks "Key Risks/Ways This Can Fail" ([Bessemer, Toast](https://www.bvp.com/memos/toast)).

## The usual order

From the median positions above, a memo runs in this order:

1. Summary and the ask (the round, the check, the recommendation in a paragraph)
2. Company and problem
3. Market
4. Product
5. Business model, unit economics and traction
6. Competition
7. Financials
8. Team
9. Deal terms
10. Risks and open questions
11. Outcomes and returns
12. Conclusion and recommendation
13. Diligence notes, sources and appendices

The two families differ in one way that matters. Bessemer puts the team in the middle and ends on a conclusion. Root sometimes leads with the team (Meroxa and Superconductive open on it). No Root memo has a conclusion. Meroxa, Okteto, Privacy Dynamics, Superconductive and Zed end on their diligence calls. The templates agree with Bessemer's spine. Hustle Fund's runs: decision snapshot, company and problem, product, market and competition, business model, traction, team, financial position, cap table and terms, risks and open questions, outcome cases, portfolio fit, final recommendation, sources and change log ([Hustle Fund](https://www.hustlefund.vc/post/investment-memo-template)).

## Typical length

From [memo_stats.csv](memo_stats.csv), counting the words of each memo's body:

- The median memo is 2,535.5 words. The shortest is 687 (the one-page angel memo) and the longest 4,732.
- Bessemer's median is 2,948 words. Root's is 1,812.
- The median memo has 9 sections. The range is 1 to 14.

Visible's guide, written for founders, says a seed memo runs two to four pages and a Series A memo five to ten ([Visible](https://visible.vc/blog/investment-memo/), "Seed vs. Series A"). The author of the one-page Esper angel memo later wrote that one page is far too short for a deal memo, though his was an angel check and not a lead investment ([Lee Edwards, Esper angel memo](https://github.com/ledwards/investment-memos/blob/main/esper.md), opening note).

## How risks and open questions are written

16 of 28 memos have a risks section. Its median length is 250.5 words.

- **A short labelled list.** 13 of the 16 write risks as a list: a short label, then one or two sentences. Pinterest's opens with "Monetization", "Consumer Adoption", "Competition" and "Team" ([Bessemer, Pinterest](https://www.bvp.com/memos/pinterest)). Auth0's opens with "Competition", "Market size" and "Technology" ([Bessemer, Auth0](https://www.bvp.com/memos/auth0)).
- **The rebuttal sits inside the risk.** Most entries name the risk and then say why the authors still believe, in the same paragraph. Only 1 of the 16 uses the word "mitigation". Dempsey explains why in his notes on his template: "for many risks, there are no mitigations." ([Dempsey, On My Mind #7](https://mhdempsey.substack.com/p/on-my-mind-7)).
- **Risks as questions to settle.** 6 of the 16 phrase some risks as open questions. Dropcam's section is headed "Risks / Additional Questions to Pursue Prior to Series A" and lists the proof points the fund wants before the next round ([Bessemer, Dropcam](https://www.bvp.com/memos/dropcam)). ServiceTitan's risks are questions, each followed by evidence ([Bessemer, ServiceTitan](https://www.bvp.com/memos/servicetitan)). This is the shape of Tricorder's ask list: what would settle the doubt, and from whom.
- **The templates ask for more structure.** Hustle Fund wants three to five ranked risks, each with a failure mode, current evidence, likelihood, impact, mitigation and a decision trigger, then a list of open questions with an owner, the source needed and a deadline. Its test for a risk: "“The team needs to execute” is not a risk. “The two pilots must become annual contracts before the company runs out of cash” is." ([Hustle Fund](https://www.hustlefund.vc/post/investment-memo-template)). Dempsey's template is a two-column table, risk against mitigating factor ([Dempsey template](https://docs.google.com/document/d/1tlqi-nPgScyG78uwVX6BOwhukztvLaZbFgRh2bF-xog/edit)). NextView puts "Investment Positives" and "Investment Concerns" side by side, no more than four positives ([NextView](https://nextview.vc/blog/the-investment-memo/)).

Outcomes are written as a few fixed scenarios with an exit value and the fund's return. 11 of 28 memos have an outcomes section. In 7 of those 11, the section's only content is a picture of a table, so the numbers are not in the page text ([Bessemer, Yelp](https://www.bvp.com/memos/yelp), "Scenario Analysis"; the saved file shows `[image]`).

## How the memos cite evidence

- **Numbers, mostly unsourced.** A Bessemer memo carries a median of 83 numbers (dollar amounts, percentages and figures of two digits or more, by the script's pattern). Root's carry 20. Bessemer's numbers come with no link and rarely a named file. The reader trusts the partner.
- **Links out.** 13 of 28 memos link to at least one outside page. The median Bessemer memo has none; the median Root memo has 6. Privacy Dynamics and Zed link each claim about the market or a founder's past work to the page that shows it ([Root, Privacy Dynamics](https://github.com/rootvc/investment-memos/blob/main/privacy_dynamics.md); [Root, Zed](https://github.com/rootvc/investment-memos/blob/main/zed.md)). Daily has a plain list of links under "Other reading" ([Root, Daily](https://github.com/rootvc/investment-memos/blob/main/daily.md)).
- **Calls as evidence.** 15 of 28 memos mention reference or customer calls. 8 have a section for them. ServiceTitan's opens: "We completed 8 customer calls and 5 calls with industry experts." ([Bessemer, ServiceTitan](https://www.bvp.com/memos/servicetitan)). Root's memos give each reference call its own subheading, named by role ([Root, Superconductive](https://github.com/rootvc/investment-memos/blob/main/superconductive.md), "Diligence Calls").
- **Appendices.** 6 of 28 memos put supporting tables in an appendix, such as PagerDuty's MRR expansion by cohort ([Bessemer, PagerDuty](https://www.bvp.com/memos/pagerduty)).
- **A source on every statement, in the newest template only.** Hustle Fund asks that every important statement carry a status (verified fact, founder claim or investor assumption), a source and an as-of date, and that evidence be linked rather than pasted: "The memo is the decision layer." ([Hustle Fund](https://www.hustlefund.vc/post/investment-memo-template)). Its worked example keeps a short evidence record in exactly that form. No published memo in this set does it line by line.

## Published memos that already do part of this (2:00 PM and 2:01 PM blocks)

The 2:00 PM block makes Tricorder's memo interactive: it reads top to bottom, and every line drills to its claims and every claim to its sources. The 2:01 PM block gives each reader their own copy and lets them tweak a few model assumptions. Here is what the published memos already do that points that way.

- **Jump to a section.** Bessemer's memo pages carry a "Jump to section" menu and a "Copy link to this section" button on every heading. The saved page shows both ([raw/memos/bvp_twilio.html](raw/memos/bvp_twilio.html), its `aria-label` attributes). This is navigation, not a drill to evidence.
- **Links from a claim to its source.** Root's memos are Markdown on GitHub, so every heading has an anchor and many claims link straight to the outside page behind them. This is one click from a claim to a source. It stops there: no memo links to a cell, a slide or a clause, and none shows which other sources agree or disagree.
- **A record of what changed.** Root's memos carry later notes in place, such as "Hindsight note: oversubscribed and blew past this target." ([Root, Privacy Dynamics](https://github.com/rootvc/investment-memos/blob/main/privacy_dynamics.md)). The Esper angel memo opens with the author's note from three years later ([Lee Edwards, Esper angel memo](https://github.com/ledwards/investment-memos/blob/main/esper.md)). Hustle Fund's template asks the writer to "Append material changes below the original memo" with the date, the new fact and its source, and the decision impact ([Hustle Fund](https://www.hustlefund.vc/post/investment-memo-template)). This is the closest published thing to a steer's visible diff.
- **Scenarios.** Bessemer's "Scenario Analysis" and "Outcomes Analysis" sections are fixed tables: a few exit values and the fund's return at each. The reader cannot change an input, and in 7 of the 11 memos with one the table is a picture. Hustle Fund asks for downside, base and upside cases with shared assumptions, and warns against false precision. No published memo lets a reader tweak churn, price or hiring and see the result.
- **Per-reader copies.** None. Every published memo is one document for every reader.

So the interactive memo and the reader's own scenarios are new. The pieces they build on (section links, source links, a change log, written scenarios) are each already in use somewhere.

## What this means for the template

- Keep the spine readers expect: summary and the ask first, risks near the end, the recommendation last. A partner opening Tricorder's memo should find it where a Bessemer or Hustle Fund memo puts it.
- Put Tricorder's top green and red flags inside the opening summary. 25 of 28 memos open with a summary, and the flags are the summary Tricorder can write from evidence.
- Write risks as a short labelled list, each with the evidence and what would settle it. That joins the Bessemer habit to Hustle Fund's structure, and it feeds the ask list.
- Give every statement a source and a status, as Hustle Fund asks, and make it clickable. The published memos show that this is the missing piece.
- Leave the recommendation and the judgement lines to the operator. In every memo here, a named partner signs them.

## Method and limits

- **Fetching.** Every page was fetched with `curl` or Python's `urllib` through [memo_fetch.py](memo_fetch.py). WebFetch was used only to search, never for text. Each saved file starts with a `SOURCE:` line. Headings were kept as Markdown `#` lines, bold as `**`, links as `[text](url)` and images as `[image]`. Root's memos were saved as their raw Markdown.
- **Labelling.** The canonical sections and the rules are in [memo_sections.py](memo_sections.py). A "Summary" heading in the last two places of a memo counts as the conclusion. The labels CSV has every heading, so any rule can be checked and changed, and the counts rerun.
- **Weighting.** 19 of the 28 memos are Bessemer's, so the counts lean toward Bessemer's habits. Root's seven seed memos are the main counterweight. The years run from 2005 to 2020 where a memo gives one, so the memos predate today's data rooms.
- **Edited copies.** Published memos are edited before release. Root says so on its front page. Treat them as the shape of a memo, not a full record of what the partners knew.
- **Not fetched.** Nothing from reddit.com. No LinkedIn pages.
