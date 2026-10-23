"""The founder-requests endpoints, through the real app."""

import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

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
    for mod in ("scans.redflags", "scans.memo"):
        subprocess.run([sys.executable, "-m", mod, str(room)], cwd=ROOT, check=True, capture_output=True)


def test_lines_and_draft(env):
    assert client.get("/api/rooms/brasswick/founder-requests").status_code == 404  # no readout yet
    _build(ROOT / "data_room" / "brasswick")
    r = client.get("/api/rooms/brasswick/founder-requests").json()
    assert r["synthetic"] is True and r["copy_command"] == "python -m founder_requests copy-room data_room/brasswick"
    assert len(r["items"]) >= 20 and len(r["default"]) == 5
    d = client.post("/api/rooms/brasswick/founder-requests/draft", json={"to": "celia@example.com"}).json()
    assert d["body"].startswith("Hi Celia,") and d["mailto"].startswith("mailto:celia@example.com?") and d["leaks"] == []
    one = client.post("/api/rooms/brasswick/founder-requests/draft", json={"numbers": [r["default"][0]]}).json()
    assert one["subject"] == "Brasswick: one document for our review"
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
    assert [s["scan"] for s in body["scans_rerun"]] == ["redflags"]
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
    assert client.post("/api/rooms/x%2F..%2Fbrasswick/founder-requests/files?answers=C22&name=p.csv", content=PLAN).status_code == 404
