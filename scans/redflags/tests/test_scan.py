from pathlib import Path

from schema.claim import ScanResult
from scans.redflags import scan

ROOM = Path(__file__).resolve().parents[3] / "data_room" / "hollis_voice_seed_drop"


def test_the_engine_runs_on_the_seed_drop_and_returns_a_result():
    result = scan.run(ROOM)
    assert isinstance(result, ScanResult)
    assert result.scan == "redflags" and result.room == "hollis_voice_seed_drop"
    assert "01_overview/pitch_deck.pdf" in result.inputs


def test_claim_ids_are_unique():
    ids = [c.id for c in scan.run(ROOM).claims]
    assert len(ids) == len(set(ids))
