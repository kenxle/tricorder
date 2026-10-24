"""The memo's routes: export, versions, operator edits, the page and the PDF.

    POST /api/rooms/{room}/memo            export a new version from the room's readout
    GET  /api/rooms/{room}/memo            the latest version (?version=N for another)
    GET  /api/rooms/{room}/memo/versions   the version numbers
    POST /api/rooms/{room}/memo/edits      {author, base_version, edits: [...]} -> the next version
    GET  /api/rooms/{room}/memo.html       the interactive page, with editing on
    GET  /api/rooms/{room}/memo.pdf        the PDF of the latest version
    GET  /api/rooms/{room}/plotly-<version>.min.js   the vendored plotly.js the page's charts load (no CDN)
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, ConfigDict, Field

from memo import store
from memo.edit import EditError
from memo.export import NoReadout, edit, export, page_reports, version_pdf
from memo.html import render_html
from memo.model import MAX_AUTHOR, MAX_EDITS, Edit, Memo
from memo.report_html import PLOTLY_FILE, PLOTLY_PATH

router = APIRouter()


class EditRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    author: str = Field(max_length=MAX_AUTHOR)
    base_version: int
    edits: list[Edit] = Field(max_length=MAX_EDITS)


def _room(room: str):
    from server.app import room_dir  # late import: app.py includes this router at its bottom
    return room_dir(room)


def _latest(room: str, version: int | None = None) -> Memo:
    memo = store.load(_room(room), version)
    if memo is None:
        raise HTTPException(404, f"no memo for {room} yet" if version is None else f"no version {version}")
    return memo


def _conflict(room: str, made_on: int | None = None) -> HTTPException:
    """409 with the version the memo is at now; the page keeps the typed changes and offers to reapply them."""
    latest = (store.versions(_room(room)) or [0])[-1]
    message = f"the memo is at version {latest}" + (f"; your changes were made on version {made_on}" if made_on is not None
                                                     else "; another save made this version first")
    return HTTPException(409, {"message": message, "latest_version": latest})


@router.post("/api/rooms/{room}/memo")
def make_memo(room: str) -> Memo:
    try:
        return export(_room(room)).memo
    except NoReadout as err:
        raise HTTPException(409, str(err))
    except FileExistsError:
        raise _conflict(room)


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
        raise _conflict(room, req.base_version)
    try:
        # The edit applies to the version just checked, never a newer one loaded after the check (S4).
        return edit(_room(room), req.edits, req.author, base=latest).memo
    except EditError as err:
        raise HTTPException(400, str(err))
    except FileExistsError:
        raise _conflict(room, req.base_version)


@router.get("/api/rooms/{room}/memo.html", response_class=HTMLResponse)
def memo_page(room: str) -> HTMLResponse:
    memo = _latest(room)
    return HTMLResponse(render_html(memo, page_reports(memo, _room(room))))


@router.get(f"/api/rooms/{{room}}/{PLOTLY_FILE}", include_in_schema=False)
def memo_plotly(room: str) -> FileResponse:
    _room(room)
    return FileResponse(PLOTLY_PATH, media_type="text/javascript", headers={"Cache-Control": "public, max-age=86400"})


@router.get("/api/rooms/{room}/memo.pdf")
def memo_pdf(room: str) -> FileResponse:
    memo = _latest(room)
    # The latest version's own PDF: built once (at save, or here after an export with --no-pdf), then served as saved.
    path = version_pdf(memo, _room(room))
    return FileResponse(path, media_type="application/pdf", filename=f"{memo.room}_memo_v{memo.version}.pdf")
