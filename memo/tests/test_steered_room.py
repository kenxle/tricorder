"""Review wave 2b, B1: after "read the full room" on the seed drop, the memo and the server read the full room.

The steer runs on the real seed drop with a temporary out folder and store, no key, offline:
the same path the steering page takes on Saturday's 3:30 beat.
"""

from __future__ import annotations

import importlib
import shutil

import pytest
from fastapi.testclient import TestClient

from schema.claim import Readout
from scans.base import ROOT, available, out_dir, write_result
from scans.memo.merge import build_readout, write_readout

FULL = ROOT / "data_room" / "hollis_voice"
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"
CUSTOMER_FILE = "03_metrics/customer_mrr_by_month.csv"  # in the full room only


@pytest.fixture(scope="module")
def steered_out(tmp_path_factory):
    out = tmp_path_factory.mktemp("steered_out")
    mp = pytest.MonkeyPatch()
    mp.setenv("TRICORDER_OUT_DIR", str(out))
    mp.setenv("TRICORDER_STORE_DIR", str(tmp_path_factory.mktemp("store")))
    mp.setenv("TRICORDER_CACHE_DIR", str(tmp_path_factory.mktemp("cache")))
    mp.setenv("TRICORDER_OFFLINE", "1")
    mp.delenv("ANTHROPIC_API_KEY", raising=False)
    try:
        for room in (FULL, SEED):
            for name in available():
                write_result(importlib.import_module(f"scans.{name}.scan").run(room), room)
            write_readout(build_readout(room), room)
        from steering import engine
        engine.steer(SEED, "retention", "read the full room", save=False)
    finally:
        mp.undo()
    return out


@pytest.fixture()
def env(tmp_path, steered_out, monkeypatch):
    out = tmp_path / "out"
    shutil.copytree(steered_out, out)
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(out))
    monkeypatch.setenv("TRICORDER_STORE_DIR", str(tmp_path / "store"))
    monkeypatch.setenv("TRICORDER_CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return out


def _readout() -> Readout:
    return Readout.model_validate_json((out_dir(SEED) / "readout.json").read_text(encoding="utf-8"))


def _full_room_line(readout: Readout):
    """A line the steer added whose source is a file only the full room holds."""
    for c in readout.claims:
        if c.id.endswith(".steer1"):
            for i, s in enumerate(c.sources):
                if s.uri == CUSTOMER_FILE:
                    return c, i
    raise AssertionError("the steer added no line citing the customer file")


def test_the_steered_seed_drop_exports_with_nothing_unverified(env):
    from memo.export import export

    written = export(SEED, pdf=False)
    unverified = [ln.text for ln in written.memo.section(14).lines if ln.kind == "unverified"]
    assert unverified == []
    line, i = _full_room_line(_readout())
    assert line.id in written.memo.claims
    got = written.memo.sources[f"{line.sources[i].uri}|{line.sources[i].locator}"]
    assert got.found and got.text and not got.text.startswith("Could not open")


def test_the_steered_seed_drop_pdf_notes_its_full_room_lines(env, tmp_path):
    from pypdf import PdfReader

    from memo.export import export

    written = export(SEED, pdf=True)
    text = " ".join(p.extract_text() for p in PdfReader(str(written.pdf)).pages)
    assert "customer_mrr_by_month.csv" in text and "Could not open" not in text


def test_the_server_opens_a_full_room_line_from_the_seed_drop(env):
    from server.app import app

    client = TestClient(app, base_url="http://127.0.0.1")
    line, i = _full_room_line(_readout())
    got = client.post("/api/rooms/hollis_voice_seed_drop/source", json=line.sources[i].model_dump(mode="json"))
    assert got.status_code == 200, got.text
    assert got.json()["text"]
    assert client.get(f"/api/rooms/hollis_voice_seed_drop/files/{CUSTOMER_FILE}").status_code == 200
    # The seed drop's own files still open, and the switch opens no other room.
    assert client.get("/api/rooms/hollis_voice_seed_drop/files/01_overview/claims.json").status_code == 200
    other = {"kind": "file", "uri": "../hollis_voice_clean/03_metrics/customer_mrr_by_month.csv", "locator": "row 2", "quote": "x"}
    assert client.post("/api/rooms/hollis_voice_seed_drop/source", json=other).status_code == 404


def test_before_a_steer_the_seed_drop_does_not_read_the_full_room(tmp_path, monkeypatch):
    from server.app import app

    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))  # no readout: nothing switched
    client = TestClient(app, base_url="http://127.0.0.1")
    body = {"kind": "file", "uri": CUSTOMER_FILE, "locator": "row 2", "quote": "x"}
    assert client.post("/api/rooms/hollis_voice_seed_drop/source", json=body).status_code == 404
    assert client.get(f"/api/rooms/hollis_voice_seed_drop/files/{CUSTOMER_FILE}").status_code == 404
