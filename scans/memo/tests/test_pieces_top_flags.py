"""The shared verdict and headline rules, through the merge-step interface."""

import json
from pathlib import Path

from schema.claim import PIECE_ORDER, Check, Claim, Gap, Readout, Source, Value
from scans.memo import pieces, top_flags


def claim(cid, label="arr", number=100, severity="info", uri="02_financials/model.xlsx",
          conflicts=(), corroborated=(), check="x", scan="redflags", unit="USD", period="2026-09"):
    return Claim(id=cid, scan=scan, text=f"The source states {cid}.", severity=severity,
                 value=Value(number=number, unit=unit, label=label, period=period) if label else None,
                 check=Check(kind="script", name=check), confidence="computed",
                 sources=[Source(kind="file", uri=uri, locator="A1", quote="source words")],
                 conflicts_with=list(conflicts), corroborated_by=list(corroborated))


def build(claims=(), gaps=(), unverified=()):
    readout = Readout(room="t", built_at="now", claims=list(claims), gaps=list(gaps), unverified=list(unverified))
    return top_flags.apply(pieces.apply(readout, Path(".")), Path("."))


def piece(readout, name):
    return next(p for p in readout.pieces if p.name == name)


def test_all_pieces_exist_in_order_even_without_a_scan():
    out = build(gaps=[Gap(what="Not in the room: founder bios", why="missing", would_need="bios", piece="team")])
    assert [p.name for p in out.pieces] == list(PIECE_ORDER)
    assert all(p.verdict == "not_enough_in_the_room" for p in out.pieces)
    assert piece(out, "team").reason == "Not in the room: founder bios"
    assert out.top_flags == []


def test_assignment_uses_scan_then_label_then_entry():
    assert pieces.piece_of(claim("a", "arr", scan="comps")) == "comps"
    assert pieces.piece_of(claim("a", "headcount", scan="signals")) == "market"
    assert pieces.piece_of(claim("a", "nrr_12m")) == "retention"
    assert pieces.piece_of(claim("a", "cash")) == "burn_and_runway"
    assert pieces.piece_of(claim("a", "headcount", check="contractor_spend_vs_headcount_and_burn")) == "team"
    assert pieces.piece_of(claim("a", None, check="deck_revenue_vs_pnl.steer")) == "traction_and_revenue"
    assert pieces.piece_of(claim("a", "other", check="one_time_fees_in_recurring_metrics")) == "traction_and_revenue"
    assert pieces.piece_of(claim("a", "other", check="cancellable_within_notice_vs_arr")) == "traction_and_revenue"
    assert pieces.piece_of(claim("a", None, check="unknown")) == "the_pitch_itself"


def test_verdicts_follow_the_first_matching_rule_and_cite_the_reason():
    claims = [claim("flag", severity="flag"), claim("a", corroborated=["b"]),
              claim("b", uri="03_metrics/metrics.csv", corroborated=["a"]),
              claim("c", "tam", corroborated=["d"]), claim("d", "tam", uri="03_metrics/market.csv", corroborated=["c"]),
              claim("x", "nrr_12m", conflicts=["y"]), claim("y", "nrr_12m", number=90, conflicts=["x"]),
              claim("m", "grr_12m", corroborated=["n"]), claim("n", "grr_12m", uri="03_metrics/retention.csv", corroborated=["m"])]
    out = build(claims)
    assert piece(out, "traction_and_revenue").verdict == "looking_weak"
    assert piece(out, "traction_and_revenue").reason_claim_ids == ["flag"]
    assert piece(out, "market").verdict == "looking_strong"
    assert piece(out, "market").reason_claim_ids == ["c"]
    assert piece(out, "retention").verdict == "mixed"
    assert piece(out, "retention").reason_claim_ids == ["m", "x"]
    assert [f.piece for f in out.top_flags if f.kind == "green"] == ["market"]


