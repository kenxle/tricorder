"""Read the operator's one sentence: a rewrite, or a request for more info.

    read_sentence("treat the pilot as non-recurring")  ->  Reading(kind="rewrite", term="pilot", ...)

Two paths, and the Reading says which ran:

- model: one reading through clients/llm.py (route "bulk"), when
  ANTHROPIC_API_KEY is set and TRICORDER_OFFLINE is not. Every string the model
  returns must be found in the sentence; if not, or if the call fails, the
  rules decide and `fallback_why` says why.
- rules: the wording rules below. They need no key, so the demo runs offline.

The operator never picks the kind (ROADMAP "steering", Includes).
"""

from __future__ import annotations

import os
import re
from typing import Callable

from scans.base import offline
from steering.models import Reading, SteerReading

_T = r"(?:the |their |our |this |that )?(?P<term>[a-z][a-z' -]*?)"
DEFINITION = [re.compile(p, re.I) for p in (
    rf"\btreat {_T} as (?:a |an )?(?:non[- ]?recurring|one[- ]?(?:time|off)|not recurring)",
    rf"\b(?:don['’]?t|do not|never) count {_T} (?:as|in|towards?) (?:recurring|arr|mrr)",
    rf"\b(?:exclude|drop|remove|take out|leave out|strip) {_T} (?:from|out of) (?:the )?(?:arr|mrr|recurring)",
    rf"^\s*{_T} (?:isn'?t|is not|is never|are not|aren'?t) recurring",
    rf"^\s*{_T} (?:is|are) (?:non[- ]?recurring|one[- ]?(?:time|off))",
)]
# "Don't treat the pilot as non-recurring" asks for the opposite of the definition (review wave 2b, S5).
NEGATED = re.compile(r"\b(?:don['’]?t|do not|never|not|no longer|stop|please don['’]?t)\s*$", re.I)
FULL_ROOM = re.compile(r"\b(?:full|whole|entire|complete) (?:data )?room\b|\bsecond tier\b|\btier (?:two|2)\b|\brest of the room\b", re.I)
MORE_VERB = re.compile(r"\b(?:read|open|pull|fetch|get|find|look (?:at|for|in)|search|bring in|dig into)\b", re.I)
NAMED = re.compile(r"\b(?:(?:the |their |a )?(?:latest |recent )?(?:competitor'?s?'? )?(?:pricing pages?|filings?|10-?k|s-1|website|reviews?|press|news|bank statements?|app store pages?))\b", re.I)
# A number is a request only after a frame that asks for it ("should be", "make it", "use",
# "change ... to"), and a bare year is never one (review wave 2b, O1).
FRAME = re.compile(
    r"(?:\bshould(?:\s+\w+)?\s+(?:be|read|say|show)|\bmust be|\bought to be|\bis (?:really|actually)|\bto be"
    r"|\bcall it|\binstead of|\brather than"
    r"|\b(?:make|use|set|change|update|put|round|bump|raise|lower|move|restate)(?:\s+[\w'$.,]+){0,3}?(?:\s+(?:to|at|as))?)"
    r"\s*$", re.I)
YEAR = re.compile(r"(?:19|20)\d\d")
NUMBER = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|thousand|billion|m|k|bn)\b)?"
    r"|\b\d[\d,]*(?:\.\d+)?(?:\s?(?:%|percent\b|million\b|thousand\b|billion\b|months?\b|m\b|k\b|x\b))?"
    r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty)\s+(?:million|thousand|percent|months)\b",
    re.I)

TASK = """Task: read one instruction an investor typed on a piece of a diligence readout, and say what it asks for.

Instruction: <instruction>{sentence}</instruction>

Answer with these fields. Copy every string exactly from the instruction; never add a word that is not in it.
- kind: "more_info" if it asks Tricorder to read or fetch a source it has not read (the full room, the second tier, a filing, a website); otherwise "rewrite".
- definition_term: if it says something should not count as recurring revenue (a pilot, a fee, a contract), that thing; else null.
- asks_for_number: true if it asks for a different figure than the one shown.
- number_text: that figure as typed; else null.
- wants_full_room: true if it asks for the full room, the second tier or the rest of the room.
- source_named: any other source it names; else null."""


def model_available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY")) and not offline()


def _clean_term(term: str) -> str:
    term = re.sub(r"\s+", " ", term.strip().lower())
    return re.sub(r"^(?:the|their|our|this|that) ", "", term)


def _definition(s: str) -> re.Match | None:
    """The first definition pattern that matches and is not negated ("don't treat ... as")."""
    for pattern in DEFINITION:
        for m in pattern.finditer(s):
            if not NEGATED.search(s[:m.start()]):
                return m
    return None


def negated_definition(sentence: str) -> bool:
    """True when the sentence names a definition only to say not to apply it."""
    return _definition(sentence) is None and any(p.search(sentence) for p in DEFINITION)


def _number_asked(s: str) -> str | None:
    for m in NUMBER.finditer(s):
        text = m.group(0).strip()
        if YEAR.fullmatch(text):
            continue
        if FRAME.search(s[:m.start()][-60:]):
            return text
    return None


def by_rules(sentence: str) -> Reading:
    s = sentence.strip()
    m = _definition(s)
    if m:
        return Reading(kind="rewrite", path="rules", term=_clean_term(m.group("term")), treat_as="non_recurring")
    if FULL_ROOM.search(s):
        return Reading(kind="more_info", path="rules", source="full_room")
    named = NAMED.search(s)
    if named and MORE_VERB.search(s):
        return Reading(kind="more_info", path="rules", source="named", source_named=named.group(0).strip())
    number = _number_asked(s)
    if number:
        return Reading(kind="rewrite", path="rules", number_text=number)
    return Reading(kind="rewrite", path="rules")


def _in(text: str | None, sentence: str) -> bool:
    return text is None or text.strip().lower() in sentence.lower()


def by_model(sentence: str, llm: Callable) -> Reading:
    """The model's reading, held to the sentence. Raises ValueError when it strays."""
    got: SteerReading = llm(SteerReading, check_name="steer.read", scan="steering",
                            task=TASK.format(sentence=sentence), route="bulk", effort="low", max_tokens=1000)
    for name in ("definition_term", "number_text", "source_named"):
        value = getattr(got, name)
        if not _in(value, sentence):
            raise ValueError(f"the model named '{value}' as {name}, which is not in the sentence")
    if got.kind == "more_info":
        if got.wants_full_room:
            return Reading(kind="more_info", path="model", source="full_room")
        return Reading(kind="more_info", path="model", source="named", source_named=got.source_named or sentence.strip())
    if got.definition_term and not negated_definition(sentence):
        return Reading(kind="rewrite", path="model", term=_clean_term(got.definition_term), treat_as="non_recurring")
    if got.asks_for_number:
        return Reading(kind="rewrite", path="model", number_text=(got.number_text or "").strip() or None)
    return Reading(kind="rewrite", path="model")


def read_sentence(sentence: str, llm: Callable | None = None) -> Reading:
    """Read one sentence. `llm` defaults to clients.llm.read when a key is set."""
    if llm is None and model_available():
        from clients.llm import read as llm
    if llm is None:
        return by_rules(sentence)
    try:
        return by_model(sentence, llm)
    except Exception as err:  # a refusal, a network error, or a reading that strays
        from clients.llm import ModelRefused

        why = f"the model refused ({err})" if isinstance(err, ModelRefused) else str(err)
        return by_rules(sentence).model_copy(update={"fallback_why": why})
