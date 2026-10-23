"""Memo versions on disk: out/<room>/memo/memo_v<N>.json.

A version, once written, is never overwritten. The page and the PDF are
rendered from the latest version into memo.html and memo.pdf beside them.
"""

from __future__ import annotations

import re
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


def save(memo: Memo, room_dir: str | Path) -> Path:
    path = memo_dir(room_dir) / f"memo_v{memo.version}.json"
    if path.exists():
        raise FileExistsError(f"version {memo.version} already exists; versions are never overwritten")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(memo.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return path
