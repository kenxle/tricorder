"""Operator edits make numbered versions; the operator's words are marked as theirs."""

from __future__ import annotations

import pytest

from memo import store
from memo.build import build_memo
from memo.edit import EditError, apply_edits, carry_operator_lines
from memo.model import Edit
from memo.tests.conftest import ROOM, by_check, with_pieces

AT = "2026-10-23T12:00:00Z"
LATER = "2026-10-23T13:00:00Z"


def test_an_operator_line_is_marked_as_theirs(readout):
    v1 = build_memo(readout, ROOM, AT)
    v2 = apply_edits(v1, [Edit(action="add", section=9, text="I met both founders; they have worked together since 2019.")], "Priya Shah", LATER)
    ids = [l.id for l in v2.section(9).lines]
    assert ids[-2:] == ["op-2-1", "s09-coverage"]  # above the section's closing coverage line
    ln = v2.section(9).lines[-2]
    assert (ln.kind, ln.author, ln.version, ln.claim_ids) == ("operator", "Priya Shah", 2, [])
    assert ln.unsourced_numbers == ["2019"]
    assert v2.version == 2 and v2.based_on_version == 1
    assert v1.version == 1 and all(l.kind != "operator" for s in v1.sections for l in s.lines)


def test_a_figure_with_no_claim_is_the_operators_figure(readout):
    v2 = apply_edits(build_memo(readout, ROOM, AT),
                     [Edit(action="replace", line_id="s15-recommendation", text="Wait. Invest $1.5M if burn is under $400,000 a month.")],
                     "Dana", LATER)
    ln = v2.section(15).lines[0]
    assert ln.kind == "operator" and ln.unsourced_numbers == ["$1.5M", "$400,000"]
    assert "s15-recommendation" in v2.withdrawn_lines


def test_a_date_is_not_a_figure(readout):
    from memo.edit import unsourced_numbers
    assert unsourced_numbers("I met them on 2026-10-20; they have worked together for 6 years.") == ["6"]
    assert unsourced_numbers("Burn in 2026-09 was $400,000.") == ["$400,000"]


def test_attached_claims_are_kept_and_unknown_claims_refused(readout):
    v1 = build_memo(readout, ROOM, AT)
    deck = by_check(readout, "deck_revenue_vs_pnl", "flag")[0]
    v2 = apply_edits(v1, [Edit(action="add", section=7, text="ARR is stated as $2,500,000 on the deck.", claim_ids=[deck])], "Dana", LATER)
    ln = v2.section(7).lines[-2]
    assert ln.claim_ids == [deck] and ln.unsourced_numbers == []
    with pytest.raises(EditError, match="no claim"):
        apply_edits(v1, [Edit(action="add", section=7, text="x", claim_ids=["nope-001"])], "Dana", LATER)


def test_a_claim_line_rewritten_with_a_new_figure_is_the_operators(readout):
    """A rewrite that keeps the claim's figures keeps its claims; one with a new figure detaches them."""
    v1 = build_memo(readout, ROOM, AT)
    cash = by_check(readout, "capitalised_spend_vs_pnl_and_cash")[0]
    line_id = f"s10-{cash}"
    old = v1.line(line_id)[1]
    kept = apply_edits(v1, [Edit(action="replace", line_id=line_id, text="Cash is $1,800,000, and the bridge ties.",
                                 claim_ids=old.claim_ids)], "Priya Shah", LATER)
    ln = next(l for l in kept.section(10).lines if l.kind == "operator")
    assert ln.claim_ids == [cash] and ln.unsourced_numbers == []
    moved = apply_edits(v1, [Edit(action="replace", line_id=line_id, text="Cash is $2,100,000 after the March wire.",
                                  claim_ids=old.claim_ids)], "Priya Shah", LATER)
    ln = next(l for l in moved.section(10).lines if l.kind == "operator")
    assert (ln.author, ln.claim_ids, ln.unsourced_numbers) == ("Priya Shah", [], ["$2,100,000"])
    assert line_id in moved.withdrawn_lines
    assert "its claims detached" in moved.changes[-1].what


