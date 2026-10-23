"""The steering routes (STEER-R14), on the real rooms with a temporary out folder and store."""

from __future__ import annotations

import importlib
import shutil

import pytest
from fastapi.testclient import TestClient

from scans.base import ROOT, available, write_result
from scans.memo.merge import build_readout, write_readout
from server.app import app

FULL = ROOT / "data_room" / "hollis_voice"
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"
client = TestClient(app, base_url="http://127.0.0.1")  # the local guard refuses any other host


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("built_out")
    mp = pytest.MonkeyPatch()
    mp.setenv("TRICORDER_OUT_DIR", str(out))
    mp.setenv("TRICORDER_OFFLINE", "1")
    mp.delenv("ANTHROPIC_API_KEY", raising=False)
    for room in (FULL, SEED):
        for name in available():  # every scan that exists, as a person's run builds the readout
            write_result(importlib.import_module(f"scans.{name}.scan").run(room), room)
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
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
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


def test_a_full_room_line_opens_from_the_seed_drop_page(env):
    """The cohort rebuild cites the customer file, which only the full room holds."""
    r = client.post("/api/rooms/hollis_voice_seed_drop/steer", json={"piece": "retention", "sentence": "read the full room"})
    assert r.status_code == 200, r.text
    claims = {c["id"]: c for c in r.json()["readout"]["claims"]}
    nrr = next(c for c in claims.values() if (c.get("value") or {}).get("label") == "nrr_12m" and c["id"].endswith(".steer1"))
    i = next(i for i, s in enumerate(nrr["sources"]) if s["uri"] == "03_metrics/customer_mrr_by_month.csv")
    # The room's own POST /source resolves through scans.memo.merge.readout_room too (review wave 2b, B1);
    # server/app.py is the memo builder's, and its test of that route lives with it.
    got = client.get(f"/api/rooms/hollis_voice_seed_drop/claims/{nrr['id']}/sources/{i}")
    assert got.status_code == 200, got.text
    assert got.json()["room"] == "hollis_voice" and got.json()["text"]


def test_claim_source_before_a_switch_reads_the_room_itself(env):
    readout = client.get("/api/rooms/hollis_voice/steerable").json()
    c = readout["claims"][0]
    got = client.get(f"/api/rooms/hollis_voice/claims/{c['id']}/sources/0")
    assert got.status_code == 200 and got.json()["room"] == "hollis_voice"


@pytest.mark.parametrize("claim_id, i", [("no-such-claim", 0), (None, 99)])
def test_claim_source_404s(env, claim_id, i):
    readout = client.get("/api/rooms/hollis_voice/steerable").json()
    cid = claim_id or readout["claims"][0]["id"]
    assert client.get(f"/api/rooms/hollis_voice/claims/{cid}/sources/{i}").status_code == 404


def test_author_defaults_from_the_setting(env, monkeypatch):
    monkeypatch.setenv("TRICORDER_OPERATOR", "Ken")
    r = client.post("/api/rooms/hollis_voice/steer", json={"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring"})
    assert r.json()["revision"]["steer"]["author"] == "Ken"


# Review wave 2b -------------------------------------------------------------------------------


@pytest.mark.parametrize("field, size", [("author", 81), ("claim_id", 121), ("sentence", 1001), ("fund", 65), ("piece", 65)])
def test_an_oversized_steer_field_is_422(env, field, size):
    """S3: a long author, line id or sentence is refused before the steer runs."""
    payload = {"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring", field: "x" * size}
    r = client.post("/api/rooms/hollis_voice/steer", json=payload)
    assert r.status_code == 422, r.text
    assert client.get("/api/rooms/hollis_voice/revisions").json()["revisions"] == []


def test_a_name_at_the_limit_is_kept(env):
    r = client.post("/api/rooms/hollis_voice/steer", json={"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring",
                                                         "author": "K" * 80})
    assert r.status_code == 200, r.text


def test_a_scan_crash_is_a_500_naming_the_scan(env, monkeypatch):
    """O2: the steer answers 500 with the scan's name, not a bare Internal Server Error."""
    from scans.redflags import scan as redflags_scan

    monkeypatch.setattr(redflags_scan, "run", lambda room: (_ for _ in ()).throw(ValueError("bad cell")))
    r = client.post("/api/rooms/hollis_voice_seed_drop/steer", json={"piece": "retention", "sentence": "read the full room"})
    assert r.status_code == 500
    assert r.json()["detail"] == "redflags failed: ValueError: bad cell"
    assert client.get("/api/rooms/hollis_voice_seed_drop/revisions").json()["revisions"] == []


def test_rebuilding_through_the_page_keeps_the_steer(env):
    """S7: steer, then the page's "Build readout" (POST .../readout), then GET .../revisions still lists the steer."""
    client.post("/api/rooms/hollis_voice/steer", json={"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring"})
    assert client.post("/api/rooms/hollis_voice/readout").status_code == 200
    revs = client.get("/api/rooms/hollis_voice/revisions").json()
    assert [r["steer"]["instruction"] for r in revs["revisions"]] == ["treat the pilot as non-recurring"]
    assert [p["name"] for p in revs["changes"]] == ["steer 1: what changed"]


# Code review of the fix round ----------------------------------------------------------------------


@pytest.mark.parametrize("uri", ["../answer_key.json", str(ROOT / "data_room" / "answer_key.json"), "../../CLAUDE.md"])
def test_claim_source_opens_nothing_outside_the_room(env, uri):
    """Round 2, item 5: a line's source opens by the same rule as POST /source, so a readout that names a
    path outside the room (or the sealed answer key) gets a 404, never the text."""
    from scans.base import out_dir
    from schema.claim import Readout

    path = out_dir(FULL) / "readout.json"
    readout = Readout.model_validate_json(path.read_text(encoding="utf-8"))
    c = readout.claims[0]
    forged = c.model_copy(update={"sources": [c.sources[0].model_copy(update={"uri": uri, "locator": "whole"})]})
    path.write_text(readout.model_copy(update={"claims": [forged] + readout.claims[1:]}).model_dump_json(), encoding="utf-8")
    got = client.get(f"/api/rooms/hollis_voice/claims/{c.id}/sources/0")
    assert got.status_code == 404, got.text
    assert "Synthetic" not in got.text and "text" not in got.json()
