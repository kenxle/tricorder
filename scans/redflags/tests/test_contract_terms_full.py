"""Contract terms in full: FRAMEWORKS.md entry 1.13, checks 1, 3, 4 and 6 and the clause notes.

Each test names the requirement it proves (docs/features/20261023.04_contract_terms/03_prd.md).
Test contracts are made up and built in tmp_path (contract_fixtures.py). Figures in the
asserts are the ones FRAMEWORKS 1.13's worked example states, which a script computed.
"""

from __future__ import annotations

import json
import shutil
import socket
from pathlib import Path

import pytest

from schema.check_quotes import check_claim
from schema.claim import Readout
from scans.base import Ids, write_result
from scans.redflags import contract_reader, contract_terms_full, scan
from scans.redflags.tests.contract_fixtures import (
    CHANGE_OF_CONTROL, HOLLIS, ONE_YEAR, ROOT, THIRTY_DAY, a_counted_customer, copy_room, order_form, write_pdf,
)

ROOMS = ROOT / "data_room"
SEED = ROOMS / "hollis_voice_seed_drop"
CLEAN = ROOMS / "hollis_voice_clean"
BRASS = ROOMS / "brasswick"
MARLOW = "04_customers/pilot_agreement_marlow.pdf"
CEDAR = "04_customers/order_form_cedar_pine.pdf"
BROOK = "04_customers/order_form_brookline_row.pdf"
P3, P4, P1, P6 = ("plan_revenue_past_term_end", "signed_not_live_vs_revenue", "cancellable_within_notice_vs_arr",
                  "counted_line_without_contract")

_CACHE: dict = {}


def run(room: Path):
    key = str(room)
    if key not in _CACHE:
        _CACHE[key] = contract_terms_full.check(room, Ids("redflags"))
    return _CACHE[key]


def claims_for(claims, check_name, uri=None):
    return [c for c in claims if c.check.name == check_name and (uri is None or any(s.uri == uri for s in c.sources))]


def panel(panels, name):
    return next(p for p in panels if p.name == name)


# ----------------------------------------------------------------------------- check 3 (CT-R3)


def test_plan_check_flags_marlow_with_its_eight_plan_months():
    claims, _gaps, _p = run(HOLLIS)
    marlow = claims_for(claims, P3, MARLOW)
    assert len(marlow) == 1
    c = marlow[0]
    assert c.severity == "flag" and c.confidence == "computed"
    assert "8 plan months" in c.text and "2027-02 to 2027-09" in c.text
    assert "no renewal clause" in c.text
    assert round(c.value.number) == 161258 and c.value.unit == "USD" and c.value.label == "other"
    assert "$17,815" in c.text and "8.0%" in c.text
    assert any(s.uri == "02_financials/financial_model.xlsx" and s.locator == "Assumptions!B18" for s in c.sources)


def test_plan_check_clears_cedar_pine_and_brookline_row():
    claims, _gaps, _p = run(HOLLIS)
    cedar, brook = claims_for(claims, P3, CEDAR), claims_for(claims, P3, BROOK)
    assert cedar and brook
    assert all(c.severity == "info" for c in cedar + brook)
    assert any("2027-08-02" in c.text for c in cedar)       # last day to give notice, inside the plan window
    assert any("0.31%" in c.text for c in brook)            # below the 1 percent line
    assert any("$3,355" in c.text for c in brook)


# ----------------------------------------------------------------------------- check 4 (CT-R4)


def test_signed_not_live_clears_the_three_hollis_contracts():
    claims, _gaps, _p = run(HOLLIS)
    for uri in (MARLOW, CEDAR, BROOK):
        found = claims_for(claims, P4, uri)
        assert found and all(c.severity == "info" for c in found), uri
    assert any("2026-04" in c.text and "$36,000" in c.text for c in claims_for(claims, P4, CEDAR))


