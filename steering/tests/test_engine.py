"""The steer itself, on the real rooms (ROADMAP "steering", Done when; STEER-R4 to R13).

Each test gets its own TRICORDER_OUT_DIR, store and cache under tmp_path, with
the readout built the way a person builds it (the redflags scan, then the
memo). Rooms in data_room/ are read in place and never written. The model path
runs on HAND-BUILT responses only; no model is called.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from schema.check_quotes import check_claim
from schema.check_quotes import main as check_quotes_main
from schema.claim import Readout
from scans.base import ROOT, out_dir, write_result
from scans.memo.merge import build_readout, write_readout
from scans.redflags import scan as redflags
from steering import engine
from steering.models import RewordLine, RewordReading
from store import open_store

FULL = ROOT / "data_room" / "hollis_voice"
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"


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


def claims_by_id(readout):
    return {c.id: c for c in readout.claims}


def arr_line(readout):
    return next(c for c in readout.claims if c.check.name == "deck_revenue_vs_pnl" and c.value and c.value.label == "arr")


def rows(panel, change):
    return [r for r in panel.rows if r[0] == change]


# Done when 1: "treat the pilot as non-recurring" on traction ---------------------------------


def test_pilot_steer_on_traction_adds_the_reread_line_and_keeps_the_checks_line(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    line = arr_line(before)
    got = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    rev = got.revision
    assert rev.steer.kind == "rewrite" and rev.steer.piece == "traction_and_revenue"
    assert len(rev.claims_added) == 1 and rev.claims_dropped == []
    added = claims_by_id(got.readout)[rev.claims_added[0]]
    assert added.value.number == 2_060_868 and added.value.label == "arr" and added.confidence == "computed"
    assert added.text.startswith("On your steer (pilot treated as non-recurring): ARR is $2,060,868")
    assert "$2,500,000" in added.text and "21.3%" in added.text and added.severity == "flag"
    assert added.id in got.readout.pieces[0].claim_ids
    # The check's own line and number stay.
    kept = claims_by_id(got.readout)[line.id]
    assert kept.text == line.text and kept.value == line.value
    assert rev.before.verdict == rev.after.verdict == "looking_weak" and rev.verdict_moved_by == []
    assert "Verdict unchanged." in rev.note and "The checks' numbers are unchanged." in rev.note
    assert "wording rules" in rev.note
    assert rows(got.changes, "added")[0][1] == added.id
    assert got.reading.path == "rules"


def test_pilot_steer_on_the_arr_line_is_the_same_reread(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    got = engine.steer(FULL, "traction_and_revenue", "the pilot isn't recurring", claim_id=arr_line(before).id)
    assert got.revision.steer.claim_id == arr_line(before).id
    assert [claims_by_id(got.readout)[i].value.number for i in got.revision.claims_added] == [2_060_868]


def test_definition_with_no_line_named_for_it_changes_nothing_and_says_so(env):
    got = engine.steer(FULL, "traction_and_revenue", "treat the reseller deal as non-recurring")
    assert got.revision.claims_added == [] and "No P&L revenue line names 'reseller deal'" in got.revision.note


# Done when 2: "read the full room" on the seed drop's retention line ----------------------------


def test_full_room_on_seed_drop_retention_adds_new_claims_and_names_the_mover(env):
    before = Readout.model_validate_json((out_dir(SEED) / "readout.json").read_text())
    tab = next(c for c in before.claims if c.value and c.value.label == "nrr_12m")
    got = engine.steer(SEED, "retention", "read the full room", claim_id=tab.id)
    rev = got.revision
    assert rev.steer.kind == "more_info" and got.source_room == "hollis_voice"
    assert rev.before.verdict == "not_enough_in_the_room" and rev.after.verdict == "looking_weak"
    new = [claims_by_id(got.readout)[i] for i in rev.claims_added]
    assert {c.value.label for c in new} == {"nrr_12m", "grr_12m"}
    assert all(c.id.endswith(".steer1") for c in new)
    nrr = next(c for c in new if c.value.label == "nrr_12m")
    assert nrr.value.number == pytest.approx(87.31, abs=0.01) and nrr.severity == "flag"
    assert rev.verdict_moved_by == [nrr.id]
    assert nrr.conflicts_with == [tab.id]  # remapped to the seed drop's id for the same tab line
    assert tab.id in claims_by_id(got.readout) and rev.claims_dropped == []
    assert any("03_metrics/customer_mrr_by_month.csv" in s for s in rev.sources_added)
    assert "More info on your instruction" in rev.note and "2 new claims, marked new" in rev.note
    assert "moved by" in rev.note and "other pieces still read hollis_voice_seed_drop" in rev.note
    # The gap the full room closes is gone; the readout keeps its room.
    assert not [g for g in got.readout.gaps if g.piece == "retention" and "customer_mrr_by_month" in g.what]
    assert got.readout.room == "hollis_voice_seed_drop"


def test_full_room_on_the_full_room_changes_nothing(env):
    got = engine.steer(FULL, "retention", "read the full room")
    assert got.revision.claims_added == [] and "already the full room" in got.revision.note


def test_named_outside_source_is_not_fetched(env):
    got = engine.steer(FULL, "market", "pull the competitor's pricing pages")
    assert got.revision.steer.kind == "more_info" and got.revision.claims_added == []
    assert "not fetched" in got.revision.note


# Done when 3: a different number is refused -----------------------------------------------------


def test_number_request_leaves_every_number_and_says_so(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    line = arr_line(before)
    got = engine.steer(FULL, "traction_and_revenue", "make ARR 3 million", claim_id=line.id)
    rev = got.revision
    assert rev.claims_added == [] and rev.claims_dropped == []
    assert [c.value for c in got.readout.claims] == [c.value for c in before.claims]
    assert "You asked for 3 million." in rev.note and "The check's number stays as it wrote it" in rev.note
    assert line.text in rev.note
    assert not any(c.value and c.value.number == 3_000_000 for c in got.readout.claims)


# Done when 4: every rewritten claim passes the quote checker ------------------------------------


def test_every_added_claim_passes_the_quote_checker(env, capsys):
    a = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    for cid in a.revision.claims_added:
        assert check_claim(claims_by_id(a.readout)[cid], FULL)[1] == []
    b = engine.steer(SEED, "retention", "read the full room")
    for cid in b.revision.claims_added:
        assert check_claim(claims_by_id(b.readout)[cid], FULL)[1] == []
    # The command a person runs, on the steered readouts as written.
    assert check_quotes_main([str(FULL), str(out_dir(FULL) / "readout.json")]) == 0
    assert check_quotes_main([str(FULL), str(out_dir(SEED) / "readout.json")]) == 0


# Every revision is kept ------------------------------------------------------------------------


def test_revisions_are_kept_in_the_readout_and_the_store(env):
    engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    got = engine.steer(FULL, "traction_and_revenue", "make ARR 3 million")
    written = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    assert len(written.revisions) == 2 == len(got.readout.revisions)
    assert [p.name for p in written.panels if p.name.startswith("steer ")] == ["steer 1: what changed", "steer 2: what changed"]
    assert got.store.saved and got.store.version == 2
    versions = open_store().list_versions("demo", "hollis_voice")
    assert [v.revisions for v in versions] == [1, 2]
    stored = open_store().get("demo", "hollis_voice", 1).readout
    assert stored.revisions[0].steer.instruction == "treat the pilot as non-recurring"


def test_more_info_store_save_copies_the_full_rooms_files(env):
    got = engine.steer(SEED, "retention", "read the full room")
    assert got.store.saved
    held = open_store().list_company("demo", "hollis_voice_seed_drop")
    assert "03_metrics/customer_mrr_by_month.csv" in {f.path for f in held.files}
    assert "02_financials/expense_ledger.csv" not in {f.path for f in held.files}  # in the full room, cited by nothing kept


# The model path, on hand-built responses ---------------------------------------------------------


def reword_llm(lines):
    """A fake model: answers SteerReading with a plain rewrite, and RewordReading with `lines` (HAND-BUILT)."""
    from steering.models import SteerReading

    def llm(output, **kwargs):
        if output is SteerReading:
            return SteerReading(kind="rewrite", definition_term=None, asks_for_number=False, number_text=None,
                                wants_full_room=False, source_named=None)
        assert output is RewordReading
        return RewordReading(lines=[RewordLine(claim_id=i, text=t) for i, t in lines])
    return llm


def test_model_reword_keeps_numbers_and_quotes(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    line = arr_line(before)
    plain = "The deck says ARR is $2,500,000 (slide 3); the P&L gives $2,240,868 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), 11.6% lower."
    got = engine.steer(FULL, "traction_and_revenue", "say the ARR line more plainly", llm=reword_llm([(line.id, plain)]))
    assert got.reading.path == "model"
    assert claims_by_id(got.readout)[line.id].text == plain
    assert [r[1:] for r in rows(got.changes, "wording")] == [[line.id, line.text, plain]]
    assert check_claim(claims_by_id(got.readout)[line.id], FULL)[1] == []
    assert "Read as a rewrite by a model reading" in got.revision.note


def test_model_reword_that_changes_a_number_is_refused(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    line = arr_line(before)
    bad = "The deck's ARR of $3,000,000 (slide 3) differs from the P&L's $2,240,868."
    got = engine.steer(FULL, "traction_and_revenue", "say the ARR line more plainly", llm=reword_llm([(line.id, bad)]))
    assert claims_by_id(got.readout)[line.id].text == line.text
    assert rows(got.changes, "wording") == []
    assert "refused" in got.revision.note and line.id in got.revision.note


def test_no_rule_and_no_key_leaves_the_piece_and_says_why(env):
    got = engine.steer(FULL, "traction_and_revenue", "say this more plainly")
    assert got.revision.claims_added == [] and "no model key is set" in got.revision.note


# Bad input -------------------------------------------------------------------------------------


@pytest.mark.parametrize("piece, sentence, claim_id", [
    ("traction_and_revenue", "   ", None),
    ("traction_and_revenue", "x" * 501, None),
    ("not_a_piece", "read the full room", None),
    ("traction_and_revenue", "read the full room", "no-such-claim"),
])
def test_bad_input(env, piece, sentence, claim_id):
    with pytest.raises(engine.BadSteer):
        engine.steer(FULL, piece, sentence, claim_id=claim_id)


def test_no_results_is_no_readout(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "empty"))
    with pytest.raises(engine.NoReadout):
        engine.steer(FULL, "retention", "read the full room")


def test_cli(env, capsys):
    assert engine.main([str(FULL), "traction_and_revenue", "treat the pilot as non-recurring"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["revision"]["claims_added"] and out["read_by"] == "rules" and out["store"]["saved"]


def test_a_line_from_another_piece_is_refused(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    with pytest.raises(engine.BadSteer, match="is in traction_and_revenue"):
        engine.steer(FULL, "retention", "read the full room", claim_id=arr_line(before).id)


def test_number_request_on_the_piece_finds_the_line_it_names(env):
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    got = engine.steer(FULL, "traction_and_revenue", "make ARR 3 million")
    assert arr_line(before).text in got.revision.note
