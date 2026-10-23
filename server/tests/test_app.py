import pytest
from fastapi.testclient import TestClient

from scans.base import ROOT
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


# Review wave 2b, S2: POST /source opens nothing outside its room. -----------------------------------


def _source(uri: str, locator: str = "line 3") -> dict:
    return {"kind": "file", "uri": uri, "locator": locator, "quote": "x"}


@pytest.mark.parametrize("uri", [
    "../../CLAUDE.md",                                   # the repo's own files
    "../answer_key.json",                                # the sealed answer key, next to the rooms
    str(ROOT / "data_room" / "answer_key.json"),         # the same, by absolute path
    str(ROOT / "CLAUDE.md"),                             # an absolute path to the repo
    "/etc/passwd",
    "../hollis_voice_clean/03_metrics/customer_mrr_by_month.csv",  # another room's file
])
def test_source_refuses_any_path_outside_the_room(uri):
    r = client.post("/api/rooms/brasswick/source", json=_source(uri, "row 2"))
    assert r.status_code == 404, r.text
    assert "text" not in r.json()


def test_source_refuses_an_answer_key_even_inside_a_room(tmp_path, monkeypatch):
    room = tmp_path / "rooms" / "sealed_room"
    (room / "01_overview").mkdir(parents=True)
    (room / "01_overview" / "notes.md").write_text("one\ntwo\nthree\n", encoding="utf-8")
    (room / "answer_key.json").write_text('{"flags": ["planted"]}', encoding="utf-8")
    monkeypatch.setenv("TRICORDER_ROOMS_DIR", str(tmp_path / "rooms"))
    assert client.post("/api/rooms/sealed_room/source", json=_source("01_overview/notes.md")).status_code == 200
    r = client.post("/api/rooms/sealed_room/source", json=_source("answer_key.json", "whole"))
    assert r.status_code == 404 and "planted" not in r.text
    assert client.get("/api/rooms/sealed_room/files/answer_key.json").status_code == 404
