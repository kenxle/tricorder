"""The interactive memo: one self-contained HTML page, no script or stylesheet from a CDN.

Two views of one memo. The partner view is the default. Its first screen is
the answer: the round, the red flags with what the pitch states beside what
the room shows, the best supported figure, and what to ask the founder. It
shows no plumbing: no check names, claim ids, checklist numbers, blanks or
commands. The operator view (the toggle in the top bar) shows all of it, and,
when the server serves the page, lets the operator edit in place and save
many changes as one new version.

Each section groups its lines instead of listing them one by one: the red
flags that touch it, what the checks found (with where), the pitch's figures,
what is not in the room, and the checklist line at its foot. A section with
nothing assessed is one muted line.

The lines are written into the page as HTML, so it reads top to bottom with
no script. The drill-downs are built by the inline script from the memo's
JSON, embedded in the page:

    one click on a line   -> the claims behind it (or, for a gap, its checklist item and ask line)
    one more on a claim   -> its sources, read as a partner reads them and in place with the quote
                             marked, and the claims that agree or disagree, with theirs

The look is direction F, "Instrument" (docs/features/20261022.05_style_directions/round_2/direction_f).
The stylesheet and the script live beside this file in memo/page/.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

from memo.figures import Figure, flag_figures, fmt, position, scale, short
from memo.model import Memo, MemoLine, MemoSection
from memo.template import LABEL_WORDS, STAGE_WORDS

PAGE_DIR = Path(__file__).with_name("page")

KIND_WORDS = {
    "claim": "Claim", "reading": "Reading", "gap": "Gap", "operator": "Operator", "slot": "Operator writes",
    "pieces": "Piece", "coverage": "Checklist", "ask": "Ask", "unverified": "Could not verify",
    "fact": "", "source": "Source", "change": "Change", "scenario": "Scenario", "ref": "",
}


HEAD_LABELS = ("To", "Date", "Re", "Room data", "Version")

# How many asks the first screen lists; the rest are in section 14.
FIRST_ASKS = 5


def _e(text: str | None) -> str:
    return html.escape(text or "", quote=True)


def recommendation(memo: Memo) -> MemoLine | None:
    """The operator's recommendation, from section 15, for the top of the summary."""
    lines = [ln for ln in memo.section(15).lines if ln.kind == "operator"]
    if not lines:
        return None
    first = lines[0]
    return first.model_copy(update={"id": "s02-recommendation", "label": "Recommendation",
                                    "text": " ".join(ln.text for ln in lines)})


def visible(section: MemoSection, view: str) -> list[MemoLine]:
    """The lines a view shows. The PDF uses the partner view without the page-only lines."""
    if view == "operator":
        return section.lines
    keep = ("all", "page") if view == "partner" else ("all",)
    return [ln for ln in section.lines if ln.audience in keep]


def _drillable(line: MemoLine) -> bool:
    if line.kind in ("fact", "slot", "change", "scenario"):
        return False
    if line.kind == "gap":
        return True
    return bool(line.claim_ids or line.checklist_ids or line.ask_ids or line.kind in ("operator", "unverified"))


def _count(line: MemoLine) -> str:
    if line.kind == "gap":
        return "what to ask" if (line.checklist_ids or line.ask_ids) else "why"
    if line.kind == "operator":
        n = len(line.claim_ids)
        return f"{n} claim{'s' if n != 1 else ''}" if n else "who wrote it"
    if line.kind == "coverage":
        n = len(line.checklist_ids)
        return f"{n} item{'s' if n != 1 else ''}"
    if line.kind == "unverified":
        return "why"
    if line.kind == "ask" and not line.claim_ids:
        n = len(line.ask_ids)
        return f"{n} request{'s' if n != 1 else ''}" if n > 1 else "checklist item"
    n = len(line.claim_ids)
    return f"{n} claim{'s' if n != 1 else ''}"


# Rows ------------------------------------------------------------------------------------------


