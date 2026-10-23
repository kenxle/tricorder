"""The founder-requests endpoints, through the real app."""

import base64
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from founder_requests.tests.conftest import ready_scans
from server.app import app

ROOT = Path(__file__).resolve().parents[2]
PLAN = (ROOT / "founder_requests" / "tests" / "fixtures" / "synthetic_brasswick_hiring_plan.csv").read_bytes()
client = TestClient(app)


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_ROOMS_DIR", str(tmp_path / "rooms"))
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    return tmp_path


def _build(room):
    for name in ready_scans(room) + ["memo"]:
        subprocess.run([sys.executable, "-m", f"scans.{name}", str(room)], cwd=ROOT, check=True, capture_output=True)


def test_lines_and_draft(env):
    assert client.get("/api/rooms/brasswick/founder-requests").status_code == 404  # no readout yet
    _build(ROOT / "data_room" / "brasswick")
    r = client.get("/api/rooms/brasswick/founder-requests").json()
    assert r["synthetic"] is True and r["copy_command"] == "python -m founder_requests copy-room data_room/brasswick"
    assert len(r["items"]) >= 20 and len(r["default"]) == 5
    d = client.post("/api/rooms/brasswick/founder-requests/draft", json={"to": "celia@example.com"}).json()
    assert d["body"].startswith("Hi Celia,") and d["mailto"].startswith("mailto:celia@example.com?") and d["leaks"] == []
    one = client.post("/api/rooms/brasswick/founder-requests/draft", json={"numbers": [r["default"][0]]}).json()
    assert one["subject"] == "Brasswick: one thing before our next meeting"
    signed = client.post("/api/rooms/brasswick/founder-requests/draft",
                         json={"by": "2026-11-06", "sender": "Sam Ortiz", "fund": "Example Ventures"}).json()
    assert "by Friday 6 November" in signed["body"] and signed["body"].rstrip().endswith("Thanks,\nSam Ortiz\nExample Ventures")
    assert signed["mailto_fits"] is True
    assert r["by"] and r["reason"] == "before our partner meeting" and "held" in r
    assert all("C1" not in i["operator_why"] for i in r["items"])
    assert client.post("/api/rooms/brasswick/founder-requests/draft", json={"numbers": [999]}).status_code == 422
    assert client.post("/api/rooms/nope/founder-requests/draft", json={}).status_code == 404


def test_upload_to_a_synthetic_room_is_refused(env):
    before = sorted(p.name for p in (ROOT / "data_room" / "brasswick").rglob("*"))
    r = client.post("/api/rooms/brasswick/founder-requests/files?answers=C22&name=plan.csv", content=PLAN)
    assert r.status_code == 409 and "copy-room" in r.json()["detail"]
    assert sorted(p.name for p in (ROOT / "data_room" / "brasswick").rglob("*")) == before


def test_copy_then_upload_reruns_and_rebuilds(env):
    r = client.post("/api/rooms/brasswick/founder-requests/copy", json={})
    assert r.status_code == 200 and r.json()["room"] == "brasswick_live"
    assert client.post("/api/rooms/brasswick/founder-requests/copy", json={}).status_code == 409
    _build(env / "rooms" / "brasswick_live")
    r = client.post("/api/rooms/brasswick_live/founder-requests/files?answers=C22&name=Brasswick%20Hiring%20Plan.csv",
                    content=PLAN)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["saved"] == "05_team/hiring_plan.csv" and body["status_before"] == "missing"
    assert body["status_after"] == "found" and body["asks_after"] == body["asks_before"] - 1
    assert [s["scan"] for s in body["scans_rerun"]] == ready_scans(env / "rooms" / "brasswick_live")
    assert all(s["ok"] for s in body["scans_rerun"])
    assert not any("redflags" in line or "Scans that were waiting" in line for line in body["summary"])
    log = client.get("/api/rooms/brasswick_live/founder-requests/received").json()
    assert log["received"][-1]["saved"] == "05_team/hiring_plan.csv"


@pytest.mark.parametrize("query, content, status", [
    ("answers=C22&name=..%2F..%2Fescape.exe", PLAN, 415),
    ("answers=C22&name=.env", PLAN, 400),
    ("answers=C22&name=plan.pdf", PLAN, 415),
    ("answers=C24&name=plan.csv", PLAN, 422),
    ("name=plan.csv", PLAN, 422),
    ("answers=C22&name=plan.csv", b"", 400),
])
def test_bad_uploads_are_refused(env, query, content, status):
    client.post("/api/rooms/brasswick/founder-requests/copy", json={})
    r = client.post(f"/api/rooms/brasswick_live/founder-requests/files?{query}", content=content)
    assert r.status_code == status, r.text
    assert not (env / "rooms" / "brasswick_live" / "05_team" / "hiring_plan.csv").exists()


def test_size_limit_is_checked_before_the_body_is_kept(env, monkeypatch):
    client.post("/api/rooms/brasswick/founder-requests/copy", json={})
    monkeypatch.setenv("TRICORDER_UPLOAD_MAX_MB", "0.0001")
    r = client.post("/api/rooms/brasswick_live/founder-requests/files?answers=C22&name=plan.csv", content=PLAN)
    assert r.status_code == 413


def test_room_ids_are_checked(env):
    assert client.get("/api/rooms/..%2F..%2Fetc/founder-requests").status_code == 404
    # An encoded slash makes the path miss the route: 404, or 405 when the built page is mounted at /.
    r = client.post("/api/rooms/x%2F..%2Fbrasswick/founder-requests/files?answers=C22&name=p.csv", content=PLAN)
    assert r.status_code in (404, 405)
    assert not (env / "rooms").exists() or not any((env / "rooms").rglob("p.csv"))


def test_several_files_in_one_add(env):
    client.post("/api/rooms/brasswick/founder-requests/copy", json={})
    _build(env / "rooms" / "brasswick_live")
    files = [{"name": "Hiring Plan.csv", "answers": "C22", "data": base64.b64encode(PLAN).decode()},
             {"name": "refs.pdf", "answers": "C97,C46", "data": base64.b64encode(b"%PDF-1.4\n%x\n").decode()}]
    r = client.post("/api/rooms/brasswick_live/founder-requests/batch", json={"files": files})
    assert r.status_code == 200, r.text
    body = r.json()
    assert [f["saved"] for f in body["files"]] == ["05_team/hiring_plan.csv", "05_team/reference_list_refs.pdf"]
    assert body["summary"][0] == "Coverage now finds Hiring plan and future org."
    bad = client.post("/api/rooms/brasswick_live/founder-requests/batch",
                      json={"files": [{"name": "x.csv", "answers": "C35", "data": "not base64!"}]})
    assert bad.status_code == 400
    assert client.post("/api/rooms/brasswick/founder-requests/batch", json={"files": files}).status_code == 409