def test_repeated_pitch_sources_count_as_one_and_repeated_cells_are_one_file():
    a = claim("a", "tam", uri="01_overview/pitch_deck.pdf", corroborated=["b", "c", "d"])
    b = claim("b", "tam", uri="01_overview/pitch_video_script.md", corroborated=["a"])
    c = claim("c", "tam", uri="02_financials/model.xlsx", corroborated=["a"])
    d = claim("d", "tam", uri="02_financials/model.xlsx", corroborated=["a"])
    out = build([a, b, c, d])
    assert piece(out, "market").corroborating_sources == 2
    assert piece(out, "market").contradicting_sources == 0


def test_unverified_claims_and_dangling_links_do_not_make_a_piece_strong():
    bad = claim("bad", "tam", corroborated=["gone"]).model_copy(update={"confidence": "unverified"})
    out = build([claim("a", "headcount", corroborated=["gone"])], unverified=[bad])
    assert piece(out, "market").claim_ids == []
    assert piece(out, "team").verdict == "not_enough_in_the_room"
    assert out.top_flags == []


def test_reds_rank_by_gap_one_per_piece_and_ties_keep_piece_order():
    out = build([claim("small", number=110, severity="flag", conflicts=["found"]),
                 claim("large", number=150, severity="flag", conflicts=["found"]), claim("found"),
                 claim("runway", "runway_months", number=40, severity="flag", conflicts=["months"]),
                 claim("months", "runway_months", number=20),
                 claim("retention", "nrr_12m", number=150, severity="flag", conflicts=["retained"]),
                 claim("retained", "nrr_12m")])
    assert [(f.piece, f.rank, f.claim_ids) for f in out.top_flags] == [
        ("burn_and_runway", 1, ["runway"]), ("traction_and_revenue", 2, ["large"]), ("retention", 3, ["retention"])]
    assert piece(out, "traction_and_revenue").reason_claim_ids == ["large"]


def test_unrankable_red_flags_stay_in_their_piece():
    out = build([claim("no-value", None, severity="flag"),
                 claim("zero", "cash", number=10, severity="flag", conflicts=["zero-found"]), claim("zero-found", "cash", number=0),
                 claim("units", "tam", severity="flag", conflicts=["wrong-unit"]), claim("wrong-unit", "tam", unit="count"),
                 claim("period", "headcount", severity="flag", conflicts=["old"]), claim("old", "headcount", period="2025-09"),
                 claim("other", "other", severity="flag", conflicts=["other-found"]), claim("other-found", "other", number=5)])
    assert out.top_flags == []
    assert piece(out, "the_pitch_itself").verdict == "looking_weak"


def test_green_ranking_ties_and_settings_limits(tmp_path, monkeypatch):
    a = claim("market", "tam", corroborated=["model"], uri="01_overview/pitch_deck.pdf")
    b = claim("model", "tam", corroborated=["market"])
    c = claim("team", "headcount", corroborated=["staff"], uri="01_overview/pitch_deck.pdf")
    d = claim("staff", "headcount", corroborated=["team"])
    out = build([a, b, c, d, claim("flag", number=150, severity="flag", conflicts=["found"]), claim("found")])
    assert [f.piece for f in out.top_flags if f.kind == "green"] == ["market", "team"]
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({"top_green_flags": 1, "top_red_flags": 0}))
    monkeypatch.setenv("TRICORDER_SETTINGS", str(settings))
    limited = build(out.claims)
    assert [(f.kind, f.piece) for f in limited.top_flags] == [("green", "market")]


def test_reapplying_steps_changes_neither_claims_nor_results():
    original = Readout(room="t", built_at="now", claims=[claim("a", severity="flag", conflicts=["b"]), claim("b", number=80)])
    before = original.model_dump()
    once = top_flags.apply(pieces.apply(original, Path(".")), Path("."))
    twice = top_flags.apply(pieces.apply(once, Path(".")), Path("."))
    assert original.model_dump() == before
    assert twice.model_dump() == once.model_dump()
    assert once.claims == original.claims
