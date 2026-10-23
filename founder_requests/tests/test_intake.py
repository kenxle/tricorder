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
from founder_requests.tests.conftest import build, ready_scans
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


def test_a_name_beside_an_earlier_file_stays_within_80_characters(env):
    room = ik.copy_room(BRASSWICK)
    ik.save(room, Path("05_team/hiring_plan.csv"), PLAN)
    row = next(r for r in cl.load() if r.id == "C22")
    stem, ext = ik.check_name("x" * 300 + ".csv")
    rel = ik.target_for(room, row, stem, ext)
    assert len(rel.stem) <= ik.STEM_MAX and rel.stem.startswith("hiring_plan_from_founder_")  # FR-R17 (O6)


def test_a_room_copy_never_follows_a_link(env, tmp_path):
    secret = tmp_path / "secret.txt"
    secret.write_text("outside the room")
    src = tmp_path / "src_room"
    import shutil
    shutil.copytree(BRASSWICK, src)
    os.symlink(secret, src / "05_team" / "link.txt")
    with pytest.raises(ik.IntakeError) as err:
        ik.copy_room(src, "linked_copy")
    assert err.value.status == 400 and "link" in err.value.message
    assert not (env[0] / "linked_copy").exists()  # O7


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
    ready = ready_scans(room)
    assert "redflags" in ready
    assert ik.waiting_scans(room) == ready  # never run
    build(room, out)
    assert ik.waiting_scans(room) == []  # ran on everything the room holds
    ik.save(room, Path("05_team/hiring_plan.csv"), PLAN)
    assert ik.waiting_scans(room) == ready  # a new input none of them has seen


