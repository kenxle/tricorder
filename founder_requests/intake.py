"""Add a founder's file to a room, then rerun the scans that were waiting on it and rebuild the readout.

The upload is attack surface, so every step is strict (03_prd.md, FR-R16 to FR-R20):

- data_room/ is never written. A synthetic room is copied to rooms/ first (`copy_room`).
- The founder's file name is never used as a path; only a cleaned stem is, under a folder this
  module picks (`check_name`, `target_for`).
- Only an allowlist of kinds, and the bytes must match the kind (`check_bytes`).
- A size limit, an exclusive write that never follows a link and never overwrites (`save`).

`TRICORDER_ROOMS_DIR` moves rooms/ (tests and verification runs); `TRICORDER_UPLOAD_MAX_MB` sets the
size limit (default 25).
"""

from __future__ import annotations

import importlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

from schema.claim import Readout, ScanResult
from scans.base import ROOT, available, missing_needs, now_iso, out_dir, room_inputs
from scans.memo import checklist as cl

DATA_ROOM = ROOT / "data_room"
COPY_SUFFIX = "_live"
MAX_UNPACKED = 100 * 1024 * 1024   # an Office file that unpacks past this is refused
MAX_ZIP_ENTRIES = 10_000
STEM_MAX = 80
TEXT = (".csv", ".md", ".txt")
OFFICE = {".xlsx": "xl/", ".docx": "word/", ".pptx": "ppt/"}
ALLOWED = (".pdf", ".json", ".png", ".jpg", ".jpeg", ".mp4") + TEXT + tuple(OFFICE)
LOG = "founder_requests.json"
COVERAGE_PANEL = "checklist coverage"

_ROOM_ID = re.compile(r"^[A-Za-z0-9_-]+$")
_NUMBERED = re.compile(r"^(\d\d)_(.+)$")
_REQUEST = re.compile(r"^C\d{1,3}$")

# The names the scans read (scans.base.INPUT_KINDS). A reply for one of these items is saved under it.
CANONICAL = {
    "C02": "monthly_metrics", "C03": "revenue_by_customer", "C19": "financial_model", "C22": "hiring_plan",
    "C23": "expense_ledger", "C53": "founder_bios", "C59": "cover_note_and_index", "C60": "pitch_deck",
    "C61": "one_page_summary", "C72": "cap_table",
}
# Prefixes where the first word of the coverage pattern is not a readable word.
PREFIX = {"C47": "market_sizing", "C34": "order_form", "C75": "safe"}

# The folder words for each checklist piece, and for items that sit apart from their piece.
FOLDER_FOR_PIECE = {
    "traction and revenue": ("metrics",), "retention": ("metrics",), "unit economics": ("financials", "finance"),
    "burn and runway": ("financials", "finance"), "customers and contracts": ("contracts", "customers"),
    "market": ("overview",), "comps": ("overview",), "the pitch itself": ("overview",), "outside world": ("overview",),
    "team": ("team",), "legal and cap table": ("legal",), "AI and data governance": ("legal",),
}
FOLDER_FOR_ID = {
    "C22": ("team",), "C53": ("team",), "C54": ("team",), "C59": ("welcome",), "C63": ("product", "overview"),
    "C72": ("financials", "finance", "legal"), "C95": ("financials", "finance", "legal"),
    "C19": ("financials", "finance"), "C20": ("financials", "finance"), "C21": ("financials", "finance"),
    "C23": ("financials", "finance"),
}


class IntakeError(Exception):
    """A refused file or request. `status` is the HTTP status the route answers with."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status, self.message = status, message


# Rooms ------------------------------------------------------------------------------------


def rooms_root() -> Path:
    return Path(os.environ.get("TRICORDER_ROOMS_DIR") or ROOT / "rooms")


def is_room(path: Path) -> bool:
    return path.is_dir() and any(_NUMBERED.match(c.name) for c in path.iterdir() if c.is_dir())


def is_synthetic(room_dir: Path) -> bool:
    return Path(room_dir).resolve().is_relative_to(DATA_ROOM.resolve())


def find_room(room: str) -> Path | None:
    """A room id to its folder: data_room/ first, then rooms/, the same order as server/app.py."""
    if not _ROOM_ID.match(room or ""):
        return None
    for parent in (DATA_ROOM, rooms_root()):
        cand = parent / room
        if cand.is_dir() and not cand.is_symlink() and is_room(cand):
            return cand
    return None


def copy_command(room_dir: Path) -> str:
    rel = Path(room_dir).resolve().relative_to(ROOT) if Path(room_dir).resolve().is_relative_to(ROOT) else room_dir
    return f"python -m founder_requests copy-room {rel}"


def copy_room(src: Path, name: str | None = None) -> Path:
    """Copy a room (usually a synthetic one) to rooms/<name>, default <room>_live. Never overwrites."""
    src = Path(src)
    if not is_room(src):
        raise IntakeError(404, f"{src} is not a room")
    name = name or src.name + COPY_SUFFIX
    if not _ROOM_ID.match(name):
        raise IntakeError(400, "A room name uses letters, digits, '-' and '_' only.")
    if (DATA_ROOM / name).exists():
        raise IntakeError(409, f"'{name}' is a room in data_room/; the copy would be hidden behind it. Pick another name.")
    dest = rooms_root() / name
    if dest.exists():
        raise IntakeError(409, f"rooms/{name} already exists; it was not touched.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)
    return dest


# The file name and its bytes --------------------------------------------------------------


def check_name(name: str | None) -> tuple[str, str]:
    """(clean stem, extension) from the founder's file name, or IntakeError."""
    if not name:
        raise IntakeError(400, "The file has no name.")
    if any(ord(c) < 32 or ord(c) == 127 for c in name):
        raise IntakeError(400, "The file name has a control character.")
    base = re.split(r"[\\/]", name)[-1]
    if not base or base in (".", "..") or base.startswith("."):
        raise IntakeError(400, "The file name is empty or hidden.")
    stem, ext = os.path.splitext(base)
    ext = ext.lower()
    if ext not in ALLOWED:
        raise IntakeError(415, f"Files of kind '{ext or 'none'}' are not accepted. Accepted: {', '.join(ALLOWED)}.")
    ascii_stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode().lower()
    clean = re.sub(r"[^a-z0-9]+", "_", ascii_stem).strip("_")[:STEM_MAX].rstrip("_")
    return clean or "file", ext


