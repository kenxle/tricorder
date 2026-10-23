import pytest
from pydantic import ValidationError

from schema.claim import PIECE_ORDER, Claim, Gap, Readout, ScanResult


def _claim(**over):
    base = {
        "id": "redflags-001",
        "scan": "redflags",
        "text": "The model counts $2,240,868 of ARR.",
        "value": {"number": 2240868, "unit": "USD", "label": "arr", "period": "2026-09"},
        "check": {"kind": "script", "name": "arr_from_subscription_rows"},
        "confidence": "computed",
        "sources": [{"kind": "file", "uri": "02_financials/financial_model.xlsx", "locator": "ARR_TOTAL", "quote": "2240868"}],
    }
    base.update(over)
    return base


def test_a_claim_validates_and_fills_defaults():
    c = Claim.model_validate(_claim())
    assert c.conflicts_with == [] and c.corroborated_by == [] and c.severity is None


def test_a_claim_with_no_source_is_refused():
    with pytest.raises(ValidationError, match="at least one source"):
        Claim.model_validate(_claim(sources=[]))


def test_extra_fields_are_refused():
    with pytest.raises(ValidationError):
        Claim.model_validate(_claim(probability=0.9))


def test_a_label_outside_the_fixed_list_is_refused():
    with pytest.raises(ValidationError):
        Claim.model_validate(_claim(value={"number": 1, "unit": "USD", "label": "revenue", "period": None}))


def test_a_judged_claim_reads_as_a_reading():
    with pytest.raises(ValidationError, match="Reading:"):
        Claim.model_validate(_claim(confidence="judged"))
    Claim.model_validate(_claim(confidence="judged", text="Reading: the cohort note drops early leavers."))


def test_nine_pieces_in_the_overview_order():
    assert PIECE_ORDER[0] == "traction_and_revenue" and PIECE_ORDER[-1] == "the_pitch_itself"
    assert len(PIECE_ORDER) == 9


def test_result_and_readout_round_trip():
    r = ScanResult(scan="redflags", room="hollis_voice", ran_at="2026-10-24T10:00:00Z",
                   claims=[Claim.model_validate(_claim())],
                   gaps=[Gap(what="Not in the room: bank statements", why="file missing", would_need="Three months of bank statements")])
    assert ScanResult.model_validate_json(r.model_dump_json()) == r
    ro = Readout(room="hollis_voice", built_at="2026-10-24T10:00:00Z", claims=r.claims)
    assert Readout.model_validate_json(ro.model_dump_json()) == ro
