"""Sources as a partner reads them: a CSV row with its column names, a cell with its line and column.

    reads_as(source, room_dir, stated) -> "month 2026-09, mrr 186,739, arr 2,240,868, ..."
    fields(source, room_dir) -> [(header, raw value), ...] for a CSV row or a spreadsheet cell
    fmt_number(raw, stated) -> "-$0.24", "$2,240,868", "3.5%", or the raw text when it is not a number

Numbers print the way the memo's claims state them: a figure gets "$" or "%" only
when a claim's own sentence writes it that way. Nothing here computes a new number.
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

from schema.claim import Source
from schema.readers import LocatorError, csv_row_text, xlsx_defined_name, xlsx_sheet

_ROW = re.compile(r"^row (\d+)$")


def _path(source: Source, room_dir: str | Path) -> Path:
    p = Path(source.uri)
    return p if p.is_absolute() else Path(room_dir) / p


def fields(source: Source, room_dir: str | Path) -> list[tuple[str, str]]:
    """Header and value pairs behind a CSV row or a spreadsheet cell; [] for anything else."""
    if source.kind != "file":
        return []
    path = _path(source, room_dir)
    try:
        if path.suffix.lower() == ".csv":
            m = _ROW.match(source.locator.strip())
            if not m or int(m.group(1)) < 2:
                return []
            header = next(csv.reader(io.StringIO(csv_row_text(path, 1))))
            values = next(csv.reader(io.StringIO(csv_row_text(path, int(m.group(1))))))
            return list(zip(header, values))
        if path.suffix.lower() in (".xlsx", ".xlsm"):
            ref = source.locator.strip()
            if "!" not in ref:
                ref = xlsx_defined_name(path, ref)
            sheet, cell = ref.split("!", 1)
            sheet = sheet.strip("'")
            col_letter, row = coordinate_from_string(cell.replace("$", ""))
            col = column_index_from_string(col_letter) - 1
            rows = xlsx_sheet(path, sheet)
            value = rows[row - 1][col] if row - 1 < len(rows) and col < len(rows[row - 1]) else None
            if col == 0:
                return [("sheet", sheet), ("value", "" if value is None else str(value))]
            line = rows[row - 1][0] if col > 0 and isinstance(rows[row - 1][0], str) else None
            column = next((r[col] for r in rows[: row - 1] if col < len(r) and isinstance(r[col], str) and len(r[col]) <= 40), None)
            out = [("sheet", sheet)]
            if line:
                out.append(("line", line))
            if column:
                out.append(("column", column))
            out.append(("value", "" if value is None else str(value)))
            return out
    except (LocatorError, OSError, StopIteration, ValueError, IndexError):
        return []
    return []


_MONEY = re.compile(r"(?:^|[\s_(])(mrr|arr|billings?|fees?|revenue|usd|cash|expenses?|costs?|price|amount)(?:$|[\s_),])", re.I)
_COUNT = re.compile(r"(?:^|[\s_(])(locations?|accounts?|staff|calls?|count|customers?|holders?|headcount|months?)(?:$|[\s_),])", re.I)


def unit_of(label: str) -> str | None:
    """'money' or 'count' from a column or line name, or None when the name does not say."""
    if _COUNT.search(label or ""):
        return "count"
    if _MONEY.search(label or ""):
        return "money"
    return None


def fmt_number(raw: str, stated: str = "", unit: str | None = None) -> str:
    """A number formatted as the claims state it; anything else unchanged.

    A whole number prints with no decimals, any other with two. A column or line
    named for money gets "$"; one named for a count gets none. When the name
    does not say, the figure gets "$" or "%" only when a claim's text writes it so.
    """
    text = raw.strip()
    try:
        v = float(text.replace(",", ""))
    except ValueError:
        return raw
    s = f"{abs(v):,.0f}" if round(v, 2) == round(v) else f"{abs(v):,.2f}"
    sign = "-" if v < 0 and s.strip("0.,") else ""
    if unit == "money":
        return f"{sign}${s}"
    if unit == "count":
        return f"{sign}{s}"
    short = s.rstrip("0").rstrip(".") if "." in s else s
    for form in {s, short}:
        if re.search(rf"\${re.escape(form)}(?![\d,.]\d)(?!\d)", stated):
            return f"{sign}${s}"
        if re.search(rf"(?<![\d.,]){re.escape(sign + form)}%", stated):
            return f"{sign}{form}%"
    return f"{sign}{s}"


def reads_as(source: Source, room_dir: str | Path, stated: str = "") -> str:
    """One plain line for a note or a source panel. Falls back to the quote."""
    pairs = fields(source, room_dir)
    if not pairs:
        if _ROW.match(source.locator.strip() or "") and source.locator.strip() == "row 1" and "," in source.quote:
            return "the column names: " + ", ".join(h.strip() for h in source.quote.split(","))
        return f"\"{source.quote}\""
    d = dict(pairs)
    if "sheet" in d:
        where = ", ".join(x for x in (d["sheet"], d.get("line"), d.get("column")) if x)
        unit = unit_of(d.get("line") or "") or unit_of(d.get("column") or "") or unit_of(d["sheet"])
        return f"{where}: {fmt_number(d['value'], stated, unit)}"
    return ", ".join(f"{h} {fmt_number(v, stated, unit_of(h))}" for h, v in pairs)
