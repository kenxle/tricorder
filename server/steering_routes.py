"""Steering's routes: one sentence on a piece or a line rebuilds that piece.

    GET  /api/rooms/{room}/steerable    the readout with piece verdicts, for the steering page
    POST /api/rooms/{room}/steer        {"piece", "sentence", "claim_id"?, "author"?, "fund"?}
    GET  /api/rooms/{room}/revisions    every revision kept, with its "what changed" Panel
    GET  /api/rooms/{room}/claims/{claim_id}/sources/{i}
                                        the text at a line's i-th source, read from the room the line
                                        reads: the full room once a "read the full room" steer switched it

A bad piece, line or sentence is a 422; a room with no readout and no scan
results is a 404 naming the commands to run.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from schema.claim import Readout
from schema.readers import LocatorError, text_at
from scans.base import room_name
from steering import engine
from steering.models import SteerOutcome

router = APIRouter(prefix="/api/rooms", tags=["steering"])


class SteerBody(BaseModel):
    piece: str
    sentence: str
    claim_id: str | None = None
    author: str | None = None
    fund: str = "demo"


def _room(room: str):
    from server.app import room_dir  # the app's room lookup: its id pattern and its room list

    return room_dir(room)


@router.get("/{room}/steerable")
def steerable(room: str) -> Readout:
    path = _room(room)
    try:
        return engine.steerable(path)
    except engine.NoReadout as err:
        raise HTTPException(404, str(err))


@router.post("/{room}/steer")
def steer(room: str, body: SteerBody) -> SteerOutcome:
    path = _room(room)
    try:
        return engine.steer(path, body.piece, body.sentence, body.claim_id, body.author, fund=body.fund)
    except engine.BadSteer as err:
        raise HTTPException(422, str(err))
    except engine.NoReadout as err:
        raise HTTPException(404, str(err))


@router.get("/{room}/revisions")
def revisions(room: str) -> dict:
    path = _room(room)
    try:
        readout = engine.load_readout(path)
    except engine.NoReadout as err:
        raise HTTPException(404, str(err))
    return {"room": readout.room, "revisions": [r.model_dump() for r in readout.revisions],
            "changes": [p.model_dump() for p in readout.panels if p.name.startswith("steer ")]}


@router.get("/{room}/claims/{claim_id}/sources/{i}")
def claim_source(room: str, claim_id: str, i: int) -> dict:
    path = _room(room)
    try:
        readout = engine.steerable(path)
    except engine.NoReadout as err:
        raise HTTPException(404, str(err))
    claim = next((c for c in readout.claims + readout.unverified if c.id == claim_id), None)
    if claim is None:
        raise HTTPException(404, f"no line {claim_id!r} in the readout")
    if not 0 <= i < len(claim.sources):
        raise HTTPException(404, f"line {claim_id!r} has {len(claim.sources)} sources")
    source_room = engine.claim_room(readout, claim_id, path)
    try:
        return {"room": room_name(source_room), "text": text_at(claim.sources[i], source_room)}
    except LocatorError as err:
        raise HTTPException(404, str(err))