def check_bytes(data: bytes, ext: str, max_unpacked: int = MAX_UNPACKED) -> None:
    """The bytes must be the kind the extension says, or IntakeError 415 (413 for a zip that unpacks too large)."""
    bad = IntakeError(415, f"The file's contents are not a {ext} file.")
    if ext == ".pdf":
        if not data.startswith(b"%PDF-"):
            raise bad
    elif ext in TEXT or ext == ".json":
        if b"\x00" in data or data.startswith((b"%PDF-", b"PK\x03\x04")):
            raise bad
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise bad from None
        if ext == ".json":
            try:
                json.loads(text)
            except ValueError:
                raise bad from None
    elif ext in OFFICE:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                infos = z.infolist()
        except (zipfile.BadZipFile, ValueError):
            raise bad from None
        names = {i.filename for i in infos}
        if "[Content_Types].xml" not in names or not any(n.startswith(OFFICE[ext]) for n in names):
            raise bad
        if len(infos) > MAX_ZIP_ENTRIES or sum(i.file_size for i in infos) > max_unpacked:
            raise IntakeError(413, "The file unpacks to more than the size limit.")
    elif ext == ".png":
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise bad
    elif ext in (".jpg", ".jpeg"):
        if not data.startswith(b"\xff\xd8\xff"):
            raise bad
    elif ext == ".mp4":
        if data[4:8] != b"ftyp":
            raise bad
    else:
        raise bad


def max_bytes() -> int:
    try:
        mb = float(os.environ.get("TRICORDER_UPLOAD_MAX_MB") or 25)
    except ValueError:
        mb = 25.0
    return int(mb * 1024 * 1024)


# Which request, which folder, which name ----------------------------------------------------


def resolve_request(answers: str | None, readout: Readout | None) -> cl.Row:
    """The checklist row a file answers: a checklist id, or an ask line's number in the readout."""
    rows = {r.id: r for r in cl.load()}
    answers = (answers or "").strip()
    cid = answers
    if answers.isdigit():
        n = int(answers)
        if readout is None or not 1 <= n <= len(readout.asks):
            raise IntakeError(422, f"There is no ask line {n}.")
        cid = readout.asks[n - 1].checklist_id or ""
    if not _REQUEST.match(cid) or cid not in rows:
        raise IntakeError(422, "Say which request this file answers: a checklist id such as C22, or the ask line's number.")
    row = rows[cid]
    if row.kind not in ("document", "ask"):
        raise IntakeError(422, f"{cid} is a check Tricorder runs, not a document. Add the file for the document it reads.")
    return row


def _numbered(room: Path) -> list[tuple[int, str]]:
    return sorted((int(m.group(1)), c.name) for c in room.iterdir()
                  if c.is_dir() and (m := _NUMBERED.match(c.name)))


def _folder(room: Path, row: cl.Row) -> str:
    if row.kind == "document" and row.id in cl.DOC_PATTERNS:
        held = cl.match_document(row, cl.room_files(room), room)
        if held and len(Path(held[0]).parts) > 1:
            return Path(held[0]).parts[0]
    words = FOLDER_FOR_ID.get(row.id) or FOLDER_FOR_PIECE.get(row.piece, ("overview",))
    folders = _numbered(room)
    for word in words:
        for _, name in folders:
            if word in _NUMBERED.match(name).group(2).lower():
                return name
    nxt = (folders[-1][0] + 1) if folders else 0
    return f"{nxt:02d}_{words[0]}"


def _prefix(cid: str) -> str | None:
    if cid in PREFIX:
        return PREFIX[cid]
    pat = cl.DOC_PATTERNS.get(cid)
    if not pat:
        return None
    first = re.sub(r"[\^$\\()?]", "", pat.split("|")[0]).strip("_/")
    return first or None


