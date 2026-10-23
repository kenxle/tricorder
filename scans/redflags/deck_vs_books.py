"""Deck revenue against the books, and partial history.

The associate's rule: "If revenue in the deck doesn't match the P&L, or you
show only part of your history, everything else becomes questionable."
(ROADMAP.md, deck-vs-books). Requirements DVB-R1 to DVB-R13 are in
docs/features/20261022.11_deck_vs_books/03_prd.md; the design is in
04_architecture.md beside it.

Two check names:

- deck_revenue_vs_pnl: every revenue figure the deck shows (a total, a chart's
  bars, a growth sentence) against the same period in the model's P&L tab.
- deck_history_vs_metrics: a revenue chart that starts after the first revenue
  month, skips months, or shows quarters where the books hold months. The name
  is the one data_room/answer_key_brasswick.json gives BF2.

Scripts only. No model call, no network. Files are read through
schema/readers.py, except the chart's pixels, which come from pdfplumber's
render of the chart's box on the slide.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import pdfplumber
from openpyxl.utils import get_column_letter

from schema import settings
from schema.claim import Check, Claim, Gap, Panel, Source, Value
from schema.readers import LocatorError, csv_row_text, csv_rows, pdf_pages, xlsx_sheet
from scans.base import Ids, find, gap

SCAN = "redflags"
CHECK_REVENUE = "deck_revenue_vs_pnl"
CHECK_HISTORY = "deck_history_vs_metrics"
PIECE = "traction_and_revenue"
MODEL = "02_financials/financial_model.xlsx"
FLAT_TOLERANCE = 0.01   # a month within 1 percent of the one before counts as flat
FLAT_MIN_MONTHS = 3     # three flat months in a row is a flat stretch
CHART_DPI = 150
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
REVENUE_WORDS = re.compile(r"\b(ARR|MRR|[Rr]evenue)\b")
MONEY = re.compile(r"\$[\d,.]+[KMB]?")
CAPTION = re.compile(r"(Monthly|Quarterly) (recurring )?revenue, (\w+ \d{4}) to (\w+ \d{4})")
PLAN_GROWTH = re.compile(r"Revenue grows ([\d.]+)% a month in the plan\.")
GREW = re.compile(r"Revenue grew every month in (\d{4})\.")
# Revenue-row columns that add up to one month's revenue, by file (DVB-R9).
ROW_COLUMNS = {"customer_mrr_by_month.csv": ("mrr",),
               "revenue_by_customer.csv": ("subscription_revenue", "recovered_from_carriers")}


# --------------------------------------------------------------------------- shapes

@dataclass(frozen=True)
class Cell:
    value: float
    uri: str
    locator: str
    quote: str


@dataclass
class Books:
    uri: str
    actual: list[str]
    plan: list[str]
    lines: dict[str, dict[str, Cell]]
    recurring_label: str
    total_label: str
    first_revenue_month: str
    is_pnl: bool = True


@dataclass
class Figure:
    kind: str                      # "stated" | "chart" | "plan_growth" | "grew_every_month"
    slide: int
    sources: list[Source]
    label: str | None = None
    printed: str | None = None
    number: float | None = None
    half_step: float = 0.0
    grain: str | None = None       # "monthly" | "quarterly"
    recurring: bool = False
    start: str | None = None
    end: str | None = None
    bars: list[int] | None = None
    pct: float | None = None
    year: int | None = None


@dataclass
class Out:
    ids: Ids
    claims: list[Claim] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)

    def claim(self, text, value, severity, check, sources):
        self.claims.append(Claim(
            id=self.ids(), scan=SCAN, text=text, value=value, severity=severity,
            check=Check(kind="script", name=check, model=None), confidence="computed",
            sources=sources, conflicts_with=[], corroborated_by=[]))

    def gap(self, what, why, would_need):
        if any(g.what == what and g.why == why for g in self.gaps):
            return  # the same missing value seen by a second figure
        self.gaps.append(gap(what, why, would_need, PIECE))

    def row(self, slide, figure, period, books, basis, gap_text, ok):
        self.rows.append([str(slide), figure, period or "", books, basis, gap_text, "yes" if ok else "no"])


# --------------------------------------------------------------------------- small helpers

def _ym(y: int, m: int) -> str:
    return f"{y:04d}-{m:02d}"


def _month(text: str) -> str:
    name, year = text.split()
    return _ym(int(year), MONTHS.index(name) + 1)


def _next(m: str) -> str:
    y, mo = map(int, m.split("-"))
    return _ym(y + (mo == 12), 1 if mo == 12 else mo + 1)


def _range(start: str, end: str) -> list[str]:
    out, m = [], start
    while m <= end:
        out.append(m)
        m = _next(m)
    return out


def _quarter(m: str) -> str:
    y, mo = map(int, m.split("-"))
    return f"{y}-Q{(mo - 1) // 3 + 1}"


def _usd(v: float) -> str:
    return f"-${-v:,.0f}" if v < 0 else f"${v:,.0f}"


def _source(uri: str, locator: str, quote: str) -> Source:
    return Source(kind="file", uri=uri, locator=locator, start_s=None, end_s=None,
                  quote=quote, retrieved_at=date.today().isoformat())


def _flat_stretch(months: list[str], values: list[float]) -> tuple[str, str] | None:
    """The first run of FLAT_MIN_MONTHS or more months, each within FLAT_TOLERANCE of the one before."""
    def is_flat(i):
        return values[i - 1] > 0 and abs(values[i] / values[i - 1] - 1) <= FLAT_TOLERANCE

    i = 1
    while i < len(values):
        if is_flat(i):
            j = i
            while j + 1 < len(values) and is_flat(j + 1):
                j += 1
            if j - i + 2 >= FLAT_MIN_MONTHS:
                return months[i - 1], months[j]
            i = j + 1
        else:
            i += 1
    return None


def _cell_source(c: Cell) -> Source:
    return _source(c.uri, c.locator, c.quote)


def parse_money(text: str) -> tuple[float, float]:
    """'$2.5M' -> (2500000, 50000): the value and half a unit of its last printed digit."""
    t = text.strip().replace(",", "")
    m = re.fullmatch(r"\$?([\d.]+)\s*([KMB])?", t)
    if not m:
        raise ValueError(text)
    digits, suffix = m.group(1), m.group(2)
    scale = {"K": 1e3, "M": 1e6, "B": 1e9}.get(suffix, 1)
    decimals = len(digits.split(".")[1]) if "." in digits else 0
    return float(digits) * scale, (0.5 * scale * 10 ** (-decimals) if suffix else 0.5)


def figure_matches(deck: float, books: float, half_step: float, tolerance: float) -> bool:
    """DVB-R3: within the relative tolerance, or within half a printed step of a short-form figure."""
    diff = abs(deck - books)
    return diff <= abs(books) * tolerance or diff <= half_step


# --------------------------------------------------------------------------- the deck

def read_bars(img) -> list[int] | None:
    """Bar heights in pixels, left to right, for a single-colour bar chart. None if unreadable."""
    w, h = img.size
    px = img.load()
    counts = Counter(px[x, y] for x in range(0, w, 2) for y in range(0, h, 2))
    colours = [c for c, _ in counts.most_common(6) if max(c) - min(c) > 40]
    if not colours:
        return None
    bar = colours[0]

    def is_bar(x, y):
        r, g, b = px[x, y][:3]
        return abs(r - bar[0]) + abs(g - bar[1]) + abs(b - bar[2]) < 30

    base = max((y for y in range(h) for x in range(0, w, 4) if is_bar(x, y)), default=None)
    if base is None:
        return None
    # Scan the bottom-most bar row itself: a bar under 1 percent of the tallest may be only
    # one or two pixels high, and a row higher would miss it.
    runs, start = [], None
    for x in range(w):
        on = is_bar(x, base)
        if on and start is None:
            start = x
        elif not on and start is not None:
            if x - start >= 4:
                runs.append((start, x - 1))
            start = None
    heights = []
    for a, b in runs:
        cx, top = (a + b) // 2, base
        while top > 0 and is_bar(cx, top - 1):
            top -= 1
        heights.append(base - top + 1)
    return heights or None


def chart_bars(deck: Path, slide: int) -> list[int] | None:
    try:
        with pdfplumber.open(str(deck)) as pdf:
            page = pdf.pages[slide - 1]
            if not page.images:
                return None
            im = page.images[0]
            box = (max(im["x0"], 0), max(im["top"], 0), min(im["x1"], page.width), min(im["bottom"], page.height))
            img = page.crop(box).to_image(resolution=CHART_DPI).original.convert("RGB")
    except Exception:  # a chart we cannot render is unreadable (DVB-R8), never a crash
        return None
    return read_bars(img)


def deck_figures(room: Path, deck: Path) -> tuple[list[Figure], str | None]:
    """DVB-R1: every revenue figure the deck shows."""
    uri = deck.relative_to(room).as_posix()
    pages = pdf_pages(deck)
    figures: list[Figure] = []
    m = re.search(r"Data as of (\d{4}-\d{2})-\d{2}", pages[0]) if pages else None
    as_of = m.group(1) if m else None

    rows = []  # (label, printed value, cited slide, source on the claims page or claims.json)
    claims_slide = next((i for i in range(len(pages), 0, -1) if pages[i - 1].startswith("Appendix")), None)
    if claims_slide:
        for line in pages[claims_slide - 1].splitlines():
            mm = re.match(r"(.+?)\s+(\$[\d,.]+[KMB]?)\s+(\d+)$", line)
            if mm and REVENUE_WORDS.search(mm.group(1)):
                rows.append((mm.group(1).strip(), mm.group(2), int(mm.group(3)),
                             _source(uri, f"slide {claims_slide}", line)))
    else:
        for path in find(room, "deck_claims"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for i, r in enumerate(data.get("claims", [])):
                if REVENUE_WORDS.search(r["label"]) and str(r["value"]).startswith("$"):
                    rows.append((r["label"], r["value"], int(r["slide"]),
                                 _source(path.relative_to(room).as_posix(), f"claims[{i}]", f'"value": "{r["value"]}"')))
    for label, printed, slide, row_src in rows:
        number, half = parse_money(printed)
        exact = f"${number:,.0f}"
        short_only = bool(re.search(r"[KMB]$", printed.strip())) and not any(exact in p for p in pages)
        sources = []
        if 1 <= slide <= len(pages):
            for tok in MONEY.findall(pages[slide - 1]):
                v, half = parse_money(tok)
                if abs(v - number) <= max(half, 0.5):
                    sources.append(_source(uri, f"slide {slide}", tok))
                    break
        sources.append(row_src)
        figures.append(Figure("stated", slide, sources, label=label, printed=printed, number=number,
                              half_step=half if short_only else 0.0))

    for i, text in enumerate(pages, 1):
        for line in text.splitlines():
            mm = CAPTION.search(line)
            if mm:
                figures.append(Figure("chart", i, [_source(uri, f"slide {i}", line.strip())],
                                      grain=mm.group(1).lower(), recurring=bool(mm.group(2)),
                                      start=_month(mm.group(3)), end=_month(mm.group(4)),
                                      bars=chart_bars(deck, i)))
            mm = PLAN_GROWTH.search(line)
            if mm:
                figures.append(Figure("plan_growth", i, [_source(uri, f"slide {i}", mm.group(0))], pct=float(mm.group(1))))
            mm = GREW.search(line)
            if mm:
                figures.append(Figure("grew_every_month", i, [_source(uri, f"slide {i}", mm.group(0))], year=int(mm.group(1))))
    return figures, as_of


# --------------------------------------------------------------------------- the books

def load_pnl(room: Path) -> Books | None:
    path = room / MODEL
    if not path.exists():
        return None
    try:
        rows = xlsx_sheet(path, "P&L")
    except (LocatorError, OSError, KeyError):
        return None
    hdr_i = next((i for i, r in enumerate(rows[:15]) if r and r[0] == "Line"), None)
    if hdr_i is None:
        return None
    hdr, kinds = rows[hdr_i], rows[hdr_i + 1]
    cols = {v: j for j, v in enumerate(hdr) if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}", v)}
    lines: dict[str, dict[str, Cell]] = {}
    for i, r in enumerate(rows[hdr_i + 2:], hdr_i + 3):
        if r and r[0] and len(r) > 1 and r[1] == "Revenue":
            lines[r[0]] = {m: Cell(r[j], MODEL, f"P&L!{get_column_letter(j + 1)}{i}", str(r[j]))
                           for m, j in cols.items() if isinstance(r[j], (int, float))}
    if not lines:
        return None
    rec = next((k for k in lines if k.startswith("Recurring revenue")), "Subscription revenue")
    total = "Total revenue" if "Total revenue" in lines else rec
    if rec not in lines:
        rec = total
    actual = [m for m, j in cols.items() if kinds[j] == "Actual"]
    plan = [m for m, j in cols.items() if kinds[j] == "Plan"]
    first = next((m for m in actual if m in lines[total] and lines[total][m].value > 0), None)
    if first is None:
        return None
    return Books(MODEL, actual, plan, lines, rec, total, first)


def load_revenue_rows(room: Path) -> Books | None:
    """DVB-R9: the customer revenue rows summed by month, used only when the P&L is missing."""
    for path in find(room, "customers"):
        cols = ROW_COLUMNS.get(path.name)
        if not cols:
            continue
        uri = path.relative_to(room).as_posix()
        sums: dict[str, float] = {}
        first_row: dict[str, int] = {}
        for n, r in enumerate(csv_rows(path), 2):
            v = sum(float(r[c] or 0) for c in cols)
            sums[r["month"]] = sums.get(r["month"], 0.0) + v
            if v > 0 and r["month"] not in first_row:
                first_row[r["month"]] = n
        months = sorted(sums)
        first = next((m for m in months if sums[m] > 0), None)
        if first is None:
            continue
        line = {}
        for m in months:
            n = first_row.get(m)
            line[m] = Cell(sums[m], uri, f"row {n}" if n else "", csv_row_text(path, n) if n else "")
        label = "revenue summed from " + path.name
        return Books(uri, months, [], {label: line}, label, label, first, is_pnl=False)
    return None


# --------------------------------------------------------------------------- the checks

def describe_hidden(months: list[str], values: list[float], chart_first: float) -> dict:
    """What the months a chart leaves out hold, and whether that is a flag or a watch.

    Flag when they hold a dip (a month below the one before, or a peak above the
    chart's first month) or a flat stretch. Watch when they hold only a climb.
    """
    peak_i = max(range(len(values)), key=lambda i: values[i])
    falls = [months[i] for i in range(1, len(values)) if values[i] < values[i - 1]]
    flat = _flat_stretch(months, values)
    parts = []
    if values[peak_i] > chart_first:
        parts.append(f"hold a peak of {_usd(values[peak_i])} in {months[peak_i]}; revenue then fell "
                     f"{100 * (1 - chart_first / values[peak_i]):.1f}% to {_usd(chart_first)} in the chart's first month")
    if falls:
        parts.append(f"revenue fell month on month in {', '.join(falls)}")
    if flat:
        parts.append(f"revenue was flat from {flat[0]} to {flat[1]}")
    if parts:
        text, severity = "; ".join(parts), "flag"
    else:
        text, severity = f"hold the climb from {_usd(values[0])} to {_usd(values[-1])}, with no fall", "watch"
    return {"text": text, "severity": severity, "peak_month": months[peak_i]}


def describe_after(months: list[str], values: list[float], chart_last: float) -> dict:
    """What the months after a chart's last month hold. Flag when revenue fell below the chart's
    last month, fell month on month, or went flat. Watch when it only kept climbing."""
    low_i = min(range(len(values)), key=lambda i: values[i])
    seq = [chart_last] + list(values)
    falls = [months[i] for i in range(len(values)) if seq[i + 1] < seq[i]]
    flat = _flat_stretch(months, values)
    parts = []
    if values[low_i] < chart_last:
        parts.append(f"revenue fell to {_usd(values[low_i])} in {months[low_i]}, "
                     f"{100 * (1 - values[low_i] / chart_last):.1f}% below the chart's last month ({_usd(chart_last)})")
    if falls:
        parts.append(f"revenue fell month on month in {', '.join(falls)}")
    if flat:
        parts.append(f"revenue was flat from {flat[0]} to {flat[1]}")
    if parts:
        return {"text": "show that " + "; ".join(parts), "severity": "flag", "low_month": months[low_i]}
    return {"text": f"hold the climb from {_usd(values[0])} to {_usd(values[-1])}, with no fall",
            "severity": "watch", "low_month": months[low_i]}


def _stated(f: Figure, books: Books, as_of: str | None, tol: float, out: Out):
    lines, label = books.lines, f.label or ""
    mm = re.search(r"(\w+) (\d{4})$", label)
    rec, total = lines[books.recurring_label], lines[books.total_label]
    if (label == "ARR" or "last 12 months" in label) and as_of is None:
        return _unmatched(f, "the deck states no 'Data as of' month, so the period is unknown", out)
    if label == "ARR" and as_of in rec:
        c = rec[as_of]
        value, cells, period = 12 * c.value, [c], as_of
        basis = f"12 x '{books.recurring_label}' for {as_of}"
        v = Value(number=f.number, unit="USD_per_year", label="arr", period=period)
    elif label.startswith("MRR") and mm and mm.group(1) in MONTHS:
        period = _month(f"{mm.group(1)} {mm.group(2)}")
        line_name = "Subscription revenue" if "Subscription revenue" in lines else books.recurring_label
        if period not in lines[line_name]:
            return _unmatched(f, f"the P&L has no '{line_name}' for {period}", out)
        c = lines[line_name][period]
        value, cells, basis = c.value, [c], f"'{line_name}' for {period}"
        v = Value(number=f.number, unit="USD_per_month", label="mrr", period=period)
    elif "last 12 months" in label and as_of in books.actual:
        i = books.actual.index(as_of)
        months = books.actual[max(0, i - 11):i + 1]
        if len(months) < 12:
            return _unmatched(f, f"the books hold only {len(months)} months up to {as_of}", out)
        cells = [total[m] for m in months]
        value, period = sum(c.value for c in cells), f"{months[0]} to {months[-1]}"
        basis = f"sum of '{books.total_label}', {period}"
        v = Value(number=f.number, unit="USD", label="other", period=period)
    else:
        return _unmatched(f, f"no rule maps the label '{label}' to a P&L line", out)
    if value == 0:
        return _unmatched(f, f"the P&L holds 0 for it ({basis})", out)
    ok = figure_matches(f.number, value, f.half_step, tol)
    gap_rel = abs(f.number - value) / abs(value)
    out.row(f.slide, f.printed, period, _usd(value), basis, f"{100 * gap_rel:.1f}%", ok)
    out.claim(f"The deck's {label} of {_usd(f.number)} (slide {f.slide}) {'matches' if ok else 'differs from'} "
              f"the P&L's {_usd(value)} ({basis}), a gap of {100 * gap_rel:.1f}%"
              + (f", within the rounding of the printed {f.printed}." if ok and gap_rel > tol else "."),
              v, "info" if ok else "flag", CHECK_REVENUE, f.sources + [_cell_source(c) for c in cells])


def _unmatched(f: Figure, reason: str, out: Out):
    what = {"stated": f"{f.label} of {f.printed}", "chart": "revenue chart",
            "plan_growth": f"plan growth of {f.pct}% a month", "grew_every_month": f"claim that revenue grew every month in {f.year}"}[f.kind]
    out.row(f.slide, what, None, "", "not matched: " + reason, "", False)
    out.claim(f"The deck's {what} (slide {f.slide}) is not matched to the books: {reason}.",
              None, "info", CHECK_REVENUE, f.sources)


def _chart(f: Figure, books: Books, tol_shape: float, out: Out):
    window = _range(f.start, f.end)
    cap = f.sources
    line_name = books.recurring_label if f.recurring else books.total_label
    line = books.lines[line_name]
    missing = [m for m in window if m not in books.actual]
    if missing:
        out.gap(f"Not in the room: monthly revenue for {missing[0]} to {missing[-1]}, shown on slide {f.slide}",
                "not stated in the file", f"The monthly P&L for {missing[0]} to {missing[-1]}")
    if f.bars is None:
        out.gap(f"Not in the room: a readable chart on slide {f.slide}", "chart image could not be read",
                "The numbers behind the chart, or a readable copy of the slide")
    elif not books.is_pnl:
        _unmatched(f, "no P&L to match against", out)
    elif not missing:
        if f.grain == "monthly":
            series = [(m, line[m].value) for m in window]
        else:
            q: dict[str, float] = {}
            for m in window:
                q[_quarter(m)] = q.get(_quarter(m), 0) + line[m].value
            series = list(q.items())
        worst = None
        ok = len(f.bars) == len(series)
        if ok:
            top_bar, top_book = max(f.bars), max(v for _, v in series)
            worst = max(abs(b / top_bar - v / top_book) for b, (_, v) in zip(f.bars, series))
            ok = worst <= tol_shape
        unit = "months" if f.grain == "monthly" else "quarters"
        detail = (f" (largest difference {100 * worst:.1f} points of the tallest bar)." if worst is not None
                  else f", because the chart has {len(f.bars)} bars for {len(series)} {unit}.")
        out.row(f.slide, f"chart, {len(f.bars)} bars", f"{window[0]} to {window[-1]}", f"'{line_name}', {len(series)} {unit}",
                "bar height / tallest bar against period / largest period",
                "" if worst is None else f"{100 * worst:.1f} points", ok)
        peak_m = max(window, key=lambda m: line[m].value)
        out.claim(f"The deck's revenue chart on slide {f.slide} has {len(f.bars)} bars for {window[0]} to {window[-1]}; "
                  f"their shape {'matches' if ok else 'does not match'} '{line_name}' in the P&L" + detail,
                  None, "info" if ok else "flag", CHECK_REVENUE,
                  cap + [_cell_source(line[window[0]]), _cell_source(line[peak_m])])
    _history(f, books, window, line, line_name, out)


def _history(f: Figure, books: Books, window: list[str], line: dict[str, Cell], line_name: str, out: Out):
    """DVB-R7: partial history."""
    first = books.first_revenue_month
    left_out = [m for m in books.actual if first <= m < window[0]]
    skipped = len(window) - len(f.bars) if (f.bars is not None and f.grain == "monthly") else 0
    parts, severities, sources = [], [], list(f.sources)
    if left_out and window[0] in line:
        held = describe_hidden(left_out, [line[m].value for m in left_out], line[window[0]].value)
        parts.append(f"starts at {window[0]}, {len(left_out)} months after the first revenue month in the books "
                     f"({first}); the months left out, {left_out[0]} to {left_out[-1]}, {held['text']}")
        severities.append(held["severity"])
        for m in dict.fromkeys([first, held["peak_month"], window[0]]):
            if line[m].locator:
                sources.append(_cell_source(line[m]))
    trailing = [m for m in books.actual if m > window[-1]]
    if trailing and window[-1] in line:
        after = describe_after(trailing, [line[m].value for m in trailing], line[window[-1]].value)
        parts.append(f"ends at {window[-1]}, {len(trailing)} months before the last month in the books "
                     f"({books.actual[-1]}); the months left out after it, {trailing[0]} to {trailing[-1]}, {after['text']}")
        severities.append(after["severity"])
        for m in dict.fromkeys([window[-1], after["low_month"]]):
            if line[m].locator:
                sources.append(_cell_source(line[m]))
    if skipped > 0:
        parts.append(f"shows {len(f.bars)} bars for a {len(window)}-month window, so {skipped} months are skipped")
        severities.append("flag")
    if f.grain == "quarterly":
        inside = [m for m in window if m in line]
        dips = [m for a, m in zip(inside, inside[1:]) if line[m].value < line[a].value]
        parts.append("shows quarters where the books hold months"
                     + (f"; the quarters hide month-on-month falls in {', '.join(dips)}" if dips
                        else "; no month inside a quarter fell"))
        severities.append("flag" if dips else "watch")
    if parts:
        sev = "flag" if "flag" in severities else "watch"
        out.row(f.slide, "chart window", f"{window[0]} to {window[-1]}", f"revenue from {first} to {books.actual[-1]}",
                "chart window against the months the books hold", "", False)
        out.claim(f"Shows part of the history: the revenue chart on slide {f.slide} " + "; it ".join(parts) + ".",
                  Value(number=len(left_out) + len(trailing), unit="months", label="other",
                        period=" and ".join(f"{r[0]} to {r[-1]}" for r in (left_out, trailing) if r) or None),
                  sev, CHECK_HISTORY, sources)
        return
    out.row(f.slide, "chart window", f"{window[0]} to {window[-1]}", f"revenue from {first} to {books.actual[-1]}",
            "chart window against the months the books hold", "", True)
    if window[0] == first:
        text = (f"The revenue chart on slide {f.slide} starts at {window[0]}, the first revenue month in the books, "
                f"and runs to {window[-1]} with no month left out.")
    else:
        text = (f"The revenue chart on slide {f.slide} runs from {window[0]} to {window[-1]}; the books begin at "
                f"{first}, and no month they hold is left out.")
    src = [_cell_source(line[first])] if first in line and line[first].locator else []
    out.claim(text, Value(number=0, unit="months", label="other", period=f"{window[0]} to {window[-1]}"),
              "info", CHECK_HISTORY, list(f.sources) + src)


def _plan_growth(f: Figure, books: Books, tol: float, out: Out):
    rec = books.lines[books.recurring_label]
    seq = books.actual[-1:] + books.plan
    if len(seq) < 2 or any(m not in rec for m in seq):
        return _unmatched(f, f"the plan columns of '{books.recurring_label}' hold no values", out)
    rates = [rec[b].value / rec[a].value - 1 for a, b in zip(seq, seq[1:])]
    lo, hi = 100 * min(rates), 100 * max(rates)
    ok = all(abs(100 * r - f.pct) <= f.pct * tol for r in rates)
    period = f"{books.plan[0]} to {books.plan[-1]}"
    out.row(f.slide, f"{f.pct}% a month (plan)", period, f"plan columns {lo:.2f}% to {hi:.2f}%",
            f"month-on-month growth of '{books.recurring_label}', plan columns", "", ok)
    out.claim(f"The deck's plan growth of {f.pct}% a month (slide {f.slide}) {'matches' if ok else 'differs from'} the "
              f"model's plan columns, which grow {lo:.2f}% to {hi:.2f}% a month. It is a plan, not a period the books hold as actuals.",
              Value(number=f.pct, unit="percent", label="other", period=period), "info" if ok else "flag", CHECK_REVENUE,
              f.sources + [_cell_source(rec[books.plan[0]])])


def _grew(f: Figure, books: Books, out: Out):
    total = books.lines[books.total_label]
    yr = [m for m in books.actual if m.startswith(str(f.year))]
    if not yr:
        return _unmatched(f, f"the books hold no actual month in {f.year}", out)
    falls = [m for a, m in zip(yr, yr[1:]) if total[m].value < total[a].value]
    prev = _ym(f.year - 1, 12)
    ok = not falls
    tail = (f", and changed by {_usd(total[yr[0]].value - total[prev].value)} from {prev} to {yr[0]}."
            if prev in total else ".")
    out.row(f.slide, "grew every month", f"{yr[0]} to {yr[-1]}", "falls in " + (", ".join(falls) or "none"),
            f"'{books.total_label}' month on month", "", ok)
    out.claim(f"The deck says revenue grew every month in {f.year} (slide {f.slide}); in the P&L '{books.total_label}' "
              + (f"rose in every month from {yr[0]} to {yr[-1]}" if ok else "fell in " + ", ".join(falls)) + tail,
              None, "info" if ok else "flag", CHECK_REVENUE,
              f.sources + [_cell_source(total[m]) for m in _cited_months(prev, yr, falls) if m in total])


def _cited_months(prev: str, yr: list[str], falls: list[str]) -> list[str]:
    """The cells behind a "grew every month" claim: each month that fell and the month before it,
    or, when none fell, the month before the year and its first month."""
    if not falls:
        return [prev, yr[0]]
    months = []
    for m in falls:
        months += [yr[yr.index(m) - 1], m]
    return list(dict.fromkeys(months))


def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap], list[Panel]]:
    room = Path(room)
    out = Out(ids)
    decks = find(room, "deck")
    if not decks:
        out.gap("Not in the room: the pitch deck (01_overview/pitch_deck.pdf)", "file missing", "The pitch deck")
        return out.claims, out.gaps, []
    s = settings.load()
    tol, tol_shape = float(s["match_tolerance"]), float(s["chart_shape_tolerance"])
    try:
        figures, as_of = deck_figures(room, decks[0])
    except (LocatorError, OSError) as err:
        out.gap("Not in the room: a readable pitch deck (01_overview/pitch_deck.pdf)", f"the deck could not be read: {err}",
                "A text PDF of the pitch deck")
        return out.claims, out.gaps, []

    books = load_pnl(room)
    if books is None:
        why = "file missing" if not (room / MODEL).exists() else "tab missing"
        out.gap("Not in the room: the monthly P&L (02_financials/financial_model.xlsx, P&L tab)", why,
                "The monthly income statement for every month since the first revenue")
        rows = load_revenue_rows(room)
        for f in figures:
            if f.kind == "chart" and rows is not None:
                window = _range(f.start, f.end)
                line = rows.lines[rows.total_label]
                if all(m in rows.actual for m in window):
                    _unmatched(f, "no P&L to match against", out)
                    _history(f, rows, window, line, rows.total_label, out)
                    continue
            _unmatched(f, "no P&L to match against", out)
        return out.claims, out.gaps, _panel(out)

    for f in figures:
        try:
            if f.kind == "stated":
                _stated(f, books, as_of, tol, out)
            elif f.kind == "chart":
                _chart(f, books, tol_shape, out)
            elif f.kind == "plan_growth":
                _plan_growth(f, books, tol, out)
            elif f.kind == "grew_every_month":
                _grew(f, books, out)
        except (KeyError, ValueError, TypeError, ZeroDivisionError, LocatorError) as err:
            missing = f"month {err.args[0]}" if isinstance(err, KeyError) and err.args else str(err)
            out.gap(f"Not in the room: a P&L revenue value the deck's figure on slide {f.slide} needs",
                    f"blank or missing cell in the P&L: {missing}",
                    "The monthly P&L with a revenue value in every month")
    return out.claims, out.gaps, _panel(out)


def _panel(out: Out) -> list[Panel]:
    if not out.rows:
        return []
    return [Panel(name="deck against the books",
                  columns=["Slide", "Deck figure", "Period", "Books", "How the books figure is made", "Gap", "Within tolerance"],
                  rows=out.rows)]
