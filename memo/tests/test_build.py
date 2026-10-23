"""The draft memo: sections in the template's order, filled from the readout or naming the gap."""

from __future__ import annotations

from pathlib import Path

from schema.check_quotes import check_claim
from schema.claim import Source

from memo.build import build_memo, claim_section
from memo.template import SECTIONS
from memo.tests.conftest import ROOM

AT = "2026-10-23T12:00:00Z"
TRICORDER_KINDS = {"claim", "reading", "pieces", "coverage", "ask", "source", "gap", "fact", "unverified", "change"}


def test_sixteen_sections_in_the_template_order(readout):
    memo = build_memo(readout, ROOM, AT)
    assert [(s.number, s.title) for s in memo.sections] == [(s.number, s.title) for s in SECTIONS]
    assert [s.title for s in memo.sections][:3] == ["Header", "Summary and the ask", "Company and problem"]


def test_every_section_is_filled_or_names_its_gap(readout):
    memo = build_memo(readout, ROOM, AT)
    for s in memo.sections:
        assert s.lines, s.title
        sourced = [ln for ln in s.lines if ln.kind in ("claim", "reading", "pieces", "ask", "source")]
        slots = [ln for ln in s.lines if ln.kind == "slot"]
        gaps = [ln for ln in s.lines if ln.kind == "gap"]
        if s.number in (13, 15):
            assert slots, s.title  # the operator's sections keep their blank
        elif not sourced and s.number != 1:
            assert gaps and s.empty_because, s.title
            assert all(t.startswith(("Not in the room:", "Not in the readout yet:")) for t in s.empty_because)


def test_hollis_voice_claims_land_in_their_sections(readout):
    memo = build_memo(readout, ROOM, AT)
    where = {cid: s.number for s in memo.sections if s.number in range(3, 12)
             for ln in s.lines if ln.kind == "claim" for cid in ln.claim_ids}
    assert where["redflags-007"] == 7   # deck ARR against the P&L: traction
    assert where["redflags-001"] == 7   # MRR mislabel: label mrr
    assert where["redflags-004"] == 10  # cash bridge: label cash
    assert where["redflags-002"] == 6   # billings against revenue: entry 1.12, business model
    assert set(where) == {c.id for c in readout.claims}


def test_flags_open_the_summary_and_reappear_as_risks(readout):
    memo = build_memo(readout, ROOM, AT)
    flagged = {c.id for c in readout.claims if c.severity == "flag"}
    assert flagged == {"redflags-001", "redflags-007"}
    s2 = {cid for ln in memo.section(2).lines for cid in ln.claim_ids}
    s12 = {cid for ln in memo.section(12).lines if ln.kind == "claim" for cid in ln.claim_ids}
    assert flagged <= s2 and flagged <= s12
    texts = [ln.text for ln in memo.section(2).lines]
    assert "Not in the readout yet: the top green and red flags." in texts


def test_missing_scans_are_named_where_they_belong(readout):
    memo = build_memo(readout, ROOM, AT)
    s8 = " ".join(ln.text for ln in memo.section(8).lines)
    assert "the comps scan's results" in s8
    s9 = " ".join(ln.text for ln in memo.section(9).lines)
    assert "the founders scan's results" in s9
    s4 = " ".join(ln.text for ln in memo.section(4).lines)
    assert "the signals scan's results" in s4 and "the frameworks scan's results" in s4


def test_room_gaps_sit_in_their_section_and_link_the_ask_list(readout):
    memo = build_memo(readout, ROOM, AT)
    s10 = [ln for ln in memo.section(10).lines if ln.text == "Not in the room: a balance sheet"]
    assert s10 and s10[0].kind == "gap" and s10[0].ask_ids
    ask = memo.asks[s10[0].ask_ids[0]]
    assert ask.what == "monthly balance sheets"
    assert "C20" in s10[0].checklist_ids


def test_sections_close_with_their_coverage(readout):
    memo = build_memo(readout, ROOM, AT)
    for n in range(3, 12):
        last = memo.section(n).lines[-1]
        assert last.kind == "coverage", n
        assert all(memo.checklist[c].id == c for c in last.checklist_ids)
    s7 = memo.section(7).lines[-1]
    assert s7.text.startswith("At Series A, this section's 30 checklist items")


