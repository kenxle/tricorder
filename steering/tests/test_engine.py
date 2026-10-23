"""The steer itself, on the real rooms (ROADMAP "steering", Done when; STEER-R4 to R13).

Each test gets its own TRICORDER_OUT_DIR, store and cache under tmp_path, with
the readout built the way a person builds it (the redflags scan, then the
memo). Rooms in data_room/ are read in place and never written. The model path
runs on HAND-BUILT responses only; no model is called.
"""

from __future__ import annotations

import json
import importlib
import shutil
from pathlib import Path

import pytest

from schema.check_quotes import check_claim
from schema.check_quotes import main as check_quotes_main
from schema.claim import Readout
from scans.base import ROOT, available, out_dir, write_result
from scans.memo.merge import build_readout, write_readout
from steering import engine
from scans.memo import pieces
from steering.models import RewordLine, RewordReading
from store import open_store

FULL = ROOT / "data_room" / "hollis_voice"
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"


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
    assert added.text.startswith("On the operator's steer, pilot not counted: ARR $2,060,868.")
    assert "$2,500,000" in added.text and "21.3%" in added.text and added.severity == "flag"
    assert "measured on the books figure" in added.text  # the gap base, as the check measures its own
    assert added.id in got.readout.pieces[0].claim_ids
    # The check's own line and number stay.
    kept = claims_by_id(got.readout)[line.id]
    assert kept.text == line.text and kept.value == line.value
    assert rev.before.verdict == rev.after.verdict == "looking_weak" and rev.verdict_moved_by == []
    assert "Verdict unchanged." in rev.note and "The checks' numbers are unchanged." in rev.note
    assert "wording rules" in rev.note
    assert rows(got.changes, "added")[0][1] == added.id
    assert got.reading.path == "rules"


def test_pilot_steer_redoes_the_piece(env, monkeypatch):
    monkeypatch.setenv("TRICORDER_OPERATOR", "Ken")
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    line = arr_line(before)
    got = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    rev = got.revision
    added = claims_by_id(got.readout)[rev.claims_added[0]]
    # Name, not "your steer"; the author comes from the setting when the request names none.
    assert rev.steer.author == "Ken"
    assert added.text.startswith("On Ken's steer, pilot not counted: ARR $2,060,868.")
    # The piece's reason is the steered figure, labelled as the operator's.
    piece = next(p for p in got.readout.pieces if p.name == "traction_and_revenue")
    assert piece.reason == added.text and piece.reason_claim_ids == [added.id]
    # The check's line moves into the diff as "before" and stays reachable.
    assert rows(got.changes, "replaced") == [["replaced", line.id, line.text, added.id]]
    assert line.id in claims_by_id(got.readout)
    # The diff's first line says what happened.
    assert got.changes.rows[0] == ["headline", "", "", "Added a scenario line."]
    assert rev.note.startswith("Added a scenario line. Rewritten on Ken's instruction")
    assert "Your scenario line is new. The original check still shows $2,240,868." in rev.note
    # The pilot agreement's notice clause, read by contract_reader.
    agreement = [s for s in added.sources if s.uri == "04_customers/pilot_agreement_marlow.pdf"]
    assert agreement and agreement[0].locator == "page 2"
    assert "30 days notice (page 2, clause 7)" in added.text
    assert check_claim(added, FULL)[1] == []


