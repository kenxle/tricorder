"""Operator edits: each batch makes the next numbered version.

The operator can add a line to a section, replace a line (Tricorder's, a
blank slot, or their own), or remove one. Whatever the operator writes is an
operator line: marked as theirs, with the version that added it. Claims are
attached only when the operator names them, and each must already be in the
memo. A number in an operator line with no claim behind it is listed as
"operator's figure, no source".

Tricorder's own lines never come from an edit. A rebuild from a newer readout
keeps the operator's lines (carry_operator_lines).
"""

from __future__ import annotations

import re

from memo.build import empty_because
from memo.model import ChangeEntry, Edit, Memo, MemoLine

# A figure: a run of digits, with any $ , . % or a word like "million" after it.
_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?\s?(?:%|percent|million|thousand|[MKk]\b)?")


class EditError(ValueError):
    """The edit names a line, section or claim that is not in the memo."""


# A date (2026-10-20 or 2026-10) says when, not how much; it is not a figure.
_DATE = re.compile(r"\b\d{4}-\d{2}(?:-\d{2})?\b")


def unsourced_numbers(text: str) -> list[str]:
    return [m.group(0).strip() for m in _NUMBER.finditer(_DATE.sub(" ", text))]


def _digits(n: str) -> str:
    return re.sub(r"[^\d.]", "", n).rstrip(".")


def numbers_not_in_claims(text: str, claims: list) -> list[str]:
    """Figures in the operator's sentence that none of the attached claims states."""
    stated = " ".join(c.text + (f" {c.value.number:g}" if c.value else "") for c in claims)
    have = {_digits(n) for n in unsourced_numbers(stated)}
    return [n for n in unsourced_numbers(text) if _digits(n) not in have]


def _operator_line(memo: Memo, version: int, k: int, text: str, claim_ids: list[str], author: str) -> MemoLine:
    """An operator line. Attached claims stay only while every figure in the sentence is one they state;
    a sentence with a figure of the operator's own is the operator's, and shows no claim behind it."""
    text = text.strip()
    if not text:
        raise EditError("an operator line needs text")
    unknown = [c for c in claim_ids if c not in memo.claims]
    if unknown:
        raise EditError(f"no claim {unknown[0]!r} in this memo; attach a claim the memo cites")
    if claim_ids and numbers_not_in_claims(text, [memo.claims[c] for c in claim_ids]):
        claim_ids = []
    return MemoLine(id=f"op-{version}-{k}", kind="operator", text=text, claim_ids=list(claim_ids), author=author,
                    version=version, unsourced_numbers=[] if claim_ids else unsourced_numbers(text))


def apply_edits(memo: Memo, edits: list[Edit], author: str, at: str) -> Memo:
    """A new version with the edits applied. The memo passed in is not changed."""
    if not edits:
        raise EditError("no edits")
    if not author.strip():
        raise EditError("an edit needs its author")
    new = memo.model_copy(deep=True)
    v = memo.version + 1
    new.version, new.based_on_version, new.built_at = v, memo.version, at
    log: list[str] = []
    for k, e in enumerate(edits, 1):
        if e.action == "add":
            if e.section is None:
                raise EditError("add needs a section number")
            try:
                sec = new.section(e.section)
            except KeyError:
                raise EditError(f"no section {e.section}") from None
            line = _operator_line(new, v, k, e.text, e.claim_ids, author)
            at_i = len(sec.lines)
            if sec.lines and sec.lines[-1].kind == "coverage":
                at_i -= 1  # sections close with their coverage
            if e.line_id:
                ids = [ln.id for ln in sec.lines]
                if e.line_id not in ids:
                    raise EditError(f"no line {e.line_id!r} in section {e.section}")
                at_i = ids.index(e.line_id) + 1
            sec.lines.insert(at_i, line)
            log.append(f"added a line to section {sec.number}")
        else:
            if not e.line_id:
                raise EditError(f"{e.action} needs a line_id")
            try:
                sec, old = new.line(e.line_id)
            except KeyError:
                raise EditError(f"no line {e.line_id!r}") from None
            i = sec.lines.index(old)
            whose = "their own" if old.kind == "operator" else ("a blank" if old.kind == "slot" else "Tricorder's")
            if old.kind != "operator":
                new.withdrawn_lines.append(old.id)
            if e.action == "remove":
                del sec.lines[i]
                log.append(f"removed {whose} line {old.id} from section {sec.number}")
            else:
                line = _operator_line(new, v, k, e.text, e.claim_ids, author)
                sec.lines[i] = line
                detached = " (its claims detached: the new sentence states a figure they do not)" if e.claim_ids and not line.claim_ids else ""
                log.append(f"replaced {whose} line {old.id} in section {sec.number}{detached}")
    for sec in new.sections:
        sec.empty_because = empty_because(sec)
    what = "; ".join(log)
    new.changes.append(ChangeEntry(version=v, at=at, author=author, what=what[:1].upper() + what[1:] + "."))
    _refresh_versions(new)
    return new


def _refresh_versions(memo: Memo) -> None:
    """The header's version line and section 16's change log follow memo.changes."""
    for ln in memo.section(1).lines:
        if ln.id == "s01-version":
            ln.text = f"Shared version {memo.version}." + (f" Made from version {memo.based_on_version}." if memo.based_on_version else "")
    s16 = memo.section(16)
    s16.lines = [ln for ln in s16.lines if ln.kind != "change"] + [
        MemoLine(id=f"s16-change-{c.version}", kind="change", label=f"Version {c.version}",
                 text=f"{c.what} By {c.author}, {c.at[:16].replace('T', ' ')}.") for c in memo.changes]


def carry_operator_lines(old: Memo, fresh: Memo, at: str) -> Memo:
    """A rebuilt memo, numbered after `old`, with the operator's lines kept where they were.

    An operator line goes back after the line it followed, when that line is still
    there, else at the end of its section. A line the operator replaced or
    removed stays replaced or removed when the rebuild writes it again.
    """
    new = fresh.model_copy(deep=True)
    new.version, new.based_on_version, new.built_at = old.version + 1, old.version, at
    new.withdrawn_lines = list(old.withdrawn_lines)
    for sec in new.sections:
        sec.lines = [ln for ln in sec.lines if ln.id not in new.withdrawn_lines]
    for osec in old.sections:
        nsec = new.section(osec.number)
        prev = None
        for ln in osec.lines:
            if ln.kind == "operator":
                ids = [x.id for x in nsec.lines]
                at_i = ids.index(prev) + 1 if prev in ids else len(nsec.lines)
                kept = [c for c in ln.claim_ids if c in new.claims]
                nsec.lines.insert(at_i, ln.model_copy(update={"claim_ids": kept}))
            prev = ln.id
    for sec in new.sections:
        sec.empty_because = empty_because(sec)
    new.changes = old.changes + [ChangeEntry(version=new.version, at=at, author="Tricorder",
                                             what=f"Redrafted from the readout built {fresh.readout_built_at}; the operator's lines kept.")]
    _refresh_versions(new)
    return new
