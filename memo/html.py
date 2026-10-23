"""The interactive memo: one self-contained HTML page, no CDN, works offline.

Two views of one memo. The partner view is the default: it opens with the
answer (the recommendation when the operator has written one, the red and
green flags, one line per piece) and shows no plumbing: no check names, claim
ids, checklist numbers, blanks or commands. The operator view (the toggle in
the masthead) shows all of it, and, when the server serves the page, lets the
operator edit in place and save many changes as one new version.

The lines are written into the page as HTML, so it reads top to bottom with
no script. The drill-downs are built by the inline script from the memo's
JSON, embedded in the page:

    one click on a line   -> the claims behind it (or, for a gap, its checklist item and ask line)
    one more on a claim   -> its sources, read as a partner reads them and in place with the quote
                             marked, and the claims that agree or disagree, with theirs
"""

from __future__ import annotations

import html
import json

from memo.model import Memo, MemoLine, MemoSection

KIND_WORDS = {
    "claim": "Claim", "reading": "Reading", "gap": "Gap", "operator": "Operator", "slot": "Operator writes",
    "pieces": "Piece", "coverage": "Checklist", "ask": "Ask", "unverified": "Could not verify",
    "fact": "", "source": "Source", "change": "Change", "scenario": "Scenario", "ref": "",
}


HEAD_LABELS = ("To", "Date", "Re", "Room data", "Version")


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


def _line(line: MemoLine, section: int) -> str:
    sev = f" sev-{line.severity}" if line.severity else ""
    lead = f"<strong>{_e(line.label)}.</strong> " if line.label else ""
    badge = KIND_WORDS.get(line.kind, "")
    badge_html = f'<span class="kind kind-{line.kind}">{_e(badge)}</span>' if badge else ""
    extra = ""
    if line.kind == "operator":
        extra = f' <span class="who">{_e(line.author)}, version {line.version}</span>'
        if line.unsourced_numbers:
            extra += f' <span class="unsourced">operator\'s figure, no source: {_e(", ".join(line.unsourced_numbers))}</span>'
    body = f"{badge_html}<span class=\"text\">{lead}{_e(line.text)}</span>{extra}"
    cls = f"line kind-{line.kind}{sev} aud-{line.audience}"
    attrs = f'data-line-id="{_e(line.id)}" data-kind="{line.kind}" data-section="{section}"'
    if _drillable(line):
        return (f'<li class="{cls}" {attrs}>'
                f'<button type="button" class="line-open" aria-expanded="false" aria-controls="drill-{_e(line.id)}">'
                f'{body}<span class="chip">{_e(_count(line))}</span></button>'
                f'<div class="drill" id="drill-{_e(line.id)}" role="region" aria-label="Behind this line" hidden></div></li>')
    return f'<li class="{cls}" {attrs}><div class="line-static">{body}</div></li>'


def _header(memo: Memo) -> str:
    """Section 1 as a compact memo head, so the first screen is the answer."""
    s = memo.section(1)
    parts = []
    for ln in s.lines:
        if ln.kind == "fact" and ln.label in HEAD_LABELS:
            parts.append(f'<span><strong>{_e(ln.label)}</strong> {_e(ln.text)}</span>')
    others = [ln for ln in s.lines if not (ln.kind == "fact" and (ln.label in HEAD_LABELS or ln.label == "Synthetic"))]
    return (f'<section class="memo-section memo-head" id="s01" data-section="1"><h2 class="sr-only">1. Header</h2>'
            f'<p class="head-line">{" ".join(parts)}</p>'
            f'<ul class="lines">{"".join(_line(ln, 1) for ln in others)}</ul>'
            f'<div class="op-add" data-section="1"></div></section>')


