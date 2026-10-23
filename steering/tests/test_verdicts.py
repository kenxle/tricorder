"""Steering's copy of FRAMEWORKS "Piece verdicts" and "Top green and red flags"
(STEER-R11), used until scans/memo/pieces.py and top_flags.py exist."""

from __future__ import annotations

from pathlib import Path

from schema.claim import Check, Claim, Gap, Readout, Source, Value
from steering import verdicts


def claim(cid, label=None, number=1.0, severity="info", uri="02_financials/financial_model.xlsx", check="x",
          conflicts=(), corroborated=(), scan="redflags"):
    return Claim(id=cid, scan=scan, text=f"claim {cid}", severity=severity,
                 value=Value(number=number, unit="percent", label=label) if label else None,
                 check=Check(kind="script", name=check), confidence="computed",
                 sources=[Source(kind="file", uri=uri, locator="A1", quote="q")],
                 conflicts_with=list(conflicts), corroborated_by=list(corroborated))


def piece(readout, name):
    return next(p for p in readout.pieces if p.name == name)


def build(claims, gaps=()):
    r = Readout(room="t", built_at="now", claims=claims, gaps=list(gaps))
    out, by = verdicts.rebuild(r, Path("."))
    return out, by


def test_piece_of_follows_the_label_table_then_the_check_table():
    assert verdicts.piece_of(claim("a", "nrr_12m")) == "retention"
    assert verdicts.piece_of(claim("a", "arr")) == "traction_and_revenue"
    assert verdicts.piece_of(claim("a", "cash")) == "burn_and_runway"
    assert verdicts.piece_of(claim("a", "other", check="one_time_fees_in_recurring_metrics")) == "traction_and_revenue"
    assert verdicts.piece_of(claim("a", None, check="deck_revenue_vs_pnl")) == "traction_and_revenue"
    assert verdicts.piece_of(claim("a", None, check="contractor_spend_vs_headcount_and_burn")) == "burn_and_runway"
    assert verdicts.piece_of(claim("a", None, check="deck_revenue_vs_pnl.steer")) == "traction_and_revenue"
    assert verdicts.piece_of(claim("a", None, check="unknown")) == "the_pitch_itself"
    assert verdicts.piece_of(claim("a", "arr", scan="comps")) == "comps"


def test_flag_makes_a_piece_weak_even_with_a_corroborated_claim():
    out, by = build([claim("a", "arr", severity="flag"), claim("b", "mrr", corroborated=["c"])])
    p = piece(out, "traction_and_revenue")
    assert p.verdict == "looking_weak" and p.reason == "claim a" and p.reason_claim_ids == ["a"]
    assert by == "steering"


def test_mixed_strong_and_not_enough():
    out, _ = build([claim("a", "nrr_12m", conflicts=["z"]), claim("b", "grr_12m", corroborated=["y"]),
                    claim("c", "tam", corroborated=["d"], uri="01_overview/pitch_deck.pdf"),
                    claim("d", "tam", corroborated=["c"])],
                   [Gap(what="Not in the room: x", why="w", would_need="n", piece="team")])
    assert piece(out, "retention").verdict == "mixed"
    assert piece(out, "market").verdict == "looking_strong"
    assert piece(out, "market").corroborating_sources == 2
    team = piece(out, "team")
    assert team.verdict == "not_enough_in_the_room" and team.reason == "Not in the room: x"
    assert len(out.pieces) == 9


def test_weak_reason_is_the_flag_with_the_largest_gap():
    found1 = claim("f1", "arr", number=100.0)
    found1 = found1.model_copy(update={"severity": "info"})
    found2 = claim("f2", "mrr", number=100.0)
    small = claim("s", "arr", number=110.0, severity="flag", conflicts=["f1"])
    big = claim("b", "mrr", number=150.0, severity="flag", conflicts=["f2"])
    out, _ = build([found1, found2, small, big])
    assert piece(out, "traction_and_revenue").reason_claim_ids == ["b"]
    reds = [f for f in out.top_flags if f.kind == "red"]
    assert reds[0].claim_ids == ["b"] and reds[0].piece == "traction_and_revenue"


def test_top_flags_one_per_piece_greens_only_from_strong_pieces():
    out, _ = build([claim("a", "arr", severity="flag"), claim("b", "nrr_12m", severity="flag"),
                    claim("c", "tam", corroborated=["d"], uri="01_overview/pitch_deck.pdf"), claim("d", "tam", corroborated=["c"])])
    greens = [f for f in out.top_flags if f.kind == "green"]
    reds = [f for f in out.top_flags if f.kind == "red"]
    assert [g.piece for g in greens] == ["market"]
    assert sorted(r.piece for r in reds) == ["retention", "traction_and_revenue"]
    assert [r.rank for r in reds] == [1, 2]
