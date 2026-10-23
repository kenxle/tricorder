"""Reading the operator's one sentence (STEER-R2, R3, R4).

The model path is tested on HAND-BUILT responses: a fake `llm` callable that
returns a SteerReading written in this file. No model is called. There is no
ANTHROPIC_API_KEY in CI.
"""

from __future__ import annotations

import pytest

from clients.llm import ModelRefused
from steering.classify import model_available, read_sentence
from steering.models import SteerReading


@pytest.fixture(autouse=True)
def no_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


@pytest.mark.parametrize("sentence, term", [
    ("treat the pilot as non-recurring", "pilot"),
    ("Treat the pilot as non recurring.", "pilot"),
    ("the pilot isn't recurring", "pilot"),
    ("don't count the pilot as recurring", "pilot"),
    ("exclude the pilot from ARR", "pilot"),
    ("treat onboarding fees as one-time", "onboarding fees"),
])
def test_definition_rewrites(sentence, term):
    r = read_sentence(sentence)
    assert r.kind == "rewrite" and r.path == "rules"
    assert r.term == term and r.treat_as == "non_recurring"
    assert r.number_text is None


@pytest.mark.parametrize("sentence", [
    "read the full room",
    "Read the full room, not the seed drop",
    "use the second tier",
    "open the rest of the room",
])
def test_full_room_is_more_info(sentence):
    r = read_sentence(sentence)
    assert r.kind == "more_info" and r.source == "full_room" and r.path == "rules"


@pytest.mark.parametrize("sentence, named", [
    ("pull the competitor's pricing pages", "competitor's pricing pages"),
    ("find their latest filing", "filing"),
])
def test_named_outside_source_is_more_info(sentence, named):
    r = read_sentence(sentence)
    assert r.kind == "more_info" and r.source == "named"
    assert named in r.source_named


@pytest.mark.parametrize("sentence, number", [
    ("make ARR 3 million", "3 million"),
    ("ARR should be $2,500,000", "$2,500,000"),
    ("set runway to 37 months", "37 months"),
    ("change NRR to 102.6%", "102.6%"),
])
def test_number_requests(sentence, number):
    r = read_sentence(sentence)
    assert r.kind == "rewrite" and r.number_text == number
    assert r.term is None


def test_plain_rewrite_with_no_rule():
    r = read_sentence("say this more plainly")
    assert r.kind == "rewrite" and r.term is None and r.number_text is None and r.source is None


def test_no_key_means_rules(monkeypatch):
    assert not model_available()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setenv("TRICORDER_OFFLINE", "1")
    assert not model_available()
    monkeypatch.delenv("TRICORDER_OFFLINE")
    assert model_available()


# Model path, on hand-built responses -------------------------------------------------


def fake(response):
    calls = []

    def llm(output, **kwargs):
        calls.append(kwargs)
        assert output is SteerReading
        if isinstance(response, Exception):
            raise response
        return response
    llm.calls = calls
    return llm


def test_model_reading_is_used_when_it_holds_to_the_sentence():
    # Hand-built response: what the model would return for this sentence.
    llm = fake(SteerReading(kind="rewrite", definition_term="Marlow pilot", asks_for_number=False, number_text=None,
                            wants_full_room=False, source_named=None))
    r = read_sentence("the Marlow pilot can end on 30 days notice, so it is not ARR", llm=llm)
    assert r.path == "model" and r.term == "marlow pilot" and r.treat_as == "non_recurring"
    assert "the Marlow pilot can end" in llm.calls[0]["task"]


def test_model_naming_a_term_not_in_the_sentence_falls_back_to_rules():
    # Hand-built response that invents a term.
    llm = fake(SteerReading(kind="rewrite", definition_term="onboarding fees", asks_for_number=False, number_text=None,
                            wants_full_room=False, source_named=None))
    r = read_sentence("treat the pilot as non-recurring", llm=llm)
    assert r.path == "rules" and r.term == "pilot"
    assert "onboarding fees" in r.fallback_why


