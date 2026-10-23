"""FRAMEWORKS entry 1.3, cohort retention rebuild: the script half only.

Check name: rebuild_cohorts_from_customer_file (the answer key's PF3).

- The Cohorts tab in financial_model.xlsx: its "All cohorts" row (customers,
  net revenue retention) and its definition note, stated as one claim.
- The raw customer file, 03_metrics/customer_mrr_by_month.csv: each cohort is
  the customers whose first month with MRR above zero is month c. Over the
  cohorts with 12 months of data,
      NRR_12 = SUM MRR_i(c+12) / SUM MRR_i(c)
      GRR_12 = SUM MIN(MRR_i(c+12), MRR_i(c)) / SUM MRR_i(c)
- Flag when the tab counts fewer customers than the rebuild, or its NRR is
  above the rebuilt NRR by more than match_tolerance. A tab NRR below the
  rebuild by more than match_tolerance is a watch that states the difference.
  "Matches" only within match_tolerance and on the same customer count.
  GRR under grr_line is a watch.

The model reading (what the tab's note leaves out, the slide 6 chart) is not
built here; it belongs to the entry's owner. Written by the steering slice so
that "read the full room" on retention has a check to rerun
(docs/features/20261023.05_steering/04_architecture.md).
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from schema import settings
from schema.claim import Check, Claim, Gap, Panel, Source, Value
from schema.readers import LocatorError, csv_row_text, csv_rows, xlsx_sheet
from scans.base import Ids, gap

CHECK = "rebuild_cohorts_from_customer_file"
SCAN = "redflags"
PIECE = "retention"
MODEL = "02_financials/financial_model.xlsx"
CUSTOMERS = "03_metrics/customer_mrr_by_month.csv"
TAB = "Cohorts"
PANEL = "cohort retention rebuild"
SCRIPT = "scans/redflags/cohorts.py"


def _add(month: str, k: int) -> str:
    y, m = map(int, month.split("-"))
    t = y * 12 + m - 1 + k
    return f"{t // 12}-{t % 12 + 1:02d}"


def _col(j: int) -> str:
    from openpyxl.utils import get_column_letter

    return get_column_letter(j + 1)


def _claim(ids: Ids, text: str, value: Value, severity: str, sources: list[Source], conflicts: list[str] | None = None) -> Claim:
    return Claim(id=ids(), scan=SCAN, text=text, value=value, severity=severity,
                 check=Check(kind="script", name=CHECK, model=None), confidence="computed",
                 sources=sources, conflicts_with=conflicts or [], corroborated_by=[])


def read_tab(room: Path) -> dict | None:
    """The tab's 'All cohorts' row and its note, with cell addresses, or None."""
    path = room / MODEL
    if not path.exists():
        return None
    try:
        rows = xlsx_sheet(path, TAB)
    except (LocatorError, OSError, KeyError):
        return None
    hdr_i = next((i for i, r in enumerate(rows) if r and isinstance(r[0], str) and r[0].startswith("Cohort (")), None)
    total_i = next((i for i, r in enumerate(rows) if r and r[0] == "All cohorts"), None)
    if hdr_i is None or total_i is None:
        return None
    hdr = rows[hdr_i]
    try:
        jc, jn = hdr.index("Customers"), hdr.index("Net revenue retention")
    except ValueError:
        return None
    total = rows[total_i]
    note_i = next((i for i, r in enumerate(rows[:hdr_i]) if r and isinstance(r[0], str) and r[0].startswith("Cohort =")), None)
    cohorts = sum(1 for r in rows[hdr_i + 1:total_i] if r and r[0])
    return {
        "customers": int(total[jc]), "nrr": 100 * float(total[jn]), "cohorts": cohorts,
        "customers_cell": f"{TAB}!{_col(jc)}{total_i + 1}", "customers_raw": str(total[jc]),
        "nrr_cell": f"{TAB}!{_col(jn)}{total_i + 1}", "nrr_raw": str(total[jn]),
        "note": rows[note_i][0] if note_i is not None else None,
        "note_cell": f"{TAB}!A{note_i + 1}" if note_i is not None else None,
    }


_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def _readable(r: dict) -> tuple[str, str, float] | None:
    """(customer, month, mrr) for a row the script can sum, or None for a row it must skip.
    A blank mrr reads as 0, as before; a blank or malformed month, a blank customer, or text in mrr is skipped."""
    cid, month = (r.get("customer_id") or "").strip(), (r.get("month") or "").strip()
    if not cid or not _MONTH.match(month):
        return None
    try:
        return cid, month, float(r.get("mrr") or 0)
    except ValueError:
        return None


