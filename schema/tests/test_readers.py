"""One known locator from each format, read from the generated room and checked
against data_room/answer_key.json, so the readers and the generator agree."""

import json
from pathlib import Path

import pytest

from schema import readers
from schema.claim import Source

ROOT = Path(__file__).resolve().parents[2]
ROOM = ROOT / "data_room" / "hollis_voice"
KEY = json.loads((ROOT / "data_room" / "answer_key.json").read_text())
FIXTURES = Path(__file__).parent / "fixtures"


def _locations():
    for entry in KEY["flags"] + KEY["decoys"] + KEY["green_flags"]:
        for loc in entry.get("locations", []):
            yield entry["id"], loc


def test_pdf_page_holds_each_key_text():
    checked = 0
    for _id, loc in _locations():
        if loc["file"].endswith(".pdf") and "page" in loc and "text" in loc:
            text = readers.pdf_page(ROOM / loc["file"], loc["page"])
            assert loc["text"] in text, (_id, loc)
            checked += 1
    assert checked >= 10


def test_xlsx_cell_and_defined_name_hold_each_key_value():
    checked = 0
    for _id, loc in _locations():
        if loc["file"].endswith(".xlsx") and ":" not in loc.get("cell", ":"):
            want = loc.get("expect", loc.get("value"))
            if want is None:
                continue
            got = readers.xlsx_cell(ROOM / loc["file"], f"{loc['sheet']}!{loc['cell']}")
            assert got == pytest.approx(want, rel=1e-5) if isinstance(want, (int, float)) else got == want, (_id, loc, got)
            if "named_cell" in loc:
                assert readers.xlsx_cell(ROOM / loc["file"], loc["named_cell"]) == got
                assert readers.xlsx_defined_name(ROOM / loc["file"], loc["named_cell"]) == f"{loc['sheet']}!{loc['cell']}"
            checked += 1
    assert checked >= 10


def test_csv_row_one_is_the_header():
    path = ROOM / "03_metrics" / "monthly_metrics.csv"
    assert readers.csv_row_text(path, 1).startswith("month,mrr,arr")
    rows = readers.csv_rows(path)
    assert rows[0]["month"] == "2025-01"
    assert readers.csv_row_text(path, 2).startswith(rows[0]["month"] + ",")


def test_md_line():
    assert readers.md_line(ROOM / "01_overview" / "pitch_video_script.md", 1).startswith("# Hollis Voice")


@pytest.mark.parametrize("name", ["pitch_video.transcript.json", "whisper_cpp.json"])
def test_transcript_shapes(name):
    segs = readers.transcript_segments(FIXTURES / name)
    spoken = [s for s in segs if "three million" in s["text"]][0]
    assert spoken["start_s"] == pytest.approx(39.1) and spoken["end_s"] == pytest.approx(44.8)


def test_text_at_dispatches_by_format():
    def src(uri, locator, kind="file"):
        return Source(kind=kind, uri=uri, locator=locator, quote="x")

    assert "$2.5M" in readers.text_at(src("01_overview/pitch_deck.pdf", "slide 3"), ROOM)
    assert readers.text_at(src("02_financials/financial_model.xlsx", "ARR_TOTAL"), ROOM) == "2240868"
    assert readers.text_at(src("03_metrics/monthly_metrics.csv", "row 1"), ROOM).startswith("month,")
    assert "8. No duty to convert." in readers.text_at(src("04_customers/pilot_agreement_marlow.pdf", "clause 8"), ROOM)
    video = str(FIXTURES / "pitch_video.transcript.json")
    assert "three million" in readers.text_at(src(video, "t=40-41", "video"), ROOM)
    assert "January 2025" in readers.text_at(src(video, "seg 1", "video"), ROOM)


def test_a_bad_locator_raises_locator_error():
    with pytest.raises(readers.LocatorError):
        readers.pdf_page(ROOM / "01_overview" / "pitch_deck.pdf", 99)
    with pytest.raises(readers.LocatorError):
        readers.xlsx_cell(ROOM / "02_financials" / "financial_model.xlsx", "NO_SUCH_NAME")
