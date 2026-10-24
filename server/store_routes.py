"""The readout store's routes, so the page can save, list, read and delete.

    GET  /api/store/{fund}                               the companies held
    GET  /api/store/{fund}/{company}                     everything held (Holding)
    GET  /api/store/{fund}/{company}/versions            the versions
    GET  /api/store/{fund}/{company}/readout?version=N   a stored readout, latest by default
    GET  /api/store/{fund}/{company}/files/{path}        a stored file, by its manifest path
    POST /api/store/{fund}/{company}/save                {"room": "<room id>"}: store the room's readout
    POST /api/store/{fund}/{company}/delete              {"confirm": "<company id>"}: remove it all

A bad fund or company id is a 422, anything not held a 404. Delete cannot be
undone, so it needs the company id typed back in the body.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from server.api_models import CompanyList
from store import BadId, NotHeld, open_store
from store.files import load_from_out
from store.models import DeleteReport, Holding, SaveResult, StoredReadout, VersionInfo

router = APIRouter(prefix="/api/store", tags=["store"])


class SaveBody(BaseModel):
    room: str


class DeleteBody(BaseModel):
    confirm: str


def _call(fn, *args):
    try:
        return fn(*args)
    except BadId as err:
        raise HTTPException(422, str(err))
    except NotHeld as err:
        raise HTTPException(404, str(err))


@router.get("/{fund}", response_model=CompanyList)
def companies(fund: str) -> dict:
    return {"fund": fund, "companies": _call(open_store().companies, fund)}


@router.get("/{fund}/{company}")
def list_company(fund: str, company: str) -> Holding:
    return _call(open_store().list_company, fund, company)


@router.get("/{fund}/{company}/versions")
def list_versions(fund: str, company: str) -> list[VersionInfo]:
    return _call(open_store().list_versions, fund, company)


@router.get("/{fund}/{company}/readout")
def get_readout(fund: str, company: str, version: int | None = None) -> StoredReadout:
    return _call(open_store().get, fund, company, version)


@router.get("/{fund}/{company}/files/{path:path}")
def get_file(fund: str, company: str, path: str) -> Response:
    data = _call(open_store().read_file, fund, company, path)
    return Response(content=data, media_type="application/octet-stream")


@router.post("/{fund}/{company}/save")
def save(fund: str, company: str, body: SaveBody) -> SaveResult:
    from server.app import room_dir  # late: app.py includes this router at its end

    room = room_dir(body.room)
    store = open_store()
    readout, results = _call(load_from_out, room)
    return _call(store.save, fund, company, readout, room, results)


@router.post("/{fund}/{company}/delete")
def delete(fund: str, company: str, body: DeleteBody) -> DeleteReport:
    store = open_store()
    _call(store.list_company, fund, company)  # a bad id is a 422 before the confirm check
    if body.confirm != company:
        raise HTTPException(400, f"type the company id {company!r} in 'confirm' to delete; nothing removed")
    return _call(store.delete_company, fund, company)
