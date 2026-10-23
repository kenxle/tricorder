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
        if sec.number not in (1, 13, 15):  # the head prints as one line; the operator's sections print once written
            assert f"{sec.number}. {sec.title.split(',')[0]}" in text, sec.title
    notes = re.findall(r"\[(\d+)\] ", text)
    assert notes and [int(n) for n in notes] == list(range(1, len(notes) + 1))
    for claim in memo.claims.values():
        assert not check_claim(claim, ROOM)[1]
        for s in claim.sources:
            assert f"{Path(s.uri).name}, {s.locator}" in text, (claim.id, s.uri, s.locator)
    assert "Not in the room:" in text and "not assessed yet" in text
    # ME-R14 (review wave 2b O3): every note names the date its source was read; a file, the export's date.
    dated = re.findall(r"\[\d+\] [^\[]*?\. Read \d{4}-\d\d-\d\d", text)
    assert len(dated) == len(notes)
    assert all(st.read_at == memo.built_at[:10] for k, st in memo.sources.items() if st.found and "://" not in k)


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
    client = TestClient(app, base_url="http://127.0.0.1")  # the local guard refuses any other host
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


# Review wave 2b, S1, S3 and S4: the page's fill, edit sizes, the PDF once per version, racing saves. ---------


def _client(tmp_path, monkeypatch):
    from server.app import app
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    build_readout(tmp_path)
    client = TestClient(app, base_url="http://127.0.0.1")
    assert client.post("/api/rooms/hollis_voice/memo").status_code == 200
    return client


def _outside_data(page: str) -> str:
    return re.sub(r'<script type="application/json" id="memo-data">.*?</script>', "", page, flags=re.S)


def test_a_line_cannot_expand_a_placeholder_or_carry_markup(tmp_path, monkeypatch):
    client = _client(tmp_path, monkeypatch)
    lines = ["{{DATA}}<img src=x onerror=1>", "See {{SCRIPT}} and {{SECTIONS}}", "<!--<script>"]
    r = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "{{TITLE}}", "base_version": 1,
                    "edits": [{"action": "add", "section": 9, "text": t} for t in lines]})
    assert r.status_code == 200, r.text
    page = client.get("/api/rooms/hollis_voice/memo.html").text
    outside = _outside_data(page)
    assert "<img" not in outside and "<!--" not in outside
    assert outside.count("<script") == 1  # the page's own script, once
    for t in ("{{DATA}}", "{{SCRIPT}}", "{{SECTIONS}}"):
        assert t in outside  # the operator's literal text, not an expansion
    # The embedded memo has no raw markup to break out of its element, and still parses.
    data = re.search(r'id="memo-data">(.*?)</script>', page, re.S).group(1)
    assert "<" not in data and ">" not in data
    assert [l.text for l in embedded(page).section(9).lines if l.kind == "operator"] == lines


def test_oversized_edits_are_refused_before_anything_is_saved(tmp_path, monkeypatch):
    from memo.model import MAX_AUTHOR, MAX_EDITS, MAX_LINE_TEXT
    client = _client(tmp_path, monkeypatch)
    add = {"action": "add", "section": 9, "text": "Met the founders."}
    for body in ({"author": "Dana", "base_version": 1, "edits": [{**add, "text": "x" * (MAX_LINE_TEXT + 1)}]},
                 {"author": "D" * (MAX_AUTHOR + 1), "base_version": 1, "edits": [add]},
                 {"author": "Dana", "base_version": 1, "edits": [add] * (MAX_EDITS + 1)}):
        assert client.post("/api/rooms/hollis_voice/memo/edits", json=body).status_code == 422
    assert client.get("/api/rooms/hollis_voice/memo/versions").json() == [1]
    at_limit = {"author": "D" * MAX_AUTHOR, "base_version": 1, "edits": [{**add, "text": "x" * MAX_LINE_TEXT}]}
    assert client.post("/api/rooms/hollis_voice/memo/edits", json=at_limit).status_code == 200


def test_the_pdf_is_built_once_per_version(tmp_path, monkeypatch):
    import memo.export as mexport
    client = _client(tmp_path, monkeypatch)  # version 1, its PDF built at export
    built = []
    real = mexport.render_pdf
    monkeypatch.setattr(mexport, "render_pdf", lambda memo, path: built.append(memo.version) or real(memo, path))
    for _ in range(3):
        r = client.get("/api/rooms/hollis_voice/memo.pdf")
        assert r.status_code == 200 and r.content[:4] == b"%PDF"
    assert built == []  # served as saved
    r = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Dana", "base_version": 1,
                    "edits": [{"action": "add", "section": 9, "text": "Met the founders."}]})
    assert r.status_code == 200 and built == [2]
    client.get("/api/rooms/hollis_voice/memo.pdf")
    client.get("/api/rooms/hollis_voice/memo.pdf")
    assert built == [2]


def test_a_save_that_loses_the_race_is_a_409_not_a_500(tmp_path, monkeypatch):
    from memo import store
    client = _client(tmp_path, monkeypatch)
    room = ROOT / "data_room" / "hollis_voice"
    v1 = store.load(room)
    edits = [{"action": "add", "section": 9, "text": "Met the founders."}]
    assert client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Dana", "base_version": 1, "edits": edits}).status_code == 200
    # The second save read version 1 before the first one wrote version 2.
    monkeypatch.setattr(store, "load", lambda room_dir, version=None: v1)
    r = client.post("/api/rooms/hollis_voice/memo/edits", json={"author": "Sam", "base_version": 1, "edits": edits})
    assert r.status_code == 409, r.text
    assert r.json()["detail"]["latest_version"] == 2
    monkeypatch.undo()
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    assert store.load(room).changes[-1].author == "Dana"  # the first save stands, not overwritten


def test_racing_saves_of_one_version_make_one_version(tmp_path, monkeypatch):
    import threading

    from memo import store
    from memo.export import edit
    from memo.model import Edit
    _client(tmp_path, monkeypatch)
    room = ROOT / "data_room" / "hollis_voice"
    v1 = store.load(room)
    gate, won, lost = threading.Barrier(8), [], []

    def save(k):
        gate.wait()
        try:
            won.append(edit(room, [Edit(action="add", section=9, text=f"Line {k}.")], f"Op {k}", pdf=False, base=v1))
        except FileExistsError:
            lost.append(k)

    threads = [threading.Thread(target=save, args=(k,)) for k in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(won) == 1 and len(lost) == 7
    assert store.versions(room) == [1, 2]
    assert store.load(room).changes[-1].author == won[0].memo.changes[-1].author
