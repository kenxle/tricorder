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
  above the rebuilt NRR by more than match_tolerance. GRR under grr_line is a
  watch.

The model reading (what the tab's note leaves out, the slide 6 chart) is not
built here; it belongs to the entry's owner. Written by the steering slice so
that "read the full room" on retention has a check to rerun
(docs/features/20261023.05_steering/04_architecture.md).
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from schema import settings
from schema.claim import Check, Claim, Gap, Source, Value
from schema.readers import LocatorError, csv_row_text, csv_rows, xlsx_sheet
from scans.base import Ids, gap

CHECK = "rebuild_cohorts_from_customer_file"
SCAN = "redflags"
PIECE = "retention"
MODEL = "02_financials/financial_model.xlsx"
CUSTOMERS = "03_metrics/customer_mrr_by_month.csv"
TAB = "Cohorts"


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


def rebuild(room: Path) -> dict | None:
    """NRR_12 and GRR_12 from the customer file, or None when it is missing."""
    path = room / CUSTOMERS
    if not path.exists():
        return None
    mrr: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    first_row: dict[tuple[str, str], int] = {}
    for n, r in enumerate(csv_rows(path), 2):
        v = float(r.get("mrr") or 0)
        mrr[r["customer_id"]][r["month"]] += v
        if v > 0:
            first_row.setdefault((r["customer_id"], r["month"]), n)
    if not mrr:
        return None
    last = max(m for d in mrr.values() for m in d)
    start = end = capped = 0.0
    members: list[tuple[str, str]] = []
    for cid, d in mrr.items():
        first = min((m for m, v in d.items() if v > 0), default=None)
        if first is None or _add(first, 12) > last:
            continue
        s, e = d[first], d.get(_add(first, 12), 0.0)
        start, end, capped = start + s, end + e, capped + min(s, e)
        members.append((first, cid))
    if not members or start == 0:
        return None
    members.sort()
    row = first_row[(members[0][1], members[0][0])]
    return {"customers": len(members), "cohorts": len({m for m, _ in members}),
            "first": members[0][0], "last": members[-1][0],
            "nrr": 100 * end / start, "grr": 100 * capped / start,
            "row": row, "row_text": csv_row_text(path, row)}


def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap]]:
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
        return claims, gaps

    row_source = Source(kind="file", uri=CUSTOMERS, locator=f"row {built['row']}", quote=built["row_text"])
    span = f"the {built['cohorts']} cohorts from {built['first']} to {built['last']} that have 12 months of data"
    if tab is not None:
        fewer = tab["customers"] < built["customers"]
        above = tab["nrr"] > built["nrr"] and abs(tab["nrr"] - built["nrr"]) / built["nrr"] > tol
        severity = "flag" if (fewer or above) else "info"
        diff = tab["nrr"] - built["nrr"]
        compare = (f", against {tab['nrr']:.1f}% over {tab['customers']} customers in the Cohorts tab: "
                   f"{abs(diff):.1f} points {'lower' if diff > 0 else 'higher'}"
                   + (f", and the tab counts {built['customers'] - tab['customers']} customers fewer." if fewer else ".")
                   if severity == "flag" else f", which matches the Cohorts tab's {tab['nrr']:.1f}% over {tab['customers']} customers.")
        sources = [row_source, Source(kind="file", uri=MODEL, locator=tab["nrr_cell"], quote=tab["nrr_raw"])]
        conflicts = [tab_claim.id] if severity == "flag" else []
    else:
        severity, compare, sources, conflicts = "info", ". The room has no Cohorts tab to compare it with.", [row_source], []
    claims.append(_claim(ids, f"Rebuilt from the customer file, 12-month net revenue retention is {built['nrr']:.1f}% over "
                              f"{built['customers']} customers in {span}{compare}",
                         Value(number=round(built["nrr"], 2), unit="percent", label="nrr_12m", period=None),
                         severity, sources, conflicts))
    under = built["grr"] < grr_line
    claims.append(_claim(ids, f"Rebuilt 12-month gross revenue retention is {built['grr']:.1f}% over the same {built['customers']} customers, "
                              f"{'under' if under else 'at or above'} the {grr_line:.0f}% line.",
                         Value(number=round(built["grr"], 2), unit="percent", label="grr_12m", period=None),
                         "watch" if under else "info", [row_source]))
    return claims, gaps
