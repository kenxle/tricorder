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
from datetime import datetime
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


def resolve_requests(answers: str | None, readout: Readout | None) -> list[cl.Row]:
    """Every request one file answers: ids or ask line numbers, comma separated. The first decides where it lands."""
    out: list[cl.Row] = []
    for part in (answers or "").split(","):
        row = resolve_request(part, readout)
        if row.id not in {r.id for r in out}:
            out.append(row)
    return out


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
    """Built scans whose needs are met and that have not seen an input file added since their last run.

    A scan reads only some input kinds, and no scan declares which, so a file it left out on purpose
    must not make it wait forever: only files written at or after the scan's `ran_at` count."""
    held = {f for files in room_inputs(room).values() for f in files}
    out = []
    for name in available():
        if missing_needs(room, _needs(name)):
            continue
        result = out_dir(room) / f"{name}.json"
        try:
            last = ScanResult.model_validate_json(result.read_text(encoding="utf-8"))
            ran = datetime.fromisoformat(last.ran_at.replace("Z", "+00:00")).timestamp()
        except (OSError, ValueError):
            out.append(name)
            continue
        if any((Path(room) / f).stat().st_mtime >= ran for f in held - set(last.inputs)):
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


def _plain(name: str) -> str:
    return name.replace("_", " ")


def _first(texts: list[str], n: int = 3) -> str:
    """Up to n distinct sentences, in order; '...' when there are more."""
    distinct = list(dict.fromkeys(texts))
    return " ".join(distinct[:n]) + (" ..." if len(distinct) > n else "")


def changes(before: Readout | None, after: Readout, answered: list[tuple[cl.Row, str, str]], files: int = 1,
            failed: int = 0) -> list[str]:
    """What the files changed, in plain words: coverage, then claims, flags and verdicts, then the ask list."""
    said: list[str] = []
    for row, was, now in answered:
        if row.kind == "ask":
            said.append(f"{row.item} is something only the founder can give, so no check reads the file. "
                        "The line stays on the ask list.")
        elif now in ("found", "checked") and was not in ("found", "checked"):
            said.append(f"Coverage now finds {row.item}.")
        elif now != was:
            said.append(f"{row.item} moved from {_plain(was)} to {_plain(now)} in coverage.")
        else:
            said.append(f"Coverage still lists {row.item} as {_plain(now)}. The file is saved under the name "
                        "for the first request it answers.")
    old = before or Readout(room=after.room, built_at="")
    # A claim keeps its id when a rerun relabels it, so the same id with new words is a change.
    old_by_id = {(c.scan, c.id): c.text for c in old.claims}
    new_by_id = {(c.scan, c.id): c.text for c in after.claims}
    new_claims = [t for k, t in new_by_id.items() if k not in old_by_id]
    changed = [t for k, t in new_by_id.items() if k in old_by_id and old_by_id[k] != t]
    gone = [k for k in old_by_id if k not in new_by_id]
    moved = False
    if changed:
        word = "claim" if len(changed) == 1 else "claims"
        said.append(f"{len(changed)} {word} changed. Now: " + _first(changed))
        moved = True
    if new_claims:
        word = "claim" if len(new_claims) == 1 else "claims"
        said.append(f"{len(new_claims)} new {word}: " + _first(new_claims))
        moved = True
    if gone:
        said.append(f"{len(gone)} claim{'' if len(gone) == 1 else 's'} no longer in the readout.")
        moved = True
    old_flags = {(f.kind, f.text) for f in old.top_flags}
    new_flags = {(f.kind, f.text) for f in after.top_flags}
    for kind, text in sorted(new_flags - old_flags):
        said.append(f"New {kind} flag: {text}")
        moved = True
    for kind, text in sorted(old_flags - new_flags):
        said.append(f"No longer a {kind} flag: {text}")
        moved = True
    verdicts = {p.name: p.verdict for p in old.pieces}
    for p in after.pieces:
        if p.name in verdicts and verdicts[p.name] != p.verdict:
            said.append(f"{_plain(p.name).capitalize()} moved from {_plain(verdicts[p.name])} to {_plain(p.verdict)}.")
            moved = True
    if not moved:
        said.append(f"No check reads {'this file' if files == 1 else 'these files'} yet, so no number changed.")
    if failed:
        what = "the new file" if files == 1 else "the new files"
        lead = "One check" if failed == 1 else f"{failed} checks"
        said.append(f"{lead} could not read {what}, so {'its' if failed == 1 else 'their'} part of the readout is from before.")
    if before is not None and len(after.asks) != len(before.asks):
        way = "down" if len(after.asks) < len(before.asks) else "up"
        said.append(f"The ask list is {way} from {len(before.asks)} to {len(after.asks)} lines.")
    return said


