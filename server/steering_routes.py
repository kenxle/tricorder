"""Steering's routes: one sentence on a piece or a line rebuilds that piece.

    GET  /api/rooms/{room}/steerable    the readout with piece verdicts, for the steering page
    POST /api/rooms/{room}/steer        {"piece", "sentence", "claim_id"?, "author"?, "fund"?}
    GET  /api/rooms/{room}/revisions    every revision kept, with its "what changed" Panel
    GET  /api/rooms/{room}/claims/{claim_id}/sources/{i}
                                        the text at a line's i-th source, read by POST /source's rule
                                        (server.app.readable_rooms and memo.rooms.text_in): the full room
                                        once a "read the full room" steer switched it, and never outside it

A bad piece, line or sentence is a 422, and so is a field over its size limit
(review wave 2b, S3); a room with no readout and no scan results is a 404 naming
the commands to run; a scan that crashes while the steer reruns it is a 500 that
names the scan, with nothing written.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from server.api_models import ClaimSource, RoomRevisions
from schema.claim import Readout
from memo.rooms import OutsideRoom, is_file_source, room_holding, text_in
from schema.readers import LocatorError
from scans.base import room_name
from steering import engine
from steering.models import SteerOutcome

router = APIRouter(prefix="/api/rooms", tags=["steering"])


class SteerBody(BaseModel):
    piece: str = Field(max_length=64)
    sentence: str = Field(max_length=2 * engine.MAX_SENTENCE)  # the engine holds the collapsed sentence to MAX_SENTENCE
    claim_id: str | None = Field(default=None, max_length=engine.MAX_LINE_ID)
    author: str | None = Field(default=None, max_length=engine.MAX_AUTHOR)
    fund: str = Field(default="demo", max_length=64)


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
    except engine.ScanFailed as err:
        raise HTTPException(500, str(err))


@router.get("/{room}/revisions", response_model=RoomRevisions)
def revisions(room: str) -> dict:
    path = _room(room)
    try:
        readout = engine.load_readout(path)
    except engine.NoReadout as err:
        raise HTTPException(404, str(err))
    return {"room": readout.room, "revisions": [r.model_dump() for r in readout.revisions],
            "changes": [p.model_dump() for p in readout.panels if p.name.startswith("steer ")]}


@router.get("/{room}/claims/{claim_id}/sources/{i}", response_model=ClaimSource)
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
    from server.app import readable_rooms  # POST /source's rule: containment, the answer-key seal, the full-room switch

    rooms = readable_rooms(room)
    source = claim.sources[i]
    try:
        held = room_holding(source, rooms) if is_file_source(source) else rooms[0]
        return {"room": room_name(held), "text": text_in(source, rooms)}
    except OutsideRoom:
        raise HTTPException(404, "no such file in this room")
    except (LocatorError, OSError) as err:
        raise HTTPException(404, str(err))
