"""The draft memo: sections in the template's order, filled from the readout or naming the gap.

Every expectation here is derived from the readout the scans built: claims are
found by the check that wrote them or by their severity, and counts come from
the readout. A new check in scans/ adds claims; it never breaks these tests.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from schema.check_quotes import check_claim
from schema.claim import Source

from memo.build import build_memo, claim_section, partner_text
from memo.html import visible
from memo.template import SECTIONS
from memo.tests.conftest import ROOM, by_check, flagged

AT = "2026-10-23T12:00:00Z"
PLUMBING = re.compile(r"redflags-\d|(?<![!\w])C\d\d\b|python -m|scans/|\.py\b|Who writes|not built|[Vv]erifier|_vs_")


def partner_lines(memo):
    return [(s, ln) for s in memo.sections for ln in visible(s, "partner")]


def test_sixteen_sections_in_the_template_order(readout):
    memo = build_memo(readout, ROOM, AT)
    assert [(s.number, s.title) for s in memo.sections] == [(s.number, s.title) for s in SECTIONS]
    assert [s.title for s in memo.sections][:3] == ["Header", "Summary and the ask", "Company and problem"]


def test_every_section_is_filled_or_names_its_gap(readout):
    memo = build_memo(readout, ROOM, AT)
    for s in memo.sections:
        assert s.lines, s.title
        sourced = [ln for ln in s.lines if ln.kind in ("claim", "reading", "pieces", "ask", "source", "ref")]
        if s.number in (13, 15):
            assert any(ln.kind == "slot" for ln in s.lines), s.title  # the operator's sections keep their blank
        elif not sourced and s.number != 1:
            assert any(ln.kind == "gap" for ln in s.lines) and s.empty_because, s.title


def test_every_claim_lands_in_one_body_section(readout):
    memo = build_memo(readout, ROOM, AT)
    where: dict[str, set[int]] = {}
    for s in memo.sections:
        if s.number in range(3, 12):
            for ln in s.lines:
                if ln.kind in ("claim", "ref"):
                    for cid in ln.claim_ids:
                        where.setdefault(cid, set()).add(s.number)
    assert set(where) >= {c.id for c in readout.claims}
    cash = by_check(readout, "capitalised_spend_vs_pnl_and_cash")[0]
    billings = by_check(readout, "billings_vs_recognised_revenue")[0]
    assert where[cash] == {10}       # label cash
    assert where[billings] == {6}    # entry 1.12, business model
    for cid in by_check(readout, "deck_revenue_vs_pnl"):
        assert where[cid] == {7}     # traction


def test_flags_open_the_summary_in_full_once_and_are_referred_to_elsewhere(readout):
    memo = build_memo(readout, ROOM, AT)
    flags = flagged(readout)
    assert flags
    s2 = [ln for ln in memo.section(2).lines if ln.severity == "red"]
    assert {cid for ln in s2 for cid in ln.claim_ids} >= set(flags)
    assert [ln.label.split(":")[0] for ln in s2] == [f"Red flag {i}" for i in range(1, len(s2) + 1)]
    # A flag's own words print once in the memo. Sections 7 and 12 point back to it.
    for cid in flags:
        words = partner_text(readout_claim(readout, cid).text)
        holders = [ln.id for _, ln in partner_lines(memo) if words in ln.text]
        if not holders:  # an ARR figure the side-by-side line states instead of its sentence
            composed = [ln for ln in s2 if ln.composed]
            assert composed and cid in composed[0].claim_ids, cid
            continue
        assert len(holders) == 1 and holders[0].startswith("s02-"), (cid, holders)
    s12_refs = [ln for ln in memo.section(12).lines if ln.kind == "ref"]
    assert len(s12_refs) == len(s2)
    assert all("Shown in full in the summary" in ln.text for ln in s12_refs)
    s7_ref_ids = {cid for ln in memo.section(7).lines if ln.kind == "ref" for cid in ln.claim_ids}
    s7_flags = {cid for cid in flags if claim_section(readout_claim(readout, cid), {}) == 7}
    assert s7_flags <= s7_ref_ids


def readout_claim(readout, cid):
    return next(c for c in readout.claims if c.id == cid)


def test_the_arr_figures_sit_side_by_side_from_claims_only(readout):
    memo = build_memo(readout, ROOM, AT)
    line = memo.line("s02-flag-arr")[1]
    assert line and line.composed and line.label == "Red flag 1: ARR figures in the room disagree"
    deck_arr = by_check(readout, "deck_revenue_vs_pnl", "flag")[0]
    assert deck_arr in line.claim_ids and set(line.claim_ids) <= set(memo.claims)
    # Every figure in the side-by-side sentence is in a cited claim's text or its sources' readings.
    side = line.text.split("side by side:", 1)[1].split(").", 1)[0]
    backing = " ".join([memo.claims[c].text for c in line.claim_ids]
                       + [memo.sources[f"{s.uri}|{s.locator}"].reads_as for c in line.claim_ids for s in memo.claims[c].sources])
    figures = re.findall(r"\$[\d,]+(?:\.\d+)?", side)
    assert len(figures) >= 2
    for f in figures:
        assert f in backing, f


def test_the_partner_view_holds_no_plumbing(readout):
    memo = build_memo(readout, ROOM, AT)
    for s, ln in partner_lines(memo):
        assert ln.kind != "slot", ln.id
        assert not PLUMBING.search(f"{ln.label or ''} {ln.text}"), (ln.id, ln.text)


def test_a_section_with_nothing_in_it_is_one_line(readout):
    memo = build_memo(readout, ROOM, AT)
    collapsed = [s for s in memo.sections if s.collapsed]
    assert collapsed
    for s in collapsed:
        lines = visible(s, "partner")
        assert len(lines) == 1, s.title
        assert re.fullmatch(rf"{re.escape(s.title)}: not assessed yet\. Needs the .+ scans?\.", lines[0].text), lines[0].text
    for s in memo.sections:
        if s.number in range(3, 12) and not s.collapsed:
            assert any(ln.kind in ("claim", "ref", "gap", "pieces") and not ln.id.endswith("-needs") for ln in s.lines), s.title


def test_not_assessed_is_said_once_and_no_gap_repeats_in_a_section(readout):
    memo = build_memo(readout, ROOM, AT)
    s2 = [ln for ln in memo.section(2).lines if ln.kind == "gap" and ln.id.startswith("s02-piece")]
    assert [ln.id for ln in s2] == ["s02-pieces-unassessed"]
    assert s2[0].text.count(",") >= 1  # every unassessed piece is named in that one line
    for s in memo.sections:
        texts = [ln.text for ln in visible(s, "partner") if ln.kind == "gap"]
        assert len(texts) == len(set(texts)), s.title


def test_room_gaps_sit_in_their_section_and_link_the_ask_list(readout):
    memo = build_memo(readout, ROOM, AT)
    s10 = [ln for ln in memo.section(10).lines if ln.text == "Not in the room: a balance sheet"]
    assert s10 and s10[0].kind == "gap" and s10[0].ask_ids
    assert memo.asks[s10[0].ask_ids[0]].what == "monthly balance sheets"
    assert s10[0].checklist_ids


def test_gaps_that_differ_only_in_their_subject_share_a_line(readout):
    memo = build_memo(readout, ROOM, AT)
    safes = [g for g in readout.gaps if g.what.startswith("Not in the room: the signed SAFE for ")]
    if len(safes) > 1:
        lines = [ln for ln in memo.section(11).lines if "signed SAFE" in ln.text]
        assert len(lines) == 1 and f"for each of these {len(safes)}:" in lines[0].text


def test_body_sections_close_with_their_coverage(readout):
    memo = build_memo(readout, ROOM, AT)
    for n in range(3, 12):
        last = memo.section(n).lines[-1]
        assert last.kind == "coverage", n
        assert all(memo.checklist[c].id == c for c in last.checklist_ids)
        n_items = len(last.checklist_ids)
        assert last.text.startswith(f"At Series A, this section's {n_items} checklist items")


def test_section_14_holds_coverage_the_ask_list_and_the_box(readout):
    memo = build_memo(readout, ROOM, AT)
    lines = memo.section(14).lines
    asks = [ln for ln in lines if ln.kind == "ask" and ln.id != "s14-asks"]
    assert len(asks) == len(readout.asks) and all(ln.audience == "operator" for ln in asks)
    summary = memo.line("s14-asks")[1]
    assert summary.audience == "page" and summary.text.startswith(f"{len(readout.asks)} requests")
    c = Counter(r.status for r in memo.checklist.values())
    assert lines[0].text.startswith(f"At Series A, {len(memo.checklist)} checklist items: {c['checked']} checked, "
                                    f"{c['found']} found, {c['missing']} missing")
    assert lines[-1].label == "Could not verify"


def test_operator_sections_stay_the_operators(readout):
    memo = build_memo(readout, ROOM, AT)
    assert [ln.kind for ln in memo.section(15).lines] == ["slot"]
    assert memo.section(15).lines[0].audience == "operator"
    s13 = memo.section(13)
    assert s13.lines[0].kind == "slot"
    assert all(ln.kind in ("slot", "gap", "claim") for ln in s13.lines)
    words = " ".join(ln.text.lower() for s in memo.sections for ln in s.lines if ln.kind != "slot")
    for banned in (" invest ", " pass ", "strong buy", "fraud", "likely", "probably", "appears to"):
        assert banned not in f" {words} ", banned


def test_every_cited_claim_is_in_the_memo_and_passes_the_quote_checker(readout):
    memo = build_memo(readout, ROOM, AT)
    cited = {cid for s in memo.sections for ln in s.lines for cid in ln.claim_ids}
    assert cited and cited <= set(memo.claims)
    assert set(memo.claims) == {c.id for c in readout.claims}
    for claim in memo.claims.values():
        _, problems = check_claim(claim, ROOM)
        assert not problems, claim.id


def test_a_claim_that_fails_the_quote_checker_moves_to_the_box(readout):
    i = next(i for i, c in enumerate(readout.claims) if c.severity == "info")
    bad = readout.claims[i]
    readout.claims[i] = bad.model_copy(update={"sources": [Source(kind="file", uri=bad.sources[0].uri, locator=bad.sources[0].locator,
                                                                  quote="a sentence that is not on this slide")]})
    memo = build_memo(readout, ROOM, AT)
    assert bad.id not in memo.claims
    assert all(bad.id not in ln.claim_ids for s in memo.sections for ln in s.lines)
    box = [ln for ln in memo.section(14).lines if ln.kind == "unverified"]
    assert [ln.id for ln in box] == [f"s14-unverified-{bad.id}"]


def test_sources_are_read_and_read_as_a_partner_reads_them(readout):
    memo = build_memo(readout, ROOM, AT)
    for c in memo.claims.values():
        for s in c.sources:
            st = memo.sources[f"{s.uri}|{s.locator}"]
            assert st.found and st.reads_as, st.key
            assert not re.search(r"\d\.\d{3,}", st.reads_as), st.reads_as  # no -0.24000000022351742
    csv_row = next(st for st in memo.sources.values() if st.key.endswith("monthly_metrics.csv|row 22"))
    assert csv_row.reads_as.startswith("month 2026-09, mrr $") and ", arr $" in csv_row.reads_as
    bridge = next((st for st in memo.sources.values() if "Cash_Bridge!" in st.key), None)
    if bridge:
        assert bridge.reads_as.startswith("Cash_Bridge, Difference")


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
    assert len([ln for ln in s2 if ln.id.startswith("s02-piece-")]) == len(full_readout.pieces)
    assert memo.line("s02-pieces-unassessed")[1].label == "Verdicts not in yet"
    opener = memo.section(7).lines[0]
    assert opener.kind == "pieces" and opener.text.startswith("Traction and revenue, looking weak (1 corroborate, 1 contradict)")
    chart = full_readout.top_flags[0].claim_ids[0]
    assert memo.claims[chart].corroborated_by  # linked claims ride along for the second click
    assert any(ln.id == "s12-piece-burn_and_runway" for ln in memo.section(12).lines)


def test_routing_prefers_the_piece(full_readout):
    contractors = by_check(full_readout, "contractor_spend_vs_headcount_and_burn")[0]
    claim = readout_claim(full_readout, contractors)
    piece_of = {cid: p.name for p in full_readout.pieces for cid in p.claim_ids}
    assert piece_of[contractors] == "burn_and_runway"
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
