from pathlib import Path

from schema.claim import Claim, ScanResult
from scans.base import write_result
from scans.memo.merge import build_readout

ROOM = Path(__file__).resolve().parents[3] / "data_room" / "hollis_voice"


def _claim(cid, quote):
    return Claim.model_validate({
        "id": cid, "scan": "redflags", "text": "A test claim.",
        "check": {"kind": "script", "name": "test"}, "confidence": "computed",
        "sources": [{"kind": "file", "uri": "01_overview/pitch_deck.pdf", "locator": "slide 4", "quote": quote}],
    })


def test_a_missing_scan_is_a_gap_not_a_crash(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    readout = build_readout(ROOM)
    assert readout.scans_run == []
    assert "redflags" in readout.scans_missing
    assert any("redflags" in g.what for g in readout.gaps)
    assert readout.synthetic_notice and "Synthetic" in readout.synthetic_notice


def test_unverified_claims_go_to_their_own_box(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    result = ScanResult(scan="redflags", room="hollis_voice", ran_at="2026-10-24T10:00:00Z",
                        claims=[_claim("redflags-001", "No customer above 9% of ARR"), _claim("redflags-002", "We have no churn")])
    write_result(result, ROOM)
    readout = build_readout(ROOM)
    assert [c.id for c in readout.claims] == ["redflags-001"]
    assert [c.id for c in readout.unverified] == ["redflags-002"]
    assert readout.scans_run == ["redflags"]
