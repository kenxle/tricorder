"""The script rereads a rewrite steer can ask for. A reread changes what is
read, never a check's number: it adds its own line, computed here from the
room's own cells, and the check's line stays beside it.

One reread exists: "treat X as non-recurring" on an ARR line that the
deck-vs-books check (1.14) built from a P&L line counting X as recurring.

    ARR without X = 12 x (that P&L line - the P&L revenue line named for X), same month

On Hollis Voice: 12 x ('Recurring revenue (subscription plus pilot)' 186,739
less 'Pilot revenue' 15,000) for 2026-09 = 2,060,868, the answer key's PF1
true value.
"""

from __future__ import annotations

import re
from pathlib import Path

from openpyxl.utils import get_column_letter

from schema import settings
from schema.claim import Check, Claim, Source, Value
from schema.readers import LocatorError, xlsx_sheet

MODEL = "02_financials/financial_model.xlsx"
SHEET = "P&L"
CHECK = "deck_revenue_vs_pnl.steer"


def usd(v: float) -> str:
    return f"${v:,.0f}"


def pnl_revenue_lines(room: Path) -> dict[str, dict[str, tuple[float, str]]]:
    """{line label: {month: (value, "P&L!W10")}} for the Revenue section, or {}."""
    path = Path(room) / MODEL
    if not path.exists():
        return {}
    try:
        rows = xlsx_sheet(path, SHEET)
    except (LocatorError, OSError):
        return {}
    hdr_i = next((i for i, r in enumerate(rows[:15]) if r and r[0] == "Line"), None)
    if hdr_i is None:
        return {}
    cols = {v: j for j, v in enumerate(rows[hdr_i]) if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}", v)}
    lines: dict[str, dict[str, tuple[float, str]]] = {}
    for i, r in enumerate(rows[hdr_i + 1:], hdr_i + 2):
        if r and isinstance(r[0], str) and len(r) > 1 and r[1] == "Revenue":
            lines[r[0]] = {m: (float(r[j]), f"{SHEET}!{get_column_letter(j + 1)}{i}")
                           for m, j in cols.items() if isinstance(r[j], (int, float))}
    return lines


def _cell_source(value: float, ref: str) -> Source:
    quote = str(int(value)) if float(value).is_integer() else str(value)
    return Source(kind="file", uri=MODEL, locator=ref, quote=quote)


def exclude_from_recurring(term: str, claims: list[Claim], room: Path, new_id) -> tuple[list[Claim], list[str]]:
    """New claims, and notes on what could not be reread. `new_id()` names each new claim."""
    term = term.lower().strip()
    lines = pnl_revenue_lines(room)
    by_ref = {ref: (label, month, value) for label, months in lines.items() for month, (value, ref) in months.items()}
    named = [label for label in lines if term in label.lower() and "recurring" not in label.lower()]
    tol = float(settings.load()["match_tolerance"])
    out, notes = [], []
    targets = [c for c in claims if c.value and c.value.label == "arr" and c.check.name == "deck_revenue_vs_pnl"]
    if not targets:
        return [], [f"No ARR line in this piece is built from the P&L, so '{term}' was not reread."]
    for c in targets:
        cell = next((s for s in c.sources if s.uri == MODEL and s.locator in by_ref), None)
        if cell is None:
            notes.append(f"{c.id} cites no P&L revenue cell, so it was not reread.")
            continue
        rec_label, month, rec_value = by_ref[cell.locator]
        if term not in rec_label.lower():
            notes.append(f"{c.id} reads '{rec_label}', which does not count '{term}', so nothing changes.")
            continue
        if not named:
            notes.append(f"No P&L revenue line names '{term}', so '{rec_label}' cannot be split.")
            continue
        term_label = named[0]
        if month not in lines[term_label]:
            notes.append(f"'{term_label}' has no value for {month}.")
            continue
        term_value, term_ref = lines[term_label][month]
        arr = 12 * (rec_value - term_value)
        stated = c.value.number
        if arr <= 0:
            notes.append(f"'{rec_label}' less '{term_label}' is not above zero for {month}.")
            continue
        gap = abs(stated - arr) / abs(arr)
        deck = [s for s in c.sources if s.uri != MODEL]
        slide = next((s.locator for s in deck), "the deck")
        text = (f"On your steer ({term} treated as non-recurring): ARR is {usd(arr)}, 12 x ('{rec_label}' {usd(rec_value)} "
                f"less '{term_label}' {usd(term_value)}) for {month}, against the deck's {usd(stated)} ({slide}), a gap of {100 * gap:.1f}%.")
        out.append(Claim(id=new_id(), scan="steering", text=text,
                         value=Value(number=arr, unit="USD_per_year", label="arr", period=month),
                         severity="flag" if gap > tol else "info", check=Check(kind="script", name=CHECK, model=None),
                         confidence="computed", sources=deck + [_cell_source(rec_value, cell.locator), _cell_source(term_value, term_ref)],
                         conflicts_with=[], corroborated_by=[]))
    if not named and not out and not any("No P&L revenue line" in n for n in notes):
        notes.append(f"No P&L revenue line names '{term}'.")
    return out, notes
