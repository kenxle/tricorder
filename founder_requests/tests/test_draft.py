"""Drafting a message from the readout's ask list (FR-R1 to FR-R10, FR-R22 to FR-R28), on readouts
built by the real commands."""

import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote

import pytest

from schema.claim import AskItem, Readout
from founder_requests import draft as d

ROOT = Path(__file__).resolve().parents[2]
BRASSWICK = ROOT / "data_room" / "brasswick"
HOLLIS = ROOT / "data_room" / "hollis_voice"


def _by_id(items, cid):
    return next(i for i in items if cid in i.covers or i.checklist_id == cid)


def test_brasswick_lines_and_default(brasswick):
    items = d.items(brasswick, BRASSWICK)
    top = sorted((i for i in items if i.top), key=lambda i: i.top)
    assert [i.top for i in top] == [1, 2, 3, 4, 5]
    assert d.default_selection(items) == [i.number for i in top]
    hiring = _by_id(items, "C22")
    assert hiring.title == "Hiring plan" and hiring.guidance["form"].startswith("A CSV")
    assert set(hiring.covers) >= {"C22", "C24"}


def test_top_five_puts_what_settles_the_decision_first(brasswick):
    """FR-R26: traction, retention and burn first; closing paperwork never in the five."""
    items = d.items(brasswick, BRASSWICK)
    five = {c for i in items if i.top for c in i.covers}
    assert {"C03", "C14", "C20"} <= five
    assert not five & {"C63", "C74", "C76", "C77"}
    pieces = [i.piece for i in sorted((i for i in items if i.top), key=lambda i: i.top)]
    weight = [d.PIECE_WEIGHT.index(p) for p in pieces]
    assert weight == sorted(weight)


def test_closing_paperwork_waits_for_the_term_sheet_at_seed(brasswick):
    """FR-R24: formation, IP assignments and minutes are asked after the term sheet at seed."""
    items = d.items(brasswick, BRASSWICK)
    for cid in ("C74", "C76", "C77"):
        it = _by_id(items, cid)
        assert it.ask_stage == "after_term_sheet" and it.top is None, cid


def test_never_ask_for_a_file_the_room_holds(brasswick):
    """FR-R22: lines are reworded to what is still missing."""
    items = d.items(brasswick, BRASSWICK)
    text = " ".join(i.text for i in items)
    assert "Send monthly revenue by customer" not in text
    revenue = next(i for i in items if i.number == 1)
    assert revenue.text.startswith("Please add the kind of revenue") and "03_metrics/revenue_by_customer.csv" in revenue.in_room
    assert revenue.includes is None  # a file they already sent needs no "Ideally it includes" line
    cohort = _by_id(items, "C14")
    assert cohort.text == "Please send the cohort export behind the deck's retention figure, with a one-line definition of a cohort."
    material = _by_id(items, "C111")
    assert "beyond the Norrgate Software Studio statement of work already in the room" in material.text


def test_a_document_the_room_holds_by_name_is_not_asked(brasswick):
    bare = brasswick.model_copy(deep=True)
    bare.asks.append(AskItem(what="Please send the hiring plan.", why="x", piece="burn_and_runway",
                             from_kind="checklist", checklist_id="C22"))
    items, held = d.analyse(bare, HOLLIS)  # Hollis Voice holds 05_team/hiring_plan.csv
    assert not any(i.number == len(bare.asks) for i in items)
    assert held[-1].files == ["05_team/hiring_plan.csv"]


def test_lines_for_the_same_papers_become_one(brasswick):
    """FR-R23: material agreements, equity records and references each become one item."""
    items = d.items(brasswick, BRASSWICK)
    for ids, title in ((("C98", "C99", "C100", "C110", "C111"), "Material agreements"),
                       (("C73", "C78"), "Option grants and 409A"),
                       (("C35", "C58", "C97"), "People we can call")):
        holders = {id(_by_id(items, c)) for c in ids}
        assert len(holders) == 1, ids
        assert _by_id(items, ids[0]).title == title
    assert len({i.number for i in items}) == len(items)
    assert sum(len(i.lines) for i in items) + len(d.held_lines(brasswick, BRASSWICK)) == len(brasswick.asks)


def test_operator_view_has_no_check_codes(brasswick):
    for i in d.items(brasswick, BRASSWICK):
        assert not re.search(r"\bC\d{1,3}\b", i.operator_why), i.operator_why


def test_no_internal_reference_reaches_the_founder(brasswick, hollis):
    for readout, room in ((brasswick, BRASSWICK), (hollis, HOLLIS)):
        every = [i.number for i in d.items(readout, room)]
        out = d.draft(readout, every, room_dir=room)
        assert out.leaks == [] and d.leaks(out.subject + out.body) == []
        for i in out.items:
            assert re.match(r"(Please|Send|If)\b", i.text), i.text
            assert i.text.endswith((".", "?")), i.text


