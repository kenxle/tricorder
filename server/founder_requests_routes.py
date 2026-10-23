"""Requests to the founder: draft from the ask list, and add the founder's files to a room.

Mounted by one line in server/app.py. Design: docs/features/20261023.02_founder_requests/.
Nothing here sends mail: the draft comes back as text and a mailto link for the operator's
own mail app.
"""

from __future__ import annotations

import base64
import binascii
import json
import os
from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from schema.claim import Readout
from scans.base import out_dir
from founder_requests import draft as d
from founder_requests import intake as ik

router = APIRouter(prefix="/api/rooms/{room}/founder-requests", tags=["founder-requests"])


class DraftAsk(BaseModel):
    numbers: list[int] | None = None
    to: str = ""
    sender: str | None = None    # None: TRICORDER_OPERATOR_NAME
    fund: str | None = None      # None: TRICORDER_FUND_NAME
    by: str | None = None        # ISO date; None: a week from today
    reason: str = d.DEFAULT_REASON


class BatchFile(BaseModel):
    name: str
    answers: str
    data: str                    # base64


class BatchAsk(BaseModel):
    files: list[BatchFile]


class CopyAsk(BaseModel):
    name: str | None = None


def _room(room: str) -> Path:
    path = ik.find_room(room)
    if path is None:
        raise HTTPException(404, f"no room {room!r}")
    return path


def _readout(path: Path) -> Readout:
    target = out_dir(path) / "readout.json"
    if not target.exists():
        raise HTTPException(404, f"No readout for {path.name} yet. Build it first.")
    return Readout.model_validate_json(target.read_text(encoding="utf-8"))


@router.get("")
def list_lines(room: str) -> dict:
    path = _room(room)
    items, held = d.analyse(_readout(path), path)
    synthetic = ik.is_synthetic(path)
    copy = ik.rooms_root() / (path.name + ik.COPY_SUFFIX)
    return {
        "room": room, "items": [asdict(i) for i in items], "default": d.default_selection(items),
        "held": [asdict(h) for h in held], "by": d.default_by().isoformat(), "reason": d.DEFAULT_REASON,
        "sender": os.environ.get("TRICORDER_OPERATOR_NAME", ""), "fund": os.environ.get("TRICORDER_FUND_NAME", ""),
        "synthetic": synthetic, "copy_command": ik.copy_command(path) if synthetic else None,
        "working_copy": copy.name if synthetic and copy.is_dir() else None,
        "mailto_max": d.MAILTO_MAX, "upload_max_bytes": ik.max_bytes(), "accepted": list(ik.ALLOWED),
    }


@router.post("/draft")
def make_draft(room: str, ask: DraftAsk) -> dict:
    path = _room(room)
    try:
        return asdict(d.draft(_readout(path), ask.numbers, room_dir=path, to=ask.to, sender=ask.sender, fund=ask.fund,
                              by=ask.by, reason=ask.reason or d.DEFAULT_REASON))
    except ValueError as err:
        raise HTTPException(422, str(err))


@router.post("/copy")
def copy_room(room: str, ask: CopyAsk) -> dict:
    try:
        dest = ik.copy_room(_room(room), ask.name)
    except ik.IntakeError as err:
        raise HTTPException(err.status, err.message)
    return {"room": dest.name, "from": room}


async def _body(request: Request, limit: int) -> bytes:
    declared = request.headers.get("content-length")
    if declared and declared.isdigit() and int(declared) > limit:
        raise HTTPException(413, "The upload is larger than the size limit.")
    chunks, size = [], 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > limit:
            raise HTTPException(413, "The upload is larger than the size limit.")
        chunks.append(chunk)
    return b"".join(chunks)


@router.post("/files")
async def add_file(room: str, request: Request, answers: str | None = None, name: str | None = None) -> dict:
    """The raw file is the request body; `name` is the founder's file name and `answers` the request it answers."""
    path = _room(room)
    data = await _body(request, ik.max_bytes())
    try:
        return ik.receive(path, data, name or "", answers)
    except ik.IntakeError as err:
        raise HTTPException(err.status, err.message)


@router.post("/batch")
async def add_files(room: str, request: Request) -> dict:
    """Several files in one add: JSON {files: [{name, answers, data (base64)}]}. One rerun, one rebuild."""
    path = _room(room)
    raw = await _body(request, ik.max_bytes() * 4 * 4 // 3 + 64 * 1024)
    try:
        ask = BatchAsk.model_validate_json(raw)
        files = [(base64.b64decode(f.data, validate=True), f.name, f.answers) for f in ask.files]
    except (ValueError, binascii.Error):
        raise HTTPException(400, "The upload is not a list of files with their names and the requests they answer.")
    try:
        return ik.receive_batch(path, files)
    except ik.IntakeError as err:
        raise HTTPException(err.status, err.message)


@router.get("/received")
def received(room: str) -> dict:
    target = out_dir(_room(room)) / ik.LOG
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"received": []}
