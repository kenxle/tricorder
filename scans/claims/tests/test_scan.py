"""The claims scan on the real rooms, through the command a user runs.

Only these tests read the answer keys (data_room/answer_key*.json); the scan
never does. Each room is scanned once per test run, by `python -m scans.claims`
in a subprocess with its own TRICORDER_OUT_DIR.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from schema.check_quotes import check_result
from schema.claim import ScanResult
from schema.readers import pdf_pages

ROOT = Path(__file__).resolve().parents[3]
ROOMS = ROOT / "data_room"


def run_scan(room: str, out: Path) -> ScanResult:
    env = dict(os.environ, TRICORDER_OUT_DIR=str(out))
    env.pop("ANTHROPIC_API_KEY", None)
    done = subprocess.run([sys.executable, "-m", "scans.claims", str(ROOMS / room)], cwd=ROOT, env=env,
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("claims: ")
    return ScanResult.model_validate_json((out / room / "claims.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def results(tmp_path_factory):
    out = tmp_path_factory.mktemp("claims_out")
    rooms = ("hollis_voice", "brasswick", "hollis_voice_seed_drop", "hollis_voice_clean")
    return {room: run_scan(room, out) for room in rooms}


def table(result: ScanResult) -> list[dict]:
    panel = next(p for p in result.panels if p.name == "claims table")
    return [dict(zip(panel.columns, row)) for row in panel.rows]


def by_id(result: ScanResult) -> dict:
    return {c.id: c for c in result.claims}


def find_row(result: ScanResult, where_start: str, stated: str) -> dict:
    rows = [r for r in table(result) if r["where"].startswith(where_start) and r["stated"] == stated]
    assert rows, f"no row at {where_start} stating {stated}"
    return rows[0]


@pytest.mark.parametrize("room", ["hollis_voice", "brasswick", "hollis_voice_seed_drop", "hollis_voice_clean"])
def test_quote_checker_passes_on_every_claim(results, room):
    checked, failures = check_result(results[room], ROOMS / room)
    assert failures == {}
    assert all(c.confidence == "computed" for c in checked.claims)


@pytest.mark.parametrize("room", ["hollis_voice", "brasswick", "hollis_voice_seed_drop", "hollis_voice_clean"])
def test_every_claim_has_one_label_and_one_row(results, room):
    result = results[room]
    rows = table(result)
    assert sorted(r["claim id"] for r in rows) == sorted(c.id for c in result.claims)
    assert {r["label"] for r in rows} <= {"supported", "contradicted", "unsupported"}
    for c in result.claims:
        prefix = c.text.split(":")[0]
        assert prefix in ("Supported", "Contradicted", "Unsupported")
        assert (c.severity == "flag") == (prefix == "Contradicted")


def _figure_lines(room: str) -> list[tuple[str, str]]:
    """Every line of every slide and of the script with a digit or a spelled-out
    count, found by a plain regex, independent of the scan's parser."""
    deck = next((ROOMS / room).glob("*/pitch_deck.pdf"))
    lines = []
    for n, text in enumerate(pdf_pages(deck), start=1):
        for line in text.splitlines():
            if line.startswith("Synthetic data room") or not re.search(r"\d", line):
                continue
            if re.fullmatch(r".*\b\d{1,2}:\d{2}\s?[ap]m", line):
                continue  # a clock time in an example call
            lines.append((f"slide {n}", line))
    script = next((ROOMS / room).glob("*/pitch_video_script.md"))
    for n, line in enumerate(script.read_text(encoding="utf-8").splitlines(), start=1):
        if line.startswith(("**", "Synthetic", "#")) or not line.strip():
            continue
        if re.search(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred|million)\b", line, re.I):
            lines.append((f"line {n}", line))
    return lines


QUALIFIER_ONLY = re.compile(r"^(Average (monthly )?net burn,? (over )?(the )?next 12 months|Planned over the next 12 months|"
                            r"Revenue, last 12 months|MRR, September 2026|Calls handled in September 2026|"
                            r"Key metrics from this deck.*|Twelve months after the first invoice,)$")


