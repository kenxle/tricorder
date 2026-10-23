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
from schema.claim import Claim, Check, Panel, Readout, Source
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


# Brasswick's planted entries that only another scan's rebuild settles, with the
# check that settles each (answer_key_brasswick.json, "check").
MEMO_CONTRADICTIONS = [
    ("BF1", "slide 4", "$943K", "gross_vs_net_revenue"),
    ("BF2", "slide 4", "January 2026 to September 2026", "deck_history_vs_metrics"),
    ("BF3", "slide 10", "29", "contractor_spend_vs_headcount_and_burn"),
]


@pytest.mark.parametrize("flag_id,where,stated,check", MEMO_CONTRADICTIONS)
def test_other_scans_flags_relabel_the_pitch_claim(readouts, flag_id, where, stated, check):
    key = {f["id"]: f for f in json.loads((ROOMS / "answer_key_brasswick.json").read_text())["flags"]}
    assert key[flag_id]["check"] == check
    r = readouts["brasswick"]
    row = row_at(r, where, stated)
    assert row["label"] == "contradicted"
    c = claim(r, row["claim id"])
    flag = next(x for x in r.claims if x.id in c.conflicts_with)
    assert flag.check.name == check and flag.scan == "redflags"
    assert c.sources[0].uri == "01_overview/pitch_deck.pdf"           # the pitch side
    assert any(s.uri != "01_overview/pitch_deck.pdf" for s in c.sources)  # the side that disagrees
    assert c.severity == "flag" and c.text.startswith("Contradicted:")
    assert check_claim(c, ROOMS / "brasswick")[1] == []


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
    assert row["label"] == "supported"
    assert "gross_margin_from_ledger" in row["ask"] and "has not run" in row["ask"]


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
