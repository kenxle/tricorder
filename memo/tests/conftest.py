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
# The scans a user runs before the memo, then the merge. A scan added here adds claims; no test names a count.
SCANS = ("scans.redflags", "scans.claims", "scans.memo")


def build_readout(out: Path, room: Path = ROOM) -> Path:
    # No model calls in tests: the claims scan reads only what its script can parse without a key.
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["TRICORDER_OUT_DIR"] = str(out)
    for mod in SCANS:
        subprocess.run([sys.executable, "-m", mod, str(room)], cwd=ROOT, env=env, check=True, capture_output=True)
    return out / room.name / "readout.json"


@pytest.fixture(autouse=True)
def no_model(monkeypatch):
    """No model calls in memo tests: the expert-read sections use the script's draft."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


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


def by_check(readout: Readout, name: str, severity: str | None = None) -> list[str]:
    """The ids of the claims a check wrote, in readout order. Tests name checks, never claim numbers."""
    return [c.id for c in readout.claims if c.check.name == name and (severity is None or c.severity == severity)]


def flagged(readout: Readout) -> list[str]:
    return [c.id for c in readout.claims if c.severity == "flag"]


def with_pieces(readout: Readout) -> Readout:
    """The real readout plus pieces, top flags and links, hand-built on its real claims.

    Hand-built test data: the pieces, top_flags and link steps are not built yet.
    Every id is looked up by the check that wrote it, so a new check never breaks this.
    The prototype uses the same shape (docs/features/20261023.03_memo_export/spike/simulate_steps.py).
    """
    from schema.claim import Piece, TopFlag

    r = readout.model_copy(deep=True)
    claims = {c.id: c for c in r.claims}
    deck_arr = by_check(r, "deck_revenue_vs_pnl", "flag")[0]
    mrr = by_check(r, "mrr_column_vs_subscription_rows", "flag")[0]
    chart, history = by_check(r, "deck_revenue_vs_pnl", "info")[0], by_check(r, "deck_history_vs_metrics")[0]
    cash = by_check(r, "capitalised_spend_vs_pnl_and_cash")[0]
    contractors = by_check(r, "contractor_spend_vs_headcount_and_burn")[0]
    billings = by_check(r, "billings_vs_recognised_revenue")[0]
    fees = by_check(r, "one_time_fees_in_recurring_metrics")[0]
    deferred = by_check(r, "deferred_revenue_vs_earned")[0]
    claims[chart].corroborated_by = [history]
    claims[history].corroborated_by = [chart]
    claims[deck_arr].conflicts_with = [mrr]
    claims[mrr].conflicts_with = [deck_arr]
    r.pieces = [
        Piece(name="traction_and_revenue", verdict="looking_weak", reason=claims[deck_arr].text,
              reason_claim_ids=[deck_arr], claim_ids=[mrr, deck_arr, chart, history],
              corroborating_sources=1, contradicting_sources=1),
        Piece(name="burn_and_runway", verdict="mixed", reason=claims[cash].text,
              reason_claim_ids=[cash], claim_ids=[contractors, cash]),
        Piece(name="unit_economics", verdict="not_enough_in_the_room", reason="Not in the room: unit economics by cohort.",
              claim_ids=[billings, deferred, fees]),
    ]
    r.top_flags = [
        TopFlag(kind="green", piece="traction_and_revenue", rank=1, text="Green flag: the revenue chart matches the books.",
                claim_ids=[chart]),
        TopFlag(kind="red", piece="traction_and_revenue", rank=1, text="Red flag: the deck's ARR is above the P&L's.",
                claim_ids=[deck_arr]),
    ]
    return r


@pytest.fixture()
def full_readout(readout) -> Readout:
    return with_pieces(readout)