FIGURE = re.compile(r"\$?\d[\d,.]*%?|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred|million)\b", re.I)


@pytest.mark.parametrize("room", ["hollis_voice", "brasswick"])
def test_every_figure_line_is_covered(results, room):
    """Done when: every numeric claim on every slide and in the script has a label.
    Every figure on a line with one sits in a claim's quote at that slide or line
    (or in a claims-page repeat the table lists), or in the not-counted panel, or
    the line only names the period of the big number above it."""
    result = results[room]
    quoted = [(s.locator, " ".join(s.quote.split())) for c in result.claims for s in c.sources]
    for row in table(result):
        for m in re.finditer(r"repeated at slide (\d+), claims page row[^:]*: '([^']*)'", row["where"]):
            quoted.append((f"slide {m.group(1)}", m.group(2)))
    skipped = next(p for p in result.panels if p.name == "claims not counted").rows
    missing = []
    for where, line in _figure_lines(room):
        flat = " ".join(line.split())
        if QUALIFIER_ONLY.match(flat) or any(flat in " ".join(r[1].split()) or " ".join(r[1].split()) in flat for r in skipped):
            continue
        here = [q for loc, q in quoted if loc.split()[0] == where.split()[0] and _locnum(loc) == _locnum(where)
                and (q in flat or flat in q or any(part and part in q for part in re.split(r"(?<=[.!?])\s+", flat)))]
        for token in FIGURE.findall(flat):
            token = token.rstrip(".,")
            if token.lower() == "one" and re.search(r"day one|one-", flat, re.I):
                continue  # "work from day one", "one-room practices": no figure
            if token and not any(token.lower() in q.lower() for q in here):
                missing.append((where, token, line))
    assert missing == [], "\n".join(map(str, missing))


def _locnum(locator: str) -> int:
    return int(re.search(r"\d+", locator).group(0))


def test_script_claims_are_labelled_as_the_script_not_the_video(results):
    for result in (results["hollis_voice"], results["brasswick"]):
        spoken = [c for c in result.claims if c.sources[0].uri.endswith("pitch_video_script.md")]
        assert spoken
        for c in spoken:
            assert "pitch video script" in c.text and "not recorded yet" in c.text
            assert c.sources[0].kind == "file" and c.sources[0].locator.startswith("line ")
        assert any(g.what.startswith("Not in the room: a transcript of the pitch video") for g in result.gaps)


def test_spoken_figures_are_marked_spoken_and_rounded(results):
    row = find_row(results["hollis_voice"], "script line 15", "about three million dollars")
    assert row["spoken"].startswith("spoken, rounded (about)")
    assert row["normalised"].startswith("ARR: 3,000,000 USD a year, 2026-09")
    row = find_row(results["brasswick"], "script line 27", "close to three years")
    assert row["normalised"].startswith("runway: 36 months")


# Planted contradictions the scan settles on its own, from the room's files.
# Each: (key id, where the pitch states it, the figure as stated, a file that must disagree).
SCAN_CONTRADICTIONS = {
    "hollis_voice": [
        ("PF2", "slide 3", "$2.5M", "02_financials/financial_model.xlsx"),
        ("PF2b", "script line 15", "about three million dollars", "01_overview/pitch_deck.pdf"),
        ("PF4", "slide 12", "24", "02_financials/financial_model.xlsx"),
        ("PF5", "slide 4", "at most 9%", "03_metrics/customer_mrr_by_month.csv"),
        ("PF7", "slide 3", "357", "03_metrics/monthly_metrics.csv"),
    ],
    "brasswick": [
        ("BF4", "slide 4", "$84,810", "03_metrics/revenue_by_customer.csv"),
        ("BF5", "script line 27", "close to three years", "02_financials/financial_model.xlsx"),
    ],
}


