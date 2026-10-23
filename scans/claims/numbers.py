"""Find every printed or spoken figure in a line of text.

A script, not a model: each figure becomes a Mention with its exact span, the
number it states, its unit, how precisely it is printed, and any hedge word
("about", "under", "close to") in front of it. Slide footers ("Slide 3 of 14")
and clock times ("4:47 pm", the script's "0:35" beats) are not figures.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december")

ONES = {w: i for i, w in enumerate((
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"))}
TENS = {w: 10 * i for i, w in enumerate(("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")) if w}
SCALES = {"hundred": 100, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000}
NUMBER_WORD = "|".join(sorted(list(ONES) + list(TENS) + list(SCALES), key=len, reverse=True))

# A counted thing after a spoken number. Without one, "one-room practices" would count.
UNIT_NOUNS = ("dollars", "percent", "years", "year", "months", "month", "weeks", "days", "people", "locations",
              "location", "cohorts", "clinics", "brokers", "hires", "employees", "customers", "staff")

# Hedges and bounds, longest first. bound "max": the figure is a ceiling; "min": a floor.
HEDGES: tuple[tuple[str, str | None], ...] = (
    ("a little over", "min"), ("a little under", "max"), ("close to", None), ("more than", "min"),
    ("less than", "max"), ("at least", "min"), ("up to", "max"), ("about", None), ("around", None),
    ("nearly", None), ("almost", None), ("roughly", None), ("approximately", None), ("near", None),
    ("under", "max"), ("below", "max"), ("over", "min"), ("above", "min"),
)

_SKIP = re.compile(r"Synthetic data room for [^.]*\.|Slide \d+ of \d+|Page \d+(?: of \d+)?$|\b\d{1,2}:\d{2}(?:\s?[ap]\.?m\.?)?", re.I)

_PATTERN = re.compile(
    r"(?P<iso>\b\d{4}-\d{2}-\d{2}\b)"
    r"|(?P<ym>\b\d{4}-\d{2}\b)"
    r"|(?P<monthyear>\b(?:" + "|".join(MONTHS) + r")\s+\d{4}\b)"
    r"|(?P<cur>\$\d[\d,]*(?:\.\d+)?(?:\s?(?:K|M|B)\b|\s(?:million|thousand|billion)\b)?)"
    r"|(?P<pct>\b\d+(?:\.\d+)?%)"
    r"|(?P<num>\b\d[\d,]*(?:\.\d+)?\b)"
    r"|(?P<words>\b(?:(?:" + NUMBER_WORD + r")(?:[\s-]+(?:and\s+)?)?)+?(?:" + NUMBER_WORD + r")?\b(?=\s+(?:"
    + "|".join(UNIT_NOUNS) + r")\b))",
    re.I,
)
_UNIT_WORD = re.compile(r"\s*([A-Za-z][A-Za-z-]*)")
_SUFFIX = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000}


@dataclass
class Mention:
    start: int
    end: int
    printed: str
    number: float | None
    unit: str | None          # "USD", "percent" or None (a count, a duration or a date)
    unit_word: str | None     # the word after the figure: "months", "hires", "locations"
    precision: float          # half of this is the rounding the printed form allows
    kind_hint: str            # currency, percent, number, year, date, month, words
    iso: str | None = None    # dates: "2026-09-30" or "2026-09"
    hedge: str | None = None
    bound: str | None = None
    spoken: bool = False


def words_to_number(text: str) -> float | None:
    """'three million' -> 3000000, 'twenty-four' -> 24, 'one hundred' -> 100."""
    total, current, seen = 0, 0, False
    for word in re.split(r"[\s-]+", text.lower().strip()):
        if word in ("", "and"):
            continue
        if word in ONES:
            current += ONES[word]
        elif word in TENS:
            current += TENS[word]
        elif word == "hundred":
            current = (current or 1) * 100
        elif word in SCALES:
            total += (current or 1) * SCALES[word]
            current = 0
        else:
            return None
        seen = True
    return float(total + current) if seen else None


def parse_spoken(text: str) -> tuple[float | None, str | None]:
    """'nine million dollars' -> (9000000, 'USD')."""
    found = mentions(text)
    return (found[0].number, found[0].unit) if found else (None, None)


def _hedge_before(text: str, start: int) -> tuple[str | None, str | None]:
    before = text[:start].lower().rstrip()
    for word, bound in HEDGES:
        if re.search(r"(?:^|[\s(])" + re.escape(word) + r"$", before):
            # "No customer above 9%" is a ceiling, not a floor.
            if bound == "min" and re.search(r"\bno\b[^.,;]*$", before[: len(before) - len(word)]):
                bound = "max"
            return word, bound
    return None, None


def _unit_word_after(text: str, end: int) -> str | None:
    m = _UNIT_WORD.match(text, end)
    return m.group(1).lower() if m else None


def _decimals(digits: str) -> int:
    return len(digits.split(".")[1]) if "." in digits else 0


def mentions(text: str) -> list[Mention]:
    """Every figure in one line or sentence, left to right."""
    masked = _SKIP.sub(lambda m: " " * len(m.group(0)), text)
    out: list[Mention] = []
    for m in _PATTERN.finditer(masked):
        s, e, group = m.start(), m.end(), m.lastgroup
        printed = text[s:e]
        hedge, bound = _hedge_before(text, s)
        unit_word = _unit_word_after(text, e)
        if group == "iso":
            out.append(Mention(s, e, printed, None, None, None, 1, "date", iso=printed))
        elif group == "ym":
            out.append(Mention(s, e, printed, None, None, None, 1, "month", iso=printed))
        elif group == "monthyear":
            month, year = printed.split()
            iso = f"{year}-{MONTHS.index(month.lower()) + 1:02d}"
            out.append(Mention(s, e, printed, None, None, None, 1, "month", iso=iso))
        elif group == "cur":
            body = re.match(r"\$([\d,]+(?:\.\d+)?)\s?([A-Za-z]*)", printed)
            digits, suffix = body.group(1).replace(",", ""), body.group(2).lower()
            scale = _SUFFIX.get(suffix, 1)
            number = float(digits) * scale
            out.append(Mention(s, e, printed, number, "USD", _unit_word_after(text, e), scale * 10 ** -_decimals(digits),
                               "currency", hedge=hedge, bound=bound))
        elif group == "pct":
            digits = printed[:-1]
            out.append(Mention(s, e, printed, float(digits), "percent", unit_word, 10 ** -_decimals(digits), "percent",
                               hedge=hedge, bound=bound))
        elif group == "num":
            digits = printed.replace(",", "")
            # A number glued to a word ("H24", "C0087", "48213-B") is an id, not a figure.
            if s > 0 and (text[s - 1].isalpha() or text[s - 1] in "#/"):
                continue
            number = float(digits)
            year = "," not in printed and "." not in printed and len(digits) == 4 and 1900 <= number <= 2100
            if year and unit_word not in UNIT_NOUNS:
                out.append(Mention(s, e, printed, number, None, None, 1, "year", iso=printed))
                continue
            out.append(Mention(s, e, printed, number, None, unit_word, 10 ** -_decimals(digits), "number",
                               hedge=hedge, bound=bound))
        elif group == "words":
            number = words_to_number(printed)
            if number is None:
                continue
            after = _unit_word_after(text, e)
            unit = "USD" if after == "dollars" else "percent" if after == "percent" else None
            last = re.split(r"[\s-]+", printed.lower().strip())[-1]
            precision = SCALES.get(last, 1)
            out.append(Mention(s, e, printed, number, unit, after, precision, "words", hedge=hedge, bound=bound, spoken=True))
    return out
