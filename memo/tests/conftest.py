"""One real Hollis Voice readout per test session, built the way a user builds it."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from schema.claim import Readout

ROOT = Path(__file__).resolve().parents[2]
ROOM = ROOT / "data_room" / "hollis_voice"


def build_readout(out: Path, room: Path = ROOM) -> Path:
    env = {**os.environ, "TRICORDER_OUT_DIR": str(out)}
    for mod in ("scans.redflags", "scans.memo"):
        subprocess.run([sys.executable, "-m", mod, str(room)], cwd=ROOT, env=env, check=True, capture_output=True)
    return out / room.name / "readout.json"


@pytest.fixture(scope="session")
def readout_path(tmp_path_factory) -> Path:
    return build_readout(tmp_path_factory.mktemp("out"))


@pytest.fixture()
def readout(readout_path) -> Readout:
    return Readout.model_validate_json(readout_path.read_text(encoding="utf-8"))


@pytest.fixture()
def out_dir(tmp_path, monkeypatch) -> Path:
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    return tmp_path


def with_pieces(readout: Readout) -> Readout:
    """The real readout plus pieces, top flags and links, hand-built from its real claim ids.

    Hand-built test data: the pieces, top_flags and link steps are not built yet.
    The prototype uses the same shape (docs/features/20261023.03_memo_export/spike/simulate_steps.py).
    """
    from schema.claim import Piece, TopFlag

    r = readout.model_copy(deep=True)
    claims = {c.id: c for c in r.claims}
    claims["redflags-008"].corroborated_by = ["redflags-009"]
    claims["redflags-009"].corroborated_by = ["redflags-008"]
    claims["redflags-007"].conflicts_with = ["redflags-001"]
    claims["redflags-001"].conflicts_with = ["redflags-007"]
    r.pieces = [
        Piece(name="traction_and_revenue", verdict="looking_weak", reason=claims["redflags-007"].text,
              reason_claim_ids=["redflags-007"], claim_ids=["redflags-001", "redflags-007", "redflags-008", "redflags-009", "redflags-010"],
              corroborating_sources=1, contradicting_sources=1),
        Piece(name="burn_and_runway", verdict="mixed", reason=claims["redflags-004"].text,
              reason_claim_ids=["redflags-004"], claim_ids=["redflags-003", "redflags-004"]),
        Piece(name="unit_economics", verdict="not_enough_in_the_room", reason="Not in the room: unit economics by cohort.",
              claim_ids=["redflags-002", "redflags-005", "redflags-006"]),
    ]
    r.top_flags = [
        TopFlag(kind="green", piece="traction_and_revenue", rank=1, text="Green flag: the revenue chart matches the books.",
                claim_ids=["redflags-008"]),
        TopFlag(kind="red", piece="traction_and_revenue", rank=1, text="Red flag: the deck's ARR is above the P&L's.",
                claim_ids=["redflags-007"]),
    ]
    return r


@pytest.fixture()
def full_readout(readout) -> Readout:
    return with_pieces(readout)
