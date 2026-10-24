"""The expert-read report sections: the script's fallback, the citation check, the model path
(with a fake model, no network) and the chart data on Hollis Voice and Brasswick.

Each room's readout is built the way a user builds it, with no model key.
Tests name checks and files, never claim numbers.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from schema.claim import Readout
from scans import knowledge
from scans.memo import charts, sections
from scans.memo.sections import PARTS, SectionDraft, DraftSentence, check_sentence, numbers_in

from memo.tests.conftest import ROOT, build_readout

HOLLIS = ROOT / "data_room" / "hollis_voice"
BRASSWICK = ROOT / "data_room" / "brasswick"


@pytest.fixture(autouse=True)
def no_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


@pytest.fixture(scope="session")
def readouts(tmp_path_factory) -> dict[str, Readout]:
    out = tmp_path_factory.mktemp("sections_out")
    return {room.name: Readout.model_validate_json(build_readout(out, room).read_text(encoding="utf-8"))
            for room in (HOLLIS, BRASSWICK)}


@pytest.fixture()
def out(tmp_path, monkeypatch) -> Path:
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    return tmp_path


def _all_sentences(section):
    return [(p.key, s) for p in section.parts for s in p.sentences]


# The script's fallback ------------------------------------------------------------


@pytest.mark.parametrize("room", [HOLLIS, BRASSWICK], ids=["hollis_voice", "brasswick"])
@pytest.mark.parametrize("piece", ["traction_and_revenue", "burn_and_runway"])
def test_without_a_key_the_script_writes_the_same_five_parts_every_sentence_cited(readouts, room, piece, out):
    readout = readouts[room.name]
    s = sections.build_section(readout, room, piece)
    assert s.written_by == "script" and s.model is None
    assert [p.key for p in s.parts] == [k for k, _ in PARTS]
    claims = {c.id: c for c in readout.claims}
    got = _all_sentences(s)
    assert {k for k, _ in got} >= {"shows", "lens", "weak", "ask"}
    for _, sent in got:
        assert sent.claim_ids and all(i in claims for i in sent.claim_ids)
        assert check_sentence(sent.text, sent.claim_ids, claims) == (sent.claim_ids, None)
        assert "—" not in sent.text and "synthetic" not in sent.text.lower()
    assert s.dropped == []
    # Every weak sentence rests on a flagged or watched claim.
    for key, sent in got:
        if key == "weak":
            assert all(claims[i].severity in ("flag", "watch") for i in sent.claim_ids)


def test_the_script_draft_is_written_beside_its_chart_and_reloads(readouts, out):
    readout = readouts["hollis_voice"]
    written = sections.build_all(readout, HOLLIS, use_model=False)
    folder = out / "hollis_voice" / "sections"
    assert sorted(p.name for p in folder.iterdir()) == [
        "burn_and_runway.chart.json", "burn_and_runway.json", "traction_and_revenue.chart.json", "traction_and_revenue.json"]
    assert "chart" not in json.loads((folder / "burn_and_runway.json").read_text())
    again = sections.load(HOLLIS, "burn_and_runway")
    assert again == written[1]
    # The memo takes the written ones for the same readout, and drafts afresh for another.
    assert sections.for_memo(readout, HOLLIS, readout.built_at)[0].built_at == written[0].built_at
    assert sections.for_memo(None, HOLLIS, "another readout") == []


# The citation and number check ------------------------------------------------------


def test_the_check_keeps_known_ids_and_drops_a_sentence_with_none_or_a_figure_its_claims_do_not_state(readouts):
    claims = {c.id: c for c in readouts["hollis_voice"].claims}
    deck = next(c for c in claims.values() if c.check.name == "deck_revenue_vs_pnl" and c.severity == "flag")
    assert check_sentence("The deck's ARR is $2,500,000.", [deck.id, "made-up-1"], claims) == ([deck.id], None)
    assert check_sentence("Revenue looks fine.", ["made-up-1"], claims) == ([], "cites no claim in the readout")
    assert check_sentence("Revenue looks fine.", [], claims)[1] == "cites no claim in the readout"
    kept, why = check_sentence("The deck's ARR is $2,700,000.", [deck.id], claims)
    assert why == "states a figure its claims do not: 2700000"
    # Figures as claims write them: commas, decimals and the slide a claim cites all match.
    assert check_sentence("Slide 3 states $2,500,000, 11.6% above the books.", [deck.id], claims)[1] is None
    assert numbers_in("$2,240,868 and 37.0 and 09") == {"2240868", "37", "9"}


def test_the_model_path_puts_kimmys_file_in_the_prompt_and_its_sentences_through_the_check(readouts, out, monkeypatch):
    import clients.llm as llm

    readout = readouts["brasswick"]
    claims = {c.id: c for c in readout.claims}
    flag = next(c for c in readout.claims if c.check.name == "contractor_spend_vs_headcount_and_burn" and c.severity == "flag")
    seen = {}

    def fake_read(output, **kw):
        seen.update(kw)
        assert output is SectionDraft
        return SectionDraft(
            shows=[DraftSentence(text="Contractor spend sits outside the plan — the plan drops it.", claim_ids=[flag.id])],
            lens=[DraftSentence(text="An expert reads spend left out of the plan as hidden burn.", claim_ids=[flag.id, "nope"])],
            strong=[DraftSentence(text="The founders are strong.", claim_ids=[])],
            weak=[DraftSentence(text="Contractors add $99,999 a month.", claim_ids=[flag.id])],
            ask=[DraftSentence(text="Who are the contractors, and will the plan pay them?", claim_ids=[flag.id])])

    monkeypatch.setattr(llm, "read", fake_read)
    s = sections.build_section(readout, BRASSWICK, "burn_and_runway", use_model=True)
    assert s.written_by == "model" and s.model == llm.model_id("read")
    # Kimmy's burn and runway file reaches the prompt as the knowledge block.
    assert seen["knowledge"] == knowledge.block(["burn_and_runway"])
    assert knowledge.text("burn_and_runway")[:200] in seen["knowledge"]
    assert f"[{flag.id}]" in seen["script_results"] and seen["scan"] == "memo"
    got = {k: [x.text for x in p.sentences] for p in s.parts for k in [p.key]}
    assert got["shows"] == ["Contractor spend sits outside the plan, the plan drops it."]
    assert [x.claim_ids for p in s.parts if p.key == "lens" for x in p.sentences] == [[flag.id]]
    assert got["strong"] == [] and got["weak"] == []
    assert {d.why for d in s.dropped} == {"cites no claim in the readout", "states a figure its claims do not: 99999"}
    assert all(i in claims for _, x in _all_sentences(s) for i in x.claim_ids)


def test_a_failed_model_call_falls_back_to_the_script_and_says_so(readouts, out):
    def broken(ev):
        raise RuntimeError("no network")

    s = sections.build_section(readouts["hollis_voice"], HOLLIS, "traction_and_revenue", use_model=True, drafter=broken)
    assert s.written_by == "script" and "model call failed" in s.note
    assert any(p.sentences for p in s.parts)


# The chart data -----------------------------------------------------------------------


def _metric_cell(room: Path, column: str, month: str) -> float:
    import csv
    with open(room / "03_metrics" / "monthly_metrics.csv", newline="") as fh:
        return float(next(r for r in csv.DictReader(fh) if r["month"] == month)[column])


def test_hollis_traction_chart_sets_the_metrics_arr_against_the_pitch(readouts):
    c = charts.traction_chart(readouts["hollis_voice"], HOLLIS)
    metric, rebuilt = c["series"]
    assert c["unit"] == "USD_per_year" and metric["source"]["file"] == "03_metrics/monthly_metrics.csv"
    assert metric["source"]["locator"].startswith("column arr")
    assert metric["x"][0] == "2025-01" and metric["x"][-1] == "2026-09"
    assert metric["y"][-1] == _metric_cell(HOLLIS, "arr", "2026-09")
    # The customer file's subscription rows leave the pilot out, so the rebuilt figure sits below the metrics file.
    assert rebuilt["source"]["file"] == "03_metrics/customer_mrr_by_month.csv" and rebuilt["y"][-1] < metric["y"][-1]
    stated = {m["source"]["file"]: m for m in c["markers"]}
    assert set(stated) == {"01_overview/pitch_deck.pdf", "01_overview/pitch_video_script.md"}
    assert all(m["y"] > metric["y"][-1] and m["claim_ids"] for m in c["markers"])


def test_brasswick_traction_chart_sets_the_metrics_mrr_against_the_deck(readouts):
    c = charts.traction_chart(readouts["brasswick"], BRASSWICK)
    metric, rebuilt = c["series"]
    assert c["unit"] == "USD_per_month" and metric["source"]["locator"].startswith("column subscription_revenue")
    assert metric["y"][-1] == _metric_cell(BRASSWICK, "subscription_revenue", "2026-09")
    assert rebuilt["source"]["file"] == "03_metrics/revenue_by_customer.csv" and rebuilt["y"][-1] < metric["y"][-1]
    (deck,) = c["markers"]
    assert deck["source"] == {"file": "01_overview/pitch_deck.pdf", "locator": "slide 4"} and deck["y"] == metric["y"][-1]


def _named(room: Path, name: str):
    wb, _ = charts._workbook(room)
    return charts._named(wb, name)


def test_hollis_burn_chart_reruns_the_plan_with_the_hires_it_leaves_out(readouts):
    c = charts.burn_chart(readouts["hollis_voice"], HOLLIS)
    plan, found = c["series"]
    lines = {ln["role"]: ln for ln in c["lines"]}
    assert plan["source"]["file"] == "02_financials/financial_model.xlsx" and plan["source"]["locator"].startswith("Cash_Runway!")
    assert plan["y"][0] == _named(HOLLIS, "CASH_START")
    # The plan's own roll gives the model's runway; with the 16 hires the model does not pay for, the
    # FRAMEWORKS 1.4 worked example's 19 months.
    assert lines["plan"]["months"] == _named(HOLLIS, "RUNWAY_MONTHS") == 37
    assert lines["found"]["months"] == 19
    assert "16 hires" in found["what"] and any(s["file"] == "05_team/hiring_plan.csv" for s in found["sources"])
    assert found["claim_ids"] and all(f <= p for f, p in zip(found["y"], plan["y"]))
    base = lines["baseline"]
    assert base["source"]["file"] == "knowledge/burn_and_runway.md" and base["months"] == charts.kimmy_runway_baseline()
    assert base["x"] == charts.add_months(base["close"], base["months"])


def test_brasswick_burn_chart_adds_the_contractor_spend_the_plan_drops(readouts):
    c = charts.burn_chart(readouts["brasswick"], BRASSWICK)
    plan, found = c["series"]
    lines = {ln["role"]: ln for ln in c["lines"]}
    assert lines["plan"]["months"] == _named(BRASSWICK, "RUNWAY_MONTHS")
    assert lines["found"]["months"] < lines["plan"]["months"]
    flag = next(x for x in readouts["brasswick"].claims if x.check.name == "contractor_spend_vs_headcount_and_burn")
    assert found["claim_ids"] == [flag.id] and "Professional services" in found["what"]
    # The first plan month's gap is the amount the claim says the plan leaves out.
    left_out = re.search(r"leaves \$([\d,]+\.\d\d) a month", flag.text).group(1).replace(",", "")
    assert round(plan["y"][1] - found["y"][1], 2) == float(left_out)


def test_a_room_with_no_files_gets_no_chart(readouts, tmp_path):
    assert charts.traction_chart(readouts["hollis_voice"], tmp_path) is None
    assert charts.burn_chart(readouts["hollis_voice"], tmp_path) is None


# The page ----------------------------------------------------------------------------


def test_the_memo_page_shows_both_sections_with_plotly_from_beside_the_page(readouts, out):
    from memo.build import build_memo
    from memo.html import render_html
    from memo.report_html import PLOTLY_FILE, PLOTLY_PATH

    readout = readouts["hollis_voice"]
    memo = build_memo(readout, HOLLIS, "2026-10-24T15:00:00Z")
    page = render_html(memo, sections.for_memo(readout, HOLLIS, memo.readout_built_at))
    assert page.count('class="xr"') == 2
    assert f'<script src="{PLOTLY_FILE}"></script>' in page and PLOTLY_PATH.stat().st_size > 1_000_000
    assert not re.search(r'<script[^>]+src="(https?:)?//', page)
    assert "—" not in page and "–" not in page
    data = json.loads(re.search(r'id="report-data">(.*?)</script>', page, re.S).group(1))
    assert [r["piece"] for r in data] == ["traction_and_revenue", "burn_and_runway"]
    assert all(i in memo.claims for r in data for p in r["parts"] for s in p["sentences"] for i in s["claim_ids"])
    # Without reports the page is as before: no plotly, no report data.
    bare = render_html(memo)
    assert "<script src=" not in bare and 'id="report-data"' not in bare and 'class="xr"' not in bare


def test_the_server_serves_the_vendored_plotly_beside_the_memo_page():
    from fastapi.testclient import TestClient

    from memo.report_html import PLOTLY_FILE, PLOTLY_PATH
    from server.app import app

    client = TestClient(app, base_url="http://127.0.0.1")
    r = client.get(f"/api/rooms/hollis_voice/{PLOTLY_FILE}")
    assert r.status_code == 200 and "javascript" in r.headers["content-type"]
    assert len(r.content) == PLOTLY_PATH.stat().st_size and r.content.startswith(b"/**\n* plotly.js v2.35.2")
    assert client.get(f"/api/rooms/nope/{PLOTLY_FILE}").status_code == 404
