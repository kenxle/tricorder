"""Evidence readers: what each document in the room says about one kind of claim.

Each reader takes the room and the Statement being checked and returns
Evidence records, every one with a Source the quote checker can find again
(a named cell, a sheet cell, a CSV row, a PDF line). Readers are scripts; none
calls a model. A reader whose document is not in the room returns no evidence
and names the missing document, so the label step can write the right gap.

Independence (ARCHITECTURE.md, "How the readout is built", step 1): the deck,
the pitch video and its script, the overview, the website, the one-pager and
the cover note are the company's own telling and count as one source. Every
other file is a source of its own.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from schema.claim import Source
from scans.base import find
from scans.claims.kinds import DEPARTMENTS, named_entities
from scans.claims.numbers import mentions, words_to_number

FOUNDER_GROUP = re.compile(r"pitch_deck|claims\.json|pitch_video|company_overview|website_copy|product_one_pager|cover_note")


def independent_group(uri: str) -> str:
    """'founder' for the company's own telling, else the file itself."""
    return "founder" if FOUNDER_GROUP.search(uri) else uri


@dataclass
class Evidence:
    number: float | None
    iso: str | None
    source: Source
    doc: str            # plain words: "financial model", "metrics export"
    row: str | None     # checklist row id of the document
    how: str            # how the script read it: "named cell RUNWAY_MONTHS"
    printed: str        # the figure as the reader shows it
    more: list[Source] = field(default_factory=list)  # the other end of a range a sum or count was made from

    @property
    def sources(self) -> list[Source]:
        return [self.source] + self.more

    @property
    def words(self) -> str:
        """Where and how, for a person: "row 22; column arr, month 2026-09", or the range a sum spans."""
        loc = self.source.locator
        if loc in self.how or "rows " in self.how:
            return self.how
        return f"{loc}; {self.how}"

    @property
    def group(self) -> str:
        return independent_group(self.source.uri)


@dataclass
class Reading:
    evidence: list[Evidence]
    missing: str | None = None   # the document that is not in the room, if that is why there is none
    any_of: bool = False         # a list of figures (every price in the contracts): only a match counts


def _src(room: Path, path: Path, locator: str, quote: str) -> Source:
    return Source(kind="file", uri=str(path.relative_to(room)), locator=locator, quote=quote)


def _fmt(n: float) -> str:
    return f"{n:,.0f}" if abs(n - round(n)) < 1e-9 else f"{n:,.2f}"


# The financial model --------------------------------------------------------


def _model(room: Path) -> Path | None:
    hits = find(room, "model")
    return hits[0] if hits else None


def _named(room: Path, names: tuple[str, ...], percent: bool = False, doc="financial model", row="C19") -> Reading:
    from schema.readers import LocatorError, xlsx_cell

    path = _model(room)
    if path is None:
        return Reading([], "the financial model")
    out = []
    for name in names:
        try:
            value = xlsx_cell(path, name)
        except LocatorError:
            continue
        if value is None:
            continue
        if isinstance(value, str):
            out.append(Evidence(None, value, _src(room, path, name, value), doc, row, f"named cell {name}", value))
            continue
        number = float(value) * (100 if percent and abs(float(value)) <= 1.5 else 1)
        out.append(Evidence(number, None, _src(room, path, name, str(value)), doc, row, f"named cell {name}", _fmt(number)))
        break
    return Reading(out)


def _period_name(st, as_of: str | None, stem: str) -> str:
    month = (as_of or "")[:7].replace("-", "_")
    return f"{stem}_{month}"


def _cap_row(room: Path, pattern: str, percent: bool = False) -> Reading:
    from schema.readers import xlsx_sheet, xlsx_sheet_names

    hits = find(room, "cap_table")
    if not hits:
        return Reading([], "the cap table")
    path = hits[0]
    out = []
    for sheet in xlsx_sheet_names(path):
        for r, row in enumerate(xlsx_sheet(path, sheet), start=1):
            if row and isinstance(row[0], str) and re.search(pattern, row[0], re.I) and len(row) > 1 and isinstance(row[1], (int, float)):
                number = float(row[1]) * (100 if percent and abs(float(row[1])) <= 1.5 else 1)
                out.append(Evidence(number, None, _src(room, path, f"{sheet}!B{r}", str(row[1])), "cap table", "C72",
                                    f"row '{row[0]}', column B", _fmt(number)))
                return Reading(out)
    return Reading(out)


