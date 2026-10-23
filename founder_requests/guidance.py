"""Guidance on what to submit, one entry per document guide.

Each entry says, in words a founder reads, what the document is, the form
that works best, and what a good one shows. Every entry is taken from its
guide in docs/reports/20261022.03_document_guides/<slug>.md: "what" and
"form" from the guide's "What it is" section, "good" from its "Green flags"
section. tests/test_guidance.py checks that every guide the checklist names
has an entry and that each entry's sections exist in its guide.

The words are rewritten for the founder: no investor jargon about flags, no
file paths, no checklist ids. A guide changes; this table is edited by hand
to match, and the test names the guide that has no entry.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDES = ROOT / "docs" / "reports" / "20261022.03_document_guides"
CHECKLIST_CSV = ROOT / "docs" / "ongoing" / "checklist.csv"

# The guide sections each field is taken from. The test finds these headings in every guide.
FROM_SECTIONS = {"what": "What it is", "form": "What it is", "good": "Green flags"}


@dataclass(frozen=True)
class Guidance:
    guide: str          # the guide's file stem, e.g. "monthly-revenue-by-customer"
    title: str          # the document's name, for the founder
    what: str           # what the document is
    form: str           # the form that works best
    good: tuple[str, ...]  # what a good one shows

    @property
    def path(self) -> str:
        return f"docs/reports/20261022.03_document_guides/{self.guide}.md"


def _g(guide, title, what, form, *good):
    return Guidance(guide, title, what, form, tuple(good))


GUIDANCE: dict[str, Guidance] = {g.guide: g for g in (
    _g("409a-valuation", "409A valuation",
       "An outside appraisal of what your common stock is worth. It sets the lowest price at which options can be granted.",
       "The PDF report from the valuation firm or cap table platform, with its effective date.",
       "A current report from an independent provider", "a refresh after each round",
       "the date the board adopted it"),
    _g("ai-and-data-governance-documents", "AI and data governance documents",
       "A short record of the AI models and vendors the product uses, the data behind them, and your rights to that data.",
       "A one-page note is enough at this stage, with the agreement for each AI vendor attached.",
       "Each dataset with its source and your right to use it", "which outside AI services you depend on",
       "how customer data is used and kept"),
    _g("audited-or-reviewed-financials", "Audited or reviewed financials",
       "Financial statements an outside accountant has reviewed or audited, with the firm's signed report on the front.",
       "The signed report and the statements it covers, as one PDF per year.",
       "A recent year", "numbers that equal your own management accounts", "the level of work: compilation, review or audit"),
    _g("bank-statements", "Bank statements",
       "Monthly statements for every business bank account, and any cards, loans and payment-processor balances.",
       "PDFs downloaded straight from the bank, one per account per month. A CSV export from the bank also works.",
       "Every account and every month in the period", "deposits that tie to revenue",
       "investor wires that match the SAFEs and the cap table"),
    _g("board-stockholder-minutes", "Board and stockholder minutes and consents",
       "The written record of decisions by the board and the stockholders: minutes of meetings and written consents.",
       "Signed PDFs, in date order, as they sit in your minute book.",
       "A consent for every stock issuance, SAFE and option grant", "approvals that match the cap table line for line"),
    _g("cap-table", "Cap table, current and pro forma",
       "A list of every holder of the company's equity and what each holds: common, preferred, options, SAFEs and notes.",
       "A spreadsheet or a cap table platform export, fully diluted, with the date it is as of. Add a pro forma tab for this round.",
       "Totals that tie out", "the option pool, issued and unissued", "how each SAFE converts in this round"),
    _g("claims-disputes-inquiries", "Statement of claims, disputes and inquiries",
       "A short written statement that lists any lawsuits, threatened claims, disputes or regulator contact, or says there are none.",
       "A signed one-page letter or PDF. A short paragraph is fine at this stage.",
       "Each matter with a line of context", "threats listed even if they may come to nothing",
       "a plain statement of \"none\" if there are none"),
    _g("cohort-or-retention-export", "Cohort or retention table",
       "A table that groups customers by the month they started and shows how many of them, or how much of their revenue, is left in each later month.",
       "A CSV or a spreadsheet tab, one row per starting month and one column per month since the start.",
       "Both customer and revenue retention", "monthly and annual plans kept apart",
       "a one-line definition of a cohort"),
    _g("cover-note-and-document-index", "Cover note and document index",
       "A one-page note at the top of the room and a list of every file in it.",
       "A PDF or a document with one line per file and the date each file is as of.",
       "An index that matches the room", "the files you are holding back, named"),
    _g("customer-contracts-and-order-forms", "Customer contracts and order forms",
       "The signed agreement with each customer: order form, master agreement, pilot agreement or amendment.",
       "Signed PDFs, one file per contract, named for the customer.",
       "Signed paper behind every customer you count", "the term, price, renewal and notice terms",
       "for a pilot, whether and how it converts to paid"),
    _g("customer-references-and-letters-of-intent", "Customer references and letters of intent",
       "Names and contacts of customers and others we may call, and any letters of intent.",
       "A short list with name, title, company, email and how they know you. Letters of intent as signed PDFs.",
       "Your largest customer", "a customer who stopped using the product",
       "letters of intent with a named buyer, a use case and a dollar figure"),
    _g("employment-advisory-and-option-grant-records", "Employment, advisory and option grant records",
       "The signed documents that say what each person was promised and holds: offer letters, advisor agreements and option grants.",
       "A spreadsheet ledger of every grant (holder, date, shares, strike, vesting, board approval date) and a folder of the signed PDFs.",
       "A ledger that ties to the cap table", "each grant approved before it was made",
       "founder vesting and 83(b) filings"),
    _g("financial-model", "Financial model",
       "Your spreadsheet of revenue, costs, hiring and cash, with past months marked actual and future months marked plan.",
       "An Excel or Google Sheets file with formulas, not a PDF of charts, with the assumptions tab visible.",
       "Assumptions on one page, each with a source", "the same logic for past and future months",
       "a downside case"),
    _g("founder-bios", "Founder bios",
       "A short bio for each founder: roles held, what they built, time in the customer's industry, and why this company.",
       "One page per founder as a PDF, with dated roles and links to public work.",
       "Dated, specific roles", "public work from before the company", "links you want us to look at"),
    _g("founder-video-or-recorded-intro", "Founder video",
       "A short recording of the founders talking about the company.",
       "A video file or a link, a few minutes long, founders only.",
       "The founders speaking plainly", "numbers that match the deck"),
    _g("hiring-plan-and-future-org", "Hiring plan",
       "A list of the people you plan to add, one row per hire.",
       "A CSV or a spreadsheet tab with one row per planned hire: role, department, start date, base pay and equity grant.",
       "The next 12 to 18 months", "pay and start date for every hire", "start dates tied to milestones"),
    _g("historical-financials", "Monthly financial statements",
       "Three statements, month by month, from your accounting system: profit and loss, balance sheet and cash flow.",
       "An export from QuickBooks, Xero or a similar tool, as a spreadsheet, one column per month, with the basis (cash or accrual) stated.",
       "Every month since the first revenue month", "actual months clearly marked",
       "revenue recognised over the service period, with deferred revenue on the balance sheet"),
    _g("incorporation-documents", "Incorporation documents and bylaws",
       "The company's formation set: the filed certificate of incorporation with amendments, the bylaws and the first board consent.",
       "File-stamped PDFs, plus a good standing certificate dated in the last few months.",
       "The full set, with every amendment", "founder stock agreements with vesting and 83(b) elections"),
    _g("investor-update-archive", "Investor updates",
       "The updates you have sent to existing investors, usually monthly.",
       "The original emails or PDFs, with send dates.",
       "The same metric definitions each month", "the bad months as well as the good ones",
       "runway stated in each update"),
    _g("ip-assignment", "IP and invention assignment agreements",
       "The signed agreements by which founders, employees and contractors give the company what they create for it.",
       "Signed PDFs, one per person, plus a list of anyone who has not signed.",
       "A signed agreement from every founder, employee and contractor who has built product",
       "founder agreements covering work from before the company", "signing dates on or before each start date"),
    _g("key-team-bios-and-org-chart", "Key team bios and org chart",
       "A short bio for each key person below the founders, and a chart of who reports to whom.",
       "A PDF page or a slide. Mark contractors and open roles on the chart.",
       "A headcount that matches the other files", "a named owner for each core function",
       "open roles tied to the hiring plan"),
    _g("kpi-dashboard-or-metrics-export", "Monthly metrics",
       "A short table of company numbers by month: monthly recurring revenue, annual recurring revenue, paying customers and churn.",
       "A CSV or a spreadsheet, one row per month since the first revenue month.",
       "New, expansion, contraction and churned revenue split out", "a one-line definition of each term",
       "pilot and one-time revenue kept apart from recurring revenue"),
    _g("market-sizing-and-competitive-landscape", "Market sizing and competitors",
       "Your estimate of the market the product can reach, and who else sells to the same buyers.",
       "A slide, a model tab or a short memo. Show the math, not only the total.",
       "The count of target customers with its source and date", "the price per customer",
       "your nearest competitors by name"),
    _g("material-agreements-other-than-customer-contracts", "Material agreements",
       "Agreements other than customer contracts that bind the company: leases, loans, insurance, licences, consulting and vendor agreements.",
       "A one-page schedule listing each agreement, with signed copies as PDFs.",
       "Every agreement with obligations over $25,000", "any loan with its lien filings",
       "signed copies kept apart from drafts"),
    _g("monthly-revenue-by-customer", "Monthly revenue by customer",
       "A table with one row per customer per month, showing what each customer paid or was billed.",
       "A CSV with one row per customer per month, exported from your billing or accounting system.",
       "Every month since the first customer", "the plan and the kind of revenue (subscription, pilot, one-time)",
       "the amount invoiced kept apart from the revenue earned"),
    _g("one-page-summary", "One-page summary",
       "A one-page fact sheet on the company: what it does, the team, traction, the market and the round.",
       "A PDF, with its date.",
       "Figures that match the deck", "dated numbers"),
    _g("pitch-deck", "Pitch deck",
       "The presentation that tells the company's story and states its numbers.",
       "A PDF of the current version, the one you sent to other investors, with its date.",
       "Numbers that can be traced to a file in the room", "an ask tied to milestones"),
    _g("prior-financing", "Prior financing documents",
       "The papers for each earlier raise: SAFEs or notes with any side letters, and term sheets.",
       "Signed PDFs, one per investor, plus the term sheet for this round.",
       "A signed document for every instrument on the cap table", "every side letter"),
    _g("product-roadmap-and-demo", "Product roadmap and demo",
       "A short plan of what the team will build and when, and a way to see the product work.",
       "A one-page roadmap with dates and owners, and a recorded demo or a sandbox login.",
       "Which parts of the demo are live", "milestones tied to the money in this round"),
    _g("sales-pipeline-snapshot", "Sales pipeline",
       "A dated list of the deals you are working: buyer, value, stage, created date, expected close and next step.",
       "An opportunity-level export from your CRM, or a sheet, including closed-lost deals.",
       "Deals that move between stages", "closed-lost deals with reasons", "the date of the export"),
    _g("tax-returns", "Tax returns",
       "The company's filed income tax returns, with proof of filing.",
       "PDFs from the tax software, one per year, with payroll and state filings.",
       "Every year since incorporation", "proof of filing"),
    _g("unit-economics", "Unit economics",
       "The numbers that say whether you make money on the average customer after paying to win and serve them: acquisition cost, payback and lifetime value.",
       "A spreadsheet tab with monthly sales and marketing spend and new paying customers by month, plus how you define each number.",
       "How acquisition cost is worked out", "spend by channel", "payback worked out on gross margin"),
    _g("use-of-funds-plan", "Use of funds",
       "A short plan for the money in this round: how much, spent on what, over how many months, to reach which milestones.",
       "A slide or a spreadsheet, by month and by category.",
       "Lines that add to the raise", "the milestones the money reaches", "when you expect to raise next"),
)}


@lru_cache(maxsize=1)
def guide_of() -> dict[str, str]:
    """Checklist id -> guide stem, from checklist.csv's `guide` column. Rows with no guide are left out."""
    with open(CHECKLIST_CSV, newline="", encoding="utf-8") as fh:
        return {r["id"]: r["guide"] for r in csv.DictReader(fh) if r.get("guide")}


def for_item(checklist_id: str | None) -> Guidance | None:
    """The guidance for a checklist item, or None when it has no guide."""
    if not checklist_id:
        return None
    stem = guide_of().get(checklist_id)
    return GUIDANCE.get(stem) if stem else None