def test_author_from_the_request_wins(env, monkeypatch):
    monkeypatch.setenv("TRICORDER_OPERATOR", "Ken")
    got = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring", author="Priya")
    assert got.revision.steer.author == "Priya"
    assert claims_by_id(got.readout)[got.revision.claims_added[0]].text.startswith("On Priya's steer")


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
    assert {"nrr_12m", "grr_12m"} <= {c.value.label for c in new if c.value}
    assert {pieces.piece_of(c) for c in new} > {"retention"}  # every piece reran on the full room, not only retention
    assert all(c.id.endswith(".steer1") for c in new)
    nrr = next(c for c in new if c.value and c.value.label == "nrr_12m")
    assert nrr.value.number == pytest.approx(87.31, abs=0.01) and nrr.severity == "flag"
    assert rev.verdict_moved_by[0] == nrr.id  # the pilot agreement's lines in retention move it too
    assert nrr.conflicts_with == [tab.id]  # remapped to the seed drop's id for the same tab line
    assert tab.id in claims_by_id(got.readout)
    # Only the claims scan's "Unsupported" lines that the full room now supports are dropped, and the diff lists them.
    was = claims_by_id(before)
    assert all(was[i].scan == "claims" and was[i].text.startswith("Unsupported") for i in rev.claims_dropped)
    assert [r[1] for r in rows(got.changes, "dropped")] == rev.claims_dropped
    assert any("03_metrics/customer_mrr_by_month.csv" in s for s in rev.sources_added)
    assert rev.note.startswith("Read 5 new files; retention moved to Looking weak")
    assert "More info on the operator's instruction" in rev.note and "new claims, marked new" in rev.note
    assert "moved by" in rev.note
    assert "Every piece now reads hollis_voice, the full room, instead of hollis_voice_seed_drop." in rev.note
    assert ["source", "", "hollis_voice_seed_drop", "hollis_voice"] in got.changes.rows
    # The gap the full room closes is gone; the readout keeps its room.
    assert not [g for g in got.readout.gaps if g.piece == "retention" and "customer_mrr_by_month" in g.what]
    assert got.readout.room == "hollis_voice_seed_drop"


def test_full_room_reruns_every_piece_and_lines_open_from_the_full_room(env):
    got = engine.steer(SEED, "retention", "read the full room")
    moved = {r[1] for r in rows(got.changes, "piece moved")}
    assert "customers" in moved  # the contracts move customers, a piece other than the one typed on
    assert set(got.readout.scans_run) == set(available())
    for c in got.readout.claims:
        assert engine.claim_room(got.readout, c.id, SEED) == FULL
        assert check_claim(c, engine.claim_room(got.readout, c.id, SEED))[1] == []
    # A second ask does not read again.
    again = engine.steer(SEED, "market", "read the full room")
    assert again.revision.claims_added == []
    assert again.revision.note.startswith("Nothing new read: every piece already reads hollis_voice")


def test_claim_room_before_a_switch_is_the_room_itself(env):
    readout = engine.steerable(SEED)
    assert all(engine.claim_room(readout, c.id, SEED) == SEED for c in readout.claims)


def test_overview_steer_reads_the_full_room(env):
    got = engine.steer(SEED, "overview", "read the full room")
    assert got.source_room == "hollis_voice" and got.revision.claims_added
    assert ["typed on", "", "", "overview"] in got.changes.rows
    assert got.revision.steer.piece in {r[1] for r in rows(got.changes, "piece moved")} | {"retention", "traction_and_revenue"}


def test_overview_steer_refuses_a_rewrite(env):
    with pytest.raises(engine.BadSteer, match="On the overview"):
        engine.steer(FULL, "overview", "treat the pilot as non-recurring")


def test_full_room_on_the_full_room_changes_nothing(env):
    got = engine.steer(FULL, "retention", "read the full room")
    assert got.revision.claims_added == [] and "already the full room" in got.revision.note


def test_named_outside_source_is_not_fetched(env):
    got = engine.steer(FULL, "market", "pull the competitor's pricing pages")
    assert got.revision.steer.kind == "more_info" and got.revision.claims_added == []
    assert got.revision.note.startswith("Not fetched:")
    assert got.changes.rows[0][3].startswith("Not fetched:")


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
    # No line took the asked-for number (the claims scan may state a deck's own $3M; it was there before).
    assert [c for c in got.readout.claims if c.value and c.value.number == 3_000_000] == \
        [c for c in before.claims if c.value and c.value.number == 3_000_000]
    # A refusal says so first, and is not filed as a rewrite.
    assert rev.note.startswith("Refused: computed numbers do not change on request.")
    assert got.changes.rows[0] == ["headline", "", "", "Refused: computed numbers do not change on request."]
    assert "Rewritten" not in rev.note


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
    held_files = {f.path for f in held.files}
    assert "03_metrics/customer_mrr_by_month.csv" in held_files
    # Every piece now reads the full room, so every file its lines cite is held, and nothing they do not cite.
    cited = {s.uri for c in got.readout.claims for s in c.sources if s.kind != "url"}
    assert cited <= held_files
    assert "02_financials/expense_ledger.csv" in held_files  # cited by the mislabels lines the full room adds


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
    plain = "The deck says ARR is $2,500,000 (slide 3), which differs from the P&L's $2,240,868 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), a gap of 11.6%."
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


