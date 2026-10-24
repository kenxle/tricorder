// The working page once the founder's data room is in: "partial" (the first files arrived) or "full".
// The page keeps its shape: what stands out, each piece, the founders, comps, market signals, the
// outside world, then the requests. The room's data merges in: what stands out leads with the room's
// green and red flags, the pieces get verdicts, pre-room claims show whether the room confirms them,
// and anything a missing file would settle says what it waits on, beside its open request.
//
// For the working page (app.js):
//   TC_ROOM_VIEW.render(state)            redraws the whole working page into #app, room data merged in; returns nothing
//   TC_ROOM_VIEW.html(state)              the page body below the company name, as an HTML string
//   TC_ROOM_VIEW.blocks(state)            the same, as {banner, standsOut, pieces, research, requests, actions}
//   TC_ROOM_VIEW.preStatus(state, claim)  a mark for one research claim (confirmed by the room, waiting...)
//   TC_ROOM_VIEW.requestStatus(state, id) {status: "answered" | "open", files} for a checklist id
//   TC_ROOM_VIEW.model(state)             the state's data: arrived files, flags, pieces, answered ids
// state is "partial" or "full". For review: index.html?company=https://ploy.ai&room=partial (or full).
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;
  const params = new URLSearchParams(location.search);

  const room = () => X.room();
  const st = (state) => room() && room().states[state === "partial" ? "partial" : "full"];
  const title = (id) => { const c = window.TC.D.checklist.find((x) => x.id === id); return c ? c.title : id; };
  const short = (f) => f.split("/").pop();

  function model(state) { return st(state); }

  function requestStatus(state, id) {
    const s = st(state);
    if (!s || !id) return { status: "open", files: [] };
    const files = (room().holds[id] || []).map((f) => f.split(", ")[0]);
    return s.answered.includes(id) ? { status: "answered", files } : { status: "open", files: files.filter((f) => !s.arrived.includes(f)) };
  }

  const PRE = {
    confirms: '<span class="tc-mark tc-mark--strong">Confirmed by the room</span>',
    answers: '<span class="tc-mark">Answered by the room</span>',
    differs: '<span class="tc-mark tc-mark--disagreement">The room differs</span>',
    "not settled": '<span class="tc-mark tc-mark--thin">Not settled by the room</span>',
  };
  function preMark(state, i) {
    const r = room();
    const pc = r.prechecks[i];
    const status = st(state).prechecks[i];
    if (status === "waiting") {
      const f = pc.source.uri.split(", ")[0];
      const req = st(state).request_of[f];
      return `<span class="tc-label tc-label--gap">Waiting on ${esc(short(f))}</span>${req ? ` <span class="tc-mark tc-mark--running">Open request: ${esc(title(req))}</span>` : ""}`;
    }
    return `${PRE[status]} ${X.roomChip(pc.source)}`;
  }
  // The room's verdict on a research claim, matched by the claim's own source and quote.
  function preStatus(state, claim) {
    const r = room();
    if (!r || !claim) return "";
    const pre = window.TC.S.research.pre;
    const i = r.prechecks.findIndex((pc) => pre[pc.pre] && pre[pc.pre].source === claim.source && pre[pc.pre].quote === claim.quote);
    return i < 0 ? "" : `<span class="x-roomsays">${preMark(state, i)}</span>`;
  }

  function flagsOf(state) {
    const r = room();
    const s = st(state);
    const all = [...r.top_flags.green, ...r.top_flags.red, ...(r.extra_flags || [])];
    const pick = (ids) => ids.map((id) => all.find((f) => f.claim_id === id)).filter(Boolean);
    return X.orderFlags([...pick(s.flags.green), ...pick(s.flags.red)]);
  }

  function banner(state) {
    const r = room();
    const s = st(state);
    const company = X.company();
    const msg = state === "partial"
      ? `${company} shared part of its data room: ${s.arrived.length} of ${s.files_total} files. Tricorder read what arrived. The rest is on the open requests.`
      : `${company} shared its data room: all ${s.files_total} files are in. Tricorder read every one.`;
    return `<div class="x-roombanner" role="status"><span class="tc-label${state === "partial" ? " tc-label--gap" : " tc-label--clean"}">${state === "partial" ? "Partly in" : "Room in"}</span>
      <span>${esc(msg)}</span></div>
      <div id="notify"><p class="banner tc-synthetic x-synthetic" role="note">This data room is synthetic. The team wrote it for the demo. It is not ${esc(company)}'s data. Data as of ${esc(r.as_of)}.</p></div>`;
  }

  function standsOut(state) {
    const r = room();
    const s = st(state);
    const flags = X.flagsHtml(r, flagsOf(state));
    const waiting = s.waiting.map((w) => `<article class="tc-card x-waiting" data-waiting="${esc(w.piece)}">
        <div class="tc-card-head"><span class="tc-label tc-label--gap">Waiting on ${esc(w.files.map(short).join(", "))}</span></div>
        <h3 class="tc-card-title x-card-title">${esc(X.pieceOf(r, w.piece).label)}</h3>
        <p class="x-card-sub">${esc(X.subtitle(w.title))}</p><p>${esc(w.text)}</p>
        <div class="tc-card-foot">${w.requests.map((id) => `<span class="tc-mark tc-mark--running">Open request: ${esc(title(id))}</span>`).join(" ")}</div></article>`).join("");
    const insights = ((window.TC_INSIGHTS || {})[window.TC.S.research.slug] || []);
    const MARK = { strong: ["tc-mark--strong", "Looking strong"], weak: ["tc-mark--weak", "Looking weak"], mixed: ["tc-mark--mixed", "Mixed"], thin: ["tc-mark--thin", "Not enough yet"] };
    const outside = insights.length ? `<h3 class="x-sub">From the outside research, before the room</h3><div class="x-insights">${insights.map((ins) => {
      const [cls, label] = MARK[ins.mark] || MARK.thin;
      return `<article class="tc-card x-insight"><div class="tc-card-head"><span class="tc-mark ${cls}">${label}</span><span class="tc-meta">${esc(ins.piece)}</span></div>
        <h3 class="tc-card-title">${esc(ins.title)}</h3><p>${esc(ins.text)}</p><div class="tc-card-foot">${X.pick(`insight:${insights.indexOf(ins)}`)}</div></article>`;
    }).join("")}</div>` : "";
    return `<section class="x-section" aria-label="What stands out"><h2 class="x-h">What stands out</h2>
      <h3 class="x-sub">From the data room</h3>
      ${flags}${waiting ? `<h3 class="x-sub">Waiting on files</h3><div class="x-flags">${waiting}</div>` : ""}${outside}</section>`;
  }

  function pieces(state) {
    const r = room();
    const s = st(state);
    return `<section class="x-section" aria-label="Each piece of the company"><h2 class="x-h">Each piece of the company</h2>
      <div class="x-verdicts">${r.pieces.map((p) => {
        const v = s.pieces[p.name];
        const wait = v.waiting.length ? `<span class="x-wait">${v.waiting.map((f) => {
          const req = s.request_of[f];
          return `<span class="tc-label tc-label--gap">Waiting on ${esc(short(f))}</span>${req ? ` <span class="tc-mark tc-mark--running">Open request: ${esc(title(req))}</span>` : ""}`;
        }).join(" ")}</span>` : "";
        const word = v.verdict === "not_enough_in_the_room" && v.waiting.length ? "not enough yet" : "";
        return X.verdictRow({ ...p, verdict: v.verdict, reason: v.reason, agree: v.agree, disagree: v.disagree, word }, wait);
      }).join("")}</div></section>`;
  }

  // The outside research, in the working page's order, each claim marked with what the room says about it.
  const ORDER = ["The founders", "Comps", "Market signals", "The outside world"];
  function research(state) {
    const R = window.TC.S.research;
    const secs = [...R.sections].sort((a, b) => ORDER.indexOf(a.title) - ORDER.indexOf(b.title));
    const numbered = X.researchNumbered();
    const row = (c) => c.placeholder
      ? `<li class="x-claim x-ph"><span class="claim-text">${esc(c.text)}</span> <span class="tc-mark tc-mark--thin">Not researched yet</span></li>`
      : `<li class="x-claim"><div class="x-claim-head"><span class="claim-text">${esc(c.text)}</span>${preStatus(state, c)}</div>
          <div class="tc-chips">${window.TC.chip(c.source, c)}${X.pick(`claim:${numbered.indexOf(c) + 1}`)}</div></li>`;
    const pre = room().prechecks.map((pc, i) => ({ pc, i })).filter(({ pc }) => !secs.some((s) => (s.parts ? s.parts.flatMap((p) => p.claims) : s.cards ? s.cards.flatMap((c) => c.claims) : s.claims)
      .some((c) => preStatus(state, c) && R.pre[pc.pre] && c.quote === R.pre[pc.pre].quote)));
    const body = secs.map((s) => {
      let inner;
      if (s.parts) inner = s.parts.map((p) => p.claims.length ? `<h3 class="x-sub">${esc(p.label)}</h3><ul class="x-claims">${p.claims.map(row).join("")}</ul>` : "").join("");
      else if (s.cards) inner = `<div class="x-cards">${s.cards.map((c) => `<article class="tc-card"><h3 class="tc-card-title">${esc(c.name)}</h3><p class="tc-meta">${esc(c.role)}</p><ul class="x-claims">${c.claims.map(row).join("")}</ul></article>`).join("")}</div>`;
      else inner = `<ul class="x-claims">${s.claims.map(row).join("")}</ul>`;
      return `<section class="x-section" aria-label="${esc(s.title)}"><h2 class="x-h">${esc(s.title)}</h2>${inner}</section>`;
    }).join("");
    const extra = pre.length ? `<section class="x-section" aria-label="Other pre-room claims"><h2 class="x-h">Other claims from before the room</h2>
      <ul class="x-claims">${pre.map(({ pc, i }) => { const c = R.pre[pc.pre]; return `<li class="x-claim"><div class="x-claim-head"><span class="claim-text">${esc(c.text)}</span><span class="x-roomsays">${preMark(state, i)}</span></div><div class="tc-chips">${window.TC.chip(c.source, c)}</div></li>`; }).join("")}</ul></section>` : "";
    return body + extra;
  }

  function requests(state) {
    const T = window.TC;
    if (!T.S.items) T.buildItems();
    const items = T.S.items.filter((i) => i.checked);
    const rows = items.map((it) => {
      const r = it.id ? requestStatus(state, it.id) : { status: "open", files: [] };
      const held = it.id && room().holds[it.id];
      const status = r.status === "answered"
        ? `<span class="tc-label tc-label--clean">Answered</span>`
        : `<span class="tc-mark tc-mark--running">Open</span>${held && r.files.length ? ` <span class="tc-label tc-label--gap">Waiting on ${esc(r.files.map(short).join(", "))}</span>` : ""}`;
      const files = r.status === "answered" ? `<div class="tc-chips">${room().holds[it.id].map((f) => X.roomChip({ uri: f.split(", ")[0], locator: f.split(", ")[1] || "whole file", quote: "Received with the room." })).join("")}</div>` : "";
      return `<li class="x-tick req" data-request="${esc(r.status)}" data-state="${esc(r.status)}">${status}<span class="x-tick-title">${esc(it.title)}</span>${files}</li>`;
    }).join("");
    const n = items.filter((it) => it.id && requestStatus(state, it.id).status === "answered").length;
    return `<section class="x-section" aria-label="Data room requests"><h2 class="x-h">Data room requests</h2>
      <p class="note">${n} of ${items.length} answered. The rest stay open.</p><ul class="x-ticks">${rows}</ul></section>`;
  }

  function actions() {
    return `<div class="actions"><button class="tc-btn primary" type="button" data-room-go="steer">Steer the readout</button>
      <a class="btn tc-btn tc-btn--secondary" href="#flags">See the flags from the room</a>
      <button class="tc-btn tc-btn--secondary" type="button" data-room-go="memo">Make the memo</button>
      <a class="btn tc-btn tc-btn--secondary" href="http://localhost:5173/">Open the built readout page</a></div>`;
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-room-go]");
    if (b) window.TC.go(b.dataset.roomGo);
  });

  function blocks(state) {
    if (!room()) return null;
    const reports = (room().reports || []).map((r) => X.reportBlock(room(), r, state)).join("");
    return { banner: banner(state), standsOut: standsOut(state), pieces: pieces(state), reports, research: research(state), requests: requests(state), actions: actions() };
  }
  function html(state) {
    const b = blocks(state);
    if (!b) return `<div class="empty" role="status"><strong>No synthetic data room for this company yet.</strong> Ploy and Sazabi have one.</div>`;
    return `<div class="x-roomview" data-room-state="${esc(state)}">${b.banner}${b.standsOut}${b.pieces}${b.reports}${b.research}${b.requests}${b.actions}</div>`;
  }

  // The whole working page, redrawn with the room's data in. state: "partial" or "full" (the default).
  function render(state) {
    const T = window.TC;
    // "partial" only when asked for by the review URL or when the page marks the room partly in
    // (S.roomPartial). A request the room never holds stays open even when every file is in.
    const s = state === "partial" && (params.get("room") === "partial" || T.S.roomPartial) ? "partial" : "full";
    T.app.innerHTML = `${T.header("room")}<h2 class="co-title" id="co-name">${esc(X.company())}</h2>${html(s)}`;
    X.drawCharts(T.app);
    window.scrollTo(0, 0);
  }

  window.TC_ROOM_VIEW = { render, html, blocks, preStatus, requestStatus, model };

  // For review by URL: ?company=...&room=partial or &room=full opens the working page in that state.
  window.TC_STEPS = window.TC_STEPS || {};
  window.TC_STEPS.room = () => {
    const T = window.TC;
    render(params.get("room") === "partial" ? "partial" : "full");
  };
  if (params.get("room")) window.addEventListener("load", () => { if (window.TC && window.TC.S.fields) location.hash = "room"; });
})();
