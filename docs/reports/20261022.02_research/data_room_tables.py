"""Tables and counts for research_data_room.md (R4).

One place holds the rows that the report prints: the data room document table (Part 1),
the red-flag catalog (Part 2), the planted flags and decoys (Part 3) and the file list (Part 3).
Every count in the report comes from this script's output.

Run: python3 -I data_room_tables.py
Writes: data_room_documents.csv, data_room_flags.csv, data_room_planted.csv, data_room_files.csv
Prints: counts, then the markdown tables the report embeds (use --tables to print them).
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = json.load(open(os.path.join(HERE, "data_room_design_numbers.json")))


def money(x):
    return "${:,.0f}".format(x)


def pct(x, d=1):
    return f"{x * 100:.{d}f}%"


# Source links. Each page was fetched and saved under raw/data_room/.
U = {
    "V": ("Visible", "https://visible.vc/blog/what-to-include-in-your-data-room/"),
    "CRV": ("CRV", "https://www.crv.com/content/what-is-a-data-room"),
    "BCV": ("BCV", "https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/"),
    "a16z": ("a16z", "https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/"),
    "Cooley": ("Cooley", "https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/"),
    "Kruze": ("Kruze", "https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/"),
    "Hustle": ("Hustle", "https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step"),
    "YC": ("YC", "https://www.ycombinator.com/blog/how-to-raise-a-seed-round/"),
    "PeonyA": ("Peony A", "https://www.peony.ink/blog/series-a-data-room"),
    "PM": ("Papermark", "https://www.papermark.com/blog/data-room-for-yc-startups"),
    "FR": ("First Round", "https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/"),
    "Ellty": ("Ellty", "https://www.ellty.com/blog/how-investors-review-a-data-room"),
    "SL": ("SeedLegals", "https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round"),
    "DS": ("DocSend", "https://www.docsend.com/blog/virtual-data-room-for-startups/"),
    "NFX": ("NFX", "https://www.nfx.com/post/the-non-obvious-guide-to-fundraising"),
    "Stealth": ("SaaStr stealth churn", "https://www.saastr.com/stealth-ai-churn-are-your-customers-starting-to-leave-already/"),
    "Carta": ("Carta", "https://support.carta.com/kb/guide/en/how-to-manage-vc-fundraising-data-rooms-MHvOEzfZwJ/Steps/3724875"),
    "Tracks": ("Deal Flow problem tracks", "https://docs.google.com/document/d/1S0ytTC-k1zLTvcoUjkRJy0JYuaNgYOWW9EQ04xN8SDA/edit"),
    "KruzeCash": ("Kruze cash forecast", "https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/"),
    "A16Z16": ("a16z 16 metrics", "https://a16z.com/16-startup-metrics/"),
    "A16Z16b": ("a16z 16 more", "https://a16z.com/16-more-startup-metrics/"),
    "BVP": ("Bessemer", "https://www.bvp.com/atlas/scaling-to-100-million"),
    "Tunguz": ("Tunguz", "https://tomtunguz.com/not-all-revenue-dollars-are-created-equal/"),
    "SaaStrTop": ("SaaStr top 10", "https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/"),
    "SaaStrGRR": ("SaaStr GRR", "https://www.saastr.com/dear-saastr-were-at-13m-arr-and-growing-but-our-grr-is-slipping-what-should-we-do/"),
    "Fortune": ("Fortune", "https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/"),
    "Lighter": ("Lighter MRR", "https://www.lightercapital.com/blog/four-metrics-to-track-when-raising-capital-for-your-saas-company"),
    "LighterC": ("Lighter CMRR", "https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr"),
    "Janz": ("Janz on Chen", "https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/"),
    "Micro": ("MicroVentures", "https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many"),
    "Stripe": ("Stripe", "https://stripe.com/en-se/resources/more/saas-gross-margin-explained-what-it-is-and-why-it-is-important"),
}


def link(*keys):
    return ", ".join(f"[{U[k][0]}]({U[k][1]})" for k in keys)


# ---------------------------------------------------------------- Part 1
# (document, pre-seed, seed, series A, who asks, what a first-pass reader does, basis, source keys)
# Stage letters: Y put it in, L lighter version or only if you have it, N leave out, - sources do not say.
# A trailing * means the letters come from a source other than Visible's table.
DOCS = [
    ("Cover note and document index", "Y", "Y", "Y", "The founder volunteers it; investors reward it", "Uses the index to find the cap table and model in seconds", "sourced", ["V", "Ellty"]),
    ("Pitch deck", "Y", "Y", "Y", "Every investor; a16z lists it first", "Treats each number as a claim and looks for the file that proves it", "sourced", ["a16z", "PeonyA", "V"]),
    ("One-page summary", "Y", "Y", "Y", "Every investor; YC says one or two pages is enough at seed", "Reads stage, ask and traction", "sourced", ["YC", "V"]),
    ("Founder video or recorded intro", "L", "L", "L", "Partner, optional", "Hears the founder state the numbers in their own voice (our use: compare with the deck)", "sourced + inferred", ["V"]),
    ("Cap table, fully diluted", "Y", "Y", "Y", "Deal team and investor counsel; a16z lists it right after the deck; first on CRV's first-pass list", "Checks that holders add to 100 percent, SAFEs are converted, and the option pool is shown", "sourced", ["a16z", "CRV", "PeonyA"]),
    ("Financial model, 3 to 5 years", "Y", "Y", "Y", "Deal team; a16z says detailed projections can wait for consumer seed; NFX says 24 months monthly plus 3 years annual", "Reads it against the deck; at Series A an associate rebuilds it", "sourced", ["V", "CRV", "PeonyA", "a16z", "NFX"]),
    ("Historical P&L, balance sheet, cash flow (monthly)", "L", "Y", "Y", "Deal team; Kruze lists three years of statements", "Reads revenue lines, cost of revenue lines, payroll, and computes burn", "sourced", ["a16z", "Kruze", "V"]),
    ("Audited or reviewed financials", "N", "N", "L", "Series A lead, accountants", "Compares reviewed numbers with management numbers", "sourced", ["V"]),
    ("KPI dashboard or metrics export (MRR, ARR, customers, churn)", "L", "Y", "Y", "Deal team", "Compares each headline number with the deck and the definition used", "sourced", ["V", "Hustle"]),
    ("Monthly revenue by customer", "-", "L*", "Y*", "BCV names it as one of two key items; Hustle and First Round also ask", "Builds customer cohorts and concentration, and sets them against sales and marketing spend", "sourced", ["BCV", "Hustle", "FR"]),
    ("Cohort or retention export", "N", "L", "Y", "Deal team; CRV lists cohort retention curves as proof", "Rebuilds retention from raw data and checks the retention claim in the deck", "sourced", ["V", "CRV", "PeonyA"]),
    ("Unit economics (CAC, LTV, payback)", "N", "L", "Y", "Deal team; a16z lists LTV/CAC and payback last of its five", "Recomputes from spend and customer counts", "sourced", ["V", "a16z"]),
    ("Bank statements (3 to 12 months)", "N", "L", "Y", "Deal team before wiring; Papermark puts them at the pre-wire step of a seed", "Checks that revenue in the deck reaches the bank", "sourced", ["V", "PM"]),
    ("409A valuation", "N", "L", "Y", "Investor counsel and Kruze's tax list", "Files it; checks the date", "sourced", ["V", "Kruze"]),
    ("Customer contracts and order forms (top ten)", "N", "L", "Y", "Series A lead; Kruze asks for top ten invoices and contracts; Peony A adds anything above about $20,000", "Checks term, renewal and termination, and whether ARR rests on the paper", "sourced + inferred", ["V", "Kruze", "PeonyA", "Fortune"]),
    ("Customer references and letters of intent", "N", "L", "Y", "Series A lead; First Round runs 5 to 15 diligence conversations", "Calls them", "sourced", ["V", "PeonyA", "FR"]),
    ("Sales pipeline snapshot", "N", "L", "Y", "Deal team", "Compares stage counts with the growth plan", "sourced", ["V", "FR"]),
    ("Incorporation documents and bylaws", "Y", "Y", "Y", "Investor counsel; Cooley section B", "Confirms they exist and match the cap table", "sourced", ["Cooley", "V", "CRV"]),
    ("Prior financing: SAFEs, notes, term sheets", "Y", "Y", "Y", "Investor counsel; Cooley section C", "Matches each instrument to a cap table row", "sourced", ["Cooley", "V", "Hustle"]),
    ("IP and invention assignment agreements", "L", "Y", "Y", "Investor counsel; on CRV's first-pass list", "Checks every founder and contractor signed", "sourced", ["CRV", "Cooley", "V"]),
    ("Board and stockholder minutes", "L", "Y", "Y", "Investor counsel; Cooley section A; a16z does not pore over them unless it has a question", "Skims for financing approvals", "sourced", ["V", "a16z"]),
    ("Founder bios", "Y", "Y", "Y", "Partner; a16z says it uses LinkedIn instead", "Reads for founder-market fit", "sourced", ["V", "a16z"]),
    ("Key team bios and org chart", "L", "Y", "Y", "Partner", "Checks that the people in the plan exist", "sourced", ["V"]),
    ("Hiring plan and future org", "L", "Y", "Y", "Deal team; Kruze asks for a three-year hiring plan", "Multiplies hires by loaded cost and compares the result with the burn in the model", "sourced + inferred", ["V", "Kruze", "KruzeCash"]),
    ("Employment, advisory and option grant records", "N", "L", "Y", "Investor counsel; SeedLegals lists founder service agreements and key employment agreements", "Matches grants to the cap table", "sourced", ["V", "SL"]),
    ("Investor update archive", "N", "L", "Y", "Deal team; CRV recommends including them at seed", "Reads the trend and compares earlier numbers with today's", "sourced + inferred", ["V", "CRV"]),
    ("Product roadmap and demo", "Y", "Y", "Y", "Partner", "Watches the demo; reads the roadmap against the use of funds", "sourced", ["V"]),
    ("Market sizing and competitive landscape", "Y", "Y", "Y", "Partner; a16z says it does its own sizing", "Skims; investors build their own", "sourced", ["V", "a16z"]),
    ("Tax returns (three years)", "-", "-", "Y*", "Investor accountants; Kruze says a professional investor will ask", "Checks they were filed", "sourced", ["Kruze"]),
    ("Disclosure of claims, disputes and regulatory inquiries", "Y*", "Y*", "Y*", "Investor counsel; Cooley section D, Hustle's pre-seed baseline", "Reads the list", "sourced", ["Cooley", "Hustle"]),
]

# ---------------------------------------------------------------- Part 2
# (id, flag, where it shows up, mechanical check, needs a model reading, sources, organiser direction)
FLAGS = [
    ("RF1", "Churn hidden in cohort charts",
     "The cohort chart shows net dollar retention, so upgrades cover lost customers; customers who leave in the first weeks are dropped from the cohort size; the newest cohorts are missing or the best cohorts are shown alone.",
     "Rebuild cohorts from the revenue-by-customer export. Compare each cohort's starting count with the count in the model's cohort tab. Compute gross retention (each customer's later MRR capped at its starting MRR) beside net retention. Compare both with the deck's number. Check the a16z test that newer cohorts do better than older ones.",
     "Reading a footnote such as 'active after onboarding' and judging whether the exclusion is fair; reading a chart that exists only as an image in the deck.",
     ["A16Z16", "A16Z16b", "a16z", "BCV", "SaaStrGRR", "SaaStrTop", "Janz"], "organisers"),
    ("RF2", "Revenue counted as ARR when it is not recurring",
     "ARR includes a pilot, one-time fees, professional services, or a signed contract that has not gone live; MRR is multiplied by 12 from an all-in month.",
     "Tag each line of the ARR build by product type using the revenue export (subscription, pilot, onboarding, services). Recompute ARR from subscription lines only. Flag any ARR line whose contract is under 12 months or can end on short notice.",
     "Reading the contract: is a pilot, an evaluation or an opt-out clause present, and does the customer owe anything after the first term.",
     ["A16Z16", "A16Z16b", "BVP", "Lighter", "LighterC", "Fortune", "Hustle"], "organisers"),
    ("RF3", "Burn does not match the hiring plan",
     "The model's payroll line grows by a few hires while the hiring plan lists many more, or the plan's start dates are earlier than the model uses. The deck's runway comes from the lighter model.",
     "Build monthly payroll from the hiring plan: base pay times a loaded-cost factor, from each start month. Compare it with the model's payroll line and the cash tab. Recompute runway from cash and net burn. Compare it with the deck.",
     "Reading start dates or comp notes that sit in text (offer letters, assumptions notes); judging whether the loaded-cost factor is fair.",
     ["KruzeCash", "A16Z16", "SaaStrTop"], "organisers"),
    ("RF4", "Numbers disagree between the deck and the model",
     "The same ARR, customer count or margin appears with different values in the deck, the model, the metrics export and what the founder says on video.",
     "Pull labeled numbers from the deck's claims page and from named cells in the model and exports. Match by label and period. Flag any pair that differs by more than a set tolerance.",
     "Matching 'customers' on a slide to 'logos' or 'paying accounts' in the model; spotting a different date or definition behind the same label; reading a number spoken on video.",
     ["a16z", "CRV", "V"], "organisers"),
    ("RF5", "Customer concentration",
     "One customer or one group of locations makes up a large share of MRR while the deck says the base is spread out.",
     "From revenue by customer: top-one and top-three share of MRR. Compare with the deck's claim. Flag when the computed share is above the deck claim, or above a set line (MicroVentures calls 20 percent a common rule of thumb; a16z gives the definition and no line, so the line is a setting).",
     "Reading the big customer's contract for renewal date and termination rights, which decide how risky the share is.",
     ["A16Z16b", "Micro", "PeonyA", "Hustle"], "extra"),
    ("RF6", "Gross margin leaves out hosting or support cost",
     "Cost of revenue holds only some delivery costs. Hosting, model inference and support staff sit under R&D or sales.",
     "Recompute gross margin with every ledger line tagged as hosting, inference, telephony, or support included. Compare with the deck. Use benchmarks as context only: Bessemer's average is 65 to 70 percent with a middle half of 60 to 80, while a16z says software should sit at 80 to 90.",
     "Classifying ambiguous ledger lines such as 'platform costs' or 'customer experience salaries'.",
     ["A16Z16", "A16Z16b", "Tunguz", "Stripe", "BVP"], "extra"),
    ("RF7", "Vanity metric: cumulative sign-ups shown as active users",
     "A count that can only rise (accounts created, downloads, total users ever) is shown as active customers.",
     "Test whether the deck's number equals the last value of a cumulative column. Test the column for never decreasing. Compare with the active or paying count in the metrics export.",
     "Reading a chart or label that does not say what 'users' means.",
     ["A16Z16", "A16Z16b"], "extra"),
]

# Published flags that are NOT planted in our room (listed so the report is honest about scope)
UNPLANTED = [
    ("Cap table that does not reconcile (unconverted SAFE, undocumented grants)", ["CRV", "PeonyA"]),
    ("Missing IP assignments from founders or contractors", ["CRV", "V", "PM"]),
    ("Bookings counted as revenue; letters of intent counted as bookings", ["A16Z16", "Hustle"]),
    ("Cherry-picked cohorts or periods; only a few months of history", ["a16z", "BCV"]),
    ("Blended CAC that hides weak paid channels", ["A16Z16"]),
    ("Stale documents that disagree with current numbers", ["CRV", "Ellty"]),
    ("Customers who keep paying but use the product far less (stealth churn)", ["Stealth"]),
    ("Tax returns not filed", ["Kruze"]),
    ("Truncated y-axis or cumulative chart used for a metric that should not be cumulative", ["A16Z16b", "A16Z16"]),
]

# ---------------------------------------------------------------- Part 3
N = NUM
PLANTED = [
    # id, name, organiser direction, where it lives, true, shown, mechanical check
    ("PF1", "Pilot booked as ARR", "revenue counted as ARR when not recurring",
     "financial_model.xlsx / ARR_Build / row 'Marlow Veterinary Group (pilot)' and cell ARR_TOTAL; monthly_metrics.csv column arr (2026-09); pilot_agreement_marlow.pdf clauses 2, 7, 8",
     f"Recurring ARR {money(N['arr_true_recurring'])}; the pilot contracts {money(N['pilot_fees_actually_contracted'])} of fees in total and can end on 30 days notice",
     f"Model ARR {money(N['arr_model_shown'])}, which counts the pilot as {money(N['pilot_arr_counted'])} a year",
     "Recompute ARR from rows with product_type = Subscription in customer_mrr_by_month.csv and compare with ARR_TOTAL"),
    ("PF2", "Deck ARR disagrees with the model", "numbers that disagree between the deck and the model",
     "pitch_deck.pdf slide 3 and claims slide 14; financial_model.xlsx cell ARR_TOTAL",
     f"Model {money(N['arr_model_shown'])} (true recurring {money(N['arr_true_recurring'])})",
     f"Deck {money(N['arr_deck_shown'])}, a gap of {money(N['arr_deck_shown'] - N['arr_model_shown'])} to the model",
     "Match the deck claim labeled ARR to the named cell ARR_TOTAL; tolerance 1 percent"),
    ("PF2b", "Video ARR disagrees with the deck", "numbers that disagree between the deck and the model",
     "pitch_video_script.md line at about 0:35 (and the recorded video, once Ken records it)",
     f"Deck {money(N['arr_deck_shown'])}",
     f"Spoken: about {money(N['arr_video_spoken'])}",
     "Transcribe the video, extract the ARR sentence, compare with the claims page"),
    ("PF3", "Churn hidden in the cohort tab", "churn hidden in cohort charts",
     "financial_model.xlsx / Cohorts (month-0 counts and the NRR row); pitch_deck.pdf slide 6 chart and claims row 'Net revenue retention'; note on the Cohorts tab: 'Cohort = customers still active after onboarding'",
     f"12-month net retention {pct(N['nrr_12m_true'])}, gross retention {pct(N['grr_12m_true'])}, {N['cohort_customers_true']} customers in the nine cohorts",
     f"Net retention {pct(N['nrr_12m_reported_in_cohort_tab'])}, {N['cohort_customers_reported']} customers (the {N['cohort_customers_true'] - N['cohort_customers_reported']} who left within two months are dropped)",
     "Rebuild cohorts from customer_mrr_by_month.csv; compare month-0 counts and NRR; compute GRR"),
    ("PF4", "Burn and runway do not match the hiring plan", "burn that does not match the hiring plan",
     "hiring_plan.csv (24 rows); financial_model.xlsx / P&L forecast row 'Payroll' and Cash_Runway; pitch_deck.pdf slide 11 and claims row 'Runway'",
     f"{N['hires_in_hiring_plan']} hires in the plan; runway {N['runway_months_implied_by_hiring_plan']} months; average net burn over the next 12 months {money(N['avg_monthly_net_burn_first_12m_implied'])} a month",
     f"The model counts {N['hires_counted_in_model']} hires; runway {N['runway_months_shown_in_model']} months in the model; average burn {money(N['avg_monthly_net_burn_first_12m_shown'])} a month",
     "Payroll from hiring_plan.csv times the load factor in Assumptions; rerun cash; compare with Cash_Runway and the deck"),
    ("PF5", "Customer concentration", "extra (published flag)",
     "customer_mrr_by_month.csv (customer C-BIG); order_form_cedar_pine.pdf; pitch_deck.pdf slide 4 and claims row 'Largest customer'",
     f"Largest customer {pct(N['big_customer_share_true'])} of MRR; top three {pct(N['top3_share_true'])}",
     f"Deck: no customer above {pct(N['big_customer_share_claimed_under'], 0)} of ARR",
     "Top-one and top-three share from customer_mrr_by_month.csv; compare with the deck claim"),
    ("PF6", "Gross margin excludes hosting, inference and support", "extra (published flag)",
     "financial_model.xlsx / P&L rows 'Cloud hosting and model inference' (under R&D) and 'Customer support specialists' (under S&M); expense_ledger.csv categories; pitch_deck.pdf slide 5 and claims row 'Gross margin'",
     f"Gross margin {pct(N['gross_margin_true'])} when delivery costs are included",
     f"Deck and model: {pct(N['gross_margin_shown'], 0)}",
     "Sum ledger lines tagged hosting, inference, telephony, support into cost of revenue; recompute"),
    ("PF7", "Cumulative sign-ups shown as active clinics", "extra (published flag)",
     "monthly_metrics.csv column accounts_created_cumulative; pitch_deck.pdf slide 3 and claims row 'Clinics on Hollis'",
     f"{N['paying_clinics_true']} paying accounts (column paying_accounts)",
     f"Deck: {N['accounts_created_cumulative_shown_as_active']} clinics, which is the last value of a column that never decreases",
     "Monotonic test on each metrics column; match the deck number to the column's last value"),
]

DECOYS = [
    ("DC1", "Onboarding fee excluded from ARR correctly", "financial_model.xlsx / ARR_Build row 'Onboarding fees (one-time, excluded)'", "A checker must not flag the $500 fee as ARR"),
    ("DC2", "Annual prepay counted as recurring correctly", "order_form_brookline_row.pdf and customer row for Brookline Row Veterinary", "Cash arrives up front, revenue is spread monthly, ARR counts it once; must not be flagged"),
    ("DC3", "Clean cap table", "cap_table.xlsx", "Holders add to 100.00 percent and the SAFE conversion at the stated cap is right; must not be flagged"),
]

# (file, format, what it is, tier) tier: seed drop (thin) or Series A (full room)
FILES = [
    ("00_welcome/cover_note_and_index.pdf", "PDF, 1 page", "Cover note and a numbered index of the room.", "seed + A"),
    ("01_overview/pitch_deck.pdf", "PDF, 14 slides", "Deck with a claims page (slide 14) listing every number with its slide.", "seed + A"),
    ("01_overview/company_overview.pdf", "PDF, 1 page", "One-page company overview: what, who, traction, ask.", "seed + A"),
    ("01_overview/pitch_video_script.md", "Markdown, about 300 words", "Two-minute script for Ken to record on his phone; says an ARR figure that differs from the deck.", "seed + A"),
    ("02_financials/financial_model.xlsx", "Excel", "Tabs: README, Assumptions, P&L, ARR_Build, Cohorts, Hiring_Plan, Cash_Runway.", "seed + A"),
    ("02_financials/cap_table.xlsx", "Excel", "Fully diluted cap table with two SAFEs and an option pool; clean (decoy).", "seed + A"),
    ("02_financials/expense_ledger.csv", "CSV", "Expense lines by month with vendor and category; lets a checker recompute gross margin.", "A"),
    ("03_metrics/monthly_metrics.csv", "CSV, 21 months", "MRR, ARR, paying accounts, accounts created (cumulative), calls handled.", "seed + A"),
    ("03_metrics/customer_mrr_by_month.csv", "CSV", "One row per customer per month with plan, MRR and product_type.", "A"),
    ("04_customers/order_form_cedar_pine.pdf", "PDF, 3 pages", "Largest customer: 17 locations, 24-month term.", "A"),
    ("04_customers/pilot_agreement_marlow.pdf", "PDF, 3 pages", "Six-month pilot, 30 days notice to end, no duty to convert.", "A"),
    ("04_customers/order_form_brookline_row.pdf", "PDF, 2 pages", "Ordinary annual prepaid subscription (decoy).", "A"),
    ("05_team/founder_bios.pdf", "PDF, 2 pages", "Two invented founders and the senior team.", "seed + A"),
    ("05_team/hiring_plan.csv", "CSV, 24 rows", "Role, department, start month, base pay.", "seed + A"),
    ("06_product/product_one_pager.pdf", "PDF, 1 page", "What the product does, pricing tiers, integrations.", "seed + A"),
    ("06_product/website_copy.md", "Markdown", "Home page and pricing copy for the web scan.", "seed + A"),
]


# Which files a mechanical check needs. A flag is catchable from the thin seed drop when every
# required file is in that drop.
REQUIRES = {
    "PF1": ["02_financials/financial_model.xlsx", "03_metrics/customer_mrr_by_month.csv", "04_customers/pilot_agreement_marlow.pdf"],
    "PF2": ["01_overview/pitch_deck.pdf", "02_financials/financial_model.xlsx"],
    "PF2b": ["01_overview/pitch_video_script.md", "01_overview/pitch_deck.pdf"],
    "PF3": ["02_financials/financial_model.xlsx", "03_metrics/customer_mrr_by_month.csv", "01_overview/pitch_deck.pdf"],
    "PF4": ["05_team/hiring_plan.csv", "02_financials/financial_model.xlsx", "01_overview/pitch_deck.pdf"],
    "PF5": ["03_metrics/customer_mrr_by_month.csv", "01_overview/pitch_deck.pdf"],
    "PF6": ["02_financials/financial_model.xlsx", "01_overview/pitch_deck.pdf"],
    "PF7": ["03_metrics/monthly_metrics.csv", "01_overview/pitch_deck.pdf"],
}


def seed_drop_paths():
    return {f[0] for f in FILES if f[3] == "seed + A"}


def catchable_from_seed_drop():
    drop = seed_drop_paths()
    return {k: all(path in drop for path in v) for k, v in REQUIRES.items()}


def write_csv(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    write_csv("data_room_documents.csv",
              ["document", "pre_seed", "seed", "series_a", "who_asks", "first_pass", "basis", "sources"],
              [(d[0], d[1], d[2], d[3], d[4], d[5], d[6], ";".join(d[7])) for d in DOCS])
    write_csv("data_room_flags.csv",
              ["id", "flag", "shows_up_as", "mechanical_check", "needs_model_reading", "sources", "direction"],
              [(f[0], f[1], f[2], f[3], f[4], ";".join(f[5]), f[6]) for f in FLAGS])
    write_csv("data_room_planted.csv", ["id", "name", "direction", "where", "true", "shown", "check"], PLANTED)
    write_csv("data_room_files.csv", ["path", "format", "what", "tier"], FILES)

    def count_stage(idx):
        out = {}
        for d in DOCS:
            v = d[idx].rstrip("*")
            out[v] = out.get(v, 0) + 1
        return out

    print("documents in table:", len(DOCS))
    print("  pre-seed Y/L/N/-:", count_stage(1))
    print("  seed     Y/L/N/-:", count_stage(2))
    print("  series A Y/L/N/-:", count_stage(3))
    print("  rows with stage letters from Visible only:", sum(1 for d in DOCS if not any(d[i].endswith("*") for i in (1, 2, 3))))
    print("  rows with a starred (non-Visible) stage:", sum(1 for d in DOCS if any(d[i].endswith("*") for i in (1, 2, 3))))
    print("red-flag catalog rows:", len(FLAGS))
    print("  organisers' four:", sum(1 for f in FLAGS if f[6] == "organisers"), " extra:", sum(1 for f in FLAGS if f[6] == "extra"))
    print("published flags we do not plant:", len(UNPLANTED))
    print("planted entries:", len(PLANTED), "(flags", len([p for p in PLANTED if not p[0].endswith('b')]), "plus", len([p for p in PLANTED if p[0].endswith('b')]), "variant)")
    print("decoys:", len(DECOYS))
    c = catchable_from_seed_drop()
    print("catchable from the seed drop:", sorted(k for k, v in c.items() if v), "count", sum(c.values()))
    print("need the full Series A room:", sorted(k for k, v in c.items() if not v), "count", sum(1 for v in c.values() if not v))
    missing = {p for v in REQUIRES.values() for p in v} - {f[0] for f in FILES}
    print("required paths missing from the file list (must be empty):", missing)
    print("files in the room:", len(FILES), " seed drop:", sum(1 for f in FILES if f[3] == "seed + A"), " Series A only:", sum(1 for f in FILES if f[3] == "A"))
    srcs = set()
    for d in DOCS:
        srcs.update(d[7])
    for f in FLAGS:
        srcs.update(f[5])
    print("distinct source pages linked in tables:", len(srcs))
    saved = [p for p in os.listdir(os.path.join(HERE, "raw", "data_room")) if p.endswith(".txt")]
    print("saved page texts under raw/data_room:", len(saved))

    if "--tables" in sys.argv:
        print("\n=== DOCS TABLE ===")
        print("| # | Document | Pre-seed | Seed | Series A | Who asks | What a first-pass reader does | Basis | Sources |")
        print("|---|---|---|---|---|---|---|---|---|")
        for i, d in enumerate(DOCS, 1):
            print(f"| {i} | {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} | {d[6]} | {link(*d[7])} |")
        print("\n=== FLAGS TABLE ===")
        for f in FLAGS:
            print(f"**{f[0]}. {f[1]}**\n- Shows up as: {f[2]}\n- Mechanical check: {f[3]}\n- Needs a model reading: {f[4]}\n- Sources: {link(*f[5])}\n")
        print("\n=== UNPLANTED ===")
        for u in UNPLANTED:
            print(f"- {u[0]}" + (f" ({link(*u[1])})" if u[1] else ""))
        print("\n=== PLANTED TABLE ===")
        print("| ID | Flag | Organiser direction | Where it lives | True | Shown | Check that catches it |")
        print("|---|---|---|---|---|---|---|")
        for p in PLANTED:
            print("| " + " | ".join(p) + " |")
        print("\n=== DECOYS ===")
        print("| ID | Clean item | Where | Why it is here |")
        print("|---|---|---|---|")
        for d in DECOYS:
            print("| " + " | ".join(d) + " |")
        print("\n=== FILES ===")
        print("| Path under data_room/out/hollis_series_a/ | Format | What it is | In the seed drop |")
        print("|---|---|---|---|")
        for f in FILES:
            print(f"| `{f[0]}` | {f[1]} | {f[2]} | {'yes' if f[3] == 'seed + A' else 'no'} |")


if __name__ == "__main__":
    main()
