"""MEMO_TEMPLATE.md's section table, as data.

One row per section, in the template's order. Each row says which readout
pieces, FRAMEWORKS entries, checklist items and scans fill it, and who writes
it. Change the template first; then change this table to match.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _ids(*spans: str) -> tuple[str, ...]:
    """'C02-C13' and 'C29' -> ('C02', ..., 'C13', 'C29')."""
    out: list[str] = []
    for span in spans:
        if "-" in span:
            a, b = span.split("-")
            out += [f"C{n:02d}" for n in range(int(a[1:]), int(b[1:]) + 1)]
        else:
            out.append(span)
    return tuple(out)


@dataclass(frozen=True)
class Section:
    number: int
    key: str
    title: str
    who_writes: str
    pieces: tuple[str, ...] = ()
    entries: tuple[str, ...] = ()
    checklist: tuple[str, ...] = ()
    # The operator writes it; Tricorder leaves a slot and supplies only facts.
    operator_owned: bool = False
    labels: tuple[str, ...] = field(default=())


SECTIONS: tuple[Section, ...] = (
    Section(1, "header", "Header", "Tricorder fills it; the operator signs it.",
            pieces=("the_pitch_itself",), checklist=_ids("C60", "C72")),
    Section(2, "summary", "Summary and the ask", "Tricorder drafts; the operator writes the recommendation line.",
            checklist=_ids("C61", "C64")),
    Section(3, "company", "Company and problem", "Tricorder drafts from the company's own words, marked as the company's.",
            entries=("1.1", "5.1", "5.2"), checklist=_ids("C59", "C92")),
    Section(4, "market", "Market", "Tricorder.",
            pieces=("market",), entries=("3.1", "3.2", "5.6"), checklist=_ids("C47-C50"),
            labels=("tam", "sam", "som", "signal")),
    Section(5, "product", "Product", "Tricorder; product judgements are marked \"Reading:\".",
            entries=("4.1", "7.1"), checklist=_ids("C63", "C68", "C62", "C89")),
    Section(6, "business_model", "Business model and unit economics", "Tricorder.",
            pieces=("unit_economics",), entries=("1.7", "1.9", "1.12"), checklist=_ids("C30-C33"),
            labels=("gross_margin", "cost_of_revenue", "arpa", "cac", "payback_months", "ltv", "price")),
    Section(7, "traction", "Traction and customers", "Tricorder.",
            pieces=("traction_and_revenue", "retention", "customers"),
            entries=("1.2", "1.3", "1.5", "1.6", "1.8", "1.13", "4.3"),
            checklist=_ids("C02-C13", "C14-C18", "C34-C46"),
            labels=("arr", "mrr", "paying_accounts", "accounts_created", "nrr_12m", "grr_12m", "cohort_size",
                    "largest_customer_share", "top3_customer_share", "acv", "contract_term", "notice_period")),
    Section(8, "competition", "Competition and comparables", "Tricorder.",
            pieces=("comps",), entries=("2.1", "2.2", "5.4"), checklist=_ids("C51", "C52")),
    Section(9, "team", "Team", "Tricorder for facts; the operator for their view of the founders.",
            pieces=("team",), entries=("6.1", "6.2"), checklist=_ids("C53-C56", "C91", "C93"),
            labels=("headcount", "hires")),
    Section(10, "financials", "Financials, burn and runway", "Tricorder.",
            pieces=("burn_and_runway",), entries=("1.4", "1.11"), checklist=_ids("C19-C22", "C24", "C29"),
            labels=("runway_months", "net_burn_monthly", "payroll_monthly", "cash")),
    Section(11, "deal_terms", "Deal terms", "Tricorder for the facts; the operator for whether the price is right.",
            pieces=("the_pitch_itself",), entries=("1.10",), checklist=_ids("C72", "C75", "C67", "C81", "C90"),
            labels=("raise_amount", "pre_money", "post_money", "ownership")),
    Section(12, "risks", "Risks and open questions", "Tricorder lists them; the operator ranks them and adds their own."),
    Section(13, "outcomes", "Outcomes", "The operator.", checklist=_ids("C52"), operator_owned=True),
    Section(14, "diligence", "Diligence: what was checked and what to ask", "Tricorder.",
            checklist=_ids("C29", "C46", "C58", "C71")),
    Section(15, "recommendation", "Recommendation", "The operator.", operator_owned=True),
    Section(16, "sources", "Sources and change log", "Tricorder.", checklist=_ids("C64")),
)

BY_NUMBER = {s.number: s for s in SECTIONS}

# Body sections a claim can be routed to, in the order routing tries them.
BODY = (3, 4, 5, 6, 7, 8, 9, 10, 11)

# A piece's home section. "the pitch itself" is deal terms (11); the header reads it too.
PIECE_SECTION = {p: s.number for s in SECTIONS if s.number in BODY for p in s.pieces}

# FRAMEWORKS entry -> body section, from the template's "Filled from" column. The first listed wins.
ENTRY_SECTION: dict[str, int] = {}
for _s in SECTIONS:
    if _s.number in BODY:
        for _e in _s.entries:
            ENTRY_SECTION.setdefault(_e, _s.number)

LABEL_SECTION = {lab: s.number for s in SECTIONS for lab in s.labels}

# Last resort: the room folder a claim's first source sits in.
FOLDER_SECTION = {"00_welcome": 3, "01_overview": 3, "02_financials": 10, "03_metrics": 7,
                  "04_customers": 7, "05_team": 9, "06_product": 5}

# FRAMEWORKS entry number's first part -> the scan that writes it.
ENTRY_SCAN = {"1": "redflags", "2": "comps", "3": "signals", "4": "video", "5": "frameworks",
              "6": "founders", "7": "presence"}
# Entry 1.1 (deck, overview and website claims) is the claims workflow's.
ENTRY_SCAN_OVERRIDE = {"1.1": "claims"}


def scans_for(section: Section) -> tuple[str, ...]:
    """The scans whose results fill a section, in entry order, without repeats."""
    out: list[str] = []
    for e in section.entries:
        name = ENTRY_SCAN_OVERRIDE.get(e) or ENTRY_SCAN[e.split(".")[0]]
        if name not in out:
            out.append(name)
    return tuple(out)


PIECE_WORDS = {
    "traction_and_revenue": "Traction and revenue", "retention": "Retention", "burn_and_runway": "Burn and runway",
    "unit_economics": "Unit economics", "customers": "Customers", "market": "Market", "comps": "Comps",
    "team": "Team", "the_pitch_itself": "The pitch itself",
}

VERDICT_WORDS = {"looking_strong": "looking strong", "looking_weak": "looking weak", "mixed": "mixed",
                 "not_enough_in_the_room": "not enough in the room"}

LABEL_WORDS = {
    "arr": "ARR", "mrr": "MRR", "paying_accounts": "Paying accounts", "accounts_created": "Accounts created",
    "nrr_12m": "Net revenue retention", "grr_12m": "Gross revenue retention", "cohort_size": "Cohort size",
    "gross_margin": "Gross margin", "cost_of_revenue": "Cost of revenue", "runway_months": "Runway",
    "net_burn_monthly": "Monthly burn", "payroll_monthly": "Payroll", "hires": "Hires", "headcount": "Headcount",
    "cash": "Cash", "largest_customer_share": "Customer concentration", "top3_customer_share": "Customer concentration",
    "arpa": "Revenue per account", "acv": "Contract value", "cac": "CAC", "payback_months": "Payback",
    "ltv": "Lifetime value", "raise_amount": "The raise", "pre_money": "Pre-money", "post_money": "Post-money",
    "ownership": "Ownership", "tam": "Market size", "sam": "Market size", "som": "Market size", "price": "Price",
    "contract_term": "Contract term", "notice_period": "Notice period", "signal": "Outside signal", "other": "",
}

STAGE_WORDS = {"pre_seed": "pre-seed", "seed": "seed", "series_a": "Series A"}
