"""The model reading: slides that hold no figure a script can parse.

Only these slides go to the model, through clients/llm.py, and only when
ANTHROPIC_API_KEY is set. The model returns the checkable facts it reads, each
with the exact quote. The script then keeps a fact only when its quote is on
the slide and any figure in it parses back to the number the model gave.
Without a key, or on a refusal, the slides become one gap. Never a crash.
"""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from scans.base import gap
from scans.claims.extract import Statement, _pages
from scans.claims.kinds import KINDS
from scans.claims.numbers import Mention, mentions
from scans.knowledge import block as knowledge_block

CHECK = "claim_extract"
# The slides' checkable facts are mostly traction: named customers, pilots, contract dates.
KNOWLEDGE_PIECES = ("traction_and_revenue",)
PROMPT = (Path(__file__).parent / "prompts" / "slide_read.md").read_text(encoding="utf-8")


class SlideFact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    slide: int
    quote: str
    kind: str
    number: float | None


class SlideFacts(BaseModel):
    model_config = ConfigDict(extra="forbid")
    facts: list[SlideFact]


def silent_slides(room: Path, statements: list[Statement]) -> list[int]:
    """Slides with text but no figure the script found."""
    decks = [s.uri for s in statements if s.origin == "deck"]
    if not decks:
        return []
    pages = _pages(room / decks[0]) or []
    with_figures = {s.slide for s in statements} | {r.slide for s in statements for r in s.repeats}
    return [n for n, text in enumerate(pages, start=1) if text.strip() and n not in with_figures]


def read_slides(room: Path, statements: list[Statement], reader=None) -> tuple[list[Statement], list]:
    slides = silent_slides(room, statements)
    if not slides:
        return [], []
    uri = next(s.uri for s in statements if s.origin == "deck")
    pages = _pages(room / uri) or []
    where = ", ".join(str(n) for n in slides)
    if reader is None and not os.environ.get("ANTHROPIC_API_KEY"):
        return [], [gap(f"Not in the room: a model reading of slides {where}, which hold no figure a script can parse",
                        "no ANTHROPIC_API_KEY, so the model reading did not run",
                        "ANTHROPIC_API_KEY set, then python -m scans.claims again", "the_pitch_itself")]
    from clients.llm import ModelRefused, read

    docs = [f'<doc path="{uri}" locator="slide {n}">\n{pages[n - 1]}\n</doc>' for n in slides]
    try:
        out = (reader or read)(SlideFacts, check_name=CHECK, scan="claims", task=PROMPT, docs=docs,
                                  knowledge=knowledge_block(KNOWLEDGE_PIECES))
    except ModelRefused as err:
        return [], [gap(f"Not in the room: a model reading of slides {where}", f"the model refused ({err})",
                        "a rerun, or the founder's own list of the facts on these slides", "the_pitch_itself")]
    kept, dropped = [], 0
    for fact in out.facts:
        if fact.slide not in slides or fact.quote.strip() not in pages[fact.slide - 1] or fact.kind not in KINDS:
            dropped += 1
            continue
        found = mentions(fact.quote)
        if fact.number is not None and not any(m.number == fact.number for m in found):
            dropped += 1
            continue
        m = next((m for m in found if m.number == fact.number), None) or Mention(0, 0, fact.quote, None, None, None, 1, "fact")
        kept.append(Statement("model", uri, f"slide {fact.slide}", fact.quote.strip(), fact.quote, m,
                              fact.kind if m.kind_hint in KINDS[fact.kind].expects else "other", slide=fact.slide))
    gaps = []
    if dropped:
        gaps.append(gap(f"Not in the room: {dropped} model readings of slides {where} whose quote or number did not check out",
                        "the quote was not on the slide, or its figure did not parse back", "a rerun", "the_pitch_itself"))
    return kept, gaps
