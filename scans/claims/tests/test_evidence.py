"""Evidence readers on hand-built page text (review wave 2a, O5).

The bios and contracts are replaced by hand-built pages through monkeypatch, so
each test says exactly which words are on the page.
"""

from __future__ import annotations

from pathlib import Path

import schema.readers
import scans.claims.evidence as evidence
from scans.claims import extract

BIOS = ("Imogen Hale ran operations for a regional veterinary group for eleven years.\n"
        "Teodoro Brandt spent nine years building speech systems at Kestrel Telecom Software.\n")


def _room(tmp_path: Path, rel: str) -> Path:
    path = tmp_path / rel
    path.parent.mkdir(parents=True)
    path.write_bytes(b"%PDF hand-built stand-in")
    return tmp_path


def _statement(text: str):
    return extract._spoken(text, "script", "01_overview/pitch_video_script.md", "line 1", line=1, beat="0:10")[0]


def test_founder_years_must_be_said_of_the_founder_the_pitch_names(tmp_path, monkeypatch):
    room = _room(tmp_path, "05_team/founder_bios.pdf")
    monkeypatch.setattr(schema.readers, "pdf_pages", lambda path: [BIOS])
    st = _statement("My co-founder, Teodoro Brandt, spent eleven years building speech systems.")
    reading = evidence.READERS["bios_years"](room, st, "2026-09-30")
    # Imogen's eleven years say nothing about Teodoro; only Teodoro's nine years count.
    assert [e.number for e in reading.evidence] == [9]
    assert not reading.any_of
    e = reading.evidence[0]
    assert "Teodoro" in e.source.quote and "'nine years'" in e.how


def test_a_contract_date_says_exactly_which_date_on_which_line_matched(tmp_path, monkeypatch):
    room = _room(tmp_path, "04_contracts/pilot_agreement_marlow.pdf")
    page = "Pilot agreement with Marlow Veterinary Group\nStart date: 2026-08-01\nInvoice terms: net 30\n"
    monkeypatch.setattr(schema.readers, "pdf_pages", lambda path: [page])
    st = next(s for s in extract._spoken("Marlow Veterinary Group started a pilot in August 2026.", "script",
                                         "x.md", "line 1", line=1, beat="0:10"))
    reading = evidence.READERS["contract_date"](room, st, "2026-09-30")
    assert len(reading.evidence) == 1
    e = reading.evidence[0]
    assert e.source.quote == "Start date: 2026-08-01"
    assert "2026-08-01" in e.how and "Marlow" in e.how
