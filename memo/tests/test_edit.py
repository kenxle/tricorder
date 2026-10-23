"""Operator edits make numbered versions; the operator's words are marked as theirs."""

from __future__ import annotations

import pytest

from memo import store
from memo.build import build_memo
from memo.edit import EditError, apply_edits, carry_operator_lines
from memo.model import Edit
from memo.tests.conftest import ROOM, with_pieces

AT = "2026-10-23T12:00:00Z"
LATER = "2026-10-23T13:00:00Z"


def test_an_operator_line_is_marked_as_theirs(readout):
    v1 = build_memo(readout, ROOM, AT)
    v2 = apply_edits(v1, [Edit(action="add", section=9, text="I met both founders; they have worked together since 2019.")], "Dana", LATER)
    ids = [l.id for l in v2.section(9).lines]
    assert ids[-2:] == ["op-2-1", "s09-coverage"]  # above the section's closing coverage line
    ln = v2.section(9).lines[-2]
    assert (ln.kind, ln.author, ln.version, ln.claim_ids) == ("operator", "Dana", 2, [])
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
    v2 = apply_edits(v1, [Edit(action="add", section=7, text="ARR is stated as $2.5M on the deck.", claim_ids=["redflags-007"])], "Dana", LATER)
    ln = v2.section(7).lines[-2]
    assert ln.claim_ids == ["redflags-007"] and ln.unsourced_numbers == []
    with pytest.raises(EditError, match="no claim"):
        apply_edits(v1, [Edit(action="add", section=7, text="x", claim_ids=["nope-001"])], "Dana", LATER)


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
    v2 = apply_edits(v1, [Edit(action="remove", line_id="s07-redflags-010")], "Dana", LATER)
    v3 = apply_edits(v2, [Edit(action="add", section=12, text="Ask about the pilot first.")], "Sam", LATER)
    changes = [ln for ln in v3.section(16).lines if ln.kind == "change"]
    assert [ln.label for ln in changes] == ["Version 1", "Version 2", "Version 3"]
    assert "Removed Tricorder's line s07-redflags-010 from section 7" in changes[1].text and "Dana" in changes[1].text
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
    v2 = apply_edits(v1, [Edit(action="add", section=7, line_id="s07-redflags-007", text="The founder says the pilot will convert."),
                          Edit(action="remove", line_id="s07-redflags-010"),
                          Edit(action="replace", line_id="s15-recommendation", text="Wait.")], "Dana", LATER)
    fresh = build_memo(with_pieces(readout), ROOM, LATER)
    v3 = carry_operator_lines(v2, fresh, LATER)
    ids = [l.id for l in v3.section(7).lines]
    assert ids[ids.index("s07-redflags-007") + 1] == "op-2-1"
    assert "s07-redflags-010" not in ids
    assert [l.kind for l in v3.section(15).lines] == ["operator"]
    assert v3.section(7).lines[0].kind == "pieces"  # the rebuild brought the new piece verdicts
    assert v3.version == 3 and v3.changes[-1].author == "Tricorder"
