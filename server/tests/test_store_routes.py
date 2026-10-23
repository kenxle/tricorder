"""The store's routes, for the page to list and delete (STORE-R8, R14)."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient

from scans.base import ROOT
from server.app import app

ROOM = ROOT / "data_room" / "hollis_voice"
client = TestClient(app)


@pytest.fixture(scope="module")
def built_out(tmp_path_factory):
    out = tmp_path_factory.mktemp("out")
    env = {**__import__("os").environ, "TRICORDER_OUT_DIR": str(out)}
    for module in ("scans.redflags", "scans.memo"):
        subprocess.run([sys.executable, "-m", module, str(ROOM)], cwd=ROOT, env=env, check=True, capture_output=True)
    return out


@pytest.fixture()
def env(tmp_path, built_out, monkeypatch):
    cache = tmp_path / "cache"
    page = cache / "outside" / "hollis_voice" / "website" / "home.html"
    page.parent.mkdir(parents=True)
    page.write_text("<p>Simulated saved page.</p>", encoding="utf-8")
    (cache / "index.json").write_text(json.dumps({"https://hollisvoice.example.com/": {"file": "outside/hollis_voice/website/home.html"}}), encoding="utf-8")
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(built_out))
    monkeypatch.setenv("TRICORDER_STORE_DIR", str(tmp_path / "store_data"))
    monkeypatch.setenv("TRICORDER_CACHE_DIR", str(cache))
    return tmp_path


def test_save_list_get_and_delete_through_the_routes(env):
    r = client.post("/api/store/demo/hollis_voice/save", json={"room": "hollis_voice"})
    assert r.status_code == 200, r.text
    assert r.json()["version"] == 1 and r.json()["new"]

    assert client.get("/api/store/demo").json() == {"fund": "demo", "companies": ["hollis_voice"]}
    held = client.get("/api/store/demo/hollis_voice").json()
    assert [v["version"] for v in held["versions"]] == [1] and held["cache"] == ["outside/hollis_voice/website/home.html"]
    assert [v["version"] for v in client.get("/api/store/demo/hollis_voice/versions").json()] == [1]

    got = client.get("/api/store/demo/hollis_voice/readout").json()
    assert got["readout"]["room"] == "hollis_voice" and got["results"][0]["scan"] == "redflags"
    assert client.get("/api/store/demo/hollis_voice/readout?version=1").status_code == 200
    assert client.get("/api/store/demo/hollis_voice/readout?version=7").status_code == 404

    f = client.get("/api/store/demo/hollis_voice/files/02_financials/expense_ledger.csv")
    assert f.status_code == 200 and f.content == (ROOM / "02_financials/expense_ledger.csv").read_bytes()

    assert client.post("/api/store/demo/hollis_voice/delete", json={}).status_code == 422
    assert client.post("/api/store/demo/hollis_voice/delete", json={"confirm": "other"}).status_code == 400
    assert client.get("/api/store/demo/hollis_voice").json()["versions"] != []

    r = client.post("/api/store/demo/hollis_voice/delete", json={"confirm": "hollis_voice"})
    assert r.status_code == 200 and r.json()["left"] == []
    after = client.get("/api/store/demo/hollis_voice").json()
    assert after["versions"] == [] and after["files"] == [] and after["cache"] == []
    assert not (env / "store_data" / "demo" / "hollis_voice").exists()
    assert not (env / "cache" / "outside" / "hollis_voice").exists()


def test_bad_ids_and_paths_are_refused(env):
    client.post("/api/store/demo/hollis_voice/save", json={"room": "hollis_voice"})
    assert client.get("/api/store/Demo").status_code == 422
    assert client.get("/api/store/demo/..%2Fetc").status_code in (404, 422)
    assert client.get("/api/store/demo/a.b").status_code == 422
    assert client.post("/api/store/demo/x.y/delete", json={"confirm": "x.y"}).status_code == 422
    assert client.get("/api/store/demo/hollis_voice/files/../version.json").status_code == 404
    assert client.get("/api/store/demo/hollis_voice/files/..%2F..%2Fversions%2F0001%2Freadout.json").status_code == 404
    assert client.get("/api/store/demo/hollis_voice/files/answer_key.json").status_code == 404


def test_save_of_an_unknown_room_or_a_room_with_no_readout_is_404(env, tmp_path, monkeypatch):
    assert client.post("/api/store/demo/hollis_voice/save", json={"room": "nope"}).status_code == 404
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "empty_out"))
    r = client.post("/api/store/demo/hollis_voice/save", json={"room": "hollis_voice"})
    assert r.status_code == 404 and "python -m scans.memo" in r.json()["detail"]


def test_unknown_company_is_404(env):
    assert client.get("/api/store/demo/nobody/readout").status_code == 404
    assert client.get("/api/store/demo/nobody/files/x.csv").status_code == 404