def _text(line: MemoLine, text: str | None = None, lead: bool = False) -> str:
    """The line's sentence, in the span an operator's rewrite replaces. The kind tag shows in the operator view."""
    badge = KIND_WORDS.get(line.kind, "")
    tag = f'<span class="kind kind-{line.kind}">{_e(badge)}</span>' if badge else ""
    head = f"<strong>{_e(line.label)}.</strong> " if lead and line.label else ""
    extra = ""
    if line.kind == "operator":
        extra = f' <span class="who">{_e(line.author)}, version {line.version}</span>'
        if line.unsourced_numbers:
            extra += f' <span class="unsourced">operator\'s figure, no source: {_e(", ".join(line.unsourced_numbers))}</span>'
    return f'{tag}<span class="text">{head}{_e(text if text is not None else line.text)}</span>{extra}'


def _row(line: MemoLine, section: int, cells: list[str], cls: str = "") -> str:
    """One line as a row. A drillable row is one button over the whole row, with its drill under it."""
    sev = f" sev-{line.severity}" if line.severity else ""
    li_cls = f"line row kind-{line.kind}{sev} aud-{line.audience}{' ' + cls if cls else ''}"
    attrs = f'data-line-id="{_e(line.id)}" data-kind="{line.kind}" data-section="{section}"'
    body = "".join(cells)
    if _drillable(line):
        return (f'<li class="{li_cls}" {attrs}>'
                f'<button type="button" class="line-open" aria-expanded="false" aria-controls="drill-{_e(line.id)}">'
                f'{body}<span class="chip">{_e(_count(line))}</span></button>'
                f'<div class="drill" id="drill-{_e(line.id)}" role="region" aria-label="Behind this line" hidden></div></li>')
    return f'<li class="{li_cls}" {attrs}><div class="line-static">{body}<span class="chip-gap"></span></div></li>'


def _cell(cls: str, inner: str) -> str:
    return f'<span class="c {cls}">{inner}</span>'


def _where(memo: Memo, line: MemoLine) -> str:
    """The file and place behind a line's first claim, as a partner reads a source."""
    for cid in line.claim_ids:
        c = memo.claims.get(cid)
        if c and c.sources:
            s = c.sources[0]
            more = len({(x.uri, x.locator) for x in c.sources}) - 1
            return f"{Path(s.uri).name}, {s.locator}" + (f" +{more}" if more > 0 else "")
    return ""


def _group(title: str, cls: str, rows: list[tuple[MemoLine, str]], head: list[str] | None = None) -> str:
    """A titled group of rows, one surface. A group whose rows are all operator-only is operator-only."""
    if not rows:
        return ""
    op = all(ln.audience == "operator" for ln, _ in rows)
    head_html = ""
    if head:
        head_html = '<li class="row-head" aria-hidden="true">' + "".join(f"<span>{_e(h)}</span>" for h in head) + "</li>"
    return (f'<div class="group {cls}{" aud-operator" if op else ""}" data-group="{cls[2:]}">'
            f'<h3 class="group-h">{_e(title)}</h3>'
            f'<ul class="lines rows">{head_html}{"".join(r for _, r in rows)}</ul></div>')


def _plain_row(line: MemoLine, n: int) -> str:
    lead = _cell("c-lead", _e(line.label)) if line.label else _cell("c-lead empty", "")
    return _row(line, n, [lead, _cell("c-text", _text(line))])


# A red flag's figures --------------------------------------------------------------------------


def _fig_cell(figs: list[Figure], role: str) -> str:
    mine = sorted([f for f in figs if f.role == role], key=lambda f: (f.spoken, -f.number))
    if not mine:
        return _cell(f"c-fig {role}", "")
    word = {"stated": "The pitch states", "found": "The room shows", "amount": "Amount"}[role]
    first = mine[0]
    wheres = sorted(first.where, key=lambda w: not w.startswith("pitch_"))
    where = wheres[0] if wheres else ""
    more = len(wheres) - 1
    also = [f"{fmt(f.number, f.unit)}{', spoken' if f.spoken else ''} ({'; '.join(f.where)})" for f in mine[1:]]
    title = "; ".join(wheres) + (". Also " + "; ".join(also) if also else "")
    return _cell(f"c-fig {role}",
                 f'<span class="k">{word}</span><b class="fig" data-figure="{role}" title="{_e(title)}">{_e(fmt(first.number, first.unit))}</b>'
                 f'<span class="w" title="{_e(title)}">{_e(where)}{f" +{more}" if more > 0 else ""}</span>')


