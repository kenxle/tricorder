"""Contract terms in full: FRAMEWORKS.md entry 1.13, the parts built before Saturday.

    check 1  cancellable_within_notice_vs_arr   a customer who can leave within short_notice_days
                                                is counted as a year of ARR
    check 3  plan_revenue_past_term_end         the plan keeps a contract's revenue after its term ends
    check 4  signed_not_live_vs_revenue         revenue counted before a contract or amendment starts
    check 6  counted_line_without_contract      a counted line has no contract in the room (gaps)
    clause_notes                                exclusivity, most-favoured-customer, change of control,
                                                and the other clauses that change what a customer
                                                pays or when it can leave (checklist row C172)

Checks 2 and 5 and the model reading are Saturday's, in `contract_terms.py`
(the contract-terms-saturday slice). Check 1 is here because this slice's Done
when needs it; Saturday's module must not write it again. Both modules read the
contracts through `contract_reader.read_room`, which reads each contract once.

Contracts are read by script (contract_reader). The counting side (the customer
file, the model's ARR build, P&L plan columns and Assumptions) is read cell by
cell through schema.readers. No language model is called here, so every claim is
"computed" or "quoted", and every number is this script's arithmetic.

Design: docs/features/20261023.04_contract_terms/04_architecture.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

from schema import settings
from schema.claim import Check, Claim, Gap, Panel, Source, Value
from schema.readers import csv_row_text, csv_rows, xlsx_sheet, xlsx_sheet_names
from scans.base import Ids, gap
from scans.redflags.contract_reader import CLAUSE_FIELDS, ContractTerms, RoomContracts, Term, read_room

P1, P3, P4, P6 = ("cancellable_within_notice_vs_arr", "plan_revenue_past_term_end", "signed_not_live_vs_revenue",
                  "counted_line_without_contract")
CLAUSES = "clause_notes"
SCAN = "redflags"
HOW = "scans/redflags/contract_terms_full.py"
CUSTOMER_FILES = ("03_metrics/customer_mrr_by_month.csv", "03_metrics/revenue_by_customer.csv")
MODEL = "02_financials/financial_model.xlsx"
METRICS = "03_metrics/monthly_metrics.csv"
CLAUSE_WORDS = {"exclusivity": "exclusivity", "most_favoured_customer": "most-favoured-customer",
                "change_of_control": "change-of-control"}

NO_COUNTING = "Not in the room: the ARR build or the customer file to compare with"


def money(x: float) -> str:
    return f"${x:,.0f}"


def pct(x: float, places: int = 1) -> str:
    return f"{100 * x:.{places}f}%"


def name_key(name: str) -> str:
    """FRAMEWORKS 1.13: lowercase, join "&" and "and", remove punctuation."""
    s = name.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return " ".join(s.split())


def _d(s: str) -> date:
    return date.fromisoformat(s)


def _add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    last = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, last))


# --------------------------------------------------------------------------- the counting side


@dataclass
class CustRow:
    file_row: int
    month: str
    name: str
    product_type: str
    mrr: float


@dataclass
class Counting:
    room: Path
    customers: str | None = None
    rows: list[CustRow] = field(default_factory=list)
    as_of: str | None = None
    as_of_src: Source | None = None
    pnl_plan: list[tuple[str, str, float]] = field(default_factory=list)  # (month, cell, value)
    plan_row_label: str | None = None
    start: tuple[str, float] | None = None  # (cell, value): the plan's starting figure
    non_renewal_rate: bool = False
    arr_lines: list[dict] = field(default_factory=list)

    # -- customer file
    def months(self) -> list[str]:
        return sorted({r.month for r in self.rows})

    def rows_for(self, key: str) -> list[CustRow]:
        return [r for r in self.rows if name_key(r.name) == key]

    def counted(self, key: str) -> tuple[float, list[CustRow]]:
        """counted_mrr(c): MRR in the as-of month, product types other than Onboarding."""
        month = (self.as_of or "")[:7]
        hit = [r for r in self.rows_for(key) if r.month == month and r.product_type.lower() != "onboarding" and r.mrr > 0]
        return sum(r.mrr for r in hit), hit

    def src_row(self, r: CustRow) -> Source:
        return Source(kind="file", uri=self.customers, locator=f"row {r.file_row}",
                      quote=csv_row_text(self.room / self.customers, r.file_row))

    def src_cell(self, cell: str, value) -> Source:
        return Source(kind="file", uri=MODEL, locator=cell, quote=str(value))

    def arr_line_for(self, key: str) -> dict | None:
        """The customer's ARR_Build line: a line naming it, or the cohort whose quarter holds its first
        subscription month (FRAMEWORKS 1.13, "Mechanical check")."""
        for line in self.arr_lines:
            if key and key in name_key(line["label"]):
                return line
        subs = sorted(r.month for r in self.rows_for(key) if r.product_type.lower() == "subscription" and r.mrr > 0)
        if not subs:
            return None
        y, m = subs[0].split("-")
        q = f"{y} Q{(int(m) - 1) // 3 + 1}"
        return next((ln for ln in self.arr_lines if q in ln["label"]), None)


def recurring_count(cnt: "Counting", key: str) -> tuple[bool, list[Source], str]:
    """Whether the counting side counts this customer as recurring revenue, with the row that shows it.

    With an ARR build, only a line for the customer or its cohort counts (FRAMEWORKS 1.13, "Mechanical
    check"); a customer file row alone does not, because the clean room lists the pilot there and leaves
    it out of ARR. With no ARR build, the customer file's subscription rows are the counting.
    A check says a contract is counted only when this returns True (review wave 2a, B1)."""
    if cnt.arr_lines:
        line = cnt.arr_line_for(key)
        if line is None:
            return False, [], "the ARR build"
        return True, [cnt.src_cell(f"ARR_Build!E{line['row']}", line["arr"])], f"the ARR build line '{line['label']}'"
    _mrr, rows = cnt.counted(key)
    subs = [r for r in rows if r.product_type.lower() == "subscription"]
    return bool(subs), [], "the customer file's subscription rows"


def _col(i: int) -> str:
    from openpyxl.utils import get_column_letter

    return get_column_letter(i + 1)


def load_counting(room: Path) -> Counting:
    c = Counting(room=room)
    for rel in CUSTOMER_FILES:
        if (room / rel).exists():
            c.customers = rel
            data = csv_rows(room / rel)
            col = "mrr" if data and "mrr" in data[0] else "subscription_revenue"
            for i, r in enumerate(data, start=2):
                try:
                    v = float(r.get(col) or 0)
                except ValueError:
                    v = 0.0
                c.rows.append(CustRow(i, r.get("month", ""), r.get("customer_name", ""),
                                      r.get("product_type") or "Subscription", v))
            break
    model = room / MODEL
    if model.exists():
        sheets = xlsx_sheet_names(model)
        if "Assumptions" in sheets:
            for i, r in enumerate(xlsx_sheet(model, "Assumptions"), start=1):
                label = str(r[0] or "")
                if label.lower() == "data date" and r[1]:
                    c.as_of, c.as_of_src = str(r[1])[:10], c.src_cell(f"Assumptions!B{i}", r[1])
                if re.search(r"recurring revenue in the last actual month", label, re.I) and isinstance(r[1], (int, float)):
                    c.start = (f"Assumptions!B{i}", float(r[1]))
                if re.search(r"non-renewal|churn|renewal rate|logo retention", label, re.I):
                    c.non_renewal_rate = True
        if "P&L" in sheets:
            rows = xlsx_sheet(model, "P&L")
            hdr = next((i for i, r in enumerate(rows[:15]) if r and r[0] == "Line"), None)
            if hdr is not None and hdr + 1 < len(rows):
                months, kinds = rows[hdr], rows[hdr + 1]
                line = next((i for i, r in enumerate(rows) if str(r[0] or "").startswith("Recurring revenue")), None)
                if line is None:
                    line = next((i for i, r in enumerate(rows) if str(r[0] or "") == "Subscription revenue"), None)
                if line is not None:
                    c.plan_row_label = rows[line][0]
                    last_actual = None
                    for j in range(2, len(months)):
                        v = rows[line][j] if j < len(rows[line]) else None
                        if kinds[j] == "Plan" and isinstance(v, (int, float)):
                            c.pnl_plan.append((str(months[j]), f"P&L!{_col(j)}{line + 1}", float(v)))
                        elif kinds[j] == "Actual" and isinstance(v, (int, float)):
                            last_actual = (f"P&L!{_col(j)}{line + 1}", float(v))
                    if c.start is None and last_actual:
                        c.start = last_actual
        if "ARR_Build" in sheets:
            rows = xlsx_sheet(model, "ARR_Build")
            hdr = next((i for i, r in enumerate(rows[:15]) if r and r[0] == "Line"), None)
            if hdr is not None:
                for i in range(hdr + 1, len(rows)):
                    r = rows[i]
                    label = str(r[0] or "")
                    if not label or label.lower().startswith("arr total"):
                        break
                    # Subtotals ("Subscription ARR") and lines that count no ARR (onboarding) are not lines.
                    if re.search(r"\bARR\b|\btotal\b", label, re.I) or not isinstance(r[4], (int, float)) or r[4] <= 0:
                        continue
                    c.arr_lines.append({"row": i + 1, "label": label, "customers": r[2], "arr": r[4]})
    if c.as_of is None and c.rows:
        last = c.months()[-1]
        y, m = map(int, last.split("-"))
        c.as_of = (_add_months(date(y, m, 1), 1) - timedelta(days=1)).isoformat()
    return c


# --------------------------------------------------------------------------- claim helpers


@dataclass
class Out:
    ids: Ids
    claims: list[Claim] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    checks: list[list[str]] = field(default_factory=list)

    def claim(self, name: str, text: str, sources: list[Source], severity: str, confidence: str = "computed",
              value: Value | None = None) -> Claim:
        c = Claim(id=self.ids(), scan=SCAN, text=text, value=value, severity=severity,
                  check=Check(kind="script", name=name), confidence=confidence, sources=sources)
        self.claims.append(c)
        return c

    def gap(self, what: str, why: str, would_need: str, piece: str) -> None:
        g = gap(what, why, would_need, piece)
        if g.what not in {x.what for x in self.gaps}:
            self.gaps.append(g)

    def row(self, contract: ContractTerms, name: str, label: str, reason: str) -> None:
        self.checks.append([contract.uri, contract.label, name, label, reason])


def term_src(c: ContractTerms, t: Term) -> Source:
    return Source(kind="file", uri=c.uri, locator=t.locator(), quote=t.quote)


# --------------------------------------------------------------------------- the clauses


def clause_notes(c: ContractTerms, out: Out) -> None:
    missing = []
    for fld in CLAUSE_FIELDS:
        t: Term = getattr(c, fld)
        if t.stated:
            out.claim(CLAUSES, f"{c.label}: has a {CLAUSE_WORDS[fld]} clause, {t.locator()}.", [term_src(c, t)],
                      "info", "quoted")
        elif t.status == "not_stated":
            missing.append(CLAUSE_WORDS[fld])
    if missing:
        names = missing[0] if len(missing) == 1 else ", ".join(missing[:-1]) + " or " + missing[-1]
        pages = [Source(kind="file", uri=c.uri, locator=f"page {i}", quote=head)
                 for i, head in enumerate(c.page_heads, start=1) if head]
        out.claim(CLAUSES, f"{c.label}: no {names} clause. {HOW} read all {c.pages} pages for the wording of each.",
                  pages, "info")
    for oc in c.other_clauses:
        loc = f"page {oc.page}" + (f", clause {oc.clause}" if oc.clause else "")
        out.claim(CLAUSES, f"{c.label}: {oc.summary}, {loc}.",
                  [Source(kind="file", uri=c.uri, locator=loc, quote=oc.quote)], "info", "quoted")


# --------------------------------------------------------------------------- check 1


def earliest_exit(c: ContractTerms, as_of: date) -> tuple[date, str, list[Term]] | None:
    """FRAMEWORKS 1.13 earliest_exit, with the terms it rests on, or None when the terms do not say."""
    tfc, days = c.termination_for_convenience, c.convenience_notice_days
    if tfc.stated and tfc.value is True and days.stated:
        return as_of + timedelta(days=int(days.value)), f"either party may end it on {days.value} days notice", [days]
    if c.term_end_date.stated:
        end = _d(str(c.term_end_date.value))
        renews = c.auto_renews.stated and c.auto_renews.value is True
        why = [c.term_end_date] + ([tfc] if tfc.stated else [])
        if not renews:
            return end, "no right to end it without cause, and it ends at its term end", why
        notice = int(c.non_renewal_notice_days.value) if c.non_renewal_notice_days.stated else 0
        if end - timedelta(days=notice) > as_of:
            return end, "no right to end it without cause; the notice not to renew sets the exit at the term end", why
        months = int(c.renewal_months.value) if c.renewal_months.stated else 12
        return _add_months(end, months), "the day to give notice not to renew has passed, so it runs a renewal term", why
    return None


def check_1(c: ContractTerms, key: str, cnt: Counting, s: dict, out: Out) -> None:
    mrr, rows = cnt.counted(key)
    as_of = _d(cnt.as_of)
    ex = earliest_exit(c, as_of)
    if ex is None:
        out.row(c, P1, "cannot_check", "the contract states neither a right to end it nor a term end")
        return
    exit_day, why, terms = ex
    days = (exit_day - as_of).days
    counted_rec, count_srcs, where = recurring_count(cnt, key)
    srcs = [term_src(c, t) for t in terms] + [cnt.src_row(r) for r in rows] + count_srcs
    arr = 12 * mrr
    term_m = int(c.term_months.value) if c.term_months.stated else None
    month = cnt.as_of[:7]
    if mrr > 0 and not counted_rec:
        out.claim(P1, f"{c.label}: {why}; the earliest exit is {exit_day}, {days} days after {as_of}. The customer "
                      f"file lists {money(mrr)} MRR for it in {month}; {where} does not count it, so it is not "
                      f"counted as a year of ARR.", srcs, "info")
        out.row(c, P1, "clear", f"not in {where}")
    elif mrr > 0 and days < 0:
        out.claim(P1, f"{c.label}: the term ended {exit_day}, {-days} days before {as_of}, and the contract states no "
                      f"renewal, but {where} counts the customer as a year of ARR: {money(arr)} (12 x {money(mrr)} MRR in "
                      f"{month}).", srcs, "flag", value=Value(number=arr, unit="USD", label="other", period=month))
        out.row(c, P1, "flag", f"term ended {exit_day}, {money(arr)} counted")
    elif mrr > 0 and days <= s["short_notice_days"]:
        out.claim(P1, f"{c.label}: {why}, so the earliest exit is {exit_day}, {days} days after {as_of}, but "
                      f"{where} counts the customer as a year of ARR: {money(arr)} (12 x {money(mrr)} MRR in {month}). "
                      f"{HOW} worked the dates and the product.", srcs, "flag",
                  value=Value(number=arr, unit="USD", label="other", period=month))
        out.row(c, P1, "flag", f"{days} days to exit, {money(arr)} counted")
    elif mrr > 0 and term_m is not None and term_m < s["min_contract_months"]:
        out.claim(P1, f"{c.label}: the term is {term_m} months, under {s['min_contract_months']}, and {where} "
                      f"counts the customer as a year of ARR: {money(arr)}. The earliest exit is {exit_day}, {days} days after {as_of}.",
                  srcs, "watch", value=Value(number=arr, unit="USD", label="other", period=month))
        out.row(c, P1, "watch", f"term {term_m} months")
    else:
        counted = f"counted at {money(mrr)} MRR in {month}" if mrr > 0 else f"not counted in {month}"
        out.claim(P1, f"{c.label}: {why}; the earliest exit is {exit_day}, {days} days after {as_of}, "
                      f"beyond the {s['short_notice_days']}-day line. It is {counted}.", srcs, "info")
        out.row(c, P1, "clear", f"{days} days to exit")


# --------------------------------------------------------------------------- check 3


def check_3(c: ContractTerms, key: str, cnt: Counting, s: dict, out: Out) -> None:
    if not cnt.pnl_plan or cnt.start is None:
        out.gap("Not in the room: the P&L plan columns", "tab or row missing",
                "the financial model with monthly plan columns for recurring revenue", "traction_and_revenue")
        out.row(c, P3, "cannot_check", "no P&L plan columns")
        return
    if not c.term_end_date.stated:
        out.row(c, P3, "cannot_check", "the contract states no term end")
        return
    end = str(c.term_end_date.value)
    mrr, rows = cnt.counted(key)
    counted_rec, count_srcs, where = recurring_count(cnt, key)
    if mrr > 0 and not counted_rec:
        # The plan's starting figure is built from the counted lines; a customer they leave out
        # has no share of the plan to rest on the contract (review wave 2a, B1).
        out.claim(P3, f"{c.label}: the term ends {end}. The customer file lists {money(mrr)} MRR for it in "
                      f"{cnt.as_of[:7]}, but {where} does not count it, so no plan revenue is taken to rest on it.",
                  [term_src(c, c.term_end_date)] + [cnt.src_row(r) for r in rows], "info")
        out.row(c, P3, "clear", f"not in {where}")
        return
    start_cell, start = cnt.start
    share = mrr / start if start else 0.0
    plan = cnt.pnl_plan
    after = [(m, cell, v) for m, cell, v in plan if m > end[:7]]
    renews = c.auto_renews.stated and c.auto_renews.value is True
    resting = share * sum(v for _, _, v in after)
    srcs = [term_src(c, c.term_end_date)] + ([term_src(c, c.auto_renews)] if renews else []) \
        + [cnt.src_cell(start_cell, start)] + [cnt.src_row(r) for r in rows] + count_srcs
    window = f"{plan[0][0]} to {plan[-1][0]}"
    if not after:
        text = f"{c.label}: the term ends {end}, after the last plan month ({plan[-1][0]}), so no plan month rests on a renewal."
        if renews and c.non_renewal_notice_days.stated:
            last = _d(end) - timedelta(days=int(c.non_renewal_notice_days.value))
            if plan[0][0] <= last.isoformat()[:7] <= plan[-1][0]:
                text += f" The last day to give notice not to renew, {last}, falls inside the plan window ({window})."
                srcs.insert(1, term_src(c, c.non_renewal_notice_days))
        out.claim(P3, text, srcs, "info")
        out.row(c, P3, "clear", "term ends after the plan")
        return
    span = f"{after[0][0]} to {after[-1][0]}" if len(after) > 1 else after[0][0]
    n_after = f"{len(after)} plan month{'s' if len(after) != 1 else ''}"
    srcs += [cnt.src_cell(cell, v) for _, cell, v in after]
    rest = (f"{money(resting)} of plan revenue rests on it over those months, {money(share * after[0][2])} of it in "
            f"{after[0][0]}, at its {pct(share, 2 if share < 0.01 else 1)} share of the plan's starting {money(start)}. {HOW} summed the plan cells.")
    val = Value(number=round(resting, 2), unit="USD", label="other", period=span)
    if share <= s["match_tolerance"]:
        out.claim(P3, f"{c.label}: the term ends {end}, and {n_after} ({span}) {'comes' if len(after) == 1 else 'come'} after it"
                      f"{', resting on its automatic renewal' if renews else ''}. It is {pct(share, 2)} of the plan's "
                      f"starting figure, below the {pct(s['match_tolerance'], 0)} line. {rest}", srcs, "info", value=val)
        out.row(c, P3, "clear", f"{pct(share, 2)} of the plan")
    elif not renews:
        out.claim(P3, f"{c.label}: the term ends {end} with no renewal clause, and the plan keeps its revenue for "
                      f"{n_after} after it ({span}). {rest}", srcs, "flag", value=val)
        out.row(c, P3, "flag", f"no renewal; {n_after}")
    elif not cnt.non_renewal_rate:
        out.claim(P3, f"{c.label}: the term ends {end} and renews by itself unless a party gives notice; the plan "
                      f"keeps its revenue for {len(after)} plan months after it ({span}) and states no non-renewal "
                      f"rate. {rest}", srcs, "watch", value=val)
        out.row(c, P3, "watch", f"auto-renewal treated as certain; {n_after}")
    else:
        out.claim(P3, f"{c.label}: the term ends {end} and renews by itself; the plan states a non-renewal rate for "
                      f"the {len(after)} months after it ({span}).", srcs, "info")
        out.row(c, P3, "clear", "plan states a non-renewal rate")


# --------------------------------------------------------------------------- check 4


def _monthly(amount: float, per: str) -> float | None:
    return amount if per == "month" else amount / 12 if per == "year" else None


def check_4(c: ContractTerms, key: str, cnt: Counting, s: dict, out: Out) -> None:
    rows = [r for r in cnt.rows_for(key) if r.product_type.lower() != "onboarding" and r.mrr > 0]
    if not c.effective_date.stated:
        out.row(c, P4, "cannot_check", "the contract states no effective date")
        return
    if not rows:
        out.row(c, P4, "clear", "no MRR counted for the customer")
        return
    live = str(c.effective_date.value)
    first = min(rows, key=lambda r: r.month)
    tol = s["match_tolerance"]
    src_c = term_src(c, c.effective_date)
    if first.month < live[:7]:
        out.claim(P4, f"{c.label}: effective {live}, but the customer file counts {money(first.mrr)} of MRR from "
                      f"{first.month}, before the contract starts.", [src_c, cnt.src_row(first)], "flag",
                  value=Value(number=first.mrr, unit="USD_per_month", label="other", period=first.month))
        out.row(c, P4, "flag", f"counted from {first.month}, live from {live[:7]}")
        return
    steps = sorted((f for f in c.fee_schedule if f.from_date and f.from_date[:7] > live[:7]), key=lambda f: f.from_date)
    for f in steps:
        new = _monthly(f.amount_usd, f.per)
        if new is None:
            continue
        early = [r for r in rows if r.month < f.from_date[:7] and abs(r.mrr - new) <= tol * new]
        fsrc = Source(kind="file", uri=c.uri, locator=f"page {f.page}", quote=f.quote)
        if early:
            r = early[0]
            out.claim(P4, f"{c.label}: the fee of {money(new)} a month takes effect {f.from_date}, but the customer "
                          f"file already counts {money(r.mrr)} in {r.month}.", [fsrc, cnt.src_row(r)], "flag",
                      value=Value(number=r.mrr, unit="USD_per_month", label="other", period=r.month))
            out.row(c, P4, "flag", f"fee change counted from {r.month}")
            return
    text = f"{c.label}: effective {live}; the customer file's first month with MRR is {first.month}."
    srcs = [src_c, cnt.src_row(first)]
    for f in steps:
        new = _monthly(f.amount_usd, f.per)
        step_row = next((r for r in sorted(rows, key=lambda r: r.month) if r.month >= f.from_date[:7]), None)
        before = [r for r in rows if r.month < f.from_date[:7]]
        if new and step_row and before:
            prev = max(before, key=lambda r: r.month)
            text += (f" The change from {f.from_date} takes effect in the file in {step_row.month}: "
                     f"{money(prev.mrr)} in {prev.month}, {money(step_row.mrr)} in {step_row.month}.")
            srcs += [Source(kind="file", uri=c.uri, locator=f"page {f.page}", quote=f.quote),
                     cnt.src_row(prev), cnt.src_row(step_row)]
            break
    out.claim(P4, text, srcs, "info")
    out.row(c, P4, "clear", "counted from the month it starts")


# --------------------------------------------------------------------------- check 6


def _ask(who: str) -> str:
    return (f"Please send the current customer contract language, the signed order form or agreement with any "
            f"amendments, for {who}.")


def check_6(customers: list[tuple[ContractTerms, str]], cnt: Counting, out: Out) -> None:
    have = {key for _, key in customers}
    month = cnt.as_of[:7]
    if cnt.arr_lines:
        for line in cnt.arr_lines:
            inside = [k for k in have if (cnt.arr_line_for(k) or {}).get("row") == line["row"]]
            n = int(line["customers"]) if isinstance(line["customers"], (int, float)) else None
            if n is not None and len(inside) >= n:
                continue
            count = f"{n} customers" if n is not None else "its customers"
            what = f"Not in the room: the contract for {line['label']} ({count})"
            if inside:
                what = what[:-1] + f", {len(inside)} of them with a contract in the room)"
            out.gap(what, "file missing", _ask(f"the {count} in the ARR build line '{line['label']}'"), "customers")
    else:
        counted = {}
        for r in cnt.rows:
            if r.month == month and r.product_type.lower() != "onboarding" and r.mrr > 0:
                counted.setdefault(name_key(r.name), r.name)
        lacking = sorted(v for k, v in counted.items() if k not in have)
        if lacking:
            out.gap(f"Not in the room: the contracts for {len(lacking)} of {len(counted)} customers counted in {month}",
                    "file missing", _ask("each of: " + "; ".join(lacking)), "customers")
    # Coverage: how much of the counted MRR rests on paper the room holds.
    covered, srcs, n_cov = 0.0, [], 0
    for _c, key in customers:
        if not recurring_count(cnt, key)[0]:
            continue  # a customer the counting leaves out is not part of the counted MRR it covers
        mrr, rows = cnt.counted(key)
        covered += mrr
        n_cov += 1
        srcs += [cnt.src_row(r) for r in rows]
    total, total_src = None, None
    if (cnt.room / METRICS).exists():
        for i, r in enumerate(csv_rows(cnt.room / METRICS), start=2):
            if r.get("month") == month and r.get("mrr"):
                total = float(r["mrr"])
                total_src = Source(kind="file", uri=METRICS, locator=f"row {i}", quote=csv_row_text(cnt.room / METRICS, i))
    if total is None:
        total = sum(r.mrr for r in cnt.rows if r.month == month and r.product_type.lower() != "onboarding")
        where = f"the customer file's {month} rows"
    else:
        where = f"monthly_metrics.csv for {month}"
    if total and srcs:
        share = covered / total
        out.claim(P6, f"Contracts in the room cover {money(covered)} of the {money(total)} counted MRR in {month} "
                      f"({pct(share)}), from {where}. {HOW} summed the customer file's rows for the "
                      f"{n_cov} counted customers with a contract.", ([total_src] if total_src else []) + srcs, "info",
                  value=Value(number=round(100 * share, 1), unit="percent", label="other", period=month))


# --------------------------------------------------------------------------- the entry


def terms_panel(contracts: list[ContractTerms]) -> Panel:
    rows = []
    for c in contracts:
        for fld, t in c.terms().items():
            rows.append([c.uri, fld, t.status, "" if t.value is None else str(t.value),
                         "" if t.page is None else str(t.page), t.quote or ""])
        for oc in c.other_clauses:
            rows.append([c.uri, f"other_clause: {oc.name}", "stated", oc.summary, str(oc.page), oc.quote])
        for a in c.amendments:
            rows.append([c.uri, f"amendment: {a.name}", "stated", a.effective_date or "", str(a.page), a.quote])
        rows.append([c.uri, "counterparty", "stated", c.counterparty, "1", c.customer_name.quote or ""])
        rows.append([c.uri, "read_by", "stated", c.read_by, "", ""])
    return Panel(name="contract terms", columns=["contract", "field", "status", "value", "page", "quote"], rows=rows)


def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap], list[Panel]]:
    room = Path(room)
    s = settings.load()
    out = Out(ids=ids)
    reading: RoomContracts = read_room(room)
    out.gaps += reading.gaps
    if not reading.contracts:
        if not reading.gaps:
            out.gap("Not in the room: customer contracts", "file missing",
                    "the signed customer contracts and order forms, with any amendments", "customers")
        return out.claims, out.gaps, []

    for c in reading.contracts:
        clause_notes(c, out)

    cnt = load_counting(room)
    customers = [c for c in reading.contracts if c.counterparty == "customer"]
    if not cnt.rows or cnt.as_of is None:
        out.gap(NO_COUNTING, "file missing",
                "the monthly revenue by customer file and the financial model with its ARR build and P&L plan",
                "traction_and_revenue")
        for c in customers:
            for name in (P1, P3, P4):
                out.row(c, name, "cannot_check", "no customer file to compare with")
    else:
        matched = []
        known = {name_key(r.name) for r in cnt.rows}
        for c in customers:
            key = name_key(c.name)
            if key not in known:
                out.gap(f"Not in the room: a customer row for {c.name}", "no row in the customer file names this customer",
                        f"the customer file with a row for {c.name}", "customers")
                for name in (P1, P3, P4):
                    out.row(c, name, "cannot_check", "no customer row")
                continue
            matched.append((c, key))
            for fn in (check_1, check_3, check_4):
                try:
                    fn(c, key, cnt, s, out)
                except Exception as err:  # noqa: BLE001 - one contract's bad cell never stops the rest
                    out.gap(f"Not in the room: a readable term for {fn.__name__.replace('_', ' ')} in {c.label}",
                            f"{type(err).__name__}: {err}", f"a clear copy of {c.uri}", "traction_and_revenue")
        check_6(matched, cnt, out)

    panels = [terms_panel(reading.contracts),
              Panel(name="contract checks", columns=["contract", "label", "check", "result", "reason"], rows=out.checks)]
    return out.claims, out.gaps, panels
