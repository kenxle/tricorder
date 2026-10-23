"""The number parser: every printed or spoken figure in the rooms' decks and scripts."""

from scans.claims.numbers import mentions, parse_spoken, words_to_number


def _one(text):
    found = mentions(text)
    assert len(found) == 1, found
    return found[0]


def test_currency_with_suffix():
    m = _one("$2.5M")
    assert (m.number, m.unit, m.printed) == (2_500_000, "USD", "$2.5M")
    assert m.precision == 100_000


def test_currency_thousands_suffix():
    m = _one("$943K")
    assert m.number == 943_000 and m.precision == 1000


def test_currency_plain():
    m = _one("We are raising $9,000,000 in a Series A")
    assert m.number == 9_000_000 and m.unit == "USD" and m.precision == 1


def test_percent_and_decimal():
    assert _one("102.6%").number == 102.6
    assert _one("80%").unit == "percent"


def test_plain_with_unit_word():
    m = _one("37 months")
    assert (m.number, m.unit_word) == (37, "months")


def test_iso_date_and_month_year():
    found = mentions("Data as of 2026-09-30")
    assert [(m.kind_hint, m.printed) for m in found] == [("date", "2026-09-30")]
    found = mentions("We started charging in January 2025.")
    assert [(m.kind_hint, m.printed, m.iso) for m in found] == [("month", "January 2025", "2025-01")]


def test_slide_footer_and_times_are_not_mentions():
    assert mentions("Synthetic data room for Deal Flow NYC 2026. Not a real company. Slide 3 of 14") == []
    assert mentions("Example call, Tuesday 4:47 pm") == []


def test_number_words():
    assert words_to_number("three million") == 3_000_000
    assert words_to_number("twenty-four") == 24
    assert words_to_number("one hundred") == 100
    assert words_to_number("eleven") == 11


def test_spoken_mentions_keep_hedge():
    m = _one("Today we're at about three million dollars in annual recurring revenue.")
    assert (m.number, m.unit, m.hedge, m.spoken) == (3_000_000, "USD", "about", True)
    m = _one("Net revenue retention is a little over one hundred percent, so")
    assert (m.number, m.unit, m.hedge, m.bound) == (100, "percent", "a little over", "min")
    m = _one("and it is still under nine percent of ARR.")
    assert (m.number, m.bound) == (9, "max")


def test_spoken_years_become_months_only_in_normalising():
    m = _one("that gives us close to three years of runway.")
    assert (m.number, m.unit_word, m.hedge) == (3, "years", "close to")


def test_number_word_needs_a_unit():
    # "one-room practices" and "one location" style words without a counted unit stay out,
    # except where a unit noun follows.
    assert mentions("from one-room practices to hospital groups") == []
    assert _one("One location, basic call answering").number == 1


def test_digits_bound_words():
    m = _one("No customer above 9% of ARR")
    assert (m.number, m.bound) == (9, "max")
    m = mentions("Largest customer under 9% of ARR 4")[0]  # the trailing 4 is the slide reference
    assert m.bound == "max"


def test_several_mentions_in_order():
    found = mentions("At $45,000,000 pre-money, for 16.67% of the company.")
    assert [m.number for m in found] == [45_000_000, 16.67]
    found = mentions("Staff grows from 17 to 41.")
    assert [m.number for m in found] == [17, 41]


def test_parse_spoken_value():
    assert parse_spoken("nine million dollars") == (9_000_000, "USD")
