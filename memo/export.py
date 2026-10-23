"""Export: readout -> a new memo version, its page and its PDF.

The one path the CLI and the server routes share. The first export of a room
writes version 1. A later export redrafts from the current readout and keeps
the operator's lines. Edits make a version from the latest one.
"""

from __future__ import annotations

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


def render(memo: Memo, room_dir: Path, pdf: bool = True) -> tuple[Path, Path | None]:
    folder = store.memo_dir(room_dir)
    folder.mkdir(parents=True, exist_ok=True)
    html_path = folder / "memo.html"
    html_path.write_text(render_html(memo), encoding="utf-8")
    pdf_path = render_pdf(memo, folder / "memo.pdf") if pdf else None
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


def edit(room_dir: Path, edits: list[Edit], author: str, pdf: bool = True) -> Written:
    room_dir = Path(room_dir)
    latest = store.load(room_dir)
    if latest is None:
        raise NoReadout(f"no memo yet; export one first with: python -m memo {room_dir}")
    memo = apply_edits(latest, edits, author, now_iso())
    path = store.save(memo, room_dir)
    html_path, pdf_path = render(memo, room_dir, pdf)
    return Written(memo, path, html_path, pdf_path)
