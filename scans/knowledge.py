"""Kimmy's expert knowledge, one file per readout piece: knowledge/<piece>.md.

A model call that reads for a piece passes `block(pieces)` to clients.llm.read
as `knowledge=`, so the words the model reads carry how an expert investor
looks at that piece. The knowledge is a lens, not evidence: the block tells the
model never to quote it, cite it or take a number from it. Numbers still come
from scripts.

A missing or unreadable file means no knowledge for that piece, never an error.
Piece names are the readout's (`schema.claim.PIECE_ORDER`), for example
"traction_and_revenue" and "burn_and_runway".
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent / "knowledge"
_PIECE = re.compile(r"[a-z][a-z0-9_]*")

LENS = ("How an expert investor reads this piece. Use it to decide what to look for and how to describe "
        "what the documents show. It is not a document: never quote it, cite it, or take a number from it. "
        "Every claim still rests only on the documents and script results in this message.")


def text(piece: str, root: Path = ROOT) -> str:
    """The piece's knowledge file, or "" when there is none."""
    if not piece or not _PIECE.fullmatch(piece):
        return ""
    try:
        return (root / f"{piece}.md").read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return ""


def block(pieces: Iterable[str | None], root: Path = ROOT) -> str | None:
    """The <expert_knowledge> blocks for the pieces that have a file, or None when none do."""
    parts = []
    for piece in dict.fromkeys(p for p in pieces if p):
        body = text(piece, root)
        if body:
            parts.append(f'<expert_knowledge piece="{piece}">\n{LENS}\n\n{body}\n</expert_knowledge>')
    return "\n\n".join(parts) or None