def test_model_inventing_a_number_falls_back():
    llm = fake(SteerReading(kind="rewrite", definition_term=None, asks_for_number=True, number_text="$3,000,000",
                            wants_full_room=False, source_named=None))
    r = read_sentence("make ARR 3 million", llm=llm)
    assert r.path == "rules" and r.number_text == "3 million"


def test_model_refusal_falls_back():
    r = read_sentence("read the full room", llm=fake(ModelRefused("cyber")))
    assert r.path == "rules" and r.kind == "more_info" and "refused" in r.fallback_why


def test_model_more_info():
    llm = fake(SteerReading(kind="more_info", definition_term=None, asks_for_number=False, number_text=None,
                            wants_full_room=True, source_named=None))
    r = read_sentence("we got tier two from the founder, use it", llm=llm)
    assert r.path == "model" and r.kind == "more_info" and r.source == "full_room"


# Negated definitions (review wave 2b, S5) ------------------------------------------------------


@pytest.mark.parametrize("sentence", [
    "Don't treat the pilot as non-recurring",
    "Don’t treat the pilot as non-recurring",
    "do not treat the pilot as one-time",
    "Never treat the pilot as non recurring",
    "please don't exclude the pilot from ARR",
])
def test_a_negated_definition_is_not_read_as_the_definition(sentence):
    r = read_sentence(sentence)
    assert r.term is None and r.treat_as is None and r.kind == "rewrite"


def test_a_negated_definition_still_reads_the_full_room():
    r = read_sentence("do not treat the pilot as non-recurring yet, read the full room")
    assert r.term is None and r.kind == "more_info" and r.source == "full_room"


def test_a_model_definition_on_a_negated_sentence_is_dropped():
    # Hand-built response: a model that misses the "don't".
    llm = fake(SteerReading(kind="rewrite", definition_term="pilot", asks_for_number=False, number_text=None,
                            wants_full_room=False, source_named=None))
    r = read_sentence("Don't treat the pilot as non-recurring", llm=llm)
    assert r.term is None and r.treat_as is None


# A number in a sentence is not by itself a request (review wave 2b, O1) ----------------------


@pytest.mark.parametrize("sentence", [
    "Explain the 37 months of runway in plain words",
    "Say the 2026 plan is aggressive",
    "Mention that 2025 was the first full year",
])
def test_a_number_with_no_request_frame_is_not_a_number_request(sentence):
    assert read_sentence(sentence).number_text is None


@pytest.mark.parametrize("sentence, number", [
    ("use $3M for ARR", "$3M"),
    ("ARR is really 3 million", "3 million"),
    ("runway should read 40 months", "40 months"),
])
def test_more_number_requests(sentence, number):
    assert read_sentence(sentence).number_text == number


# Code review of the fix round ----------------------------------------------------------------------


@pytest.mark.parametrize("sentence, number", [
    # Item 2: in "from A to B" the request is B.
    ("Change ARR from $3M to $2.5M", "$2.5M"),
    ("Update NRR from 120% to 110%", "110%"),
    # Item 3: a four-digit number right after a frame word is a request; the frame reaches the asked number.
    ("Use the 2024 ARR of $2.1M", "$2.1M"),
    ("set the customer count to 2000", "2000"),
])
def test_the_number_asked_for_is_the_one_read(sentence, number):
    assert read_sentence(sentence).number_text == number


def test_a_bare_year_is_still_not_a_request():
    assert read_sentence("the 2026 plan is aggressive").number_text is None


@pytest.mark.parametrize("sentence", [
    "the pilot isn’t recurring",
    "the pilots aren’t recurring",
    "Why not treat the pilot as non-recurring",
])
def test_curly_apostrophes_and_why_not_read_the_definition(sentence):
    # Item 4: U+2019 in "isn't" and "aren't"; "why not" suggests the term, it does not negate it.
    r = read_sentence(sentence)
    assert r.term in ("pilot", "pilots") and r.treat_as == "non_recurring"
