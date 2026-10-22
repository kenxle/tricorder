# One-page summary

**In one line:** the one-pager is the page a partner forwards. It must say the same thing as the deck, and Tricorder checks that it does.

Written 2026-10-22 for the Tricorder document guides (group: story). Every quote below was checked word for word against the saved page by `raw/_verify_story/verify_quotes_story.py`; the rows are in `quotes_story.csv`. Vendor and educator views are marked.

## 1. What it is

A one-page (sometimes two-page) fact sheet that sums up the company: what it does, the team, traction, market, the ask and what was raised before. Investors call it the executive summary or the one-pager. The CEO writes it. It arrives as a PDF.

It is built to be passed on. Visible, a vendor of investor-update software, says: "the one-pager is what gets forwarded internally to partners who haven't opened the deck yet." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)) YC says to bring one so investors can pass it around: "You will probably want an executive summary and a slide deck you can walk investors through and, potentially, leave behind so VCs can show to other partners." ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/)) The Capital Network, a nonprofit that connects angels and founders, says the same about use: "It is a piece of “collateral” that an investor can use to discuss your company with other investors" ([The Capital Network](https://www.thecapitalnetwork.org/2017/04/10/one-page-matters)).

## 2. At seed and at Series A

It is expected at both stages and at pre-seed. Visible's checklist includes it at every stage (vendor view, [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)).

- **Seed:** YC sets the content and the length. "The executive summary should be one or two pages (one is better) and should include vision, product, team (location, contact info), traction, market size, and minimum financials (revenue, if any, and fundraising prior and current)." ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/)) The law firm Wilson Sonsini says its purpose is to win the next step: "Your one-page executive summary is a standardized document whose purpose is to get an investor to agree to meet with you, or at least to review your pitch deck." ([Wilson Sonsini](https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf))
- **Series A:** the same page, with proof in place of promise. Angel Investors Network (an educator that sells marketing services, so a weaker source) writes: "Series A : Product-market fit evidence dominates." and lists revenue growth rates, retention metrics and customer acquisition cost ([Angel Investors Network, educator view](https://angelinvestorsnetwork.com/startups/executive-summary-template-startup-funding-the-first-page-vcs-actually-read)).
- **What changes for Tricorder:** more of the page's numbers have a file behind them at Series A, so a one-pager number with no second source is a bigger gap there.

## 3. What a first pass checks

1. Does it fit on one page, and does the first half stand alone? "If an investor stops reading after page one, they should still understand the opportunity." ([Angel Investors Network, educator view](https://angelinvestorsnetwork.com/startups/executive-summary-template-startup-funding-the-first-page-vcs-actually-read))
2. What stage, ask and traction does it state?
3. Does every number match the deck? Visible: "the deck and the executive summary need to agree before you upload anything else." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))
4. Does it state any number the deck does not (a new claim with no slide)?
5. Is it dated, and is the date the same as the deck's?
6. Does it show what was raised before, the terms, and the current ask?
7. Does it carry the basics YC lists: location, contact, market size?
8. Does it name competition? Wilson Sonsini's list includes "Your competition (and don’t say that there isn’t any!)" ([Wilson Sonsini](https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf))

## 4. Green flags

- **It agrees with the deck, line by line** (Visible quote above). Two files that say the same thing is the corroboration Tricorder counts, though the readout notes that the deck and the one-pager come from one author, so they count as one source.
- **It stands alone and is easy to forward.** Both the YC and Capital Network quotes above describe the use. "One page wins. Two pages acceptable. Three pages unread." ([Angel Investors Network, educator view](https://angelinvestorsnetwork.com/startups/executive-summary-template-startup-funding-the-first-page-vcs-actually-read))
- **It carries the hard facts YC lists:** location, contact, prior raise, minimum financials.
- **Dated numbers.** A figure with an as-of date is easier to test than one without. This is my inference; no source states it.

## 5. Red flags and pitfalls

Common:

- **Numbers that differ from the deck.** Visible calls internal contradictions "the most common credibility hit at the opening of diligence." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)) The one-pager is where a figure is most often left at an older value after the deck is updated (my inference).
- **A sloppy or crowded page.** The Capital Network: "a sloppy or bad executive summary is a big red flag." ([The Capital Network](https://www.thecapitalnetwork.org/2017/04/10/one-page-matters)) Tricorder cannot judge design; it can count pages and words.
- **Vague market sizing.** Angel Investors Network lists "Vague market sizing." among the usual mistakes. ([educator view](https://angelinvestorsnetwork.com/startups/executive-summary-template-startup-funding-the-first-page-vcs-actually-read))
- **Projections copied from a template.** Same source: "Financial projections that match SaaS templates exactly (40% annual growth, 85% gross margins, 24-month payback)".
- **Claiming no competition** (Wilson Sonsini, above).

Rare but serious:

- **A headline number that is a different kind of number from the deck's.** For example, run rate shown as ARR, or a pilot counted in revenue. The one-pager is short, so the label carries all the weight and the definition is missing. Tricorder's accounting-mislabel checks (FRAMEWORKS 1.2 and 1.12) read the number's underlying file, not the label.

## 6. How Tricorder checks it

**What a script can check**

- `Deck claim extraction` (FRAMEWORKS 1.1) lists the one-pager among the files whose numbers it reads, and `deck_claim_vs_named_cell` (1.5) pairs each one-pager number with the deck, the model and the metrics export. Both run on the one-pager after Saturday.
- Proposed `new_claims_not_in_deck`: build the set of (label, period) pairs from the one-pager and from the deck's claims; list the pairs that are only on the one-pager. Each is a claim with no slide behind it.
- Proposed `page_and_word_count`: pages (one or two) and words. A one-pager over two pages or over a word limit is noted, not scored.
- Proposed `as_of_match`: the one-pager's date against the deck's.

**What needs a model to read**

- Pull each number with its quote and page. The script re-parses it.
- Match labels between the one-pager and the deck.
- Read non-numeric claims (customers named, awards, "profitable") and mark which have no file behind them.

**What Tricorder cannot check (leave to the operator)**

- Whether this is the version the founder sent others.
- Whether the page is well designed or well written.
- Whether a named customer or award is real; a reference call or a web search settles it.

## 7. Which readout pieces it feeds

- **The pitch itself:** checklist item "One-page summary" (id C61), and "Deck numbers match the model and the metrics export" (C65).
- **Every business piece**, by each claim's label, because the one-pager repeats the headline numbers. Agreement between deck and one-pager is not independent: both come from the company.

## 8. If it is missing

- **Seed:** a gap, not a flag. Many founders send only a deck. Tricorder's own readout is a one-page summary of the company, so the cost is small.
- **Series A:** still a gap. A room with a deck but no summary is less friendly to a partner who forwards, but the numbers are in the deck.
- **Ask-list line:** "Please send the one-page summary you give investors, with its date."

## 9. In the Hollis Voice room

The room holds `01_overview/company_overview.pdf` (one page) in the full room and the seed drop.

- It repeats the deck's headline numbers: ARR $2,500,000, 357 clinics, 80% gross margin, 102.6% net revenue retention, largest customer under 9% of ARR, and 72,149 calls in September 2026. Five of those sit under planted flags: ARR (PF2, deck ARR above the model), clinics (PF7, cumulative sign-ups shown as clinics), gross margin (PF6), retention (PF3) and largest customer (PF5). The 37 months of runway in the ask line sits under PF4. The answer key lists the overview as a location for PF2 and PF7 and says it repeats the deck's planted claims without adding new ones.
- It states the ask ($9,000,000 at $45,000,000 pre-money), 24 hires, 37 months of runway (PF4), and earlier funding: $5,500,000 in SAFEs, $2,000,000 on a $12,000,000 post-money cap and $3,500,000 on a $28,000,000 cap. The SAFE total agrees with the cap table and the model. It gives the founders, a headcount of 17, an as-of date of 2026-09-30 and an email address.
- It has no market size and no competition line, which both the YC list and the Wilson Sonsini list include. These are gaps in a synthetic page, not planted.
- The 17-person headcount and the SAFE total are green flags: the overview, the deck, the model and the cap table agree on them.

## 10. Sources

Each page is saved under `raw/one-page-summary/`.

- YC, "How to raise a seed round": https://www.ycombinator.com/blog/how-to-raise-a-seed-round/ , `ycombinator_com_blog_how_to_raise_a_seed_round.txt`
- Wilson Sonsini, "Pitching to US VCs": https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf , `wsgr_com_images_content_2_6_26592_Pitching_to_US_VCs_pdf.txt`
- The Capital Network, "One page that matters": https://www.thecapitalnetwork.org/2017/04/10/one-page-matters , `thecapitalnetwork_org_2017_04_10_one_page_matters.txt`
- Visible (vendor view): https://visible.vc/blog/what-to-include-in-your-data-room/ , `visible_vc_blog_what_to_include_in_your_data_room.txt`
- Angel Investors Network (educator view): https://angelinvestorsnetwork.com/startups/executive-summary-template-startup-funding-the-first-page-vcs-actually-read , `angelinvestorsnetwork_com_startups_executive_summary_template_startup_funding_the_first_page_vcs_act.txt`
- Saved and read, not quoted: DocSend (vendor) on executive summaries https://www.docsend.com/blog/startup-executive-summary/ ; SETsquared guidelines (UK) https://www.setsquared.co.uk/wp-content/uploads/2022/10/SETsquared@20-Executive-Summary-Guidelines-2022.pdf ; Vestbee (a VC database vendor) https://vestbee.com/blog/articles/startup-fundraising-how-to-craft-startup-one-pager-for-investors ; Launchrock https://www.launchrock.com/library/expert-advice/one-pager
- I found no VC's own post on what they want in a forwarded summary, only advisers and vendors. The strongest sources here are YC (an accelerator and its own guide) and a law firm.
