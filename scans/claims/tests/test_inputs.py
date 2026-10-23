"""Partial rooms and other input shapes, through `python -m scans.claims`.

The transcripts here are hand-built test data in the shapes schema/readers.py
reads (our own {"segments": [...]} and whisper.cpp's -oj output). The video is
not recorded yet, so no real transcript exists.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from schema.check_quotes import check_result
from schema.claim import ScanResult

ROOT = Path(__file__).resolve().parents[3]
HOLLIS = ROOT / "data_room" / "hollis_voice"


def make_room(tmp: Path, files: list[str], name: str = "room") -> Path:
    room = tmp / name
    for rel in files:
        target = room / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(HOLLIS / rel, target)
    return room


def scan(room: Path, out: Path) -> ScanResult:
    env = dict(os.environ, TRICORDER_OUT_DIR=str(out))
    env.pop("ANTHROPIC_API_KEY", None)
    done = subprocess.run([sys.executable, "-m", "scans.claims", str(room)], cwd=ROOT, env=env, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return ScanResult.model_validate_json((out / room.name / "claims.json").read_text(encoding="utf-8"))


SEGMENTS = [
    {"id": 0, "start_s": 35.2, "end_s": 41.0, "text": "We started charging in January 2025. Since then we have grown every quarter."},
    {"id": 1, "start_s": 41.0, "end_s": 47.5, "text": "Today we're at about three million dollars in annual recurring revenue."},
    {"id": 2, "start_s": 104.0, "end_s": 111.0, "text": "At our plan, that gives us 37 months of runway."},
]


def test_transcript_is_used_and_times_are_copied(tmp_path):
    room = make_room(tmp_path, ["01_overview/pitch_deck.pdf", "01_overview/pitch_video_script.md",
                                "02_financials/financial_model.xlsx", "03_metrics/monthly_metrics.csv"])
    (room / "01_overview" / "pitch_video.transcript.json").write_text(json.dumps({"segments": SEGMENTS}), encoding="utf-8")
    result = scan(room, tmp_path / "out")
    spoken = [c for c in result.claims if c.sources[0].kind == "video"]
    assert spoken and not any(c.sources[0].uri.endswith(".md") for c in result.claims)  # the transcript wins over the script
    arr = next(c for c in spoken if c.sources[0].locator == "seg 1")
    assert (arr.sources[0].start_s, arr.sources[0].end_s) == (41.0, 47.5)
    assert arr.text.startswith("Contradicted: The pitch video (41s to 48s) gives ARR as about three million dollars")
    assert arr.check.name == "spoken_arr_vs_claims_page"
    assert "01_overview/pitch_deck.pdf" in [s.uri for s in arr.sources]
    runway = next(c for c in spoken if c.sources[0].locator == "seg 2")
    assert runway.text.startswith("Unsupported:") and "only a model reading backs this" in runway.text  # the model alone
    _, failures = check_result(result, room)
    assert failures == {}
    assert not any("transcript of the pitch video" in g.what for g in result.gaps)


def test_whisper_cpp_output_shape(tmp_path):
    room = make_room(tmp_path, ["01_overview/pitch_deck.pdf", "02_financials/financial_model.xlsx"])
    whisper = {"transcription": [{"offsets": {"from": int(s["start_s"] * 1000), "to": int(s["end_s"] * 1000)}, "text": " " + s["text"]}
                                 for s in SEGMENTS]}
    (room / "01_overview" / "pitch_video.transcript.json").write_text(json.dumps(whisper), encoding="utf-8")
    result = scan(room, tmp_path / "out")
    arr = next(c for c in result.claims if c.sources[0].kind == "video" and c.sources[0].locator == "seg 1")
    assert arr.sources[0].start_s == 41.0
    assert check_result(result, room)[1] == {}


def test_unreadable_deck_falls_back_to_claims_json(tmp_path):
    room = make_room(tmp_path, ["01_overview/claims.json", "02_financials/financial_model.xlsx"])
    (room / "01_overview" / "pitch_deck.pdf").write_bytes(b"not a pdf")
    result = scan(room, tmp_path / "out")
    assert result.claims and all(c.sources[0].uri == "01_overview/claims.json" for c in result.claims)
    arr = next(c for c in result.claims if c.value and c.value.label == "arr")
    assert arr.text.startswith("Contradicted: The deck's claims.json gives ARR as $2,500,000")
    assert check_result(result, room)[1] == {}
    assert any("claims.json stands in" in g.what for g in result.gaps)


def test_no_deck_is_a_gap_and_the_script_still_reads(tmp_path):
    room = make_room(tmp_path, ["01_overview/pitch_video_script.md"])
    result = scan(room, tmp_path / "out")
    assert any(g.what.startswith("Not in the room: the pitch deck") for g in result.gaps)
    assert result.claims and all(c.text.startswith("Unsupported:") for c in result.claims)
    assert check_result(result, room)[1] == {}


def test_deck_alone_is_all_unsupported_with_missing_files_named(tmp_path):
    room = make_room(tmp_path, ["01_overview/pitch_deck.pdf"])
    result = scan(room, tmp_path / "out")
    assert all(c.text.startswith("Unsupported:") for c in result.claims)
    whys = " ".join(g.why for g in result.gaps)
    for doc in ("the financial model", "the metrics export", "monthly revenue by customer", "the cap table", "the hiring plan"):
        assert doc in whys
    assert any("transcript of the pitch video, or its script" in g.what for g in result.gaps)


def test_empty_room_exits_zero(tmp_path):
    room = tmp_path / "empty"
    room.mkdir()
    result = scan(room, tmp_path / "out")
    assert result.claims == []
    assert {g.what.split(":")[0] for g in result.gaps} == {"Not in the room"}


def test_a_missing_named_cell_and_a_missing_column_fall_through_without_a_crash(tmp_path):
    """CS-F6: the model loses its ARR_TOTAL name and the metrics export loses its
    paying-customers column. The scan still exits 0, ARR is still read from the
    other documents, and every claim passes the quote checker."""
    import csv

    import openpyxl

    room = make_room(tmp_path, ["01_overview/pitch_deck.pdf", "02_financials/financial_model.xlsx",
                                "03_metrics/monthly_metrics.csv", "03_metrics/customer_mrr_by_month.csv"])
    model = room / "02_financials" / "financial_model.xlsx"
    wb = openpyxl.load_workbook(model)
    del wb.defined_names["ARR_TOTAL"]
    wb.save(model)
    metrics = room / "03_metrics" / "monthly_metrics.csv"
    rows = list(csv.reader(metrics.read_text(encoding="utf-8").splitlines()))
    drop = rows[0].index("paying_accounts")
    metrics.write_text("\n".join(",".join(r[:drop] + r[drop + 1:]) for r in rows) + "\n", encoding="utf-8")

    result = scan(room, tmp_path / "out")
    assert check_result(result, room)[1] == {}
    arr = next(c for c in result.claims if c.value and c.value.label == "arr" and c.sources[0].locator == "slide 3")
    assert arr.text.startswith("Contradicted:")
    assert "02_financials/financial_model.xlsx" not in [s.uri for s in arr.sources]
    assert "03_metrics/monthly_metrics.csv" in [s.uri for s in arr.sources]


# Review wave 2a, S5: founders send their own files. A file with other columns,
# text in a number cell, or a malformed claims.json must never crash the scan.
# The claim kinds that file backs read "not found in that file", and a gap names it.


def _unreadable_gap(result: ScanResult, rel: str):
    return [g for g in result.gaps if rel in g.what and "could not be read" in g.what]


def test_a_hiring_plan_with_other_columns_is_a_gap_not_a_crash(tmp_path):
    room = make_room(tmp_path, ["01_overview/pitch_deck.pdf", "02_financials/financial_model.xlsx"])
    plan = room / "05_team" / "hiring_plan.csv"
    plan.parent.mkdir(parents=True)
    plan.write_text("role,start_month\nSenior Voice Engineer,2026-10\nAccount Executive,2026-11\n", encoding="utf-8")
    result = scan(room, tmp_path / "out")
    assert check_result(result, room)[1] == {}
    gaps = _unreadable_gap(result, "05_team/hiring_plan.csv")
    assert len(gaps) == 1, [g.what for g in result.gaps]
    assert "hire_id" in gaps[0].why or "headcount_after_hire" in gaps[0].why
    # A plan with no department column says nothing about hires by department.
    assert not any("department" in c.text and "hiring plan" in c.text for c in result.claims)


def test_text_in_a_metrics_cell_is_a_gap_not_a_crash(tmp_path):
    room = tmp_path / "bw"
    for rel in ("01_overview/pitch_deck.pdf", "03_metrics/monthly_metrics.csv"):
        (room / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "data_room" / "brasswick" / rel, room / rel)
    metrics = room / "03_metrics" / "monthly_metrics.csv"
    lines = metrics.read_text(encoding="utf-8").splitlines()
    head = lines[0].split(",")
    row = next(i for i, line in enumerate(lines) if line.startswith("2026-09,"))
    cells = lines[row].split(",")
    cells[head.index("total_revenue")] = "n/a"
    lines[row] = ",".join(cells)
    metrics.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = scan(room, tmp_path / "out")
    assert check_result(result, room)[1] == {}
    gaps = _unreadable_gap(result, "03_metrics/monthly_metrics.csv")
    assert len(gaps) == 1, [g.what for g in result.gaps]
    assert "n/a" in gaps[0].why
    # The cells that are numbers still back what they can: paying_brokers is untouched.
    brokers = next(c for c in result.claims if c.sources[0].locator == "slide 5" and c.value and c.value.label == "paying_accounts")
    assert "03_metrics/monthly_metrics.csv" in [s.uri for s in brokers.sources]


def test_a_malformed_claims_json_is_a_gap_not_a_crash(tmp_path):
    room = make_room(tmp_path, ["02_financials/financial_model.xlsx"])
    (room / "01_overview").mkdir(parents=True)
    (room / "01_overview" / "pitch_deck.pdf").write_bytes(b"not a pdf")
    (room / "01_overview" / "claims.json").write_text(json.dumps({"claims": [{"label": "ARR"}, "junk", {"value": 3}]}),
                                                       encoding="utf-8")
    result = scan(room, tmp_path / "out")
    assert result.claims == []
    assert any("claims.json" in g.what and "3 rows" in g.why for g in result.gaps), [(g.what, g.why) for g in result.gaps]
