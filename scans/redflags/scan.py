"""The red-flag engine: runs every check in CHECKS and writes one ScanResult."""

from __future__ import annotations

import importlib
from pathlib import Path

from schema.claim import ScanResult
from scans.base import Ids, now_iso, room_inputs, room_name

NAME = "redflags"
NEEDS = ("deck",)

# Modules in this package that define check(room, ids) returning
# (claims, gaps) or (claims, gaps, panels). Add one line per
# FRAMEWORKS entry as it lands. A module listed here that does not exist yet
# is skipped, so parallel branches can each add their own line.
CHECKS: tuple[str, ...] = (
    "deck_claims",      # 1.1 Deck claim extraction
    "arr_definition",   # 1.2 ARR definition check
    "cohorts",          # 1.3 Cohort retention rebuild
    "burn_runway",      # 1.4 Burn against the hiring plan and runway
    "deck_vs_model",    # 1.5 Deck-against-model reconciliation
    "concentration",    # 1.6 Customer concentration
    "gross_margin",     # 1.7 Gross margin composition
    "vanity",           # 1.8 Vanity metric check
    "cap_table",        # 1.10 Cap table reconciliation
    "mislabels",        # 1.12 Accounting mislabels
    "contract_terms",   # 1.13 Contract terms
    "deck_vs_books",    # Deck revenue against the P&L
)


def _load(name: str):
    try:
        return importlib.import_module(f"scans.redflags.{name}")
    except ModuleNotFoundError as err:
        if err.name == f"scans.redflags.{name}":
            return None
        raise


def run(room_dir: Path) -> ScanResult:
    ids = Ids(NAME)
    claims, gaps, panels = [], [], []
    for name in CHECKS:
        module = _load(name)
        if module is None:
            continue
        out = module.check(Path(room_dir), ids)
        claims += out[0]
        gaps += out[1]
        if len(out) > 2:
            panels += out[2]
    inputs = sorted({f for files in room_inputs(room_dir).values() for f in files})
    return ScanResult(scan=NAME, room=room_name(room_dir), ran_at=now_iso(), inputs=inputs, claims=claims, gaps=gaps, panels=panels)
