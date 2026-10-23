"""The claim_support merge step, on readouts the real commands build.

Each room runs the commands a user runs: the red-flag scan, the claims scan,
the memo, then `python -m scans.memo.claim_support` (the step's own command
until merge.py lists it). Only eval reads the answer keys.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from eval.score import score
from schema.check_quotes import check_claim
from schema.claim import Claim, Check, Panel, Readout, Source, Value
from scans.memo import claim_support

ROOT = Path(__file__).resolve().parents[3]
ROOMS = ROOT / "data_room"


def _run(args, out: Path):
    env = dict(os.environ, TRICORDER_OUT_DIR=str(out))
    env.pop("ANTHROPIC_API_KEY", None)
    done = subprocess.run([sys.executable, "-m", *args], cwd=ROOT, env=env, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    return done.stdout


@pytest.fixture(scope="module")
def readouts(tmp_path_factory):
    out = tmp_path_factory.mktemp("cs_out")
    built = {}
    for room in ("hollis_voice", "brasswick", "hollis_voice_clean"):
        path = str(ROOMS / room)
        _run(["scans.redflags", path], out)
        _run(["scans.claims", path], out)
        _run(["scans.memo", path], out)
        printed = json.loads(_run(["scans.memo.claim_support", path], out))
        assert printed["claims_table"]["relabelled by the memo step"] == "yes"
        built[room] = Readout.model_validate_json((out / room / "readout.json").read_text(encoding="utf-8"))
    return built


def rows(readout: Readout) -> list[dict]:
    panel = next(p for p in readout.panels if p.name == "claims table")
    return [dict(zip(panel.columns, r)) for r in panel.rows]


def row_at(readout, where, stated):
    return next(r for r in rows(readout) if r["where"].startswith(where) and r["stated"] == stated)


def claim(readout, cid) -> Claim:
    return next(c for c in readout.claims if c.id == cid)


# Planted entries that another scan's flag settles in the memo step: BF2's flag cites
# the same slide words; PF3's cohort rebuild carries a value the claim's own
# comparison disagrees with (review wave 2a, S6).
MEMO_CONTRADICTIONS = [
    ("brasswick", "BF2", "slide 4", "January 2026 to September 2026", "deck_history_vs_metrics"),
    ("hollis_voice", "PF3", "slide 6", "102.6%", "rebuild_cohorts_from_customer_file"),
]


@pytest.mark.parametrize("room,flag_id,where,stated,check", MEMO_CONTRADICTIONS)
def test_other_scans_flags_relabel_the_pitch_claim(readouts, room, flag_id, where, stated, check):
    name = "answer_key.json" if room == "hollis_voice" else "answer_key_brasswick.json"
    key = {f["id"]: f for f in json.loads((ROOMS / name).read_text())["flags"]}
    assert key[flag_id]["check"] == check
    r = readouts[room]
    row = row_at(r, where, stated)
    assert row["label"] == "contradicted"
    c = claim(r, row["claim id"])
    flag = next(x for x in r.claims if x.id in c.conflicts_with)
    assert flag.check.name == check and flag.scan == "redflags"
    assert c.sources[0].uri == "01_overview/pitch_deck.pdf"           # the pitch side
    assert any(s.uri != "01_overview/pitch_deck.pdf" for s in c.sources)  # the side that disagrees
    assert c.severity == "flag" and c.text.startswith("Contradicted:")
    assert check_claim(c, ROOMS / room)[1] == []


# Flags whose value cannot be set against the pitch figure (another label or unit):
# the row says the check raises a problem, and the label stays (review wave 2a, S6).
NOT_COMPARED = [("slide 4", "$943K", "gross_vs_net_revenue"), ("slide 10", "29", "contractor_spend_vs_headcount_and_burn")]


@pytest.mark.parametrize("where,stated,check", NOT_COMPARED)
def test_a_flag_that_cannot_be_compared_is_named_but_does_not_relabel(readouts, where, stated, check):
    r = readouts["brasswick"]
    row = row_at(r, where, stated)
    assert row["label"] != "contradicted"
    assert f"{check}" in row["disagrees"] and "raises a problem with this figure" in row["disagrees"]
    c = claim(r, row["claim id"])
    assert c.severity == "info" and not c.text.startswith("Contradicted:")


def test_a_shared_export_row_does_not_relabel(readouts):
    # Hollis Voice's mrr_column flag cites monthly_metrics.csv row 22, which the calls figure also cites.
    row = row_at(readouts["hollis_voice"], "slide 3", "72,149")
    assert row["label"] == "supported"


def test_labels_and_counts_stay_in_step(readouts):
    for r in readouts.values():
        table = rows(r)
        counts = dict(next(p for p in r.panels if p.name == "claims table counts").rows)
        for label in ("supported", "contradicted", "unsupported"):
            assert int(counts[label]) == sum(1 for t in table if t["label"] == label)
        by_id = {c.id: c for c in r.claims if c.scan == "claims"}
        for t in table:
            assert (by_id[t["claim id"]].severity == "flag") == (t["label"] == "contradicted")


def test_no_decoy_flagged_and_clean_room_clear(readouts):
    for room in ("hollis_voice", "brasswick", "hollis_voice_clean"):
        name = {"hollis_voice": "answer_key.json", "brasswick": "answer_key_brasswick.json",
                "hollis_voice_clean": "answer_key_clean.json"}[room]
        line, _ = score(readouts[room], json.loads((ROOMS / name).read_text()), room)
        assert line.decoys_flagged == 0, room
    assert [t for t in rows(readouts["hollis_voice_clean"]) if t["label"] == "contradicted"] == []


def test_spoken_entries_score_through_the_claims_scan(readouts):
    for room, name, flag_id in (("hollis_voice", "answer_key.json", "PF2b"), ("brasswick", "answer_key_brasswick.json", "BF5")):
        key = json.loads((ROOMS / name).read_text())
        only = key | {"flags": [f for f in key["flags"] if f["id"] == flag_id]}
        r = readouts[room].model_copy(update={"claims": [c for c in readouts[room].claims if c.scan == "claims"]})
        line, _ = score(r, only, room)
        assert line.found == 1, flag_id


def test_model_only_support_is_said_out_loud(readouts):
    row = row_at(readouts["hollis_voice"], "slide 5", "80%")
    assert row["label"] == "unsupported"
    assert "only a model reading backs this" in row["ask"]
    assert "gross_margin_from_ledger" in row["ask"] and "has not run" in row["ask"]


def test_runway_and_burn_name_the_rebuild_that_has_not_run(readouts):
    """Review wave 2a, S7: an info claim under a settling check's name does not count as
    that rebuild having tested the figure; the note names the checks that have not run."""
    for stated in ("37", "$374,462"):
        row = row_at(readouts["hollis_voice"], "slide 11", stated)
        assert row["label"] == "unsupported"
        assert "payroll_from_hiring_plan_and_rerun_cash" in row["ask"] and "has not run" in row["ask"]
        assert row["ask"].count("has not run") == 1   # the merge and the command both ran the step


def test_the_count_row_is_written_once(readouts):
    """Review wave 2a, O4: the merge runs the step, and so does the command."""
    for r in readouts.values():
        counts = next(p for p in r.panels if p.name == "claims table counts")
        assert [row[0] for row in counts.rows].count("relabelled by the memo step") == 1


def _share(flag_number: float):
    """A deck ceiling of 25% and a top_customer_share flag. HAND-BUILT test data."""
    src = Source(kind="file", uri="01_overview/pitch_deck.pdf", locator="slide 4", quote="No customer above 25% of ARR")
    mine = Claim(id="claims-001", scan="claims", severity="info", confidence="computed",
                 text="Supported: The deck (slide 4) gives largest customer share as at most 25%. Outside the pitch, x agrees.",
                 check=Check(kind="script", name="claim_support"), sources=[src],
                 value=Value(number=25.0, unit="percent", label="largest_customer_share", period="2026-09"))
    flag = Claim(id="redflags-concentration-001", scan="redflags", severity="flag", confidence="computed",
                 text=f"The largest customer is {flag_number}% of MRR in 2026-09, over the 20% line.",
                 check=Check(kind="script", name="top_customer_share"),
                 value=Value(number=flag_number, unit="percent", label="largest_customer_share", period="2026-09"),
                 sources=[Source(kind="file", uri="03_metrics/customer_mrr_by_month.csv", locator="row 1984", quote="x")])
    columns = ["claim id", "label", "where", "quote", "kind", "stated", "normalised", "spoken", "agrees", "disagrees",
               "should be backed by", "ask"]
    table = Panel(name="claims table", columns=columns,
                  rows=[["claims-001", "supported", "slide 4", "No customer above 25% of ARR", "largest customer share",
                         "at most 25%", "largest customer share: at most 25 percent, 2026-09", "", "revenue by customer: 21.0%",
                         "", "", ""]])
    counts = Panel(name="claims table counts", columns=["what", "count"], rows=[["supported", "1"], ["contradicted", "0"]])
    return Readout(room="t", built_at="now", claims=[mine, flag], panels=[table, counts])


def test_a_flag_that_agrees_with_the_ceiling_does_not_relabel():
    """Review wave 2a, S6: 21% is under the deck's 25% ceiling, so the deck is right."""
    out = claim_support.apply(_share(21.0), Path("."))
    assert out.panels[0].rows[0][1] == "supported"
    assert next(c for c in out.claims if c.id == "claims-001").severity == "info"