def strip(figs: list[Figure]) -> str:
    """The range strip: one tick per figure on a rounded range, the pitch's figure in red under a marker.

    A band shows only when the room holds one figure; when the room's files disagree, no band picks a winner.
    """
    stated = [f for f in figs if f.role == "stated"]
    found = [f for f in figs if f.role == "found"]
    if not stated or not found:
        return ""
    lo, hi = scale(figs)
    unit = figs[0].unit
    parts = []
    if len({round(f.number, 1) for f in found}) == 1:
        p = position(found[0].number, lo, hi)
        parts.append(f'<span class="band" style="left:{max(0.0, p - 2):.2f}%;width:4%"></span>')
    for f in found:
        parts.append(f'<span class="tk" style="left:{position(f.number, lo, hi):.2f}%"></span>')
    for f in stated:
        parts.append(f'<span class="tk w{" fz" if f.spoken else ""}" style="left:{position(f.number, lo, hi):.2f}%"></span>')
    lead = sorted(stated, key=lambda f: (f.spoken, -f.number))[0]
    parts.append(f'<span class="oor" style="left:{position(lead.number, lo, hi):.2f}%"></span>')
    label = (f"Range from {short(lo, unit)} to {short(hi, unit)}. The pitch states "
             + ", ".join(fmt(f.number, f.unit) for f in stated) + ". The room shows "
             + ", ".join(fmt(f.number, f.unit) for f in found) + ".")
    return (f'<span class="strip" role="img" aria-label="{_e(label)}" data-strip>'
            f'<span class="rail">{"".join(parts)}</span>'
            f'<span class="axis"><span>{_e(short(lo, unit))}</span><span>{_e(short(hi, unit))}</span></span></span>')


_FLAG = re.compile(r"^(Red|Green) flag(?: (\d+))?(?::\s*(.*))?$")


def _flag_title(line: MemoLine) -> tuple[str, str]:
    """A flag's number and its short title, from its label; else the first sentence of its text."""
    m = _FLAG.match(line.label or "")
    if m and m.group(3):
        return m.group(2) or "", m.group(3)
    first = re.split(r"(?<=[.:])\s", re.sub(r"^(red|green) flag:\s*", "", line.text, flags=re.I), maxsplit=1)[0]
    return ((m.group(2) or "") if m else ""), first.rstrip(".:")


def _flag_row(memo: Memo, line: MemoLine) -> str:
    n, title = _flag_title(line)
    figs = flag_figures(memo, line)
    if figs and figs[0].role == "amount":
        figs_html = _fig_cell(figs, "amount") + _cell("c-fig found", "") + _cell("c-strip", "")
    else:
        figs_html = _fig_cell(figs, "stated") + _fig_cell(figs, "found") + _cell("c-strip", strip(figs))
    cells = [_cell("c-n", _e(n)),
             _cell("c-title", f'<strong class="flag-title">{_e(title)}</strong>'
                               f'<span class="flag-text">{_text(line)}</span>'),
             figs_html]
    return _row(line, 2, cells, "flag-row")


# The head and the summary ---------------------------------------------------------------------------