def _team_hires(room: Path) -> Reading:
    from schema.readers import LocatorError, xlsx_cell, xlsx_defined_name

    path = _model(room)
    if path is None:
        return Reading([], "the financial model")
    try:
        after, now = xlsx_cell(path, "EMPLOYEES_AFTER_HIRES"), xlsx_cell(path, "EMPLOYEES_NOW")
    except LocatorError:
        return Reading([])
    a, n = xlsx_defined_name(path, "EMPLOYEES_AFTER_HIRES"), xlsx_defined_name(path, "EMPLOYEES_NOW")
    number = float(after) - float(now)
    source = _src(room, path, "EMPLOYEES_AFTER_HIRES", str(after))
    return Reading([Evidence(number, None, source, "financial model", "C19",
                             f"named cells EMPLOYEES_AFTER_HIRES ({a}, {after}) less EMPLOYEES_NOW ({n}, {now})", _fmt(number))])


# CSV exports ------------------------------------------------------------------


def _csv(room: Path, kind: str):
    from schema.readers import csv_rows

    hits = find(room, kind)
    if kind == "customers":
        hits = [h for h in hits if "customer" in h.name]
    return (hits[0], csv_rows(hits[0])) if hits else (None, [])


def _row_source(room: Path, path: Path, index: int) -> Source:
    from schema.readers import csv_row_text

    return _src(room, path, f"row {index + 2}", csv_row_text(path, index + 2))


def _month_index(rows: list[dict], month: str | None) -> int | None:
    if not month:
        return len(rows) - 1 if rows else None
    for i, r in enumerate(rows):
        if r.get("month") == month:
            return i
    return None


def _metrics(room: Path, st, as_of, columns: tuple[str, ...], scale: float = 1.0) -> Reading:
    path, rows = _csv(room, "metrics")
    if path is None:
        return Reading([], "the metrics export")
    i = _month_index(rows, _period(st, as_of))
    if i is None:
        return Reading([])
    for col in columns:
        if col in rows[i] and rows[i][col] not in ("", None):
            number = float(rows[i][col]) * scale
            how = f"column {col}, month {rows[i]['month']}" + (" times 12" if scale == 12 else "")
            return Reading([Evidence(number, None, _row_source(room, path, i), "metrics export", "C02", how, _fmt(number))])
    return Reading([])


def _period(st, as_of: str | None) -> str | None:
    """The month a statement is about: its own 'September 2026' if it names one, else the data month."""
    for m in mentions(st.quote) if st is not None else []:
        if m.kind_hint == "month" and m.iso:
            return m.iso
    return (as_of or "")[:7] or None


def _revenue_col(rows: list[dict]) -> str | None:
    for col in ("total_revenue", "mrr", "subscription_revenue"):
        if rows and col in rows[0]:
            return col
    return None


def _metrics_ltm(room: Path, st, as_of) -> Reading:
    path, rows = _csv(room, "metrics")
    if path is None:
        return Reading([], "the metrics export")
    col = _revenue_col(rows)
    i = _month_index(rows, (as_of or "")[:7])
    if col is None or i is None or i < 11:
        return Reading([])
    number = sum(float(r[col]) for r in rows[i - 11:i + 1])
    how = f"sum of column {col}, {rows[i - 11]['month']} to {rows[i]['month']} (rows {i - 9} to {i + 2})"
    return Reading([Evidence(number, None, _row_source(room, path, i - 11), "metrics export", "C02", how, _fmt(number),
                             [_row_source(room, path, i)])])


def _metrics_first(room: Path, st, as_of) -> Reading:
    path, rows = _csv(room, "metrics")
    if path is None:
        return Reading([], "the metrics export")
    col = _revenue_col(rows)
    for i, r in enumerate(rows):
        if col and float(r[col] or 0) > 0:
            return Reading([Evidence(None, r["month"], _row_source(room, path, i), "metrics export", "C02",
                                     f"first month with {col} above 0", r["month"])])
    return Reading([])


