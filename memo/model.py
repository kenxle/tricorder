"""The memo's data shape: sections, lines, claim ids, operator text, versions.

The memo is its own model, outside schema/ (which is frozen). It is built from
a Readout and is self-contained: every claim a line cites is copied in, with
its sources, so the page and the PDF render from this one object and a later
reader copy can lay over one version of it (docs/features/20261023.03_memo_export/
04_architecture.md, "The memo's data shape").

Line kinds follow MEMO_TEMPLATE.md, "How each line links down", plus the
structural kinds the template's rules ask for (a section's opening pieces
line, its closing coverage line, ask lines, the operator's blank slots).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from schema.claim import AskItem, Claim

LineKind = Literal[
    "claim",       # A sentence Tricorder wrote from one or more claims.
    "reading",     # A model's judgement; text starts "Reading:".
    "gap",         # Starts "Not in the room:" or "Not in the readout yet:".
    "operator",    # A sentence the operator wrote.
    "scenario",    # Reserved for reader copies (reader-scenarios). The export never writes one.
    "slot",        # A blank the operator fills: the recommendation, the outcome cases, the signature.
    "pieces",      # A section's first line: the pieces it draws on, with verdicts and counts.
    "coverage",    # A section's last line: its checklist items found, checked and missing.
    "ask",         # One line of the ask list.
    "unverified",  # A claim in the "could not verify" box.
    "fact",        # A header field: to, date, version, the synthetic notice.
    "source",      # One cited source in section 16.
    "change",      # One change-log line in section 16.
]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GapRef(_Strict):
    """Why a gap line exists: the readout Gap, or a part of the readout not built yet."""

    what: str
    why: str
    would_need: str
    missing_from: Literal["room", "readout"] = "room"


class MemoLine(_Strict):
    id: str = Field(description="Stable inside the memo, for example 's07-l03' or 'op-2-1'. Operator edits name lines by id.")
    kind: LineKind
    text: str
    label: str | None = Field(default=None, description="A short bold lead, for example 'Red flag: ARR' or 'Runway'.")
    claim_ids: list[str] = Field(default_factory=list, description="The claims one click opens.")
    checklist_ids: list[str] = Field(default_factory=list)
    ask_ids: list[str] = Field(default_factory=list, description="Ask-list lines (ids in Memo.asks) this line links to.")
    gap: GapRef | None = None
    author: str | None = Field(default=None, description="Operator lines only: who wrote it.")
    version: int | None = Field(default=None, description="Operator lines only: the version that added or last changed it.")
    unsourced_numbers: list[str] = Field(default_factory=list, description="Numbers in an operator line with no claim behind them: 'operator's figure, no source'.")
    severity: Literal["green", "red", "flag", "watch", "info"] | None = None


class MemoSection(_Strict):
    number: int
    key: str
    title: str
    who_writes: str = Field(description="From MEMO_TEMPLATE.md, 'Who writes it'.")
    lines: list[MemoLine] = Field(default_factory=list)
    empty_because: list[str] = Field(default_factory=list, description="When Tricorder has nothing to put here: the gap lines' text that say why.")


class ChecklistRef(_Strict):
    """One checklist coverage row, copied from the readout's 'checklist coverage' panel."""

    id: str
    item: str
    piece: str
    expected: str
    status: str
    detail: str
    named_by: list[str] = Field(default_factory=list)
    named_by_urls: list[str] = Field(default_factory=list)


class SourceText(_Strict):
    """The text at one source's locator, read at export, so the page opens it offline."""

    key: str = Field(description="'uri|locator'")
    text: str
    found: bool = Field(description="The quote checker found the quote in this text.")


class ChangeEntry(_Strict):
    version: int
    at: str
    author: str
    what: str


class Memo(_Strict):
    room: str
    company: str
    readout_built_at: str
    built_at: str
    version: int
    based_on_version: int | None = Field(default=None, description="The version this one was made from; None for version 1.")
    synthetic_notice: str | None = None
    sections: list[MemoSection]
    claims: dict[str, Claim] = Field(default_factory=dict, description="Every claim a line cites, plus the claims they corroborate or conflict with.")
    asks: dict[str, AskItem] = Field(default_factory=dict, description="The ask list, by id 'ask-01'...")
    checklist: dict[str, ChecklistRef] = Field(default_factory=dict)
    sources: dict[str, SourceText] = Field(default_factory=dict)
    changes: list[ChangeEntry] = Field(default_factory=list)
    withdrawn_lines: list[str] = Field(default_factory=list, description="Tricorder's lines (and slots) the operator replaced or removed. A rebuild leaves them out.")
    stage: str | None = None
    steps_missing: list[str] = Field(default_factory=list, description="Merge steps not built in this checkout (link, pieces, top_flags), so the page can say what it cannot show yet.")

    def section(self, number: int) -> MemoSection:
        for s in self.sections:
            if s.number == number:
                return s
        raise KeyError(number)

    def line(self, line_id: str) -> tuple[MemoSection, MemoLine]:
        for s in self.sections:
            for ln in s.lines:
                if ln.id == line_id:
                    return s, ln
        raise KeyError(line_id)


class Edit(_Strict):
    """One operator edit. A batch of edits makes one new version."""

    action: Literal["add", "replace", "remove"]
    section: int | None = Field(default=None, description="For add: the section number.")
    line_id: str | None = Field(default=None, description="For replace and remove: the line. For add: the line to add after (optional).")
    text: str = ""
    claim_ids: list[str] = Field(default_factory=list, description="Claims the operator attaches. Each must be a claim in the memo.")


def source_key(uri: str, locator: str) -> str:
    return f"{uri}|{locator}"
