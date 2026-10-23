"""Steering's own shapes. Owned here, not in schema/, which is frozen.

The schema's Steer and PieceRevision carry what the readout keeps. These carry
what steering needs on the way: how the sentence was read, and what the model
may answer (structured output, so strict).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from schema.claim import Panel, PieceRevision, Readout


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Reading(BaseModel):
    """How Tricorder read the operator's sentence."""

    kind: Literal["rewrite", "more_info"]
    path: Literal["model", "rules"] = Field(description="model: a reading through clients/llm.py; rules: steering's wording rules.")
    term: str | None = Field(default=None, description="What the operator wants read differently, lower case, e.g. 'pilot'.")
    treat_as: Literal["non_recurring"] | None = None
    number_text: str | None = Field(default=None, description="The number the operator asked for, as typed.")
    source: Literal["full_room", "named"] | None = None
    source_named: str | None = Field(default=None, description="An outside source the sentence names, as typed.")
    fallback_why: str | None = Field(default=None, description="Why the model path was not used, when a key was set.")


class SteerReading(_Strict):
    """What the model returns for one sentence. Every string must be copied from the sentence."""

    kind: Literal["rewrite", "more_info"]
    definition_term: str | None = Field(description="The thing the operator says is not recurring revenue, copied from the sentence, else null.")
    asks_for_number: bool = Field(description="True when the operator asks for a different figure.")
    number_text: str | None = Field(description="That figure, copied from the sentence, else null.")
    wants_full_room: bool = Field(description="True when the operator asks to read the full room, the second tier or the rest of the room.")
    source_named: str | None = Field(description="Any other source to fetch, copied from the sentence, else null.")


class RewordLine(_Strict):
    claim_id: str
    text: str


class RewordReading(_Strict):
    """The model's rewording of a piece's lines. Numbers may not change."""

    lines: list[RewordLine]


class StoreNote(BaseModel):
    saved: bool
    version: int | None = None
    new: bool | None = None
    why: str | None = None


class SteerOutcome(BaseModel):
    readout: Readout
    revision: PieceRevision
    changes: Panel
    reading: Reading
    source_room: str
    rebuilt_by: str
    store: StoreNote
