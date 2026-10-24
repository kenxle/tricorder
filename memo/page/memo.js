(function () {
  var M = JSON.parse(document.getElementById('memo-data').textContent);
  var lineById = {};
  M.sections.forEach(function (s) { s.lines.forEach(function (l) { lineById[l.id] = l; }); });
  // The expert-read sections' sentences open their claims like any claim line.
  var R = document.getElementById('report-data'); R = R ? JSON.parse(R.textContent) : [];
  R.forEach(function (r) { r.parts.forEach(function (p) { p.sentences.forEach(function (x) {
    lineById[x.id] = {id: x.id, kind: 'claim', text: x.text, claim_ids: x.claim_ids, checklist_ids: [], ask_ids: [], replaces: []}; }); }); });
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
      if (!open && !drill.childNodes.length) {
        // A flag row shows only its title and figures; its full sentence opens the drill.
        if (li.classList.contains('flag-row')) drill.appendChild(el('p', 'drill-lead partner-only', l.text));
        fill(drill, l);
      }
      btn.setAttribute('aria-expanded', open ? 'false' : 'true'); drill.hidden = open;
    });
  }
  document.querySelectorAll('.line-open').forEach(wire);

  // Contents: open as a side rail on a wide screen.
  var toc = document.querySelector('details.toc');
  var wide = window.matchMedia('(min-width: 1200px)');
  if (wide.matches) toc.open = true;
  // The contents mark the section being read.
  if ('IntersectionObserver' in window) {
    var links = {};
    document.querySelectorAll('a[data-toc]').forEach(function (a) { links[a.getAttribute('data-toc')] = a; });
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var n = en.target.getAttribute('data-section');
        Object.keys(links).forEach(function (k) { links[k].classList.toggle('here', k === n); });
      });
    }, {rootMargin: '-15% 0px -75% 0px'});
    document.querySelectorAll('.memo-section[data-section]').forEach(function (s) { seen.observe(s); });
  }

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
      var ul = document.querySelector('#s' + String(e.section).padStart(2, '0') + ' .lines-added');
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
    if (!l || ['fact', 'source', 'change'].indexOf(l.kind) >= 0 || id === 's02-recommendation' || li.closest('.xr')) return;
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