def rebuild(room: Path) -> dict | None:
    """NRR_12 and GRR_12 from the customer file, with the file rows each cohort sums, or None when it is missing.
    Rows the script cannot read are skipped and counted (`skipped`, `read`), never fatal; with no readable row,
    or no cohort with 12 months of data, the dict has no "nrr"."""
    path = room / CUSTOMERS
    if not path.exists():
        return None
    mrr: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    rows_at: dict[tuple[str, str], list[int]] = defaultdict(list)
    skipped: list[int] = []
    read = 0
    for n, r in enumerate(csv_rows(path), 2):
        read += 1
        got = _readable(r)
        if got is None:
            skipped.append(n)
            continue
        cid, month, v = got
        mrr[cid][month] += v
        if v:  # a row with no MRR adds nothing to the sums, so the panel does not list it
            rows_at[(cid, month)].append(n)
    counted = {"skipped": skipped, "read": read}
    if not mrr:
        return counted
    last = max(m for d in mrr.values() for m in d)
    by_cohort: dict[str, dict] = {}
    for cid, d in mrr.items():
        first = min((m for m, v in d.items() if v > 0), default=None)
        if first is None or _add(first, 12) > last:
            continue
        later = _add(first, 12)
        s_, e_ = d[first], d.get(later, 0.0)
        c = by_cohort.setdefault(first, {"customers": 0, "start": 0.0, "end": 0.0, "kept": 0.0, "start_rows": [], "end_rows": []})
        c["customers"] += 1
        c["start"] += s_
        c["end"] += e_
        c["kept"] += min(s_, e_)
        c["start_rows"] += rows_at[(cid, first)]
        c["end_rows"] += rows_at.get((cid, later), [])
    start = sum(c["start"] for c in by_cohort.values())
    if not by_cohort or start == 0:
        return counted
    end = sum(c["end"] for c in by_cohort.values())
    kept = sum(c["kept"] for c in by_cohort.values())
    months = sorted(by_cohort)
    return {"customers": sum(c["customers"] for c in by_cohort.values()), "cohorts": len(months),
            "first": months[0], "last": months[-1], "nrr": 100 * end / start, "grr": 100 * kept / start,
            "by_cohort": {m: by_cohort[m] for m in months}, "header": csv_row_text(path, 1), **counted}