def test_section_14_holds_coverage_every_ask_and_the_box(readout):
    memo = build_memo(readout, ROOM, AT)
    lines = memo.section(14).lines
    asks = [ln for ln in lines if ln.kind == "ask"]
    assert len(asks) == len(readout.asks) == 27
    assert lines[0].text.startswith("At Series A, 193 checklist items: 13 checked, 15 found, 45 missing")
    assert lines[-1].label == "Could not verify"


def test_operator_sections_stay_the_operators(readout):
    memo = build_memo(readout, ROOM, AT)
    assert [ln.kind for ln in memo.section(15).lines] == ["slot"]
    s13 = memo.section(13)
    assert s13.lines[0].kind == "slot"
    assert all(ln.kind in ("slot", "gap", "claim") for ln in s13.lines)
    assert any(ln.id == "s02-recommendation" and ln.kind == "slot" for ln in memo.section(2).lines)
    words = " ".join(ln.text.lower() for s in memo.sections for ln in s.lines if ln.kind != "slot")
    for banned in (" invest ", " pass ", "strong buy", "fraud", "likely", "probably", "appears to"):
        assert banned not in f" {words} ", banned


def test_every_cited_claim_is_in_the_memo_and_passes_the_quote_checker(readout):
    memo = build_memo(readout, ROOM, AT)
    cited = {cid for s in memo.sections for ln in s.lines for cid in ln.claim_ids}
    assert cited and cited <= set(memo.claims)
    for claim in memo.claims.values():
        _, problems = check_claim(claim, ROOM)
        assert not problems, claim.id


def test_a_claim_that_fails_the_quote_checker_moves_to_the_box(readout):
    bad = readout.claims[6]
    readout.claims[6] = bad.model_copy(update={"sources": [Source(kind="file", uri=bad.sources[0].uri, locator=bad.sources[0].locator,
                                                                  quote="a sentence that is not on this slide")]})
    memo = build_memo(readout, ROOM, AT)
    assert bad.id not in memo.claims
    assert all(bad.id not in ln.claim_ids for s in memo.sections for ln in s.lines)
    box = [ln for ln in memo.section(14).lines if ln.kind == "unverified"]
    assert [ln.id for ln in box] == [f"s14-unverified-{bad.id}"]


def test_sources_text_is_read_for_every_cited_source(readout):
    memo = build_memo(readout, ROOM, AT)
    for c in memo.claims.values():
        for s in c.sources:
            st = memo.sources[f"{s.uri}|{s.locator}"]
            assert st.found, st.key


def test_section_16_lists_every_cited_source_once(readout):
    memo = build_memo(readout, ROOM, AT)
    src_lines = [ln for ln in memo.section(16).lines if ln.kind == "source"]
    keys = {f"{s.uri}|{s.locator}" for c in memo.claims.values() for s in c.sources}
    assert len(src_lines) == len(keys)


def test_with_pieces_and_flags_the_summary_and_openers_fill(full_readout):
    memo = build_memo(full_readout, ROOM, AT)
    s2 = memo.section(2).lines
    flags = [ln for ln in s2 if ln.severity in ("green", "red") and ln.kind == "claim"]
    assert [ln.severity for ln in flags] == ["green", "red"]  # green first
    assert len([ln for ln in s2 if ln.id.startswith("s02-piece-")]) == 3
    opener = memo.section(7).lines[0]
    assert opener.kind == "pieces" and opener.text.startswith("Traction and revenue, looking weak (1 corroborate, 1 contradict)")
    # Linked claims are carried so the second click can open them.
    assert "redflags-009" in memo.claims and memo.claims["redflags-008"].corroborated_by == ["redflags-009"]
    assert any(ln.id == "s12-piece-burn_and_runway" for ln in memo.section(12).lines)


def test_routing_prefers_the_piece(full_readout):
    claim = next(c for c in full_readout.claims if c.id == "redflags-003")
    piece_of = {cid: p.name for p in full_readout.pieces for cid in p.claim_ids}
    assert claim_section(claim, piece_of) == 10
    assert claim_section(claim, {}) == 6


def test_a_bare_readout_still_builds(tmp_path):
    from schema.claim import Readout
    memo = build_memo(Readout(room="empty_room", built_at=AT), tmp_path, AT)
    assert len(memo.sections) == 16
    assert all(s.lines for s in memo.sections)
    assert memo.company == "Empty Room"


def test_room_path_can_be_relative(readout, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[2])
    memo = build_memo(readout, "data_room/hollis_voice", AT)
    assert memo.claims
