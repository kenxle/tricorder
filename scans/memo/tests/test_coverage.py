"""Tests for the checklist coverage step (FRAMEWORKS.md, "Checklist coverage").

Each test names the requirement it proves, from
docs/features/20261022.13_checklist_coverage/03_prd.md (CC-R1 to CC-R20).
Every room used here is synthetic.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from schema.claim import Claim, Gap, Readout
from scans.memo import checklist, coverage
from scans.memo.merge import build_readout

ROOT = Path(__file__).resolve().parents[3]
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"
FULL = ROOT / "data_room" / "hollis_voice"
BRASS = ROOT / "data_room" / "brasswick"
SAMPLE_GAPS = ROOT / "docs/features/20261022.13_checklist_coverage/spike/sample_gaps_seed_drop.json"


@pytest.fixture(autouse=True)
def _out(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "out"))
    return tmp_path / "out"


def _readout(room, gaps=(), claims=()):
    return Readout(room=room.name, built_at="2026-10-24T10:00:00Z", gaps=list(gaps), claims=list(claims))


def _sample_gaps():
    return [Gap(**{k: g[k] for k in ("what", "why", "would_need", "piece")})
            for g in json.loads(SAMPLE_GAPS.read_text())["gaps"]]


def _set_stage(out, room, stage):
    folder = out / room.name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "operator.json").write_text(json.dumps({"stage": stage}))


def _panel(readout, name):
    return next(p for p in readout.panels if p.name == name)


def _counts(readout):
    return dict((k, v) for k, v in _panel(readout, coverage.COUNTS_PANEL).rows)


def _records(readout):
    panel = _panel(readout, coverage.COVERAGE_PANEL)
    return {row[0]: dict(zip(panel.columns, row)) for row in panel.rows}


def _claim(cid, check_name, uri="01_overview/pitch_deck.pdf", severity=None):
    return Claim.model_validate({
        "id": cid, "scan": "redflags", "text": "A test claim.", "severity": severity,
        "check": {"kind": "script", "name": check_name}, "confidence": "computed",
        "sources": [{"kind": "file", "uri": uri, "locator": "page 1", "quote": "x"}],
    })


def _checklist_lines(readout):
    return [a for a in readout.asks if a.checklist_id]


# Stage ---------------------------------------------------------------------


def test_stage_read_from_deck_cover():  # CC-R1
    r = coverage.apply(_readout(SEED), SEED)
    c = _counts(r)
    assert c["stage"] == "series_a" and c["stage_set_by"] == "deck"
    assert "01_overview/pitch_deck.pdf, slide 1" in c["stage_source"]
    assert "Series A |" in c["stage_source"]


def test_stage_brasswick_is_seed():  # CC-R1
    assert _counts(coverage.apply(_readout(BRASS), BRASS))["stage"] == "seed"


def test_stage_falls_back_to_claims_json(tmp_path):  # CC-R1
    room = tmp_path / "room"
    (room / "01_overview").mkdir(parents=True)
    shutil.copy(SEED / "01_overview/claims.json", room / "01_overview/claims.json")
    c = _counts(coverage.apply(_readout(room), room))
    assert c["stage"] == "series_a"
    assert "claims.json" in c["stage_source"]


def test_operator_stage_wins_and_changes_nothing_else(_out):  # CC-R2
    before = coverage.apply(_readout(SEED, claims=[_claim("redflags-001", "cap_table_reconcile")]), SEED)
    _set_stage(_out, SEED, "pre_seed")
    after = coverage.apply(_readout(SEED, claims=[_claim("redflags-001", "cap_table_reconcile")]), SEED)
    c = _counts(after)
    assert c["stage"] == "pre_seed" and c["stage_set_by"] == "operator" and c["deck_stage"] == "series_a"
    assert after.claims == before.claims and after.pieces == before.pieces and after.top_flags == before.top_flags


def test_unknown_stage_writes_no_statuses(tmp_path):  # CC-R3
    room = tmp_path / "room"
    (room / "03_metrics").mkdir(parents=True)
    (room / "03_metrics/monthly_metrics.csv").write_text("month,mrr\n")
    r = coverage.apply(_readout(room), room)
    assert _counts(r)["label"] == "stage_unknown"
    assert not any(p.name == coverage.COVERAGE_PANEL for p in r.panels)
    assert _checklist_lines(r) == []


def test_stage_outside_three_is_unknown(_out):  # CC-R3
    _set_stage(_out, SEED, "series_b")
    r = coverage.apply(_readout(SEED), SEED)
    c = _counts(r)
    assert c["label"] == "stage_unknown" and "series_b" in c["label_reason"]
    assert _checklist_lines(r) == []


# Coverage ------------------------------------------------------------------


def test_every_item_has_one_status():  # CC-R4
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    recs = _records(r)
    total = len(checklist.load())
    assert len(recs) == total
    assert {rec["status"] for rec in recs.values()} <= set(coverage.STATUSES)
    c = _counts(r)
    assert sum(int(c[s]) for s in coverage.STATUSES) == total


def test_load_rejects_unknown_level(tmp_path):  # CC-R4
    bad = tmp_path / "checklist.csv"
    text = checklist.CHECKLIST_CSV.read_text().splitlines()
    head, first = text[0], text[1].replace(",no,no,lighter,", ",maybe,no,lighter,", 1)
    bad.write_text("\n".join([head, first]) + "\n")
    with pytest.raises(ValueError):
        checklist.load(bad)


def test_check_row_needs_a_real_claim():  # CC-R5
    r = coverage.apply(_readout(FULL), FULL)
    assert _records(r)["C05"]["status"] == "not_checked"
    r = coverage.apply(_readout(FULL, claims=[_claim("redflags-007", "arr_from_subscription_rows")]), FULL)
    rec = _records(r)["C05"]
    assert rec["status"] == "checked" and "redflags-007" in rec["detail"]


def test_row_checks_are_exact_for_1_12_and_1_13():  # CC-R5
    r = coverage.apply(_readout(FULL, claims=[_claim("redflags-001", "billings_vs_recognised_revenue")]), FULL)
    recs = _records(r)
    assert recs["C07"]["status"] == "checked"
    assert recs["C06"]["status"] != "checked"


def test_entry_checks_cover_every_entry():  # CC-R5
    for row in checklist.load():
        for entry in row.entries:
            assert checklist.ENTRY_CHECKS.get(entry), f"{row.id} names {entry}, which has no check name"


def test_missing_check_names_inputs(_out):  # CC-R5
    recs = _records(coverage.apply(_readout(SEED), SEED))
    assert recs["C05"]["status"] == "missing"
    assert "C03" in recs["C05"]["detail"] and "C34" in recs["C05"]["detail"]


def test_check_with_later_stage_input_is_not_checked(_out):  # CC-R5
    _set_stage(_out, SEED, "pre_seed")
    recs = _records(coverage.apply(_readout(SEED), SEED))
    rows = {r.id: r for r in checklist.load()}
    # C37 (concentration) is "not stated" at pre-seed; its input C34 (contracts) is "no" there.
    assert rows["C37"].stage["pre_seed"] == "not stated" and rows["C34"].stage["pre_seed"] == "no"
    assert recs["C37"]["status"] == "not_checked"
    assert "C34" in recs["C37"]["detail"] and "not expected" in recs["C37"]["detail"]


def test_outside_rows_never_missing():  # CC-R5
    for room in (SEED, FULL, BRASS):
        recs = _records(coverage.apply(_readout(room), room))
        outside = [r for r in recs.values() if r["kind"] == "outside"]
        assert outside and all(r["status"] != "missing" for r in outside)


def test_cannot_check_is_not_checked():  # CC-R5
    # A check that cannot run writes a gap and no claim. The claim, not the gap, is what checks a row.
    gap = Gap(what="Not in the room: the cap table", why="cannot_check", would_need="the cap table")
    assert _records(coverage.apply(_readout(FULL, gaps=[gap]), FULL))["C81"]["status"] == "not_checked"
    ran = _claim("redflags-003", "cap_table_reconcile", uri="02_financials/cap_table.xlsx")
    assert _records(coverage.apply(_readout(FULL, gaps=[gap], claims=[ran]), FULL))["C81"]["status"] == "checked"


def test_deck_vs_books_claims_check_c65():  # CC-R5, review S9
    r = coverage.apply(_readout(FULL, claims=[_claim("redflags-008", "deck_revenue_vs_pnl")]), FULL)
    assert _records(r)["C65"]["status"] == "checked"
    r = coverage.apply(_readout(FULL, claims=[_claim("redflags-009", "deck_history_vs_metrics")]), FULL)
    assert _records(r)["C65"]["status"] == "checked"


def test_check_that_ran_without_a_missing_file_is_checked_and_still_asked():  # CC-R5, CC-R9, review S10
    r = coverage.apply(_readout(SEED, claims=[_claim("redflags-001", "mrr_column_vs_subscription_rows",
                                                    uri="02_financials/financial_model.xlsx")]), SEED)
    rec = _records(r)["C06"]
    assert rec["status"] == "checked"
    assert "redflags-001" in rec["detail"] and "C03" in rec["detail"] and "Cannot run" not in rec["detail"]
    c03 = next(row for row in _panel(r, coverage.ASKS_PANEL).rows if "C03" in row[1].split(", "))
    assert "C06" in c03[1].split(", ")


def test_founder_text_has_no_cell_reference():  # review U8
    r = coverage.apply(_readout(SEED), SEED)
    for a in r.asks:
        assert "Cap_Table!" not in a.what and ".xlsx" not in a.what, a.what


def test_balance_sheet_gap_is_not_revenue_by_customer():  # review U8
    g = Gap(what="Not in the room: a balance sheet with a deferred revenue line", why="file missing",
            would_need="monthly balance sheets, or invoices and revenue by customer")
    assert "C03" not in checklist.items_for_gap(g)


def test_ask_line_numbers_are_positions_in_readout_asks():  # review U9
    from schema.claim import AskItem
    before = AskItem(what="Something the ask-list step wrote first", why="x", piece="market", from_kind="weak_piece")
    r = _readout(SEED); r.asks = [before]
    r = coverage.apply(r, SEED)
    rec = _records(r)["C03"]
    n = int(rec["ask_line"])
    assert r.asks[n - 1].checklist_id is not None and "C03" in next(
        row for row in _panel(r, coverage.ASKS_PANEL).rows if row[0] == r.asks[n - 1].what)[1]


def test_match_by_pattern_not_column():  # CC-R6
    recs = _records(coverage.apply(_readout(FULL), FULL))
    assert recs["C23"]["status"] == "found"
    assert "02_financials/expense_ledger.csv" in recs["C23"]["detail"]


def test_sow_is_not_a_customer_contract():  # CC-R6
    rec = _records(coverage.apply(_readout(BRASS), BRASS))["C34"]
    assert rec["status"] == "found"
    assert "order_form_ostley_freight.pdf" in rec["detail"] and "msa_corvane_logistics.pdf" in rec["detail"]
    assert "sow_" not in rec["detail"]


def test_matcher_agrees_with_hollis_voice_column():  # CC-R6
    files = checklist.room_files(FULL)
    for row in checklist.load():
        if row.kind != "document":
            continue
        col = row.hollis_voice_file.split(" ")[0].rstrip(",")
        if not col or col == "not" or col.endswith("/"):
            continue
        assert col in checklist.match_document(row, files, FULL), f"{row.id} should match {col}"


def test_every_row_says_why():  # CC-R7
    for rec in _records(coverage.apply(_readout(SEED), SEED)).values():
        assert rec["detail"].strip(), rec["id"]


# Ask list ------------------------------------------------------------------


def test_every_missing_item_is_asked():  # CC-R8
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    missing = {k for k, v in _records(r).items() if v["status"] == "missing"}
    covered = {i for row in _panel(r, coverage.ASKS_PANEL).rows for i in row[1].split(", ")}
    assert missing and missing <= covered


def test_lighter_items_are_if_you_have_it():  # CC-R8, and Ken's default 1 for "not stated"
    r = coverage.apply(_readout(SEED), SEED)
    rows = {r_.id: r_ for r_ in checklist.load()}
    details = {row[0]: row[1].split(", ") for row in _panel(r, coverage.ASKS_PANEL).rows}
    for a in _checklist_lines(r):
        levels = {rows[i].stage["series_a"] for i in details[a.what]}
        assert a.if_you_have_it == ("yes" not in levels)


def test_not_stated_items_are_asked_if_you_have_it():  # Ken's default 1
    r = coverage.apply(_readout(FULL), FULL)
    rec = _records(r)["C99"]  # insurance policies: "not stated" at Series A
    assert rec["status"] == "missing"
    line = next(a for a in _checklist_lines(r) if a.checklist_id == "C99")
    assert line.if_you_have_it


def test_missing_checks_fold_into_documents():  # CC-R9
    r = coverage.apply(_readout(SEED), SEED)
    kinds = {row.id: row.kind for row in checklist.load()}
    assert all(kinds[a.checklist_id] != "check" for a in _checklist_lines(r))
    c03 = next(row for row in _panel(r, coverage.ASKS_PANEL).rows if row[1].split(", ")[0] == "C03")
    assert {"C05", "C15", "C37"} <= set(c03[1].split(", "))


def test_pre_seed_asks_nothing_expected_later(_out):  # CC-R10
    _set_stage(_out, SEED, "pre_seed")
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    rows = {row.id: row for row in checklist.load()}
    for line in _panel(r, coverage.ASKS_PANEL).rows:
        assert any(rows[i].stage["pre_seed"] != "no" for i in line[1].split(", ")), line
    # The order forms and the pilot agreement (C34) are "no" at pre-seed.
    assert not any("order form" in a.what.lower() or "pilot agreement" in a.what.lower() for a in r.asks)


def test_ask_text_comes_from_guide():  # CC-R11
    r = coverage.apply(_readout(FULL), FULL)
    guide = (ROOT / "docs/reports/20261022.03_document_guides/ip-assignment.md").read_text()
    line = next(a for a in _checklist_lines(r) if a.checklist_id == "C76")
    assert line.what in guide


def test_ask_text_names_no_flag():  # CC-R11
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    for a in _checklist_lines(r):
        text = (a.what + " " + a.why).lower()
        assert "flag" not in text and "fraud" not in text and "discrepan" not in text


def test_cannot_settle_asks_and_stage():  # CC-R12
    r = coverage.apply(_readout(FULL), FULL)
    late = {a.checklist_id for a in _checklist_lines(r) if a.why.startswith("After the term sheet.")}
    assert late == {"C01", "C21", "C79"}


def test_walk_through_replaced_by_flag_lines():  # CC-R12
    r = coverage.apply(_readout(FULL), FULL)
    assert any(a.checklist_id == "C71" for a in r.asks)
    r = coverage.apply(_readout(FULL, claims=[_claim("redflags-002", "top_customer_share", severity="flag")]), FULL)
    assert not any(a.checklist_id == "C71" for a in r.asks)


def test_cap_table_instruments_without_documents():  # CC-R13, Ken's default 3
    r = coverage.apply(_readout(SEED), SEED)
    safe_gaps = [g for g in r.gaps if g.what.startswith("Not in the room: the signed SAFE for")]
    assert len(safe_gaps) == 3 and all(g.piece == "the_pitch_itself" for g in safe_gaps)
    safe_lines = [a for a in r.asks if "signed SAFE" in a.what]
    assert len(safe_lines) == 1
    for holder in ("Tidewater Seed Fund I, LP", "Winifred Hartley (angel)", "Ostrander Lane Ventures II, LP"):
        assert holder in safe_lines[0].what
    assert any("option grant" in g.what for g in r.gaps)


# Dedupe --------------------------------------------------------------------


def test_no_request_twice():  # CC-R14: the real merge, with a fake scan result on disk
    from schema.claim import ScanResult
    from scans.base import write_result

    for room, gaps in ((SEED, _sample_gaps()), (FULL, []), (BRASS, [])):
        dup = [Gap(what="Not in the room: an expense ledger", why="file missing", would_need="the expense ledger"),
               Gap(what="Not in the room: an expense ledger", why="file missing", would_need="the expense ledger by vendor")]
        write_result(ScanResult(scan="redflags", room=room.name, ran_at="2026-10-24T10:00:00Z", gaps=list(gaps) + dup), room)
        r = build_readout(room)
        assert "redflags" in r.scans_run
        whats = [a.what.strip().lower() for a in r.asks]
        assert len(whats) == len(set(whats)), room
        kinds = {row.id: row.kind for row in checklist.load()}
        by_item = {}
        for row in _panel(r, coverage.ASKS_PANEL).rows:
            # A check row may sit on two lines when it needs two missing files; a document is asked once.
            for i in (i for i in row[1].split(", ") if kinds[i] != "check"):
                by_item.setdefault(i, set()).add(row[2])
        assert not any({"gap", "checklist"} <= k for k in by_item.values()), room
        assert sum(1 for a in r.asks if "expense ledger" in a.what.lower()) <= 1, room


def test_gap_wins_over_checklist():  # CC-R15
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    gap_lines = [a for a in r.asks if a.from_kind == "gap"]
    whats = {a.what for a in gap_lines}
    for g in _sample_gaps():
        assert g.would_need in whats
    assert not any(a.from_kind == "checklist" and a.checklist_id in ("C03", "C23", "C34") for a in r.asks)
    assert checklist.gap_is_asked(r.asks, _sample_gaps()[0])


def test_two_gaps_for_one_document_ask_once():  # CC-R14, found on the real redflags output
    gaps = [Gap(what="Not in the room: an expense ledger", why="file missing", would_need="the expense ledger with vendor, description and amount"),
            Gap(what="Not in the room: an expense ledger", why="file missing", would_need="the expense ledger with booked_as and category")]
    r = coverage.apply(_readout(SEED, gaps=gaps), SEED)
    assert sum(1 for a in r.asks if "expense ledger" in a.what) == 1


def test_same_request_rows_fold():  # CC-R16
    r = coverage.apply(_readout(FULL), FULL)
    line = next(row for row in _panel(r, coverage.ASKS_PANEL).rows if row[1].split(", ")[0] == "C35")
    assert "C46" in line[1].split(", ")
    assert not any(a.checklist_id == "C46" for a in r.asks)


def test_top_five_pinned():  # Ken's default 5
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    tops = [row for row in _panel(r, coverage.ASKS_PANEL).rows if row[4]]
    assert [row[4] for row in sorted(tops, key=lambda x: int(x[4]))] == ["1", "2", "3", "4", "5"]
    assert all(row[3] == "before_second_meeting" for row in tops)


# Output --------------------------------------------------------------------


def test_readout_with_coverage_validates():  # CC-R18
    r = coverage.apply(_readout(SEED, gaps=_sample_gaps()), SEED)
    Readout.model_validate_json(r.model_dump_json())
    names = {p.name for p in r.panels}
    assert {coverage.COVERAGE_PANEL, coverage.COUNTS_PANEL, coverage.ASKS_PANEL} <= names


def test_merge_runs_coverage_on_the_seed_drop():  # CC-R18, the slice's Done when
    r = build_readout(SEED)
    assert any(p.name == coverage.COVERAGE_PANEL for p in r.panels)
    assert any(a.from_kind == "checklist" and a.checklist_id for a in r.asks)


def test_runs_offline(monkeypatch):  # CC-R20
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    import socket

    def _no_network(*a, **k):
        raise AssertionError("coverage opened a network connection")

    monkeypatch.setattr(socket, "create_connection", _no_network)
    monkeypatch.setattr(socket.socket, "connect", _no_network)
    coverage.apply(_readout(SEED), SEED)