def _check_room(room: Path) -> Path:
    if is_synthetic(room):
        raise IntakeError(409, f"{room.name} is a synthetic room checked into the repo, so Tricorder never writes "
                               f"into it. Copy it first: {copy_command(room)}")
    if not room.resolve().is_relative_to(rooms_root().resolve()) or not is_room(room):
        raise IntakeError(409, "Files are added only to rooms under rooms/.")
    return room.resolve()


def receive_batch(room_dir: Path, files: list[tuple[bytes, str, str | None]]) -> dict:
    """Several files in one add: every file is checked before any is written, then one rerun and one rebuild.

    Each entry is (bytes, the founder's file name, the requests it answers: "C22" or "6,C97")."""
    from scans.memo.merge import build_readout, write_readout

    room = _check_room(Path(room_dir))
    if not files:
        raise IntakeError(400, "No files were added.")
    before = _readout(room)
    total = 0
    plans = []
    for data, name, answers in files:
        rows = resolve_requests(answers, before)
        if not data:
            raise IntakeError(400, f"{name or 'The file'} is empty.")
        total += len(data)
        if len(data) > max_bytes() or total > max_bytes() * 4:
            raise IntakeError(413, f"{name} is larger than the {max_bytes() // (1024 * 1024) or 1} MB limit.")
        stem, ext = check_name(name)
        try:
            check_bytes(data, ext)
        except IntakeError as err:
            raise IntakeError(err.status, f"{name}: {err.message}") from None
        plans.append((data, name, rows, stem, ext))
    targets: set[Path] = set()
    saved = []
    for data, name, rows, stem, ext in plans:
        rel = target_for(room, rows[0], stem, ext)
        if rel in targets:
            raise IntakeError(409, f"Two files in this add would both be saved as {rel}. Add them one at a time.")
        targets.add(rel)
        saved.append((rel, data, name, rows, ext))
    for rel, data, *_ in saved:
        if (room / rel).exists():
            raise IntakeError(409, f"{rel} is already in the room; nothing was overwritten.")
    for rel, data, *_ in saved:
        save(room, rel, data)

    reran = run_scans(room, waiting_scans(room))
    readout = build_readout(room)
    target = write_readout(readout, room)
    at = now_iso()
    entries, answered = [], []
    for rel, data, name, rows, ext in saved:
        answers = [{"checklist_id": r.id, "item": r.item, "status_before": item_status(before, r.id),
                    "status_after": item_status(readout, r.id)} for r in rows]
        answered += [(r, a["status_before"], a["status_after"]) for r, a in zip(rows, answers)]
        entry = {"original_name": name, "saved": str(rel), "bytes": len(data), "answers": answers,
                 "checklist_id": rows[0].id, "item": rows[0].item, "at": at}
        if CANONICAL.get(rows[0].id) and rel.stem != CANONICAL[rows[0].id]:
            entry["note"] = (f"An earlier {CANONICAL[rows[0].id]}{ext} is in the room, so this file was saved beside "
                             "it. The scans still read the earlier file.")
        entries.append(entry)
    receipt = {
        "room": room.name, "files": entries, "scans_rerun": reran,
        "asks_before": len(before.asks) if before else None, "asks_after": len(readout.asks),
        "summary": changes(before, readout, answered, len(entries), sum(not r["ok"] for r in reran)), "at": at,
    }
    log_path = out_dir(room) / LOG
    try:
        log = json.loads(log_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        log = {"received": []}
    for e in entries:
        log.setdefault("received", []).append(e | {"summary": receipt["summary"]})
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    return receipt | {"readout": str(target)}


def receive(room_dir: Path, data: bytes, name: str, answers: str | None) -> dict:
    """One file: the batch of one, with its first entry's fields at the top for a short receipt."""
    receipt = receive_batch(room_dir, [(data, name, answers)])
    first = receipt["files"][0]
    top = {k: first[k] for k in ("checklist_id", "item", "original_name", "saved", "bytes") }
    top |= {"status_before": first["answers"][0]["status_before"], "status_after": first["answers"][0]["status_after"]}
    if "note" in first:
        top["note"] = first["note"]
    return receipt | top
