"""The server answers only its own page on this machine (review wave 2a, S1).

Cross-site requests and DNS rebinding are refused before any route runs, for every router."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from server.app import app

ROOT = Path(__file__).resolve().parents[2]
client = TestClient(app, base_url="http://127.0.0.1:8812")

# One unsafe route from each router that writes: store, founder requests (both uploads), steering, memo.
UNSAFE = [
    "/api/store/demo/brasswick/delete",
    "/api/rooms/brasswick/founder-requests/files?answers=C22&name=plan.csv",
    "/api/rooms/brasswick/founder-requests/batch",
    "/api/rooms/brasswick/steer",
    "/api/rooms/brasswick/memo/edits",
    "/api/rooms/brasswick/memo",
]


@pytest.fixture(autouse=True)
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_ROOMS_DIR", str(tmp_path / "rooms"))
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("TRICORDER_STORE_DIR", str(tmp_path / "store"))
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    return tmp_path


@pytest.mark.parametrize("host", ["evil.example", "attacker.example:8820", "localhost.evil.example", "127.0.0.1.nip.io", ""])
def test_a_foreign_host_is_refused(host):
    r = client.get("/health", headers={"host": host})
    assert r.status_code == 403 and "host" in r.text.lower()


@pytest.mark.parametrize("host", ["127.0.0.1:8812", "localhost:5173", "localhost", "[::1]:8787"])
def test_a_local_host_is_served(host):
    assert client.get("/health", headers={"host": host}).status_code == 200


@pytest.mark.parametrize("path", UNSAFE)
@pytest.mark.parametrize("headers", [
    {"origin": "http://evil.example", "content-type": "application/json"},
    {"origin": "null", "content-type": "application/json"},
    {"origin": "http://localhost.evil.example:8812", "content-type": "application/json"},
    {"referer": "http://evil.example/page", "content-type": "application/json"},
])
def test_a_cross_site_write_is_refused_on_every_router(env, path, headers):
    r = client.post(path, headers=headers, content=b"{}")
    assert r.status_code == 403, r.text
    assert not (env / "rooms").exists() and not (env / "out").exists() and not (env / "store").exists()


@pytest.mark.parametrize("path", UNSAFE)
@pytest.mark.parametrize("ctype", ["text/plain", "text/plain;charset=UTF-8", "application/x-www-form-urlencoded", "text/csv"])
def test_a_simple_form_body_is_refused(env, path, ctype):
    r = client.post(path, headers={"content-type": ctype}, content=b'{"files": []}')
    assert r.status_code == 415, r.text
    assert not (env / "rooms").exists() and not (env / "out").exists()


@pytest.mark.parametrize("origin", [None, "http://127.0.0.1:8812", "http://localhost:5173"])
def test_the_page_and_the_dev_server_get_through(origin):
    headers = {"content-type": "application/json"} | ({"origin": origin} if origin else {})
    r = client.post("/api/rooms/nope/founder-requests/draft", headers=headers, content=b"{}")
    assert r.status_code == 404  # past the guard; the room does not exist
    r = client.post("/api/rooms/nope/readout", headers={"origin": origin} if origin else {})
    assert r.status_code == 404  # a write with no body needs no content type


def test_a_body_without_a_content_type_is_refused():
    r = client.post("/api/rooms/nope/founder-requests/draft", content=b"{}", headers={"content-type": ""})
    assert r.status_code == 415
