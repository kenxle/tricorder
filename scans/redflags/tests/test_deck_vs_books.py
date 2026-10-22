"""deck_vs_books: deck revenue against the P&L, and partial history.

One test per row of the verification table in
docs/features/20261022.11_deck_vs_books/05_plan.md. Rooms in data_room/ are
read in place and never written. Test rooms are built in tmp_path.
"""

from __future__ import annotations

import json
import socket
from functools import lru_cache
from pathlib import Path

import pytest

from eval.score import score
from schema.check_quotes import check_claim
from schema.claim import Readout
from scans.base import Ids
from scans.redflags import deck_vs_books as dvb
from scans.redflags.tests.deck_vs_books_fixtures import (DATA_ROOM, DECK, HOLLIS, MODEL, _deck_size, chart_slide, copy_room,
                                                         make_room, month_label, replace_slides, text_slide, total_revenue)

BRASSWICK = DATA_ROOM / "brasswick"
CLEAN = DATA_ROOM / "hollis_voice_clean"
SEED = DATA_ROOM / "hollis_voice_seed_drop"
REVENUE = dvb.CHECK_REVENUE
HISTORY = dvb.CHECK_HISTORY


def run(room: Path):
    claims, gaps, _panels = dvb.check(Path(room), Ids("redflags"))
    return claims, gaps


@lru_cache(maxsize=None)
def run_real(name: str):
    return run(DATA_ROOM / name)


def by_check(claims, name):
    return [c for c in claims if c.check.name == name]


def locators(claim):
    return {(s.uri, s.locator) for s in claim.sources}


def quotes(claim):
    return [s.quote for s in claim.sources]


# DVB-R1 -------------------------------------------------------------------

def test_finds_every_revenue_figure_hollis():
    claims, gaps = run_real("hollis_voice")
    slides = sorted({int(s.locator.split()[1]) for c in claims for s in c.sources
                     if s.uri == "01_overview/pitch_deck.pdf"})
    assert slides == [3, 11, 14]
    texts = " ".join(c.text for c in claims)
    assert "ARR" in texts and "chart on slide 3" in texts and "3.5% a month" in texts
    assert not [c for c in claims if "not matched" in c.text]
    assert gaps == []


def test_finds_every_revenue_figure_brasswick():
    claims, _ = run_real("brasswick")
    texts = [c.text for c in claims]
    assert any("Revenue, last 12 months" in t for t in texts)
    assert any("MRR, September 2026" in t for t in texts)
    assert any("chart on slide 4" in t for t in texts)
    assert any("grew every month in 2026" in t for t in texts)


def test_claims_json_fallback(tmp_path):
    room = make_room(tmp_path, "no_claims_page")
    claims, _ = run(room)
    arr = next(c for c in by_check(claims, REVENUE) if c.value and c.value.label == "arr")
    assert ("01_overview/claims.json", "claims[0]") in locators(arr)
    assert arr.severity == "flag"


# DVB-R2, R3, R4 -------------------------------------------------------------

def test_hollis_arr_flags_against_pnl():
    claims, _ = run_real("hollis_voice")
    arr = next(c for c in claims if c.value and c.value.label == "arr")
    assert arr.check.name == REVENUE and arr.check.kind == "script" and arr.confidence == "computed"
    assert arr.severity == "flag"
    assert arr.value.number == 2_500_000 and arr.value.unit == "USD_per_year" and arr.value.period == "2026-09"
    assert "$2,240,868" in arr.text and "11.6%" in arr.text
    assert ("01_overview/pitch_deck.pdf", "slide 3") in locators(arr)
    assert ("01_overview/pitch_deck.pdf", "slide 14") in locators(arr)
    assert (MODEL, "P&L!W10") in locators(arr)
    assert "$2.5M" in quotes(arr)


def test_brasswick_stated_figures_match():
    claims, _ = run_real("brasswick")
    ltm = next(c for c in claims if "Revenue, last 12 months" in c.text)
    mrr = next(c for c in claims if "MRR, September 2026" in c.text)
    assert ltm.severity == "info" and mrr.severity == "info"
    assert len([s for s in ltm.sources if s.uri == MODEL]) == 12
    assert mrr.value.label == "mrr" and mrr.value.number == 84_810