def _metrics_range(room: Path, st, as_of) -> Reading:
    path, rows = _csv(room, "metrics")
    if path is None:
        return Reading([], "the metrics export")
    first, last = (st.mention.iso or "..").split("..")
    a, b = _month_index(rows, first), _month_index(rows, last)
    if a is None or b is None:
        return Reading([])
    how = f"rows for {first} and {last} exist; the export starts at {rows[0]['month']}"
    iso = f"{first}..{last}"
    how += f" (rows {a + 2} and {b + 2})"
    return Reading([Evidence(None, iso, _row_source(room, path, a), "metrics export", "C02", how, iso,
                             [_row_source(room, path, b)] if b != a else [])])


def _metrics_grew(room: Path, st, as_of) -> Reading:
    path, rows = _csv(room, "metrics")
    if path is None:
        return Reading([], "the metrics export")
    col, year = _revenue_col(rows), st.mention.printed
    idx = [i for i, r in enumerate(rows) if r["month"].startswith(year)]
    if not col or len(idx) < 2:
        return Reading([])
    values = [float(rows[i][col]) for i in idx]
    grew = all(b > a for a, b in zip(values, values[1:]))
    how = (f"column {col}, {rows[idx[0]]['month']} to {rows[idx[-1]]['month']} (rows {idx[0] + 2} to {idx[-1] + 2}): "
           + ("rose every month" if grew else "did not rise every month"))
    return Reading([Evidence(1.0 if grew else 0.0, None, _row_source(room, path, idx[0]), "metrics export", "C02", how,
                             "rose every month" if grew else "did not rise every month", [_row_source(room, path, idx[-1])])])


def _customers(room: Path, st, as_of, what: str) -> Reading:
    path, rows = _csv(room, "customers")
    if path is None:
        return Reading([], "monthly revenue by customer")
    col = "mrr" if rows and "mrr" in rows[0] else "subscription_revenue"
    month = (as_of or "")[:7] or (rows[-1]["month"] if rows else None)
    # Recurring rows only: a pilot or a one-time line is not recurring revenue (checklist C05).
    recurring = (lambda r: r.get("product_type", "Subscription").lower() == "subscription")
    idx = [i for i, r in enumerate(rows) if r["month"] == month and recurring(r)]
    if not idx:
        return Reading([])
    rev = {i: float(rows[i][col] or 0) for i in idx}
    total = sum(rev.values())
    span = f"rows {idx[0] + 2} to {idx[-1] + 2}" + (", product_type Subscription" if "product_type" in rows[0] else "")
    doc, row = "revenue by customer", "C03"

    def ranged(number: float, used: list[int], how: str, printed: str, first: int | None = None) -> Reading:
        """Cite the rows the figure was made from: the first and last of the range."""
        lead = used[0] if first is None else first
        more = [_row_source(room, path, i) for i in sorted({used[0], used[-1]} - {lead})]
        return Reading([Evidence(number, None, _row_source(room, path, lead), doc, row, how, printed, more)])

    if what in ("sum", "arr"):
        number = total * (12 if what == "arr" else 1)
        how = f"sum of column {col} for {month}, {span}" + (", times 12" if what == "arr" else "")
        return ranged(number, idx, how, _fmt(number))
    if what == "count_now":
        paying = [i for i in idx if rev[i] > 0]
        how = f"customers with {col} above 0 in {month}, rows {paying[0] + 2} to {paying[-1] + 2}" if paying else ""
        return ranged(float(len(paying)), paying, how, str(len(paying))) if paying else Reading([])
    if what == "count_ever":
        used = [i for i, r in enumerate(rows) if r["month"] <= month and recurring(r) and float(r[col] or 0) > 0]
        ever = {rows[i]["customer_id"] for i in used}
        how = f"distinct customer_id with {col} above 0 in any month to {month}, rows {used[0] + 2} to {used[-1] + 2}" if used else ""
        return ranged(float(len(ever)), used, how, str(len(ever))) if used else Reading([])
    if what == "largest_share":
        top = max(idx, key=lambda i: rev[i])
        share = 100 * rev[top] / total if total else 0.0
        how = f"{rows[top]['customer_name']} {col} {_fmt(rev[top])} (row {top + 2}) of {_fmt(total)}, the sum for {month}, {span}"
        return ranged(share, idx, how, f"{share:.1f}%", first=top)
    if what == "locations" and "locations" in rows[idx[0]]:
        names = named_entities(st.quote)
        pick = [i for i in idx if any(n.split()[0].lower() in rows[i]["customer_name"].lower() for n in names)] if names else []
        top = pick[0] if pick else max(idx, key=lambda i: rev[i])
        number = float(rows[top]["locations"])
        how = f"column locations for {rows[top]['customer_name']}, {month}" + ("" if pick else " (the largest customer)")
        return Reading([Evidence(number, None, _row_source(room, path, top), doc, row, how, _fmt(number))])
    if what == "invoices" and "carrier_invoices_audited" in rows[idx[0]]:
        number = sum(float(rows[i]["carrier_invoices_audited"] or 0) for i in idx)
        how = f"sum of column carrier_invoices_audited for {month}, {span}"
        return ranged(number, idx, how, _fmt(number))
    return Reading([])