# Review wave 2b ---------------------------------------------------------------------------------


def test_a_negated_definition_steer_adds_no_scenario_line(env):
    """S5: "Don't treat the pilot as non-recurring" must not apply the opposite."""
    got = engine.steer(FULL, "traction_and_revenue", "Don't treat the pilot as non-recurring", author="Ken")
    assert not [c for c in got.readout.claims if c.scan == "steering"]
    assert got.revision.claims_added == []
    assert got.revision.note.startswith("Nothing changed: Tricorder could not tell what to change")


def test_a_later_rewrite_keeps_the_earlier_scenario_line(env):
    """S6: "Make this shorter" after the pilot steer keeps steer1-001 and the piece's reason."""
    first = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    line = first.revision.claims_added[0]
    assert line == "steer1-001"
    second = engine.steer(FULL, "traction_and_revenue", "Make this shorter")
    assert line in claims_by_id(second.readout)
    assert line not in second.revision.claims_dropped
    piece = next(p for p in second.readout.pieces if p.name == "traction_and_revenue")
    assert piece.reason_claim_ids == [line]
    written = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    assert line in claims_by_id(written)


def test_a_second_pilot_steer_keeps_the_first_line(env):
    """S6: a repeat pilot steer does not drop steer1's line for an identical one."""
    engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    second = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    assert "steer1-001" in claims_by_id(second.readout)
    assert "steer1-001" not in second.revision.claims_dropped
    assert [c.id for c in second.readout.claims if c.scan == "steering"] == ["steer1-001"]
    assert second.revision.note.startswith("Nothing changed: the scenario line is already in the piece (steer1-001)")


def _rebuild_as_a_person_does(room):
    """The page's "Build readout" button and python -m scans.memo: build, then write."""
    write_readout(build_readout(room), room)
    return Readout.model_validate_json((out_dir(room) / "readout.json").read_text())


def test_rebuilding_keeps_revisions_scenario_lines_and_panels(env):
    """S7: a rebuild after a steer keeps every revision, the steer panels and the scenario line."""
    first = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    engine.steer(FULL, "traction_and_revenue", "make ARR 3 million")
    rebuilt = _rebuild_as_a_person_does(FULL)
    assert [r.steer.instruction for r in rebuilt.revisions] == ["treat the pilot as non-recurring", "make ARR 3 million"]
    assert [p.name for p in rebuilt.panels if p.name.startswith("steer ")] == ["steer 1: what changed", "steer 2: what changed"]
    line = first.revision.claims_added[0]
    assert line in claims_by_id(rebuilt)
    piece = next(p for p in rebuilt.pieces if p.name == "traction_and_revenue")
    assert piece.reason_claim_ids == [line]
    # The next steer numbers itself after the kept ones, so no id repeats one an earlier version holds.
    third = engine.steer(FULL, "traction_and_revenue", "treat the pilot as non-recurring")
    assert third.changes.name == "steer 3: what changed"


def test_rebuilding_a_switched_seed_drop_keeps_the_full_room(env):
    """S7 and B1: a rebuild of the seed drop after "read the full room" still reads the full room."""
    got = engine.steer(SEED, "retention", "read the full room")
    steered = {c.id for c in got.readout.claims}
    rebuilt = _rebuild_as_a_person_does(SEED)
    assert rebuilt.room == "hollis_voice_seed_drop"
    assert engine.reads_room(rebuilt, SEED) == FULL
    assert {c.id for c in rebuilt.claims} == steered
    assert [p.verdict for p in rebuilt.pieces] == [p.verdict for p in got.readout.pieces]
    for c in rebuilt.claims:
        assert check_claim(c, FULL)[1] == []


