"""The memo page's structure: the one-screen summary, grouped sections, figures read from the claims.

Structure is checked through classes and data attributes, never through wording.
Every expectation comes from the memo the readout builds, so a new check never breaks these.
"""

from __future__ import annotations

import html
import re

from memo.build import build_memo
from memo.figures import flag_figures, fmt, said_in_room
from memo.html import FIRST_ASKS, render_html, top_asks
from memo.tests.conftest import ROOM, with_pieces

AT = "2026-10-23T12:00:00Z"


def page_of(memo) -> str:
    return render_html(memo)


def without_data(page: str) -> str:
    return re.sub(r'<script type="application/json" id="memo-data">.*?</script>', "", page, flags=re.S)


def reds(memo):
    return [ln for ln in memo.section(2).lines if ln.severity == "red" and ln.kind == "claim"]


def test_the_first_screen_runs_round_flags_green_then_asks(readout):
    memo = build_memo(readout, ROOM, AT)
    page = page_of(memo)
    marks = ['data-round', 'data-group="red-flags"', 'data-panel="green"', 'data-panel="ask"', 'id="s03"']
    at = [page.index(m) for m in marks]
    assert at == sorted(at), marks
    for ln in reds(memo):
        assert re.search(rf'<li class="[^"]*flag-row[^"]*" data-line-id="{re.escape(ln.id)}"', page), ln.id


def test_each_red_flag_shows_figures_read_from_its_claims(readout):
    memo = build_memo(readout, ROOM, AT)
    page = page_of(memo)
    paired = 0
    for ln in reds(memo):
        figs = flag_figures(memo, ln)
        claims = [memo.claims[c] for c in ln.claim_ids]
        known = {round(c.value.number, 2) for c in claims if c.value}
        known |= {round(memo.claims[o].value.number, 2) for c in claims for o in c.conflicts_with
                  if o in memo.claims and memo.claims[o].value}
        known |= {round(n, 2) for c in claims for n, _ in said_in_room(c)}
        for f in figs:
            assert round(f.number, 2) in known, (ln.id, f)
        roles = {f.role for f in figs}
        if {"stated", "found"} <= roles:
            paired += 1
            row = page.split(f'data-line-id="{ln.id}"', 1)[1].split("</li>", 1)[0]
            assert "data-strip" in row
            for role in ("stated", "found"):
                shown = re.search(rf'data-figure="{role}"[^>]*>([^<]+)<', row).group(1)
                assert html.unescape(shown) in {fmt(f.number, f.unit) for f in figs if f.role == role}
    assert paired, "no red flag had both a stated and a found figure"


def test_sections_group_their_lines_and_unassessed_sections_are_one_row(readout):
    memo = build_memo(readout, ROOM, AT)
    page = page_of(memo)
    for s in memo.sections[2:]:
        body = page.split(f'id="s{s.number:02d}"', 1)[1].split("</section>", 1)[0]
        if s.collapsed:
            assert 'class="collapsed-row"' in body and 'class="group' not in body, s.title
        # Every line in the section is on the page exactly once, as a row.
        for ln in s.lines:
            assert body.count(f'data-line-id="{ln.id}"') == 1, ln.id
    # The pitch's one-by-one claim lines are a compact operator table, not partner sentences.
    for row in re.findall(r'<li class="([^"]*pitch-claim[^"]*)"', page):
        assert "aud-operator" in row


def test_the_ask_panel_lists_the_first_asks_without_if_you_have_it(readout):
    memo = build_memo(readout, ROOM, AT)
    picked = top_asks(memo)
    assert 0 < len(picked) <= FIRST_ASKS
    assert not any(memo.asks[aid].if_you_have_it for aid, _ in picked)
    keys = [memo.asks[aid].checklist_id or aid for aid, _ in picked]
    assert len(keys) == len(set(keys))
    panel = page_of(memo).split('data-panel="ask"', 1)[1].split("</article>", 1)[0]
    assert re.findall(r'data-ask-id="([^"]+)"', panel) == [aid for aid, _ in picked]
    assert not re.search(r"\(C\d\d\)", panel)


def test_the_coverage_bar_counts_every_checklist_row(readout):
    memo = build_memo(readout, ROOM, AT)
    page = page_of(memo)
    counts = [int(n) for n in re.findall(r'class="seg [^"]*"[^>]*data-count="(\d+)"', page)]
    assert sum(counts) == len(memo.checklist)


def test_a_real_green_flag_takes_the_green_panel(readout):
    memo = build_memo(with_pieces(readout), ROOM, AT)
    green = next(ln for ln in memo.section(2).lines if ln.severity == "green")
    panel = page_of(memo).split('data-panel="green"', 1)[1].split("</article>", 1)[0]
    assert f'data-line-id="{green.id}"' in panel


def test_until_then_the_round_takes_the_green_panel(readout):
    memo = build_memo(readout, ROOM, AT)
    panel = page_of(memo).split('data-panel="green"', 1)[1].split("</article>", 1)[0]
    assert 'data-line-id="s01-round"' in panel


def test_the_page_chrome_keeps_to_the_brand_words(readout):
    memo = build_memo(readout, ROOM, AT)
    page = without_data(page_of(memo))
    for s in memo.sections:
        for ln in s.lines:
            for t in (ln.text, ln.label or ""):
                if t:
                    page = page.replace(html.escape(t, quote=True), "")
    text = re.sub(r"<style>.*?</style>|<script>.*?</script>|<[^>]+>", " ", page, flags=re.S)
    assert "—" not in page and "–" not in page
    assert not re.search(r"\b(verified|invest|fraud|insights?|recommend)\b", text, re.I)
    assert not re.search(r"(?<!first )\bpass\b(?!-)", text, re.I)
    # No synthetic banner: the notice shows once, in the footer.
    assert page.count('class="synthetic"') == 1
