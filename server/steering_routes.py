"""Steering's routes: one sentence on a piece or a line rebuilds that piece.

    GET  /api/rooms/{room}/steerable    the readout with piece verdicts, for the steering page
    POST /api/rooms/{room}/steer        {"piece", "sentence", "claim_id"?, "author"?, "fund"?}
    GET  /api/rooms/{room}/revisions    every revision kept, with its "what changed" Panel

A bad piece, line or sentence is a 422; a room with no readout and no scan
results is a 404 naming the commands to run.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from schema.claim import Readout
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
