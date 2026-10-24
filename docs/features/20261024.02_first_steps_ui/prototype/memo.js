// Steps 7 and 8: the memo. A document about the company and its investment case, written from the
// associate's working page with the noise taken out (Ken, 2:14 PM). It reads top to bottom in prose:
// what the company does, the investment case, what is strong, what is weak and why, what is still
// unknown and what was asked, and the recommendation. The evidence behind each paragraph sits behind
// numbered references (hover for the fact and its source) and an Evidence toggle that expands the flags
// and claims in place. Nothing is a PDF.
//
// Step 7 (#memo): the associate's view. They write the recommendation, then "Send to the partners".
// Step 8 (#principal): the partner reviewing it. Each paragraph takes agree, disagree and a question,
// the investment case has a what-if, and a chat beside the memo answers questions from the memo's own
// content and jumps to the paragraph that answers it.
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;

  function money(n) { return `$${Math.round(n).toLocaleString("en-US")}`; }
  const lower = (s) => s.charAt(0).toLowerCase() + s.slice(1);
  const listText = (xs) => (xs.length < 2 ? xs.join("") : `${xs.slice(0, -1).join(", ")} and ${xs[xs.length - 1]}`);

  // The what-if: the same rules the scripts use, run in the page. Its defaults give Tricorder's rebuilt figures.
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

  // Evidence: every fact a paragraph rests on gets one number for the whole memo.
  function evidence(room) {
    const T = window.TC;
    const map = new Map();
    const research = (T.S.research.sections || []).flatMap((s) => s.parts ? s.parts.flatMap((p) => p.claims) : s.cards ? s.cards.flatMap((c) => c.claims) : s.claims)
      .filter((c) => !c.placeholder);
    const srcLabel = (s) => (s.public ? s.uri : `${s.uri}, ${s.locator}`);
    return {
      map,
      room(id) {
        const c = room.claims[id];
        if (!c) return null;
        const key = `c:${id}`;
        if (!map.has(key)) map.set(key, { n: map.size + 1, key, text: c.text, src: c.sources.map(srcLabel).join("; "), html: X.claimBody(c) });
        return key;
      },
      research(fragment) {
        const c = research.find((x) => x.text.includes(fragment));
        if (!c) return null;
        const key = `r:${c.source}:${c.quote}`;
        if (!map.has(key)) map.set(key, { n: map.size + 1, key, text: c.text, src: T.D.sources[c.source].title,
          html: `<div class="x-claim-head"><span class="claim-text">${esc(c.text)}</span></div><div class="tc-chips">${T.chip(c.source, c)}</div>` });
        return key;
      },
      source(s, text) {
        const key = `s:${s.uri}:${s.locator}`;
        if (!map.has(key)) map.set(key, { n: map.size + 1, key, text, src: srcLabel(s), html: `<div class="x-claim-head"><span class="claim-text">${esc(text)}</span></div>${X.chips([s])}` });
        return key;
      },
    };
  }

  // The memo as paragraphs. The chat answers from the same paragraphs, so its links always land on the memo.
  function build(room) {
    const T = window.TC;
    const st = X.st();
    const ev = evidence(room);
    const company = X.company();
    // Only what the associate picked reaches the memo (memo_picks.js): flags and insights are in unless taken out.
    const flags = X.orderFlags([...room.top_flags.green, ...room.top_flags.red]).filter((f) => X.picked(`flag:${f.claim_id}`));
    const headline = flags.filter((f) => X.weight(f) === "headline");
    const reds = flags.filter((f) => X.weight(f) === "big");
    const small = flags.filter((f) => X.weight(f) === "small");
    const steersOn = (piece) => st.steers.filter((s) => s.piece === piece);
    const reasonOf = (p) => { const rw = steersOn(p.name).filter((s) => s.kind === "rewrite").pop(); return rw ? rw.after : p.reason; };
    const steerNotes = (piece) => steersOn(piece).filter((s) => s.kind === "figure" || s.kind === "note").map((s) => s.kind === "figure"
      ? ` The associate's own figure is ${s.steer_value}, beside the check's ${s.check_value}.` : ` The associate notes: "${s.sentence}"`).join("");
    const refs = (ids) => ids.map((id) => ev.room(id)).filter(Boolean);
    const secs = [];
    let pn = 0;
    const P = (sec, p) => { p.id = `p${++pn}`; sec.paras.push(p); return p; };

    // What the company does
    const about = (window.TC_ABOUT || {})[T.S.research.slug];
    const s1 = { key: "about", title: "What the company does", paras: [] };
    if (about) P(s1, { kind: "about", lead: "", body: about.text, refs: about.refs.map((r) => ev.research(r)).filter(Boolean) });
    const history = room.memo_company.split(". ").slice(1).join(". ");
    P(s1, { kind: "history", lead: "", body: history, refs: [ev.source(room.round.source, `The round on the deck: ${room.round.raise} at ${room.round.pre_money} pre-money.`), ...refs(["lc-1", "lc-2"])].filter(Boolean) });
    secs.push(s1);

    // The outside research the associate kept: the first readout's insights, and any evidence row they put in.
    const insights = ((window.TC_INSIGHTS || {})[T.S.research.slug] || []).map((ins, i) => ({ ins, i })).filter(({ i }) => X.picked(`insight:${i}`));
    if (insights.length) {
      const so = { key: "outside", title: "What the outside research shows", paras: [] };
      insights.forEach(({ ins }) => P(so, { kind: "insight", lead: ins.title, body: ins.text, refs: ins.refs.map((r) => ev.research(r)).filter(Boolean) }));
      secs.push(so);
    }

    // The investment case
    const op = st.op;
    const s2 = { key: "case", title: "The investment case", paras: [] };
    const rec = op.rec ? `The associate recommends: ${op.rec}${op.amount ? `, ${op.amount}` : ""}. ` : "";
    P(s2, { kind: "case", lead: rec ? rec.trim() : "",
      body: `${company} asks for ${room.round.raise} at ${room.round.pre_money} pre-money (${room.round.post_money} after the round), so the new money would own ${room.round.ownership}. `
        + `The data room backs ${headline.length} clear strength${headline.length === 1 ? "" : "s"} and ${small.length ? `${small.length} figure${small.length === 1 ? "" : "s"} that check out across sources` : "no cross-checked figures"}, `
        + `and turns up ${reds.length} place${reds.length === 1 ? "" : "s"} where the company's own numbers do not hold.`,
      refs: [ev.source(room.round.source, `The round on the deck: ${room.round.raise} at ${room.round.pre_money} pre-money.`)], whatif: true });
    secs.push(s2);

    // What is strong
    const s3 = { key: "strong", title: "What is strong", paras: [] };
    const covered = new Set();
    headline.forEach((f) => { covered.add(f.piece); P(s3, { kind: "flag", lead: f.title, body: (f.why || "") + steerNotes(f.piece), refs: refs([f.claim_id]), flag: f, piece: f.piece }); });
    room.pieces.filter((p) => p.verdict === "looking_strong" && !covered.has(p.name))
      .forEach((p) => P(s3, { kind: "piece", lead: `${p.label}.`, body: reasonOf(p) + steerNotes(p.name), refs: refs(p.claim_ids), piece: p.name }));
    if (small.length) P(s3, { kind: "small", lead: "Figures that check out across sources.", body: small.map((f) => f.title).join(" "), refs: refs(small.map((f) => f.claim_id)), flags: small });
    secs.push(s3);

    // What is weak, and why
    const s4 = { key: "weak", title: "What is weak, and why", paras: [] };
    const weakCovered = new Set();
    reds.forEach((f) => {
      weakCovered.add(f.piece);
      P(s4, { kind: "flag", lead: f.title, body: `The company states ${f.stated.value}; the room shows ${f.found.value} (${f.found.key.replace(/^Found, /, "")}). ${f.why || ""}${steerNotes(f.piece)}`,
        refs: refs([f.claim_id]), flag: f, piece: f.piece });
    });
    room.pieces.filter((p) => (p.verdict === "looking_weak" || p.verdict === "mixed") && !weakCovered.has(p.name))
      .forEach((p) => P(s4, { kind: "piece", lead: `${p.label}${p.verdict === "mixed" ? ", mixed" : ""}.`, body: reasonOf(p) + steerNotes(p.name), refs: refs(p.claim_ids), piece: p.name }));
    secs.push(s4);

    // Evidence the associate put in by hand: first-readout rows and the room's own claims.
    const numbered = X.researchNumbered();
    const hand = [
      ...numbered.map((c, i) => ({ c, key: `claim:${i + 1}` })).filter((x) => X.picked(x.key)).map((x) => ({ text: x.c.text, ref: ev.research(x.c.text.slice(0, 60)) })),
      ...Object.keys(room.claims).filter((id) => X.picked(`room:${id}`)).map((id) => ({ text: room.claims[id].text, ref: ev.room(id) })),
    ];
    if (hand.length) {
      const sh = { key: "picked", title: "Evidence the associate added", paras: [] };
      hand.forEach((h) => P(sh, { kind: "picked", lead: "", body: h.text, refs: [h.ref].filter(Boolean) }));
      secs.push(sh);
    }

    // The reports, read through Kimmy's expert knowledge, each with its chart.
    (room.reports || []).forEach((rep) => {
      const sr = { key: `report-${rep.key}`, title: rep.title, paras: [], report: rep };
      rep.paras.forEach((p) => P(sr, { kind: "report", lead: p.lead, body: p.body, refs: refs(p.refs) }));
      P(sr, { kind: "asks", lead: "What to ask.", body: rep.asks.join(" "), refs: [] });
      secs.push(sr);
    });

    // What is still unknown, and what was asked
    const s5 = { key: "unknown", title: "What is still unknown, and what was asked", paras: [] };
    room.pieces.filter((p) => p.verdict === "not_enough_in_the_room")
      .forEach((p) => P(s5, { kind: "piece", lead: `${p.label}.`, body: reasonOf(p), refs: refs(p.claim_ids), piece: p.name }));
    if (!T.S.items) T.buildItems();
    const asked = T.S.items.filter((i) => i.checked);
    const missing = asked.filter((i) => !(i.id && room.holds[i.id]) && !i.custom).map((i) => lower(i.title));
    const questions = asked.filter((i) => i.custom).map((i) => i.ask.replace(/\.$/, ""));
    if (missing.length) P(s5, { kind: "asked", lead: "Asked of the founder, not yet in the room.", body: `${listText(missing)}.`, refs: [] });
    if (questions.length) P(s5, { kind: "questions", lead: "Questions put to the founder.", body: questions.map((q) => `${q}.`).join(" "), refs: [] });
    secs.push(s5);

    // The recommendation
    const s6 = { key: "rec", title: "Recommendation", paras: [] };
    P(s6, { kind: "rec", lead: op.rec ? `${op.rec}${op.amount ? `, ${op.amount}` : ""}.` : "",
      body: [op.reasons && `The two reasons that decide it: ${op.reasons}`, op.wrong && `Why it could be wrong: ${op.wrong}`].filter(Boolean).join(" ")
        || (op.rec ? "" : "The associate has not written a recommendation yet."), refs: [] });
    secs.push(s6);
    return { secs, ev };
  }

  // A paragraph: prose, numbered evidence, and the evidence in place behind a toggle.
  function paraHtml(room, p, built, mode) {
    const st = X.st();
    const nums = p.refs.map((k) => built.ev.map.get(k)).filter(Boolean);
    const refsHtml = nums.length ? ` <span class="x-refs">${nums.map((e) => `<button type="button" class="x-ev" data-ev="${esc(e.key)}" data-para="${p.id}" aria-label="Evidence ${e.n}">${e.n}</button>`).join("")}</span>` : "";
    const flagCards = p.flag ? X.flagCard(room, p.flag, { noAsk: true, noPick: true }) : p.flags ? `<ul class="x-smallflags">${p.flags.map((f) => X.smallFlag(room, f, { noPick: true })).join("")}</ul>` : "";
    const evList = nums.length ? `<ol class="x-evlist">${nums.map((e) => `<li class="x-claim" id="ev-${p.id}-${e.n}" value="${e.n}">${e.html}</li>`).join("")}</ol>` : "";
    const hasEv = !!(flagCards || evList);
    const v = st.views[p.id];
    const q = (st.partnerQs || []).filter((x) => x.para === p.id);
    const partner = mode === "principal" ? `<span class="x-para-acts">
        <button type="button" class="tc-link-btn" data-view="agree" data-id="${p.id}" aria-pressed="${v === "agree"}">Agree</button>
        <button type="button" class="tc-link-btn" data-view="disagree" data-id="${p.id}" aria-pressed="${v === "disagree"}">Disagree</button>
        <button type="button" class="tc-link-btn" data-askpara="${p.id}">Ask</button></span>` : "";
    const marks = [v === "agree" ? '<span class="tc-mark">You agree</span>' : v === "disagree" ? '<span class="tc-mark tc-mark--disagreement">You disagree</span>' : "",
      ...q.map((x) => `<span class="x-partnerq"><span class="tc-label tc-label--ask">Your question</span> ${esc(x.text)}</span>`)].join("");
    return `<div class="x-para" id="${p.id}" data-kind="${esc(p.kind)}">
      <p>${p.lead ? `<strong>${esc(p.lead)}</strong> ` : ""}${esc(p.body)}${refsHtml}</p>
      ${hasEv || partner ? `<div class="x-para-tools">${hasEv ? `<button type="button" class="tc-link-btn" data-evtoggle="${p.id}" aria-expanded="false">Evidence${nums.length ? ` (${nums.length})` : ""}</button>` : ""}${partner}</div>` : ""}
      ${marks ? `<div class="x-para-marks">${marks}</div>` : ""}
      <div class="x-askslot" data-askslot="${p.id}"></div>
      ${hasEv ? `<div class="x-para-ev" id="ev-${p.id}" hidden>${flagCards}${evList}</div>` : ""}
    </div>`;
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
    return `<div class="x-whatif" aria-label="What if">
      <p class="note">Change an assumption and the same rules recompute. A what-if changes no flag and stays in your copy.</p>
      <div class="x-whatif-controls">
        ${W.pilot ? `<label class="x-checkrow"><input class="tc-check" type="checkbox" id="w-pilot"${w.pilot ? " checked" : ""} /> Count the ${esc(W.pilot.name)} pilot as recurring</label>` : ""}
        <div><label class="tc-label" for="w-churn">Monthly churn, %</label><input class="tc-input" type="number" id="w-churn" step="0.5" min="0" max="20" value="${(w.churn * 100).toFixed(1)}" /></div>
        <div><label class="tc-label" for="w-price">${esc(tweak.name)} price, $ a month</label><input class="tc-input" type="number" id="w-price" step="10" min="0" value="${w.price}" /></div>
        <div><label class="tc-label" for="w-pace">Hiring pace: ${Math.round(w.pace * W.extra_count)} of the ${W.extra_count} hires the model leaves out</label><input type="range" id="w-pace" min="0" max="1" step="0.05" value="${w.pace}" /></div>
      </div>
      <div class="tc-table-wrap"><table class="tc-table tc-table--stack x-wtable"><thead><tr><th>Figure</th><th class="tc-fig">The company's</th><th class="tc-fig">Tricorder's rebuilt</th><th class="tc-fig x-scn">Your scenario</th></tr></thead>
        <tbody>${rows.map((row) => `<tr><td data-label="Figure">${esc(row[0])}</td><td class="tc-fig" data-label="The company's">${esc(row[1])}</td><td class="tc-fig" data-label="Tricorder's rebuilt">${esc(row[2])}</td><td class="tc-fig x-scn" data-label="Your scenario">${esc(row[3])}</td></tr>`).join("")}</tbody></table></div>
    </div>`;
  }

  function opFields() {
    const op = X.st().op;
    const ta = (k, label) => `<label class="tc-label" for="op-${k}">${label}</label><textarea class="tc-input" id="op-${k}" data-op="${k}">${esc(op[k])}</textarea>`;
    return `<div class="x-op"><label class="tc-label" for="op-rec">Invest, pass or wait</label>
      <select class="tc-input" id="op-rec" data-op="rec"><option value="">Choose</option>${["Invest", "Pass", "Wait"].map((o) => `<option${op.rec === o ? " selected" : ""}>${o}</option>`).join("")}</select>
      <label class="tc-label" for="op-amount">Amount and conditions</label><input class="tc-input" type="text" id="op-amount" data-op="amount" value="${esc(op.amount)}" />
      ${ta("reasons", "The two reasons that decide it")}${ta("wrong", "Why it could be wrong")}</div>`;
  }

  // The chat beside the partner's view. It answers from the memo's paragraphs and links to them.
  function suggestions(built, room) {
    const flags = built.secs.find((s) => s.key === "weak").paras.filter((p) => p.kind === "flag");
    return [
      "What does the company do?",
      "What is the round?",
      ...flags.slice(0, 2).map((p) => `Why is ${lower(X.pieceOf(room, p.piece).label)} a red flag?`),
      "What is strong?",
      "What is still missing?",
      "What does the associate recommend?",
    ];
  }
  function answer(question, built, room) {
    const q = question.toLowerCase();
    const sec = (k) => built.secs.find((s) => s.key === k);
    const first = (p) => `${p.lead ? `${p.lead} ` : ""}${p.body.split(/(?<=\.)\s/)[0]}`;
    const all = built.secs.flatMap((s) => s.paras);
    const byPiece = all.find((p) => p.piece && (() => {
      const label = X.pieceOf(room, p.piece).label.toLowerCase();
      const words = { traction_and_revenue: ["arr", "revenue", "traction", "pilot"], unit_economics: ["margin", "unit economics", "inference", "credits"],
        burn_and_runway: ["runway", "burn", "hires", "hiring"], legal_and_cap_table: ["cap table", "safe", "signed", "legal"], market: ["market"],
        customers: ["customer", "concentration"], retention: ["retention", "churn", "nrr"], team: ["team", "founder"], the_pitch_itself: ["pitch", "deck"],
        outside_world: ["outside", "public"] }[p.piece] || [];
      return q.includes(label) || words.some((w) => q.includes(w));
    })());
    if (/missing|unknown|asked|waiting|still need/.test(q)) {
      const ps = sec("unknown").paras;
      return { text: ps.length ? ps.map(first).join(" ") : "Nothing is still missing.", links: ps.map((p) => p.id) };
    }
    if (/recommend|invest|pass|verdict/.test(q)) { const p = sec("rec").paras[0]; return { text: p.lead ? first(p) : "The associate has not written a recommendation yet.", links: [p.id] }; }
    if (/strong|good|green|strength/.test(q)) { const ps = sec("strong").paras; return { text: ps.map((p) => p.lead || first(p)).join(" "), links: ps.map((p) => p.id) }; }
    if (/round|raise|valuation|price|own/.test(q) && !/red flag/.test(q)) { const p = sec("case").paras[0]; return { text: first({ ...p, lead: "" }), links: [p.id] }; }
    if (byPiece) return { text: first(byPiece), links: [byPiece.id] };
    if (/what (does|do)|company|business|product/.test(q)) { const p = sec("about").paras[0]; return { text: first(p), links: [p.id] }; }
    if (/red|weak|risk|problem|wrong|flag/.test(q)) { const ps = sec("weak").paras; return { text: ps.map((p) => p.lead).join(" "), links: ps.map((p) => p.id) }; }
    return { text: "I answer from this memo only. Try one of the questions below, or name a part of the company, such as the margin or the runway.", links: [] };
  }
  function chatHtml(built, room) {
    const st = X.st();
    const msgs = (st.chat || []).map((m) => m.who === "you"
      ? `<li class="x-msg x-msg--you">${esc(m.text)}</li>`
      : `<li class="x-msg x-msg--memo">${esc(m.text)}${m.links.length ? `<div class="x-msg-links">${m.links.map((id) => {
          const p = built.secs.flatMap((s) => s.paras).find((x) => x.id === id);
          const sec = built.secs.find((s) => s.paras.includes(p));
          return p ? `<button type="button" class="tc-chip" data-goto="${id}">${esc(p.lead ? p.lead.replace(/\.$/, "") : sec.title)}</button>` : "";
        }).join("")}</div>` : ""}</li>`).join("");
    return `<aside class="x-chat" aria-label="Ask about this memo">
      <h3>Ask about this memo</h3>
      <p class="note">Answers come from the memo and take you to the paragraph.</p>
      <ol class="x-msgs" id="x-msgs" aria-live="polite">${msgs}</ol>
      <div class="x-suggest">${suggestions(built, room).map((s) => `<button type="button" class="tc-chip" data-suggest="${esc(s)}">${esc(s)}</button>`).join("")}</div>
      <form class="x-chatform" id="x-chatform"><input class="tc-input" type="text" id="x-chatin" placeholder="Ask about the memo" aria-label="Ask about the memo" />
        <button class="tc-btn tc-btn--small" type="submit">Ask</button></form>
    </aside>`;
  }

  function render(mode) {
    const T = window.TC;
    const room = X.room();
    const step = mode === "principal" ? "principal" : "memo";
    if (!room) return X.noRoom(step);
    const st = X.st();
    const company = X.company();
    const built = build(room);
    const who = T.S.sender || "The associate";
    const sent = st.sentAt ? `Sent to the partners at ${st.sentAt.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}` : "Draft, not sent yet";
    const sections = built.secs.map((s) => `<section class="x-memo-sec" aria-label="${esc(s.title)}" data-sec="${s.key}">
        <h3>${esc(s.title)}</h3>
        ${s.report ? `${X.kimmyLine(s.report)}${X.reportChart(s.report)}` : ""}
        ${s.paras.map((p) => paraHtml(room, p, built, mode)).join("")}
        ${s.key === "case" && mode === "principal" ? `<details class="x-whatif-d"><summary>Try a what-if</summary><div id="x-whatif-slot">${whatifHtml(room)}</div></details>` : ""}
        ${s.key === "rec" && mode === "associate" ? opFields() : ""}
      </section>`).join("");
    const head = `<header class="x-memohead">
        <p class="tc-label">Investment memo</p>
        <h2 class="co-title">${esc(company)}</h2>
        <p class="x-memohead-sub">${esc(room.round.name)}: ${esc(room.round.raise)} at ${esc(room.round.pre_money)} pre-money</p>
        <p class="tc-meta">From ${esc(who)} · Data room as of ${esc(room.as_of)} · ${esc(sent)}</p>
        <p class="tc-synthetic">This data room is synthetic. The team wrote it for the demo. It is not ${esc(company)}'s data.</p>
      </header>`;
    if (mode === "associate") {
      T.app.innerHTML = `${T.header("memo")}
        <article class="x-memo x-doc">${head}${sections}</article>
        <div class="actions"><button class="tc-btn primary" type="button" id="send-memo">Send to the partners</button></div>`;
      X.drawCharts(T.app);
      document.getElementById("send-memo").addEventListener("click", () => { st.sentAt = new Date(); T.go("principal"); });
      T.app.querySelectorAll("[data-op]").forEach((el) => el.addEventListener("change", () => { st.op[el.dataset.op] = el.value; render(mode); }));
    } else {
      const views = Object.values(st.views).filter(Boolean);
      T.app.innerHTML = `${T.header("principal")}
        <p class="x-review tc-meta">Reviewing as ${esc(st.reader)} · ${views.filter((v) => v === "agree").length} agree, ${views.filter((v) => v === "disagree").length} disagree, ${(st.partnerQs || []).length} questions. Only you see these.</p>
        <div class="x-reviewgrid">
          <article class="x-memo x-doc">${head}${sections}</article>
          ${chatHtml(built, room)}
        </div>
        <div class="actions"><a class="btn tc-btn tc-btn--secondary" href="http://localhost:5173/">Open the built readout page</a>
          <button class="tc-btn tc-btn--secondary" type="button" id="to-start">Start with another company</button></div>`;
      X.drawCharts(T.app);
      document.getElementById("to-start").addEventListener("click", () => T.go("start"));
      bindWhatif(room);
      bindChat(built, room);
    }
  }

  function bindWhatif(room) {
    const st = X.st();
    const slot = document.getElementById("x-whatif-slot");
    if (!slot) return;
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

  function goTo(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    el.classList.remove("x-hl");
    void el.offsetWidth;
    el.classList.add("x-hl");
  }
  function ask(text, built, room) {
    const st = X.st();
    st.chat = st.chat || [];
    const a = answer(text, built, room);
    st.chat.push({ who: "you", text }, { who: "memo", text: a.text, links: a.links });
    const box = document.querySelector(".x-chat");
    box.outerHTML = chatHtml(built, room);
    bindChat(built, room);
    const list = document.getElementById("x-msgs");
    list.scrollTop = list.scrollHeight;
    if (a.links[0]) goTo(a.links[0]);
  }
  function bindChat(built, room) {
    const form = document.getElementById("x-chatform");
    if (!form) return;
    form.addEventListener("submit", (e) => { e.preventDefault(); const v = document.getElementById("x-chatin").value.trim(); if (v) ask(v, built, room); });
    document.querySelectorAll("[data-suggest]").forEach((b) => b.addEventListener("click", () => ask(b.dataset.suggest, built, room)));
  }

  // Evidence numbers: hover or focus shows the fact and its source; a click opens the evidence in place.
  let tip = null;
  const hideTip = () => { if (tip) { tip.remove(); tip = null; } };
  function showTip(b) {
    hideTip();
    const room = X.room();
    if (!room) return;
    const built = build(room);
    const e = built.ev.map.get(b.dataset.ev);
    if (!e) return;
    tip = document.createElement("div");
    tip.className = "ev-tip";
    tip.setAttribute("role", "tooltip");
    tip.innerHTML = `<span class="ev-tip-n">${e.n}</span> ${esc(e.text)}<span class="ev-tip-src">Source: ${esc(e.src)}</span>`;
    document.body.appendChild(tip);
    const r = b.getBoundingClientRect();
    const w = Math.min(380, window.innerWidth - 32);
    tip.style.width = `${w}px`;
    tip.style.left = `${Math.max(16, Math.min(window.scrollX + r.left, window.scrollX + window.innerWidth - w - 16))}px`;
    tip.style.top = `${window.scrollY + r.bottom + 8}px`;
  }
  const onMemo = () => location.hash === "#memo" || location.hash === "#principal";
  document.addEventListener("mouseover", (e) => { const b = e.target.closest(".x-ev"); if (b && onMemo()) showTip(b); });
  document.addEventListener("mouseout", (e) => { if (e.target.closest(".x-ev")) hideTip(); });
  document.addEventListener("focusin", (e) => { const b = e.target.closest(".x-ev"); if (b && onMemo()) showTip(b); });
  document.addEventListener("focusout", (e) => { if (e.target.closest(".x-ev")) hideTip(); });

  function toggleEv(pid, open) {
    const box = document.getElementById(`ev-${pid}`);
    const btn = document.querySelector(`[data-evtoggle="${pid}"]`);
    if (!box || !btn) return;
    const show = open === undefined ? box.hidden : open;
    box.hidden = !show;
    btn.setAttribute("aria-expanded", String(show));
  }

  document.addEventListener("click", (e) => {
    if (!onMemo()) return;
    const st = X.st();
    const t = e.target.closest("[data-evtoggle], .x-ev, [data-view], [data-askpara], [data-goto]");
    if (!t) return;
    if (t.dataset.evtoggle) return toggleEv(t.dataset.evtoggle);
    if (t.classList.contains("x-ev")) {
      hideTip();
      toggleEv(t.dataset.para, true);
      const n = X.room() && build(X.room()).ev.map.get(t.dataset.ev);
      if (n) goTo(`ev-${t.dataset.para}-${n.n}`);
      return;
    }
    if (t.dataset.goto) return goTo(t.dataset.goto);
    if (t.dataset.view) {
      st.views[t.dataset.id] = st.views[t.dataset.id] === t.dataset.view ? null : t.dataset.view;
      const y = window.scrollY;
      render("principal");
      window.scrollTo(0, y);
      return;
    }
    if (t.dataset.askpara) {
      const slot = document.querySelector(`[data-askslot="${t.dataset.askpara}"]`);
      slot.innerHTML = `<form class="x-steerbox"><input class="tc-input" type="text" aria-label="Your question to the associate" placeholder="Your question to the associate" />
        <button class="tc-btn tc-btn--small" type="submit">Send</button></form>`;
      const f = slot.querySelector("form");
      f.querySelector("input").focus();
      f.addEventListener("submit", (ev) => {
        ev.preventDefault();
        const v = f.querySelector("input").value.trim();
        if (!v) return;
        st.partnerQs = st.partnerQs || [];
        st.partnerQs.push({ para: t.dataset.askpara, text: v });
        const y = window.scrollY;
        render("principal");
        window.scrollTo(0, y);
      });
    }
  });

  window.TC_STEPS.memo = () => render("associate");
  window.TC_STEPS.principal = () => render("principal");
})();
