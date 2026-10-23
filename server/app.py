"""The local server: serves rooms, scan results and readouts to the page.

    uvicorn server.app:app --port 8787

The page only reads JSON from here, so it never waits on Python. Scans run as
their own processes (python -m scans.<name>), the same command a person runs.
Everything binds to localhost; the demo needs no venue wifi.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from schema.claim import Readout, ScanResult, Source
from schema.readers import LocatorError, text_at
from scans import SCANS
from scans.base import ROOT, available, out_dir, room_inputs
from scans.memo.merge import build_readout, write_readout

# Where rooms live: the synthetic rooms, and rooms that arrive by upload or
# the inbox (git-ignored).
ROOM_PARENTS = [ROOT / "data_room", ROOT / "rooms"]
SAMPLE_OUT = ROOT / "sample_out"
PAGE_DIST = ROOT / "readout" / "dist"
_ROOM_ID = re.compile(r"^[A-Za-z0-9_\-]+$")
_ROOM_PART = re.compile(r"^\d\d_")

app = FastAPI(title="Tricorder", version="0.1.0")


def rooms() -> dict[str, Path]:
    """Every folder that looks like a data room: it holds a 00_ to 09_ folder."""
    found = {}
    for parent in ROOM_PARENTS:
        if not parent.is_dir():
            continue
        for d in sorted(parent.iterdir()):
            if d.is_dir() and any(_ROOM_PART.match(c.name) for c in d.iterdir() if c.is_dir()):
                found.setdefault(d.name, d)
    return found


def room_dir(room: str) -> Path:
    if not _ROOM_ID.match(room) or room not in rooms():
        raise HTTPException(404, f"no room {room!r}")
    return rooms()[room]


def _inside(base: Path, rel: str) -> Path:
    """rel resolved under base, or a 404. No path ever leaves its room."""
    target = (base / rel).resolve()
    if not target.is_relative_to(base.resolve()) or not target.is_file():
        raise HTTPException(404, "no such file")
    return target


@app.get("/health")
def health() -> dict:
    return {"ok": True, "scans": available()}


@app.get("/api/scans")
def list_scans() -> dict:
    return {"all": list(SCANS), "available": available()}


@app.get("/api/rooms")
def list_rooms() -> list[dict]:
    return [
        {
            "id": name,
            "path": str(path.relative_to(ROOT)),
            "inputs": sorted(room_inputs(path)),
            "has_readout": (out_dir(path) / "readout.json").exists(),
        }
        for name, path in rooms().items()
    ]


@app.post("/api/rooms/{room}/scans/{scan}")
def run_scan(room: str, scan: str) -> ScanResult:
    path = room_dir(room)
    if scan not in available():
        raise HTTPException(404, f"no scan {scan!r}")
    done = subprocess.run([sys.executable, "-m", f"scans.{scan}", str(path)], cwd=ROOT, capture_output=True, text=True, env=os.environ.copy())
    if done.returncode != 0:
        raise HTTPException(500, f"{scan} failed: {done.stderr[-2000:]}")
    return ScanResult.model_validate_json((out_dir(path) / f"{scan}.json").read_text(encoding="utf-8"))


@app.get("/api/rooms/{room}/results/{scan}")
def get_result(room: str, scan: str) -> ScanResult:
    path = room_dir(room)
    if scan not in SCANS:
        raise HTTPException(404, f"no scan {scan!r}")
    target = out_dir(path) / f"{scan}.json"
    if not target.exists():
        raise HTTPException(404, f"{scan} has not run on {room}")
    return ScanResult.model_validate_json(target.read_text(encoding="utf-8"))


@app.post("/api/rooms/{room}/readout")
def make_readout(room: str) -> Readout:
    path = room_dir(room)
    readout = build_readout(path)
    write_readout(readout, path)
    return readout


@app.get("/api/rooms/{room}/readout")
def get_readout(room: str) -> Readout:
    """The room's readout; the hand-written example in sample_out/ until one is built."""
    path = room_dir(room)
    for target in (out_dir(path) / "readout.json", SAMPLE_OUT / room / "readout.json"):
        if target.exists():
            return Readout.model_validate_json(target.read_text(encoding="utf-8"))
    raise HTTPException(404, f"no readout for {room} yet")


@app.get("/api/rooms/{room}/files/{rel:path}")
def get_file(room: str, rel: str) -> FileResponse:
    """A room file, for the source panel. Never outside the room."""
    return FileResponse(_inside(room_dir(room), rel))


@app.post("/api/rooms/{room}/source")
def source_text(room: str, source: Source) -> dict:
    """The text at a source's locator, for the footnote panel."""
    try:
        return {"text": text_at(source, room_dir(room))}
    except LocatorError as err:
        raise HTTPException(404, str(err))


from server.store_routes import router as store_router  # noqa: E402
app.include_router(store_router)
from server.founder_requests_routes import router as founder_requests_router  # noqa: E402

app.include_router(founder_requests_router)  # above the page mount, which answers every path
from server.memo_routes import router as memo_router  # noqa: E402  (memo-export; before the page mount, which catches "/")
app.include_router(memo_router)

if PAGE_DIST.is_dir():
    app.mount("/", StaticFiles(directory=PAGE_DIST, html=True), name="page")
