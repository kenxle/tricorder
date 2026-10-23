"""The steering routes (STEER-R14), on the real rooms with a temporary out folder and store."""

from __future__ import annotations

import shutil

import pytest
from fastapi.testclient import TestClient

from scans.base import ROOT, write_result
from scans.memo.merge import build_readout, write_readout
from scans.redflags import scan as redflags
from server.app import app

FULL = ROOT / "data_room" / "hollis_voice"
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"
client = TestClient(app)


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("built_out")
    mp = pytest.MonkeyPatch()
    mp.setenv("TRICORDER_OUT_DIR", str(out))
    for room in (FULL, SEED):
        write_result(redflags.run(room), room)
        write_readout(build_readout(room), room)
    mp.undo()
    return out


@pytest.fixture()
def env(tmp_path, built, monkeypatch):
    out = tmp_path / "out"
    shutil.copytree(built, out)
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(out))
    monkeypatch.setenv("TRICORDER_STORE_DIR", str(tmp_path / "store_data"))
    monkeypatch.setenv("TRICORDER_CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return out


def test_steerable_has_nine_pieces_with_verdicts(env):
    r = client.get("/api/rooms/hollis_voice_seed_drop/steerable")
    assert r.status_code == 200
    pieces = {p["name"]: p["verdict"] for p in r.json()["pieces"]}
    assert len(pieces) == 9 and pieces["retention"] == "not_enough_in_the_room" and pieces["traction_and_revenue"] == "looking_weak"


def test_steer_route_runs_the_steer_and_keeps_it(env):
    r = client.post("/api/rooms/hollis_voice/steer", json={"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring"})
    assert r.status_code == 200, r.text
    body = r.json()
    added = body["revision"]["claims_added"]
    assert len(added) == 1
    line = next(c for c in body["readout"]["claims"] if c["id"] == added[0])
    assert line["value"]["number"] == 2060868
    assert body["reading"]["path"] == "rules" and body["store"]["saved"] is True
    assert body["changes"]["name"] == "steer 1: what changed"
    revs = client.get("/api/rooms/hollis_voice/revisions").json()
    assert [x["steer"]["instruction"] for x in revs["revisions"]] == ["treat the pilot as non-recurring"]
    assert revs["changes"][0]["name"] == "steer 1: what changed"
    # The readout the page reads now carries the revision.
    assert len(client.get("/api/rooms/hollis_voice/readout").json()["revisions"]) == 1


def test_more_info_route_names_the_source_room(env):
    body = client.post("/api/rooms/hollis_voice_seed_drop/steer", json={"piece": "retention", "sentence": "read the full room"}).json()
    assert body["source_room"] == "hollis_voice"
    assert body["revision"]["before"]["verdict"] == "not_enough_in_the_room" and body["revision"]["after"]["verdict"] == "looking_weak"


@pytest.mark.parametrize("payload", [
    {"piece": "traction_and_revenue", "sentence": ""},
    {"piece": "nope", "sentence": "read the full room"},
    {"piece": "retention", "sentence": "read the full room", "claim_id": "no-such"},
    {"piece": "retention"},
])
def test_bad_steer_is_422(env, payload):
    assert client.post("/api/rooms/hollis_voice/steer", json=payload).status_code == 422


def test_unknown_room_is_404(env):
    assert client.post("/api/rooms/nope/steer", json={"piece": "retention", "sentence": "x"}).status_code == 404


def test_no_readout_is_404(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "empty"))
    r = client.get("/api/rooms/hollis_voice/steerable")
    assert r.status_code == 404 and "scans.redflags" in r.json()["detail"]