def _head(memo: Memo, green_line: MemoLine | None) -> str:
    """Section 1 as the top of the page: the company, the round, the memo's facts."""
    s = memo.section(1)
    facts = [ln for ln in s.lines if ln.kind == "fact" and ln.label in HEAD_LABELS]
    dl = "".join(f'<div class="fact" data-line-id="{_e(ln.id)}"><dt>{_e(ln.label)}</dt><dd>{_e(ln.text)}</dd></div>'
                 for ln in facts)
    round_line = next((ln for ln in s.lines if ln.id == "s01-round"), None)
    lead = f'<p class="lead" data-round>{_e(round_line.text)}</p>' if round_line else ""
    skip = {ln.id for ln in facts} | {"s01-synthetic"} | ({green_line.id} if green_line else set())
    rows = [(ln, _plain_row(ln, 1)) for ln in s.lines if ln.id not in skip]
    return (f'<section class="memo-section memo-head" id="s01" data-section="1">'
            f'<h2 class="sr-only">1. Header</h2>'
            f'<div class="g10 hero"><div class="hero-main">'
            f'<p class="eyebrow">{_e(STAGE_WORDS.get(memo.stage or "", "Memo"))}, first pass</p>'
            f'<h1 class="t-1">{_e(memo.company)}</h1>{lead}</div>'
            f'<dl class="facts">{dl}</dl></div>'
            f'{_group("The header in full", "g-plain", rows)}'
            f'<ul class="lines lines-added"></ul>'
            f'<div class="op-add" data-section="1"></div></section>')


def _green_panel(memo: Memo, line: MemoLine | None, no_green: MemoLine | None, section: int) -> str:
    """The best green flag. Until the top-flags step runs, the round, which the room's files support."""
    if not line:
        text = no_green.text if no_green else "No green flag in the checks run so far."
        return (f'<article class="panel green" data-panel="green"><div class="panel-head">'
                f'<span class="mark m-strong"><i aria-hidden="true"></i>Green flag</span></div>'
                f'<p class="panel-body muted">{_e(text)}</p></article>')
    is_flag = line.severity == "green"
    claims = [memo.claims[c] for c in line.claim_ids if c in memo.claims]
    values: dict[str, tuple[str, str]] = {}
    for c in claims:
        if c.value and c.value.label not in values:
            values[c.value.label] = (LABEL_WORDS.get(c.value.label, c.value.label.replace("_", " ").capitalize()),
                                     fmt(c.value.number, c.value.unit))
    by_file: dict[str, list[str]] = {}
    for c in claims:
        for src in c.sources:
            places = by_file.setdefault(Path(src.uri).name, [])
            if src.locator not in places:
                places.append(src.locator)
    sources = [f"{name}, {', '.join(places)}" for name, places in by_file.items()]
    figs = "".join(f'<span class="gfig"><span class="k">{_e(k)}</span><b class="fig">{_e(v)}</b></span>'
                   for k, v in list(values.values())[:2])
    title = (_flag_title(line)[1] if is_flag else line.label) or "Green flag"
    cells = [f'<span class="c c-gtitle"><span class="mark m-strong"><i aria-hidden="true"></i>'
             f'{"Green flag" if is_flag else "Best supported"}</span><strong class="t-3">{_e(title)}</strong></span>',
             f'<span class="c c-gfigs">{figs}</span>' if figs else "",
             f'<span class="c c-text{" sr-only" if figs else ""}">{_text(line)}</span>',
             f'<span class="c c-src"><span class="k">Where the room states it</span><span class="srcs">'
             + "".join(f'<span class="src">{_e(w)}</span>' for w in sources) + "</span></span>"]
    return (f'<article class="panel green" data-panel="green"><ul class="lines">'
            f'{_row(line, section, cells, "green-row")}</ul></article>')


def top_asks(memo: Memo) -> list[tuple[str, str]]:
    """What to ask the founder first: gap asks before checklist asks, none 'if you have it', one per checklist item."""
    from memo.build import partner_text

    seen: set[str] = set()
    picked: list[tuple[str, str]] = []
    for aid, a in sorted(memo.asks.items(), key=lambda kv: (kv[1].from_kind != "gap", kv[0])):
        key = a.checklist_id or aid
        if a.if_you_have_it or key in seen:
            continue
        seen.add(key)
        what = partner_text(a.what)
        picked.append((aid, what[:1].upper() + what[1:]))
        if len(picked) == FIRST_ASKS:
            break
    return picked


