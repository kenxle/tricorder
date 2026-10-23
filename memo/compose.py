"""Memo-local composition: one plain sentence from several claims' values and sources.

The merge's link step (not built yet) will say which claims agree or disagree.
Until then the memo puts the ARR figures side by side itself, from what the
claims already hold: a claim's own value when its label is "arr", and any
source a claim cites whose column or line is named ARR (a CSV column "arr", a
spreadsheet line named ARR, or an ARR column on a row that a flag cites).
Every figure is copied from a claim or a
cited source and linked to the claims that cite it. No figure is computed here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from schema.claim import Claim

from memo.sources import fields, fmt_number

_ARR = re.compile(r"\barr\b", re.I)


@dataclass
class Figure:
    number: float
    where: str
    claim_ids: list[str] = field(default_factory=list)


def _num(raw: str) -> float | None:
    try:
        return float(str(raw).replace(",", "").replace("$", ""))
    except ValueError:
        return None


def arr_figures(claims: list[Claim], room_dir: str | Path) -> list[Figure]:
    """Distinct ARR figures in the claims and their sources, largest first."""
    found: dict[float, Figure] = {}

    def add(n: float, where: str, cid: str) -> None:
        f = found.setdefault(round(n, 2), Figure(n, where))
        if cid not in f.claim_ids:
            f.claim_ids.append(cid)

    for c in claims:
        if c.value and c.value.label == "arr" and c.value.unit in ("USD", "USD_per_year"):
            s = c.sources[0]
            add(c.value.number, f"{Path(s.uri).name}, {s.locator}", c.id)
    for c in claims:
        for s in c.sources:
            pairs = fields(s, room_dir)
            if not pairs:
                continue
            d = dict(pairs)
            name = Path(s.uri).name
            # A flag about ARR or MRR brings the ARR column of the rows it cites; a flag about
            # something else (paying customers on the same row) does not.
            flagged = c.severity == "flag" and (bool(c.value and c.value.label in ("arr", "mrr")) or bool(_ARR.search(c.text)))
            if "sheet" in d:
                # A line named ARR (a total), or an ARR column on a line a flag cites.
                if _ARR.search(d.get("line") or "") or (flagged and _ARR.search(d.get("column") or "")):
                    n = _num(d["value"])
                    if n:
                        where = ", ".join(x for x in (name, d["sheet"], d.get("line"), d.get("column")) if x)
                        add(n, where, c.id)
            else:
                for h, v in pairs:
                    if flagged and _ARR.fullmatch(h.strip()) and (n := _num(v)):
                        add(n, f"{name}, {s.locator}, column {h} for {pairs[0][1]}", c.id)
    return sorted(found.values(), key=lambda f: -f.number)


def arr_side_by_side(claims: list[Claim], room_dir: str | Path) -> tuple[str, list[str]] | None:
    """The sentence and the claim ids behind it, when the room holds two or more ARR figures."""
    figs = arr_figures(claims, room_dir)
    if len(figs) < 2:
        return None
    stated = " ".join(c.text for c in claims)
    parts = [f"{fmt_number(str(f.number), stated, 'money')} ({f.where})" for f in figs]
    ids: list[str] = []
    for f in figs:
        ids += [i for i in f.claim_ids if i not in ids]
    return f"The room gives {len(figs)} ARR figures, side by side: " + "; ".join(parts) + ".", ids