def test_signed_not_live_flags_revenue_before_the_effective_date(tmp_path):
    room = copy_room(tmp_path)
    name, _mrr = a_counted_customer(room)
    write_pdf(room / "04_customers" / "order_form_test_late.pdf",
              order_form(name, term_line="Term 12 months, from 2026-10-01 to 2027-09-30.", termination=ONE_YEAR,
                         effective="2026-10-01"))
    claims, _g, _p = contract_terms_full.check(room, Ids("redflags"))
    hit = claims_for(claims, P4, "04_customers/order_form_test_late.pdf")
    assert [c.severity for c in hit] == ["flag"]
    assert "2026-10" in hit[0].text


# ----------------------------------------------------------------------------- check 6 (CT-R5, CT-R6)


def test_counted_lines_without_contract_are_seven_gaps():
    _claims, gaps, _p = run(HOLLIS)
    line_gaps = [g for g in gaps if g.what.startswith("Not in the room: the contract for ")]
    assert len(line_gaps) == 7
    assert any(g.what == "Not in the room: the contract for Subscriptions signed 2025 Q1 (13 customers)" for g in line_gaps)
    assert not any("Marlow" in g.what for g in line_gaps)
    assert all(g.piece == "customers" for g in line_gaps)
    # The ask line the memo turns it into asks for the current contract language.
    assert all("current customer contract language" in g.would_need for g in line_gaps)


def test_coverage_claim_is_27_6_percent():
    claims, _g, _p = run(HOLLIS)
    cov = claims_for(claims, P6)
    assert len(cov) == 1
    assert "$51,584" in cov[0].text and "$186,739" in cov[0].text and "27.6%" in cov[0].text
    assert cov[0].severity == "info"


def test_missing_contracts_become_ask_lines_through_the_memo(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path / "out"))
    from scans.memo.merge import build_readout

    write_result(scan.run(HOLLIS), HOLLIS)
    readout: Readout = build_readout(HOLLIS)
    asks = [a for a in readout.asks if "current customer contract language" in a.what]
    assert any("Subscriptions signed 2025 Q1" in a.what for a in asks)
    assert all(a.from_kind == "gap" and a.checklist_id == "C34" for a in asks)


# ----------------------------------------------------------------------------- clauses (CT-R7, CT-R8)


def test_clause_fields_are_not_stated_on_hollis_read_from_each_contract():
    claims, _g, panels = run(HOLLIS)
    terms = panel(panels, "contract terms")
    for uri in (MARLOW, CEDAR, BROOK):
        rows = {r[1]: r for r in terms.rows if r[0] == uri}
        for fld in ("exclusivity", "most_favoured_customer", "change_of_control"):
            assert rows[fld][2] == "not_stated", (uri, fld)
        note = [c for c in claims_for(claims, "clause_notes", uri) if "no exclusivity" in c.text]
        assert len(note) == 1
        pages = {s.locator for s in note[0].sources if s.uri == uri}
        n_pages = len(contract_reader.pdf_pages(HOLLIS / uri))
        assert pages == {f"page {i}" for i in range(1, n_pages + 1)}, "every page is cited as read"


def test_change_of_control_clause_returns_its_quote(tmp_path):
    room = copy_room(tmp_path)
    name, _ = a_counted_customer(room)
    uri = "04_customers/order_form_test_coc.pdf"
    write_pdf(room / uri, order_form(name, term_line="Term 12 months, from 2026-06-01 to 2027-05-31.",
                                     termination=ONE_YEAR, extra=CHANGE_OF_CONTROL))
    claims, _g, _p = contract_terms_full.check(room, Ids("redflags"))
    coc = [c for c in claims_for(claims, "clause_notes", uri) if "change-of-control clause" in c.text]
    assert len(coc) == 1
    q = coc[0].sources[0].quote
    assert q.startswith("3. Change of control.") and "is acquired by another company" in q
    assert coc[0].confidence == "quoted"
    assert check_claim(coc[0], room)[1] == []
    # The change-of-control exit is not read as a right to leave for any reason.
    assert not [c for c in claims_for(claims, P1, uri) if c.severity == "flag"]