def _ask_panel(memo: Memo) -> str:
    if not memo.asks:
        return ""
    items = "".join(f'<li data-ask-id="{_e(aid)}"><span class="ask-n">{i}</span><span>{_e(what)}</span></li>'
                    for i, (aid, what) in enumerate(top_asks(memo), 1))
    n = len(memo.asks)
    return (f'<article class="panel ask" data-panel="ask"><div class="panel-head">'
            f'<span class="mark m-ask"><i aria-hidden="true"></i>Ask the founder</span>'
            f'<span class="count">{n} request{"s" if n != 1 else ""} in all</span></div>'
            f'<ol class="asks">{items}</ol>'
            f'<div class="panel-foot"><a href="#s14">The full ask list, in section 14</a></div></article>')


def _summary(memo: Memo, s: MemoSection, rec: MemoLine | None, green_line: MemoLine | None) -> str:
    lines = list(s.lines)
    reds = [ln for ln in lines if ln.severity == "red" and ln.kind == "claim"]
    greens = [ln for ln in lines if ln.severity == "green" and ln.kind == "claim"]
    no_green = next((ln for ln in lines if ln.id == "s02-no-green"), None)
    used = {ln.id for ln in reds} | {ln.id for ln in greens[:1]} | ({no_green.id} if no_green else set())
    rest = [ln for ln in lines if ln.id not in used]
    pieces = [ln for ln in rest if ln.kind == "pieces"]
    quiet = [ln for ln in rest if ln.kind != "pieces"]
    out = [f'<div class="sec-head summary-head"><h2 class="t-2 sr-only">2. {_e(s.title)}</h2>'
           f'<p class="note aud-operator">Who writes it: {_e(s.who_writes)}</p></div>']
    if rec:
        out.append(f'<div class="rec"><ul class="lines">'
                   f'{_row(rec, 2, [_cell("c-lead", "Recommendation"), _cell("c-text", _text(rec))], "rec-row")}</ul></div>')
    if reds:
        n = len(reds)
        head = ('<li class="row-head" aria-hidden="true"><span></span><span>Red flag</span><span>The pitch states</span>'
                '<span>The room shows</span><span>Range</span><span></span></li>')
        out.append(f'<div class="group flags" data-group="red-flags"><h3 class="group-h">'
                   f'<span class="mark m-weak"><i aria-hidden="true"></i>{n} red flag{"s" if n != 1 else ""}</span></h3>'
                   f'<ul class="lines rows flag-rows">{head}{"".join(_flag_row(memo, ln) for ln in reds)}</ul></div>')
    green = greens[0] if greens else green_line
    out.append(f'<div class="g10 pair">{_green_panel(memo, green, no_green, 2 if greens else 1)}{_ask_panel(memo)}</div>')
    if pieces:
        out.append(_group("The pieces", "g-plain", [(ln, _plain_row(ln, 2)) for ln in pieces]))
    quiet = greens[1:] + quiet
    if quiet:
        out.append(f'<ul class="lines quiet" data-group="status">{"".join(_plain_row(ln, 2) for ln in quiet)}</ul>')
    return "".join(out)


# Sections 3 to 16 -----------------------------------------------------------------------------------


def _is_needs(line: MemoLine) -> bool:
    """A line that says what has not been assessed yet, rather than what is missing from the room."""
    return line.kind == "gap" and (line.gap is None or line.gap.missing_from == "readout"
                                   or line.id.endswith(("-needs", "-empty", "-facts")))


def _gap_cells(line: MemoLine) -> list[str]:
    body = re.sub(r"^Not in the room:\s*", "", line.text)
    doc, _, backs = body.partition(", to back ")
    if not backs:
        doc, sep, backs = body.partition(": ")
        if not sep:
            doc, backs = body, ""
    tag = f'<span class="kind kind-gap">{KIND_WORDS["gap"]}</span>'
    return [_cell("c-doc", f'{tag}<span class="text">{_e(doc[:1].upper() + doc[1:])}</span>'),
            _cell("c-backs", _e(backs[:1].upper() + backs[1:]))]


