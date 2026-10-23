"""Adding a founder's file to a room (FR-R11 to FR-R20). Rooms are copied into a temporary
TRICORDER_ROOMS_DIR; data_room/ is never written."""

from __future__ import annotations

import io
import json
import os
import zipfile
from pathlib import Path

import pytest

from founder_requests import intake as ik
from founder_requests.tests.conftest import build
from scans.memo import checklist as cl

ROOT = Path(__file__).resolve().parents[2]
BRASSWICK = ROOT / "data_room" / "brasswick"
PLAN = (Path(__file__).parent / "fixtures" / "synthetic_brasswick_hiring_plan.csv").read_bytes()
PDF = b"%PDF-1.4\n%synthetic test\n"


@pytest.fixture
def env(tmp_path, monkeypatch):
    rooms, out = tmp_path / "rooms", tmp_path / "out"
    monkeypatch.setenv("TRICORDER_ROOMS_DIR", str(rooms))
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(out))
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    return rooms, out


def _snapshot(folder: Path) -> dict:
    return {str(p.relative_to(folder)): p.stat().st_mtime_ns for p in folder.rglob("*")}


# Names --------------------------------------------------------------------------------------


@pytest.mark.parametrize("name, want", [
    ("Hiring Plan.csv", ("hiring_plan", ".csv")),
    ("../../etc/passwd.csv", ("passwd", ".csv")),
    ("C:\\Users\\celia\\Hiring Plan (v2).CSV", ("hiring_plan_v2", ".csv")),
    ("409A report 2026.pdf", ("409a_report_2026", ".pdf")),
    ("Ünïcode naïve.md", ("unicode_naive", ".md")),
    ("%%%.csv", ("file", ".csv")),
])
def test_names_are_reduced_to_a_safe_stem(name, want):
    assert ik.check_name(name) == want


def test_long_names_are_cut():
    stem, ext = ik.check_name("a" * 300 + ".pdf")
    assert len(stem) == 80 and ext == ".pdf"


@pytest.mark.parametrize("name", ["", ".env", "..", "dir/", "plan", "plan.exe", "plan.csv.sh", "a\x00b.csv",
                                  "line\nbreak.csv", ".hidden.csv"])
def test_bad_names_are_refused(name):
    with pytest.raises(ik.IntakeError) as err:
        ik.check_name(name)
    assert err.value.status in (400, 415)


# Bytes --------------------------------------------------------------------------------------


