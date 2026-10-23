"""The model's rewording of a piece's lines, held to the numbers (STEER-R9).

Used only on the model path: with no key there is nothing to reword with, and
the revision says so. A rewording is kept only when the new text carries
exactly the numbers the old text did, and a judged line still starts
"Reading:". The sources do not change, so the quote checker still finds them.
"""

from __future__ import annotations

import re
from typing import Callable

from schema.claim import Claim
from steering.models import RewordReading

_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")

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


def reword(claims: list[Claim], sentence: str, llm: Callable) -> tuple[dict[str, str], list[str]]:
    """({claim id: new text} kept, [why each refused line was refused])."""
    by_id = {c.id: c for c in claims}
    lines = "\n".join(f"[{c.id}] {c.text}" for c in claims)
    got: RewordReading = llm(RewordReading, check_name="steer.reword", scan="steering",
                             task=TASK.format(sentence=sentence, lines=lines), route="read", effort="medium", max_tokens=4000)
    kept, refused = {}, []
    for line in got.lines:
        old = by_id.get(line.claim_id)
        new = line.text.strip()
        if old is None:
            refused.append(f"{line.claim_id} is not a line in this piece")
        elif numbers(new) != numbers(old.text):
            refused.append(f"{line.claim_id}: the rewording changed a number")
        elif old.confidence == "judged" and not new.startswith("Reading:"):
            refused.append(f"{line.claim_id}: a judged line must start 'Reading:'")
        elif new and new != old.text:
            kept[line.claim_id] = new
    return kept, refused