def _hiring(room: Path, st, as_of, what: str) -> Reading:
    path, rows = _csv(room, "hiring_plan")
    if path is None:
        return Reading([], "the hiring plan")
    if not rows:
        return Reading([])
    doc, row = "hiring plan", "C22"
    if what == "count":
        ids = f", {rows[0]['hire_id']} to {rows[-1]['hire_id']}" if "hire_id" in rows[0] else ""
        return Reading([Evidence(float(len(rows)), None, _row_source(room, path, len(rows) - 1), doc, row,
                                 f"{len(rows)} hire rows (rows 2 to {len(rows) + 1}){ids}", str(len(rows)))])
    if what == "last_headcount":
        number = float(rows[-1]["headcount_after_hire"])
        return Reading([Evidence(number, None, _row_source(room, path, len(rows) - 1), doc, row,
                                 "column headcount_after_hire, last row", _fmt(number))])
    if what == "dept":
        line = st.quote.lower()
        dept = next((d for d in DEPARTMENTS if line.startswith(d)), None)
        if dept is None or "department" not in rows[0]:
            return Reading([])
        hits = [i for i, r in enumerate(rows) if r.get("department", "").lower() == dept]
        if not hits:
            return Reading([Evidence(0.0, None, _row_source(room, path, 0), doc, row, f"no rows with department {dept}", "0")])
        return Reading([Evidence(float(len(hits)), None, _row_source(room, path, hits[-1]), doc, row,
                                 f"{len(hits)} rows with department '{rows[hits[0]]['department']}'", str(len(hits)))])
    return Reading([])


# Documents read as text: contracts and bios ----------------------------------------


def _pdf_lines(room: Path, kind: str):
    from schema.readers import pdf_pages

    for path in find(room, kind):
        if path.suffix.lower() != ".pdf" or "sow_" in path.name:
            continue  # a statement of work is a vendor contract, not a customer's
        for n, text in enumerate(pdf_pages(path), start=1):
            for line in text.splitlines():
                yield path, n, line, text


def _pattern(room: Path, kind: str, pattern: str, doc: str, row: str, entity_from=None, percent=False) -> Reading:
    """Every match in the room's contracts (or bios), with the number it states. The
    pattern runs over each page's text, so a phrase a line wrap split still matches;
    the quote is the whole line or lines the match sits on, as the reader returns them."""
    from schema.readers import pdf_pages

    if not find(room, kind):
        return Reading([], {"contracts": "signed customer contracts", "bios": "founder bios"}[kind])
    names = named_entities(entity_from.quote) if entity_from is not None else []
    out = []
    for path in find(room, kind):
        if path.suffix.lower() != ".pdf" or "sow_" in path.name:
            continue  # a statement of work is a vendor contract, not a customer's
        for n, page in enumerate(pdf_pages(path), start=1):
            if entity_from is not None and (not names or not any(name.split()[0] in page for name in names)):
                continue
            for m in re.finditer(pattern.replace(" ", r"\s+"), page):
                raw = m.group(1)
                number = words_to_number(raw) if raw.isalpha() else float(raw.replace(",", ""))
                if number is None:
                    continue
                start = page.rfind("\n", 0, m.start()) + 1
                end = page.find("\n", m.end())
                quote = page[start:end if end != -1 else len(page)].strip()
                out.append(Evidence(number, None, _src(room, path, f"page {n}", quote), doc, row,
                                    f"{path.name}, page {n}", " ".join(m.group(0).split())))
    return Reading(out, any_of=entity_from is None)


