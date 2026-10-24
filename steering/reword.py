"""The model's rewording of a piece's lines, held to the numbers (STEER-R9).

Used only on the model path: with no key there is nothing to reword with, and
the revision says so. A rewording is kept only when `guard` passes it:

- the new text carries the same numbers, with the same units, in the same order;
- every number keeps the source it is stated against: the sequence of source
  words (deck, P&L, model, tab, ...) and numbers reads the same;
- what the line says about its numbers keeps its sense: the classes of words
  that agree, differ, point up, point down or negate are the same;
- a judged line still starts "Reading:".

A refused rewording keeps the line's own words, so a guard that is too strict
costs only a plainer line (review wave 2b, S8). The sources do not change, so
the quote checker still finds them.
"""

from __future__ import annotations

import re
from typing import Callable

from schema.claim import Claim
from scans.knowledge import block as knowledge_block
from steering.models import RewordReading

_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
_FIGURE = re.compile(r"(?P<cur>\$\s?)?(?P<n>\d[\d,]*(?:\.\d+)?)(?:\s?(?P<unit>%|percent\b|points?\b|pts\b|months?\b|"
                     r"million\b|thousand\b|billion\b|bn\b|k\b|m\b|x\b))?", re.I)
_UNITS = {"percent": "%", "point": "points", "pts": "points", "month": "months", "m": "million", "k": "thousand", "bn": "billion"}
SOURCE_WORDS = re.compile(r"\b(?:deck|slides?|p&l|p and l|model|tab|books|ledger|export|contracts?|agreement|customer file|"
                          r"rebuil[dt]|plan|bank|statements?|filing|website|video|transcript|founder)\b", re.I)
SENSE = {
    "agree": r"agrees?|agreed|match(?:es|ed)?|same|equals?|equal to|consistent|in line|ties",
    "differ": r"differs?|differed|different|disagrees?|gap|mismatch(?:es)?|inconsistent|does not match|doesn't match",
    "up": r"higher|above|over|more|exceeds?|overstates?|larger|greater|up",
    "down": r"lower|below|under|less|fewer|understates?|smaller|short|down",
    "not": r"not|no|never|none|without|isn't|aren't|doesn't|don't|didn't|wasn't|won't|can't",
}
_SENSE = {k: re.compile(rf"(?:\b(?:{v})\b)", re.I) for k, v in SENSE.items()}

TASK = """Task: reword the lines of one piece of a diligence readout, following the investor's instruction.

Instruction: <instruction>{sentence}</instruction>

Lines, one per claim id:
{lines}

Rules:
- Return only the lines you change, each with its claim id.
- Keep every number exactly as written, and add no number.
- Keep the meaning. Do not say a check found something it did not.
- A line that starts with "Reading:" still starts with "Reading:".
- Plain words, one idea per sentence, no dashes between clauses."""


def numbers(text: str) -> list[str]:
    return sorted(n.replace(",", "") for n in _NUM.findall(text))


def figures(text: str) -> list[str]:
    """Each number in order, with its currency and unit: "$2500000", "11.6%", "3"."""
    out = []
    for m in _FIGURE.finditer(text):
        unit = (m.group("unit") or "").lower()
        out.append(("$" if m.group("cur") else "") + m.group("n").replace(",", "") + _UNITS.get(unit, unit))
    return out


def _source_word(word: str) -> str:
    """One spelling per source: "P and L" is "p&l", "slides" is "slide", "rebuilt" is "rebuild"."""
    word = word.lower().replace("p and l", "p&l").rstrip("s")
    return "rebuild" if word == "rebuilt" else word


def frame(text: str) -> list[str]:
    """Source words and figures in the order the line states them, repeats of one source word merged."""
    items = [(m.start(), _source_word(m.group(0))) for m in SOURCE_WORDS.finditer(text)]
    items += [(m.start(), f) for m, f in zip(_FIGURE.finditer(text), figures(text))]
    seq = []
    for _, item in sorted(items):
        if not seq or seq[-1] != item:
            seq.append(item)
    return seq


def sense(text: str) -> set[str]:
    return {k for k, rx in _SENSE.items() if rx.search(text)}


def guard(old: str, new: str) -> str | None:
    """Why a rewording of `old` into `new` is refused, or None when it keeps the numbers and their sense."""
    if numbers(new) != numbers(old):
        return "the rewording changed a number"
    if figures(new) != figures(old):
        return "the rewording moved a number or changed its unit"
    if frame(new) != frame(old):
        return "the rewording stated a number against another source"
    if sense(new) != sense(old):
        return "the rewording changed what the line says about its numbers"
    return None


def reword(claims: list[Claim], sentence: str, llm: Callable, piece: str | None = None) -> tuple[dict[str, str], list[str]]:
    """({claim id: new text} kept, [why each refused line was refused]).

    `piece` loads that piece's expert knowledge (knowledge/<piece>.md) into the prompt, when it has a file."""
    by_id = {c.id: c for c in claims}
    lines = "\n".join(f"[{c.id}] {c.text}" for c in claims)
    got: RewordReading = llm(RewordReading, check_name="steer.reword", scan="steering",
                             task=TASK.format(sentence=sentence, lines=lines), route="read", effort="medium", max_tokens=4000,
                             knowledge=knowledge_block([piece]))
    kept, refused = {}, []
    for line in got.lines:
        old = by_id.get(line.claim_id)
        new = line.text.strip()
        if old is None:
            refused.append(f"{line.claim_id} is not a line in this piece")
        elif (why := guard(old.text, new)) is not None:
            refused.append(f"{line.claim_id}: {why}")
        elif old.confidence == "judged" and not new.startswith("Reading:"):
            refused.append(f"{line.claim_id}: a judged line must start 'Reading:'")
        elif new and new != old.text:
            kept[line.claim_id] = new
    return kept, refused