def _zip(entries: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for k, v in entries.items():
            z.writestr(k, v)
    return buf.getvalue()


def test_kinds_must_match_their_bytes():
    ik.check_bytes(PDF, ".pdf")
    ik.check_bytes(PLAN, ".csv")
    ik.check_bytes(b'{"a": 1}', ".json")
    ik.check_bytes(_zip({"[Content_Types].xml": b"<x/>", "xl/workbook.xml": b"<w/>"}), ".xlsx")
    ik.check_bytes(b"\x89PNG\r\n\x1a\nrest", ".png")
    for data, ext in [(b"not a pdf", ".pdf"), (b"a,b\x00,c", ".csv"), (b"\xff\xfe\xfa", ".csv"), (b"{nope", ".json"),
                      (b"PK not really", ".xlsx"), (_zip({"a.txt": b"x"}), ".xlsx"), (b"GIF89a", ".png"),
                      (PDF, ".csv")]:
        with pytest.raises(ik.IntakeError) as err:
            ik.check_bytes(data, ext)
        assert err.value.status == 415, (data[:10], ext)


def test_a_zip_that_unpacks_too_large_is_refused():
    bomb = _zip({"[Content_Types].xml": b"<x/>", "xl/big.xml": b"0" * 50_000})
    with pytest.raises(ik.IntakeError) as err:
        ik.check_bytes(bomb, ".xlsx", max_unpacked=10_000)
    assert err.value.status == 413


# Rooms --------------------------------------------------------------------------------------


def test_a_synthetic_room_is_never_written(env):
    before = _snapshot(BRASSWICK)
    with pytest.raises(ik.IntakeError) as err:
        ik.receive(BRASSWICK, PLAN, "hiring_plan.csv", "C22")
    assert err.value.status == 409 and "python -m founder_requests copy-room data_room/brasswick" in err.value.message
    assert _snapshot(BRASSWICK) == before


def test_copy_room_makes_a_working_copy_and_never_overwrites(env):
    rooms, _ = env
    dest = ik.copy_room(BRASSWICK)
    assert dest == rooms / "brasswick_live"
    assert (dest / "05_team" / "founder_bios.pdf").exists()
    with pytest.raises(ik.IntakeError) as err:
        ik.copy_room(BRASSWICK)
    assert err.value.status == 409
    with pytest.raises(ik.IntakeError):
        ik.copy_room(BRASSWICK, "hollis_voice")  # a data_room name would be shadowed
    with pytest.raises(ik.IntakeError):
        ik.copy_room(BRASSWICK, "../escape")
    assert not (rooms.parent / "escape").exists()


def test_a_room_outside_the_rooms_folder_is_refused(env, tmp_path):
    stray = tmp_path / "elsewhere" / "room"
    (stray / "01_overview").mkdir(parents=True)
    with pytest.raises(ik.IntakeError) as err:
        ik.receive(stray, PLAN, "hiring_plan.csv", "C22")
    assert err.value.status == 409


# Where a file lands -------------------------------------------------------------------------


def test_folders_and_names_on_brasswick(env):
    room = ik.copy_room(BRASSWICK)
    rows = {r.id: r for r in cl.load()}
    assert ik.target_for(room, rows["C22"], "brasswick_hiring_plan", ".csv") == Path("05_team/hiring_plan.csv")
    assert ik.target_for(room, rows["C34"], "acme_signed", ".pdf") == Path("04_contracts/order_form_acme_signed.pdf")
    # Brasswick already holds monthly_metrics.csv: a new copy goes beside it, never over it.
    assert ik.target_for(room, rows["C02"], "kpis", ".csv") == Path("03_metrics/monthly_metrics_from_founder_kpis.csv")
    assert ik.target_for(room, rows["C73"], "report", ".pdf") == Path("06_legal/409a_report.pdf")
    assert ik.target_for(room, rows["C61"], "one_pager", ".pdf").parent == Path("01_overview")


def test_every_document_row_is_found_by_coverage_after_it_lands(tmp_path):
    room = tmp_path / "room"
    for d in ("00_welcome", "01_overview", "02_financials", "03_metrics", "04_contracts", "05_team"):
        (room / d).mkdir(parents=True)
    for r in cl.load():
        if r.kind != "document" or r.id not in cl.DOC_PATTERNS:
            continue
        rel = ik.target_for(room, r, "reply_from_founder", ".pdf")
        assert rel.parts[0][:3].rstrip("_").isdigit(), (r.id, rel)
        assert cl.match_document(r, [str(rel)]), (r.id, rel)


def test_check_rows_and_unknown_requests_are_refused():
    for bad in ("C24", "C999", "hiring", "", None):
        with pytest.raises(ik.IntakeError) as err:
            ik.resolve_request(bad, None)
        assert err.value.status == 422


def test_an_ask_number_resolves_through_the_readout(brasswick):
    n = next(i for i, a in enumerate(brasswick.asks, start=1) if a.checklist_id == "C22")
    assert ik.resolve_request(str(n), brasswick).id == "C22"
    with pytest.raises(ik.IntakeError):
        ik.resolve_request("999", brasswick)


def test_no_overwrite_and_no_links(env, tmp_path):
    room = ik.copy_room(BRASSWICK)
    ik.save(room, Path("05_team/hiring_plan.csv"), PLAN)
    with pytest.raises(ik.IntakeError) as err:
        ik.save(room, Path("05_team/hiring_plan.csv"), b"other")
    assert err.value.status == 409
    assert (room / "05_team/hiring_plan.csv").read_bytes() == PLAN
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(outside, room / "07_linked")
    with pytest.raises(ik.IntakeError):
        ik.save(room, Path("07_linked/x.csv"), PLAN)
    os.symlink(outside / "target.csv", room / "03_metrics" / "trap.csv")
    with pytest.raises(ik.IntakeError):
        ik.save(room, Path("03_metrics/trap.csv"), PLAN)
    assert list(outside.iterdir()) == []
    with pytest.raises(ik.IntakeError):
        ik.save(room, Path("../escape.csv"), PLAN)


def test_size_limits(env, monkeypatch):
    room = ik.copy_room(BRASSWICK)
    monkeypatch.setenv("TRICORDER_UPLOAD_MAX_MB", "0.0001")
    with pytest.raises(ik.IntakeError) as err:
        ik.receive(room, PLAN, "hiring_plan.csv", "C22")
    assert err.value.status == 413
    monkeypatch.delenv("TRICORDER_UPLOAD_MAX_MB")
    with pytest.raises(ik.IntakeError) as err:
        ik.receive(room, b"", "hiring_plan.csv", "C22")
    assert err.value.status == 400
    assert not (room / "05_team" / "hiring_plan.csv").exists()


# Waiting scans and the rebuild --------------------------------------------------------------


def test_waiting_scans_follow_needs_and_inputs(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    assert ik.waiting_scans(room) == ["redflags"]  # never run
    build(room, out)
    assert ik.waiting_scans(room) == []  # ran on everything the room holds
    ik.save(room, Path("05_team/hiring_plan.csv"), PLAN)
    assert ik.waiting_scans(room) == ["redflags"]  # a new input it has not seen


def test_hiring_plan_reply_reruns_and_rebuilds(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    before = build(room, out)
    receipt = ik.receive(room, PLAN, "Brasswick Hiring Plan.csv", "C22")
    assert receipt["saved"] == "05_team/hiring_plan.csv"
    assert (room / receipt["saved"]).read_bytes() == PLAN
    assert [s["scan"] for s in receipt["scans_rerun"]] == ["redflags"] and receipt["scans_rerun"][0]["ok"]
    assert receipt["status_before"] == "missing" and receipt["status_after"] == "found"
    assert receipt["asks_before"] == len(before.asks) and receipt["asks_after"] == len(before.asks) - 1
    redflags = json.loads((out / room.name / "redflags.json").read_text())
    assert "05_team/hiring_plan.csv" in redflags["inputs"]
    readout = json.loads((out / room.name / "readout.json").read_text())
    assert not any(a["checklist_id"] == "C22" for a in readout["asks"])
    log = json.loads((out / room.name / "founder_requests.json").read_text())
    entry = log["received"][-1]
    assert entry["original_name"] == "Brasswick Hiring Plan.csv" and entry["checklist_id"] == "C22"
    assert entry["bytes"] == len(PLAN) and entry["at"]


def test_a_reply_before_any_readout_builds_one(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    receipt = ik.receive(room, PLAN, "plan.csv", "C22")
    assert receipt["status_before"] == "unknown" and receipt["asks_before"] is None
    assert receipt["status_after"] == "found"
    assert (out / room.name / "readout.json").exists()
