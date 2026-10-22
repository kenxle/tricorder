"""Accounting mislabels: FRAMEWORKS.md entry 1.12, the sub-checks the Saturday engine does not run.

A mislabel is a number filed under a label it does not earn. Entries 1.2 and 1.7
own kinds a (the ARR side) and d. This module runs the rest, scripts only:

    a  mrr_column_vs_subscription_rows         the `mrr` column holds non-subscription money
    b  billings_vs_recognised_revenue          revenue is really cash invoiced
    c  gross_vs_net_revenue                    revenue includes money passed on to others
    e  contractor_spend_vs_headcount_and_burn  contractors outside the P&L, or cut from the plan
    f  capitalised_spend_vs_pnl_and_cash       spend recorded as an asset, off the P&L
    g  deferred_revenue_vs_earned              cash for service not yet delivered counted as earned
    h  one_time_fees_in_recurring_metrics      a setup fee inside MRR or ARR

Each sub-check ends in one outcome: flag, watch, clear, cannot_check or not_run.
A flag or watch writes claims; a clear writes one info claim with its tie-out; a
cannot_check or not_run writes a gap. Kinds e and g carry tests that extend
entry 1.12 (docs/features/20261022.12_accounting_mislabels/proposed_frameworks_changes.md).

"The model" in a fallback below is the company's financial model workbook, read
cell by cell. No language model is called, so every claim is "computed".

Design: docs/features/20261022.12_accounting_mislabels/04_architecture.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from openpyxl.utils import get_column_letter

from schema import settings
from schema.claim import Check, Claim, Gap, Panel, Source, Value
from schema.readers import csv_row_text, csv_rows, xlsx_cell, xlsx_defined_name, xlsx_sheet
from scans.base import Ids, find, gap, now_iso

MODEL = "02_financials/financial_model.xlsx"
METRICS = "03_metrics/monthly_metrics.csv"
LEDGER = "02_financials/expense_ledger.csv"
HOLLIS_CUST = "03_metrics/customer_mrr_by_month.csv"
BRASS_CUST = "03_metrics/revenue_by_customer.csv"

A, B, C = "mrr_column_vs_subscription_rows", "billings_vs_recognised_revenue", "gross_vs_net_revenue"
E, F, G, H = ("contractor_spend_vs_headcount_and_burn", "capitalised_spend_vs_pnl_and_cash",
              "deferred_revenue_vs_earned", "one_time_fees_in_recurring_metrics")
ORDER = [("a", A), ("b", B), ("c", C), ("e", E), ("f", F), ("g", G), ("h", H)]

KIND_TEXT = {
    A: "Mislabel kind a: non-recurring revenue in MRR.",
    B: "Mislabel kind b: billings shown as revenue.",
    C: "Mislabel kind c: pass-through money shown as revenue.",
    E: "Mislabel kind e: contractors left out of burn.",
    F: "Mislabel kind f: capitalised costs off the P&L.",
    G: "Mislabel kind g: deferred revenue counted as earned.",
    H: "Mislabel kind h: one-time fees in recurring metrics.",
}
PIECE = {A: "traction_and_revenue", B: "traction_and_revenue", C: "traction_and_revenue",
         E: "burn_and_runway", F: "burn_and_runway", G: "traction_and_revenue", H: "traction_and_revenue"}
LABEL_CLAIMED = {A: "MRR", B: "Revenue", C: "Revenue", E: "Headcount, burn", F: "Expense, burn",
                 G: "Revenue, ARR", H: "MRR, ARR"}

CONTRACTOR_RE = re.compile(r"\b(contractors?|consultants?|consulting|freelance|freelancers?|agency|staffing|"
                           r"contract engineering|statement of work|sow)\b", re.I)
ASSET_RE = re.compile(r"(capitali[sz]ed|asset|balance sheet|prepaid)", re.I)
PASS_TYPE_RE = re.compile(r"(resale|pass.?through|reimburs)", re.I)
PASS_COL_RE = re.compile(r"(remitted|pass.?through|paid_to_customer|on_behalf)", re.I)
PASS_LEDGER_RE = re.compile(r"(remittance|resale|pass.?through|at cost)", re.I)
MONTH_RE = re.compile(r"\d{4}-\d{2}$")

ORDER_RANK = {"flag": 3, "watch": 2, "clear": 1, "cannot_check": 0, "not_run": 0}


class Missing(Exception):
    """An input this sub-check needs is not in the room. Becomes a gap."""

    def __init__(self, what: str, why: str, would_need: str):
        super().__init__(what)
        self.what, self.why, self.would_need = what, why, would_need


# --------------------------------------------------------------------------- formatting


def money(x: float) -> str:
    sign = "-" if x < 0 else ""
    x = abs(x)
    return sign + (f"${x:,.0f}" if abs(x - round(x)) < 0.005 else f"${x:,.2f}")


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def num(v) -> float:
    if v is None or v == "":
        return 0.0
    return float(v)


# --------------------------------------------------------------------------- the room


@dataclass(frozen=True)
class Layout:
    customers: str | None
    revenue_col: str
    billings_col: str
    fee_col: str | None
    type_col: str | None


@dataclass(frozen=True)
class Row:
    file_row: int
    values: dict[str, str]

    def __getitem__(self, k: str) -> str:
        return self.values[k]

    def get(self, k: str, default=None):
        return self.values.get(k, default)


@dataclass
class Pnl:
    months: list[tuple[str, str, str]]          # (month, "Actual" or "Plan", column letter)
    rows: dict[str, tuple[int, str | None]]     # label -> (sheet row, section)
    values: dict[tuple[int, str], object]       # (sheet row, column letter) -> cached value

    def cell(self, label: str, month: str) -> tuple[str, float]:
        if label not in self.rows:
            raise Missing(f'Not in the room: the P&L row "{label}"', "row missing",
                          f'a monthly P&L with a "{label}" row')
        r = self.rows[label][0]
        for m, _s, col in self.months:
            if m == month:
                v = self.values.get((r, col))
                if not isinstance(v, (int, float)):
                    raise Missing(f'Not in the room: a value for the P&L row "{label}" in {month}',
                                  "cell empty", "the monthly P&L with its values")
                return f"P&L!{col}{r}", float(v)
        raise Missing(f"Not in the room: the P&L month {month}", "column missing", "a monthly P&L")

    def actual(self) -> list[str]:
        return [m for m, s, _ in self.months if s == "Actual"]

    def first_plan(self) -> str | None:
        plans = [m for m, s, _ in self.months if s == "Plan"]
        return plans[0] if plans else None


@dataclass
class Room:
    path: Path
    tol: float
    layout: Layout
    _csv: dict = field(default_factory=dict)
    _pnl: Pnl | None = None

    def has(self, rel: str | None) -> bool:
        return bool(rel) and (self.path / rel).exists()

    def rows(self, rel: str) -> list[Row]:
        if rel not in self._csv:
            self._csv[rel] = [Row(i + 2, r) for i, r in enumerate(csv_rows(self.path / rel))]
        return self._csv[rel]

    def header(self, rel: str) -> list[str]:
        return next(iter(_csv_header(self.path / rel)), [])

    def src_row(self, rel: str, file_row: int) -> Source:
        return _src(rel, f"row {file_row}", csv_row_text(self.path / rel, file_row))

    def src_cell(self, loc: str, value) -> Source:
        return _src(MODEL, loc, "" if value is None else str(value))

    @property
    def pnl(self) -> Pnl:
        if self._pnl is None:
            if not self.has(MODEL):
                raise Missing("Not in the room: a financial model", "file missing", "the financial model with its P&L")
            sheet = xlsx_sheet(self.path / MODEL, "P&L")
            hdr = next((i for i, r in enumerate(sheet[:15]) if r and r[0] == "Line"), None)
            if hdr is None:
                raise Missing("Not in the room: a monthly P&L", "tab missing", "a monthly P&L")
            months = []
            for ci, m in enumerate(sheet[hdr]):
                if ci >= 2 and m:
                    status = sheet[hdr + 1][ci] if hdr + 1 < len(sheet) else None
                    months.append((str(m), status, get_column_letter(ci + 1)))
            rows, values = {}, {}
            for ri in range(hdr + 2, len(sheet)):
                row = sheet[ri]
                if row and row[0]:
                    rows[str(row[0])] = (ri + 1, row[1] if len(row) > 1 else None)
                for ci, v in enumerate(row):
                    values[(ri + 1, get_column_letter(ci + 1))] = v
            self._pnl = Pnl(months, rows, values)
        return self._pnl

    def sheet(self, name: str) -> list[list]:
        return xlsx_sheet(self.path / MODEL, name)

    def has_sheet(self, name: str) -> bool:
        from schema.readers import xlsx_sheet_names
        return self.has(MODEL) and name in xlsx_sheet_names(self.path / MODEL)

    def named(self, name: str) -> tuple[str, object] | None:
        if not self.has(MODEL):
            return None
        try:
            return xlsx_defined_name(self.path / MODEL, name), xlsx_cell(self.path / MODEL, name)
        except Exception:  # noqa: BLE001 - a missing name is simply absent
            return None


def _csv_header(path: Path):
    import csv
    with open(path, newline="", encoding="utf-8") as f:
        yield next(csv.reader(f), [])


def _src(uri: str, locator: str, quote: str) -> Source:
    return Source(kind="file", uri=uri, locator=locator, quote=quote, retrieved_at=now_iso()[:10])


def layout_for(room: Path) -> Layout:
    files = [str(p.relative_to(room)) for p in find(room, "customers")]
    if BRASS_CUST in files:
        return Layout(BRASS_CUST, "subscription_revenue", "billings", None, None)
    return Layout(HOLLIS_CUST if HOLLIS_CUST in files else None, "mrr", "billings", "one_time_fee", "product_type")


# --------------------------------------------------------------------------- outcome


@dataclass
class Outcome:
    name: str
    label: str = "clear"
    claims: list[Claim] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    really_is: str = "nothing_found"
    file: str = ""
    column: str = ""
    lines: list[tuple[str, str, str, str]] = field(default_factory=list)   # locator, label shown, kind, claim id


class Ctx:
    def __init__(self, room: Room, ids: Ids):
        self.room, self.ids = room, ids

    def claim(self, out: Outcome, text: str, value: Value | None, severity: str, sources: list[Source]) -> str:
        if severity in ("flag", "watch"):
            text = f"{text} {KIND_TEXT[out.name]}"
        c = Claim(id=self.ids(), scan="redflags", text=text, value=value, severity=severity,
                  check=Check(kind="script", name=out.name, model=None), confidence="computed",
                  sources=sources, conflicts_with=[], corroborated_by=[])
        out.claims.append(c)
        return c.id

    def gap(self, out: Outcome, what: str, why: str, would_need: str) -> None:
        if not any(g.what == what for g in out.gaps):
            out.gaps.append(gap(what, why, would_need, PIECE[out.name]))


def _val(number, unit, label, period) -> Value:
    return Value(number=round(float(number), 2), unit=unit, label=label, period=period)


# --------------------------------------------------------------------------- shared sums


def _by_month(room: Room) -> dict[str, list[Row]]:
    out: dict[str, list[Row]] = {}
    for r in room.rows(room.layout.customers):
        out.setdefault(r["month"], []).append(r)
    return out


def _is_sub(r: Row, lay: Layout) -> bool:
    return lay.type_col is None or r[lay.type_col] == "Subscription"


def _require_cols(room: Room, rel: str, cols: list[str], what: str, would_need: str) -> None:
    missing = [c for c in cols if c and c not in room.header(rel)]
    if missing:
        raise Missing(what, f"column missing: {', '.join(missing)}", would_need)


def _sub_sums(room: Room) -> tuple[dict[str, float], dict[str, float]]:
    lay = room.layout
    rev, bill = {}, {}
    for m, rows in _by_month(room).items():
        rev[m] = sum(num(r[lay.revenue_col]) for r in rows if _is_sub(r, lay))
        bill[m] = sum(num(r[lay.billings_col]) for r in rows if _is_sub(r, lay))
    return rev, bill


def _metrics(room: Room) -> dict[str, Row]:
    return {r["month"]: r for r in room.rows(METRICS)}


def _ledger_totals(room: Room) -> dict[str, float]:
    tot: dict[str, float] = {}
    for r in room.rows(LEDGER):
        tot[r["month"]] = tot.get(r["month"], 0.0) + num(r["amount_usd"])
    return tot


def _tie_gaps(room: Room) -> tuple[dict[str, float], dict[str, float]]:
    tot = _ledger_totals(room)
    out = {}
    for m in room.pnl.actual():
        out[m] = tot.get(m, 0.0) - (room.pnl.cell("Total cost of revenue", m)[1]
                                    + room.pnl.cell("Total operating expenses", m)[1])
    return out, tot


def _arr_build(room: Room) -> tuple[list[tuple[int, list]], dict[str, tuple[int, float]]]:
    """(line table rows as (sheet row, values), monthly history month -> (sheet row, subscription MRR))."""
    sheet = room.sheet("ARR_Build")
    lines, hist, in_hist = [], {}, False
    for i, r in enumerate(sheet):
        a = r[0] if r else None
        if a == "Month":
            in_hist = True
        elif in_hist and isinstance(a, str) and MONTH_RE.match(a):
            hist[a] = (i + 1, num(r[2]))
        elif not in_hist and len(r) > 4 and r[1] not in (None, "Product type"):
            lines.append((i + 1, r))
    return lines, hist


# --------------------------------------------------------------------------- a


def _check_a(ctx: Ctx, out: Outcome) -> None:
    room = ctx.room
    out.file, out.column = METRICS, "mrr"
    if not room.has(METRICS) or "mrr" not in room.header(METRICS):
        out.label, out.really_is = "not_run", "not_checked"
        return
    met = _metrics(room)
    as_of = max(met)
    shown = num(met[as_of]["mrr"])
    if room.has(room.layout.customers):
        bm = _by_month(room)
        sub = {t: sum(num(r["mrr"]) for r in rows if r["product_type"] == "Subscription") for t, rows in bm.items()}
        others = [r for r in bm.get(as_of, []) if r["product_type"] not in ("Subscription", "Onboarding") and num(r["mrr"]) > 0]
        groups: dict[str, list[Row]] = {}
        for r in others:
            groups.setdefault(r["product_type"], []).append(r)
        srcs, parts = [], []
        for ptype, rows in sorted(groups.items()):
            top = max(rows, key=lambda r: num(r["mrr"]))
            srcs.append(room.src_row(room.layout.customers, top.file_row))
            total = sum(num(r["mrr"]) for r in rows)
            parts.append(f"{top['customer_name']} ({ptype}, {money(total)})" if len(rows) == 1
                         else f"{len(rows)} {ptype} rows ({money(total)})")
        types = set(groups)
        other_sum = sum(num(r["mrr"]) for r in others)
        out.file, out.column = room.layout.customers, "product_type, mrr"
        sub_words = "The subscription rows add to"
    else:
        ctx.gap(out, "Not in the room: a revenue export by product type", "file missing",
                "monthly revenue by customer with a product type column")
        if not room.has_sheet("ARR_Build"):
            out.label, out.really_is = "cannot_check", "not_checked"
            return
        lines, hist = _arr_build(room)
        sub = {m: v for m, (_r, v) in hist.items()}
        nonsub = [(r, v) for r, v in lines if v[1] not in ("Subscription", "Onboarding") and num(v[3]) > 0]
        types = {v[1] for _, v in nonsub}
        other_sum = sum(num(v[3]) for _, v in nonsub)
        parts = [f"{v[0]} ({v[1]}, {money(num(v[3]))})" for _, v in nonsub]
        srcs = [room.src_cell(f"ARR_Build!B{r}", v[1]) for r, v in nonsub]
        if as_of in hist:
            srcs.append(room.src_cell(f"ARR_Build!C{hist[as_of][0]}", room.sheet("ARR_Build")[hist[as_of][0] - 1][2]))
        out.file, out.column = MODEL, "ARR_Build Product type, MRR"
        sub_words = "The model's ARR_Build shows subscription MRR of"
    # Cite the model's ARR_Build row for the same line: the shared source that links this claim
    # to entry 1.2's pilot-as-ARR flag, which cites ARR_Build!E13 (04_architecture.md, D3).
    if room.has_sheet("ARR_Build"):
        for r, v in _arr_build(room)[0]:
            if v[1] in types and num(v[4]) > 0:
                srcs += [room.src_cell(f"ARR_Build!A{r}", v[0]), room.src_cell(f"ARR_Build!E{r}", v[4])]
    sub_now = sub.get(as_of, 0.0)
    flagged = [t for t in sorted(met) if sub.get(t) and (num(met[t]["mrr"]) - sub[t]) / sub[t] > room.tol]
    m_src = room.src_row(METRICS, met[as_of].file_row)
    if not flagged:
        cid = ctx.claim(out, f"The mrr column in monthly_metrics.csv for {as_of}, {money(shown)}, matches subscription "
                             f"MRR ({money(sub_now)}) within {pct(room.tol)}.",
                        _val(sub_now, "USD_per_month", "mrr", as_of), "info", [m_src])
        return
    diff = shown - sub_now
    explained = parts and abs(diff - other_sum) <= room.tol * max(diff, 1)
    text = (f"monthly_metrics.csv shows MRR of {money(shown)} for {as_of}. {sub_words} {money(sub_now)}. "
            f"The {money(diff)} difference is {pct(diff / sub_now)} of subscription MRR"
            + (f" and equals the non-subscription lines: {'; '.join(parts)}." if explained else ".")
            + f" Months over tolerance: {', '.join(flagged)}.")
    cid = ctx.claim(out, text, _val(sub_now, "USD_per_month", "mrr", as_of), "flag", [m_src] + srcs)
    kind = "pilot" if "Pilot" in types else ("pass_through" if any(PASS_TYPE_RE.search(t) for t in types) else "one_time_fee")
    out.label, out.really_is = "flag", kind
    out.lines.append((f"{METRICS} row {met[as_of].file_row}", "mrr", kind, cid))
    if room.has(MODEL):
        for label in room.pnl.rows:
            if label.lower().startswith("recurring revenue"):
                loc, v = room.pnl.cell(label, as_of)
                if other_sum and abs(v - (sub_now + other_sum)) <= room.tol * sub_now:
                    out.lines.append((loc, label, kind, cid))


# --------------------------------------------------------------------------- b


def _check_b(ctx: Ctx, out: Outcome) -> None:
    room, lay = ctx.room, ctx.room.layout
    what = "Not in the room: an invoices or billings export"
    need = "monthly invoices or billings by customer"
    out.file, out.column = lay.customers or HOLLIS_CUST, f"{lay.billings_col}, {lay.revenue_col}"
    if not room.has(lay.customers):
        raise Missing(what, "file missing", need)
    _require_cols(room, lay.customers, [lay.billings_col, lay.revenue_col], what, need)
    rev, bill = _sub_sums(room)
    months = [m for m in room.pnl.actual() if m in rev]
    as_of = months[-1]
    fired, maxdiff = [], 0.0
    for t in months:
        loc, shown = room.pnl.cell("Subscription revenue", t)
        maxdiff = max(maxdiff, abs(shown - rev[t]))
        if abs(shown - bill[t]) < abs(shown - rev[t]) and abs(shown - rev[t]) / rev[t] > room.tol:
            fired.append((t, loc, shown))
    for t, loc, shown in fired:
        ctx.claim(out, f'The P&L row "Subscription revenue" for {t} is {money(shown)}. Subscription billings in '
                       f"{Path(lay.customers).name} add to {money(bill[t])} and subscription revenue adds to "
                       f"{money(rev[t])}. The P&L figure sits on the billings side.",
                  _val(rev[t], "USD", "other", t), "flag", [room.src_cell(loc, room.pnl.values[_rc(loc)])])
    arr = room.named("ARR_TOTAL")
    if arr:
        a12 = num(arr[1]) / 12
        if abs(a12 - bill[as_of]) < abs(a12 - rev[as_of]) and abs(a12 - rev[as_of]) / rev[as_of] > room.tol:
            ctx.claim(out, f"ARR_TOTAL divided by 12 is {money(a12)}, nearer {as_of} billings ({money(bill[as_of])}) "
                           f"than {as_of} subscription revenue ({money(rev[as_of])}).",
                      _val(12 * rev[as_of], "USD", "arr", as_of), "flag", [_src(MODEL, "ARR_TOTAL", str(arr[1]))])
    if out.claims:
        out.label, out.really_is = "flag", "billings"
        return
    spikes = [t for t in months if abs(bill[t] - rev[t]) / rev[t] > room.tol]
    loc, shown = room.pnl.cell("Subscription revenue", as_of)
    ctx.claim(out, f'The P&L row "Subscription revenue" matches subscription revenue in the customer file in all '
                   f"{len(months)} actual months (largest difference {money(maxdiff)}). Billings differ from revenue by "
                   f"more than {pct(room.tol)} in {len(spikes)} of those months, which annual plans paid up front "
                   f"explain on their own.",
              _val(shown, "USD", "other", as_of), "info",
              [room.src_cell(loc, room.pnl.values[_rc(loc)]), room.src_row(lay.customers, 1)])


# --------------------------------------------------------------------------- c


def _check_c(ctx: Ctx, out: Outcome) -> None:
    room, lay = ctx.room, ctx.room.layout
    what = "Not in the room: a revenue export that separates pass-through money"
    need = "a revenue export with a pass-through or resale column, and the ledger lines paid on at cost"
    out.file = lay.customers or HOLLIS_CUST
    if not room.has(lay.customers):
        raise Missing(what, "file missing", need)
    hdr = room.header(lay.customers)
    bm = _by_month(room)
    pt_col = next((h for h in hdr if PASS_COL_RE.search(h)), None)
    fee_col = next((h for h in hdr if "fee" in h and h not in (pt_col, lay.fee_col)), None)
    pt, incl, excl, desc = {}, {}, {}, ""
    if pt_col and fee_col:
        for t, rows in bm.items():
            pt[t] = sum(num(r[pt_col]) for r in rows)
            excl[t] = sum(num(r[fee_col]) for r in rows)
            incl[t] = excl[t] + pt[t]
        desc, out.column = f"column {pt_col}", f"{pt_col}, {fee_col}"
        is_pt = lambda r: num(r[pt_col]) > 0  # noqa: E731
    elif lay.type_col:
        pt_types = {r[lay.type_col] for rows in bm.values() for r in rows if PASS_TYPE_RE.search(r[lay.type_col])}
        out.column = "product_type, mrr"
        for t, rows in bm.items():
            pt[t] = sum(num(r["mrr"]) for r in rows if r[lay.type_col] in pt_types)
            excl[t] = sum(num(r["mrr"]) for r in rows if r[lay.type_col] not in pt_types)
            incl[t] = excl[t] + pt[t]
        desc = f"product type {', '.join(sorted(pt_types))}"
        is_pt = lambda r: r[lay.type_col] in pt_types  # noqa: E731
    if not pt or not any(pt.values()):
        ctx.gap(out, what, "not stated in the file", need)
        out.label, out.really_is = "not_run", "not_checked"
        return
    as_of = max(bm)
    met = _metrics(room) if room.has(METRICS) else {}
    holders = []   # (kind, label, locator, value)
    if room.has(MODEL):
        for label, (_r, sec) in room.pnl.rows.items():
            if sec == "Revenue" and not label.lower().startswith("total"):
                loc, v = room.pnl.cell(label, as_of)
                holders.append(("P&L", label, loc, v))
    if as_of in met:
        for h in room.header(METRICS):
            if re.search(r"(revenue|mrr)", h) and not h.startswith("total"):
                holders.append(("metrics", h, f"row {met[as_of].file_row}", num(met[as_of][h])))
    holders = [x for x in holders if abs(x[3] - incl[as_of]) <= room.tol * incl[as_of]
               and abs(x[3] - incl[as_of]) < abs(x[3] - excl[as_of])]
    ltm = sorted(t for t in bm if t <= as_of)[-12:]
    pt_ltm = sum(pt.get(t, 0.0) for t in ltm)
    if any(k == "P&L" for k, *_ in holders):
        shown_ltm = sum(room.pnl.cell("Total revenue", t)[1] for t in ltm)
        shown_label = "P&L Total revenue"
    else:
        h = next((x for x in holders if x[0] == "metrics"), None)
        shown_ltm = sum(num(met[t][h[1]]) for t in ltm if t in met) if h else 0.0
        shown_label = f"monthly_metrics.csv {h[1]}" if h else "revenue"
    share = pt_ltm / shown_ltm if shown_ltm else 0.0
    if not holders or share <= room.tol or any("gross" in x[1].lower() for x in holders):
        return
    led_src, led_ltm = [], 0.0
    if room.has(LEDGER):
        for r in room.rows(LEDGER):
            if r["month"] in ltm and PASS_LEDGER_RE.search(f"{r['category']} {r['description']}"):
                led_ltm += num(r["amount_usd"])
                if r["month"] == as_of and not led_src:
                    led_src.append(room.src_row(LEDGER, r.file_row))
    srcs = []
    for kind, label, loc, v in holders[:2]:
        srcs.append(room.src_cell(loc, room.pnl.values[_rc(loc)]) if kind == "P&L"
                    else room.src_row(METRICS, met[as_of].file_row))
    pt_row = next((r for r in bm[as_of] if is_pt(r)), None)
    if pt_row:
        srcs.append(room.src_row(lay.customers, pt_row.file_row))
    srcs += led_src
    names = ", ".join(f'{k} "{lab}"' for k, lab, *_ in holders)
    cid = ctx.claim(out, f"{names} for {as_of} equals the gross amount ({money(incl[as_of])}), including "
                         f"{money(pt[as_of])} passed on ({desc}). Over the 12 months to {as_of}, {money(pt_ltm)} of "
                         f"pass-through money sits inside {money(shown_ltm)} of {shown_label}, {pct(share)}. Net of it: "
                         f"{money(shown_ltm - pt_ltm)}."
                         + (f" The ledger shows {money(led_ltm)} paid on in the same months." if led_ltm else ""),
                    _val(shown_ltm - pt_ltm, "USD", "other", f"{ltm[0]} to {ltm[-1]}"), "flag", srcs)
    out.label, out.really_is = "flag", "pass_through"
    for kind, label, loc, _v in holders:
        out.lines.append((loc if kind == "P&L" else f"{METRICS} {loc}", label, "pass_through", cid))


def _rc(loc: str) -> tuple[int, str]:
    ref = loc.split("!")[1]
    col = re.match(r"[A-Z]+", ref).group()
    return int(ref[len(col):]), col


# --------------------------------------------------------------------------- e


def contractor_vendors(room: Path | Room) -> set[str]:
    """Vendors with at least one ledger line naming a contractor; every line of theirs counts (extends 1.12)."""
    if isinstance(room, Path):
        room = Room(Path(room), 0.01, layout_for(Path(room)))
    return {r["vendor"] for r in room.rows(LEDGER)
            if CONTRACTOR_RE.search(f"{r['vendor']} {r['description']} {r['category']}")}


def _check_e(ctx: Ctx, out: Outcome) -> None:
    room = ctx.room
    out.file, out.column = LEDGER, "vendor, description, amount_usd"
    if not room.has(LEDGER):
        raise Missing("Not in the room: an expense ledger", "file missing", "the expense ledger with vendor, description and amount")
    ties, tot = _tie_gaps(room)
    months = sorted(ties)
    as_of = months[-1]
    vendors = contractor_vendors(room)
    lines = [r for r in room.rows(LEDGER) if r["vendor"] in vendors]
    now_lines = [r for r in lines if r["month"] == as_of]
    now = sum(num(r["amount_usd"]) for r in now_lines)
    staff = room.named("STAFF_NOW") or room.named("EMPLOYEES_NOW")
    for t in months:
        if tot.get(t) and abs(ties[t]) / tot[t] > room.tol:
            loc, v = room.pnl.cell("Total operating expenses", t)
            ctx.claim(out, f"Ledger lines for {t} add to {money(tot[t])}. P&L cost of revenue plus operating expenses "
                           f"differ from that by {money(ties[t])}.",
                      _val(ties[t], "USD", "other", t), "flag", [room.src_cell(loc, v)])
    plan_m = room.pnl.first_plan()
    if now > 0 and plan_m:
        cats = {r["category"] for r in now_lines}
        cat_sum = sum(num(r["amount_usd"]) for r in room.rows(LEDGER) if r["month"] == as_of and r["category"] in cats)
        row_label = None
        for label in room.pnl.rows:
            try:
                _loc, v = room.pnl.cell(label, as_of)
            except Missing:
                continue
            if abs(v - cat_sum) < 0.01:
                row_label = label
                break
        if row_label:
            act_loc, act = room.pnl.cell(row_label, as_of)
            plan_loc, plan_v = room.pnl.cell(row_label, plan_m)
            covered = plan_v - (act - now)
            if covered < now * (1 - room.tol):
                srcs = [room.src_cell(act_loc, room.pnl.values[_rc(act_loc)]),
                        room.src_cell(plan_loc, room.pnl.values[_rc(plan_loc)])]
                srcs += [room.src_row(LEDGER, r.file_row) for r in now_lines[:3]]
                if staff:
                    srcs.append(room.src_cell(staff[0], staff[1]))
                names = ", ".join(sorted({r["vendor"] for r in now_lines}))
                ctx.claim(out, f"Contractor lines in the ledger add to {money(now)} in {as_of} ({len(now_lines)} lines "
                               f'from {names}). They sit in the P&L row "{row_label}", {money(act)} in {as_of}. The plan '
                               f"puts {money(plan_v)} on that row from {plan_m}, which leaves "
                               f"{money(now - max(covered, 0))} a month of the contractors out of the plan's burn."
                               + (f" The staff count is {staff[1]} ({staff[0]})." if staff else ""),
                          _val(now, "USD_per_month", "payroll_monthly", as_of), "flag", srcs)
    if out.claims:
        out.label, out.really_is = "flag", "contractor_spend"
        ctx.gap(out, "Not in the room: a statement of whether the staff count includes contractors",
                "not stated in the file", "a contractor list, or an org chart that shows them")
        return
    worst = max(months, key=lambda t: abs(ties[t]))
    loc, v = room.pnl.cell("Total operating expenses", as_of)
    srcs = [room.src_cell(loc, room.pnl.values[_rc(loc)])]
    if staff:
        srcs.append(room.src_cell(staff[0], staff[1]))
    text = (f"Ledger lines tie to P&L cost of revenue plus operating expenses in all {len(months)} actual months "
            f"(largest difference {money(abs(ties[worst]))}). "
            + (f"Contractor lines add to {money(now)} in {as_of}, and the plan keeps them." if now
               else "No ledger line names a contractor, consultant, freelancer, agency or statement of work."))
    ctx.claim(out, text, _val(tot[as_of], "USD", "other", as_of), "watch" if now else "info", srcs)
    if now:
        out.label, out.really_is = "watch", "contractor_spend"
    ctx.gap(out, "Not in the room: a list of contractors, or an org chart that shows them", "file missing",
            "a contractor list or contractor agreements")


# --------------------------------------------------------------------------- f


def _check_f(ctx: Ctx, out: Outcome) -> None:
    room = ctx.room
    out.file, out.column = LEDGER, "booked_as, category"
    if not room.has(LEDGER):
        raise Missing("Not in the room: an expense ledger", "file missing", "the expense ledger with booked_as and category")
    ties, tot = _tie_gaps(room)
    months = sorted(ties)
    as_of = months[-1]
    cap: dict[str, float] = {}
    for r in room.rows(LEDGER):
        if ASSET_RE.search(f"{r['booked_as']} {r['category']}"):
            cap[r["month"]] = cap.get(r["month"], 0.0) + num(r["amount_usd"])
    bridge, cash = room.named("CASH_BRIDGE_DIFF"), room.named("CASH_START")
    fired = [t for t in months if tot.get(t) and (cap.get(t, 0) / tot[t] > room.tol or abs(ties[t]) / tot[t] > room.tol)]
    bridge_bad = bool(bridge and cash and abs(num(bridge[1])) / num(cash[1]) > room.tol)
    booked = sorted({r["booked_as"] for r in room.rows(LEDGER)})
    srcs = [room.src_row(LEDGER, 1)]
    if bridge:
        srcs.append(room.src_cell(bridge[0], bridge[1]))
    if cash:
        srcs.append(room.src_cell(cash[0], cash[1]))
    bridge_txt = money(num(bridge[1])) if bridge else "not stated"
    cash_txt = money(num(cash[1])) if cash else "not stated"
    if fired or bridge_bad:
        ctx.claim(out, f"Spend recorded as an asset or outside the P&L in {', '.join(fired) or 'no month'}; the cash "
                       f"bridge difference is {bridge_txt} against cash of {cash_txt}. Whether the treatment is allowed "
                       f"is for the investor's accountant.", None, "flag", srcs)
        out.label, out.really_is = "flag", "capitalised_spend"
    else:
        ctx.claim(out, f"Every ledger line is booked as one of {', '.join(booked)}; none names an asset. The cash bridge "
                       f"difference is {bridge_txt} against cash of {cash_txt}.",
                  _val(num(cash[1]), "USD", "cash", as_of) if cash else None, "info", srcs)
    ctx.gap(out, "Not in the room: a balance sheet", "file missing", "monthly balance sheets")


# --------------------------------------------------------------------------- g


def _check_g(ctx: Ctx, out: Outcome) -> None:
    room, lay = ctx.room, ctx.room.layout
    what = "Not in the room: a balance sheet with a deferred revenue line"
    out.file, out.column = lay.customers or HOLLIS_CUST, f"{lay.billings_col}, {lay.revenue_col}"
    if not room.has(lay.customers):
        raise Missing(what, "file missing", "monthly balance sheets, or invoices and revenue by customer")
    _require_cols(room, lay.customers, [lay.billings_col, lay.revenue_col], what, "invoices and revenue by customer")
    bm = _by_month(room)
    as_of = max(bm)
    cum: dict[str, float] = {}
    for t in sorted(bm):
        for r in bm[t]:
            earned = num(r[lay.revenue_col]) + (num(r[lay.fee_col]) if lay.fee_col else 0.0)
            cum[r["customer_id"]] = cum.get(r["customer_id"], 0.0) + num(r[lay.billings_col]) - earned
    deferred = {c: v for c, v in cum.items() if v > 0.005}
    total = sum(deferred.values())
    rev, _bill = _sub_sums(room)
    for t in [m for m in room.pnl.actual() if m in rev]:
        loc, shown = room.pnl.cell("Subscription revenue", t)
        if shown > rev[t] * (1 + room.tol):
            excess = shown - rev[t]
            culprits = [r for r in bm[t] if num(r[lay.billings_col]) - num(r[lay.revenue_col]) > 0.005]
            matched = abs(sum(num(r[lay.billings_col]) - num(r[lay.revenue_col]) for r in culprits) - excess) <= room.tol * excess
            names = ", ".join(r["customer_name"] for r in culprits)
            srcs = [room.src_cell(loc, room.pnl.values[_rc(loc)])] + [room.src_row(lay.customers, r.file_row) for r in culprits[:3]]
            ctx.claim(out, f'The P&L row "Subscription revenue" for {t} is {money(shown)}. Revenue earned in the customer '
                           f"file is {money(rev[t])}. The {money(excess)} excess "
                           + (f"equals the unearned part of the invoices billed that month to {names}." if matched
                              else "is not explained by one invoice."),
                      _val(rev[t], "USD_per_month", "mrr", t), "flag", srcs)
    arr_sub = None
    if room.has_sheet("ARR_Build"):
        for i, r in enumerate(room.sheet("ARR_Build")):
            if r and r[0] == "Subscription ARR":
                arr_sub = (f"ARR_Build!E{i + 1}", r[4])
        if arr_sub and num(arr_sub[1]) > 12 * rev[as_of] * (1 + room.tol):
            ctx.claim(out, f"ARR_Build Subscription ARR {money(num(arr_sub[1]))} is above 12 times {as_of} subscription "
                           f"revenue ({money(12 * rev[as_of])}).", _val(12 * rev[as_of], "USD", "arr", as_of), "flag",
                      [room.src_cell(*arr_sub)])
    pnl_flag = bool(out.claims)
    dnamed = room.named("DEFERRED_REVENUE_USD")
    if dnamed and abs(num(dnamed[1]) - total) > room.tol * max(total, 1):
        # Info when a P&L flag already fired: the bridge cell is also a decoy location (Brasswick DC1),
        # and eval.score counts any flag that cites it (extends 1.12; AM-R24).
        ctx.claim(out, f"Deferred revenue rebuilt from billings less revenue is {money(total)} across {len(deferred)} "
                       f"customers at {as_of}. The model's cash bridge carries {money(num(dnamed[1]))}.",
                  _val(total, "USD", "other", as_of), "info" if pnl_flag else "flag", [room.src_cell(*dnamed)])
    if any(c.severity == "flag" for c in out.claims):
        out.label, out.really_is = "flag", "deferred_revenue"
    else:
        srcs = [room.src_row(lay.customers, 1)] + ([room.src_cell(*arr_sub)] if arr_sub else [])
        ctx.claim(out, f"Billed but not yet earned at {as_of}: {money(total)} across {len(deferred)} customers. The P&L "
                       f'row "Subscription revenue" does not exceed revenue earned in any month'
                       + (f", and ARR_Build Subscription ARR ({money(num(arr_sub[1]))}) is 12 times {as_of} subscription "
                          f"revenue." if arr_sub else "."),
                  _val(total, "USD", "other", as_of), "info", srcs)
    if not dnamed:
        ctx.gap(out, what, "file missing", "monthly balance sheets")


# --------------------------------------------------------------------------- h


def _check_h(ctx: Ctx, out: Outcome) -> None:
    room, lay = ctx.room, ctx.room.layout
    out.column = "one_time_fee"
    has_cust = bool(lay.fee_col) and room.has(lay.customers)
    fee_row = None
    if room.has(MODEL):
        fee_row = next((l for l in room.pnl.rows if "one-time" in l.lower()), None)
    if not (has_cust or fee_row) or not room.has(METRICS) or "mrr" not in room.header(METRICS):
        out.label, out.really_is, out.file = "not_run", "not_checked", lay.customers or METRICS
        return
    met = _metrics(room)
    fees, sub = {}, {}
    if has_cust:
        for t, rows in _by_month(room).items():
            fees[t] = sum(num(r[lay.fee_col]) for r in rows)
            sub[t] = sum(num(r["mrr"]) for r in rows if r["product_type"] == "Subscription")
        out.file = lay.customers
    else:
        for t in room.pnl.actual():
            fees[t] = room.pnl.cell(fee_row, t)[1]
        sub = {m: v for m, (_r, v) in _arr_build(room)[1].items()}
        out.file = MODEL
    fired = [t for t in sorted(met) if fees.get(t, 0) > 0
             and abs(num(met[t]["mrr"]) - sub.get(t, 0) - fees[t]) / fees[t] <= room.tol]
    onboard = None
    if room.has_sheet("ARR_Build"):
        for r, v in _arr_build(room)[0]:
            if v[1] == "Onboarding":
                onboard = (r, v)
    as_of = max(met)
    m_src = room.src_row(METRICS, met[as_of].file_row)
    if fired or (onboard and num(onboard[1][4]) > 0):
        srcs = [m_src] + ([room.src_cell(f"ARR_Build!E{onboard[0]}", onboard[1][4])] if onboard else [])
        ctx.claim(out, f"One-time fees appear in recurring figures: the mrr gap equals the month's fees in "
                       f"{', '.join(fired) or 'no month'}; ARR counted on the onboarding row is "
                       f"{money(num(onboard[1][4])) if onboard else '$0'}.", None, "flag", srcs)
        out.label, out.really_is = "flag", "one_time_fee"
        return
    g = num(met[as_of]["mrr"]) - sub.get(as_of, 0)
    srcs = [m_src]
    if onboard:
        srcs += [room.src_cell(f"ARR_Build!A{onboard[0]}", onboard[1][0]),
                 room.src_cell(f"ARR_Build!E{onboard[0]}", onboard[1][4])]
    ctx.claim(out, f"One-time fees of {money(fees.get(as_of, 0))} in {as_of} are not in the mrr column: the gap between "
                   f"mrr and subscription MRR is {money(g)}, not the fee total"
                   + (f', and the ARR_Build row "{onboard[1][0]}" counts {money(num(onboard[1][4]))} of ARR.' if onboard else "."),
              _val(fees.get(as_of, 0), "USD", "other", as_of), "info", srcs)


# --------------------------------------------------------------------------- entry


def _run(room_dir: Path, ids: Ids) -> list[Outcome]:
    room_dir = Path(room_dir)
    room = Room(room_dir, float(settings.load()["match_tolerance"]), layout_for(room_dir))
    ctx = Ctx(room, ids)
    outs = []
    for letter, name in ORDER:
        out = Outcome(name)
        fn = globals()[f"_check_{letter}"]   # looked up at call time, so a test can replace one
        try:
            fn(ctx, out)
        except Missing as m:
            out.claims, out.label, out.really_is = [], "cannot_check", "not_checked"
            ctx.gap(out, m.what, m.why, m.would_need)
        except Exception as err:  # noqa: BLE001 - one broken sub-check never stops the others (AM-R6)
            out.claims, out.label, out.really_is = [], "cannot_check", "not_checked"
            ctx.gap(out, f"Not in the room: readable input for {name}", f"{type(err).__name__}: {err}",
                    "the files this check reads, in the shape the room index describes")
        outs.append(out)
    return outs


def _panels(outs: list[Outcome]) -> list[Panel]:
    worst = max((o.label for o in outs), key=lambda x: ORDER_RANK[x])
    if all(o.label in ("cannot_check", "not_run") for o in outs):
        worst = "cannot_check"
    why = [o.name for o in outs if o.label == worst]
    checks = Panel(name="accounting mislabels: checks",
                   columns=["check_name", "defined_in", "scope", "label", "label_claimed", "really_is", "file", "column", "claim_ids"],
                   rows=[[o.name, "1.12", "after_saturday", o.label, LABEL_CLAIMED[o.name], o.really_is, o.file, o.column,
                          ", ".join(c.id for c in o.claims)] for o in outs])
    lines = Panel(name="accounting mislabels: lines", columns=["locator", "label_shown", "kind", "claim_id"],
                  rows=[list(ln) for o in outs for ln in o.lines])
    entry = Panel(name="accounting mislabels: entry", columns=["framework", "label", "label_reason"],
                  rows=[["accounting_mislabels", worst, f"Worst sub-check label is {worst}: {', '.join(why)}."]])
    return [entry, checks, lines]


def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap], list[Panel]]:
    outs = _run(room, ids)
    claims = [c for o in outs for c in o.claims]
    gaps = [g for o in outs for g in o.gaps]
    return claims, gaps, _panels(outs)


def outcomes(room: Path) -> dict[str, str]:
    """Each sub-check's label for a room: flag, watch, clear, cannot_check or not_run."""
    return {o.name: o.label for o in _run(Path(room), Ids("redflags"))}