def test_a_flag_that_breaks_the_ceiling_relabels():
    out = claim_support.apply(_share(31.0), Path("."))
    assert out.panels[0].rows[0][1] == "contradicted"
    mine = next(c for c in out.claims if c.id == "claims-001")
    assert mine.severity == "flag" and mine.conflicts_with == ["redflags-concentration-001"]
    assert "31.0" in mine.text


def test_corroborated_by_names_another_scans_agreeing_claim():
    """Review wave 2a, O1. On the demo rooms no other scan writes a non-flag claim with a
    Value the claims table also holds and no pitch source, so nothing is corroborated
    there; this HAND-BUILT pair shows the rule fires when one exists, and that a claim
    citing the pitch does not count."""
    r = _share(21.0)
    r.claims[1] = r.claims[1].model_copy(update={"severity": "info", "id": "model-001", "scan": "model",
                                                  "value": Value(number=25.1, unit="percent", label="largest_customer_share",
                                                                 period="2026-09")})
    pitchy = r.claims[1].model_copy(update={"id": "model-002", "sources": [r.claims[0].sources[0]]})
    r.claims.append(pitchy)
    out = claim_support.apply(r, Path("."))
    assert next(c for c in out.claims if c.id == "claims-001").corroborated_by == ["model-001"]


def _tiny(table_label="supported"):
    src = Source(kind="file", uri="01_overview/pitch_deck.pdf", locator="slide 3", quote="$2.5M\nARR")
    mine = Claim(id="claims-001", scan="claims", text="Supported: The deck (slide 3) gives ARR as $2.5M. Outside the pitch, x agrees.",
                 severity="info", check=Check(kind="script", name="claim_support"), confidence="computed", sources=[src])
    other = Claim(id="redflags-007", scan="redflags", text="The deck's ARR differs from the P&L.", severity="flag",
                  check=Check(kind="script", name="deck_revenue_vs_pnl"), confidence="computed",
                  sources=[Source(kind="file", uri="01_overview/pitch_deck.pdf", locator="slide 3", quote="$2.5M"),
                           Source(kind="file", uri="02_financials/financial_model.xlsx", locator="P&L!W10", quote="186739")])
    columns = ["claim id", "label", "where", "quote", "kind", "stated", "normalised", "spoken", "agrees", "disagrees",
               "should be backed by", "ask"]
    table = Panel(name="claims table", columns=columns,
                  rows=[["claims-001", table_label, "slide 3", "$2.5M ARR", "ARR", "$2.5M", "", "", "metrics export (row 22): 2,500,000", "", "", ""]])
    counts = Panel(name="claims table counts", columns=["what", "count"], rows=[["supported", "1"], ["contradicted", "0"]])
    return Readout(room="t", built_at="now", claims=[mine, other], panels=[table, counts])


