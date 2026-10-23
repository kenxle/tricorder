"""The memo's routes: export, versions, operator edits, the page and the PDF.

    POST /api/rooms/{room}/memo            export a new version from the room's readout
    GET  /api/rooms/{room}/memo            the latest version (?version=N for another)
    GET  /api/rooms/{room}/memo/versions   the version numbers
    POST /api/rooms/{room}/memo/edits      {author, base_version, edits: [...]} -> the next version
    GET  /api/rooms/{room}/memo.html       the interactive page, with editing on
    GET  /api/rooms/{room}/memo.pdf        the PDF of the latest version
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, ConfigDict

from memo import store
from memo.edit import EditError
from memo.export import NoReadout, edit, export, render
from memo.html import render_html
from memo.model import Edit, Memo

router = APIRouter()


class EditRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    author: str
    base_version: int
    edits: list[Edit]


def _room(room: str):
    from server.app import room_dir  # late import: app.py includes this router at its bottom
    return room_dir(room)


def _latest(room: str, version: int | None = None) -> Memo:
    memo = store.load(_room(room), version)
    if memo is None:
        raise HTTPException(404, f"no memo for {room} yet" if version is None else f"no version {version}")
    return memo


@router.post("/api/rooms/{room}/memo")
def make_memo(room: str) -> Memo:
    try:
        return export(_room(room)).memo
    except NoReadout as err:
        raise HTTPException(409, str(err))


@router.get("/api/rooms/{room}/memo")
def get_memo(room: str, version: int | None = None) -> Memo:
    return _latest(room, version)


@router.get("/api/rooms/{room}/memo/versions")
def memo_versions(room: str) -> list[int]:
    return store.versions(_room(room))


@router.post("/api/rooms/{room}/memo/edits")
def edit_memo(room: str, req: EditRequest) -> Memo:
    latest = _latest(room)
    if req.base_version != latest.version:
        raise HTTPException(409, f"the memo is at version {latest.version}; reload and edit that version")
    try:
        return edit(_room(room), req.edits, req.author).memo
    except EditError as err:
        raise HTTPException(400, str(err))


@router.get("/api/rooms/{room}/memo.html", response_class=HTMLResponse)
def memo_page(room: str) -> HTMLResponse:
    return HTMLResponse(render_html(_latest(room)))


@router.get("/api/rooms/{room}/memo.pdf")
def memo_pdf(room: str) -> FileResponse:
    memo = _latest(room)
    _, path = render(memo, _room(room))  # always the latest version, even after an export with --no-pdf
    return FileResponse(path, media_type="application/pdf", filename=f"{memo.room}_memo_v{memo.version}.pdf")