def _key(room: str) -> dict:
    name = "answer_key.json" if room == "hollis_voice" else f"answer_key_{room}.json"
    return json.loads((ROOMS / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("room", ["hollis_voice", "brasswick"])
def test_planted_contradictions_are_contradicted_with_both_sources(results, room):
    key = {f["id"]: f for f in _key(room)["flags"]}
    claims = by_id(results[room])
    for flag_id, where, stated, other_file in SCAN_CONTRADICTIONS[room]:
        assert flag_id in key
        row = find_row(results[room], where, stated)
        assert row["label"] == "contradicted", (flag_id, row)
        claim = claims[row["claim id"]]
        uris = [s.uri for s in claim.sources]
        key_files = {loc["file"] for loc in key[flag_id]["locations"]}
        assert uris[0] in key_files, (flag_id, uris)          # the pitch side, a file the key names
        assert other_file in uris, (flag_id, uris)            # the side that disagrees
        assert claim.severity == "flag"


def test_spoken_disagreements_carry_the_three_way_check_names(results):
    hv = by_id(results["hollis_voice"])
    row = find_row(results["hollis_voice"], "script line 15", "about three million dollars")
    assert hv[row["claim id"]].check.name == "spoken_arr_vs_claims_page"   # PF2b's check in the key
    bw = by_id(results["brasswick"])
    row = find_row(results["brasswick"], "script line 27", "close to three years")
    assert bw[row["claim id"]].check.name == "spoken_number_vs_claims_page"  # BF5's check in the key


# Green flags: (key id, where the deck states it, as stated, label). A figure only the
# company's financial model states reads unsupported (review wave 2a, S7): the key's
# GF2 and the 17 of GF3 are backed by the model alone.
GREENS = {
    "hollis_voice": [("GF1", "slide 13", "$9,000,000", "supported"), ("GF2", "slide 8", "near $252,000,000", "unsupported"),
                     ("GF3", "slide 10", "17", "unsupported"), ("GF3", "slide 12", "41", "supported")],
    "brasswick": [("GF1", "slide 11", "$3,000,000", "supported"), ("GF2", "slide 5", "14", "supported"),
                  ("GF3", "slide 5", "20%", "supported")],
}


@pytest.mark.parametrize("room", ["hollis_voice", "brasswick"])
def test_green_flags_are_supported_with_two_independent_sources(results, room):
    key = {g["id"]: g for g in _key(room)["green_flags"]}
    claims = by_id(results[room])
    for gid, where, stated, label in GREENS[room]:
        row = find_row(results[room], where, stated)
        assert row["label"] == label, (gid, row)
        claim = claims[row["claim id"]]
        outside = {s.uri for s in claim.sources if "pitch_deck" not in s.uri}
        assert outside, gid
        files = {loc["file"] for loc in key[gid]["locations"]} | {
            loc["file"] for extra in key[gid].get("also_agree", []) for loc in extra["locations"]}
        assert outside & files, (gid, outside)
        assert claim.sources[0].uri == "01_overview/pitch_deck.pdf"
        if label == "supported":
            assert outside - {"02_financials/financial_model.xlsx"}, gid


def test_a_figure_only_the_model_states_is_unsupported_and_says_so(results):
    """Review wave 2a, S7: the model is the company's own calculation, so it alone
    does not support a pitch figure. Runway and burn on Hollis Voice (PF4)."""
    result = results["hollis_voice"]
    for stated in ("37", "$374,462"):
        row = find_row(result, "slide 11", stated)
        assert row["label"] == "unsupported", row
        assert row["agrees"].startswith("financial model"), row
        assert "only a model reading backs this" in row["ask"]
        claim = by_id(result)[row["claim id"]]
        assert claim.text.startswith("Unsupported:") and "only a model reading backs this" in claim.text
        assert "02_financials/financial_model.xlsx" in [s.uri for s in claim.sources]


def test_clean_room_has_no_contradiction(results):
    assert [r for r in table(results["hollis_voice_clean"]) if r["label"] == "contradicted"] == []


def test_seed_drop_names_the_missing_customer_file(results):
    result = results["hollis_voice_seed_drop"]
    row = find_row(result, "slide 4", "at most 9%")
    assert row["label"] == "unsupported"
    assert any("file missing: monthly revenue by customer" in g.why and "largest customer share" in g.what for g in result.gaps)


def test_unsupported_claims_have_an_ask_and_a_gap(results):
    result = results["hollis_voice"]
    for row in table(result):
        if row["label"] == "unsupported":
            assert row["ask"].startswith("Please send ")
            assert any(row["stated"] in g.what for g in result.gaps), row


def test_examples_are_not_counted_as_claims(results):
    skipped = next(p for p in results["brasswick"].panels if p.name == "claims not counted").rows
    assert any("$405" in r[1] for r in skipped)
    assert not any("$405" in c.sources[0].quote for c in results["brasswick"].claims)


def test_independence_the_pitch_never_supports_itself(results):
    for room in ("hollis_voice", "brasswick"):
        claims = by_id(results[room])
        for row in table(results[room]):
            if row["label"] == "supported":
                srcs = claims[row["claim id"]].sources
                assert any(not re.search(r"pitch_deck|pitch_video|claims\.json|overview|website|one_pager", s.uri) for s in srcs)


def test_a_ceiling_written_as_no_customer_above_reads_at_most(results):
    """The deck says "No customer above 9% of ARR": a ceiling. The claim must not
    read as if the deck said some customer is above 9%."""
    result = results["hollis_voice"]
    row = find_row(result, "slide 4", "at most 9%")
    claim = by_id(result)[row["claim id"]]
    assert "as at most 9%" in claim.text
    assert "as above 9%" not in claim.text


def test_a_bare_figure_reads_with_its_unit_in_the_claim_text(results):
    """The table's "stated" column keeps the figure as printed ("29"); the sentence
    a reader sees says what it counts ("29 months")."""
    result = results["brasswick"]
    row = find_row(result, "slide 10", "29")
    assert row["kind"] == "runway"
    assert "gives runway as 29 months" in by_id(result)[row["claim id"]].text


# Review wave 2a, S8: a figure the script made from many rows cites the rows it was
# made from (the first and last of the range) and says how it was made.


def test_a_sum_cites_its_range_and_says_how_it_was_made(results):
    result = results["hollis_voice"]
    row = find_row(result, "script line 15", "about three million dollars")
    claim = by_id(result)[row["claim id"]]
    assert "sum of column mrr for 2026-09" in claim.text and "times 12" in claim.text
    assert "sum of column mrr for 2026-09" in row["disagrees"]
    cited = [s.locator for s in claim.sources if s.uri == "03_metrics/customer_mrr_by_month.csv"]
    span = re.search(r"rows (\d+) to (\d+)", claim.text)
    assert span and cited == [f"row {span.group(1)}", f"row {span.group(2)}"], (cited, claim.text)


def test_a_count_cites_its_range_and_says_how_it_was_made(results):
    result = results["brasswick"]
    rows = [r for r in table(result) if r["kind"] == "customers ever" and r["where"].startswith("slide 5")]
    assert rows
    claim = by_id(result)[rows[0]["claim id"]]
    assert "distinct customer_id" in claim.text
    cited = [s.locator for s in claim.sources if s.uri == "03_metrics/revenue_by_customer.csv"]
    assert len(cited) == 2 and cited[0] != cited[1], cited


@pytest.mark.parametrize("room", ["hollis_voice", "brasswick", "hollis_voice_seed_drop", "hollis_voice_clean"])
def test_one_row_per_figure_per_slide_or_line(results, room):
    """Steering's drive showed one figure twice in a section. Two sentences on one slide
    (or one script line) that state the same figure of the same kind are one claim;
    the second is listed as a repeat."""
    # Kinds that list one figure per item (a plan, a spend line, a department) may repeat a value on one slide.
    listed = {"plan limit", "list price", "use of funds", "use of funds share", "planned hires by department",
              "cost as a share of revenue", "other figure"}
    seen = {}
    for r in table(results[room]):
        if r["kind"] in listed:
            continue
        key = (r["where"].split(";")[0].split(" (beat")[0], r["kind"], r["normalised"])
        assert key not in seen, (key, seen.get(key), r["claim id"])
        seen[key] = r["claim id"]