def _contract_date(room: Path, st, as_of) -> Reading:
    if not find(room, "contracts"):
        return Reading([], "signed customer contracts")
    names = named_entities(st.quote)
    if not names:
        return Reading([])
    iso = st.mention.iso or ""
    out = []
    for path, n, line, page in _pdf_lines(room, "contracts"):
        if not any(name.split()[0] in page for name in names):
            continue
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", line)
        if any(d.startswith(iso) for d in dates):
            hit = next(d for d in dates if d.startswith(iso))
            out.append(Evidence(None, hit[:len(iso)], _src(room, path, f"page {n}", line.strip()), "customer contract", "C34",
                                f"{path.name}, page {n}", hit))
            break
    return Reading(out)


def _contract_number(room: Path, st, as_of) -> Reading:
    if not find(room, "contracts"):
        return Reading([], "signed customer contracts")
    names = named_entities(st.quote)
    if not names or st.mention.number is None:
        return Reading([])
    target = st.mention.number
    out = []
    for path, n, line, page in _pdf_lines(room, "contracts"):
        if not any(name.split()[0] in page for name in names) or "location" not in line.lower():
            continue
        for m in re.finditer(r"\b(\d+)\b(?!-\d)", line):
            if float(m.group(1)) == target:
                out.append(Evidence(target, None, _src(room, path, f"page {n}", line.strip()), "customer contract", "C34",
                                    f"{path.name}, page {n}", m.group(1)))
                return Reading(out)
    return Reading(out)


def _bios_founded(room: Path, st, as_of) -> Reading:
    reading = _pattern(room, "bios", r"[Ff]ounded [A-Z][\w ]*? in (\d{4})", "founder bios", "C53")
    for e in reading.evidence:
        e.iso, e.printed = str(int(e.number)), str(int(e.number))
    return reading


# The map from reader keys to readers -------------------------------------------

Reader = Callable[[Path, object, str | None], Reading]

