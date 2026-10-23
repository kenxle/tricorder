"""Review wave 2a, O8: a deck that is not a PDF is a gap or no banner, never a crash."""

from __future__ import annotations

from scans.base import Ids, synthetic_notice
from scans.redflags import deck_vs_books, scan


def _room(tmp_path):
    room = tmp_path / "room"
    (room / "01_overview").mkdir(parents=True)
    (room / "01_overview" / "pitch_deck.pdf").write_bytes(b"this is not a PDF")
    return room


def test_synthetic_notice_is_none_for_a_deck_that_is_not_a_pdf(tmp_path):
    assert synthetic_notice(_room(tmp_path)) is None


def test_deck_vs_books_writes_a_gap_for_a_deck_that_is_not_a_pdf(tmp_path):
    claims, gaps, _panels = deck_vs_books.check(_room(tmp_path), Ids("redflags"))
    assert claims == []
    assert any(g.what.startswith("Not in the room: a readable pitch deck") for g in gaps)


def test_the_memo_merge_runs_on_such_a_room(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "out"))
    from scans.base import write_result
    from scans.memo.merge import build_readout

    room = _room(tmp_path)
    write_result(scan.run(room), room)
    readout = build_readout(room)
    assert readout.synthetic_notice is None