def test_many_changes_make_one_version(readout):
    v1 = build_memo(readout, ROOM, AT)
    clause = by_check(readout, "clause_notes")[0]
    v2 = apply_edits(v1, [Edit(action="add", section=9, text="Met both founders."),
                          Edit(action="remove", line_id=f"s07-{clause}"),
                          Edit(action="replace", line_id="s15-recommendation", text="Wait for the bank statements.")],
                     "Priya Shah", LATER)
    assert v2.version == 2 and len([c for c in v2.changes if c.version == 2]) == 1


def test_the_recommendation_opens_the_summary(readout):
    from memo.html import recommendation
    v1 = build_memo(readout, ROOM, AT)
    assert recommendation(v1) is None
    v2 = apply_edits(v1, [Edit(action="replace", line_id="s15-recommendation", text="Wait for the bank statements.")],
                     "Priya Shah", LATER)
    rec = recommendation(v2)
    assert (rec.id, rec.label, rec.text, rec.author) == ("s02-recommendation", "Recommendation", "Wait for the bank statements.", "Priya Shah")


def test_bad_edits_are_refused(readout):
    v1 = build_memo(readout, ROOM, AT)
    for e, msg in ((Edit(action="add", text="x"), "section"), (Edit(action="add", section=99, text="x"), "no section"),
                   (Edit(action="remove", line_id="nope"), "no line"), (Edit(action="replace", line_id="s15-recommendation", text="  "), "text")):
        with pytest.raises(EditError, match=msg):
            apply_edits(v1, [e], "Dana", LATER)
    with pytest.raises(EditError, match="author"):
        apply_edits(v1, [Edit(action="add", section=9, text="x")], " ", LATER)


def test_each_version_gets_a_change_log_line_and_the_header_follows(readout):
    v1 = build_memo(readout, ROOM, AT)
    line_id = f"s07-{by_check(readout, 'clause_notes')[0]}"
    v2 = apply_edits(v1, [Edit(action="remove", line_id=line_id)], "Dana", LATER)
    v3 = apply_edits(v2, [Edit(action="add", section=12, text="Ask about the pilot first.")], "Sam", LATER)
    changes = [ln for ln in v3.section(16).lines if ln.kind == "change"]
    assert [ln.label for ln in changes] == ["Version 1", "Version 2", "Version 3"]
    assert f"Removed Tricorder's line {line_id} from section 7" in changes[1].text and "Dana" in changes[1].text
    assert next(l for l in v3.section(1).lines if l.id == "s01-version").text == "Shared version 3. Made from version 2."


def test_versions_are_saved_and_never_overwritten(readout, out_dir):
    v1 = build_memo(readout, ROOM, AT)
    store.save(v1, ROOM)
    with pytest.raises(FileExistsError):
        store.save(v1, ROOM)
    store.save(apply_edits(v1, [Edit(action="add", section=9, text="Met them.")], "Dana", LATER), ROOM)
    assert store.versions(ROOM) == [1, 2]
    assert store.load(ROOM).version == 2 and store.load(ROOM, 1).version == 1


def test_a_rebuild_keeps_the_operators_lines(readout):
    v1 = build_memo(readout, ROOM, AT)
    first, second = (f"s07-{c}" for c in by_check(readout, "clause_notes")[:2])
    v2 = apply_edits(v1, [Edit(action="add", section=7, line_id=first, text="The founder says the pilot will convert."),
                          Edit(action="remove", line_id=second),
                          Edit(action="replace", line_id="s15-recommendation", text="Wait.")], "Dana", LATER)
    fresh = build_memo(with_pieces(readout), ROOM, LATER)
    v3 = carry_operator_lines(v2, fresh, LATER)
    ids = [l.id for l in v3.section(7).lines]
    assert ids[ids.index(first) + 1] == "op-2-1"
    assert second not in ids
    assert [l.kind for l in v3.section(15).lines] == ["operator"]
    assert v3.section(7).lines[0].kind == "pieces"  # the rebuild brought the new piece verdicts
    assert v3.version == 3 and v3.changes[-1].author == "Tricorder"
