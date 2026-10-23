"""The real paths: the CLI, the PDF and the server routes."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pdfplumber
from fastapi.testclient import TestClient

from schema.check_quotes import check_claim
from schema.claim import Readout

from memo.model import Memo
from memo.tests.conftest import ROOM, ROOT, build_readout


def run_cli(out: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "TRICORDER_OUT_DIR": str(out)}
    return subprocess.run([sys.executable, "-m", "memo", *args], cwd=ROOT, env=env, capture_output=True, text=True)


def embedded(html_text: str) -> Memo:
    m = re.search(r'<script type="application/json" id="memo-data">(.*?)</script>', html_text, re.S)
    return Memo.model_validate_json(m.group(1).replace("<\\/", "</"))


def pdf_text(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages)


def test_cli_writes_the_draft_the_page_and_the_pdf(tmp_path):
    build_readout(tmp_path)
    done = run_cli(tmp_path, str(ROOM))
    assert done.returncode == 0, done.stderr
    summary = json.loads(done.stdout)
    folder = tmp_path / "hollis_voice" / "memo"
    assert summary["version"] == 1 and Path(summary["memo"]) == folder / "memo_v1.json"
    assert (folder / "memo.html").exists() and (folder / "memo.pdf").exists()
    assert summary["sections_empty"] and all(isinstance(v, list) for v in summary["sections_empty"].values())


def test_cli_takes_a_readout_json_and_a_second_run_makes_version_2(tmp_path):
    readout = build_readout(tmp_path)
    assert run_cli(tmp_path, str(readout), "--room-dir", str(ROOM)).returncode == 0
    done = run_cli(tmp_path, str(ROOM))
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["version"] == 2


def test_cli_applies_an_edit_file(tmp_path):
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    edits = tmp_path / "edits.json"
    edits.write_text(json.dumps([{"action": "replace", "line_id": "s15-recommendation", "text": "Wait for the bank statements."}]))
    done = run_cli(tmp_path, str(ROOM), "--edit", str(edits), "--author", "Dana")
    assert done.returncode == 0, done.stderr
    memo = embedded((tmp_path / "hollis_voice" / "memo" / "memo.html").read_text(encoding="utf-8"))
    assert memo.version == 2 and memo.section(15).lines[0].author == "Dana"


def test_cli_refuses_without_a_readout_or_with_a_bad_edit(tmp_path):
    done = run_cli(tmp_path, str(ROOM))
    assert done.returncode == 2 and "python -m scans.memo" in done.stderr
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    edits = tmp_path / "edits.json"
    edits.write_text(json.dumps([{"action": "remove", "line_id": "nope"}]))
    done = run_cli(tmp_path, str(ROOM), "--edit", str(edits), "--author", "Dana")
    assert done.returncode == 2 and "no line" in done.stderr


def test_every_claim_in_the_page_passes_the_quote_checker(tmp_path):
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    memo = embedded((tmp_path / "hollis_voice" / "memo" / "memo.html").read_text(encoding="utf-8"))
    assert len(memo.claims) == 10
    for claim in memo.claims.values():
        assert not check_claim(claim, ROOM)[1], claim.id


def test_every_claim_in_the_pdf_has_a_note_naming_its_source_and_locator(tmp_path):
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    folder = tmp_path / "hollis_voice" / "memo"
    memo = Memo.model_validate_json((folder / "memo_v1.json").read_text(encoding="utf-8"))
    text = re.sub(r"\s+", " ", pdf_text(folder / "memo.pdf"))
    for sec in [s.title for s in memo.sections]:
        assert sec.split(",")[0] in text
    notes = re.findall(r"\[(\d+)\] (redflags-\d{3})\.", text)
    assert {cid for _, cid in notes} == set(memo.claims)
    for claim in memo.claims.values():
        assert not check_claim(claim, ROOM)[1]
        for s in claim.sources:
            assert f"{s.uri}, {s.locator}" in text, (claim.id, s.uri, s.locator)
    assert "OPERATOR WRITES" in text and "GAP" in text and "Not in the readout yet:" in text and "Not in the room:" in text


def test_server_routes_build_edit_and_serve(tmp_path, monkeypatch):
    from server.app import app
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    client = TestClient(app, base_url="http://127.0.0.1")  # the local guard refuses any other host
    assert client.get("/api/rooms/hollis_voice/memo").status_code == 404
    assert client.post("/api/rooms/hollis_voice/memo").status_code == 409  # no readout yet
    build_readout(tmp_path)
    r = client.post("/api/rooms/hollis_voice/memo")
    assert r.status_code == 200 and r.json()["version"] == 1
    r = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Dana", "base_version": 1,
                    "edits": [{"action": "add", "section": 9, "text": "Met the founders."}]})
    assert r.status_code == 200 and r.json()["version"] == 2
    stale = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Sam", "base_version": 1,
                        "edits": [{"action": "add", "section": 9, "text": "x"}]})
    assert stale.status_code == 409
    bad = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Sam", "base_version": 2,
                      "edits": [{"action": "remove", "line_id": "nope"}]})
    assert bad.status_code == 400
    assert client.get("/api/rooms/hollis_voice/memo/versions").json() == [1, 2]
    assert client.get("/api/rooms/hollis_voice/memo?version=1").json()["version"] == 1
    page = client.get("/api/rooms/hollis_voice/memo.html")
    assert page.status_code == 200 and "text/html" in page.headers["content-type"]
    assert embedded(page.text).version == 2
    pdf = client.get("/api/rooms/hollis_voice/memo.pdf")
    assert pdf.status_code == 200 and pdf.content[:4] == b"%PDF"
    assert client.get("/api/rooms/nope/memo").status_code == 404


def test_the_page_needs_no_network(tmp_path):
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    page = (tmp_path / "hollis_voice" / "memo" / "memo.html").read_text(encoding="utf-8")
    assert not re.search(r'<(script|link|img)[^>]+(src|href)="(https?:)?//', page)
    assert "\u2014" not in page and "\u2013" not in page
