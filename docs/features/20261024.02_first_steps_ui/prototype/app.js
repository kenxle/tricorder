// Tricorder first-steps prototype: company URL -> first readout -> data-room request -> room received.
// Data comes from data.js (window.DATA), written by build_data.py from the saved research files.
// No network: every source chip opens a readable copy under sources/.
(function () {
  "use strict";
  const D = window.DATA;
  const app = document.getElementById("app");
  const params = new URLSearchParams(location.search);
  const PACE = params.has("pace") ? Number(params.get("pace")) : 1; // 0 shows everything at once (for checks)
  const STAGES = { pre_seed: "Pre-seed", seed: "Seed", series_a: "Series A" };
  const STEPS = [["start", "Company URL"], ["readout", "First readout"], ["request", "Data-room request"], ["received", "Room received"],
    ["flags", "Flags from the room"], ["steer", "Steer the readout"], ["memo", "Make the memo"], ["principal", "The principal's view"]]; // steps 5 to 8: step5.js, step6.js, memo.js

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const hostOf = (u) => {
    try { return new URL(/^[a-z]+:\/\//i.test(u) ? u : "https://" + u).hostname.toLowerCase().replace(/^www\./, ""); } catch (e) { return ""; }
  };
  const lcfirst = (s) => (s.length > 1 && s[1] === s[1].toUpperCase() && /[A-Z]/.test(s[1]) ? s : s[0].toLowerCase() + s.slice(1));

  // State --------------------------------------------------------------------------------
  const S = {
    url: "", company: null, research: null, fields: null, streamed: false, run: 0,
    items: null, itemsStage: null, added: 0,
    to: "", by: "", sender: "", fund: "", subject: "", body: "", autoBody: "", edited: false,
  };
  try { S.sender = localStorage.getItem("tricorder.proto.sender") || ""; S.fund = localStorage.getItem("tricorder.proto.fund") || ""; } catch (e) { /* no storage */ }

  // Resolve a URL against the saved YC list ------------------------------------------------
  function resolve(input) {
    const raw = input.trim();
    const host = hostOf(raw);
    let company = null;
    let how = "";
    const yc = raw.match(/ycombinator\.com\/companies\/([a-z0-9-]+)/i);
    if (yc) {
      company = D.companies.find((c) => c.slug === yc[1].toLowerCase()) || null;
      how = company ? `YC slug "${yc[1]}"` : "";
    } else if (host) {
      company = D.companies.find((c) => c.host === host || host.endsWith("." + c.host)) || null;
      how = company ? `domain ${host}` : "";
    }
    return { input: raw, host, company, how };
  }

  function setupFor(r) {
    const c = r.company;
    const research = c ? D.research[c.slug] || null : null;
    if (research) {
      const f = JSON.parse(JSON.stringify(research.setup));
      return { research, fields: f };
    }
    const list = D.list_source;
    const yf = c ? D.yc_founders[c.slug] : null;
    const f = c ? {
      name: { value: c.name, source: list },
      website: { value: c.website, source: list },
      founders: yf ? { value: yf.map((x) => x.name).join(", "), source: yf[0].source } : { value: "", note: "Not in the saved files" },
      batch: { value: c.batch, source: list },
      stage: { value: "seed", note: "Not found. Set by the associate" },
      location: { value: (c.regions || [])[0] || "", source: list },
      team_size: { value: String(c.team_size), source: list },
    } : {
      name: { value: "", note: "Not in the saved YC Spring 2026 list" },
      website: { value: r.input, note: "From the URL you gave" },
      founders: { value: "", note: "Not found" },
      batch: { value: "", note: "Not found" },
      stage: { value: "seed", note: "Not found. Set by the associate" },
      location: { value: "", note: "Not found" },
      team_size: { value: "", note: "Not found" },
    };
    return { research: null, fields: f };
  }

  function startCompany(input) {
    const r = resolve(input);
    const s = setupFor(r);
    Object.assign(S, { url: r.input, company: r.company, how: r.how, research: s.research, fields: s.fields, streamed: false,
      items: null, itemsStage: null, edited: false, requests: null, roomShared: false, roomOpened: false, roomPartial: false, roomMore: false, roomFull: false });
    clearTimeout(S.arrivalTimer); clearTimeout(S.moreTimer);
    const q = new URLSearchParams(location.search);
    q.set("company", r.input);
    history.replaceState(null, "", "?" + q.toString() + "#readout");
    render();
  }

  // Routing --------------------------------------------------------------------------------
  function route() { return (location.hash || "#start").slice(1); }
  function go(step) { location.hash = step; }
  window.addEventListener("hashchange", render);

  function stepsNav(cur) {
    return `<ol class="steps" aria-label="Steps">${STEPS.map(([k, t], i) =>
      `<li${k === cur ? ' aria-current="step"' : ""}>${i + 1}. ${esc(t)}</li>`).join("")}</ol>`;
  }
  // The product's own bar, no prototype chrome (Ken, 1:00 PM: "make this like a real mock as though we're actually using the product").
  function header(cur) {
    const go = cur === "start" ? "" : `<form class="appbar-go" data-appbar-go><input class="tc-input" type="text" placeholder="Paste a company URL" aria-label="Company URL" /></form>`;
    return `<header class="masthead appbar"><a class="tc-brand" href="#start">Tricorder</a>${go}</header>`;
  }
  app.addEventListener("submit", (e) => {
    const f = e.target.closest("[data-appbar-go]");
    if (!f) return;
    e.preventDefault();
    const v = f.querySelector("input").value.trim();
    if (v) startCompany(v);
  });

  app.addEventListener("click", (e) => {
    if (e.target.closest("#to-request")) openRequest();
    if (e.target.closest("#open-room")) openRoom();
    if (e.target.closest("#open-more")) openMore();
  });

  function render() {
    S.run++; // stops any arrival that is still playing
    const r = route();
    if (r !== "start" && !S.fields) return renderStart();
    const dlg = document.getElementById("req-modal");
    if (dlg && dlg.open) dlg.close();
    if (r === "readout") return S.roomOpened && window.TC_ROOM_VIEW ? showRoomView() : renderReadout();
    if (r === "request") { renderReadout(); return openRequest(); }
    if (r === "received") { if (S.requests && roomOf()) { if (!S.roomOpened) openRoom(); else showRoomView(); return; } return renderReadout(); }
    if (window.TC_STEPS && window.TC_STEPS[r]) return window.TC_STEPS[r]();
    return renderStart();
  }

  // Step 1: the URL -------------------------------------------------------------------------
  function renderStart() {
    const tries = ["https://www.sazabi.com/", "https://ploy.ai", "https://www.ycombinator.com/companies/ploy", "https://tester.army"];
    app.innerHTML = `${header("start")}
      <section class="start" aria-label="Start from a company URL">
        <h2>Diligence on whom?</h2>
        <p>Paste the company's website or its YC company page. Tricorder sets the company up and starts the research.</p>
        <form id="urlform">
          <input type="url" id="url" name="url" required class="tc-input" placeholder="https://www.sazabi.com/" aria-label="Company URL" value="${esc(S.url)}" />
          <button class="tc-btn primary" type="submit">Start</button>
        </form>
      </section>`;
    const form = document.getElementById("urlform");
    form.addEventListener("submit", (e) => { e.preventDefault(); startCompany(document.getElementById("url").value); });
    app.querySelectorAll("[data-try]").forEach((b) => b.addEventListener("click", () => startCompany(b.dataset.try)));
    document.getElementById("url").setAttribute("type", "text"); // accept a bare domain too
  }

  // Source chips -----------------------------------------------------------------------------
  let chipN = 0;
  function chip(sid, claimObj) {
    if (!sid || !D.sources[sid]) return "";
    chipN++;
    const src = D.sources[sid];
    const data = claimObj ? ` data-claim='${esc(JSON.stringify({ q: claimObj.quote, e: claimObj.excerpt, url: claimObj.url || "" }))}'` : "";
    return `<button class="tc-chip srcchip" type="button" data-src="${esc(sid)}"${data} aria-expanded="false" title="${esc(src.title)}">source</button>`;
  }
  function sourcePanel(sid, c) {
    const s = D.sources[sid];
    const url = (c && c.url) || s.url;
    return `<span class="panel" role="note">
      <strong>${esc(s.title)}</strong><br />
      <span class="note">Saved copy: <code>${esc(s.path)}</code></span><br />
      ${url ? `<span class="note">Original: <a href="${esc(url)}" target="_blank" rel="noopener">${esc(url)}</a></span><br />` : `<span class="note">Original: written by Tricorder's research, no outside URL.</span><br />`}
      ${c && c.e ? `<pre>…${esc(c.e.before)}<mark>${esc(c.e.match)}</mark>${esc(c.e.after)}…</pre>` : ""}
      <a href="${esc(s.copy)}" target="_blank" rel="noopener">Open the saved copy</a>
      ${s.kind === "readable copy" ? `<span class="note"> (a readable copy made from the saved file)</span>` : ""}
    </span>`;
  }
  // Hovering an evidence number shows the fact and its source (Ken, 12:58 PM).
  let tip = null;
  function hideTip() { if (tip) { tip.remove(); tip = null; } }
  function showTip(a) {
    hideTip();
    const row = document.getElementById(a.getAttribute("href").slice(1));
    if (!row) return;
    const text = row.querySelector(".claim-text").textContent.replace(/^\s*\d+\s*/, "").trim();
    const chipEl = row.querySelector(".srcchip");
    const s = chipEl ? D.sources[chipEl.dataset.src] : null;
    tip = document.createElement("div");
    tip.className = "ev-tip";
    tip.setAttribute("role", "tooltip");
    tip.innerHTML = `<span class="ev-tip-n">${esc(a.textContent)}</span> ${esc(text)}${s ? `<span class="ev-tip-src">Source: ${esc(s.title)}</span>` : ""}`;
    document.body.appendChild(tip);
    const r = a.getBoundingClientRect();
    const w = Math.min(380, window.innerWidth - 32);
    tip.style.width = w + "px";
    tip.style.left = Math.max(16, Math.min(window.scrollX + r.left, window.scrollX + window.innerWidth - w - 16)) + "px";
    tip.style.top = (window.scrollY + r.bottom + 8) + "px";
  }
  app.addEventListener("mouseover", (e) => { const a = e.target.closest(".ev-ref"); if (a) showTip(a); });
  app.addEventListener("mouseout", (e) => { if (e.target.closest(".ev-ref")) hideTip(); });
  app.addEventListener("focusin", (e) => { const a = e.target.closest(".ev-ref"); if (a) showTip(a); });
  app.addEventListener("focusout", (e) => { if (e.target.closest(".ev-ref")) hideTip(); });

  app.addEventListener("click", (e) => {
    const b = e.target.closest(".srcchip");
    if (!b) return;
    const open = b.getAttribute("aria-expanded") === "true";
    const row = b.closest("tr");
    const next = row ? row.nextElementSibling : b.nextElementSibling;
    if (open && next && next.classList.contains("panel")) { next.remove(); b.setAttribute("aria-expanded", "false"); return; }
    const c = b.dataset.claim ? JSON.parse(b.dataset.claim) : null;
    if (row) row.insertAdjacentHTML("afterend", `<tr class="panel"><td colspan="2">${sourcePanel(b.dataset.src, c)}</td></tr>`);
    else b.insertAdjacentHTML("afterend", sourcePanel(b.dataset.src, c));
    b.setAttribute("aria-expanded", "true");
  });

  const KIND = {
    "company says": '<span class="tc-mark says">The company says</span>',
    "no signal": '<span class="tc-mark nosignal">No signal</span>',
    match: '<span class="tc-mark tc-mark--strong match">Matches</span>',
    differs: '<span class="tc-mark tc-mark--weak warn">Differs</span>',
    unconfirmed: '<span class="tc-mark tc-mark--thin warn">Not confirmed</span>',
  };
  function claimLi(c) {
    if (c.placeholder) {
      return `<tr class="claim ph wait"><td class="claim-text">${esc(c.text)}</td><td class="claim-src"><span class="tc-mark ph" title="Not researched yet">Placeholder</span></td></tr>`;
    }
    return `<tr class="claim wait" id="ev-${c._n}"><td class="claim-text"><span class="ev-n">${c._n}</span> ${esc(c.text)} ${KIND[c.kind] || ""}</td><td class="claim-src">${chip(c.source, c)}${window.TC_MEMO ? ` ${window.TC_MEMO.toggleHtml("claim:" + c._n)}` : ""}</td></tr>`;
  }
  const MARKS = { strong: ["tc-mark--strong", "Looking strong"], weak: ["tc-mark--weak", "Looking weak"], mixed: ["tc-mark--mixed", "Mixed"], thin: ["tc-mark--thin", "Not enough yet"] };
  function allClaims(R) {
    return R.sections.flatMap((s) => s.parts ? s.parts.flatMap((p) => p.claims) : s.cards ? s.cards.flatMap((c) => c.claims) : s.claims);
  }
  function numberClaims(R) {
    let n = 0;
    allClaims(R).forEach((c) => { if (!c.placeholder) c._n = ++n; });
  }
  // Ken, 12:55 PM: what the company does, then the founders, then comps, then market signals.
  const SECTION_ORDER = ["The founders", "Comps", "Market signals", "The outside world"];
  function orderedResearch(R) {
    if (!R) return R;
    const rank = (s) => { const i = SECTION_ORDER.indexOf(s.title); return i < 0 ? 99 : i; };
    return { ...R, sections: [...R.sections].sort((a, b) => rank(a) - rank(b)) };
  }
  function refNums(R, refs) {
    const claims = allClaims(R).filter((c) => !c.placeholder);
    return [...new Set(refs.map((r) => (claims.find((c) => c.text.includes(r)) || {})._n).filter(Boolean))];
  }
  function aboutHtml(R) {
    const a = (window.TC_ABOUT || {})[R.slug];
    if (!a) return "";
    return `<p class="about">${esc(a.text)} <span class="based">${refNums(R, a.refs).map((n) => `<a class="ev-ref" href="#ev-${n}">${n}</a>`).join(" ")}</span></p>`;
  }
  function insightsHtml(R) {
    const list = (window.TC_INSIGHTS || {})[R.slug] || [];
    if (!list.length) return "";
    const claims = allClaims(R).filter((c) => !c.placeholder);
    const cards = list.map((ins, idx) => {
      const nums = [...new Set(ins.refs.map((r) => (claims.find((c) => c.text.includes(r)) || {})._n).filter(Boolean))];
      const [cls, label] = MARKS[ins.mark] || MARKS.thin;
      return `<article class="tc-card insight wait"><div class="tc-card-head"><span class="tc-mark ${cls}">${label}</span><span class="piece">${esc(ins.piece)}</span></div>
        <h3>${esc(ins.title)}</h3><p>${esc(ins.text)}</p>
        <p class="based"><span>Based on ${nums.map((n) => `<a class="ev-ref" href="#ev-${n}">${n}</a>`).join(" ")}</span>${window.TC_MEMO ? window.TC_MEMO.toggleHtml("insight:" + idx) : ""}</p></article>`;
    }).join("");
    return `<section class="insights" aria-label="What stands out"><h2>What stands out</h2><div class="insight-grid">${cards}</div></section>`;
  }
  function claimsTable(claims) {
    return `<table class="tc-table claims"><thead><tr><th scope="col">What we found</th><th scope="col">Source</th></tr></thead><tbody>${claims.map(claimLi).join("")}</tbody></table>`;
  }
  function gapsList(gaps) {
    if (!gaps || !gaps.length) return "";
    return `<ul class="gaps tc-gap-list">${gaps.map((g) => `<li class="wait"><strong>Gap:</strong> ${esc(g.text)} <span class="why">${esc(g.why)}</span></li>`).join("")}</ul>`;
  }

  // Step 2: the first readout ------------------------------------------------------------------
  const FIELD_LABELS = [["name", "Name"], ["website", "Website"], ["founders", "Founders"], ["stage", "Stage"], ["location", "Location"], ["team_size", "Team size"]];
  function setupPanel() {
    const f = S.fields;
    const cells = FIELD_LABELS.map(([k, label]) => {
      const v = f[k];
      const input = k === "stage"
        ? `<select class="tc-input" id="f-${k}" data-field="${k}">${Object.entries(STAGES).map(([sk, st]) => `<option value="${sk}"${v.value === sk ? " selected" : ""}>${st}</option>`).join("")}</select>`
        : `<input class="tc-input" type="text" id="f-${k}" data-field="${k}" value="${esc(v.value)}" />`;
      const src = v.source ? chip(v.source) : esc(v.note || "");
      return `<div class="field"><label class="tc-label" for="f-${k}">${label}</label>${input}<div class="src">${src}${v.edited ? ' <span class="tc-mark warn">Corrected by you</span>' : ""}</div></div>`;
    }).join("");
    const unknown = S.company ? "" : `<p class="note">This URL is not in the saved YC Spring 2026 list.</p>`;
    return `<section class="setup" aria-label="The company">
      ${unknown}
      <div class="fields">${cells}</div></section>`;
  }
  function bindSetup() {
    app.querySelectorAll("[data-field]").forEach((el) => {
      el.addEventListener("input", () => {
        const k = el.dataset.field;
        S.fields[k].value = el.value;
        S.fields[k].edited = true;
        const src = el.parentElement.querySelector(".src");
        if (src && !src.querySelector(".warn")) src.insertAdjacentHTML("beforeend", ' <span class="tc-mark warn">Corrected by you</span>');
        if (k === "name") { const t = document.getElementById("co-name"); if (t) t.textContent = el.value || "This company"; }
      });
    });
  }

  function sectionHtml(s, i) {
    let inner = "";
    if (s.parts) {
      inner = s.parts.map((p) => `<div class="part wait"><h3>${esc(p.label)}</h3>${p.claims.length
        ? claimsTable(p.claims) : `<p class="note wait">Nothing found.</p>`}</div>`).join("");
    } else if (s.cards) {
      inner = `<div class="cards">${s.cards.map((c) => `<article class="card wait"><h3>${esc(c.name)}</h3><div class="role">${esc(c.role)}</div>
        <div class="links">${c.x ? `X: <a href="${esc(c.x)}" target="_blank" rel="noopener">linked, not read</a>` : ""}${c.github ? ` · <a href="${esc(c.github)}" target="_blank" rel="noopener">GitHub</a>` : ""}</div>
        ${claimsTable(c.claims)}</article>`).join("")}</div>`;
    } else {
      inner = claimsTable(s.claims);
    }
    return `<section class="section wait" data-sec="${i}" aria-label="${esc(s.title)}">
      <h2>${esc(s.title)} <span class="status" data-status>Waiting</span></h2>${inner}${gapsList(s.gaps)}</section>`;
  }

  function countOf(s) {
    const all = s.parts ? s.parts.flatMap((p) => p.claims) : s.cards ? s.cards.flatMap((c) => c.claims) : s.claims;
    const sourced = all.filter((c) => !c.placeholder).length;
    return `${sourced} sourced claim${sourced === 1 ? "" : "s"}` + ((s.gaps || []).length ? `, ${s.gaps.length} gap${s.gaps.length === 1 ? "" : "s"}` : "");
  }

  function renderReadout() {
    chipN = 0;
    const R = orderedResearch(S.research);
    const name = S.fields.name.value || "This company";
    let body;
    if (!R) {
      body = `<div class="empty" role="status"><strong>Research not cached for this company.</strong>
        Tricorder has saved research for Ploy and Sazabi only. Research for other companies is not set up yet.
        You can still draft the data-room request from the stage's first-tier documents.</div>
        <div class="actions"><button class="tc-btn primary" id="to-request" type="button">Draft the data-room request</button></div>`;
    } else {
      numberClaims(R);
      body = `<p class="tc-sr-only" id="overall" role="status"></p>
        ${insightsHtml(R)}
        ${R.sections.map(sectionHtml).join("")}
        <section class="roomgaps wait" id="roomgaps" aria-label="Up Next: Data Room Requests">
          ${S.requests ? requestsInner() : `<h2>Up Next: Data Room Requests</h2>
          <p class="note">These become the first items on the data-room request.</p>
          <ul class="gaps tc-gap-list">${R.room_gaps.map((g) => `<li class="wait"><strong>${esc(g.text)}</strong> <span class="why">${esc(g.why)}</span></li>`).join("")}</ul>
          <div class="actions"><button class="tc-btn primary" id="to-request" type="button">Draft the data-room request</button></div>`}
        </section>`;
    }
    app.innerHTML = `${header("readout", ["start", "the company URL"])}
      <div id="notify" aria-live="polite">${notifyHtml()}</div>
      <h2 id="co-name" class="co-title">${esc(name)}</h2>
      ${R ? aboutHtml(R) : setupPanel()}

      ${body}`;
    bindSetup();
    if (R) {
      arrive(R);
    }
  }

  // Each section shows a skeleton until its data arrives, then fills in whole (Ken, 1:00 PM).
  function arrive(R) {
    const run = ++S.run;
    const overall = document.getElementById("overall");
    app.querySelectorAll(".wait").forEach((el) => el.classList.remove("wait"));
    const blocks = [...app.querySelectorAll(".insights, .section, #roomgaps")];
    const done = () => { overall.textContent = `Research done: ${R.sections.length} sections.`; S.streamed = true; };
    app.querySelectorAll(".section").forEach((b) => { const st = b.querySelector("[data-status]"); if (st) st.textContent = `Done: ${countOf(R.sections[Number(b.dataset.sec)])}`; });
    if (S.streamed || PACE === 0) return done();
    const skel = '<div class="skel" aria-hidden="true"><span></span><span></span><span></span></div>';
    blocks.forEach((b) => { b.classList.add("loading"); b.insertAdjacentHTML("beforeend", skel); });
    overall.textContent = "Researching";
    // Order data lands in: the sections, then the insights read from them, then what only a room can answer.
    const order = [...app.querySelectorAll(".section"), app.querySelector(".insights"), document.getElementById("roomgaps")].filter(Boolean);
    order.forEach((b, i) => setTimeout(() => {
      if (run !== S.run) return;
      b.classList.remove("loading");
      const s = b.querySelector(":scope > .skel"); if (s) s.remove();
      if (i === order.length - 1) done();
    }, (500 + i * 650) * PACE));
  }

  // Step 3: the data-room request ---------------------------------------------------------------
  const byId = Object.fromEntries(D.checklist.map((c) => [c.id, c]));
  function buildItems() {
    const stage = S.fields.stage.value;
    const early = stage === "pre_seed" || stage === "seed";
    const items = [];
    const find = (id) => items.find((x) => x.id === id);
    for (const g of (S.research ? S.research.room_gaps : [])) {
      for (const id of g.ids) {
        const c = byId[id];
        if (!c) continue;
        const have = find(id);
        if (have) { have.reasons.push(g.text); continue; }
        items.push({ key: id, id, title: c.title, item: c.item, ask: c.ask, includes: c.includes, guide: c.guide, guidance: c.guidance,
          fromReadout: true, firstTier: false, reasons: [g.text], checked: true });
      }
    }
    for (const c of D.checklist) {
      if (c.kind !== "document" || c.stages[stage] !== "yes" || (early && c.closing_at_early_stage)) continue;
      const have = find(c.id);
      if (have) { have.firstTier = true; continue; }
      items.push({ key: c.id, id: c.id, title: c.title, item: c.item, ask: c.ask, includes: c.includes, guide: c.guide, guidance: c.guidance,
        fromReadout: false, firstTier: true, reasons: [], checked: true });
    }
    items.forEach((it) => { if (it.fromReadout && byId[it.id].stages[stage] === "yes") it.firstTier = true; });
    S.items = items;
    S.itemsStage = stage;
  }

  function whenText(iso) {
    const d = new Date(iso + "T12:00:00");
    if (isNaN(d)) return iso;
    return `${d.toLocaleDateString("en-US", { weekday: "long" })} ${d.getDate()} ${d.toLocaleDateString("en-US", { month: "long" })}`;
  }
  function defaultBy() {
    const d = new Date();
    d.setDate(d.getDate() + 7);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  }

  function draftText() {
    const company = S.fields.name.value || "your company";
    const first = (S.fields.founders.value || "").split(",")[0].trim().split(/\s+/)[0] || "";
    const chosen = S.items.filter((i) => i.checked);
    const lines = [first ? `Hi ${first},` : "Hello,", "",
      `Thanks for talking with us about ${company}. Before our next meeting, could you set up a data room with the ${chosen.length === 1 ? "item" : "items"} below by ${whenText(S.by)}? A rough version is fine, and if something does not exist yet, just say so.`, ""];
    const seen = new Set();
    chosen.forEach((it, n) => {
      lines.push(`${n + 1}. ${it.ask}`);
      if (it.includes && !seen.has(it.guide)) { lines.push(`   Ideally it includes ${it.includes}.`); seen.add(it.guide); }
    });
    lines.push("", "Thanks,");
    if (S.sender) lines.push(S.sender);
    if (S.fund) lines.push(S.fund);
    return { subject: `${company}: a few things for a data room`, body: lines.join("\n") + "\n" };
  }

  const isQuestion = (it) => String(it.key).startsWith("ask-");
  function itemLi(it) {
    const g = it.guidance;
    const tags = [
      it.fromReadout ? '<span class="tc-mark warn">From the readout</span>' : "",
      it.firstTier ? `<span class="tc-mark">First tier at ${esc(STAGES[S.itemsStage])}</span>` : "",
      it.custom && !isQuestion(it) ? '<span class="tc-mark">Added by you</span>' : "",
      isQuestion(it) ? '<span class="tc-mark warn">From the room</span>' : "",
    ].join("");
    return `<li class="ask" data-key="${esc(it.key)}">
      <label class="hit"><input class="tc-check" type="checkbox" data-item="${esc(it.key)}" aria-label="Ask for ${esc(it.title)}"${it.checked ? " checked" : ""} /></label>
      <div>
        <div class="title">${esc(it.title)}</div>
        <div>${esc(it.ask)}</div>
        <div class="meta">${tags}</div>
        ${it.reasons.length ? `<div class="why">For you, not sent: ${it.reasons.map(esc).join(" ")}</div>` : ""}
        ${g ? `<details><summary>Guidance for this document</summary>
          <div><strong>What it is.</strong> ${esc(g.what)}</div>
          <div><strong>Best form.</strong> ${esc(g.form)}</div>
          <div><strong>A good one shows:</strong></div><ul>${g.good.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
          <div class="note">From <code>${esc(g.path)}</code></div></details>`
          : `<div class="why">No document guide for this item.</div>`}
      </div></li>`;
  }

  // The data-room request is a dialog over the associate's working page (Ken, 1:03 PM).
  function openRequest(itemId) {
    if (!S.fields) return;
    if (!S.items || S.itemsStage !== S.fields.stage.value) buildItems();
    if (!S.by) S.by = defaultBy();
    const company = S.fields.name.value || "This company";
    const fromReadout = S.items.filter((i) => i.fromReadout).length;
    let dlg = document.getElementById("req-modal");
    if (!dlg) {
      dlg = document.createElement("dialog");
      dlg.id = "req-modal";
      dlg.setAttribute("aria-labelledby", "req-title");
      document.body.appendChild(dlg);
      dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    }
    dlg.innerHTML = `<div class="modal-head"><h2 id="req-title">${esc(company)}: the data-room request</h2>
        <button class="tc-btn tc-btn--secondary" type="button" id="req-close">Close</button></div>
      <div class="modal-body">
      <p class="banner tc-synthetic" role="note">For the demo, the data room that comes back is synthetic. The team writes it. It is not ${esc(company)}'s data.</p>
      <p class="note">The readout's gaps come first (${fromReadout}), then the standard first-tier documents for a ${esc(STAGES[S.itemsStage].toLowerCase())} company. Uncheck, check or add items. The draft updates as you go. Tricorder never sends it.</p>
      <div class="toolbar">
        <span class="note">Select:</span>
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-pick="all">All</button>
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-pick="none">None</button>
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-pick="readout">Only from the readout</button>
        <span class="note push" id="count"></span>
      </div>
      <div class="layout">
        <div>
          <ul class="asks" id="asks">${askList()}</ul>
          <form class="addrow" id="addform"><input class="tc-input" type="text" id="addtext" placeholder="Add an item, for example: your SOC 2 report" aria-label="Add an item" />
            <button class="tc-btn tc-btn--secondary" type="submit">Add</button></form>
        </div>
        <div class="side">
          <aside class="drawer" aria-label="Draft to the founder">
            <h3>Draft to the founder</h3>
            <p class="drawer-note">Tricorder never sends this. Copy it, or open it in your own mail app and send it from there.</p>
            <label for="d-to">To</label><input class="tc-input" id="d-to" type="email" placeholder="founder's email" value="${esc(S.to)}" />
            <div class="row">
              <div><label for="d-by">Ask for it by</label><input class="tc-input" id="d-by" type="date" value="${esc(S.by)}" /></div>
              <div><label for="d-sender">Your name</label><input class="tc-input" id="d-sender" type="text" value="${esc(S.sender)}" /></div>
              <div><label for="d-fund">Fund</label><input class="tc-input" id="d-fund" type="text" value="${esc(S.fund)}" /></div>
            </div>
            <p class="note" id="redo" hidden><button class="tc-btn tc-btn--secondary tc-btn--small" type="button" id="redo-btn">Redo the draft with these</button> This replaces your edits to the message.</p>
            <label for="d-subject">Subject</label><input class="tc-input" id="d-subject" type="text" />
            <label for="d-body">Message (edit freely)</label><textarea class="tc-input" id="d-body"></textarea>
            <div class="actions drawer-actions">
              <button class="tc-btn primary" type="button" id="copy">Copy text</button>
              <a class="btn tc-btn tc-btn--secondary" id="mailto" href="#">Open in mail app</a>
              <span class="ok" id="copied" role="status"></span>
            </div>
          </aside>
        </div>
      </div></div>
      <div class="modal-foot"><span class="note">Send it from your own mail, then mark it sent.</span>
        <button class="tc-btn primary" type="button" id="mark-sent">Mark as sent</button></div>`;
    bindRequest(dlg);
    if (S.edited) { document.getElementById("d-subject").value = S.subject; document.getElementById("d-body").value = S.body; }
    refreshDraft(false);
    if (!dlg.open) dlg.showModal();
    if (itemId) focusItem(dlg, itemId);
  }

  // The list: the checklist and your own additions, then "Questions for the founder" that flag cards added.
  const QHEAD = '<li class="ask-group" id="ask-group"><h3>Questions for the founder</h3><p class="note">Added from the flags in the data room.</p></li>';
  function askList() {
    const qs = S.items.filter(isQuestion);
    return S.items.filter((i) => !isQuestion(i)).map(itemLi).join("") + (qs.length ? QHEAD + qs.map(itemLi).join("") : "");
  }
  function focusItem(dlg, id) {
    let it = S.items.find((x) => x.key === id || x.key === `ask-${id}` || x.id === id);
    if (!it && window.TCX && roomOf()) { window.TCX.addAsk(roomOf(), id); it = S.items.find((x) => x.key === `ask-${id}`); if (it) { dlg.querySelector("#asks").innerHTML = askList(); refreshDraft(); } }
    const li = it && [...dlg.querySelectorAll("#asks li.ask")].find((x) => x.dataset.key === it.key);
    if (!li) return;
    li.scrollIntoView({ block: "center" });
    li.classList.add("flash");
    setTimeout(() => li.classList.remove("flash"), 2200);
  }
  window.TC_OPEN_REQUEST = (itemId) => openRequest(itemId);

  // Questions added from a card land in the Data room requests box straight away.
  function refreshRequestsBox() {
    const view = window.TC_ROOM_VIEW;
    const sec = document.querySelector('.x-roomview .x-section[aria-label="Data room requests"]');
    if (sec && view && typeof view.blocks === "function") {
      const b = view.blocks(S.roomPartial ? "partial" : "full");
      if (b) sec.outerHTML = b.requests;
    } else if (S.requests) paintWorking();
  }
  document.addEventListener("click", (e) => { if (e.target.closest("[data-ask]")) refreshRequestsBox(); });

  // After the request goes out: the working page lists each item as Open, then the room arrives ------
  const askedText = (d) => d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  const roomOf = () => (S.research && S.research.room) || null;
  const heldBy = (it) => { const r = roomOf(); return r && it.id && r.holds[it.id] ? r.holds[it.id] : null; };
  const founderFull = () => (S.fields.founders.value || "").split(",")[0].trim() || "the founder";

  function markSent() {
    const now = new Date();
    if (S.requests) { S.items.filter((i) => i.checked && !i.askedAt).forEach((i) => { i.askedAt = now; }); refreshRequestsBox(); return; }
    S.requests = { sentAt: now };
    S.roomShared = false; S.roomOpened = false; S.roomPartial = false; S.roomMore = false; S.roomFull = false;
    clearTimeout(S.moreTimer);
    S.items.filter((i) => i.checked).forEach((i) => { i.askedAt = now; });
    clearTimeout(S.arrivalTimer);
    if (roomOf()) {
      const run = S.runStart = (S.runStart || 0) + 1;
      S.arrivalTimer = setTimeout(() => { if (run === S.runStart && S.requests) { S.roomShared = true; paintWorking(); } }, 1800 * PACE);
    }
    paintWorking();
  }

  // Opening the room hands the working page to room_view.js: the first files arrive, then the rest (Ken, 1:03 PM).
  const roomStates = () => { const r = roomOf(); return r && r.states ? r.states : null; };
  function openRoom() {
    S.roomShared = true; S.roomOpened = true; S.roomPartial = !S.roomFull && !!roomStates();
    showRoomView();
    scheduleMore();
  }
  function openMore() {
    S.roomPartial = false; S.roomFull = true;
    showRoomView();
  }
  function showRoomView() {
    const view = window.TC_ROOM_VIEW;
    if (!view || typeof view.render !== "function") return renderReadout();
    view.render(S.roomPartial ? "partial" : "full");
    paintMore();
  }
  function scheduleMore() {
    const st = roomStates();
    if (!st || !S.roomPartial || S.roomMore) return;
    clearTimeout(S.moreTimer);
    S.moreTimer = setTimeout(() => { S.roomMore = true; paintMore(); }, 1800 * PACE);
  }
  function paintMore() {
    const st = roomStates();
    const n = document.getElementById("notify");
    if (!st || !n || !S.roomMore || !S.roomPartial || n.querySelector("#open-more")) return;
    const k = st.full.files_total - st.partial.arrived.length;
    const company = S.fields.name.value || "This company";
    n.insertAdjacentHTML("beforeend", `<div class="notice" role="status"><div><strong>${esc(company)} added ${k} more file${k === 1 ? "" : "s"}</strong> <span class="dot" aria-hidden="true">·</span> just now</div>
      <button class="tc-btn primary" type="button" id="open-more">Open the data room</button></div>`);
  }

  function requestsInner() {
    const company = S.fields.name.value || "This company";
    const rows = S.items.filter((i) => i.checked);
    rows.forEach((i) => { if (!i.askedAt) i.askedAt = new Date(); });
    return `<h2>Data room requests</h2>
      <p class="note" id="req-note">${rows.length} item${rows.length === 1 ? "" : "s"} asked for, all open. Request sent to ${esc(founderFull())} <span class="dot" aria-hidden="true">·</span> waiting for ${esc(company)}'s data room</p>
      <ul class="reqs">${rows.map((it) => `<li class="req" data-state="open">
        <span class="tc-mark">Open</span>
        <div><div class="title">${esc(it.title)}</div><div class="meta">Asked ${esc(askedText(it.askedAt))}</div></div></li>`).join("")}</ul>`;
  }

  function notifyHtml() {
    const room = roomOf();
    if (!S.requests || !room || !S.roomShared || S.roomOpened) return "";
    const company = S.fields.name.value || "This company";
    const st = roomStates();
    const n = st ? st.partial.arrived.length : room.files.length;
    return `<div class="notice" role="status"><div><strong>${esc(company)} shared its data room</strong> <span class="dot" aria-hidden="true">·</span> ${n} file${n === 1 ? "" : "s"} <span class="dot" aria-hidden="true">·</span> just now</div>
      <button class="tc-btn primary" type="button" id="open-room">Open the data room</button></div>`;
  }

  function paintWorking() {
    const n = document.getElementById("notify");
    if (n) n.innerHTML = notifyHtml();
    const box = document.getElementById("roomgaps");
    if (box && S.requests) { box.setAttribute("aria-label", "Data room requests"); box.innerHTML = requestsInner(); }
  }

  function refreshDraft(force) {
    const n = S.items.filter((i) => i.checked).length;
    document.getElementById("count").textContent = `${n} of ${S.items.length} selected`;
    const d = draftText();
    const subj = document.getElementById("d-subject");
    const body = document.getElementById("d-body");
    if (force || !S.edited) {
      S.subject = d.subject; S.body = d.body; S.autoBody = d.body; S.edited = false;
      subj.value = S.subject; body.value = S.body;
    }
    document.getElementById("redo").hidden = !S.edited;
    const enc = encodeURIComponent;
    document.getElementById("mailto").href = `mailto:${enc(S.to).replace("%40", "@")}?subject=${enc(S.subject)}&body=${enc(S.body.replace(/\r?\n/g, "\r\n"))}`;
  }

  function bindRequest(dlg) {
    const asks = document.getElementById("asks");
    asks.addEventListener("change", (e) => {
      const key = e.target.dataset.item;
      const it = S.items.find((x) => x.key === key);
      if (it) { it.checked = e.target.checked; refreshDraft(); }
    });
    dlg.querySelectorAll("[data-pick]").forEach((b) => b.addEventListener("click", () => {
      const k = b.dataset.pick;
      S.items.forEach((i) => { i.checked = k === "all" || (k === "readout" && i.fromReadout); });
      asks.querySelectorAll("input[type=checkbox]").forEach((cb) => { cb.checked = S.items.find((x) => x.key === cb.dataset.item).checked; });
      refreshDraft();
    }));
    document.getElementById("addform").addEventListener("submit", (e) => {
      e.preventDefault();
      const el = document.getElementById("addtext");
      const text = el.value.trim().replace(/\.$/, "");
      if (!text) return;
      const it = { key: `add-${++S.added}`, id: null, title: text[0].toUpperCase() + text.slice(1), ask: `Please send ${lcfirst(text)}.`,
        includes: null, guide: null, guidance: null, fromReadout: false, firstTier: false, custom: true, reasons: [], checked: true };
      S.items.push(it);
      const grp = asks.querySelector("#ask-group");
      if (grp) grp.insertAdjacentHTML("beforebegin", itemLi(it)); else asks.insertAdjacentHTML("beforeend", itemLi(it));
      el.value = "";
      refreshDraft();
    });
    const field = (id, key, store) => document.getElementById(id).addEventListener("input", (e) => {
      S[key] = e.target.value;
      if (store) { try { localStorage.setItem(`tricorder.proto.${key}`, e.target.value); } catch (err) { /* no storage */ } }
      refreshDraft();
    });
    field("d-to", "to"); field("d-by", "by"); field("d-sender", "sender", true); field("d-fund", "fund", true);
    document.getElementById("d-subject").addEventListener("input", (e) => { S.subject = e.target.value; S.edited = true; refreshDraft(); });
    document.getElementById("d-body").addEventListener("input", (e) => { S.body = e.target.value; S.edited = S.body !== S.autoBody; refreshDraft(); });
    document.getElementById("redo-btn").addEventListener("click", () => refreshDraft(true));
    document.getElementById("req-close").addEventListener("click", () => dlg.close());
    document.getElementById("mark-sent").addEventListener("click", () => { if (!S.items.some((i) => i.checked)) { document.getElementById("copied").textContent = "Pick at least one item first."; return; } dlg.close(); markSent(); });
    document.getElementById("copy").addEventListener("click", () => {
      const text = `Subject: ${S.subject}\n\n${S.body}`;
      const done = (ok) => { document.getElementById("copied").textContent = ok ? "Copied." : "Copy did not work here. Select the text instead."; };
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => done(true), () => done(false));
    });
  }

  // Steps 5 to 8 live in their own files and read state and helpers from here.
  window.TC = { D, S, app, esc, chip, sourcePanel, header, go, buildItems, render, openRoom };

  // Start ------------------------------------------------------------------------------------------
  const fromAddress = params.get("company");
  if (fromAddress) {
    startCompany(fromAddress);
  } else {
    if (route() !== "start") history.replaceState(null, "", location.pathname + location.search + "#start");
    render();
  }
})();