@pytest.mark.parametrize("deck,books,half,expect", [
    (2_500_000, 2_460_000, 50_000, True),    # $2.5M printed: within half a step
    (2_500_000, 2_240_868, 50_000, False),   # outside both the step and 1 percent
    (943_340, 943_339.5, 0, True),           # exact form: within 1 percent
    (100, 102, 0, False),
])
def test_rounded_figure_within_half_step_matches(deck, books, half, expect):
    assert dvb.figure_matches(deck, books, half, 0.01) is expect


def test_clean_room_has_no_flags():
    claims, gaps = run_real("hollis_voice_clean")
    assert claims and not [c for c in claims if c.severity == "flag"]
    arr = next(c for c in claims if c.value and c.value.label == "arr")
    assert arr.severity == "info" and arr.value.number == 2_060_868


# DVB-R5 --------------------------------------------------------------------

def test_missing_pnl_lists_figures_unmatched(tmp_path):
    room = copy_room(tmp_path, leave_out=(MODEL, "03_metrics/customer_mrr_by_month.csv"))
    claims, gaps = run(room)
    unmatched = [c for c in claims if "not matched" in c.text]
    assert len(unmatched) == 3
    assert all(c.severity == "info" and "no P&L to match against" in c.text for c in unmatched)


# DVB-R6 --------------------------------------------------------------------

def test_chart_bars_match_books_hollis():
    claims, _ = run_real("hollis_voice")
    chart = next(c for c in by_check(claims, REVENUE) if "chart on slide 3" in c.text)
    assert chart.severity == "info"
    assert "21 bars" in chart.text and "matches" in chart.text


def test_quarterly_chart_compared_by_quarter(tmp_path):
    claims, _ = run(make_room(tmp_path, "quarterly"))
    chart = next(c for c in by_check(claims, REVENUE) if "chart on slide 3" in c.text)
    assert "7 bars" in chart.text and chart.severity == "info"


# DVB-R7 --------------------------------------------------------------------

def test_chart_starting_six_months_late_is_flagged(tmp_path):
    """The roadmap's test deck. Its hidden months hold a climb, so it is a watch (Ken's call, 2026-10-22)."""
    claims, _ = run(make_room(tmp_path, "starts_late"))
    (hist,) = by_check(claims, HISTORY)
    assert hist.text.startswith("Shows part of the history:")
    assert hist.severity == "watch"
    assert "2025-01 to 2025-06" in hist.text and "$2,651" in hist.text and "$19,462" in hist.text
    assert hist.value.number == 6 and hist.value.unit == "months" and hist.value.label == "other"
    assert hist.value.period == "2025-01 to 2025-06"


def test_brasswick_partial_history_names_hidden_peak():
    claims, _ = run_real("brasswick")
    (hist,) = by_check(claims, HISTORY)
    assert hist.severity == "flag"
    assert "2025-05 to 2025-12" in hist.text and "2025-09" in hist.text
    assert "$84,090" in hist.text and "28.2%" in hist.text and "$60,400" in hist.text
    assert ("01_overview/pitch_deck.pdf", "slide 4") in locators(hist)


def test_brasswick_bf2_counts_as_found_and_no_decoy_flagged():
    claims, _ = run_real("brasswick")
    key = json.loads((DATA_ROOM / "answer_key_brasswick.json").read_text())
    line, lines = score(Readout(room="brasswick", built_at="test", claims=claims), key, "brasswick")
    assert any(ln.startswith("found") and "BF2" in ln for ln in lines)
    assert line.decoys_flagged == 0


def test_hollis_answer_key_decoys_stay_clear():
    for name, key in (("hollis_voice", "answer_key.json"), ("hollis_voice_clean", "answer_key_clean.json")):
        claims, _ = run_real(name)
        k = json.loads((DATA_ROOM / key).read_text())
        line, _ = score(Readout(room=name, built_at="test", claims=claims), k, name)
        assert line.decoys_flagged == 0


def test_full_history_chart_is_info():
    claims, _ = run_real("hollis_voice")
    (hist,) = by_check(claims, HISTORY)
    assert hist.severity == "info" and "no month left out" in hist.text