def test_shared_pitch_quote_relabels_with_both_sides():
    out = claim_support.apply(_tiny(), Path("."))
    mine = next(c for c in out.claims if c.id == "claims-001")
    assert mine.severity == "flag" and mine.conflicts_with == ["redflags-007"]
    assert [s.uri for s in mine.sources] == ["01_overview/pitch_deck.pdf", "02_financials/financial_model.xlsx"]
    assert dict(out.panels[1].rows)["contradicted"] == "1"


def test_unverified_reads_could_not_verify():
    r = _tiny()
    r.unverified, r.claims = [r.claims[0]], r.claims[1:]
    out = claim_support.apply(r, Path("."))
    assert out.panels[0].rows[0][1] == "could not verify"


def test_no_table_no_change():
    r = Readout(room="t", built_at="now")
    assert claim_support.apply(r, Path(".")) == r


def test_command_without_a_readout_exits_2(tmp_path):
    env = dict(os.environ, TRICORDER_OUT_DIR=str(tmp_path))
    done = subprocess.run([sys.executable, "-m", "scans.memo.claim_support", str(ROOMS / "brasswick")], cwd=ROOT, env=env,
                          capture_output=True, text=True)
    assert done.returncode == 2 and "no readout" in done.stdout


def test_a_rebuild_flag_from_a_later_check_relabels_the_model_only_figure(readouts):
    """PF6 waits on entry 1.7 (gross_margin_from_ledger), not on main yet. This flag
    claim is HAND-BUILT test data in the shape that entry will write; it cites
    real P&L cells. When it lands, the deck's 80% must read contradicted."""
    r = readouts["hollis_voice"].model_copy(deep=True)
    rebuilt = Claim(id="redflags-900", scan="redflags", severity="flag", confidence="computed",
                    text="Gross margin rebuilt with hosting, inference and support in cost of revenue is 58.1%, not 80%.",
                    check=Check(kind="script", name="gross_margin_from_ledger"),
                    value=Value(number=58.1, unit="percent", label="gross_margin", period=None),
                    sources=[Source(kind="file", uri="02_financials/financial_model.xlsx", locator="GM_PCT", quote="0.8"),
                             Source(kind="file", uri="02_financials/financial_model.xlsx", locator="P&L!A20",
                                    quote="Cloud hosting and model inference")])
    r.claims.append(rebuilt)
    out = claim_support.apply(r, ROOMS / "hollis_voice")
    row = row_at(out, "slide 5", "80%")
    assert row["label"] == "contradicted"
    c = claim(out, row["claim id"])
    assert c.conflicts_with == ["redflags-900"] and c.sources[0].uri == "01_overview/pitch_deck.pdf"
    assert {s.locator for s in c.sources[1:]} == {"GM_PCT", "P&L!A20"}
    assert check_claim(c, ROOMS / "hollis_voice")[1] == []