def test_fee_freeze_is_an_other_clause_on_cedar_pine():
    claims, _g, _p = run(HOLLIS)
    notes = [c for c in claims_for(claims, "clause_notes", CEDAR) if "holds the fees fixed" in c.text]
    assert notes and notes[0].sources[0].quote == "Fees are fixed for the initial term."


# ----------------------------------------------------------------------------- check 1 (CT-R9)


def _thirty_day_room(tmp_path, committed: bool):
    room = copy_room(tmp_path, "room_committed" if committed else "room_30day")
    name, mrr = a_counted_customer(room)
    term = "Term 12 months, from 2026-06-01 to 2027-05-31." if committed else "Term month to month."
    uri = "04_customers/order_form_test_30day.pdf"
    write_pdf(room / uri, order_form(name, term_line=term, termination=ONE_YEAR if committed else THIRTY_DAY))
    return room, uri, mrr


def test_thirty_day_cancellation_counted_as_a_year_of_arr_is_flagged(tmp_path):
    room, uri, mrr = _thirty_day_room(tmp_path, committed=False)
    claims, _g, _p = contract_terms_full.check(room, Ids("redflags"))
    hit = claims_for(claims, P1, uri)
    assert [c.severity for c in hit] == ["flag"]
    assert "30 days" in hit[0].text and f"${12 * mrr:,.0f}" in hit[0].text


def test_one_year_commitment_is_not_flagged(tmp_path):
    room, uri, _ = _thirty_day_room(tmp_path, committed=True)
    claims, _g, _p = contract_terms_full.check(room, Ids("redflags"))
    hit = claims_for(claims, P1, uri)
    assert hit and all(c.severity == "info" for c in hit)


def test_notice_check_on_hollis_flags_marlow_only():
    claims, _g, _p = run(HOLLIS)
    flagged = {s.uri for c in claims_for(claims, P1) if c.severity in ("flag", "watch") for s in c.sources}
    assert MARLOW in flagged and CEDAR not in flagged and BROOK not in flagged


# ----------------------------------------------------------------------------- inputs (CT-R1, CT-R2, CT-R10)


def test_a_folder_of_only_contracts_is_read_with_no_crash(tmp_path):
    folder = tmp_path / "uploaded_contracts"
    folder.mkdir()
    for i, uri in enumerate((MARLOW, CEDAR, BROOK)):
        shutil.copyfile(HOLLIS / uri, folder / f"contract_{i}.pdf")   # names the room patterns do not know
    claims, gaps, panels = contract_terms_full.check(folder, Ids("redflags"))
    assert len({r[0] for r in panel(panels, "contract terms").rows}) == 3
    assert any(g.what == "Not in the room: the ARR build or the customer file to compare with" for g in gaps)
    assert claims_for(claims, "clause_notes")
    result = scan.run(folder)   # the whole engine on the folder
    assert any(c.check.name == "clause_notes" for c in result.claims)


def test_seed_drop_has_no_contracts_and_says_so():
    claims, gaps, _p = run(SEED)
    assert claims == []
    assert [g.what for g in gaps] == ["Not in the room: customer contracts"]


def test_a_pdf_that_cannot_be_read_is_a_gap(tmp_path):
    room = copy_room(tmp_path)
    (room / "04_customers" / "order_form_broken.pdf").write_bytes(b"%PDF-1.4 not really")
    claims, gaps, _p = contract_terms_full.check(room, Ids("redflags"))
    assert any("a readable copy of 04_customers/order_form_broken.pdf" in g.what for g in gaps)
    assert claims_for(claims, P3, MARLOW)