# "The deck (slide 1) gives year founded as 2024." -> what the pitch states, and the figure it gives.
_GIVES = re.compile(r"\bgives (.+?) as (.+?)(?:[;,.](?:\s|$)|$)")


def _pitch_cells(memo: Memo, line: MemoLine) -> list[str]:
    c = memo.claims.get(line.claim_ids[0]) if line.claim_ids else None
    status = line.text.split(":", 1)[0] if ":" in line.text[:16] else ""
    said = _GIVES.search(line.text)
    label = line.label or (said.group(1)[:1].upper() + said.group(1)[1:] if said else "") \
        or (LABEL_WORDS.get(c.value.label, "") if c and c.value else "")
    fig = fmt(c.value.number, c.value.unit) if c and c.value else (said.group(2) if said else "")
    return [_cell("c-lead", _e(label)),
            _cell("c-fig1", f'<b class="fig">{_e(fig)}</b>'),
            _cell("c-where", _e(_where(memo, line))),
            _cell("c-status", f'<span class="st st-{_e(status.lower())}">{_e(status)}</span>' if status else ""),
            _cell("c-text clip", _text(line))]


def _ref_cells(line: MemoLine) -> list[str]:
    n, title = _flag_title(line)
    lead = f"Red flag {n}" if n else "Red flag"
    named = f"<strong>{_e(title)}.</strong> " if ":" in (line.label or "") and title else ""
    return [_cell("c-lead", f'<span class="mark m-weak"><i aria-hidden="true"></i>{_e(lead)}</span>'),
            _cell("c-text", named + _text(line))]


def _flag_number(line: MemoLine) -> int:
    n = _flag_title(line)[0]
    return int(n) if n.isdigit() else 999


def coverage_counts(memo: Memo) -> Counter:
    return Counter(r.status for r in memo.checklist.values())


def _coverage_bar(memo: Memo) -> str:
    """Section 14's checklist as one bar, counted from the checklist rows' own statuses."""
    counts = coverage_counts(memo)
    if not counts:
        return ""
    total = sum(counts.values())
    order = [("checked", "Checked"), ("found", "Found, not checked yet"), ("missing", "Missing"),
             ("not_checked", "Not checked yet"), ("not_expected", "Not expected")]
    order += [(k, k.replace("_", " ").capitalize()) for k in counts if k not in dict(order)]
    segs, keys = [], []
    for k, word in order:
        n = counts.get(k, 0)
        if n:
            segs.append(f'<span class="seg seg-{_e(k)}" style="flex:{n}" data-status="{_e(k)}" data-count="{n}"></span>')
            keys.append(f'<span class="ck"><i class="sw seg-{_e(k)}" aria-hidden="true"></i>{_e(word)} <b>{n}</b></span>')
    label = ", ".join(f"{w}: {counts[k]}" for k, w in order if counts.get(k)) + f". {total} items."
    return (f'<div class="coverage" data-coverage><div class="cbar" role="img" aria-label="{_e(label)}">{"".join(segs)}</div>'
            f'<div class="ckey">{"".join(keys)}<span class="ck total">All items <b>{total}</b></span></div></div>')


