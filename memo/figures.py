"""The two numbers behind a red flag: what the pitch states and what the rest of the room shows.

    flag_figures(memo, line) -> [Figure(role="stated" | "found" | "amount", ...), ...]
    fmt(number, unit) -> "$2,240,868", "87.3%", "212"
    short(number, unit) -> "$2.24M", "87%", "212"  (axis labels only)
    scale(figures) -> (lo, hi), a rounded range that holds every figure

The page draws these as two figures side by side and a range strip. Every
number is read from the memo's own claims: a claim's value, a conflicting
claim's value, or the figure a claim's own sentence says the room holds
("... but metrics export (row 22; ...) says 212, 40.6% lower"). Nothing here
computes a new figure; it only picks, groups and formats the ones the claims
already state.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

from schema.claim import Claim

from memo.model import Memo, MemoLine


@dataclass
class Figure:
    number: float
    unit: str
    role: str  # "stated" (the pitch), "found" (the rest of the room) or "amount" (a flag's one figure)
    where: list[str] = field(default_factory=list)
    spoken: bool = False  # said in the pitch video, so rounded by the speaker
    claim_ids: list[str] = field(default_factory=list)


def _is_pitch(uri: str) -> bool:
    return Path(uri).name.startswith("pitch_")


def _where(claim: Claim) -> str:
    s = claim.sources[0]
    return f"{Path(s.uri).name}, {s.locator}"


# "<who> says 212" inside a claim_support sentence. <who> runs back to "but " or "; " outside brackets.
_SAYS = re.compile(r"\bsays (-?\d[\d,]*(?:\.\d+)?)(%?)")


def _who(text: str, end: int) -> str:
    depth, i = 0, end
    while i > 0:
        i -= 1
        ch = text[i]
        if ch == ")":
            depth += 1
        elif ch == "(":
            depth -= 1
        elif depth == 0 and (text.startswith("but ", i) or text.startswith("; ", i)):
            start = i + (4 if text.startswith("but ", i) else 2)
            return re.sub(r"\s*\([^()]*(?:\([^()]*\)[^()]*)*\)", "", text[start:end]).strip()
    return ""


def said_in_room(claim: Claim) -> list[tuple[float, str]]:
    """The figures a claim's sentence says other files hold, with who holds each."""
    out = []
    for m in _SAYS.finditer(claim.text):
        try:
            n = float(m.group(1).replace(",", ""))
        except ValueError:
            continue
        out.append((n, _who(claim.text, m.start()) or "the room"))
    return out


def _add(figs: list[Figure], number: float, unit: str, role: str, where: str, cid: str, spoken: bool = False) -> None:
    for f in figs:
        if f.role == role and round(f.number, 1) == round(number, 1):
            if where and where not in f.where:
                f.where.append(where)
            if cid not in f.claim_ids:
                f.claim_ids.append(cid)
            f.spoken = f.spoken and spoken
            return
    figs.append(Figure(number, unit, role, [where] if where else [], spoken, [cid]))


def flag_figures(memo: Memo, line: MemoLine) -> list[Figure]:
    """Stated and found figures for a red-flag line, stated first. [] when its claims hold none."""
    figs: list[Figure] = []
    claims = [memo.claims[c] for c in line.claim_ids if c in memo.claims]
    flagged = [c for c in claims if c.value and c.severity == "flag"]
    labels = {c.value.label for c in flagged if c.value and _is_pitch(c.sources[0].uri)}
    for c in flagged:
        v = c.value
        if _is_pitch(c.sources[0].uri):
            _add(figs, v.number, v.unit, "stated", _where(c), c.id, spoken=c.sources[0].uri.endswith(".md") and "video" in c.sources[0].uri)
            for n, who in said_in_room(c):
                _add(figs, n, v.unit, "found", who, c.id)
        elif c.conflicts_with and (not labels or v.label in labels):
            # A check rebuilt the figure; the claims it conflicts with hold what was stated.
            _add(figs, v.number, v.unit, "found", f"rebuilt from {Path(c.sources[0].uri).name}", c.id)
            for other in c.conflicts_with:
                o = memo.claims.get(other)
                if o and o.value and o.value.label == v.label:
                    _add(figs, o.value.number, o.value.unit, "stated", _where(o), o.id)
    if not any(f.role == "stated" for f in figs) or not any(f.role == "found" for f in figs):
        figs = []
        first = next((c for c in claims if c.value and c.severity == "flag"), None)
        if first:
            figs.append(Figure(first.value.number, first.value.unit, "amount",
                               [first.value.period] if first.value.period else [], False, [first.id]))
        return figs
    return sorted(figs, key=lambda f: (f.role != "stated", -f.number))


def fmt(number: float, unit: str) -> str:
    if unit == "percent":
        return f"{number:,.1f}".rstrip("0").rstrip(".") + "%"
    whole = round(number, 2) == round(number) or (unit.startswith("USD") and abs(number) >= 100)
    s = f"{abs(number):,.0f}" if whole else f"{abs(number):,.2f}"
    sign = "-" if number < 0 else ""
    return f"{sign}${s}" if unit.startswith("USD") else f"{sign}{s}"


def short(number: float, unit: str) -> str:
    if unit.startswith("USD"):
        a = abs(number)
        if a >= 1_000_000:
            body = f"{a / 1_000_000:.2f}".rstrip("0").rstrip(".") + "M"
        elif a >= 10_000:
            body = f"{a / 1_000:.0f}K"
        else:
            body = f"{a:,.0f}"
        return ("-" if number < 0 else "") + "$" + body
    if unit == "percent":
        return f"{number:.0f}%"
    return f"{number:,.0f}"


def _nice(step: float) -> float:
    if step <= 0:
        return 1.0
    p = 10 ** math.floor(math.log10(step))
    for m in (1, 2, 2.5, 5, 10):
        if step <= m * p:
            return m * p
    return 10 * p


def scale(figs: list[Figure]) -> tuple[float, float]:
    """A rounded range with room either side, from 0 when the figures sit near it."""
    nums = [f.number for f in figs]
    lo, hi = min(nums), max(nums)
    span = hi - lo or abs(hi) or 1.0
    step = _nice(span / 3)
    a = math.floor((lo - span * 0.3) / step) * step
    b = math.ceil((hi + span * 0.3) / step) * step
    if lo >= 0 and (a < 0 or a < span * 0.5):
        a = 0.0
    return a, b


def position(number: float, lo: float, hi: float) -> float:
    """Where a figure sits on the strip, in percent of its width."""
    return round(100 * (number - lo) / (hi - lo), 2) if hi > lo else 50.0