def test_supplier_contract_gets_no_customer_checks():
    claims, gaps, panels = run(BRASS)
    sow = "04_contracts/sow_norrgate_software_studio.pdf"
    assert not [c for c in claims if c.check.name in (P1, P3, P4) and any(s.uri == sow for s in c.sources)]
    assert not any("Norrgate" in g.what for g in gaps)
    assert any(r[0] == sow for r in panel(panels, "contract terms").rows)


# ----------------------------------------------------------------------------- the shared reader (CT-R11)


def test_each_contract_is_read_once_for_both_modules(monkeypatch):
    calls = []
    real = contract_reader.read_contract
    monkeypatch.setattr(contract_reader, "read_contract", lambda p, r: calls.append(p) or real(p, r))
    contract_reader._CACHE.clear()
    contract_terms_full.check(HOLLIS, Ids("redflags"))
    contract_reader.read_room(HOLLIS)   # what Saturday's module calls
    assert len(calls) == 3


def test_a_model_reader_plugs_in_and_a_failed_one_falls_back(monkeypatch):
    # Hand-built model reading, labelled as such: the script's own reading of Cedar & Pine,
    # with read_by set to "model". No model is called.
    real = contract_reader.read_room(HOLLIS).contracts
    hand_built = [c.model_copy(update={"read_by": "model"}) for c in real if c.uri == CEDAR]
    contract_reader.set_model_reader(lambda room, paths: hand_built)
    try:
        got = contract_reader.read_room(HOLLIS)
        assert got.read_by == "model" and [c.uri for c in got.contracts] == [CEDAR]

        def broken(room, paths):
            raise RuntimeError("no key")

        contract_reader.set_model_reader(broken)
        got = contract_reader.read_room(HOLLIS)
        assert got.read_by == "script" and len(got.contracts) == 3
        assert any("model reading failed: no key" in g.why for g in got.gaps)
    finally:
        contract_reader.set_model_reader(None)


# ----------------------------------------------------------------------------- every quote (CT-R12)


@pytest.mark.parametrize("room", [HOLLIS, CLEAN, BRASS, SEED], ids=lambda p: p.name)
def test_every_quote_passes_the_quote_checker(room):
    claims, _g, _p = run(room)
    for c in claims:
        assert check_claim(c, room)[1] == [], c.id


def test_every_quote_passes_on_the_test_contracts(tmp_path):
    room = copy_room(tmp_path)
    name, _ = a_counted_customer(room)
    write_pdf(room / "04_customers/order_form_test.pdf",
              order_form(name, term_line="Term month to month.", termination=THIRTY_DAY, extra=CHANGE_OF_CONTROL))
    claims, _g, _p = contract_terms_full.check(room, Ids("redflags"))
    assert claims
    for c in claims:
        assert check_claim(c, room)[1] == [], c.id


# ----------------------------------------------------------------------------- the engine (CT-R13)


def test_the_engine_lists_the_module_and_leaves_saturdays_name_free():
    assert "contract_terms_full" in scan.CHECKS and "contract_terms" in scan.CHECKS
    assert not (Path(scan.__file__).parent / "contract_terms.py").exists()


def test_no_decoy_is_flagged_and_claim_ids_are_unique():
    result = scan.run(HOLLIS)
    ids = [c.id for c in result.claims]
    assert len(ids) == len(set(ids))
    flags = [c for c in result.claims if c.severity == "flag"]
    assert not any(s.uri == BROOK for c in flags for s in c.sources)
    assert not any(s.locator in ("ARR_Build!A14", "ARR_Build!E14") for c in flags for s in c.sources)


def test_runs_offline(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("network call")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    contract_reader._CACHE.clear()
    contract_terms_full.check(HOLLIS, Ids("redflags"))


def test_result_serialises():
    claims, gaps, panels = run(HOLLIS)
    json.dumps([c.model_dump() for c in claims] + [g.model_dump() for g in gaps] + [p.model_dump() for p in panels])
