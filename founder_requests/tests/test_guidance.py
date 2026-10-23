"""FR-R3: every guide the checklist names has guidance, tied to sections that exist in the guide."""

import re

from founder_requests import draft as d
from founder_requests import guidance as gd


def _headings(stem):
    text = (gd.GUIDES / f"{stem}.md").read_text(encoding="utf-8")
    return [re.sub(r"^\d+\.\s*", "", h).strip().lower() for h in re.findall(r"^## (.+)$", text, re.M)]


def test_every_checklist_guide_has_guidance():
    named = set(gd.guide_of().values())
    assert named, "checklist.csv names no guides"
    missing = sorted(named - set(gd.GUIDANCE))
    assert not missing, f"guides with no guidance entry: {missing}"


def test_every_entry_is_a_real_guide_with_the_sections_it_draws_on():
    for stem, g in gd.GUIDANCE.items():
        assert (gd.GUIDES / f"{stem}.md").exists(), stem
        heads = _headings(stem)
        for section in set(gd.FROM_SECTIONS.values()):
            assert any(h.startswith(section.lower()) for h in heads), (stem, section)
        assert g.what and g.form and g.good, stem


def test_guidance_words_are_founder_safe():
    for g in gd.GUIDANCE.values():
        text = " ".join([g.title, g.what, g.form, *g.good])
        assert not d.leaks(text), (g.guide, d.leaks(text))
        assert chr(0x2014) not in text and chr(0x2013) not in text, g.guide


def test_for_item_follows_the_checklist_guide_column():
    assert gd.for_item("C22").guide == "hiring-plan-and-future-org"
    assert gd.for_item("C03").title == "Monthly revenue by customer"
    assert gd.for_item(None) is None and gd.for_item("C999") is None
