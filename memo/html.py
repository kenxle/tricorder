"""The interactive memo: one self-contained HTML page, no CDN, works offline.

The lines are written into the page as HTML, so it reads top to bottom with
no script. The drill-downs are built by the inline script from the memo's
JSON, embedded in the page:

    one click on a line   -> the claims behind it (or, for a gap, its checklist item and ask line)
    one more on a claim   -> its sources' text in place, and the claims that agree or disagree, with theirs

Served by the server (http), the page also lets the operator write, replace
and remove lines; each save makes a new version. Opened as a file, it is read only.
"""

from __future__ import annotations

import html
import json

from memo.model import Memo, MemoLine
from memo.template import BY_NUMBER

DRILLABLE = {"claim", "reading", "gap", "operator", "pieces", "coverage", "ask", "source", "unverified"}

KIND_WORDS = {
    "claim": "Claim", "reading": "Reading", "gap": "Gap", "operator": "Operator", "slot": "Operator writes",
    "pieces": "Pieces", "coverage": "Checklist", "ask": "Ask", "unverified": "Could not verify",
    "fact": "", "source": "Source", "change": "Change", "scenario": "Scenario",
}


def _e(text: str | None) -> str:
    return html.escape(text or "", quote=True)


def _count(line: MemoLine) -> str:
    if line.kind == "gap":
        n = len(line.checklist_ids) + len(line.ask_ids)
        return "what to ask" if n else "why"
    if line.kind == "operator":
        return f"{len(line.claim_ids)} claim{'s' if len(line.claim_ids) != 1 else ''}" if line.claim_ids else "who wrote it"
    if line.kind == "coverage":
        return f"{len(line.checklist_ids)} item{'s' if len(line.checklist_ids) != 1 else ''}"
    if line.kind == "unverified":
        return "why"
    n = len(line.claim_ids)
    if line.kind == "ask" and not n:
        return "checklist item"
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
    attrs = f'data-line-id="{_e(line.id)}" data-kind="{line.kind}" data-section="{section}"'
    if line.kind in DRILLABLE:
        return (f'<li class="line kind-{line.kind}{sev}" {attrs}>'
                f'<button type="button" class="line-open" aria-expanded="false" aria-controls="drill-{_e(line.id)}">'
                f'{body}<span class="chip">{_e(_count(line))}</span></button>'
                f'<div class="drill" id="drill-{_e(line.id)}" role="region" aria-label="Behind this line" hidden></div></li>')
    return f'<li class="line kind-{line.kind}{sev}" {attrs}><div class="line-static">{body}</div></li>'


