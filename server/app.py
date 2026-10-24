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
from schema.readers import LocatorError
from scans import SCANS
from scans.base import ROOT, available, out_dir, room_inputs
from scans.memo.merge import build_readout, readout_room, write_readout
from memo.rooms import OutsideRoom, resolve, source_rooms, text_in
from server.api_models import Health, RoomInfo, ScanList, SourceText
from server.local_guard import LocalGuard
from founder_requests.intake import rooms_root

# Where rooms live: the synthetic rooms, and rooms that arrive by upload or
# the inbox (git-ignored): rooms/, or TRICORDER_ROOMS_DIR, read on every call.
def room_parents() -> list[Path]:
    return [ROOT / "data_room", rooms_root()]
SAMPLE_OUT = ROOT / "sample_out"
PAGE_DIST = ROOT / "apps" / "web" / "dist"
_ROOM_ID = re.compile(r"^[A-Za-z0-9_\-]+$")
_ROOM_PART = re.compile(r"^\d\d_")

app = FastAPI(title="Tricorder", version="0.1.0")
app.add_middleware(LocalGuard)  # localhost only, no cross-site writes (server/local_guard.py)


def rooms() -> dict[str, Path]:
    """Every folder that looks like a data room: it holds a 00_ to 09_ folder."""
    found = {}
    for parent in room_parents():
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


_reads: dict[str, tuple[tuple[int, int], Path]] = {}  # readout.json path -> ((mtime_ns, size), the room it reads)


def _reads_room(path: Path) -> Path:
    """readout_room, parsed once per change of readout.json. A readout that cannot be read (bad JSON, an
    old schema) reads the room itself, so it never turns a file request into a 500."""
    target = out_dir(path) / "readout.json"
    try:
        st = target.stat()
    except OSError:
        return path
    stamp = (st.st_mtime_ns, st.st_size)
    hit = _reads.get(str(target))
    if hit is not None and hit[0] == stamp:
        return hit[1]
    try:
        reads = readout_room(path)
    except (ValueError, OSError):  # pydantic's ValidationError is a ValueError
        reads = path
    _reads[str(target)] = (stamp, reads)
    return reads


def readable_rooms(room: str) -> list[Path]:
    """Where the room's files open: the room itself, or, once a "read the full room" steer
    switched its readout, the full room first (scans.memo.merge.readout_room). Never any other folder."""
    path = room_dir(room)
    return source_rooms(_reads_room(path), path)


def _inside(rooms_: list[Path], rel: str) -> Path:
    """rel resolved inside one of the rooms, or a 404. No path ever leaves its room."""
    try:
        return resolve(rel, rooms_)
    except LocatorError:
        raise HTTPException(404, "no such file")


@app.get("/health", response_model=Health)
def health() -> dict:
    return {"ok": True, "scans": available()}


@app.get("/api/scans", response_model=ScanList)
def list_scans() -> dict:
    return {"all": list(SCANS), "available": available()}


@app.get("/api/rooms", response_model=list[RoomInfo])
def list_rooms() -> list[dict]:
    return [
        {
            "id": name,
            "path": str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path),
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
    return FileResponse(_inside(readable_rooms(room), rel))


@app.post("/api/rooms/{room}/source", response_model=SourceText)
def source_text(room: str, source: Source) -> dict:
    """The text at a source's locator, for the footnote panel. A file source opens only inside
    the room (or the full room it was switched to): never an absolute path, another room, the
    repo's own files or an answer key."""
    try:
        return {"text": text_in(source, readable_rooms(room))}
    except OutsideRoom:
        raise HTTPException(404, "no such file in this room")
    except (LocatorError, OSError) as err:
        raise HTTPException(404, str(err))


from server.store_routes import router as store_router  # noqa: E402
app.include_router(store_router)
from server.founder_requests_routes import router as founder_requests_router  # noqa: E402

app.include_router(founder_requests_router)  # above the page mount, which answers every path
from server.memo_routes import router as memo_router  # noqa: E402  (memo-export; before the page mount, which catches "/")
app.include_router(memo_router)
from server.steering_routes import router as steering_router  # noqa: E402
app.include_router(steering_router)
from server.trpc_routes import router as trpc_router  # noqa: E402
app.include_router(trpc_router)

if PAGE_DIST.is_dir():
    app.mount("/", StaticFiles(directory=PAGE_DIST, html=True), name="page")
