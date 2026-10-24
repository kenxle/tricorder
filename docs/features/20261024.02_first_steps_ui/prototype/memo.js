// Steps 7 and 8: the interactive memo. Step 7 is the associate's draft, step 8 the principal's view.
// Modelled on docs/ongoing/MEMO_TEMPLATE.md and the memo-export slice: sections in the template's order,
// every line one of five kinds, one click opens the claims behind a line and one more opens a claim's
// source. The principal's view opens on the round and the flags, and adds agree, disagree and a what-if.
// A what-if changes no verdict and no flag; it stays in the reader's copy.
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;

  const SECTIONS = [
    ["Traction and customers", ["traction_and_revenue", "retention", "customers"]],
    ["Business model and unit economics", ["unit_economics"]],
    ["Market", ["market", "outside_world"]],
    ["Team", ["team"]],
    ["Financials, burn and runway", ["burn_and_runway"]],
    ["Deal terms", ["the_pitch_itself", "legal_and_cap_table"]],
  ];
  const KIND = { claim: "Claim", reading: "Reading", gap: "Gap", operator: "Yours", steer: "Steer", scenario: "Scenario" };
  const CHECKLIST_PIECE = { "customers and contracts": "customers" };

  function money(n) { return `$${Math.round(n).toLocaleString("en-US")}`; }

  // The what-if: the same rules the scripts use, run in the page. Defaults give Tricorder's rebuilt figures.
  function runway(cash, base, hires, pace, revChange) {
    let left = cash;
    for (let m = 1; m <= 120; m++) {
      const burn = base - revChange + pace * hires.filter((h) => h.start <= m).reduce((a, h) => a + h.monthly_cost, 0);
      if (burn <= 0) return 120;
      if (left < burn) return m - 1 + left / burn;
      left -= burn;
    }
    return 120;
  }
  function scenario(W, w) {
    const base = W.lines.reduce((a, l) => a + l.units * l.price, 0);
    const now = W.lines.reduce((a, l) => a + l.units * (l.tweak ? w.price : l.price), 0);
    const mrr = now + (w.pilot && W.pilot ? W.pilot.mrr : 0);
    const arr = 12 * mrr;
    return { arr, arr12: arr * Math.pow(1 - w.churn, 12), runway: runway(W.cash, W.base_burn, W.extra_hires, w.pace, now - base) };
  }
  X.scenario = scenario;

  function lines(room) {
    const T = window.TC;
    const st = X.st();
    if (!T.S.items) T.buildItems();
    const asked = T.S.items.filter((i) => i.checked);
    const missing = asked.filter((i) => !(i.id && room.holds[i.id]));
    const byPiece = (name) => missing.filter((i) => i.id && (() => {
      const c = T.D.checklist.find((x) => x.id === i.id);
      const p = c ? (CHECKLIST_PIECE[c.piece] || c.piece.replace(/ /g, "_")) : "";
      return p === name;
    })());
    const op = st.op;
    const out = [];

    out.push({ title: "Summary and the ask", n: 2, lines: [
      { kind: "claim", text: room.memo_company, claims: ["pi-1", "lc-1"].filter((id) => room.claims[id]) },
      ...room.top_flags.green.map((f) => ({ kind: "claim", text: `Green flag. ${f.title}`, claims: [f.claim_id] })),
      ...room.top_flags.red.map((f) => ({ kind: "claim", text: `Red flag. ${f.title} Stated ${f.stated.value}, found ${f.found.value}.`, claims: [f.claim_id] })),
      { kind: "operator", field: "rec", text: op.rec ? `Recommendation: ${op.rec}${op.amount ? `, ${op.amount}` : ""}.` : "" },
    ], glance: room.pieces.map((p) => p.name) });

    SECTIONS.forEach(([title, names], i) => {
      const ls = [];
      names.forEach((name) => {
        const p = X.pieceOf(room, name);
        const rw = st.steers.filter((s) => s.piece === name && s.kind === "rewrite").pop();
        if (rw) ls.push({ kind: "steer", text: rw.after, claims: p.claim_ids });
        p.claim_ids.forEach((id) => ls.push({ kind: "claim", text: room.claims[id].text, claims: [id] }));
        st.steers.filter((s) => s.piece === name && s.kind === "figure")
          .forEach((s) => ls.push({ kind: "steer", text: `The associate's figure: ${s.steer_value}, beside the check's ${s.check_value}. "${s.sentence}"` }));
        st.steers.filter((s) => s.piece === name && s.kind === "note")
          .forEach((s) => ls.push({ kind: "steer", text: `The associate's note: "${s.sentence}"`, claims: [s.line] }));
        if (!p.claim_ids.length) ls.push({ kind: "reading", text: p.reason });
        byPiece(name).forEach((it) => ls.push({ kind: "gap", text: `Not in the room: ${it.title.toLowerCase()}.` }));
      });
      out.push({ title, n: i + 3, lines: ls, pieces: names });
    });

    out.push({ title: "Risks and open questions", n: 9, lines: room.top_flags.red.map((f) => ({ kind: "claim",
      text: `${X.pieceOf(room, f.piece).label}: ${f.title} Stated ${f.stated.value}, found ${f.found.value}. To settle it, ask: "${f.ask}"`, claims: [f.claim_id] })) });
    out.push({ title: "Outcomes", n: 10, lines: [
      { kind: "operator", field: "down", text: op.down ? `Downside: ${op.down}` : "" },
      { kind: "operator", field: "base", text: op.base ? `Base: ${op.base}` : "" },
      { kind: "operator", field: "up", text: op.up ? `Upside: ${op.up}` : "" },
    ] });
    const held = asked.length - missing.length;
    out.push({ title: "Diligence: what was checked and what to ask", n: 11, lines: [
      { kind: "claim", text: `The room holds ${held} of the ${asked.length} items asked for.` },
      ...missing.map((it) => ({ kind: "gap", text: `Not in the room: ${it.title.toLowerCase()}. Still on the request.` })),
    ] });
    out.push({ title: "Recommendation", n: 12, lines: [
      { kind: "operator", field: "rec", text: op.rec ? `${op.rec}${op.amount ? `, ${op.amount}` : ""}.` : "" },
      { kind: "operator", field: "reasons", text: op.reasons ? `The two reasons that decide it: ${op.reasons}` : "" },
      { kind: "operator", field: "wrong", text: op.wrong ? `Why it could be wrong: ${op.wrong}` : "" },
    ] });
    out.push({ title: "Sources and change log", n: 13, lines: [
      { kind: "claim", text: `${room.files.length} files from the synthetic room are cited, each with its place.` },
      ...st.steers.map((s, i) => ({ kind: "steer", text: `v${i + 2}: ${X.pieceOf(room, s.piece).label}, "${s.sentence}"` })),
    ] });
    out.forEach((sec) => sec.lines.forEach((l, j) => { l.id = `${sec.n}-${j}`; }));
    return out;
  }

  function lineHtml(room, l, mode) {
    const st = X.st();
    if (l.kind === "operator" && mode === "principal" && !l.text) return "";
    const label = `<span class="tc-label${l.kind === "gap" ? " tc-label--gap" : l.kind === "steer" ? " tc-label--steered" : ""}">${KIND[l.kind]}</span>`;
    if (l.kind === "operator" && mode === "associate") {
      return `<li class="x-mline" data-kind="operator">${label} <span class="x-mline-text">${l.text ? esc(l.text) : '<span class="note">Yours to write, in the fields below.</span>'}</span></li>`;
    }
    const has = l.claims && l.claims.length;
    const text = has
      ? `<button type="button" class="x-mline-text" data-mline="${esc(l.id)}" aria-expanded="false">${esc(l.text)}</button>`
      : `<span class="x-mline-text">${esc(l.text)}</span>`;
    const v = st.views[l.id];
    const view = mode === "principal" ? `<span class="x-view">
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-view="agree" data-id="${esc(l.id)}" aria-pressed="${v === "agree"}">Agree</button>
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-view="disagree" data-id="${esc(l.id)}" aria-pressed="${v === "disagree"}">Disagree</button>
        ${v === "agree" ? '<span class="tc-mark">You agree</span>' : v === "disagree" ? '<span class="tc-mark tc-mark--disagreement">You disagree</span>' : ""}</span>` : "";
    const claims = has ? `<div class="x-mline-claims" id="mc-${esc(l.id)}" hidden><ul class="x-claims">${l.claims.map((id) => `<li class="x-claim">${X.claimBody(room.claims[id])}</li>`).join("")}</ul></div>` : "";
    return `<li class="x-mline" data-kind="${esc(l.kind)}"><div class="x-mline-row">${label}${text}${view}</div>${claims}</li>`;
  }

  function opFields(sec) {
    const op = X.st().op;
    const ta = (k, label) => `<label class="tc-label" for="op-${k}">${label}</label><textarea class="tc-input" id="op-${k}" data-op="${k}">${esc(op[k])}</textarea>`;
    if (sec.title === "Summary and the ask" || sec.title === "Recommendation") {
      if (sec.title === "Summary and the ask") return "";
      return `<div class="x-op"><label class="tc-label" for="op-rec">Invest, pass or wait</label>
        <select class="tc-input" id="op-rec" data-op="rec"><option value="">Choose</option>${["Invest", "Pass", "Wait"].map((o) => `<option${op.rec === o ? " selected" : ""}>${o}</option>`).join("")}</select>
        <label class="tc-label" for="op-amount">Amount and conditions</label><input class="tc-input" type="text" id="op-amount" data-op="amount" value="${esc(op.amount)}" />
        ${ta("reasons", "The two reasons that decide it")}${ta("wrong", "Why it could be wrong")}</div>`;
    }
    if (sec.title === "Outcomes") return `<div class="x-op">${ta("down", "Downside case")}${ta("base", "Base case")}${ta("up", "Upside case")}</div>`;
    return "";
  }

  function whatifHtml(room) {
    const st = X.st();
    const W = room.whatif;
    const tweak = W.lines.find((l) => l.tweak);
    if (!st.whatif) st.whatif = { pilot: false, churn: W.churn, price: tweak.price, pace: 1 };
    const w = st.whatif;
    const s = scenario(W, w);
    const r = scenario(W, { pilot: false, churn: W.churn, price: tweak.price, pace: 1 });
    const mo = (n) => `${n.toFixed(1)} months`;
    const rows = [
      ["ARR", W.company_arr ? money(W.company_arr) : "not stated", money(r.arr), money(s.arr)],
      ["ARR in 12 months, with no new customers", "not stated", money(r.arr12), money(s.arr12)],
      ["Runway with the hiring plan", W.company_runway ? `${W.company_runway} months` : "not stated", mo(r.runway), mo(s.runway)],
    ];
    return `<section class="x-whatif" aria-label="Your what-if">
      <h3>Your what-if</h3>
      <p class="note">Change an assumption and the same rules recompute. A what-if changes no verdict and no flag, and it stays in your copy.</p>
      <div class="x-whatif-controls">
        ${W.pilot ? `<label class="x-checkrow"><input class="tc-check" type="checkbox" id="w-pilot"${w.pilot ? " checked" : ""} /> Count the ${esc(W.pilot.name)} pilot as recurring</label>` : ""}
        <div><label class="tc-label" for="w-churn">Monthly churn, %</label><input class="tc-input" type="number" id="w-churn" step="0.5" min="0" max="20" value="${(w.churn * 100).toFixed(1)}" /></div>
        <div><label class="tc-label" for="w-price">${esc(tweak.name)} price, $ a month</label><input class="tc-input" type="number" id="w-price" step="10" min="0" value="${w.price}" /></div>
        <div><label class="tc-label" for="w-pace">Hiring pace: ${Math.round(w.pace * W.extra_count)} of the ${W.extra_count} hires the model leaves out</label><input type="range" id="w-pace" min="0" max="1" step="0.05" value="${w.pace}" /></div>
      </div>
      <div class="tc-table-wrap"><table class="tc-table tc-table--stack x-wtable"><thead><tr><th>Figure</th><th class="tc-fig">The company's</th><th class="tc-fig">Tricorder's rebuilt</th><th class="tc-fig x-scn">Your scenario (<span id="w-reader">${esc(st.reader)}</span>)</th></tr></thead>
        <tbody>${rows.map((row) => `<tr><td data-label="Figure">${esc(row[0])}</td><td class="tc-fig" data-label="The company's">${esc(row[1])}</td><td class="tc-fig" data-label="Tricorder's rebuilt">${esc(row[2])}</td><td class="tc-fig x-scn" data-label="Your scenario">${esc(row[3])}</td></tr>`).join("")}</tbody></table></div>
    </section>`;
  }

  function render(mode) {
    const T = window.TC;
    const room = X.room();
    const step = mode === "principal" ? "principal" : "memo";
    if (!room) return X.noRoom(step, mode === "principal" ? ["memo", "the memo"] : ["steer", "steering"]);
    const st = X.st();
    const company = X.company();
    const secs = lines(room);
    const version = `v${1 + st.steers.length}`;
    const today = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    const views = Object.values(st.views);
    const head = `<dl class="tc-facts x-head-facts">
        <dt>To</dt><dd>The partners</dd><dt>From</dt><dd>${esc(T.S.sender || "The associate")}</dd><dt>Date</dt><dd>${esc(today)}</dd>
        <dt>Re</dt><dd>${esc(company)}, ${esc(room.round.name)}: ${esc(room.round.raise)} at ${esc(room.round.pre_money)} pre-money</dd>
        <dt>Data as of</dt><dd>${esc(room.as_of)}</dd><dt>Version</dt><dd>${version}</dd></dl>`;
    const round = `<div class="x-round" aria-label="The round">
        ${[["Raise", room.round.raise], ["Pre-money", room.round.pre_money], ["Post-money", room.round.post_money], ["New money owns", room.round.ownership]]
          .map(([k, v]) => `<div><div class="tc-pair-key">${k}</div><div class="tc-pair-value">${esc(v)}</div></div>`).join("")}
      </div><div class="tc-chips">${X.roomChip(room.round.source)}</div>`;
    const sections = secs.map((sec) => `<section class="x-memo-sec" aria-label="${esc(sec.title)}">
        <h3><span class="tc-meta">${sec.n}</span>${esc(sec.title)}</h3>
        ${sec.pieces ? `<p class="x-secpieces">${sec.pieces.map((n) => { const p = X.pieceOf(room, n); return `<span><b>${esc(p.label)}</b> ${X.verdictMark(p.verdict)} <span class="tc-meta">${X.counts(p)}</span></span>`; }).join("")}</p>` : ""}
        <ul class="x-mlines">${sec.lines.filter((l) => !(sec.glance && l.field === "rec")).map((l) => lineHtml(room, l, mode)).join("")}</ul>
        ${sec.glance ? `<h4 class="x-glance">The pieces at a glance</h4><div class="x-verdicts">${sec.glance.map((n) => X.verdictRow(X.pieceOf(room, n))).join("")}</div>
          <ul class="x-mlines">${sec.lines.filter((l) => l.field === "rec").map((l) => lineHtml(room, l, mode)).join("")}</ul>` : ""}
        ${mode === "associate" ? opFields(sec) : ""}</section>`).join("");

    if (mode === "associate") {
      T.app.innerHTML = `${T.header("memo", ["steer", "steering"])}
        <h2 class="co-title">${esc(company)}: the memo, drafted</h2>
        ${X.notice(room)}
        <p class="x-lede">Tricorder drafted every section it can source, in the template's order. The recommendation and the outcomes are yours. Click a line to see the claims behind it, then a claim's chip to see its source.</p>
        <article class="x-memo"><section class="x-memo-sec" aria-label="Header"><h3><span class="tc-meta">1</span>Header</h3>${head}${round}</section>${sections}</article>
        <div class="actions"><button class="tc-btn primary" type="button" id="to-principal">Share with the partners</button></div>`;
      document.getElementById("to-principal").addEventListener("click", () => T.go("principal"));
      T.app.querySelectorAll("[data-op]").forEach((el) => el.addEventListener("change", () => { st.op[el.dataset.op] = el.value; render(mode); }));
    } else {
      T.app.innerHTML = `${T.header("principal", ["memo", "the memo"])}
        <h2 class="co-title">${esc(company)}, ${esc(room.round.name)}</h2>
        ${X.notice(room)}
        <div class="x-reader"><label class="tc-label" for="reader">Reading as</label><input class="tc-input" type="text" id="reader" value="${esc(st.reader)}" style="max-width:320px" /></div>
        <section class="x-section" aria-label="The round"><h2 class="x-h">The round</h2>${round}
          ${st.op.rec ? `<p class="x-lede">The associate's recommendation: <strong>${esc(st.op.rec)}</strong>${st.op.amount ? `, ${esc(st.op.amount)}` : ""}.</p>` : '<p class="note">The associate has not written a recommendation yet.</p>'}</section>
        <section class="x-section" aria-label="The flags"><h2 class="x-h">The flags</h2>
          <div class="x-flags">${[...room.top_flags.green, ...room.top_flags.red].map((f) => X.flagCard(room, f, { noAsk: true })).join("")}</div></section>
        <div id="x-whatif-slot">${whatifHtml(room)}</div>
        <section class="x-section" aria-label="The memo"><h2 class="x-h">The memo</h2>
          <p class="x-yourview" id="x-yourview">Your view: ${views.filter((v) => v === "agree").length} agree, ${views.filter((v) => v === "disagree").length} disagree. Only you see it.</p>
          <article class="x-memo"><section class="x-memo-sec" aria-label="Header"><h3><span class="tc-meta">1</span>Header</h3>${head}</section>${sections}</article></section>
        <div class="actions"><a class="btn tc-btn primary" href="http://localhost:5173/">Open the built readout page</a>
          <button class="tc-btn tc-btn--secondary" type="button" id="to-start">Start with another company</button></div>`;
      bindWhatif(room);
      document.getElementById("to-start").addEventListener("click", () => T.go("start"));
      document.getElementById("reader").addEventListener("input", (e) => { st.reader = e.target.value || "Partner"; const el = document.getElementById("w-reader"); if (el) el.textContent = st.reader; });
    }
  }

  function bindWhatif(room) {
    const st = X.st();
    const slot = document.getElementById("x-whatif-slot");
    const upd = () => {
      const w = st.whatif;
      const pilot = document.getElementById("w-pilot");
      if (pilot) w.pilot = pilot.checked;
      w.churn = Math.max(0, Number(document.getElementById("w-churn").value) || 0) / 100;
      w.price = Math.max(0, Number(document.getElementById("w-price").value) || 0);
      w.pace = Number(document.getElementById("w-pace").value);
      const focus = document.activeElement && document.activeElement.id;
      slot.innerHTML = whatifHtml(room);
      bindWhatif(room);
      if (focus) { const el = document.getElementById(focus); if (el) el.focus(); }
    };
    slot.querySelectorAll("input").forEach((el) => el.addEventListener(el.type === "number" ? "change" : "input", upd));
  }

  document.addEventListener("click", (e) => {
    if (location.hash !== "#memo" && location.hash !== "#principal") return;
    const b = e.target.closest("[data-mline]");
    if (b) {
      const box = document.getElementById(`mc-${b.dataset.mline}`);
      const open = b.getAttribute("aria-expanded") === "true";
      b.setAttribute("aria-expanded", String(!open));
      if (box) box.hidden = open;
      return;
    }
    const v = e.target.closest("[data-view]");
    if (v) {
      const st = X.st();
      st.views[v.dataset.id] = st.views[v.dataset.id] === v.dataset.view ? null : v.dataset.view;
      const y = window.scrollY;
      render("principal");
      window.scrollTo(0, y);
    }
  });

  window.TC_STEPS.memo = () => render("associate");
  window.TC_STEPS.principal = () => render("principal");
})();
