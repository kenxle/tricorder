"""Export: readout -> a new memo version, its page and its PDF.

The one path the CLI and the server routes share. The first export of a room
writes version 1. A later export redrafts from the current readout and keeps
the operator's lines. Edits make a version from the latest one.
"""

from __future__ import annotations

import os
import shutil
import threading
from dataclasses import dataclass
from pathlib import Path

from schema.claim import Readout
from scans.base import now_iso, out_dir

from memo import store
from memo.build import build_memo
from memo.edit import apply_edits, carry_operator_lines
from memo.html import render_html
from memo.model import Edit, Memo
from memo.pdf import render_pdf


class NoReadout(FileNotFoundError):
    """No readout.json for the room yet."""


@dataclass
class Written:
    memo: Memo
    json: Path
    html: Path
    pdf: Path | None


def readout_path(room_dir: Path) -> Path:
    return out_dir(room_dir) / "readout.json"


def load_readout(room_dir: Path, path: Path | None = None) -> Readout:
    path = path or readout_path(room_dir)
    if not path.exists():
        raise NoReadout(f"no readout at {path}; build it first with: python -m scans.memo {room_dir}")
    return Readout.model_validate_json(path.read_text(encoding="utf-8"))


def _replace(path: Path, text: str | None = None, src: Path | None = None) -> None:
    """Write path whole or not at all, so a reader never gets half a page or half a PDF."""
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    if src is not None:
        shutil.copyfile(src, tmp)
    else:
        tmp.write_text(text or "", encoding="utf-8")
    os.replace(tmp, path)


def version_pdf(memo: Memo, room_dir: Path) -> Path:
    """The PDF of this version: built once, then served as saved (review wave 2b S3)."""
    path = store.pdf_path(room_dir, memo.version)
    with store.lock(room_dir):
        if not path.exists():
            tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
            render_pdf(memo, tmp)
            os.replace(tmp, path)
    return path


def render(memo: Memo, room_dir: Path, pdf: bool = True) -> tuple[Path, Path | None]:
    folder = store.memo_dir(room_dir)
    folder.mkdir(parents=True, exist_ok=True)
    html_path = folder / "memo.html"
    _replace(html_path, render_html(memo))
    if not pdf:
        return html_path, None
    pdf_path = folder / "memo.pdf"
    _replace(pdf_path, src=version_pdf(memo, room_dir))
    return html_path, pdf_path


def export(room_dir: Path, readout_file: Path | None = None, pdf: bool = True) -> Written:
    room_dir = Path(room_dir)
    readout = load_readout(room_dir, readout_file)
    at = now_iso()
    memo = build_memo(readout, room_dir, at)
    latest = store.load(room_dir)
    if latest is not None:
        memo = carry_operator_lines(latest, memo, at)
    path = store.save(memo, room_dir)
    html_path, pdf_path = render(memo, room_dir, pdf)
    return Written(memo, path, html_path, pdf_path)


def edit(room_dir: Path, edits: list[Edit], author: str, pdf: bool = True, base: Memo | None = None) -> Written:
    """The next version, made from `base` (the version the editor saw) or, without one, the latest.
    FileExistsError when another save made that version first: the caller answers 409."""
    room_dir = Path(room_dir)
    latest = base if base is not None else store.load(room_dir)
    if latest is None:
        raise NoReadout(f"no memo yet; export one first with: python -m memo {room_dir}")
    memo = apply_edits(latest, edits, author, now_iso())
    path = store.save(memo, room_dir)
    html_path, pdf_path = render(memo, room_dir, pdf)
    return Written(memo, path, html_path, pdf_path)