def target_for(room: Path, row: cl.Row, stem: str, ext: str) -> Path:
    """Where a file for this request lands, relative to the room: its folder and a name coverage recognises."""
    folder = _folder(Path(room), row)
    if row.id in CANONICAL:
        name = CANONICAL[row.id]
        if (Path(room) / folder / f"{name}{ext}").exists():
            name = f"{name}_from_founder_{stem}"[:STEM_MAX + 20]
    else:
        pat, prefix = cl.DOC_PATTERNS.get(row.id), _prefix(row.id)
        name = stem if not pat or re.search(pat, f"{stem}{ext}") or not prefix else f"{prefix}_{stem}"
    return Path(folder) / f"{name}{ext}"


def save(room: Path, rel: Path, data: bytes) -> Path:
    """Write the file exclusively, never through a link, never outside the room."""
    room = Path(room).resolve()
    rel = Path(rel)
    if rel.is_absolute() or ".." in rel.parts or len(rel.parts) != 2:
        raise IntakeError(400, "The target is not a file in one of the room's folders.")
    folder = room / rel.parent
    if folder.is_symlink() or (folder.exists() and not folder.resolve().is_relative_to(room)):
        raise IntakeError(400, "The room's folder is a link; nothing was written.")
    folder.mkdir(exist_ok=True)
    target = folder / rel.name
    try:
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
    except FileExistsError:
        raise IntakeError(409, f"{rel} is already in the room; nothing was overwritten.") from None
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    return target


# Waiting scans, the rerun and the rebuild ---------------------------------------------------


def _needs(name: str) -> tuple[str, ...]:
    return tuple(getattr(importlib.import_module(f"scans.{name}.scan"), "NEEDS", ()))


def waiting_scans(room: Path) -> list[str]:
    """Built scans whose needs are met and that have not seen every input file the room now holds."""
    held = {f for files in room_inputs(room).values() for f in files}
    out = []
    for name in available():
        if missing_needs(room, _needs(name)):
            continue
        result = out_dir(room) / f"{name}.json"
        try:
            seen = set(ScanResult.model_validate_json(result.read_text(encoding="utf-8")).inputs)
        except (OSError, ValueError):
            seen = None
        if seen is None or held - seen:
            out.append(name)
    return out


def run_scans(room: Path, names: list[str]) -> list[dict]:
    done = []
    for name in names:
        proc = subprocess.run([sys.executable, "-m", f"scans.{name}", str(room)], cwd=ROOT, capture_output=True,
                              text=True, env=os.environ.copy(), timeout=900)
        done.append({"scan": name, "ok": proc.returncode == 0,
                     "error": None if proc.returncode == 0 else proc.stderr[-1500:]})
    return done


def _readout(room: Path) -> Readout | None:
    try:
        return Readout.model_validate_json((out_dir(room) / "readout.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def item_status(readout: Readout | None, cid: str) -> str:
    if readout is None:
        return "unknown"
    for p in readout.panels:
        if p.name == COVERAGE_PANEL:
            for r in p.rows:
                if r[0] == cid:
                    return r[5]
    return "unknown"


def receive(room_dir: Path, data: bytes, name: str, answers: str | None) -> dict:
    """The whole intake: checks, save, waiting scans, merge, log. Returns the receipt."""
    from scans.memo.merge import build_readout, write_readout

    room = Path(room_dir)
    if is_synthetic(room):
        raise IntakeError(409, f"{room.name} is a synthetic room checked into the repo, so Tricorder never writes "
                               f"into it. Copy it first: {copy_command(room)}")
    if not room.resolve().is_relative_to(rooms_root().resolve()) or not is_room(room):
        raise IntakeError(409, "Files are added only to rooms under rooms/.")
    room = room.resolve()
    before = _readout(room)
    row = resolve_request(answers, before)
    if not data:
        raise IntakeError(400, "The file is empty.")
    if len(data) > max_bytes():
        raise IntakeError(413, f"The file is larger than the {max_bytes() // (1024 * 1024) or 1} MB limit.")
    stem, ext = check_name(name)
    check_bytes(data, ext)
    rel = target_for(room, row, stem, ext)
    status_before = item_status(before, row.id)
    save(room, rel, data)

    reran = run_scans(room, waiting_scans(room))
    readout = build_readout(room)
    target = write_readout(readout, room)
    receipt = {
        "room": room.name, "checklist_id": row.id, "item": row.item, "original_name": name,
        "saved": str(rel), "bytes": len(data), "scans_rerun": reran,
        "status_before": status_before, "status_after": item_status(readout, row.id),
        "asks_before": len(before.asks) if before else None, "asks_after": len(readout.asks),
        "at": now_iso(),
    }
    if CANONICAL.get(row.id) and rel.stem != CANONICAL[row.id]:
        receipt["note"] = (f"An earlier {CANONICAL[row.id]}{ext} is in the room, so this file was saved beside it. "
                           "The scans still read the earlier file.")
    log_path = out_dir(room) / LOG
    try:
        log = json.loads(log_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        log = {"received": []}
    log.setdefault("received", []).append(receipt)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    return receipt | {"readout": str(target)}
