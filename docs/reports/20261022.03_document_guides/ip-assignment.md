# IP and invention assignment agreements

Written 2026-10-22 for the Tricorder document guides. Quotes are checked word for word against saved pages (see `quotes_equity.csv`). Vendor and law-firm views are marked.

**In one line:** these are the signed papers that make the company, and not the people who wrote the code, the owner of its technology, and the reader checks that every founder, employee and contractor signed one, and that nobody else holds a claim.

## 1. What it is

An invention assignment agreement is the paper by which a person transfers to the company what they create for it. The common names are Proprietary Information and Inventions Assignment Agreement (PIIA) and Confidential Information and Inventions Assignment Agreement (CIIAA). Cooley GO, a law firm, describes the employee version this way: it assigns IP an employee creates on the job to the employer and carves out IP the person created before the job. It often adds nondisclosure and nonsolicitation terms, and noncompetition clauses are unenforceable in some states such as California ([Cooley GO glossary](https://www.cooleygo.com/glossary/confidential-information-and-inventions-assignment-agreements/)).

Three groups sign:

- **Founders**, at formation, assigning their work including anything built before the company existed.
- **Employees**, on or before the first day.
- **Contractors, agencies and advisors**, in a stand-alone agreement or in a clause of the contractor agreement.

A startup lawyer supplies the forms. The signed copies arrive as PDFs, often with a list of who signed.

## 2. At seed and at Series A

The data-room research marks it L, Y, Y for pre-seed, seed and Series A: lighter at pre-seed, included at seed and Series A ([research_data_room.md](../20261022.02_research/research_data_room.md), row 20). Kruze's checklist, a vendor view, asks for signed invention agreements from employees, founders and consultants since inception (Maybe at pre-seed and seed, Yes from Series A), and for a list of people who have not signed (No at pre-seed, Maybe at seed, Yes from Series A) ([Kruze](https://kruzeconsulting.com/blog/due-diligence-checklist/); [kruze_stage_rows.csv](raw/ip-assignment/kruze_stage_rows.csv)). Hustle Fund, a fund, puts it in the pre-seed baseline: "IP, confidentiality, and invention-assignment agreements for founders and material contributors." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

CRV, a fund, puts it on the deal team's first-pass list:

> "the cap table, the financial model, the articles of incorporation and the intellectual property (IP) assignment agreements" ([CRV](https://www.crv.com/content/what-is-a-data-room))

- **At seed**, the founders' assignments and the agreements for the engineers and contractors who built the product.
- **At Series A**, everyone who has contributed since the start, with the list of who has not signed. OneGC, a legal services vendor, says why: every priced-round term sheet includes a representation that the company owns or has valid licenses to the IP it uses, and the company either cannot make it or creates a liability if it does and is wrong. ([OneGC](https://onegc.com/blog/ip-assignment-for-startups))

## 3. What a first pass checks

In order:

1. Did each founder sign an assignment that covers work done before incorporation?
2. Did every employee sign on or before their start date?
3. Does every contractor and agency have an assignment in writing?
4. Who has not signed? Is there a list?
5. What do the words say? A present assignment ("hereby assigns") is different from a promise to assign later.
6. What does the carve-out list exclude, and does it touch the core product?
7. Does anyone else hold a claim: a founder's former employer, a university, a departed co-founder?
8. What third-party and open source code is in the product, and under what licenses?

## 4. Green flags

- **Assignments signed at formation and on the first day.** Koley Jessen, a law firm: "At the company formation stage, all founders should assign their relevant IP to the new company." ([Koley Jessen](https://www.koleyjessen.com/insights/publications/mother-knows-best-all-startups-need-to-have-a-clean-room))
- **Every contributor, including contractors and advisors, covered.** Hustle Fund lists the check as "IP, confidentiality, and invention-assignment agreements for founders and material contributors". ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **A signer list that matches the team.** Cooley GO's request list asks for a list of non-signers, "including a list any periods of time where key employees or consultants performed services for the Company while not bound by such agreements". A company that already has this list is ahead. ([Cooley GO list](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf))
- **Retroactive assignments already collected.** OneGC: "Former contractors have less incentive to cooperate once the relationship is over, and some will ask for additional compensation to sign." Having them in hand early is the point. ([OneGC](https://onegc.com/blog/ip-assignment-for-startups))
- **A clean start for the founders' time.** Goodwin partner William Wilson, writing in TechCrunch: "Investors are particularly concerned about startups having exclusive ownership of their intellectual property." A founder who started after leaving the old job, and documented it, answers the concern. ([TechCrunch](https://techcrunch.com/2022/04/22/10-ip-and-commercial-contract-loose-ends-to-tie-up-before-you-approach-investors))
- **An open source inventory.** The same article says "Investors will often request a list of open source software used". ([TechCrunch](https://techcrunch.com/2022/04/22/10-ip-and-commercial-contract-loose-ends-to-tie-up-before-you-approach-investors))
- **Short prior-inventions lists.** Cooley GO asks for the agreements "that contain any exclusions from assignment to the Company", so a clean one has none that touch the product. ([Cooley GO list](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf))

## 5. Red flags and pitfalls

- **A contractor who wrote core code and never signed (common).** Cooley GO names it as the typical deal killer: "the contractor who wrote your code and never signed an IP assignment". ([Cooley GO](https://www.cooleygo.com/cant-afford-disorganized)) CRV: "Missing IP assignments from engineers and contractors are one of the more common legal gaps in technology-company diligence." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **Payment is not assignment (common).** CRV: "Paying for development work does not, by itself, create the written chain of title an investor wants." ([CRV](https://www.crv.com/content/what-is-a-data-room)) OneGC: "A purchase order is not an assignment." ([OneGC](https://onegc.com/blog/ip-assignment-for-startups))
- **Work built before incorporation (common).** OneGC: "The act of incorporation does not transfer ownership of pre-existing work." It calls this the most common gap, and says of the holes in general: "These are not edge cases. They are the default state of most startups before Series A." ([OneGC](https://onegc.com/blog/ip-assignment-for-startups))
- **An offer letter that points to an agreement nobody signed (common).** OneGC: "The clause in the offer letter is a promise to sign a future agreement, not an assignment itself." ([OneGC](https://onegc.com/blog/ip-assignment-for-startups))
- **A departed co-founder or early contractor who never assigned (rare but serious).** CRV: "The gap often traces to a departed co-founder or early contractor". Koley Jessen: a founder who leaves "may have leverage" if they later learn critical IP was never assigned, and that person may sue. ([CRV](https://www.crv.com/content/what-is-a-data-room); [Koley Jessen](https://www.koleyjessen.com/insights/publications/mother-knows-best-all-startups-need-to-have-a-clean-room))
- **The cost is paid in cash and equity.** Weintraub, a law firm, describes a Series Seed where "the lead investor’s counsel asked for proof that the company owned all of its source code. It didn’t." The developer's agreement had never been signed; "The investor froze the round until the issue was resolved." The developer demanded payment and equity before signing, and the founders lost months and part of their cap table. ([Weintraub](https://www.weintraub.com/2026/01/who-really-owns-your-startups-ip/))
- **Someone else's claim: a founder's former employer (less common, serious).** Wilson: "This exclusive ownership often faces risks when a founder moonlights on their new startup while still employed by another company, especially if the former employer offers a competing product or service." ([TechCrunch](https://techcrunch.com/2022/04/22/10-ip-and-commercial-contract-loose-ends-to-tie-up-before-you-approach-investors)) Koley Jessen adds that IP claims "typically don’t manifest until the company has had some measure of success". ([Koley Jessen](https://www.koleyjessen.com/insights/publications/mother-knows-best-all-startups-need-to-have-a-clean-room))
- **Confidentiality is not assignment.** Hustle Fund: "Confidentiality obligations alone do not transfer IP ownership." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **Wording and state carve-outs.** A typical clause reads "agree to assign and hereby do irrevocably assign" ([startupcompanylawyer.com](https://www.startupcompanylawyer.com/2009/01/08/what-do-you-need-to-do-before-you-quit-your-job-to-form-a-startup-company/)), a present transfer. OneGC says California Labor Code Section 2870 limits what an employer may require, and an agreement that ignores state carve-outs may be partly unenforceable.
- **Former employees.** Holloway, written by two lawyers, tells the investor to ask: "Did the ex-employees sign IP assignment agreements and NDAs?" ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))

## 6. How Tricorder checks it

### What a script can check

- **`present(type)`** (exists, [FRAMEWORKS 1.11](../../ongoing/FRAMEWORKS.md)). Does the file list hold an IP assignment agreement? When none is present, the entry returns an ask. The checklist notes that signatures are not read.
- **`ip_assignment_coverage`** (proposed). Formula: `coverage = contributors with a signed agreement ÷ all contributors`. Contributors are the founders in the bios, employees in the team files and payroll lines, option holders, and contractors and agencies found in the expense ledger. Signers are read from the signature blocks. List every contributor with no match.
- **`assignment_date_vs_start`** (proposed). `signature_date ≤ start_date`, per person, with start dates from the hiring plan and the option grant dates.
- **`repo_history_vs_incorporation`** (proposed, outside world). Formula: `gap_days = incorporation_date − earliest_public_commit_date`, for the founders' and the company's GitHub accounts (GitHub is an approved source for the founder scan). If `gap_days > 0`, work predates the company, so ask for the founder assignment that covers it.
- **`open_source_license_scan`** (proposed). For public repositories, read the dependency manifests and list `licenses ∩ {GPL, AGPL, LGPL}`. OneGC names GPL, AGPL and LGPL as the ones that can force proprietary code open. ([OneGC](https://onegc.com/blog/ip-assignment-for-startups))

### What needs a model to read

- Each agreement: the parties, the effective date, the operative words (a present assignment or a promise to assign), the scope, any prior-inventions exhibit and any state carve-out language, and whether it is signed. The model must quote each.
- The founders' bios against the product, looking for a former employer in the same field. The model raises it as a question, with the bio line quoted.
- Third-party license agreements in the room (the Cooley list asks for them).

### What Tricorder cannot check and leaves to the operator

- Whether a person who has not signed will sign.
- What the founders' former employment agreements say and whether the former employer has a claim.
- Whether code was copied. A technical review, or a clean-room record.
- A patent or trademark search.
- The legal opinion on the wording. A lawyer reads it.

## 7. Which readout pieces it feeds

- **Legal and cap table.**
- The founder and employer overlap also feeds **team** as a question, not a verdict.
- The repo history check belongs to the **outside world** piece.

Checklist items ([CHECKLIST.md](../../ongoing/CHECKLIST.md)): IP and invention assignment agreements (the document); every founder and contractor signed an IP assignment; patents, trademarks, copyrights and domain names.

## 8. If it is missing

- **Pre-seed:** lighter. A gap, with an ask for the founders' assignments.
- **Seed:** a gap and an ask. CRV puts it on the first-pass list, so it is among the first things a reader looks for.
- **Series A:** a gap, and a likely red flag if the company has engineers or contractors and no agreements at all. The call on how serious is the operator's. The label is `cannot_check` with one ask per missing item (FRAMEWORKS 1.11).

**Ask-list line:** "Please send the signed invention assignment agreements for each founder (covering any work before incorporation), each employee and each contractor who has written code, designs or content, and a list of anyone who has not signed."

## 9. In the Hollis Voice room

**Not in the room.** FRAMEWORKS 1.11's worked example already records that the 17 files hold "no IP assignments". A scan of the room's text finds no hits for "assignment" or "invention" (`raw/_equity_tools/hv_terms_scan.py`). No planted flag. At seed and Series A this is a gap and an ask.

What the room does show that a reader would raise as questions (observations, not planted flags):

- The CTO "spent eleven years building speech and telephony systems at Kestrel Telecom Software", and Hollis Voice sells a phone agent. A first pass would ask when he left, what his employment agreement said about inventions, and whether any work on the product started before he left. The lead voice engineer built call-routing systems at a regional telephone carrier (founder bios).
- The expense ledger has 21 monthly lines each to Marsh Speech Licensing ("Speech recognition and voice licences") and Halcyon Inference API ("Language model and speech API usage"). These are third-party technology, so the Cooley list's request for licenses applies.
- The ledger shows no software development contractor or agency among its 13 vendors, which narrows the contractor question to individuals on payroll. Payroll lines go through Ironbridge Payroll Services.

## 10. Sources

Each page is saved under [raw/ip-assignment/](raw/ip-assignment/).

- [CRV, What is a data room](https://www.crv.com/content/what-is-a-data-room), [saved](raw/ip-assignment/crv_com_content_what_is_a_data_room.txt). Fund view.
- [Hustle Fund, Angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [saved](raw/ip-assignment/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt). Fund view.
- [Cooley GO, Sample VC Due Diligence Request List (PDF)](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf), [saved](raw/ip-assignment/cooleygo_com_wp_content_uploads_2014_07_Cooley_GO_Tip_Sheet_Sample_VC_Due_Diligence_Request_List_pdf.txt). Law firm.
- [Cooley GO, Why you can't afford to be disorganized](https://www.cooleygo.com/cant-afford-disorganized), [saved](raw/ip-assignment/cooleygo_com_cant_afford_disorganized.txt). Law firm.
- [Cooley GO glossary, CIIAA](https://www.cooleygo.com/glossary/confidential-information-and-inventions-assignment-agreements/), [saved](raw/ip-assignment/cooleygo_com_glossary_confidential_information_and_inventions_assignment_agreements.txt). Law firm.
- [Koley Jessen, All startups need to have a clean room (2024)](https://www.koleyjessen.com/insights/publications/mother-knows-best-all-startups-need-to-have-a-clean-room), [saved](raw/ip-assignment/koleyjessen_com_insights_publications_mother_knows_best_all_startups_need_to_have_a_clean_room.txt). Law firm.
- [TechCrunch, 10 IP and commercial contract loose ends (William Wilson, Goodwin, 2022)](https://techcrunch.com/2022/04/22/10-ip-and-commercial-contract-loose-ends-to-tie-up-before-you-approach-investors), [saved](raw/ip-assignment/techcrunch_com_2022_04_22_10_ip_and_commercial_contract_loose_ends_to_tie_up_before_you_approach_inv.txt). Law firm partner.
- [Weintraub, Who really owns your startup's IP (2026)](https://www.weintraub.com/2026/01/who-really-owns-your-startups-ip/), [saved](raw/ip-assignment/weintraub_com_2026_01_who_really_owns_your_startups_ip.txt). Law firm.
- [OneGC, IP assignment for startups](https://onegc.com/blog/ip-assignment-for-startups), [saved](raw/ip-assignment/onegc_com_blog_ip_assignment_for_startups.txt). Legal services vendor.
- [Holloway, Legal due diligence for angel investments](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments), [saved](raw/ip-assignment/holloway_com_g_angel_investing_sections_legal_due_diligence_for_angel_investments.txt). Two lawyers.
- [Kruze, VC due diligence checklist](https://kruzeconsulting.com/blog/due-diligence-checklist/), [saved](raw/ip-assignment/kruzeconsulting_com_blog_due_diligence_checklist.txt) and [stage rows](raw/ip-assignment/kruze_stage_rows.csv). Vendor.
- [startupcompanylawyer.com, What to do before you quit your job to form a startup](https://www.startupcompanylawyer.com/2009/01/08/what-do-you-need-to-do-before-you-quit-your-job-to-form-a-startup-company/), [saved](raw/ip-assignment/startupcompanylawyer_com_2009_01_08_what_do_you_need_to_do_before_you_quit_your_job_to_form_a_startu.txt). Startup lawyer's site.

Pages I could not fetch: DLA Piper's trade secrets article (HTTP 429, rate limited).

Reddit: no thread URLs surfaced in search, so there is no `.json` list.
