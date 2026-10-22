from pathlib import Path

from schema.check_quotes import check_claim
from schema.claim import Claim

ROOM = Path(__file__).resolve().parents[2] / "data_room" / "hollis_voice"


def _claim(uri, locator, quote):
    return Claim.model_validate({
        "id": "t-001", "scan": "test", "text": "A test claim.",
        "check": {"kind": "script", "name": "test"}, "confidence": "computed",
        "sources": [{"kind": "file", "uri": uri, "locator": locator, "quote": quote}],
    })


def test_a_real_quote_passes():
    claim, problems = check_claim(_claim("01_overview/pitch_deck.pdf", "slide 4", "No customer above 9% of ARR"), ROOM)
    assert problems == [] and claim.confidence == "computed"


def test_spacing_and_case_are_ignored():
    _, problems = check_claim(_claim("01_overview/pitch_deck.pdf", "slide 4", "no   customer above 9%\nof arr"), ROOM)
    assert problems == []


def test_a_spreadsheet_number_matches_with_commas():
    _, problems = check_claim(_claim("02_financials/financial_model.xlsx", "ARR_TOTAL", "2,240,868"), ROOM)
    assert problems == []


def test_an_invented_quote_fails_and_is_marked_unverified():
    claim, problems = check_claim(_claim("01_overview/pitch_deck.pdf", "slide 4", "Our churn is zero"), ROOM)
    assert claim.confidence == "unverified" and problems


def test_the_right_quote_at_the_wrong_slide_fails():
    claim, _ = check_claim(_claim("01_overview/pitch_deck.pdf", "slide 5", "No customer above 9% of ARR"), ROOM)
    assert claim.confidence == "unverified"


def test_a_missing_file_fails_without_crashing():
    claim, problems = check_claim(_claim("99_nothing/none.pdf", "page 1", "x"), ROOM)
    assert claim.confidence == "unverified" and "does not exist" in problems[0]
