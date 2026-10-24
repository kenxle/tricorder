"""The expert-read report sections on the memo page: five short parts and a chart.

    report_block(report, memo) -> HTML for one section's report (scans/memo/sections.py)
    for_page(reports, memo) -> the reports with each sentence's claims cut to the memo's own

The sentences are rows like the memo's other lines: one click opens the claims
behind a sentence, from the memo's own data. The chart is drawn by the page's
script with plotly.js, loaded from the file beside the page (PLOTLY_FILE),
never from a CDN. Without that file the chart's data and sources still show
in the table under it.
"""

from __future__ import annotations

import html
from pathlib import Path

from memo.figures import fmt
from memo.model import Memo, MemoLine

PLOTLY_VERSION = "2.35.2"
PLOTLY_FILE = f"plotly-{PLOTLY_VERSION}.min.js"
PLOTLY_PATH = Path(__file__).with_name("page") / "vendor" / PLOTLY_FILE

BY = {
    "model": "Written by the model with Kimmy's expert knowledge in its prompt. Every sentence cites the claims "
             "it rests on, and every figure is copied from those claims.",
    "script": "Drafted by a script from the claims' own sentences and Kimmy's rules, because no model ran. "
              "With a model key, the model writes this section with her knowledge in its prompt.",
}


def _e(text) -> str:
    return html.escape("" if text is None else str(text), quote=True)


def for_page(reports: list, memo: Memo) -> list:
    """Each sentence keeps only claims the memo holds (the quote checker passed them); a sentence left
    with none is not shown."""
    out = []
    for r in reports:
        r = r.model_copy(deep=True)
        for part in r.parts:
            kept = []
            for s in part.sentences:
                s.claim_ids = [c for c in s.claim_ids if c in memo.claims]
                if s.claim_ids:
                    kept.append(s)
            part.sentences = kept
        if any(p.sentences for p in r.parts) or r.chart:
            out.append(r)
    return out


def _sentence_row(s, section: int) -> str:
    from memo.html import _cell, _row, _text

    line = MemoLine(id=s.id, kind="claim", text=s.text, claim_ids=s.claim_ids)
    return _row(line, section, [_cell("c-text", _text(line))], "xr-row")


def _value(v: float, unit: str) -> str:
    return fmt(v, unit)


def _data_table(chart: dict) -> str:
    unit = chart.get("unit", "USD")
    rows = []
    for s in chart.get("series", []):
        last = f"{s['x'][-1]}: {_value(s['y'][-1], unit)}" if s.get("x") else ""
        srcs = s.get("sources") or [s["source"]]
        where = "; ".join(f"{x['file']}, {x['locator']}" for x in srcs)
        rows.append(f"<tr><td>{_e(s['name'])}</td><td class=\"mono\">{_e(last)}</td><td class=\"mono\">{_e(where)}</td></tr>")
    for m in chart.get("markers", []):
        rows.append(f"<tr><td>{_e(m['name'])}</td><td class=\"mono\">{_e(m['x'])}: {_e(_value(m['y'], unit))}</td>"
                    f"<td class=\"mono\">{_e(m['source']['file'])}, {_e(m['source']['locator'])}</td></tr>")
    for ln in chart.get("lines", []):
        rows.append(f"<tr><td>{_e(ln['name'])}</td><td class=\"mono\">{_e(ln['x'])}"
                    f"{' (' + _e(ln['months']) + ' months)' if ln.get('months') else ''}</td>"
                    f"<td class=\"mono\">{_e(ln['source']['file'])}, {_e(ln['source']['locator'])}</td></tr>")
    return ('<details class="xr-data"><summary>The chart\'s data and where each line comes from</summary>'
            '<table><thead><tr><th>Line</th><th>Latest</th><th>Source</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></details>')


def caption(chart: dict) -> str:
    """One plain sentence under the chart, from the chart's own script data."""
    unit = chart.get("unit", "USD")
    if chart.get("kind") == "revenue_over_time":
        s = chart["series"][0]
        parts = [f"The metrics file shows {_value(s['y'][-1], unit)} for {s['x'][-1]}"]
        if len(chart["series"]) > 1:
            r = chart["series"][1]
            parts.append(f"the customer file's subscription rows add to {_value(r['y'][-1], unit)}")
        for m in chart.get("markers", []):
            parts.append(f"{m['name'][:1].lower() + m['name'][1:]} states {_value(m['y'], unit)}")
        return "; ".join(parts) + "."
    lines = {ln["role"]: ln for ln in chart.get("lines", [])}
    out = []
    if "plan" in lines:
        out.append(f"Under the company's plan the cash lasts to {lines['plan']['x']} ({lines['plan']['months']} months)")
    if "found" in lines:
        out.append(f"with the burn the checks found, to {lines['found']['x']} ({lines['found']['months']} months)")
    if "baseline" in lines:
        b = lines["baseline"]
        out.append(f"Kimmy's baseline of {b['months']} months after the round closes ({b['close']}) is {b['x']}")
    found = next((s for s in chart.get("series", []) if s.get("role") == "found"), None)
    text = "; ".join(out) + "." if out else ""
    if found and found.get("what"):
        text += f" The second line: {found['what']}"
    return text


def report_block(report, memo: Memo) -> str:
    n = report.section
    parts = []
    for p in report.parts:
        if not p.sentences:
            continue
        rows = "".join(_sentence_row(s, n) for s in p.sentences)
        parts.append(f'<div class="group xr-part xr-{p.key}" data-group="xr-{p.key}"><h4 class="group-h">{_e(p.heading)}</h4>'
                     f'<ul class="lines rows">{rows}</ul></div>')
    chart = ""
    if report.chart:
        cid = f"xr-plot-{report.piece}"
        chart = (f'<figure class="xr-chart"><figcaption class="t-4">{_e(report.chart["title"])}</figcaption>'
                 f'<div class="xr-plot" id="{cid}" data-piece="{_e(report.piece)}" role="img" '
                 f'aria-label="{_e(report.chart["title"])}. {_e(caption(report.chart))}"></div>'
                 f'<p class="xr-cap">{_e(caption(report.chart))}</p>{_data_table(report.chart)}</figure>')
    dropped = ""
    if report.dropped:
        items = "".join(f"<li>{_e(d.text)} <span class=\"muted\">({_e(d.why)})</span></li>" for d in report.dropped)
        dropped = (f'<details class="xr-dropped aud-operator"><summary>{len(report.dropped)} sentence'
                   f'{"s" if len(report.dropped) != 1 else ""} dropped by the citation check</summary><ul>{items}</ul></details>')
    note = f'<p class="xr-note">{_e(report.note)}</p>' if report.note else ""
    return (f'<div class="xr" data-report="{_e(report.piece)}">'
            f'<div class="xr-head"><p class="eyebrow">Expert read</p><h3 class="t-3">{_e(report.title)}</h3>'
            f'<p class="xr-by">{_e(BY[report.written_by])}</p>{note}</div>'
            f'{chart}<div class="xr-parts">{"".join(parts)}</div>{dropped}</div>')