def _body(memo: Memo, s: MemoSection) -> str:
    n = s.number
    needs = [ln for ln in s.lines if _is_needs(ln)]
    refs = [ln for ln in s.lines if ln.kind == "ref"]
    pitch = [ln for ln in s.lines if ln.id.endswith("-pitch")]
    pitch_claims = [ln for ln in s.lines if ln.kind == "claim" and ln.audience == "operator"
                    and ln.id.startswith(f"s{n:02d}-claims-")]
    findings = [ln for ln in s.lines if ln.kind in ("claim", "reading") and ln not in pitch and ln not in pitch_claims]
    gaps = [ln for ln in s.lines if ln.kind == "gap" and ln not in needs]
    coverage = [ln for ln in s.lines if ln.kind == "coverage"]
    asks = [ln for ln in s.lines if ln.kind == "ask"]
    sources = [ln for ln in s.lines if ln.kind == "source"]
    grouped = {id(ln) for ln in needs + refs + pitch + pitch_claims + findings + gaps + coverage + asks + sources}
    other = [ln for ln in s.lines if id(ln) not in grouped]

    out = []
    if needs:
        out.append(f'<ul class="lines needs">{"".join(_row(ln, n, [_cell("c-text", _text(ln))]) for ln in needs)}</ul>')
    if refs:
        title = "The red flags, and what settles each" if n == 12 else "Red flags in this section"
        out.append(_group(title, "g-refs", [(ln, _row(ln, n, _ref_cells(ln))) for ln in sorted(refs, key=_flag_number)]))
    if findings:
        rows = [(ln, _row(ln, n, [_cell("c-text", _text(ln, lead=True)), _cell("c-where", _e(_where(memo, ln)))]))
                for ln in findings]
        out.append(_group("What the checks found", "g-findings", rows, head=["Finding", "Where", ""]))
    if pitch or pitch_claims:
        rows = [(ln, _row(ln, n, [_cell("c-text", _text(ln))], "pitch-sum")) for ln in pitch]
        rows += [(ln, _row(ln, n, _pitch_cells(memo, ln), "pitch-claim")) for ln in pitch_claims]
        out.append(_group("The pitch's figures", "g-pitch", rows))
    if gaps:
        out.append(_group("Not in the room", "g-gaps", [(ln, _row(ln, n, _gap_cells(ln))) for ln in gaps],
                          head=["Document", "What it would back", ""]))
    if n == 14 and coverage:
        out.append(_coverage_bar(memo))
        out.append(_group("Checklist", "g-coverage", [(ln, _plain_row(ln, n)) for ln in coverage]))
        coverage = []
    if asks:
        rows = [(ln, _row(ln, n, [_cell("c-lead", _e(ln.label or "")), _cell("c-text", _text(ln))])) for ln in asks]
        out.append(_group("To ask the founder", "g-asks", rows))
    if sources:
        out.append(_group("Sources", "g-sources", [(ln, _row(ln, n, [_cell("c-text mono", _text(ln))])) for ln in sources]))
    if other:
        out.append(f'<ul class="lines plain">{"".join(_plain_row(ln, n) for ln in other)}</ul>')
    if coverage:
        out.append(f'<ul class="lines foot">{"".join(_plain_row(ln, n) for ln in coverage)}</ul>')
    return "".join(out)


def _collapsed(s: MemoSection) -> str:
    """A section with nothing assessed: its heading and one muted line, on one row."""
    rows = []
    for ln in s.lines:
        text = re.sub(rf"^{re.escape(s.title)}:\s*", "", ln.text)
        rows.append(_row(ln, s.number, [_cell("c-text", _text(ln, text[:1].upper() + text[1:]))]))
    return (f'<div class="collapsed-row"><h2 class="t-4">{s.number}. {_e(s.title)}</h2>'
            f'<ul class="lines needs">{"".join(rows)}</ul></div>')


