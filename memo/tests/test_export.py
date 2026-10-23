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
    done = run_cli(tmp_path, str(ROOM), "--edit", str(edits), "--author", "Priya Shah")
    assert done.returncode == 0, done.stderr
    folder = tmp_path / "hollis_voice" / "memo"
    page = (folder / "memo.html").read_text(encoding="utf-8")
    memo = embedded(page)
    assert memo.version == 2 and memo.section(15).lines[0].author == "Priya Shah"
    # The operator's recommendation opens the summary, on the page and in the PDF.
    assert 'data-line-id="s02-recommendation"' in page
    text = re.sub(r"\s+", " ", pdf_text(folder / "memo.pdf"))
    s2 = text.split("2. Summary and the ask", 1)[1]
    assert s2.lstrip().startswith("Recommendation. Wait for the bank statements. (Priya Shah, version 2)")


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
    readout = Readout.model_validate_json(build_readout(tmp_path).read_text(encoding="utf-8"))
    run_cli(tmp_path, str(ROOM))
    memo = embedded((tmp_path / "hollis_voice" / "memo" / "memo.html").read_text(encoding="utf-8"))
    assert set(memo.claims) == {c.id for c in readout.claims}
    for claim in memo.claims.values():
        assert not check_claim(claim, ROOM)[1], claim.id


def built_pdf(tmp_path):
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    folder = tmp_path / "hollis_voice" / "memo"
    memo = Memo.model_validate_json((folder / "memo_v1.json").read_text(encoding="utf-8"))
    return memo, re.sub(r"\s+", " ", pdf_text(folder / "memo.pdf"))


def test_every_claim_in_the_pdf_has_a_note_naming_its_file_and_locator(tmp_path):
    memo, text = built_pdf(tmp_path)
    for sec in memo.sections:
        if sec.number not in (13, 15):  # the operator's sections print once the operator writes them
            assert f"{sec.number}. {sec.title.split(',')[0]}" in text, sec.title
    notes = re.findall(r"\[(\d+)\] ", text)
    assert notes and [int(n) for n in notes] == list(range(1, len(notes) + 1))
    for claim in memo.claims.values():
        assert not check_claim(claim, ROOM)[1]
        for s in claim.sources:
            assert f"{Path(s.uri).name}, {s.locator}" in text, (claim.id, s.uri, s.locator)
    assert "Not in the room:" in text and "not assessed yet" in text


def test_the_pdf_is_for_partners(tmp_path):
    memo, text = built_pdf(tmp_path)
    # No plumbing: no claim ids, check names, checklist numbers, commands or blanks.
    for cid in memo.claims:
        assert cid not in text
    for c in memo.claims.values():
        assert c.check.name not in text
    assert not re.search(r"(?<![!\w])C\d\d\b|python -m|scans/|Who writes|not built|[Vv]erifier|OPERATOR WRITES", text)
    for ln in (ln for s in memo.sections for ln in s.lines if ln.kind == "slot"):
        assert ln.text not in text, ln.id
    # The ask list goes to the founder, not the partners.
    assert "To ask the founder" not in text
    for a in memo.asks.values():
        assert a.what[:60] not in text
    # Numbers print as people write them, and a CSV row shows its column names.
    assert not re.search(r"\d\.\d{3,}", text)
    assert "-$0.24" in text or "Cash_Bridge" not in text
    assert "monthly_metrics.csv, row 22: month 2026-09, mrr $" in text


def test_server_routes_build_edit_and_serve(tmp_path, monkeypatch):
    from server.app import app
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    client = TestClient(app)
    assert client.get("/api/rooms/hollis_voice/memo").status_code == 404
    assert client.post("/api/rooms/hollis_voice/memo").status_code == 409  # no readout yet
    build_readout(tmp_path)
    r = client.post("/api/rooms/hollis_voice/memo")
    assert r.status_code == 200 and r.json()["version"] == 1
    r = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Dana", "base_version": 1,
                    "edits": [{"action": "add", "section": 9, "text": "Met the founders."}]})
    assert r.status_code == 200 and r.json()["version"] == 2
    kept = [{"action": "add", "section": 9, "text": "Both founders built the last product together."},
            {"action": "add", "section": 12, "text": "Ask about the pilot first."}]
    stale = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Sam Okafor", "base_version": 1, "edits": kept})
    assert stale.status_code == 409 and stale.json()["detail"]["latest_version"] == 2
    # The page keeps the typed changes and reapplies them on the version it was told about.
    again = client.post("/api/rooms/hollis_voice/memo/edits",
                        json={"author": "Sam Okafor", "base_version": stale.json()["detail"]["latest_version"], "edits": kept})
    assert again.status_code == 200 and again.json()["version"] == 3
    assert [l.text for l in Memo.model_validate(again.json()).section(9).lines if l.kind == "operator"] == \
        ["Met the founders.", "Both founders built the last product together."]
    bad = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Sam", "base_version": 3,
                      "edits": [{"action": "remove", "line_id": "nope"}]})
    assert bad.status_code == 400
    assert client.get("/api/rooms/hollis_voice/memo/versions").json() == [1, 2, 3]
    assert client.get("/api/rooms/hollis_voice/memo?version=1").json()["version"] == 1
    page = client.get("/api/rooms/hollis_voice/memo.html")
    assert page.status_code == 200 and "text/html" in page.headers["content-type"]
    assert embedded(page.text).version == 3
    pdf = client.get("/api/rooms/hollis_voice/memo.pdf")
    assert pdf.status_code == 200 and pdf.content[:4] == b"%PDF"
    assert client.get("/api/rooms/nope/memo").status_code == 404


def test_the_page_needs_no_network(tmp_path):
    build_readout(tmp_path)
    run_cli(tmp_path, str(ROOM))
    page = (tmp_path / "hollis_voice" / "memo" / "memo.html").read_text(encoding="utf-8")
    assert not re.search(r'<(script|link|img)[^>]+(src|href)="(https?:)?//', page)
    assert "\u2014" not in page and "\u2013" not in page
