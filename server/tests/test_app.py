from fastapi.testclient import TestClient

from server.app import app

client = TestClient(app, base_url="http://127.0.0.1")  # the local guard refuses any other host


def test_health_answers():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["ok"] is True


def test_rooms_lists_the_synthetic_rooms():
    ids = {r["id"] for r in client.get("/api/rooms").json()}
    assert {"hollis_voice", "hollis_voice_seed_drop", "brasswick"} <= ids


def test_a_room_file_is_served_and_nothing_outside_it():
    assert client.get("/api/rooms/hollis_voice/files/01_overview/claims.json").status_code == 200
    assert client.get("/api/rooms/hollis_voice/files/../answer_key.json").status_code == 404
    assert client.get("/api/rooms/hollis_voice/files/..%2Fanswer_key.json").status_code == 404
    assert client.get("/api/rooms/..%2F..%2Fetc/files/passwd").status_code == 404


def test_an_unknown_room_or_scan_is_a_404():
    assert client.get("/api/rooms/nope/readout").status_code == 404
    assert client.post("/api/rooms/hollis_voice/scans/nope").status_code == 404


def test_source_text_reads_at_the_locator():
    body = {"kind": "file", "uri": "02_financials/financial_model.xlsx", "locator": "ARR_TOTAL", "quote": "2240868"}
    assert client.post("/api/rooms/hollis_voice/source", json=body).json()["text"] == "2240868"


def test_running_a_scan_and_building_a_readout(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    r = client.post("/api/rooms/hollis_voice_seed_drop/scans/redflags")
    assert r.status_code == 200 and r.json()["scan"] == "redflags"
    r = client.post("/api/rooms/hollis_voice_seed_drop/readout")
    assert r.status_code == 200 and "redflags" in r.json()["scans_run"]