READERS: dict[str, Reader] = {
    "model_date": lambda r, st, a: _named(r, ("AS_OF_DATE",)),
    "model_raise": lambda r, st, a: _named(r, ("SERIES_A_RAISE", "SEED_RAISE", "ROUND_RAISE")),
    "model_pre_money": lambda r, st, a: _named(r, ("SEED_PRE_MONEY", "SERIES_A_PRE_MONEY", "PRE_MONEY")),
    "cap_new_money": lambda r, st, a: _cap_row(r, r"^new money"),
    "cap_pre_money": lambda r, st, a: _cap_row(r, r"^pre-money valuation"),
    "cap_ownership": lambda r, st, a: _cap_row(r, r"^(series [a-z]|seed) ownership$", percent=True),
    "model_arr": lambda r, st, a: _named(r, ("ARR_TOTAL",)),
    "metrics_arr": lambda r, st, a: _metrics(r, st, a, ("arr",)),
    "customers_arr": lambda r, st, a: _customers(r, st, a, "arr"),
    "model_mrr": lambda r, st, a: _named(r, (_period_name(st, _period(st, a) or a, "MRR"), _period_name(st, _period(st, a) or a, "SUB_REVENUE"), "MRR_TOTAL")),
    "metrics_mrr": lambda r, st, a: _metrics(r, st, a, ("mrr", "subscription_revenue")),
    "customers_mrr": lambda r, st, a: _customers(r, st, a, "sum"),
    "metrics_revenue_ltm": _metrics_ltm,
    "metrics_range": _metrics_range,
    "metrics_grew": _metrics_grew,
    "metrics_first": _metrics_first,
    "metrics_paying": lambda r, st, a: _metrics(r, st, a, ("paying_accounts", "paying_brokers")),
    "model_paying": lambda r, st, a: _named(r, ("PAYING_BROKERS", "PAYING_ACCOUNTS")),
    "customers_count_now": lambda r, st, a: _customers(r, st, a, "count_now"),
    "customers_count_ever": lambda r, st, a: _customers(r, st, a, "count_ever"),
    "metrics_calls": lambda r, st, a: _metrics(r, st, a, ("calls_handled",)),
    "metrics_invoices": lambda r, st, a: _metrics(r, st, a, ("carrier_invoices_audited",)),
    "customers_invoices": lambda r, st, a: _customers(r, st, a, "invoices"),
    "metrics_invoices_total": lambda r, st, a: _metrics(r, st, a, ("carrier_invoices_audited_since_launch",)),
    "customers_largest_share": lambda r, st, a: _customers(r, st, a, "largest_share"),
    "model_largest_share": lambda r, st, a: Reading([]),
    "contract_number": _contract_number,
    "customers_locations": lambda r, st, a: _customers(r, st, a, "locations"),
    "contract_term": lambda r, st, a: _pattern(r, "contracts", r"(\d+) months, from", "customer contract", "C34", entity_from=st),
    "contract_date": _contract_date,
    "model_gross_margin": lambda r, st, a: _named(r, ("GM_PCT",), percent=True),
    "model_cost_share": lambda r, st, a: _named(r, ("TELEPHONY_PCT",) if re.search(r"phone|telephon", st.quote, re.I) else ("LICENCES_PCT",), percent=True),
    "model_nrr": lambda r, st, a: _named(r, ("NRR_12M",), percent=True),
    "contract_list_price": lambda r, st, a: _pattern(r, "contracts", r"\$([\d,]+) list price", "customer contract", "C34"),
    "contract_onboarding_fee": lambda r, st, a: _pattern(r, "contracts", r"Onboarding fee \$([\d,]+)", "customer contract", "C34"),
    "contract_discount": lambda r, st, a: _pattern(r, "contracts", r"(\d+)% off", "customer contract", "C34"),
    "model_recovery_fee": lambda r, st, a: _named(r, ("RECOVERY_FEE_SHARE",), percent=True),
    "contract_recovery_fee": lambda r, st, a: _pattern(r, "contracts", r"(\d+)% of money recovered", "customer contract", "C34"),
    "model_market_count": lambda r, st, a: _named(r, ("MARKET_CLINICS", "MARKET_BUYERS", "MARKET_COUNT")),
    "model_market_acv": lambda r, st, a: _named(r, ("MARKET_ACV_USD",)),
    "model_tam": lambda r, st, a: _named(r, ("MARKET_TAM_USD",)),
    "model_runway": lambda r, st, a: _named(r, ("RUNWAY_MONTHS",)),
    "model_net_burn": lambda r, st, a: _named(r, ("AVG_NET_BURN_12M",)),
    "model_growth": lambda r, st, a: _named(r, ("REV_GROWTH", "GROWTH_Y1"), percent=True),
    "hiring_count": lambda r, st, a: _hiring(r, st, a, "count"),
    "model_hires": lambda r, st, a: _named(r, ("HIRES_COUNTED",)),
    "team_hires": lambda r, st, a: _team_hires(r),
    "hiring_dept": lambda r, st, a: _hiring(r, st, a, "dept"),
    "model_staff_now": lambda r, st, a: _named(r, ("STAFF_NOW", "EMPLOYEES_NOW")),
    "hiring_last_headcount": lambda r, st, a: _hiring(r, st, a, "last_headcount"),
    "model_staff_after": lambda r, st, a: _named(r, ("EMPLOYEES_AFTER_HIRES", "STAFF_AFTER_HIRES")),
    "bios_years": lambda r, st, a: _pattern(r, "bios", r"\b([a-z]+|\d+) years\b", "founder bios", "C53"),
    "bios_founded": _bios_founded,
}
