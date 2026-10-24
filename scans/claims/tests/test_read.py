"""The model reading of slides with no parseable figure.

There is no ANTHROPIC_API_KEY here and no test calls a model. The responses
below are HAND-BUILT test data in the SlideFacts shape, not recorded model
output. They go through scan.run, the function the command line calls, with
clients.llm.read replaced.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import clients.llm
from schema.check_quotes import check_result
from scans.claims import scan
from scans.claims.read import SlideFact, SlideFacts

ROOM = Path(__file__).resolve().parents[3] / "data_room" / "hollis_voice"

HAND_BUILT = SlideFacts(facts=[
    # Slide 9 holds no figure; this fact's quote is on it, word for word.
    SlideFact(slide=9, quote="Built for vet clinics: vaccine", kind="other", number=None),
    # A quote the slide does not hold: the script must drop it.
    SlideFact(slide=9, quote="Hollis Voice has 500 vet clinic customers", kind="customers_now", number=500),
    # A number the quote does not state: dropped.
    SlideFact(slide=2, quote="Front desks are busy with people at the counter,", kind="other", number=12),
])


@pytest.fixture
def fake_model(monkeypatch, tmp_path):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-used")
    calls = []

    def fake_read(output, **kwargs):
        calls.append(kwargs)
        assert output is SlideFacts
        return HAND_BUILT

    monkeypatch.setattr(clients.llm, "read", fake_read)
    return calls


def test_model_facts_are_kept_only_when_quote_and_number_check_out(fake_model):
    result = scan.run(ROOM)
    assert len(fake_model) == 1
    sent = "\n".join(fake_model[0]["docs"])
    assert 'locator="slide 2"' in sent and 'locator="slide 9"' in sent
    assert 'locator="slide 3"' not in sent           # slides with figures never go to the model
    assert fake_model[0]["check_name"] == "claim_extract"
    assert fake_model[0]["knowledge"].startswith('<expert_knowledge piece="traction_and_revenue">')
    model_claims = [c for c in result.claims if "read by the model" in c.text]
    assert [c.sources[0].quote for c in model_claims] == ["Built for vet clinics: vaccine"]
    assert model_claims[0].text.startswith("Unsupported:")
    assert (model_claims[0].confidence, model_claims[0].check.kind, model_claims[0].check.name) == ("quoted", "model", "claim_support.read")
    assert any("2 model readings" in g.what for g in result.gaps)
    assert check_result(result, ROOM)[1] == {}


def test_no_key_is_a_gap_not_a_call(monkeypatch, tmp_path):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(clients.llm, "read", lambda *a, **k: pytest.fail("the model was called without a key"))
    result = scan.run(ROOM)
    gap = next(g for g in result.gaps if "model reading" in g.what)
    assert gap.why == "no ANTHROPIC_API_KEY, so the model reading did not run"
    assert "slides 2, 9" in gap.what


def test_refusal_is_a_gap(monkeypatch, tmp_path):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-used")

    def refuse(*a, **k):
        raise clients.llm.ModelRefused("policy")

    monkeypatch.setattr(clients.llm, "read", refuse)
    result = scan.run(ROOM)
    assert any("the model refused (policy)" in g.why for g in result.gaps)
