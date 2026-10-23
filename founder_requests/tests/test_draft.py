"""Drafting a message from the readout's ask list (FR-R1 to FR-R10), on readouts built by the real commands."""

import re
from pathlib import Path
from urllib.parse import unquote

import pytest

from schema.claim import AskItem, Readout
from founder_requests import draft as d

ROOT = Path(__file__).resolve().parents[2]
BRASSWICK = ROOT / "data_room" / "brasswick"


def test_brasswick_lines_and_default(brasswick):
    items = d.items(brasswick)
    assert [i.number for i in items] == list(range(1, len(brasswick.asks) + 1))
    assert len(items) >= 20
    top = sorted((i for i in items if i.top), key=lambda i: i.top)
    assert [i.top for i in top] == [1, 2, 3, 4, 5]
    assert d.default_selection(items) == [i.number for i in top]
    hiring = next(i for i in items if i.checklist_id == "C22")
    assert hiring.top == 1 and hiring.title == "Hiring plan"
    assert hiring.guidance["form"].startswith("A CSV")
    assert set(hiring.covers) >= {"C22", "C24"}


def test_every_document_line_on_brasswick_carries_guidance(brasswick):
    for i in d.items(brasswick):
        if i.checklist_id and i.checklist_id not in d.OWN_TITLE:
            g = i.guidance
            assert g and g["what"] and g["form"] and g["good"], i.number


def test_no_internal_reference_reaches_the_founder(brasswick, hollis):
    for readout, room in ((brasswick, BRASSWICK), (hollis, ROOT / "data_room" / "hollis_voice")):
        every = [i.number for i in d.items(readout)]
        out = d.draft(readout, every, room_dir=room)
        assert out.leaks == [], out.leaks
        assert d.leaks(out.subject + out.body) == []
        for i in out.items:
            assert re.match(r"(Please|Send|If)\b", i.text), i.text
            assert i.text.endswith((".", "?")), i.text
            assert i.operator_why not in out.body or not i.operator_why


def test_founder_text_strips_locations_and_ids():
    ask = AskItem(what="the option grant records for every holder", why="x (02_financials/cap_table.xlsx, Cap_Table!A7)",
                  piece="the_pitch_itself", from_kind="gap", checklist_id="C78")
    assert d.founder_text(ask) == "Please send the option grant records for every holder."
    ask.what = "the signed SAFE (02_financials/cap_table.xlsx, Cap_Table!A12) per C75 and redflags-004"
    text = d.founder_text(ask)
    assert d.leaks(text) == [] and "cap_table" not in text and text.endswith(".")
    ask.what, ask.checklist_id = "Please send: Property leases.", "C999"
    assert d.founder_text(ask) == "Please send your property leases."


def test_grouping_and_optional_section(brasswick):
    items = d.items(brasswick)
    material = [i.number for i in items if i.guidance and i.guidance["guide"].startswith("material-agreements")]
    required = next(i.number for i in items if i.checklist_id == "C22")
    assert len(material) >= 2
    out = d.draft(brasswick, [*material, required], room_dir=BRASSWICK)
    assert out.body.count("What it is:") == 2
    assert out.body.count("Material agreements") == 1
    assert out.body.index("1. Hiring plan") < out.body.index("If you have them:") < out.body.index("Material agreements")


def test_greeting_and_company_from_the_room(brasswick):
    out = d.draft(brasswick, room_dir=BRASSWICK, sender="Sam")
    assert out.body.startswith("Hi Celia,\n")
    assert out.company == "Brasswick" and out.subject == "Brasswick: documents for our review"
    assert "cover_note_and_index.pdf" in out.read_from and "pitch_deck.pdf" in out.read_from
    assert out.body.rstrip().endswith("Thank you,\nSam")
    plain = d.draft(brasswick, room_dir=None)
    assert plain.body.startswith("Hello,\n") and plain.company == "Brasswick"


def test_mailto_encoding(brasswick):
    out = d.draft(brasswick, [d.items(brasswick)[5].number], room_dir=BRASSWICK, to="celia@example.com")
    assert out.mailto.startswith("mailto:celia@example.com?subject=Brasswick%3A%20one%20document")
    assert "%0D%0A" in out.mailto and "+" not in out.mailto.split("?", 1)[1]
    body = unquote(out.mailto.split("&body=", 1)[1]).replace("\r\n", "\n")
    assert body == out.body
    assert out.mailto_fits == (len(out.mailto) <= d.MAILTO_MAX)
    long = d.draft(brasswick, [i.number for i in d.items(brasswick)], room_dir=BRASSWICK)
    assert long.mailto_fits is False


def test_unknown_line_and_empty_list_are_refused(brasswick):
    with pytest.raises(ValueError, match="no ask line 999"):
        d.draft(brasswick, [999])
    empty = Readout(room="empty", built_at="2026-10-23T00:00:00Z")
    assert d.items(empty) == []
    with pytest.raises(ValueError, match="Nothing to ask for"):
        d.draft(empty)


def test_without_the_coverage_panel_every_required_line_is_the_default(brasswick):
    bare = brasswick.model_copy(deep=True)
    bare.panels = []
    items = d.items(bare)
    assert all(i.top is None for i in items)
    assert d.default_selection(items) == [i.number for i in items if not i.if_you_have_it]