def render_html(memo: Memo) -> str:
    rec = recommendation(memo)
    s2 = memo.section(2)
    has_green = any(ln.severity == "green" and ln.kind == "claim" for ln in s2.lines)
    round_line = next((ln for ln in memo.section(1).lines if ln.id == "s01-round" and ln.claim_ids), None)
    green_line = None if has_green else round_line
    secs = [_head(memo, green_line)]
    toc = []
    for s in memo.sections[1:]:
        lines = list(s.lines)
        if s.number == 2 and rec:
            lines.insert(0, rec)
        partner_empty = not visible(s.model_copy(update={"lines": lines}), "partner")
        cls = "memo-section" + (" collapsed" if s.collapsed else "") + (" aud-operator" if partner_empty else "")
        toc_cls = " ".join(c for c in ("aud-operator" if partner_empty else "", "muted" if s.collapsed else "") if c)
        toc.append(f'<li class="{toc_cls}"><a href="#s{s.number:02d}" data-toc="{s.number}">'
                   f'<span class="n">{s.number}.</span><span>{_e(s.title)}</span></a></li>')
        if s.number == 2:
            inner = _summary(memo, s, rec, green_line)
        elif s.collapsed:
            inner = _collapsed(s)
        else:
            inner = (f'<div class="sec-head"><h2 class="t-2">{s.number}. {_e(s.title)}</h2>'
                     f'<p class="note aud-operator">Who writes it: {_e(s.who_writes)}</p></div>{_body(memo, s)}')
        secs.append(f'<section class="{cls}" id="s{s.number:02d}" data-section="{s.number}">{inner}'
                    f'<ul class="lines lines-added"></ul><div class="op-add" data-section="{s.number}"></div></section>')
    data = json.dumps(memo.model_dump(mode="json"), ensure_ascii=False).replace("</", "<\\/")
    return (PAGE.replace("{{STYLE}}", (PAGE_DIR / "memo.css").read_text(encoding="utf-8"))
            .replace("{{TITLE}}", _e(f"{memo.company} memo"))
            .replace("{{COMPANY}}", _e(memo.company))
            .replace("{{VERSION}}", str(memo.version))
            .replace("{{BUILT}}", _e(memo.built_at[:16].replace("T", " ")))
            .replace("{{FOOT}}", _e(memo.synthetic_notice))
            .replace("{{TOC}}", "".join(toc))
            .replace("{{SECTIONS}}", "".join(secs))
            .replace("{{DATA}}", data)
            .replace("{{SCRIPT}}", (PAGE_DIR / "memo.js").read_text(encoding="utf-8")))


BRAND_MARK = ('<svg width="24" height="24" viewBox="0 0 26 26" aria-hidden="true"><rect x="0.75" y="0.75" width="24.5" '
              'height="24.5" rx="6" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="5" y1="15" x2="21" y2="15" '
              'stroke="currentColor" stroke-opacity="0.45"/><rect x="6" y="12" width="7" height="6" rx="1.5" fill="var(--band)" '
              'stroke="var(--band-edge)"/><rect x="8.75" y="9.5" width="1.5" height="11" rx="0.75" fill="currentColor"/>'
              '<path d="M15.5 6.5 L20.5 6.5 L18 10.5 Z" fill="var(--weak)"/><rect x="17.25" y="11" width="1.5" height="9.5" '
              'rx="0.75" fill="var(--weak)"/></svg>')

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
{{STYLE}}
</style>
</head>
<body>
<header class="top">
<div class="wrap bar">
<span class="brand">""" + BRAND_MARK + """Tricorder</span>
<span class="bar-title">{{COMPANY}}</span>
<span class="bar-meta">Version {{VERSION}}, {{BUILT}} UTC</span>
<span class="bar-tools">
<button type="button" class="tbtn" id="view-toggle" aria-pressed="false">Operator view</button>
<button type="button" class="tbtn" id="theme-toggle" aria-label="Switch light or dark">Theme</button>
</span>
</div>
</header>
<div class="wrap layout">
<nav class="toc-col" aria-label="Contents">
<details class="toc"><summary>Contents</summary><ol>{{TOC}}</ol></details>
</nav>
<main class="content">
{{SECTIONS}}
<footer class="page-foot">
<p>Click any line for the claims behind it, then a claim for its sources and the sources that agree or disagree.</p>
<p class="synthetic">{{FOOT}}</p>
</footer>
</main>
</div>
<div class="edit-bar" role="region" aria-label="Your changes">
<label>Your name <input id="edit-author" autocomplete="name"></label>
<button type="button" id="edit-save" disabled>Save changes</button>
<button type="button" id="edit-discard" disabled>Discard</button>
<span class="status" id="edit-status" role="status"></span>
</div>
<script type="application/json" id="memo-data">{{DATA}}</script>
<script>{{SCRIPT}}</script>
</body>
</html>
"""