def render_html(memo: Memo) -> str:
    rec = recommendation(memo)
    secs = [_header(memo)]
    toc = []
    for s in memo.sections[1:]:
        lines = list(s.lines)
        if s.number == 2 and rec:
            lines.insert(0, rec)
        partner_empty = not visible(s.model_copy(update={"lines": lines}), "partner")
        cls = "memo-section" + (" collapsed" if s.collapsed else "") + (" aud-operator" if partner_empty else "")
        toc.append(f'<li class="{"aud-operator" if partner_empty else ""}"><a href="#s{s.number:02d}">{_e(s.title)}</a></li>')
        secs.append(
            f'<section class="{cls}" id="s{s.number:02d}" data-section="{s.number}">'
            f'<h2>{s.number}. {_e(s.title)}</h2><p class="note aud-operator">Who writes it: {_e(s.who_writes)}</p>'
            f'<ul class="lines">{"".join(_line(ln, s.number) for ln in lines)}</ul>'
            f'<div class="op-add" data-section="{s.number}"></div></section>')
    data = json.dumps(memo.model_dump(mode="json"), ensure_ascii=False).replace("</", "<\\/")
    banner = f'<p class="banner" role="note">{_e(memo.synthetic_notice)}</p>' if memo.synthetic_notice else ""
    return (PAGE.replace("{{TITLE}}", _e(f"{memo.company} memo"))
            .replace("{{COMPANY}}", _e(memo.company))
            .replace("{{VERSION}}", str(memo.version))
            .replace("{{BUILT}}", _e(memo.built_at[:16].replace("T", " ")))
            .replace("{{BANNER}}", banner)
            .replace("{{TOC}}", "".join(toc))
            .replace("{{SECTIONS}}", "".join(secs))
            .replace("{{DATA}}", data)
            .replace("{{SCRIPT}}", SCRIPT))


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
:root { --bg:#ffffff; --fg:#16181d; --muted:#5d6470; --line:#e3e5e8; --soft:#f5f6f7; --green:#1f7a4d; --red:#b3261e; --amber:#8a5a00;
  --font: system-ui, -apple-system, "Segoe UI", sans-serif; --mono: ui-monospace, "SF Mono", Menlo, monospace; color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#111317; --fg:#e8eaed; --muted:#9aa1ab; --line:#2a2e35; --soft:#191c21; --green:#5cc48d; --red:#ff8a80; --amber:#f0b44c; color-scheme: dark; } }
:root[data-theme="dark"] { --bg:#111317; --fg:#e8eaed; --muted:#9aa1ab; --line:#2a2e35; --soft:#191c21; --green:#5cc48d; --red:#ff8a80; --amber:#f0b44c; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 var(--font); }
.sr-only { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }
.page { max-width: 860px; margin: 0 auto; padding: 12px 16px 96px; }
.masthead { display:flex; gap:8px 12px; align-items:center; flex-wrap:wrap; border-bottom:1px solid var(--line); padding-bottom:8px; }
.masthead h1 { margin:0 auto 0 0; font-size:21px; line-height:1.25; }
.masthead .note { font-size:13px; margin:0; }
.banner { border:1px solid var(--amber); color:var(--amber); padding:4px 10px; border-radius:6px; margin:8px 0; font-size:14px; }
.note { color:var(--muted); margin:2px 0 6px; font-size:14px; }
button.tool, .op-add button, .op-tools button, .edit-bar button { font:inherit; font-size:14px; background:var(--soft); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:3px 10px; cursor:pointer; }
button.tool[aria-pressed="true"] { border-color:var(--fg); }
details.toc { font-size:14px; margin:8px 0 0; }
details.toc summary { cursor:pointer; color:var(--muted); }
details.toc ol { padding-left:20px; margin:6px 0; columns:2; }
details.toc a { color:inherit; }
@media (min-width: 1240px) {
  details.toc { position:fixed; top:16px; left:max(16px, calc(50% - 430px - 230px)); width:200px; }
  details.toc ol { columns:1; }
}
.memo-head .head-line { margin:8px 0 0; display:flex; flex-wrap:wrap; gap:4px 16px; font-size:14px; color:var(--muted); }
.memo-head .head-line strong { color:var(--fg); font-weight:600; }
.memo-section { border-top:1px solid var(--line); padding-top:4px; margin-top:16px; }
.memo-head { border-top:0; margin-top:0; }
.memo-section h2 { font-size:18px; margin:8px 0 2px; }
/* A section with nothing in it yet is one quiet line; its heading stays for screen readers and the contents list. */
.memo-section.collapsed { margin-top:4px; padding-top:0; border-top:0; }
.memo-section.collapsed h2 { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
body.operator .memo-section.collapsed h2 { position:static; width:auto; height:auto; clip:auto; white-space:normal; font-size:16px; }
.memo-section.collapsed .line { border:0; }
.memo-section.collapsed .kind { display:none; }
.memo-section.collapsed .text { color:var(--muted); }
.lines { list-style:none; padding:0; margin:0; }
.line { margin:2px 0; border-left:3px solid transparent; }
.line.sev-green { border-left-color:var(--green); }
.line.sev-red, .line.sev-flag { border-left-color:var(--red); }
.line-open, .line-static { display:block; width:100%; text-align:left; background:none; border:0; color:inherit; font:inherit; padding:5px 8px; border-radius:6px; }
.line-open { cursor:pointer; }
.line-open:hover, .line-open:focus-visible { background:var(--soft); outline:none; }
.line-open:focus-visible { box-shadow: 0 0 0 2px var(--muted); }
.line-open[aria-expanded="true"] { background:var(--soft); }
.kind { display:inline-block; font-size:11px; letter-spacing:.02em; text-transform:uppercase; color:var(--muted); border:1px solid var(--line); border-radius:4px; padding:0 5px; margin-right:6px; vertical-align:1px; }
.kind-gap .kind { color:var(--amber); border-color:var(--amber); }
.kind-operator .kind, .kind-slot .kind { color:var(--fg); border-color:var(--fg); }
.kind-slot .text { color:var(--muted); font-style:italic; }
.kind-unverified .kind { color:var(--red); border-color:var(--red); }
.kind-ref .text { color:var(--muted); }
.sev-red > .line-open strong, .sev-red > .line-static strong { color:var(--red); }
.sev-green > .line-open strong { color:var(--green); }
.chip { display:inline-block; margin-left:8px; font-size:12px; color:var(--muted); border-bottom:1px dotted var(--muted); white-space:nowrap; }
.who { font-size:13px; color:var(--muted); }
.unsourced { font-size:12px; color:var(--amber); border:1px dashed var(--amber); border-radius:4px; padding:0 5px; }
.drill { margin:4px 0 10px 14px; padding:8px 10px; border-left:2px solid var(--line); }
.claim { padding:6px 0; border-bottom:1px solid var(--line); }
.claim:last-child { border-bottom:0; }
.claim .meta, .meta { font-size:13px; color:var(--muted); }
.mark { font-size:12px; font-weight:600; border-radius:10px; padding:0 8px; margin-right:4px; }
.mark.corroborated { color:var(--green); border:1px solid var(--green); }
.mark.contradicted { color:var(--red); border:1px solid var(--red); }
.source-open { font:inherit; font-size:14px; background:none; border:1px solid var(--line); color:inherit; border-radius:6px; padding:2px 10px; margin-top:4px; cursor:pointer; }
.source-open[aria-expanded="true"] { background:var(--soft); }
.sources { margin:6px 0 0; }
.source { margin:8px 0; }
.source .where { font-family:var(--mono); font-size:13px; }
.source .reads { font-size:14px; margin:2px 0; }
.source-text { white-space:pre-wrap; font:13px/1.45 var(--mono); background:var(--soft); border:1px solid var(--line); border-radius:6px; padding:8px; max-height:180px; overflow:auto; margin:4px 0; }
mark { background: color-mix(in srgb, var(--amber) 30%, transparent); color:inherit; }
.agree h4, .disagree h4 { margin:8px 0 2px; font-size:14px; }
.agree h4 { color:var(--green); } .disagree h4 { color:var(--red); }
.op-tools { margin:2px 0 6px 8px; display:flex; gap:6px; flex-wrap:wrap; }
.op-add { margin:4px 0; }
textarea.op-text { width:100%; font:inherit; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:6px; }
.pending { outline:2px dashed var(--amber); outline-offset:2px; border-radius:6px; }
.pending-remove .text { text-decoration:line-through; }
.edit-bar { position:fixed; left:0; right:0; bottom:0; background:var(--bg); border-top:1px solid var(--line); padding:8px 16px; display:none; gap:8px; align-items:center; flex-wrap:wrap; }
body.editing .edit-bar { display:flex; }
.edit-bar input { font:inherit; font-size:14px; padding:3px 6px; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:6px; width:12em; }
.status { font-size:14px; color:var(--muted); }
body:not(.operator) .aud-operator, body:not(.operator) .op-only, body.operator .partner-only { display:none !important; }
/* The kind badges (Claim, Gap, Checklist) help the operator sort lines; a partner reads the sentence. */
body:not(.operator) .line .kind { display:none; }
.claim.before { opacity:.75; border-left-style:dashed; }
body:not(.editing) .op-tools, body:not(.editing) .op-add { display:none; }
a { color:inherit; }
@media (max-width: 560px) { details.toc ol { columns:1; } .masthead h1 { font-size:19px; } }
@media print { .masthead .tool, .chip, .drill, details.toc, .op-add, .op-tools, .edit-bar { display:none !important; } }
</style>
</head>
<body>
<main class="page">
<header class="masthead">
<h1>{{COMPANY}}: memo for the partners' meeting</h1>
<span class="note">Version {{VERSION}}, {{BUILT}} UTC</span>
<button type="button" class="tool" id="view-toggle" aria-pressed="false">Operator view</button>
<button type="button" class="tool" id="theme-toggle" aria-label="Switch light or dark">Light or dark</button>
</header>
{{BANNER}}
<details class="toc"><summary>Contents</summary><ol>{{TOC}}</ol></details>
{{SECTIONS}}
<p class="note">Click any line for the claims behind it, then a claim for its sources and the sources that agree or disagree.</p>
</main>
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

SCRIPT = r"""
(function () {
  var M = JSON.parse(document.getElementById('memo-data').textContent);
  var lineById = {};
  M.sections.forEach(function (s) { s.lines.forEach(function (l) { lineById[l.id] = l; }); });
  var rec = M.sections[14].lines.filter(function (l) { return l.kind === 'operator'; });
  if (rec.length) lineById['s02-recommendation'] = Object.assign({}, rec[0], {id: 's02-recommendation', text: rec.map(function (l) { return l.text; }).join(' ')});
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function money(v) { if (!v) return ''; var n = v.number; var u = v.unit;
    var s = (u.indexOf('USD') === 0 ? '$' : '') + Math.abs(n).toLocaleString('en-US', {maximumFractionDigits: 2});
    if (n < 0) s = '-' + s;
    return s + (u === 'percent' ? '%' : u === 'USD_per_month' ? ' a month' : u === 'USD_per_year' ? ' a year' : (u.indexOf('USD') === 0 ? '' : ' ' + u)) + (v.period ? ', ' + v.period : ''); }
  var CONF = {computed: 'Computed by a script', quoted: 'Quoted from the source', judged: 'Judged by a model', unverified: 'Could not verify'};

  // A sentence for a partner: drops sentences that name a checklist number, a script or a command.
  // The operator view shows the full text beside it.
  function plain(t) { return (t || '').replace(/\bthe \w+ scan's [a-z0-9_]+ check\b/g, 'a check on the room')
    .replace(/\s*\((?:C\d\d(?:,\s*|\s+and\s+)?)+\)/g, '')
    .replace(/(?:[^.]|\.(?!\s|$))*(?:\bC\d\d\b|scans\/|\.py\b|python -m|Mislabel kind|\b[a-z]+(?:_[a-z0-9]+){2,}\b)(?:[^.]|\.(?!\s|$))*(?:\.(?=\s|$))?\s*/g, ' ')
    .replace(/\s{2,}/g, ' ').trim(); }
  function both(cls, full) {
    var d = el('div', cls); var p = plain(full);
    if (p) d.appendChild(el('span', p === full ? null : 'partner-only', p));
    if (p !== full) d.appendChild(el('span', 'op-only', full));
    return d;
  }
  // The quote as the quote checker finds it: any run of spaces or line breaks matches any other,
  // and a number matches a cell holding the same number (186739.0 and 186739).
  function find(text, quote) {
    if (!quote || !quote.trim()) return null;
    var words = quote.trim().split(/\s+/).map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); });
    var hit = new RegExp(words.join('\\s+'), 'i').exec(text);
    if (hit) return [hit.index, hit[0].length];
    var q = Number(quote.replace(/,/g, '')), t = Number(text.trim().replace(/,/g, ''));
    if (!isNaN(q) && !isNaN(t) && text.trim() && q === t) return [text.indexOf(text.trim()), text.trim().length];
    return null;
  }
  function highlight(pre, text, quote) {
    var f = find(text, quote);
    if (!f) { pre.textContent = text; return; }
    var i = f[0], n = f[1];
    pre.appendChild(document.createTextNode(text.slice(0, i)));
    pre.appendChild(el('mark', null, text.slice(i, i + n)));
    pre.appendChild(document.createTextNode(text.slice(i + n)));
    setTimeout(function () { var m = pre.querySelector('mark'); if (m) pre.scrollTop = Math.max(0, m.offsetTop - pre.offsetTop - 40); }, 0);
  }
  function sourceBlock(s) {
    var d = el('div', 'source');
    var st = M.sources[s.uri + '|' + s.locator];
    d.appendChild(el('div', 'where', s.uri + ', ' + s.locator + (s.retrieved_at ? ' (read ' + s.retrieved_at + ')' : '')));
    if (st && st.reads_as) d.appendChild(el('div', 'reads', st.reads_as));
    var pre = el('pre', 'source-text'); pre.setAttribute('data-source-key', s.uri + '|' + s.locator);
    highlight(pre, st ? st.text : 'This source was not read at export.', s.quote);
    d.appendChild(pre);
    return d;
  }
  function relatedBlock(cls, title, ids) {
    var box = el('div', cls); box.appendChild(el('h4', null, title + ' (' + ids.length + ')'));
    if (!ids.length) box.appendChild(el('div', 'meta', M.steps_missing.indexOf('link') >= 0 ?
      'Not compared yet across the room.' : 'None in the room.'));
    ids.forEach(function (id) { var c = M.claims[id]; if (!c) return;
      var d = el('div', 'related-claim'); d.setAttribute('data-claim-id', id);
      var t = both(null, c.text); if (c.value) t.appendChild(document.createTextNode(' [' + money(c.value) + ']')); d.appendChild(t);
      c.sources.forEach(function (s) { d.appendChild(sourceBlock(s)); });
      box.appendChild(d); });
    return box;
  }
  function claimCard(id, lineText) {
    var c = M.claims[id]; var d = el('div', 'claim'); d.setAttribute('data-claim-id', id);
    if (!c) { d.textContent = 'This claim is not in this memo.'; return d; }
    if (c.text !== lineText && plain(c.text) !== lineText) d.appendChild(both(null, c.text));
    var meta = el('div', 'meta');
    meta.appendChild(document.createTextNode((c.value ? money(c.value) + '. ' : '') + CONF[c.confidence] + '. '));
    meta.appendChild(el('span', 'op-only', 'Check ' + c.check.name + ', ' + id + '. '));
    if (c.corroborated_by.length) meta.appendChild(el('span', 'mark corroborated', 'corroborated by ' + c.corroborated_by.length));
    if (c.conflicts_with.length) meta.appendChild(el('span', 'mark contradicted', 'contradicted by ' + c.conflicts_with.length));
    d.appendChild(meta);
    var nrel = c.corroborated_by.length + c.conflicts_with.length;
    var b = el('button', 'source-open', 'Open ' + c.sources.length + ' source' + (c.sources.length === 1 ? '' : 's') +
      (nrel ? ' and the ' + nrel + ' that agree or disagree' : ''));
    b.type = 'button'; b.setAttribute('aria-expanded', 'false');
    var panel = el('div', 'sources'); panel.hidden = true; panel.id = 'src-' + id + '-' + Math.random().toString(36).slice(2, 7);
    b.setAttribute('aria-controls', panel.id);
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      if (!open && !panel.childNodes.length) {
        c.sources.forEach(function (s) { panel.appendChild(sourceBlock(s)); });
        panel.appendChild(relatedBlock('agree', 'Sources that agree', c.corroborated_by));
        panel.appendChild(relatedBlock('disagree', 'Sources that disagree', c.conflicts_with));
      }
      b.setAttribute('aria-expanded', open ? 'false' : 'true'); panel.hidden = open;
    });
    d.appendChild(b); d.appendChild(panel);
    return d;
  }
  function checklistCard(id) {
    var r = M.checklist[id]; var d = el('div', 'claim checklist-item'); d.setAttribute('data-checklist-id', id);
    if (!r) { d.textContent = 'Not in the coverage table.'; return d; }
    var head = el('div'); head.appendChild(el('span', 'op-only', id + ': ')); head.appendChild(document.createTextNode(r.item)); d.appendChild(head);
    d.appendChild(el('div', 'meta', 'Status: ' + r.status.replace('_', ' ') + '. Expected at this stage: ' + r.expected + '.'));
    d.appendChild(el('div', 'meta op-only', r.detail));
    if (r.named_by.length) {
      var b = el('button', 'source-open', 'Published checklists that name it (' + r.named_by.length + ')'); b.type = 'button'; b.setAttribute('aria-expanded', 'false');
      var p = el('div', 'sources'); p.hidden = true;
      r.named_by.forEach(function (n, i) { var row = el('div', 'source'); var url = r.named_by_urls[i];
        if (url) { var a = el('a', null, n); a.href = url; a.rel = 'noopener'; row.appendChild(a); } else row.textContent = n; p.appendChild(row); });
      b.addEventListener('click', function () { var o = b.getAttribute('aria-expanded') === 'true'; b.setAttribute('aria-expanded', o ? 'false' : 'true'); p.hidden = o; });
      d.appendChild(b); d.appendChild(p);
    }
    return d;
  }
  function askCard(id) {
    var a = M.asks[id]; var d = el('div', 'claim ask-item'); d.setAttribute('data-ask-id', id);
    if (!a) return d;
    var what = a.what.charAt(0).toUpperCase() + a.what.slice(1) + (a.if_you_have_it ? ' (if you have it)' : '');
    d.appendChild(both(null, what));
    d.appendChild(both('meta', 'Why: ' + a.why));
    return d;
  }
  function fill(drill, l) {
    if (l.kind === 'gap') {
      if (l.gap && l.gap.missing_from === 'room') drill.appendChild(both('meta', 'What would close it: ' + l.gap.would_need));
      if (l.gap && l.gap.missing_from === 'readout') {
        drill.appendChild(el('div', 'meta', 'Tricorder has not assessed this yet; it fills in when the checks that feed it run.'));
        drill.appendChild(el('div', 'meta op-only', 'Why: ' + l.gap.why + '. To fill it: ' + l.gap.would_need + '.'));
      }
      l.checklist_ids.forEach(function (id) { drill.appendChild(checklistCard(id)); });
      l.ask_ids.forEach(function (id) { drill.appendChild(askCard(id)); });
      return;
    }
    if (l.kind === 'operator') {
      drill.appendChild(el('div', 'meta', 'Written by ' + l.author + ' in version ' + l.version + '. ' +
        (l.claim_ids.length ? 'Claims the operator attached:' : 'No claim behind it.') +
        (l.unsourced_numbers.length ? ' Operator\'s figure, no source: ' + l.unsourced_numbers.join(', ') + '.' : '')));
    }
    if (l.kind === 'unverified') { drill.appendChild(el('div', 'meta', 'The quote checker could not find this claim\'s quote at its source, so no line in the memo cites it.')); return; }
    if (l.kind === 'coverage') { l.checklist_ids.forEach(function (id) { drill.appendChild(checklistCard(id)); }); return; }
    if (l.kind === 'ask') { l.ask_ids.forEach(function (id) { drill.appendChild(askCard(id)); }); l.checklist_ids.forEach(function (id) { drill.appendChild(checklistCard(id)); }); }
    if (l.composed) drill.appendChild(el('div', 'meta', 'Tricorder put these figures side by side from the claims below; each figure is in a claim or one of its sources.'));
    l.claim_ids.forEach(function (id) { drill.appendChild(claimCard(id, l.text)); });
    (l.replaces || []).forEach(function (id) {
      drill.appendChild(el('div', 'meta before-head', 'Before the operator steered it, this line read:'));
      var card = claimCard(id, ''); card.classList.add('before'); drill.appendChild(card);
    });
  }
  function wire(btn) {
    btn.addEventListener('click', function () {
      var li = btn.closest('.line'); var l = lineById[li.getAttribute('data-line-id')];
      var drill = document.getElementById(btn.getAttribute('aria-controls'));
      var open = btn.getAttribute('aria-expanded') === 'true';
      if (!open && !drill.childNodes.length) fill(drill, l);
      btn.setAttribute('aria-expanded', open ? 'false' : 'true'); drill.hidden = open;
    });
  }
  document.querySelectorAll('.line-open').forEach(wire);

  // Contents: open as a side rail on a wide screen.
  var toc = document.querySelector('details.toc');
  if (window.matchMedia('(min-width: 1240px)').matches) toc.open = true;

  // Theme: the system's choice unless the reader picks one.
  var root = document.documentElement;
  try { var t = localStorage.getItem('memo-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) {}
  document.getElementById('theme-toggle').addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') ? root.getAttribute('data-theme') === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.setAttribute('data-theme', dark ? 'light' : 'dark');
    try { localStorage.setItem('memo-theme', root.getAttribute('data-theme')); } catch (e) {}
  });

  // Operator view, and editing when the server serves the page.
  var m = location.pathname.match(/\/api\/rooms\/([^\/]+)\/memo\.html$/);
  var viewBtn = document.getElementById('view-toggle');
  viewBtn.addEventListener('click', function () {
    var on = document.body.classList.toggle('operator'); viewBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (m) document.body.classList.toggle('editing', on);
  });
  if (!m) return;
  viewBtn.textContent = 'Operator view and editing';
  var api = '/api/rooms/' + m[1] + '/memo';
  var status = document.getElementById('edit-status');
  var saveBtn = document.getElementById('edit-save'), discardBtn = document.getElementById('edit-discard');
  var authorIn = document.getElementById('edit-author');
  var key = 'memo-pending-' + m[1];
  var pending = [];
  try { authorIn.value = localStorage.getItem('memo-author') || ''; pending = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
  function store() { try { localStorage.setItem(key, JSON.stringify(pending)); localStorage.setItem('memo-author', authorIn.value); } catch (e) {} }
  function refresh() {
    saveBtn.disabled = discardBtn.disabled = !pending.length;
    saveBtn.textContent = pending.length ? 'Save ' + pending.length + ' change' + (pending.length === 1 ? '' : 's') + ' as version ' + (M.version + 1) : 'Save changes';
    store();
  }
  function post(base, after) {
    var a = authorIn.value.trim();
    if (!a) { status.textContent = 'Type your name first: each version records who made it.'; authorIn.focus(); return; }
    status.textContent = 'Saving...';
    fetch(api + '/edits', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({author: a, base_version: base, edits: pending})})
      .then(function (r) { return r.json().then(function (j) { return {code: r.status, j: j}; }); })
      .then(function (res) {
        if (res.code === 409) {
          var told = res.j.detail && res.j.detail.latest_version;
          (told ? Promise.resolve([told]) : fetch(api + '/versions').then(function (r) { return r.json(); })).then(function (vs) {
            var latest = vs[vs.length - 1];
            status.textContent = 'Someone saved version ' + latest + ' first. Your ' + pending.length + ' changes are kept. ';
            var re = el('button', null, 'Reapply them on version ' + latest); re.type = 'button'; re.id = 'edit-reapply';
            re.addEventListener('click', function () { re.remove(); post(latest); });
            status.appendChild(re);
          });
          return;
        }
        if (res.code !== 200) { status.textContent = 'Not saved: ' + (res.j.detail || 'the server refused the change') + '. Your changes are kept.'; return; }
        pending = []; store();
        status.textContent = 'Saved as version ' + res.j.version + '. Reloading.'; location.reload();
      })
      .catch(function () { status.textContent = 'Not saved: the server did not answer. Your changes are kept.'; });
  }
  saveBtn.addEventListener('click', function () { post(M.version); });
  discardBtn.addEventListener('click', function () { pending = []; store(); location.reload(); });
  authorIn.addEventListener('change', store);
  function editor(parent, initial, onKeep) {
    var box = el('div', 'op-tools'); var ta = el('textarea', 'op-text'); ta.rows = 2; ta.value = initial || ''; ta.setAttribute('aria-label', 'Your line');
    var ok = el('button', null, 'Keep'); ok.type = 'button';
    var no = el('button', null, 'Cancel'); no.type = 'button';
    ok.addEventListener('click', function () { if (ta.value.trim()) { onKeep(ta.value.trim()); box.remove(); } });
    no.addEventListener('click', function () { box.remove(); });
    box.appendChild(ta); box.appendChild(ok); box.appendChild(no); parent.appendChild(box); ta.focus();
  }
  function showPending(e) {
    if (e.action === 'add') {
      var ul = document.querySelector('#s' + String(e.section).padStart(2, '0') + ' .lines');
      var li = el('li', 'line kind-operator pending'); li.appendChild(el('div', 'line-static', e.text)); ul.appendChild(li);
    } else {
      var li2 = document.querySelector('.line[data-line-id="' + e.line_id + '"]'); if (!li2) return;
      li2.classList.add('pending', e.action === 'remove' ? 'pending-remove' : 'pending-replace');
      if (e.action === 'replace') li2.querySelector('.text').textContent = e.text;
    }
  }
  pending.forEach(showPending);
  if (pending.length) { document.body.classList.add('operator', 'editing'); viewBtn.setAttribute('aria-pressed', 'true'); status.textContent = pending.length + ' unsaved changes from before.'; }
  function queue(e) { pending.push(e); showPending(e); refresh(); }
  document.querySelectorAll('.memo-section').forEach(function (sec) {
    var n = +sec.getAttribute('data-section'); var add = sec.querySelector('.op-add');
    var b = el('button', null, 'Write a line in section ' + n); b.type = 'button';
    b.addEventListener('click', function () { editor(add, '', function (t) { queue({action: 'add', section: n, text: t}); }); });
    add.appendChild(b);
  });
  document.querySelectorAll('.line[data-line-id]').forEach(function (li) {
    var id = li.getAttribute('data-line-id'); var l = lineById[id];
    if (!l || ['fact', 'source', 'change'].indexOf(l.kind) >= 0 || id === 's02-recommendation') return;
    var tools = el('div', 'op-tools');
    var rw = el('button', null, l.kind === 'slot' ? 'Write this' : 'Rewrite'); rw.type = 'button';
    rw.addEventListener('click', function () { editor(li, l.kind === 'slot' ? '' : l.text, function (t) {
      queue({action: 'replace', line_id: id, text: t, claim_ids: ['claim', 'reading', 'operator', 'ref'].indexOf(l.kind) >= 0 ? l.claim_ids : []}); }); });
    tools.appendChild(rw);
    if (l.kind !== 'slot') { var rm = el('button', null, 'Remove'); rm.type = 'button';
      rm.addEventListener('click', function () { queue({action: 'remove', line_id: id}); }); tools.appendChild(rm); }
    li.appendChild(tools);
  });
  refresh();
})();
"""