def test_founder_text_strips_locations_and_ids():
    ask = AskItem(what="the option grant records for every holder", why="x (02_financials/cap_table.xlsx, Cap_Table!A7)",
                  piece="the_pitch_itself", from_kind="gap", checklist_id="C78")
    assert d.founder_text(ask) == "Please send the option grant records for every holder."
    ask.what = "the signed SAFE (02_financials/cap_table.xlsx, Cap_Table!A12) per C75 and redflags-004"
    text = d.founder_text(ask)
    assert d.leaks(text) == [] and "cap_table" not in text and text.endswith(".")
    ask.what, ask.checklist_id = "Please send: Property leases.", "C999"
    assert d.founder_text(ask) == "Please send your property leases."


def test_the_email_is_short_and_warm(brasswick):
    """FR-R27: one line per item plus one "Ideally it includes" line, a date with a reason, a sign-off."""
    out = d.draft(brasswick, room_dir=BRASSWICK, to="celia@example.com", sender="Sam Ortiz",
                  fund="Ridgeline Ventures", by=date(2026, 10, 30))
    assert out.subject == "Brasswick: a few things before our next meeting"
    assert out.body.startswith("Hi Celia,\n")
    assert "by Friday 30 October" in out.body and "before our partner meeting" in out.body
    assert out.body.rstrip().endswith("Thanks,\nSam Ortiz\nRidgeline Ventures")
    for gone in ("What it is:", "Best form:", "A good one shows", "term sheet for this round"):
        assert gone not in out.body
    assert out.body.count("Ideally it includes") == 4  # not for the revenue file they already sent
    assert out.mailto_fits, len(out.mailto)
    assert out.by == "2026-10-30"


def test_one_item_and_the_default_date(brasswick, monkeypatch):
    monkeypatch.setenv("TRICORDER_OPERATOR_NAME", "Sam")
    monkeypatch.setenv("TRICORDER_FUND_NAME", "Ridgeline")
    hiring = _by_id(d.items(brasswick, BRASSWICK), "C22")
    out = d.draft(brasswick, [hiring.number], room_dir=BRASSWICK)
    assert out.subject == "Brasswick: one thing before our next meeting"
    assert out.by == d.default_by().isoformat() and out.body.rstrip().endswith("Sam\nRidgeline")
    plain = d.draft(brasswick, [hiring.number], room_dir=None, sender="", fund="")
    assert plain.body.startswith("Hello,\n") and plain.body.rstrip().endswith("Thanks,")


def test_grouping_and_optional_section(brasswick):
    items = d.items(brasswick, BRASSWICK)
    hiring, material = _by_id(items, "C22"), _by_id(items, "C98")
    out = d.draft(brasswick, [material.number, hiring.number], room_dir=BRASSWICK)
    assert out.body.index("Please send your hiring plan") < out.body.index("If you have them:") < out.body.index("agreements over $25,000")


def test_mailto_encoding(brasswick):
    hiring = _by_id(d.items(brasswick, BRASSWICK), "C22")
    out = d.draft(brasswick, [hiring.number], room_dir=BRASSWICK, to="celia@example.com")
    assert out.mailto.startswith("mailto:celia@example.com?subject=Brasswick%3A%20one%20thing")
    assert "%0D%0A" in out.mailto and "+" not in out.mailto.split("?", 1)[1]
    assert unquote(out.mailto.split("&body=", 1)[1]).replace("\r\n", "\n") == out.body
    long = d.draft(brasswick, [i.number for i in d.items(brasswick, BRASSWICK)], room_dir=BRASSWICK)
    assert long.mailto_fits is False


def test_unknown_line_and_empty_list_are_refused(brasswick):
    with pytest.raises(ValueError, match="no ask line 999"):
        d.draft(brasswick, [999])
    empty = Readout(room="empty", built_at="2026-10-23T00:00:00Z")
    assert d.items(empty) == []
    with pytest.raises(ValueError, match="Nothing to ask for"):
        d.draft(empty)


def test_a_merged_line_number_drafts_its_item(brasswick):
    material = _by_id(d.items(brasswick, BRASSWICK), "C98")
    later = material.lines[-1]
    out = d.draft(brasswick, [later], room_dir=BRASSWICK)
    assert len(out.items) == 1 and out.items[0].title == "Material agreements"


def test_a_merged_item_lists_each_request_a_reply_can_answer(brasswick):
    people = next(i for i in d.items(brasswick, BRASSWICK) if i.title == "People we can call")
    ids = [r["checklist_id"] for r in people.requests]
    assert ids[0] == "C35" and "C97" in ids and len(ids) == len(set(ids)) == len(people.lines)
    names = {r["checklist_id"]: r["name"] for r in people.requests}
    assert names["C97"].startswith("Reference list") and not any("C" + "9" in n for n in names.values())
    hiring = _by_id(d.items(brasswick, BRASSWICK), "C22")
    assert hiring.requests == [{"checklist_id": "C22", "name": "Hiring plan and future org"}]