def test_quarterly_chart_flags_partial_history(tmp_path):
    claims, _ = run(make_room(tmp_path, "quarterly"))
    (hist,) = by_check(claims, HISTORY)
    assert hist.text.startswith("Shows part of the history:")
    assert "quarters where the books hold months" in hist.text and "no month inside a quarter fell" in hist.text
    assert hist.severity == "watch"


@pytest.mark.parametrize("values,first_chart,expect", [
    ([10, 20, 30], 40, "watch"),             # a climb
    ([10, 50, 30], 40, "flag"),              # a dip
    ([10, 80, 60], 40, "flag"),              # a peak above the chart's first month
    ([10, 20, 20.1, 20.2, 20.3], 25, "flag"),  # a flat stretch of four months, no fall
])
def test_hidden_months_severity(values, first_chart, expect):
    months = [f"2025-{i + 1:02d}" for i in range(len(values))]
    assert dvb.describe_hidden(months, values, first_chart)["severity"] == expect


# DVB-R8 --------------------------------------------------------------------

def test_unreadable_chart_is_a_gap(tmp_path):
    claims, gaps = run(make_room(tmp_path, "unreadable"))
    assert any(g.what == "Not in the room: a readable chart on slide 3" for g in gaps)
    (hist,) = by_check(claims, HISTORY)
    assert hist.severity == "info"
    assert not [c for c in by_check(claims, REVENUE) if "bars" in c.text]


# DVB-R9 --------------------------------------------------------------------

def test_revenue_row_differences_write_no_claim():
    for name in ("brasswick", "hollis_voice_clean"):
        claims, _ = run_real(name)
        cited = {s.uri for c in claims for s in c.sources}
        assert not {u for u in cited if u.startswith("03_metrics/")}, name


def test_window_from_revenue_rows_when_pnl_missing(tmp_path):
    room = make_room(tmp_path, "starts_late", leave_out=(MODEL,))
    claims, gaps = run(room)
    (hist,) = by_check(claims, HISTORY)
    assert "2025-01 to 2025-06" in hist.text
    assert any(s.uri == "03_metrics/customer_mrr_by_month.csv" for s in hist.sources)
    assert any("monthly P&L" in g.what for g in gaps)


# DVB-R10 -------------------------------------------------------------------

def test_missing_deck_is_one_gap(tmp_path):
    room = copy_room(tmp_path, leave_out=("01_overview/pitch_deck.pdf",))
    claims, gaps = run(room)
    assert claims == []
    assert len(gaps) == 1 and gaps[0].what == "Not in the room: the pitch deck (01_overview/pitch_deck.pdf)"


def test_missing_pnl_gap_has_piece(tmp_path):
    room = copy_room(tmp_path, leave_out=(MODEL,))
    _, gaps = run(room)
    g = next(g for g in gaps if "monthly P&L" in g.what)
    assert g.what == "Not in the room: the monthly P&L (02_financials/financial_model.xlsx, P&L tab)"
    assert g.piece == "traction_and_revenue"


def test_chart_months_missing_from_books_is_a_gap(tmp_path):
    claims, gaps = run(make_room(tmp_path, "before_books"))
    g = next(g for g in gaps if "2024-10 to 2024-12" in g.what)
    assert g.what == "Not in the room: monthly revenue for 2024-10 to 2024-12, shown on slide 3"
    assert g.piece == "traction_and_revenue"
    # The first made-up bar is under 1 percent of the tallest. It must still count as a bar,
    # or the check would report a skipped month that is not there.
    assert not [c for c in by_check(claims, HISTORY) if "skipped" in c.text]


# DVB-R11 -------------------------------------------------------------------

def test_value_labels_route_pieces():
    claims, _ = run_real("brasswick")
    hist = by_check(claims, HISTORY)[0]
    assert hist.value.label == "other" and hist.value.unit == "months"
    hv, _ = run_real("hollis_voice")
    assert next(c for c in hv if c.value and c.value.label == "arr").value.unit == "USD_per_year"


# DVB-R12 -------------------------------------------------------------------

@pytest.mark.parametrize("name", ["hollis_voice", "hollis_voice_seed_drop", "hollis_voice_clean", "brasswick"])
def test_every_claim_passes_quote_checker(name):
    claims, _ = run_real(name)
    assert claims
    for c in claims:
        _, problems = check_claim(c, DATA_ROOM / name)
        assert problems == [], (c.id, problems)