def render_html(memo: Memo) -> str:
    toc = "".join(f'<li><a href="#s{s.number:02d}">{_e(s.title)}</a></li>' for s in memo.sections)
    secs = []
    for s in memo.sections:
        empty = ""
        if s.empty_because:
            empty = '<p class="empty-note">Tricorder has nothing sourced for this section yet. The gap lines below say why.</p>'
        operator_note = ' <span class="owner">The operator\'s section</span>' if BY_NUMBER[s.number].operator_owned else ""
        secs.append(
            f'<section class="memo-section" id="s{s.number:02d}" data-section="{s.number}">'
            f'<h2>{s.number}. {_e(s.title)}{operator_note}</h2><p class="note">Who writes it: {_e(s.who_writes)}</p>{empty}'
            f'<ul class="lines">{"".join(_line(ln, s.number) for ln in s.lines)}</ul>'
            f'<div class="op-add" data-section="{s.number}" hidden></div></section>')
    data = json.dumps(memo.model_dump(mode="json"), ensure_ascii=False).replace("</", "<\\/")
    banner = f'<p class="banner" role="note">{_e(memo.synthetic_notice)}</p>' if memo.synthetic_notice else ""
    return (PAGE.replace("{{TITLE}}", _e(f"{memo.company} memo"))
            .replace("{{COMPANY}}", _e(memo.company))
            .replace("{{VERSION}}", str(memo.version))
            .replace("{{BUILT}}", _e(memo.built_at[:16].replace("T", " ")))
            .replace("{{BANNER}}", banner)
            .replace("{{TOC}}", toc)
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
.page { max-width: 880px; margin: 0 auto; padding: 16px 16px 64px; }
.masthead { display:flex; gap:12px; align-items:baseline; flex-wrap:wrap; border-bottom:1px solid var(--line); padding-bottom:10px; }
.masthead h1 { margin:0 auto 0 0; font-size:24px; }
.masthead .note { font-size:14px; }
.banner { border:1px solid var(--amber); color:var(--amber); padding:6px 10px; border-radius:6px; margin:12px 0; }
.note { color:var(--muted); margin:2px 0 8px; font-size:14px; }
.toolbar button, .op-add button, .op-tools button { font:inherit; font-size:14px; background:var(--soft); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:3px 10px; cursor:pointer; }
nav.toc ol { columns: 2; font-size:14px; padding-left:20px; margin:12px 0; }
nav.toc a { color:inherit; }
.memo-section { border-top:1px solid var(--line); padding-top:6px; margin-top:22px; }
.memo-section h2 { font-size:19px; margin:8px 0 0; }
.owner { font-size:12px; font-weight:600; color:var(--amber); border:1px solid var(--amber); border-radius:10px; padding:1px 8px; vertical-align:middle; margin-left:6px; }
.empty-note { color:var(--muted); font-style:italic; margin:4px 0; }
.lines { list-style:none; padding:0; margin:0; }
.line { margin:2px 0; border-left:3px solid transparent; }
.line.sev-green { border-left-color:var(--green); }
.line.sev-red, .line.sev-flag { border-left-color:var(--red); }
.line-open, .line-static { display:block; width:100%; text-align:left; background:none; border:0; color:inherit; font:inherit; padding:6px 8px; border-radius:6px; }
.line-open { cursor:pointer; }
.line-open:hover, .line-open:focus-visible { background:var(--soft); outline:none; }
.line-open:focus-visible { box-shadow: 0 0 0 2px var(--muted); }
.line-open[aria-expanded="true"] { background:var(--soft); }
.kind { display:inline-block; font-size:11px; letter-spacing:.02em; text-transform:uppercase; color:var(--muted); border:1px solid var(--line); border-radius:4px; padding:0 5px; margin-right:6px; vertical-align:1px; }
.kind-gap .kind { color:var(--amber); border-color:var(--amber); }
.kind-operator .kind, .kind-slot .kind { color:var(--fg); border-color:var(--fg); }
.kind-slot .text { color:var(--muted); font-style:italic; }
.kind-fact .text { color:var(--fg); }
.kind-unverified .kind { color:var(--red); border-color:var(--red); }
.chip { display:inline-block; margin-left:8px; font-size:12px; color:var(--muted); border-bottom:1px dotted var(--muted); white-space:nowrap; }
.who { font-size:13px; color:var(--muted); }
.unsourced { font-size:12px; color:var(--amber); border:1px dashed var(--amber); border-radius:4px; padding:0 5px; }
.drill { margin:4px 0 10px 14px; padding:8px 10px; border-left:2px solid var(--line); }
.claim { padding:6px 0; border-bottom:1px solid var(--line); }
.claim:last-child { border-bottom:0; }
.claim .meta { font-size:13px; color:var(--muted); }
.mark { font-size:12px; font-weight:600; border-radius:10px; padding:0 8px; margin-right:4px; }
.mark.corroborated { color:var(--green); border:1px solid var(--green); }
.mark.contradicted { color:var(--red); border:1px solid var(--red); }
.source-open { font:inherit; font-size:14px; background:none; border:1px solid var(--line); color:inherit; border-radius:6px; padding:2px 10px; margin-top:4px; cursor:pointer; }
.source-open[aria-expanded="true"] { background:var(--soft); }
.sources { margin:6px 0 0; }
.source { margin:6px 0; }
.source .where { font-family:var(--mono); font-size:13px; }
.source-text { white-space:pre-wrap; font:13px/1.45 var(--mono); background:var(--soft); border:1px solid var(--line); border-radius:6px; padding:8px; max-height:220px; overflow:auto; margin:4px 0; }
mark { background: color-mix(in srgb, var(--amber) 30%, transparent); color:inherit; }
.agree h4, .disagree h4 { margin:8px 0 2px; font-size:14px; }
.agree h4 { color:var(--green); } .disagree h4 { color:var(--red); }
.op-tools { margin:4px 0; display:flex; gap:6px; flex-wrap:wrap; }
.op-add textarea, .op-tools textarea { width:100%; font:inherit; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:6px; }
.status { font-size:14px; color:var(--muted); }
a { color:inherit; }
@media (max-width: 560px) { nav.toc ol { columns:1; } .page { padding: 12px 16px 48px; } }
@media print { .toolbar, .chip, .drill, nav.toc, .op-add, .op-tools { display:none !important; } }
</style>
</head>
<body>
<main class="page">
<header class="masthead">
<h1>{{COMPANY}}: memo for the partners' meeting</h1>
<span class="note">Shared version {{VERSION}}, drafted {{BUILT}} UTC</span>
<span class="toolbar"><button type="button" id="theme-toggle" aria-label="Switch light or dark">Light or dark</button></span>
</header>
{{BANNER}}
<p class="note">Every line opens what stands behind it: click a line for its claims, then a claim for its sources and the sources that agree or disagree. Lines marked Operator were written by the operator, with no claim behind them unless one is shown.</p>
<p class="status" id="edit-status" role="status"></p>
<nav class="toc" aria-label="Sections"><ol>{{TOC}}</ol></nav>
{{SECTIONS}}
</main>
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
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function money(v) { if (!v) return ''; var n = v.number; var u = v.unit;
    var s = (u.indexOf('USD') === 0 ? '$' : '') + n.toLocaleString('en-US', {maximumFractionDigits: 2});
    return s + (u === 'percent' ? '%' : u === 'USD_per_month' ? ' a month' : u === 'USD_per_year' ? ' a year' : (u.indexOf('USD') === 0 ? '' : ' ' + u)) + (v.period ? ', ' + v.period : ''); }
  var CONF = {computed: 'computed by a script', quoted: 'quoted from the source', judged: 'judged by a model', unverified: 'could not verify'};

  function highlight(pre, text, quote) {
    var i = quote ? text.toLowerCase().indexOf(quote.toLowerCase()) : -1;
    if (i < 0) { pre.textContent = text; return; }
    pre.appendChild(document.createTextNode(text.slice(0, i)));
    pre.appendChild(el('mark', null, text.slice(i, i + quote.length)));
    pre.appendChild(document.createTextNode(text.slice(i + quote.length)));
    setTimeout(function () { var m = pre.querySelector('mark'); if (m) pre.scrollTop = Math.max(0, m.offsetTop - pre.offsetTop - 40); }, 0);
  }
  function sourceBlock(s) {
    var d = el('div', 'source');
    var where = el('div', 'where', s.uri + ', ' + s.locator + (s.retrieved_at ? ' (read ' + s.retrieved_at + ')' : ''));
    d.appendChild(where);
    var st = M.sources[s.uri + '|' + s.locator];
    var pre = el('pre', 'source-text'); pre.setAttribute('data-source-key', s.uri + '|' + s.locator);
    highlight(pre, st ? st.text : 'This source was not read at export.', s.quote);
    d.appendChild(pre);
    d.appendChild(el('div', 'meta', 'Quoted: "' + s.quote + '"'));
    return d;
  }
  function relatedBlock(cls, title, ids) {
    var box = el('div', cls); box.appendChild(el('h4', null, title + ' (' + ids.length + ')'));
    if (!ids.length) box.appendChild(el('div', 'meta', M.steps_missing.indexOf('link') >= 0 ?
      'Not checked yet: the merge step that links agreeing and disagreeing claims is not built.' : 'None in the room.'));
    ids.forEach(function (id) { var c = M.claims[id]; if (!c) return;
      var d = el('div', 'related-claim'); d.setAttribute('data-claim-id', id);
      d.appendChild(el('div', null, c.text + (c.value ? ' [' + money(c.value) + ']' : '')));
      c.sources.forEach(function (s) { d.appendChild(sourceBlock(s)); });
      box.appendChild(d); });
    return box;
  }
  function claimCard(id, lineText) {
    var c = M.claims[id]; var d = el('div', 'claim'); d.setAttribute('data-claim-id', id);
    if (!c) { d.textContent = 'Claim ' + id + ' is not in this memo.'; return d; }
    if (c.text !== lineText) d.appendChild(el('div', null, c.text));
    var meta = el('div', 'meta');
    meta.appendChild(document.createTextNode((c.value ? money(c.value) + '. ' : '') + CONF[c.confidence] + '. Check: ' + c.check.name + '. ' + id + '. '));
    if (c.corroborated_by.length) meta.appendChild(el('span', 'mark corroborated', 'corroborated by ' + c.corroborated_by.length));
    if (c.conflicts_with.length) meta.appendChild(el('span', 'mark contradicted', 'contradicted by ' + c.conflicts_with.length));
    d.appendChild(meta);
    var b = el('button', 'source-open', 'Open ' + c.sources.length + ' source' + (c.sources.length === 1 ? '' : 's') +
      (c.corroborated_by.length + c.conflicts_with.length ? ' and the ' + (c.corroborated_by.length + c.conflicts_with.length) + ' that agree or disagree' : ''));
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
    if (!r) { d.textContent = id + ': not in the coverage table.'; return d; }
    d.appendChild(el('div', null, id + ': ' + r.item));
    d.appendChild(el('div', 'meta', 'Status: ' + r.status.replace('_', ' ') + '. Expected at this stage: ' + r.expected + '. ' + r.detail));
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
    d.appendChild(el('div', null, 'On the ask list: ' + a.what));
    d.appendChild(el('div', 'meta', 'Why: ' + a.why + (a.if_you_have_it ? ' Asked "if you have it".' : '')));
    return d;
  }
  function fill(drill, l) {
    if (l.kind === 'gap') {
      if (l.gap) drill.appendChild(el('div', 'meta', 'Why: ' + l.gap.why + '. What would close it: ' + l.gap.would_need + '.'));
      l.checklist_ids.forEach(function (id) { drill.appendChild(checklistCard(id)); });
      l.ask_ids.forEach(function (id) { drill.appendChild(askCard(id)); });
      if (!l.checklist_ids.length && !l.ask_ids.length) drill.appendChild(el('div', 'meta', 'No checklist item or ask-list line names this gap yet.'));
      return;
    }
    if (l.kind === 'operator') {
      drill.appendChild(el('div', 'meta', 'Written by ' + l.author + ' in version ' + l.version + '. ' +
        (l.claim_ids.length ? 'Claims attached by the operator:' : 'No claim behind it.') +
        (l.unsourced_numbers.length ? ' Operator\'s figure, no source: ' + l.unsourced_numbers.join(', ') + '.' : '')));
    }
    if (l.kind === 'unverified') { drill.appendChild(el('div', 'meta', 'The quote checker could not find this claim\'s quote at its source, so no line in the memo cites it.')); return; }
    if (l.kind === 'coverage') { l.checklist_ids.forEach(function (id) { drill.appendChild(checklistCard(id)); }); return; }
    if (l.kind === 'ask') { l.ask_ids.forEach(function (id) { drill.appendChild(askCard(id)); }); l.checklist_ids.forEach(function (id) { drill.appendChild(checklistCard(id)); }); }
    l.claim_ids.forEach(function (id) { drill.appendChild(claimCard(id, l.text)); });
  }
  document.querySelectorAll('.line-open').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.closest('.line'); var l = lineById[li.getAttribute('data-line-id')];
      var drill = document.getElementById(btn.getAttribute('aria-controls'));
      var open = btn.getAttribute('aria-expanded') === 'true';
      if (!open && !drill.childNodes.length) fill(drill, l);
      btn.setAttribute('aria-expanded', open ? 'false' : 'true'); drill.hidden = open;
    });
  });
  // Section 14: copy the ask list, ready to paste into an email to the founder.
  var s14 = document.querySelector('#s14 .lines');
  if (s14) {
    var copy = el('button', 'source-open', 'Copy the ask list'); copy.type = 'button'; copy.id = 'copy-asks';
    var said = el('span', 'status'); said.setAttribute('role', 'status');
    copy.addEventListener('click', function () {
      var text = Object.keys(M.asks).map(function (k, i) { var a = M.asks[k]; return (i + 1) + '. ' + a.what + (a.if_you_have_it ? ' (if you have it)' : ''); }).join('\n');
      var done = function () { said.textContent = ' Copied ' + Object.keys(M.asks).length + ' requests.'; };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { said.textContent = ' Copy failed: select the lines by hand.'; });
      else said.textContent = ' Copy is not available here: select the lines by hand.';
    });
    s14.parentNode.insertBefore(copy, s14); s14.parentNode.insertBefore(said, s14);
  }
  // Theme: the system's choice unless the reader picks one.
  var root = document.documentElement;
  try { var t = localStorage.getItem('memo-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) {}
  document.getElementById('theme-toggle').addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') ? root.getAttribute('data-theme') === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.setAttribute('data-theme', dark ? 'light' : 'dark');
    try { localStorage.setItem('memo-theme', root.getAttribute('data-theme')); } catch (e) {}
  });

  // Editing: only when the server serves the page.
  var m = location.pathname.match(/\/api\/rooms\/([^\/]+)\/memo\.html$/);
  if (!m) return;
  var api = '/api/rooms/' + m[1] + '/memo';
  var status = document.getElementById('edit-status');
  function author() { var a = ''; try { a = localStorage.getItem('memo-author') || ''; } catch (e) {}
    if (!a) { a = (prompt('Your name, for the change log') || '').trim(); try { localStorage.setItem('memo-author', a); } catch (e) {} } return a; }
  function save(edits) {
    var a = author(); if (!a) { status.textContent = 'Not saved: an edit needs your name.'; return; }
    status.textContent = 'Saving...';
    fetch(api + '/edits', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({author: a, base_version: M.version, edits: edits})})
      .then(function (r) { return r.json().then(function (j) { return {ok: r.ok, j: j}; }); })
      .then(function (res) { if (!res.ok) { status.textContent = 'Not saved: ' + (res.j.detail || 'the server refused the edit'); return; }
        status.textContent = 'Saved as version ' + res.j.version + '. Reloading.'; location.reload(); })
      .catch(function () { status.textContent = 'Not saved: the server did not answer.'; });
  }
  function editor(parent, initial, onSave) {
    var box = el('div', 'op-tools'); var ta = el('textarea'); ta.rows = 2; ta.value = initial || ''; ta.setAttribute('aria-label', 'Your line');
    var ok = el('button', null, 'Save as a new version'); ok.type = 'button';
    var no = el('button', null, 'Cancel'); no.type = 'button';
    ok.addEventListener('click', function () { if (ta.value.trim()) onSave(ta.value.trim()); });
    no.addEventListener('click', function () { box.remove(); });
    box.appendChild(ta); box.appendChild(ok); box.appendChild(no); parent.appendChild(box); ta.focus();
  }
  document.querySelectorAll('.memo-section').forEach(function (sec) {
    var n = +sec.getAttribute('data-section'); var add = sec.querySelector('.op-add'); add.hidden = false;
    var b = el('button', null, 'Write a line in section ' + n); b.type = 'button';
    b.addEventListener('click', function () { editor(add, '', function (t) { save([{action: 'add', section: n, text: t}]); }); });
    add.appendChild(b);
  });
  document.querySelectorAll('.line').forEach(function (li) {
    var id = li.getAttribute('data-line-id'); var l = lineById[id];
    if (['fact', 'source', 'change'].indexOf(l.kind) >= 0) return;
    var tools = el('div', 'op-tools');
    var rw = el('button', null, l.kind === 'slot' ? 'Write this' : 'Rewrite'); rw.type = 'button';
    rw.addEventListener('click', function () { editor(li, l.kind === 'slot' ? '' : l.text, function (t) { save([{action: 'replace', line_id: id, text: t, claim_ids: (l.kind === 'claim' || l.kind === 'reading' || l.kind === 'operator') ? l.claim_ids : []}]); }); });
    tools.appendChild(rw);
    if (l.kind !== 'slot') { var rm = el('button', null, 'Remove'); rm.type = 'button';
      rm.addEventListener('click', function () { save([{action: 'remove', line_id: id}]); }); tools.appendChild(rm); }
    li.appendChild(tools);
  });
})();
"""
