// Shared pieces for steps 5 to 8: the synthetic room, its source chips, marks, range strips and claim lines.
// app.js exposes window.TC (state and helpers) and routes a step to window.TC_STEPS[name].
(function () {
  "use strict";
  window.TC_STEPS = window.TC_STEPS || {};
  const X = (window.TCX = {});

  X.esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const esc = X.esc;

  X.room = () => (window.TC.S.research && window.TC.S.research.room) || null;
  X.company = () => window.TC.S.fields.name.value || "This company";

  // Per-company state for steps 5 to 8. It resets when a new company is fed in.
  X.st = () => {
    const S = window.TC.S;
    if (!S.x5 || S.x5.url !== S.url) {
      S.x5 = { url: S.url, steers: [], lineViews: {}, linesOpen: {}, op: { rec: "", amount: "", reasons: "", wrong: "", down: "", base: "", up: "" },
        views: {}, reader: "Partner", whatif: null, asked: {} };
    }
    return S.x5;
  };

  X.notice = (room) => `<p class="tc-synthetic x-synthetic">${esc(room.synthetic_notice)} Data as of ${esc(room.as_of)}.</p>`;

  X.noRoom = (step, back) => {
    const T = window.TC;
    T.app.innerHTML = `${T.header(step, back)}<h2 class="co-title">${esc(X.company())}</h2>
      <div class="empty" role="status"><strong>No synthetic data room for this company yet.</strong>
      Ploy and Sazabi have one. Paste ploy.ai or sazabi.com above to see their room.</div>`;
  };

  // Marks
  const VERDICT = { looking_strong: ["strong", "looking strong"], looking_weak: ["weak", "looking weak"], mixed: ["mixed", "mixed"],
    not_enough_in_the_room: ["thin", "not enough in the room"] };
  X.verdictMark = (v, word) => `<span class="tc-mark tc-mark--${VERDICT[v][0]}">${word || VERDICT[v][1]}</span>`;
  X.claimMark = (c) => {
    if (c.severity === "flag") return '<span class="tc-mark tc-mark--weak">Red flag</span>';
    if (c.mark === "corroborated") return '<span class="tc-mark tc-mark--strong">Corroborated</span>';
    if (c.mark === "contradicted") return '<span class="tc-mark tc-mark--disagreement">Contradicted</span>';
    return "";
  };
  X.pieceOf = (room, name) => room.pieces.find((p) => p.name === name);

  // Chips. A room file opens its synthetic excerpt; an outside source opens the saved public page.
  X.roomChip = (s) => {
    if (s.public) {
      return X.pubChip(s.public, s.uri);
    }
    return `<button class="tc-chip roomchip" type="button" aria-expanded="false" data-r="${esc(JSON.stringify(s))}">${esc(s.uri)}, ${esc(s.locator)}</button>`;
  };
  // A chip for a saved public source, named for the source. app.js opens it.
  X.pubChip = (key, label) => {
    const pre = window.TC.S.research.pre[key];
    const data = esc(JSON.stringify({ q: pre.quote, e: pre.excerpt, url: pre.url || "" }));
    return `<button class="tc-chip srcchip" type="button" data-src="${esc(pre.source)}" data-claim="${data}" aria-expanded="false" title="${esc(window.TC.D.sources[pre.source].title)}">${esc(label)}</button>`;
  };
  X.roomPanel = (s) => `<span class="panel" role="note"><strong>${esc(s.uri)}</strong><br />
      <span class="note">${esc(s.locator)}</span>
      <pre><mark>${esc(s.quote)}</mark></pre></span>`;
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".roomchip");
    if (!b) return;
    const next = b.nextElementSibling;
    if (b.getAttribute("aria-expanded") === "true" && next && next.classList.contains("panel")) {
      next.remove(); b.setAttribute("aria-expanded", "false"); return;
    }
    b.insertAdjacentHTML("afterend", X.roomPanel(JSON.parse(b.dataset.r)));
    b.setAttribute("aria-expanded", "true");
  });
  X.chips = (sources, lead) => (sources && sources.length
    ? `<div class="tc-chips">${lead ? `<span class="x-chiplead">${esc(lead)}</span>` : ""}${sources.map(X.roomChip).join("")}</div>` : "");

  // A claim line: the sentence, its marks, then its sources on their own row.
  X.claimBody = (c) => `<div class="x-claim-head"><span class="claim-text">${esc(c.text)}</span>
      <span class="x-marks">${X.claimMark(c)}<span class="tc-mark">${esc(c.confidence)}</span></span></div>
      ${X.chips(c.sources)}${X.chips(c.agree, "Agrees")}${X.chips(c.disagree, "Disagrees")}`;

  // The range strip, from numbers. Labels near an edge turn inward.
  // One decimal when that is exact. Money takes two when one would change it ($5.25M, not $5.3M);
  // a percent or a month count takes two only when two are exact.
  const exact = (x, n) => Math.abs(Number(x.toFixed(n)) - x) < 1e-9;
  const dec = (x) => (exact(x, 1) || !exact(x, 2) ? x.toFixed(1) : x.toFixed(2));
  X.fmt = (v, unit) => {
    if (unit === "usd") return v >= 1e6 ? `$${(v / 1e6).toFixed(exact(v / 1e6, 1) ? 1 : 2)}M` : `$${Math.round(v).toLocaleString("en-US")}`;
    if (unit === "percent") return `${dec(v)}%`;
    if (unit === "months") return `${dec(v)} mo`;
    return Math.round(v).toLocaleString("en-US");
  };
  // The range strip draws a figure against a sourced normal range (Ken, 1:48 PM). A flag gets one only
  // when its strip carries a benchmark {label, source}; stated beside found alone never gets a strip.
  X.strip = (st, foundLabel) => {
    const pos = (v) => (v - st.min) / (st.max - st.min);
    const side = (v) => (pos(v) > 0.85 ? " is-right" : pos(v) < 0.15 ? " is-left" : "");
    const labels = st.ticks.map((t) => `<span class="tc-strip-label is-${t.pos === "above" ? "above" : "below"}${t.out ? " is-out" : ""}${side(t.v)}" style="--v:${t.v}">${esc(t.label)}</span>`).join("");
    const ticks = st.ticks.map((t) => `<span class="tc-strip-tick${t.out ? " is-out" : ""}" style="--v:${t.v}"></span>`).join("");
    const below = st.ticks.some((t) => t.pos !== "above" && Math.abs(pos(t.v) - pos(st.band)) < 0.2);
    const bandLabel = `<span class="tc-strip-label ${below ? "is-above" : "is-below"} is-band${side(st.band)}" style="--v:${st.band}">${esc(foundLabel)} ${esc(X.fmt(st.band, st.unit))}</span>`;
    const aria = `Range strip: found ${X.fmt(st.band, st.unit)}. ` + st.ticks.map((t) => `${t.label}${t.out ? ", outside the band" : ", inside the band"}`).join(". ");
    return `<div class="x-strip"><div class="tc-strip tc-strip--labelled" style="--min:${st.min};--max:${st.max}" role="img" aria-label="${esc(aria)}">
        ${labels}${bandLabel}
        <div class="tc-strip-track"><span class="tc-strip-band" style="--v:${st.band}"></span><span class="tc-strip-tick" style="--v:${st.band}"></span>${ticks}</div>
      </div>
      <div class="tc-strip-axis"><span>${esc(X.fmt(st.min, st.unit))}</span><span>${esc(X.fmt(st.max, st.unit))}</span></div></div>`;
  };

  X.pair = (a, b) => `<div class="tc-pair">
      <div><div class="tc-pair-key">${esc(a.key)}</div><div class="tc-pair-value${a.out ? " is-out" : ""}">${esc(a.value)}</div><div class="tc-pair-source">${X.roomChip(a.source)}</div></div>
      <div><div class="tc-pair-key">${esc(b.key)}</div><div class="tc-pair-value">${esc(b.value)}</div><div class="tc-pair-source">${X.roomChip(b.source)}</div></div>
    </div>`;

  // A flag card: stated beside found, both sources, the strip, and for a red flag the question for the founder.
  X.flagCard = (room, f, opts) => {
    const piece = X.pieceOf(room, f.piece);
    const others = f.others.length ? `<p class="x-others">${f.others.map((o) => `${esc(o.key)}: <span class="tc-mono">${esc(o.value)}</span> ${X.roomChip(o.source)}`).join(" ")}</p>` : "";
    const asked = X.st().asked[f.claim_id];
    const ask = f.ask && !(opts && opts.noAsk) ? `<div class="tc-ask"><span class="tc-label tc-label--ask">Ask the founder</span>
        <p class="tc-ask-question">${esc(f.ask)}</p>
        <div class="tc-ask-actions">${asked ? X.viewReq(`ask-${f.claim_id}`) : `<button class="tc-btn tc-btn--small" type="button" data-ask="${esc(f.claim_id)}">Add to the request</button>`}
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-copyask="${esc(f.ask)}">Copy the question</button></div></div>` : "";
    return `<article class="tc-card x-flag" data-flag="${esc(f.kind)}" id="flag-${esc(f.claim_id)}">
      <div class="tc-card-head"><span class="tc-mark tc-mark--${f.kind === "red" ? "weak" : "strong"}">${f.kind === "red" ? "Red flag" : "Green flag"}</span>
        <span class="x-flaghead-right"><span class="tc-meta">${esc(piece.label)}</span>${opts && opts.noPick ? "" : X.pick(`flag:${f.claim_id}`)}</span></div>
      <h3 class="tc-card-title">${esc(f.title)}</h3>
      ${f.why ? `<p class="x-why">${esc(f.why)}</p>` : ""}
      ${X.pair(f.stated, f.found)}${others}
      ${f.strip && f.strip.benchmark ? X.strip(f.strip, f.strip.benchmark.label) : ""}
      ${ask}</article>`;
  };

  // A card titled "<piece>: <text>" shows the piece as its title and the text as a subtitle (Ken, 1:25 PM).
  X.subtitle = (t) => { const i = t.indexOf(": "); const rest = i < 0 ? t : t.slice(i + 2); return rest[0].toUpperCase() + rest.slice(1); };

  // "In memo" toggles (memo_picks.js). Keys: flag:<claim id> and insight:<n> are in by default; claim:<n> (a first-readout
  // evidence row, numbered as app.js numbers it) and room:<claim id> (the room's own evidence) are out by default.
  X.pick = (key) => (window.TC_MEMO ? window.TC_MEMO.toggleHtml(key) : "");
  X.picked = (key) => (window.TC_MEMO ? window.TC_MEMO.get(key) : /^(flag|insight):/.test(key));
  // The first readout's evidence rows in app.js's order: founders, comps, market signals, the outside world.
  X.researchNumbered = () => {
    const R = window.TC.S.research;
    if (!R) return [];
    const order = ["The founders", "Comps", "Market signals", "The outside world"];
    const rank = (s) => { const i = order.indexOf(s.title); return i < 0 ? 99 : i; };
    return [...R.sections].sort((a, b) => rank(a) - rank(b))
      .flatMap((s) => (s.parts ? s.parts.flatMap((p) => p.claims) : s.cards ? s.cards.flatMap((c) => c.claims) : s.claims))
      .filter((c) => !c.placeholder);
  };

  // Flag weight. Rule (Ken, 1:22 PM): two sources that agree make a small green flag; two that disagree make a big red flag.
  X.weight = (f) => (f.kind === "red" || f.basis === "disagreement" ? "big" : f.basis === "agreement" ? "small" : "headline");
  // Headline green flags (real strengths) first, then big red flags worst first, then small green flags.
  X.orderFlags = (flags) => [
    ...flags.filter((f) => X.weight(f) === "headline"),
    ...flags.filter((f) => X.weight(f) === "big").sort((a, b) => (b.relative_gap || 0) - (a.relative_gap || 0)),
    ...flags.filter((f) => X.weight(f) === "small"),
  ];
  X.smallFlag = (room, f, opts) => `<li class="x-smallflag" data-flag="small-green"><span class="tc-mark tc-mark--strong">Small green flag</span>
      <span class="x-small-title">${esc(f.title)}</span> <span class="tc-meta">${esc(X.pieceOf(room, f.piece).label)}</span>${opts && opts.noPick ? "" : X.pick(`flag:${f.claim_id}`)}
      <div class="tc-chips">${X.roomChip(f.stated.source)}${X.roomChip(f.found.source)}</div></li>`;
  X.flagsHtml = (room, flags, opts) => {
    const ordered = X.orderFlags(flags);
    const big = ordered.filter((f) => X.weight(f) !== "small");
    const small = ordered.filter((f) => X.weight(f) === "small");
    return `<div class="x-flags">${big.map((f) => X.flagCard(room, f, opts)).join("")}</div>
      ${small.length ? `<h3 class="x-sub">Small green flags: sources that agree</h3><ul class="x-smallflags">${small.map((f) => X.smallFlag(room, f, opts)).join("")}</ul>` : ""}`;
  };

  // "View in the request" opens the request over the page at that item (app.js), or the request screen.
  X.viewReq = (key) => `<button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-viewreq="${esc(key)}">View in the request</button>`;
  document.addEventListener("click", (e) => {
    const v = e.target.closest("[data-viewreq]");
    if (!v) return;
    if (typeof window.TC_OPEN_REQUEST === "function") window.TC_OPEN_REQUEST(v.dataset.viewreq);
    else location.hash = "#request";
  });

  // "Add to the request" puts the founder question on the request list as an item of its own.
  X.addAsk = (room, cid) => {
    const T = window.TC;
    const f = [...room.top_flags.red, ...room.top_flags.green, ...(room.extra_flags || [])].find((x) => x.claim_id === cid);
    if (!f) return;
    if (!T.S.items) T.buildItems();
    const it = { key: `ask-${cid}`, id: null, title: `Question: ${X.pieceOf(room, f.piece).label}`, ask: f.ask, includes: null, guide: null, guidance: null,
      fromReadout: false, firstTier: false, custom: true, reasons: [f.title], checked: true };
    if (!T.S.items.some((x) => x.key === it.key)) T.S.items.push(it);
    X.st().asked[cid] = true;
  };
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-ask]");
    if (a) {
      X.addAsk(X.room(), a.dataset.ask);
      a.outerHTML = X.viewReq(`ask-${a.dataset.ask}`);
      return;
    }
    const c = e.target.closest("[data-copyask]");
    if (c) {
      const done = (ok) => { c.textContent = ok ? "Copied" : "Copy did not work here"; };
      (navigator.clipboard ? navigator.clipboard.writeText(c.dataset.copyask) : Promise.reject()).then(() => done(true), () => done(false));
    }
  });

  // In-page jumps scroll; a hash link would change the step.
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-scroll]");
    if (!b) return;
    const el = document.getElementById(b.dataset.scroll);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  X.counts = (p) => `${p.agree} source${p.agree === 1 ? " agrees" : "s agree"} · ${p.disagree} disagree${p.disagree === 1 ? "s" : ""}`;

  // The overview row for a piece.
  X.verdictRow = (p, extra) => `<div class="tc-verdict" data-piece="${esc(p.name)}"><b>${esc(p.label)}</b><span>${X.verdictMark(p.verdict, p.word)}</span>
      <div class="tc-verdict-why">${esc(p.reason)}<span class="tc-verdict-count">${X.counts(p)}</span>${extra || ""}</div></div>`;

  X.table = (panel) => `<div class="tc-table-wrap"><table class="tc-table tc-table--stack"><caption class="x-caption">${esc(panel.name)}</caption>
      <thead><tr>${panel.columns.map((c, i) => `<th${i > 0 ? ' class="tc-fig"' : ""}>${esc(c)}</th>`).join("")}</tr></thead>
      <tbody>${panel.rows.map((r) => `<tr>${r.map((v, i) => `<td${i > 0 ? ' class="tc-fig"' : ""} data-label="${esc(panel.columns[i])}">${esc(v)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
})();