def _money(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else f"{v:.2f}"


def rows_panel(built: dict) -> Panel:
    """Every row the rebuild summed, by cohort, so each retention line opens its rows."""
    rows = []
    for month, c in built["by_cohort"].items():
        rows.append([month, str(c["customers"]), _money(c["start"]), _money(c["end"]), _money(c["kept"]),
                     ", ".join(str(r) for r in sorted(c["start_rows"])), ", ".join(str(r) for r in sorted(c["end_rows"]))])
    return Panel(name=PANEL, columns=["Cohort", "Customers", "MRR in the first month", "MRR 12 months later",
                                      "MRR kept (capped at the first month)", f"Rows in {CUSTOMERS}, first month",
                                      f"Rows in {CUSTOMERS}, 12 months later"], rows=rows)


def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap], list[Panel]]:
    room = Path(room)
    s = settings.load()
    tol, grr_line = float(s["match_tolerance"]), float(s["grr_line"])
    claims: list[Claim] = []
    gaps: list[Gap] = []
    tab, built = read_tab(room), rebuild(room)

    tab_claim = None
    if tab is None:
        gaps.append(gap("Not in the room: the Cohorts tab in financial_model.xlsx", "tab missing" if (room / MODEL).exists() else "file missing",
                        "The company's cohort retention table, with the cohort definition", PIECE))
    else:
        sources = [Source(kind="file", uri=MODEL, locator=tab["nrr_cell"], quote=tab["nrr_raw"]),
                   Source(kind="file", uri=MODEL, locator=tab["customers_cell"], quote=tab["customers_raw"])]
        definition = ""
        if tab["note"]:
            sources.append(Source(kind="file", uri=MODEL, locator=tab["note_cell"], quote=tab["note"]))
            definition = f' The tab defines a cohort as "{tab["note"].removeprefix("Cohort = ")}".'
        tab_claim = _claim(ids, f"The Cohorts tab states 12-month net revenue retention of {tab['nrr']:.1f}% "
                                f"for {tab['customers']} customers in {tab['cohorts']} cohorts.{definition}",
                           Value(number=round(tab["nrr"], 2), unit="percent", label="nrr_12m", period=None), "info", sources)
        claims.append(tab_claim)

    if built is None:
        gaps.append(gap(f"Not in the room: the customer file ({CUSTOMERS}), so the cohorts cannot be rebuilt",
                        "file missing", "Monthly revenue by customer since the first sale, with MRR per month", PIECE))
        return claims, gaps, []
    if built["skipped"]:
        rows = built["skipped"]
        listed = ", ".join(map(str, rows[:10])) + (f" and {len(rows) - 10} more" if len(rows) > 10 else "")
        gaps.append(gap(f"Not in the room: a customer, a month (YYYY-MM) and a number for MRR in every row of the customer file ({CUSTOMERS})",
                        f"{len(rows)} of {built['read']} rows could not be read and were skipped: rows {listed}",
                        "the same export with every row filled in", PIECE))
    if "nrr" not in built:
        gaps.append(gap(f"Not in the room: 12 months of readable rows in the customer file ({CUSTOMERS}), so the cohorts cannot be rebuilt",
                        f"no cohort has 12 months of data in the {built['read'] - len(built['skipped'])} rows read",
                        "Monthly revenue by customer since the first sale, with MRR per month", PIECE))
        return claims, gaps, []

    # The header row: the columns the script summed. The rows themselves are in the panel, one list per cohort.
    row_source = Source(kind="file", uri=CUSTOMERS, locator="row 1", quote=built["header"])
    span = f"the {built['cohorts']} cohorts from {built['first']} to {built['last']} that have 12 months of data"
    how = f" {SCRIPT} summed the mrr column of the rows listed in the panel '{PANEL}'." + (
        f" It skipped {len(built['skipped'])} row{'s' if len(built['skipped']) != 1 else ''} it could not read (see the gaps)."
        if built["skipped"] else "")
    if tab is not None:
        fewer = tab["customers"] < built["customers"]
        diff = tab["nrr"] - built["nrr"]
        within = abs(diff) / built["nrr"] <= tol
        above = diff > 0 and not within
        severity = "flag" if (fewer or above) else ("info" if within else "watch")
        theirs = f"{tab['nrr']:.1f}% over {tab['customers']} customers"
        if severity == "flag":
            compare = (f", against {theirs} in the Cohorts tab: {abs(diff):.1f} points {'lower' if diff > 0 else 'higher'}"
                       + (f", and the tab counts {built['customers'] - tab['customers']} customers fewer." if fewer else "."))
        elif not within:  # the tab is below the rebuild by more than the tolerance: stated, never called a match
            compare = f", which is {abs(diff):.1f} points higher than the Cohorts tab's {theirs}."
        elif tab["customers"] == built["customers"]:
            compare = f", which matches the Cohorts tab's {theirs}."
        else:
            compare = (f", within {100 * tol:.0f}% of the Cohorts tab's {theirs}, "
                       f"though the tab counts {tab['customers'] - built['customers']} customers more.")
        sources = [row_source, Source(kind="file", uri=MODEL, locator=tab["nrr_cell"], quote=tab["nrr_raw"])]
        conflicts = [tab_claim.id] if severity == "flag" else []
    else:
        severity, compare, sources, conflicts = "info", ". The room has no Cohorts tab to compare it with.", [row_source], []
    claims.append(_claim(ids, f"Rebuilt from the customer file, 12-month net revenue retention is {built['nrr']:.1f}% over "
                              f"{built['customers']} customers in {span}{compare}",
                         Value(number=round(built["nrr"], 2), unit="percent", label="nrr_12m", period=None),
                         severity, sources, conflicts))
    claims[-1] = claims[-1].model_copy(update={"text": claims[-1].text + how})
    under = built["grr"] < grr_line
    claims.append(_claim(ids, f"Rebuilt 12-month gross revenue retention is {built['grr']:.1f}% over the same {built['customers']} customers, "
                              f"{'under' if under else 'at or above'} the {grr_line:.0f}% line.",
                         Value(number=round(built["grr"], 2), unit="percent", label="grr_12m", period=None),
                         "watch" if under else "info", [row_source]))
    claims[-1] = claims[-1].model_copy(update={"text": claims[-1].text + how})
    return claims, gaps, [rows_panel(built)]