def test_the_full_room_marker_is_an_explicit_panel(env):
    """B1: the switch is a "reads room" panel, read by scans.memo.merge.reads_room, so the memo and the server use it."""
    from scans.memo import merge

    got = engine.steer(SEED, "retention", "read the full room")
    marker = [p for p in got.readout.panels if p.name == merge.READS_PANEL]
    assert [p.model_dump() for p in marker] == [{"name": "reads room", "columns": ["Room", "Since"], "rows": [["hollis_voice", "steer 1"]]}]
    written = Readout.model_validate_json((out_dir(SEED) / "readout.json").read_text())
    assert merge.reads_room(written, SEED) == FULL
    assert merge.readout_room(SEED) == FULL
    assert merge.readout_room(FULL) == FULL
    # A marker that names any room other than the seed drop's own full room is ignored.
    forged = written.model_copy(update={"panels": [merge.reads_panel("brasswick", 1)]})
    assert merge.reads_room(forged, SEED) == SEED
    assert merge.reads_room(written, FULL) == FULL


def test_a_rewording_that_swaps_two_figures_is_refused(env):
    """S8, on a HAND-BUILT model answer: the same numbers in another order, with "agrees" for "differs"."""
    before = Readout.model_validate_json((out_dir(FULL) / "readout.json").read_text())
    line = arr_line(before)
    swapped = "The deck's ARR of $2,240,868 (slide 3) agrees with the P&L's $2,500,000 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), a gap of 11.6%."
    got = engine.steer(FULL, "traction_and_revenue", "say the ARR line more plainly", llm=reword_llm([(line.id, swapped)]))
    assert claims_by_id(got.readout)[line.id].text == line.text
    assert rows(got.changes, "wording") == []
    assert "refused" in got.revision.note


@pytest.mark.parametrize("bad", [
    # HAND-BUILT model answers. "differs" becomes "agrees", numbers in place.
    "The deck's ARR of $2,500,000 (slide 3) agrees with the P&L's $2,240,868 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), a gap of 11.6%.",
    # The sources swap around the numbers.
    "The P&L's ARR of $2,500,000 (slide 3) differs from the deck's $2,240,868 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), a gap of 11.6%.",
    # A unit changes.
    "The deck's ARR of $2,500,000 (slide 3) differs from the P&L's $2,240,868 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), a gap of 11.6 points.",
])
def test_a_rewording_that_changes_the_meaning_is_refused(bad):
    from steering.reword import guard

    old = "The deck's ARR of $2,500,000 (slide 3) differs from the P&L's $2,240,868 (12 x 'Recurring revenue (subscription plus pilot)' for 2026-09), a gap of 11.6%."
    assert guard(old, bad) is not None
    assert guard(old, old.replace("The deck's ARR of", "The deck puts ARR at")) is None


def test_a_scan_that_crashes_during_a_steer_names_the_scan_and_writes_nothing(env, monkeypatch):
    """O2: the steer stops with the scan's name, and no scan result or readout is half written."""
    from scans.redflags import scan as redflags_scan

    def boom(room):
        raise RuntimeError("the parser fell over")
    monkeypatch.setattr(redflags_scan, "run", boom)
    folder = out_dir(SEED)
    before = {p.name: p.read_bytes() for p in folder.iterdir()}
    full_before = {p.name: p.read_bytes() for p in out_dir(FULL).iterdir()}
    with pytest.raises(engine.ScanFailed, match="redflags failed: RuntimeError: the parser fell over"):
        engine.steer(SEED, "retention", "read the full room")
    assert {p.name: p.read_bytes() for p in folder.iterdir()} == before
    assert {p.name: p.read_bytes() for p in out_dir(FULL).iterdir()} == full_before


def test_the_merge_command_keeps_steers_and_starts_over_only_when_asked(env, capsys):
    """S7: python -m scans.memo keeps the steers; --fresh is the one way to start over, and says so."""
    from scans.memo import merge

    engine.steer(SEED, "retention", "read the full room")
    assert merge.main([str(SEED)]) == 0
    kept = json.loads(capsys.readouterr().out)
    assert kept["revisions_kept"] == 1 and kept["reads_room"] == "hollis_voice"
    assert merge.main([str(SEED), "--fresh"]) == 0
    fresh = json.loads(capsys.readouterr().out)
    assert fresh["revisions_kept"] == 0 and fresh["reads_room"] == "hollis_voice_seed_drop"
    assert merge.readout_room(SEED) == SEED
