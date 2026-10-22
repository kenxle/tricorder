"""The Claim schema, typed in from FRAMEWORKS.md, "The shared Claim".

The JSON Schema in FRAMEWORKS.md is the single source for every field type.
These Pydantic models follow it field for field. If the two ever differ,
FRAMEWORKS wins and this file changes. `python -m schema.export` writes
`schema/claim.schema.json` and `schema/ts/claim.ts` from these models; a test
fails when either is stale.

Frozen before Saturday. On Saturday only the captain changes this file, and
only to fix a bug (ROADMAP.md, "Who owns what").
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class _Strict(BaseModel):
    # additionalProperties: false, as Claude's structured outputs require.
    model_config = ConfigDict(extra="forbid", json_schema_serialization_defaults_required=True)


SourceKind = Literal["file", "url", "api", "video"]

Unit = Literal["USD", "USD_per_month", "USD_per_year", "percent", "months", "days", "accounts", "count"]

ValueLabel = Literal[
    "arr", "mrr", "paying_accounts", "accounts_created", "nrr_12m", "grr_12m", "cohort_size",
    "gross_margin", "cost_of_revenue", "runway_months", "net_burn_monthly", "payroll_monthly",
    "hires", "headcount", "cash", "largest_customer_share", "top3_customer_share", "arpa", "acv",
    "cac", "payback_months", "ltv", "raise_amount", "pre_money", "post_money", "ownership", "tam",
    "sam", "som", "price", "contract_term", "notice_period", "signal", "other",
]

Severity = Literal["info", "watch", "flag"]

Confidence = Literal["computed", "quoted", "judged", "unverified"]

PieceName = Literal[
    "traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers",
    "market", "comps", "team", "the_pitch_itself",
]

# The overview's default order. A view, not data: the operator can reorder.
PIECE_ORDER: tuple[str, ...] = PieceName.__args__  # type: ignore[attr-defined]

Verdict = Literal["looking_strong", "looking_weak", "mixed", "not_enough_in_the_room"]


class Source(_Strict):
    kind: SourceKind
    uri: str = Field(description="Path inside the data room, a URL, or the API call.")
    locator: str = Field(description="For example 'slide 3', 'page 2', 'ARR_Build!E14', 'ARR_TOTAL', 'clause 7', 'line 12', 'row 118', 't=35-41'.")
    start_s: float | None = Field(default=None, description="Video only. Copied from the transcript by the script.")
    end_s: float | None = Field(default=None, description="Video only. Copied from the transcript by the script.")
    quote: str = Field(description="The exact span relied on, copied character for character.")
    retrieved_at: str | None = Field(default=None, description="ISO date the source was read.")


class Value(_Strict):
    number: float
    unit: Unit
    label: ValueLabel
    period: str | None = Field(default=None, description="The month or span the number is for, for example '2026-09'.")


class Check(_Strict):
    kind: Literal["script", "model"]
    name: str = Field(description="The entry's check name, plus '.read' for a model claim.")
    model: str | None = Field(default=None, description="Model id. The model sets null; the script fills it.")


class Claim(_Strict):
    id: str = Field(description="Unique inside the scan, for example 'redflags-004'.")
    scan: str
    text: str = Field(description="The one plain sentence the readout shows. Judged claims start with 'Reading:'.")
    value: Value | None = None
    severity: Severity | None = Field(default=None, description="The model sets null; the script sets it from the label.")
    check: Check
    confidence: Confidence
    sources: list[Source] = Field(description="At least one. A missing input is a Gap, never a claim.")
    conflicts_with: list[str] = Field(default_factory=list, description="Ids of claims that state a different number for the same label, unit and period.")
    corroborated_by: list[str] = Field(default_factory=list, description="Ids of claims from an independent source that agree within tolerance. The memo fills it; a scan leaves it empty.")

    @field_validator("sources")
    @classmethod
    def _at_least_one_source(cls, v: list[Source]) -> list[Source]:
        if not v:
            raise ValueError("a claim needs at least one source; a missing input is a Gap")
        return v

    @model_validator(mode="after")
    def _judged_reads_as_reading(self) -> "Claim":
        if self.confidence == "judged" and not self.text.startswith("Reading:"):
            raise ValueError("a judged claim's text starts with 'Reading:'")
        return self


class Gap(_Strict):
    what: str = Field(description="Starts with 'Not in the room:' and names what is missing.")
    why: str = Field(description="For example 'file missing', 'tab missing', 'Akta plan returns 403', 'not stated in the file'.")
    would_need: str = Field(description="The document or source that would close the gap.")
    piece: PieceName | None = Field(default=None, description="The piece the gap feeds. The scan sets it when it knows; the memo fills the rest.")


class Panel(_Strict):
    name: str = Field(description="For example 'comps table', 'signals grid', 'video moments'.")
    columns: list[str]
    rows: list[list[str]]


class Piece(_Strict):
    name: PieceName
    verdict: Verdict
    reason: str = Field(description="One line, with its number and source.")
    reason_claim_ids: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(default_factory=list, description="Every claim in the piece, for the drill-down.")
    corroborating_sources: int = 0
    contradicting_sources: int = 0
    status: Literal["done", "running", "waiting_on_input"] = "done"
    waiting_on: list[str] = Field(default_factory=list, description="Inputs the piece still needs, such as 'financial model'.")


class TopFlag(_Strict):
    kind: Literal["green", "red"]
    piece: PieceName
    rank: int = Field(description="1 is the strongest green or the worst red.")
    text: str
    claim_ids: list[str]


class AskItem(_Strict):
    what: str = Field(description="What to request, in words the operator can paste into an email.")
    why: str = Field(description="The claim or gap it would settle, with its number.")
    piece: PieceName
    from_kind: Literal["gap", "weak_piece", "checklist"]
    claim_ids: list[str] = Field(default_factory=list)
    checklist_id: str | None = Field(default=None, description="For example 'C29', when the line comes from a missing checklist item.")
    if_you_have_it: bool = Field(default=False, description="True when the item is only 'lighter' at the company's stage.")


class ScanResult(_Strict):
    """What every scan writes: one file, out/<room>/<scan>.json."""

    scan: str
    room: str
    ran_at: str
    inputs: list[str] = Field(default_factory=list, description="Files and calls the scan read.")
    claims: list[Claim] = Field(default_factory=list)
    gaps: list[Gap] = Field(default_factory=list)
    panels: list[Panel] = Field(default_factory=list, description="Optional named tables the page shows beside the claims.")


class Steer(_Strict):
    """One plain sentence from the operator on a piece or a line."""

    piece: PieceName
    kind: Literal["rewrite", "more_info"] = Field(description="Tricorder tells the two apart from the sentence; the operator never picks.")
    instruction: str
    claim_id: str | None = Field(default=None, description="The line the operator typed on, when it was a line and not the whole piece.")
    at: str
    author: str | None = None


class PieceRevision(_Strict):
    steer: Steer
    before: Piece
    after: Piece
    claims_added: list[str] = Field(default_factory=list)
    sources_added: list[str] = Field(default_factory=list)
    claims_dropped: list[str] = Field(default_factory=list)
    verdict_moved_by: list[str] = Field(default_factory=list)
    note: str | None = Field(default=None, description="For example why a requested number change was not carried out.")


class ScoreLine(_Strict):
    """One line of eval/score.py against an answer key."""

    room: str
    found: int
    planted: int
    decoys_flagged: int
    decoys: int


class Readout(_Strict):
    """out/<room>/readout.json: what the page renders, in the order it shows it."""

    room: str
    built_at: str
    synthetic_notice: str | None = Field(default=None, description="Shown as a banner on every screen when set.")
    top_flags: list[TopFlag] = Field(default_factory=list)
    pieces: list[Piece] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    unverified: list[Claim] = Field(default_factory=list, description="The 'could not verify' box.")
    gaps: list[Gap] = Field(default_factory=list)
    asks: list[AskItem] = Field(default_factory=list)
    panels: list[Panel] = Field(default_factory=list)
    scans_run: list[str] = Field(default_factory=list)
    scans_missing: list[str] = Field(default_factory=list)
    revisions: list[PieceRevision] = Field(default_factory=list)
    connecting: list[str] = Field(default_factory=list, description="The memo pass's connecting sentences, each citing claim ids.")
    scores: list[ScoreLine] = Field(default_factory=list)


# Every model the JSON Schema export and the TypeScript types carry.
EXPORTED = (Source, Value, Check, Claim, Gap, Panel, Piece, TopFlag, AskItem, ScanResult, Steer, PieceRevision, ScoreLine, Readout)