def test_hiring_plan_reply_reruns_and_rebuilds(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    before = build(room, out)
    receipt = ik.receive(room, PLAN, "Brasswick Hiring Plan.csv", "C22")
    assert receipt["saved"] == "05_team/hiring_plan.csv"
    assert (room / receipt["saved"]).read_bytes() == PLAN
    assert [s["scan"] for s in receipt["scans_rerun"]] == ready_scans(room)
    assert all(s["ok"] for s in receipt["scans_rerun"]), receipt["scans_rerun"]
    assert receipt["status_before"] == "missing" and receipt["status_after"] == "found"
    assert receipt["asks_before"] == len(before.asks) and receipt["asks_after"] == len(before.asks) - 1
    for name in ready_scans(room):
        result = json.loads((out / room.name / f"{name}.json").read_text())
        assert "05_team/hiring_plan.csv" in result["inputs"], name
    assert ik.waiting_scans(room) == []  # nothing left waiting after the rerun
    readout = json.loads((out / room.name / "readout.json").read_text())
    assert not any(a["checklist_id"] == "C22" for a in readout["asks"])
    log = json.loads((out / room.name / "founder_requests.json").read_text())
    entry = log["received"][-1]
    assert entry["scans_rerun"] == receipt["scans_rerun"] and entry["scans_rerun"]  # FR-R15
    assert entry["original_name"] == "Brasswick Hiring Plan.csv" and entry["checklist_id"] == "C22"
    assert entry["bytes"] == len(PLAN) and entry["at"]


def test_a_reply_before_any_readout_builds_one(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    receipt = ik.receive(room, PLAN, "plan.csv", "C22")
    assert receipt["status_before"] == "unknown" and receipt["asks_before"] is None
    assert receipt["status_after"] == "found"
    assert (out / room.name / "readout.json").exists()


# One file for several lines, several files in one add, and a receipt in plain words (FR-R27, FR-R28) --


def test_one_file_can_answer_several_requests(brasswick):
    rows = ik.resolve_requests("C97, C46,C97", None)
    assert [r.id for r in rows] == ["C97", "C46"]
    n = next(i for i, a in enumerate(brasswick.asks, start=1) if a.checklist_id == "C22")
    assert [r.id for r in ik.resolve_requests(f"{n},C97", brasswick)] == ["C22", "C97"]
    with pytest.raises(ik.IntakeError) as err:
        ik.resolve_requests("C22,C24", None)
    assert err.value.status == 422


def _claim(cid, text, scan="redflags"):
    from schema.claim import Check, Claim, Source
    return Claim(id=cid, scan=scan, text=text, check=Check(kind="script", name="x"), confidence="computed",
                 sources=[Source(kind="file", uri="05_team/hiring_plan.csv", locator="row 2", quote="q")])


def test_changes_are_said_in_plain_words(brasswick):
    from schema.claim import TopFlag
    same = ik.changes(brasswick, brasswick.model_copy(deep=True), [])
    assert same == ["No check reads this file yet, so no number changed."]
    assert ik.changes(brasswick, brasswick.model_copy(deep=True), [], files=2) == [
        "No check reads these files yet, so no number changed."]
    after = brasswick.model_copy(deep=True)
    after.claims.append(_claim("redflags-900", "Hiring plan adds 6 engineers before the round closes."))
    after.top_flags.append(TopFlag(kind="red", piece="burn_and_runway", rank=9, text="Runway falls under 12 months.",
                                   claim_ids=["redflags-900"]))
    from schema.claim import Piece
    before = brasswick.model_copy(deep=True)
    before.pieces = [Piece(name="burn_and_runway", verdict="mixed", reason="r")]
    after.pieces = [Piece(name="burn_and_runway", verdict="looking_weak", reason="r")]
    old = before.claims[0]
    after.claims = [c.model_copy(update={"text": "Contradicted: the plan says 5."}) if c.id == old.id else c
                    for c in after.claims]
    said = " ".join(ik.changes(before, after, []))
    assert "1 claim changed. Now: Contradicted: the plan says 5." in said
    assert "no longer in the readout" not in said
    assert "1 new claim: Hiring plan adds 6 engineers before the round closes." in said
    assert "New red flag: Runway falls under 12 months." in said
    assert "Burn and runway moved from mixed to looking weak." in said and "No check reads" not in said
    assert "redflags" not in said and "Scans that were waiting" not in said


def test_hiring_plan_receipt_says_what_changed(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    before = build(room, out)
    receipt = ik.receive(room, PLAN, "Brasswick Hiring Plan.csv", "C22")
    after = ik._readout(room)
    assert receipt["summary"][0] == "Coverage now finds Hiring plan and future org."
    said = " ".join(receipt["summary"])
    moved = ({(c.id, c.text) for c in before.claims} != {(c.id, c.text) for c in after.claims}
             or before.top_flags != after.top_flags or [p.verdict for p in before.pieces] != [p.verdict for p in after.pieces])
    assert ("No check reads this file yet, so no number changed." in said) == (not moved)
    changed = [c.text for c in after.claims if c.id in {b.id for b in before.claims} and c.text not in {b.text for b in before.claims}]
    for text in changed[:3]:
        assert text in said  # a relabelled claim is said in its new words
    assert any(s.startswith("The ask list is down from") for s in receipt["summary"])
    assert "redflags" not in said and "Scans that were waiting" not in said


def test_several_files_in_one_add_rerun_once(env, monkeypatch):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    build(room, out)
    calls = []
    real = ik.run_scans
    monkeypatch.setattr(ik, "run_scans", lambda r, names: calls.append(names) or real(r, names))
    receipt = ik.receive_batch(room, [(PLAN, "Hiring Plan.csv", "C22"), (PDF, "Our references.pdf", "C97,C46")])
    assert len(calls) == 1
    files = receipt["files"]
    assert [f["saved"] for f in files] == ["05_team/hiring_plan.csv", "05_team/reference_list_our_references.pdf"]
    assert [a["checklist_id"] for a in files[1]["answers"]] == ["C97", "C46"]
    assert files[0]["answers"][0]["status_after"] == "found"
    assert "Coverage now finds Reference list: management, customers, current investors, advisors." in receipt["summary"]
    assert ("Customer reference calls is something only the founder can give, so no check reads the file. "
            "The line stays on the ask list.") in receipt["summary"]
    log = json.loads((out / room.name / "founder_requests.json").read_text())
    assert [e["original_name"] for e in log["received"][-2:]] == ["Hiring Plan.csv", "Our references.pdf"]


def test_a_batch_with_one_bad_file_writes_nothing(env):
    room = ik.copy_room(BRASSWICK)
    before = _snapshot(room)
    with pytest.raises(ik.IntakeError) as err:
        ik.receive_batch(room, [(PLAN, "plan.csv", "C22"), (b"MZ\x90", "refs.pdf", "C97")])
    assert err.value.status == 415 and "refs.pdf" in err.value.message
    with pytest.raises(ik.IntakeError):
        ik.receive_batch(room, [])
    assert _snapshot(room) == before


def test_a_file_a_scan_left_out_on_purpose_does_not_keep_it_waiting(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    build(room, out)
    result = out / room.name / "redflags.json"
    data = json.loads(result.read_text())
    left_out = data["inputs"].pop()
    result.write_text(json.dumps(data))
    assert "redflags" not in ik.waiting_scans(room)  # older than the run: read or skipped then
    os.utime(room / left_out)
    assert "redflags" in ik.waiting_scans(room)  # changed since the run


def test_a_scan_that_fails_on_the_new_file_is_said_plainly(env, monkeypatch):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    build(room, out)
    monkeypatch.setattr(ik, "run_scans", lambda r, names: [{"scan": n, "ok": n != "redflags", "error": "boom"} for n in names])
    receipt = ik.receive(room, PLAN, "plan.csv", "C22")
    assert receipt["summary"][0] == "One check could not read the new file, so its part of the readout is from before."
    assert not any("no number changed" in s for s in receipt["summary"])  # a crash is not "nothing changed" (S3)
    assert not any("redflags" in s or "boom" in s for s in receipt["summary"])
    log = json.loads((out / room.name / "founder_requests.json").read_text())
    assert log["received"][-1]["scans_rerun"] == receipt["scans_rerun"]  # FR-R15 (S4)


def test_a_gap_about_the_new_file_counts_as_not_read(brasswick):
    from schema.claim import Gap
    after = brasswick.model_copy(deep=True)
    after.gaps.append(Gap(what="Not in the room: a readable hiring plan", why="05_team/hiring_plan.csv has no hire_id column",
                          would_need="the hiring plan with one row per hire"))
    said = ik.changes(brasswick, after, [], saved=["05_team/hiring_plan.csv"])
    assert said[0] == "One check could not read the new file, so its part of the readout is from before."
    assert not any("no number changed" in s for s in said)
    assert ik.changes(brasswick, after, [], saved=["06_legal/other.pdf"]) == [
        "No check reads this file yet, so no number changed."]


def test_a_plan_in_the_founders_own_columns_still_lands(env):
    _, out = env
    room = ik.copy_room(BRASSWICK)
    build(room, out)
    own = (Path(__file__).parent / "fixtures" / "synthetic_brasswick_hiring_plan_own_columns.csv").read_bytes()
    receipt = ik.receive(room, own, "Hiring Plan.csv", "C22")
    assert receipt["saved"] == "05_team/hiring_plan.csv" and receipt["status_after"] == "found"
    assert "Coverage now finds Hiring plan and future org." in receipt["summary"]
    failed = sum(not s["ok"] for s in receipt["scans_rerun"])
    if failed:
        assert receipt["summary"][0].endswith("could not read the new file, so its part of the readout is from before.")
        assert not any("no number changed" in s for s in receipt["summary"])
    said = " ".join(receipt["summary"])
    assert ("could not read the new file" in said) == bool(failed)
    assert not any(s["scan"] in said for s in receipt["scans_rerun"])


def test_the_same_sentence_is_said_once(brasswick):
    after = brasswick.model_copy(deep=True)
    after.claims += [_claim("redflags-901", "Plan says 5."), _claim("redflags-902", "Plan says 5.")]
    said = ik.changes(brasswick, after, [])
    assert "2 new claims: Plan says 5." in said


def test_a_room_with_no_readout_before_says_so_instead_of_listing_every_claim(brasswick):
    said = ik.changes(None, brasswick, [])
    assert said == [f"This room had no readout before, so this is its first: {len(brasswick.claims)} claims."]
