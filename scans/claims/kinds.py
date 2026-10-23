"""What each claim is about, and where the room should back it up.

`classify` gives a figure its kind from the words around it, by ordered rules.
`KINDS` is the normalisation and the evidence map in one table: for each kind,
the shared ValueLabel, the one unit it is compared in, the readout piece, the
documents that should support it (each an evidence reader in evidence.py,
named with the checklist row it comes from), and what to ask for when nothing
does. The checklist rows are docs/ongoing/checklist.csv; the document guides
behind them are docs/reports/20261022.03_document_guides/.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from scans.claims.numbers import Mention


@dataclass(frozen=True)
class Kind:
    name: str               # plain words for the table: "ARR", "runway"
    label: str              # schema ValueLabel
    unit: str | None        # schema Unit the claim is compared in; None for dates
    piece: str              # schema PieceName
    definition: str         # what the figure means once normalised
    evidence: tuple[str, ...] = ()   # evidence reader keys, evidence.py READERS
    ask_doc: str = ""       # the document that would back it, in founder words
    ask_row: str | None = None       # checklist row id for that document
    period: str = "as_of"   # as_of, plan, ltm, none
    expects: tuple[str, ...] = field(default=("number", "currency", "percent", "words"))


K = Kind
KINDS: dict[str, Kind] = {
    "as_of": K("data date", "other", None, "the_pitch_itself", "the date the room's figures are as of",
               ("model_date",), "the financial model with its data date", "C19", "none", ("date",)),
    "founded": K("year founded", "other", None, "team", "the year the company was founded",
                 ("bios_founded",), "founder bios", "C53", "none", ("year",)),
    "raise": K("round size", "raise_amount", "USD", "the_pitch_itself", "new money in this round",
               ("model_raise", "cap_new_money"), "the cap table with the round modelled", "C72", "none", ("currency", "words")),
    "pre_money": K("pre-money valuation", "pre_money", "USD", "the_pitch_itself", "valuation before the new money",
                   ("model_pre_money", "cap_pre_money"), "the cap table with the round modelled", "C72", "none", ("currency",)),
    "ownership_sold": K("ownership sold", "ownership", "percent", "the_pitch_itself", "share of the company the new money buys",
                        ("cap_ownership",), "the cap table with the round modelled", "C72", "none", ("percent",)),
    "use_of_funds": K("use of funds", "other", "USD", "the_pitch_itself", "planned spend of the new money on one line",
                      (), "a use-of-funds plan tied to the financial model", "C19", "none", ("currency",)),
    "use_of_funds_share": K("use of funds share", "other", "percent", "the_pitch_itself", "share of the new money for one line",
                            (), "a use-of-funds plan tied to the financial model", "C19", "none", ("percent",)),
    "arr": K("ARR", "arr", "USD_per_year", "traction_and_revenue", "annual recurring revenue, 12 times the month's recurring revenue",
             ("model_arr", "metrics_arr", "customers_arr"), "monthly revenue by customer", "C03", "as_of", ("currency", "words")),
    "mrr": K("MRR", "mrr", "USD_per_month", "traction_and_revenue", "recurring revenue for one month",
             ("model_mrr", "metrics_mrr", "customers_mrr"), "monthly revenue by customer", "C03", "as_of", ("currency",)),
    "revenue_ltm": K("revenue, last 12 months", "other", "USD", "traction_and_revenue", "total revenue over the 12 months to the data date",
                     ("metrics_revenue_ltm",), "the monthly P&L for the last 12 months", "C20", "ltm", ("currency",)),
    "chart_range": K("chart months", "other", None, "traction_and_revenue", "the months a revenue chart shows",
                     ("metrics_range",), "the metrics export for every month", "C02", "none", ("range",)),
    "grew_every_month": K("growth every month", "other", None, "traction_and_revenue", "revenue rose in every month of the year",
                          ("metrics_grew",), "the metrics export for every month", "C02", "none", ("year",)),
    "first_revenue": K("first month of revenue", "other", None, "traction_and_revenue", "the first month with revenue",
                       ("metrics_first",), "the metrics export from the first month", "C02", "none", ("month",)),
    "customers_now": K("paying customers", "paying_accounts", "accounts", "customers", "customers paying in the data month",
                       ("metrics_paying", "model_paying", "customers_count_now"), "monthly revenue by customer", "C03", "as_of",
                       ("number", "words")),
    "customers_ever": K("customers ever", "other", "accounts", "retention", "customers who have ever paid",
                        ("customers_count_ever",), "monthly revenue by customer", "C03", "as_of", ("number", "words")),
    "calls_month": K("calls handled", "other", "count", "traction_and_revenue", "calls handled in the month",
                     ("metrics_calls",), "the metrics export", "C02", "as_of", ("number",)),
    "invoices_month": K("invoices audited, month", "other", "count", "traction_and_revenue", "carrier invoices audited in the month",
                        ("metrics_invoices", "customers_invoices"), "the metrics export", "C02", "as_of", ("number",)),
    "invoices_total": K("invoices audited, since launch", "other", "count", "traction_and_revenue", "carrier invoices audited since launch",
                        ("metrics_invoices_total",), "the metrics export", "C02", "as_of", ("number",)),
    "largest_customer_share": K("largest customer share", "largest_customer_share", "percent", "customers",
                                "the largest customer's share of the month's revenue",
                                ("customers_largest_share", "model_largest_share"), "monthly revenue by customer", "C03", "as_of",
                                ("percent", "words")),
    "customer_locations": K("locations of a customer", "other", "count", "customers", "locations a named customer runs it in",
                            ("contract_number", "customers_locations"), "the customer's signed contract", "C34", "as_of",
                            ("number", "words")),
    "contract_term": K("contract term", "contract_term", "months", "customers", "length of a named customer's contract",
                       ("contract_term",), "the customer's signed contract", "C34", "none", ("number",)),
    "customer_date": K("customer contract date", "other", None, "customers", "a date in a named customer's contract",
                       ("contract_date",), "the customer's signed contract", "C34", "none", ("date", "month")),
    "gross_margin": K("gross margin", "gross_margin", "percent", "unit_economics", "revenue less cost of revenue, as a share of revenue",
                      ("model_gross_margin",), "the expense ledger by function", "C23", "as_of", ("percent",)),
    "cost_share": K("cost as a share of revenue", "other", "percent", "unit_economics", "one cost line as a share of revenue",
                    ("model_cost_share",), "the expense ledger by function", "C23", "as_of", ("percent",)),
    "nrr": K("net revenue retention", "nrr_12m", "percent", "retention", "12-month net revenue retention of the cohorts",
             ("model_nrr",), "a cohort export built from revenue by customer", "C14", "as_of", ("percent", "words")),
    "cohort_count": K("cohorts", "other", "count", "retention", "how many cohorts the retention figure covers",
                      (), "a cohort export built from revenue by customer", "C14", "none", ("words", "number", "range")),
    "price": K("list price", "price", "USD_per_month", "unit_economics", "list price of one plan, a month",
               ("contract_list_price",), "signed order forms that show the list price", "C34", "none", ("currency",)),
    "onboarding_fee": K("onboarding fee", "other", "USD", "unit_economics", "one-time fee for a new customer",
                        ("contract_onboarding_fee",), "signed order forms", "C34", "none", ("currency",)),
    "annual_discount": K("annual plan discount", "other", "percent", "unit_economics", "discount for paying a year ahead",
                         ("contract_discount",), "signed order forms", "C34", "none", ("percent",)),
    "recovery_fee": K("recovery fee", "other", "percent", "unit_economics", "share of recovered money the company keeps",
                      ("model_recovery_fee", "contract_recovery_fee"), "signed customer contracts", "C34", "none",
                      ("percent", "number")),
    "plan_limit": K("plan limit", "other", "count", "unit_economics", "a limit written into a price plan",
                    (), "signed order forms that show the plan's terms", "C34", "none", ("number", "words")),
    "market_count": K("market count", "other", "count", "market", "how many buyers the market estimate counts",
                      ("model_market_count",), "a market sizing with its sources", "C47", "none", ("number",)),
    "market_acv": K("market price per buyer", "acv", "USD_per_year", "market", "what one buyer pays a year in the market estimate",
                    ("model_market_acv",), "a market sizing with its sources", "C47", "none", ("currency",)),
    "tam": K("market size", "tam", "USD", "market", "the market size the company estimates",
             ("model_tam",), "a market sizing with its sources", "C47", "none", ("currency",)),
    "runway": K("runway", "runway_months", "months", "burn_and_runway", "months of cash from the data date, in the plan",
                ("model_runway",), "bank statements and the current burn", "C21", "plan", ("number", "words")),
    "net_burn": K("average net burn", "net_burn_monthly", "USD_per_month", "burn_and_runway", "average monthly net burn over the plan's first 12 months",
                  ("model_net_burn",), "bank statements and the current burn", "C21", "plan", ("currency",)),
    "growth_plan": K("planned growth", "other", "percent", "burn_and_runway", "revenue growth a month in the plan",
                     ("model_growth",), "the financial model", "C19", "plan", ("percent",)),
    "hires_planned": K("planned hires", "hires", "count", "team", "people the plan hires",
                       ("hiring_count", "model_hires", "team_hires"), "the hiring plan", "C22", "plan", ("number", "words")),
    "hires_dept": K("planned hires by department", "hires", "count", "team", "planned hires in one department",
                    ("hiring_dept",), "the hiring plan", "C22", "plan", ("number",)),
    "headcount_now": K("staff today", "headcount", "count", "team", "people employed at the data date",
                       ("model_staff_now",), "an org chart with start dates", "C54", "as_of", ("number", "words")),
    "headcount_after": K("staff after hiring", "headcount", "count", "team", "people employed after the planned hires",
                         ("hiring_last_headcount", "model_staff_after"), "the hiring plan", "C22", "plan", ("number",)),
    "founder_years": K("founder experience", "other", "count", "team", "years a founder spent in a past role",
                       ("bios_years",), "founder bios", "C53", "none", ("words", "number")),
    "other": K("other figure", "other", None, "the_pitch_itself", "a figure the scan has no rule for",
               (), "the document behind this figure", None, "none",
               ("number", "currency", "percent", "words", "date", "month", "year", "range")),
}

DEPARTMENTS = ("engineering", "sales", "customer success", "support", "marketing", "g&a")
_NAMED = re.compile(r"\b([A-Z][a-z]+(?:\s+(?:&\s+)?[A-Z][a-z]+)+)\b")


def named_entities(text: str) -> list[str]:
    """Capitalised multi-word names in a sentence: 'Cedar & Pine Animal Hospitals', 'Corvane Logistics'."""
    skip = {"Hollis Voice", "Series A", "United States", "New York", "Deal Flow", "Use Of"}
    return [n for n in _NAMED.findall(text) if n not in skip and not n.startswith(("Our ", "The ", "We "))]


def _has(text: str, *words: str) -> bool:
    return any(re.search(w, text) for w in words)


def classify(m: Mention, local: str, sentence: str, role: str | None = None) -> str:
    """The kind of one figure. `local` is the text from the previous figure to the next,
    `sentence` the whole sentence (or the big number's label line), both lower case.
    `role` is "part" or "whole" for "X of the Y", "from" or "to" for "from X to Y"."""
    h, uw = m.kind_hint, (m.unit_word or "")
    s, loc = sentence, local

    if h == "date" and (_has(s, r"as of") or _has(s, r"runway") and _has(loc, r"from")):
        return "as_of"
    if h == "year" and _has(loc + s, r"founded"):
        return "founded"
    if h == "year" and _has(s, r"grew every month", r"grown every month"):
        return "grew_every_month"
    if h == "range":
        if _has(s, r"cohort"):
            return "cohort_count"
        if _has(s, r"revenue", r"chart"):
            return "chart_range"
    if h == "month" and _has(s, r"started charging", r"first revenue", r"first invoice"):
        return "first_revenue"

    if h == "percent" or m.unit == "percent":
        if _has(s, r"pre-money") and _has(loc, r"of the company"):
            return "ownership_sold"
        if _has(s, r"use of funds") or re.match(r"^\s*\(", loc) or _has(s, r"^(engineering|sales|customer success|general)[^:]*:"):
            return "use_of_funds_share"
        if _has(s, r"largest customer", r"biggest customer", r"no customer above") or _has(loc, r"of (arr|subscription revenue)"):
            return "largest_customer_share"
        if _has(s, r"phone minutes", r"licen[cs]es?", r"telephony"):
            return "cost_share"
        if _has(s, r"gross margin"):
            return "gross_margin"
        if _has(s, r"net revenue retention", r"\bnrr\b"):
            return "nrr"
        if _has(s, r"recover"):
            return "recovery_fee"
        if _has(loc + s, r"% off", r"\d+% less", r"percent less", r"pay a year in", r"annual plans"):
            return "annual_discount"
        if _has(s, r"grows", r"growth") and _has(s, r"a month"):
            return "growth_plan"
    if h in ("currency", "words") and m.unit == "USD" or h == "currency":
        if _has(s, r"pre-money"):
            return "pre_money"
        if _has(s, r"use of funds") or _has(s, r"^(engineering|sales and marketing|sales|customer success[^:]*|general and administrative)\s*:"):
            return "use_of_funds"
        if _has(s, r"onboarding fee"):
            return "onboarding_fee"
        if _has(s, r"\barr\b", r"annual recurring revenue"):
            return "arr"
        if _has(s, r"\bmrr\b", r"monthly recurring revenue,? september"):
            return "mrr"
        if _has(s, r"last 12 months", r"last twelve months"):
            return "revenue_ltm"
        if _has(s, r"net burn"):
            return "net_burn"
        if re.search(re.escape(m.printed.lower()) + r"\s+a year per", loc) or _has(s, r"would pay a year"):
            return "market_acv"
        if _has(s, r"market size", r"market near", r"a market of"):
            return "tam"
        if _has(s, r"series a", r"seed raise", r"\braising\b", r"^seed\s*\|", r"seed round", r"\bseed\b"):
            return "raise"
        if _has(s, r"a month", r"plans start", r"starter|standard|\bpro\b|\blane\b|\bfleet\b", r"custom"):
            return "price"
    if h in ("number", "words"):
        if role == "whole" and _has(s, r"paid", r"customers?", r"brokers?", r"clinics?"):
            return "customers_ever"
        if role == "part" and _has(s, r"paid", r"paying", r"still"):
            return "customers_now"
        if role == "from" and _has(s, r"(staff|team|headcount|employees) grows"):
            return "headcount_now"
        if role == "to" and _has(s, r"(staff|team|headcount|employees) grows"):
            return "headcount_after"
        if uw in ("hires", "hire"):
            return "hires_planned"
        if uw in ("months", "month", "years", "year") and _has(s, r"runway"):
            return "runway"
        if uw in ("months", "month") and _has(s, r"agreement", r"contract", r"term"):
            return "contract_term"
        if uw in ("years", "year"):
            return "founder_years"
        if _has(s, r"hires?\b", r"\bhire\b", r"to hire") and not _has(s, r"employees after", r"staff after"):
            return "hires_planned"
        if _has(s, r"^(engineering|sales|customer success|support|marketing|g&a)\s*:"):
            return "hires_dept"
        if _has(s, r"employees after", r"staff after", r"after the seed hires", r"after hiring"):
            return "headcount_after"
        if _has(s, r"people today", r"employees today", r"people work", r"full-time (people|employees)", r"staff today"):
            return "headcount_now"
        if _has(s, r"clinics on", r"paying", r"pay us today", r"brokers pay", r"active clinics"):
            return "customers_now"
        if _has(s, r"calls handled"):
            return "calls_month"
        if _has(s, r"since launch"):
            return "invoices_total"
        if _has(s, r"invoices audited"):
            return "invoices_month"
        if uw in ("locations", "location") and _has(s, r"up to", r"one location"):
            return "plan_limit"
        if uw in ("locations", "location") or _has(loc, r"locations"):
            return "customer_locations"
        if _has(s, r"cohorts"):
            return "cohort_count"
        if _has(s, r"clinics in the united states", r"freight brokers with", r"independent (veterinary )?clinics", r"us freight brokers"):
            return "market_count"
        if _has(s, r"recover"):
            return "recovery_fee"
    return "other"


def classify_with_entities(m: Mention, local: str, sentence: str, original: str, role: str | None = None) -> str:
    """classify, plus the one rule that needs capital letters: a date in a sentence that
    names a customer is a contract date."""
    if m.kind_hint in ("date", "month") and not re.search(r"as of|started charging|first", sentence):
        if named_entities(original):
            return "customer_date"
    return classify(m, local, sentence, role)
