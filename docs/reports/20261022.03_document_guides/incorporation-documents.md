# Incorporation documents and bylaws

Written 2026-10-22 for the Tricorder document guides. Quotes are checked word for word against saved pages (see `quotes_equity.csv`). Vendor and law-firm views are marked.

**In one line:** these papers prove the company exists as the kind of company an investor can buy preferred stock in, and a reader checks that the name, the state, the share counts and the rules in them match the cap table and the financing papers.

## 1. What it is

The formation set for a company:

- The **certificate (or articles) of incorporation** as filed with the state, plus every amendment, or the restated version.
- The **bylaws**.
- The **first board action**: the incorporator's consent and the organizational consent of the initial directors, which appoint directors and officers, adopt the bylaws and approve the first stock issuance.
- **Founder stock purchase agreements** (with vesting) and **83(b) elections**.
- A **good standing certificate** from the state, and any foreign qualification where the company operates.

A startup lawyer or a formation service prepares them. They arrive as file-stamped PDFs. Holloway's angel investing guide, written by two lawyers, lists what a reviewer should see:

> "If you are reviewing the corporate documents for a startup, you should see at least the following documents:" ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))

Then it names the certificate, bylaws, organizational consent, incorporator consent, stock purchase agreements, founder IP assignments, the equity plan and copies of filed 83(b) elections. Cooley GO's request list asks for "The Company’s current Certificate of Incorporation/Articles of Incorporation, including any amendments thereto." ([Cooley GO list](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf))

## 2. At seed and at Series A

The data-room research marks it expected at pre-seed, seed and Series A ([research_data_room.md](../20261022.02_research/research_data_room.md), row 18). Kruze's checklist, a vendor view, expects the articles and the bylaws at every stage from pre-seed to Series C, and a state good standing certificate as No at pre-seed and seed, Maybe at Series A and B, and Yes at Series C ([Kruze](https://kruzeconsulting.com/blog/due-diligence-checklist/); [kruze_stage_rows.csv](raw/incorporation-documents/kruze_stage_rows.csv)). CRV, a fund, says a pre-seed room is rounded out by "Incorporation papers, a clean cap table and early proof points like customer interviews or a waitlist". ([CRV](https://www.crv.com/content/what-is-a-data-room))