@pytest.mark.parametrize("kind", ["starts_late", "quarterly", "unreadable", "no_claims_page"])
def test_every_claim_passes_quote_checker_on_test_rooms(tmp_path, kind):
    room = make_room(tmp_path, kind)
    claims, _ = run(room)
    for c in claims:
        assert all(not s.uri.startswith("/") for s in c.sources)
        _, problems = check_claim(c, room)
        assert problems == [], (c.id, problems)


# DVB-R13 -------------------------------------------------------------------

def test_runs_offline(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("deck_vs_books opened a network connection")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    claims, _ = run(HOLLIS)
    assert claims


def test_bars_read_without_pypdf():
    src = Path(dvb.__file__).read_text()
    assert "pypdf" not in src.replace("pdfplumber", "")
    assert "anthropic" not in src


def test_claim_ids_come_from_ids():
    ids = Ids("redflags")
    claims, _, _ = dvb.check(HOLLIS, ids)
    assert [c.id for c in claims] == [f"redflags-{i:03d}" for i in range(1, len(claims) + 1)]


def test_match_table_panel():
    _, _, panels = dvb.check(BRASSWICK, Ids("redflags"))
    (panel,) = panels
    assert panel.name == "deck against the books"
    assert panel.columns[0] == "Slide"
    assert any("chart window" in row[1] for row in panel.rows)


def test_chart_shape_tolerance_is_a_setting(monkeypatch, tmp_path):
    from schema import settings
    assert settings.DEFAULTS["chart_shape_tolerance"] == 0.02
    path = tmp_path / "s.json"
    path.write_text('{"chart_shape_tolerance": 0.0001}')
    monkeypatch.setenv("TRICORDER_SETTINGS", str(path))
    claims, _ = run(HOLLIS)
    chart = next(c for c in by_check(claims, REVENUE) if "chart on slide 3" in c.text)
    assert chart.severity == "flag"



# Review round 1 (docs/features/20261022.10_feature_breakdown/review_wave1.md) -----

def test_s1_short_form_figure_uses_half_step_through_check(tmp_path):
    """S1: a "$2.2M" ARR with no exact form in the deck matches books of $2,240,868 (half step $50,000)."""
    room = make_room(tmp_path, "no_claims_page")
    cj = room / "01_overview/claims.json"
    data = json.loads(cj.read_text())
    data["claims"][0]["value"] = "$2.2M"
    cj.write_text(json.dumps(data, indent=2))
    claims, _ = run(room)
    arr = next(c for c in by_check(claims, REVENUE) if c.value and c.value.label == "arr")
    assert arr.value.number == 2_200_000
    assert arr.severity == "info" and "matches" in arr.text
    assert "within the rounding of the printed $2.2M" in arr.text


def test_s1_exact_form_keeps_one_percent_rule():
    """The real deck prints $2,500,000 exactly, so no half step applies and it stays a flag."""
    claims, _ = run_real("hollis_voice")
    arr = next(c for c in claims if c.value and c.value.label == "arr")
    assert arr.severity == "flag"


def test_s2_plan_growth_mismatch_is_a_flag(tmp_path):
    room = replace_slides(tmp_path, HOLLIS, {11: text_slide(_deck_size(HOLLIS), "Plan and runway",
                                                            ["Revenue grows 8.0% a month in the plan."])})
    claims, _ = run(room)
    plan = next(c for c in claims if "plan growth" in c.text)
    assert "differs from" in plan.text
    assert plan.severity == "flag"


def _brasswick_chart_room(tmp_path, start, end):
    series = [(m, v) for m, v in total_revenue(BRASSWICK) if start <= m <= end]
    cap = f"Monthly revenue, {month_label(series[0][0])} to {month_label(series[-1][0])}"
    slide = chart_slide(_deck_size(BRASSWICK), "Traction", [m for m, _ in series], [v for _, v in series], cap)
    return replace_slides(tmp_path, BRASSWICK, {4: slide})


def test_s3_chart_ending_early_is_partial_history(tmp_path):
    """S3: a chart from 2025-05 to 2025-09 ends at the peak and hides the fall after it."""
    claims, _ = run(_brasswick_chart_room(tmp_path, "2025-05", "2025-09"))
    (hist,) = by_check(claims, HISTORY)
    assert "no month left out" not in hist.text
    assert hist.text.startswith("Shows part of the history:")
    assert "ends at 2025-09" in hist.text and "2025-10 to 2026-09" in hist.text
    assert hist.severity == "flag"
    assert hist.value.number == 12


def test_s3_whole_window_still_info(tmp_path):
    claims, _ = run(_brasswick_chart_room(tmp_path, "2025-05", "2026-09"))
    (hist,) = by_check(claims, HISTORY)
    assert hist.severity == "info" and "no month left out" in hist.text


def test_s4_blank_revenue_cell_is_a_gap_not_a_crash(monkeypatch):
    """S4: one month missing from "Total revenue" must not crash check() or the engine."""
    real = dvb.load_pnl

    def holed(room):
        books = real(room)
        if books is not None:
            books.lines[books.total_label].pop("2026-03", None)
        return books

    monkeypatch.setattr(dvb, "load_pnl", holed)
    claims, gaps = run(BRASSWICK)
    assert any("2026-03" in g.why for g in gaps)
    assert all(g.piece == "traction_and_revenue" for g in gaps)
    assert len({(g.what, g.why) for g in gaps}) == len(gaps)  # one gap per missing value, not one per figure
    assert claims  # the figures that do not need 2026-03 still run
    from scans.redflags import scan
    result = scan.run(BRASSWICK)
    assert any(c.check.name == HISTORY for c in result.claims) or any("2026-03" in g.why for g in result.gaps)


def test_s4_zero_books_value_is_unmatched_not_a_crash(monkeypatch):
    real = dvb.load_pnl

    def zeroed(room):
        books = real(room)
        c = books.lines["Subscription revenue"]["2026-09"]
        books.lines["Subscription revenue"]["2026-09"] = dvb.Cell(0, c.uri, c.locator, "0")
        return books

    monkeypatch.setattr(dvb, "load_pnl", zeroed)
    claims, _ = run(BRASSWICK)
    mrr = next(c for c in claims if "MRR, September 2026" in c.text)
    assert "not matched" in mrr.text and mrr.severity == "info"


def test_s5_grew_flag_cites_the_months_that_fell(tmp_path):
    """S5: "grew every month in 2025" on Brasswick fell in 2025-10 and 2025-12; cite those cells and the months before."""
    room = replace_slides(tmp_path, BRASSWICK, {4: text_slide(_deck_size(BRASSWICK), "Traction",
                                                              ["Revenue grew every month in 2025."])})
    claims, _ = run(room)
    grew = next(c for c in claims if "grew every month in 2025" in c.text)
    assert grew.severity == "flag" and "2025-10" in grew.text and "2025-12" in grew.text
    books = dvb.load_pnl(BRASSWICK)
    total = books.lines[books.total_label]
    cited = {s.locator for s in grew.sources if s.uri == MODEL}
    assert {total[m].locator for m in ("2025-09", "2025-10", "2025-11", "2025-12")} <= cited


def test_u1_no_as_of_month_gives_the_real_reason(tmp_path):
    room = replace_slides(tmp_path, HOLLIS, {1: text_slide(_deck_size(HOLLIS), "Hollis Voice", ["Series A"])})
    claims, _ = run(room)
    arr = next(c for c in claims if "ARR" in c.text and "not matched" in c.text)
    assert "no 'Data as of' month" in arr.text


def test_u7_history_value_counts_months_left_out_only(tmp_path):
    """A chart captioned 2026-01 to 2026-09 with only 8 bars: 8 months left out before it, 1 skipped. The value is 8."""
    series = [(m, v) for m, v in total_revenue(BRASSWICK) if "2026-02" <= m <= "2026-09"]
    slide = chart_slide(_deck_size(BRASSWICK), "Traction", [m for m, _ in series], [v for _, v in series],
                        "Monthly revenue, January 2026 to September 2026")
    claims, _ = run(replace_slides(tmp_path, BRASSWICK, {4: slide}))
    (hist,) = by_check(claims, HISTORY)
    assert "1 months are skipped" in hist.text or "1 month is skipped" in hist.text
    assert hist.value.number == 8
