"""Memo versions on disk: out/<room>/memo/memo_v<N>.json.

A version, once written, is never overwritten: the save is an exclusive create (a hard link
from a temporary file, or O_CREAT|O_EXCL where the filesystem has no hard links), so of
two saves of the same version number one wins and the other gets FileExistsError, and a
reader never sees a half-written version. The page and the PDF are rendered from the
latest version into memo.html and memo.pdf beside them; each version's PDF is kept as
memo_v<N>.pdf, built once.
"""

from __future__ import annotations

import os
import re
import threading
from pathlib import Path

from scans.base import out_dir

from memo.model import Memo

_V = re.compile(r"^memo_v(\d+)\.json$")


def memo_dir(room_dir: str | Path) -> Path:
    return out_dir(room_dir) / "memo"


def versions(room_dir: str | Path) -> list[int]:
    d = memo_dir(room_dir)
    if not d.is_dir():
        return []
    return sorted(int(m.group(1)) for p in d.iterdir() if (m := _V.match(p.name)))


def load(room_dir: str | Path, version: int | None = None) -> Memo | None:
    vs = versions(room_dir)
    if not vs:
        return None
    v = vs[-1] if version is None else version
    path = memo_dir(room_dir) / f"memo_v{v}.json"
    if not path.exists():
        return None
    return Memo.model_validate_json(path.read_text(encoding="utf-8"))


def pdf_path(room_dir: str | Path, version: int) -> Path:
    return memo_dir(room_dir) / f"memo_v{version}.pdf"


def save(memo: Memo, room_dir: str | Path) -> Path:
    """Write a new version. FileExistsError when that version is already on disk."""
    path = memo_dir(room_dir) / f"memo_v{memo.version}.json"
    if path.exists():
        raise FileExistsError(f"version {memo.version} already exists; versions are never overwritten")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(memo.model_dump_json(indent=2) + "\n", encoding="utf-8")
    try:
        try:
            os.link(tmp, path)  # atomic and exclusive: fails when another save made this version first
        except FileExistsError:
            raise
        except OSError:  # a filesystem with no hard links (EPERM, ENOTSUP): an exclusive create instead
            _create_exclusive(path, tmp.read_bytes())
    except FileExistsError:
        raise FileExistsError(f"version {memo.version} already exists; versions are never overwritten") from None
    finally:
        tmp.unlink()  # the version's own name now holds the text; the temporary name is not a version
    return path


def _create_exclusive(path: Path, data: bytes) -> None:
    """Write `data` to a new file at `path`. FileExistsError when it is there already, so one save wins."""
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    with os.fdopen(fd, "wb") as f:
        f.write(data)


_locks: dict[str, threading.Lock] = {}
_locks_guard = threading.Lock()


def lock(room_dir: str | Path) -> threading.Lock:
    """One lock per room's memo folder, so one server builds a version's PDF once."""
    key = str(memo_dir(room_dir).resolve())
    with _locks_guard:
        return _locks.setdefault(key, threading.Lock())