- **At seed**, the certificate, bylaws and founder papers. Hustle Fund's pre-seed baseline is "Formation document, governing document, and relevant amendments." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **At Series A**, the set is longer. Each earlier priced round changed the charter, so every amendment should be in the room. Startups.com's glossary notes that "the charter must be amended at each round to authorize the new preferred class", so the Series A will bring another amendment ([Startups.com](https://www.launchrock.com/library/expert-advice/authorized-shares), a vendor). A good standing certificate and any foreign qualification are asked for more often.

## 3. What a first pass checks

In order:

1. What kind of entity is it, and in which state? A venture investor expects a Delaware C corporation.
2. Does the legal name match every other paper (cap table, SAFEs, contracts, deck)?
3. Is the certificate file-stamped, complete, and followed by every amendment?
4. Do the authorized shares cover what is issued, reserved for options, and owed on conversion?
5. Do the bylaws exist, and are they the current ones? What do they say about board size and written consent?
6. Is the company in good standing, and is the state's tax paid?
7. Do the founder stock purchase agreements and 83(b) elections exist?
8. Do the dates fit: incorporation first, then the first board action, then the first stock issuance?

## 4. Green flags

- **A lawyer-formed Delaware C corporation with the full set.** Holloway: "Most startups incorporate in Delaware as C corporations". The same guide warns "Beware of companies that are incorporated in places other than either Delaware or their home state." ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))
- **File-stamped copies, organized in a minute book.** Cooley GO's list of what a minute book holds starts with "A file-stamped copy of the certificate/articles of incorporation and all subsequent amendments as filed in the state of incorporation." ([Cooley GO](https://www.cooleygo.com/maintain-corporate-minute-book/))
- **Decision authority and equity set up before the money.** CRV on a company it backed: "Mercury's founding team formalized decision authority and equity structure before raising institutional capital." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **A clean room speeds the deal.** Cooley GO: "You will not be able to close a round of financing, sell your company or do an IPO if your corporate house is a mess." ([Cooley GO](https://www.cooleygo.com/cant-afford-disorganized)) The reverse is the green flag: a tidy set means no search for papers.
- **Headroom in authorized shares.** Startups.com says amending the charter for more shares takes board approval, stockholder approval and a state filing, so companies authorize "well above current issuance" ([Startups.com](https://www.launchrock.com/library/expert-advice/authorized-shares)). A table that sits well inside the authorized count shows planning.
- **Founder vesting and 83(b)s on file.** Holloway lists "copies of Section 83(b) elections the founders filed with the IRS, if the founders’ shares were subject to vesting" among the formation papers. ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))

## 5. Red flags and pitfalls

- **A founder-formed company that missed something (common).** Holloway: "It is not uncommon for founders to form companies themselves, without any legal assistance. In almost all situations this means the founders have missed something." The guide names late 83(b) elections, bylaws never adopted and stock purchase agreements never signed. ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))
- **A missed 83(b) election (common).** Burkland, a fractional CFO firm (vendor), calls it "A common misfire we see arise in diligence" and notes the filing window is 30 days after the grant, so it is too late by diligence. ([Burkland](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/)) Gust (vendor) says the same: "You have 30 days after the date of the stock grant to file it." ([Gust](https://gust.com/blog/missing-the-83b-deadline-can-spell-disaster-for-founders/))
- **An unusual state of incorporation (less common).** Holloway: "Beware of companies that are incorporated in places other than either Delaware or their home state." ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))
- **An LLC, S corporation or other entity that never converted (less common).** The terms.law conversion guide (a legal services site) says VCs will require a C-Corp before investing, so an LLC should convert before fundraising talks start. ([terms.law](https://terms.law/2025/11/14/llc-to-c-corp-conversion-guide/))
- **Not in good standing.** Holloway: "Make sure the company is in “good standing”" and the company "has not let its corporate charter lapse". ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments)) Delaware's franchise tax is due each March 1, and Rho (a banking vendor) says late payment brings a $200 penalty plus 1.5% interest a month ([Rho](https://www.rho.co/blog/delaware-franchise-tax)). Antone Johnson, a startup lawyer, wrote of "irate founders of new startups who received franchise tax bills from the State of Delaware for an insane amount like $75,000", which comes from the default authorized-shares method. ([Gust](https://gust.com/blog/heart-attack-tax-season-for-delaware-startups/)) Whether a late tax costs good standing is a lawyer's question.
- **More shares issued than the charter authorizes (rare but serious).** An overissue can make stock defective. A North Carolina Bar blog case study shows how one startup that issued stock before electing a board needed to find and ratify every defect in turn. ([NC Bar blog](https://www.ncbarblog.com/tips-for-using-new-statutory-ratification-procedure-to-cure-defects-in-authorizations-of-share-issuances-and-other-corporate-actions/)) In Delaware, a lawyer at Rutan & Tucker writes that attempts to ratify improperly issued shares used to fail, and that a Delaware statute amended "several years ago" (before the 2017 article) now allows a cure with steps that vary by defect. ([Rutan & Tucker](https://www.rutan.com/wp-content/uploads/2017/11/rutan-8.14.17.pdf)) The minutes guide covers the cure.
- **Control terms in the charter that are not standard (rare but serious).** Holloway warns of "any company that has an irregular voting, shareholder or proxy agreement that gives one individual near total authority over the affairs of a company", for example special voting classes. ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))
- **Names that do not match across papers.** A differences-in-reporting item: the legal name on the certificate differs from the name on the cap table, a SAFE or a customer contract.
- **Disorganized records.** Cooley GO says "disorganized companies tend to get labeled as having “hair” and are typically subjected to higher levels of due diligence scrutiny". ([Cooley GO](https://www.cooleygo.com/cant-afford-disorganized))

## 6. How Tricorder checks it

No FRAMEWORKS entry covers this document yet (the checklist marks it "not checked yet"). The checks below are proposals.

### What a script can check

- **`entity_name_consistency`** (proposed). Normalize each legal name (drop punctuation and the Inc./LLC suffix for comparison, keep the suffix as a separate field) and list every file where the name or suffix differs from the certificate.
- **`authorized_shares_cover`** (proposed). For each class: `headroom = authorized − (issued + reserved for options + shares owed on conversion)`. A negative headroom for an existing class is a flag. For the new Series A class the headroom will be negative before the closing amendment, which is normal; report it as "needs amendment", not as a flag.
- **`formation_date_order`** (proposed). Every stock issuance and board action is dated on or after the incorporation date, and each issuance is on or after the board action that approved it.
- **`class_names_match`** (proposed). Formula: `cap_table_classes ⊆ charter_classes`, after normalizing names. Preferred rows that come from SAFEs are excluded until conversion.
- **`good_standing_age`** (proposed, report only). Months between the certificate's date and the room's as-of date, from a date tool.
- **`file_present`** (proposed, the same pattern as FRAMEWORKS 1.11's `present(type)`). `present(type)` is true when the file list holds a file of that type: certificate, bylaws, organizational consent, stock purchase agreements, 83(b) copies.

### What needs a model to read

- The certificate: legal name, state, filing date, authorized shares by class and par value, preferred stock terms, and the list of amendments. The model must quote each.
- The bylaws: board size, quorum, written consent rule, officers, share transfer limits.
- The organizational consent: who the directors and officers are, what shares were issued to whom at what price.
- The stock purchase agreements: vesting terms and repurchase rights.
- A match of all of this to the cap table.

### What Tricorder cannot check and leaves to the operator

- Whether the filed charter matches the copy in the room. That needs a certified copy from the state or counsel.
- Good standing and tax status today. That is a state lookup that needs a fee or counsel.
- Whether a defect is curable, and how.
- Tax elections beyond the copies in the room, and whether an LLC conversion was done in a way that preserves the founders' tax position.

## 7. Which readout pieces it feeds

- **Legal and cap table.**

Checklist items ([CHECKLIST.md](../../ongoing/CHECKLIST.md)): incorporation documents and bylaws (the document itself); incorporation papers and minutes match the cap table and approve each financing; every instrument and grant on the cap table has a document.

## 8. If it is missing

- **Pre-seed, seed and Series A:** a gap at every stage, since the research and Kruze mark it expected at all three. The certificate is also a public filing, so the founder can supply it quickly. The label is `cannot_check`. It becomes a red flag only if the founder cannot say where the company is incorporated or declines to share. That is the operator's call. Hustle Fund: "Missing or irreconcilable basics such as formation records, the cap table, financing documents, and IP assignments can stall a close until the gaps are resolved." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

**Ask-list line:** "Please send the filed certificate of incorporation with every amendment, the current bylaws, the organizational board consent, the founders' stock purchase agreements and 83(b) elections, and a good standing certificate dated within the last few months."

## 9. In the Hollis Voice room

**Not in the room.** None of the 17 files is a certificate, bylaws, a consent or a good standing certificate. A scan of the room's text (`raw/_equity_tools/hv_terms_scan.py`) finds no hits for "Delaware", "incorporated", "bylaws", "certificate of incorporation" or "good standing". The state and form of the company are not stated anywhere in the room.

What the room does show: the legal name "Hollis Voice, Inc." appears the same way on the cover note, the cap table and all three customer agreements (`raw/_equity_tools/hv_entity_names.py`); the deck, overview, video script, model, bios and website copy say "Hollis Voice". That is consistent. The README places the company in Brooklyn and says it was founded in 2024, and the ledger shows "Legal and filing fees" to Pembry Legal Services from January 2025, so a lawyer holds the formation papers. No planted flag. At Series A this is a gap and an ask.

## 10. Sources

Each page is saved under [raw/incorporation-documents/](raw/incorporation-documents/).

- [Holloway, Legal due diligence for angel investments](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments), [saved](raw/incorporation-documents/holloway_com_g_angel_investing_sections_legal_due_diligence_for_angel_investments.txt). Two lawyers.
- [Cooley GO, Sample VC Due Diligence Request List (PDF)](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf), [saved](raw/incorporation-documents/cooleygo_com_wp_content_uploads_2014_07_Cooley_GO_Tip_Sheet_Sample_VC_Due_Diligence_Request_List_pdf.txt). Law firm.
- [Cooley GO, Why (and how) do you maintain a corporate minute book](https://www.cooleygo.com/maintain-corporate-minute-book/), [saved](raw/incorporation-documents/cooleygo_com_maintain_corporate_minute_book.txt). Law firm.
- [Cooley GO, Why you can't afford to be disorganized](https://www.cooleygo.com/cant-afford-disorganized), [saved](raw/incorporation-documents/cooleygo_com_cant_afford_disorganized.txt). Law firm.
- [CRV, What is a data room](https://www.crv.com/content/what-is-a-data-room), [saved](raw/incorporation-documents/crv_com_content_what_is_a_data_room.txt). Fund view.
- [Hustle Fund, Angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [saved](raw/incorporation-documents/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt). Fund view.
- [Kruze, VC due diligence checklist](https://kruzeconsulting.com/blog/due-diligence-checklist/), [saved](raw/incorporation-documents/kruzeconsulting_com_blog_due_diligence_checklist.txt) and [stage rows](raw/incorporation-documents/kruze_stage_rows.csv). Vendor.
- [Burkland Associates, Surviving due diligence part 3](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/), [saved](raw/incorporation-documents/burklandassociates_com_2021_11_02_surviving_due_diligence_part_3_cap_tables.txt). Vendor.
- [Gust, Heart-attack tax season for Delaware startups](https://gust.com/blog/heart-attack-tax-season-for-delaware-startups/), [saved](raw/incorporation-documents/gust_com_blog_heart_attack_tax_season_for_delaware_startups.txt). Startup lawyer (2012), Gust is a vendor.
- [Rho, Delaware franchise tax](https://www.rho.co/blog/delaware-franchise-tax), [saved](raw/incorporation-documents/rho_co_blog_delaware_franchise_tax.txt). Banking vendor.
- [Gust, Missing the 83(b) deadline can spell disaster for founders](https://gust.com/blog/missing-the-83b-deadline-can-spell-disaster-for-founders/), [saved](raw/incorporation-documents/gust_com_blog_missing_the_83b_deadline_can_spell_disaster_for_founders.txt). Vendor.
- [Startups.com, Authorized shares](https://www.launchrock.com/library/expert-advice/authorized-shares), [saved](raw/incorporation-documents/launchrock_com_library_expert_advice_authorized_shares.txt). Vendor.
- [terms.law, LLC to C-Corp conversion guide](https://terms.law/2025/11/14/llc-to-c-corp-conversion-guide/), [saved](raw/incorporation-documents/terms_law_2025_11_14_llc_to_c_corp_conversion_guide.txt). Legal services site.
- [NC Bar blog, Tips for using the new statutory ratification procedure](https://www.ncbarblog.com/tips-for-using-new-statutory-ratification-procedure-to-cure-defects-in-authorizations-of-share-issuances-and-other-corporate-actions/), [saved](raw/incorporation-documents/ncbarblog_com_tips_for_using_new_statutory_ratification_procedure_to_cure_defects_in_authorizations_.txt). Law blog.
- [Rutan & Tucker, Fixing the unfixable cap table (Orange County Business Journal, 2017)](https://www.rutan.com/wp-content/uploads/2017/11/rutan-8.14.17.pdf), [saved](raw/incorporation-documents/rutan_com_wp_content_uploads_2017_11_rutan_8_14_17_pdf.txt). Law firm.

Pages I could not fetch: Delaware's Division of Corporations pages and DLA Piper's franchise tax article (HTTP 429, rate limited).

Reddit: no thread URLs surfaced in search, so there is no `.json` list.
