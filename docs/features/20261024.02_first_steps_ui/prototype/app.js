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
      items: null, itemsStage: null, edited: false });
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
  function header(cur, back) {
    return `<header class="masthead"><h1 class="tc-brand">Tricorder</h1><span class="note">Prototype. First steps, before any data room.</span></header>
      ${stepsNav(cur)}${back ? `<p class="back"><a href="#${back[0]}">Back to ${esc(back[1])}</a></p>` : ""}`;
  }

  function render() {
    S.run++; // stops any arrival that is still playing
    const r = route();
    if (r !== "start" && !S.fields) return renderStart();
    if (r === "readout") return renderReadout();
    if (r === "request") return renderRequest();
    if (r === "received") return renderReceived();
    if (window.TC_STEPS && window.TC_STEPS[r]) return window.TC_STEPS[r]();
    return renderStart();
  }

  // Step 1: the URL -------------------------------------------------------------------------
  function renderStart() {
    const tries = ["https://ploy.ai", "https://www.sazabi.com/", "https://www.ycombinator.com/companies/ploy", "https://tester.army"];
    app.innerHTML = `${header("start")}
      <section class="start" aria-label="Start from a company URL">
        <h2>Which company?</h2>
        <p>Paste the company's website or its YC company page. Tricorder sets the company up and starts the research.</p>
        <form id="urlform">
          <input type="url" id="url" name="url" required class="tc-input" placeholder="https://ploy.ai" aria-label="Company URL" value="${esc(S.url)}" />
          <button class="tc-btn primary" type="submit">Start</button>
        </form>
        <div class="tries"><span class="note">Try:</span>${tries.map((t) => `<button type="button" class="link tc-link-btn" data-try="${esc(t)}">${esc(t.replace(/^https:\/\//, ""))}</button>`).join("")}</div>
        <p class="note">Tricorder matches the URL against the saved YC Spring 2026 list of ${D.companies.length} companies. A link with <code>?company=</code> and a URL opens a company directly.</p>
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
      return `<tr class="claim ph wait"><td class="claim-text">${esc(c.text)}</td><td class="claim-src"><span class="tc-mark ph" title="Prototype filler. Benjamin's research builds this part.">Placeholder</span></td></tr>`;
    }
    return `<tr class="claim wait" id="ev-${c._n}"><td class="claim-text"><span class="ev-n">${c._n}</span> ${esc(c.text)} ${KIND[c.kind] || ""}</td><td class="claim-src">${chip(c.source, c)}</td></tr>`;
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
    const cards = list.map((ins) => {
      const nums = [...new Set(ins.refs.map((r) => (claims.find((c) => c.text.includes(r)) || {})._n).filter(Boolean))];
      const [cls, label] = MARKS[ins.mark] || MARKS.thin;
      return `<article class="tc-card insight wait"><div class="tc-card-head"><span class="tc-mark ${cls}">${label}</span><span class="piece">${esc(ins.piece)}</span></div>
        <h3>${esc(ins.title)}</h3><p>${esc(ins.text)}</p>
        <p class="based">Based on ${nums.map((n) => `<a class="ev-ref" href="#ev-${n}">${n}</a>`).join(" ")}</p></article>`;
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
        The prototype holds saved research for Ploy and Sazabi only. In the built app, Tricorder runs the outside scans here, section by section.
        You can still draft the data-room request from the stage's first-tier documents.</div>`;
    } else {
      numberClaims(R);
      body = `<p class="status" id="overall" role="status"></p>
        ${insightsHtml(R)}
        <div class="evidence-head"><h2>Evidence</h2><p class="note">Every fact Tricorder found, numbered, each with its source: the founders, comps, market signals, then the outside world.</p></div>
        ${R.sections.map(sectionHtml).join("")}
        <section class="roomgaps wait" id="roomgaps" aria-label="What only a data room can answer">
          <h2>What only a data room can answer</h2>
          <p class="note">These become the first items on the data-room request.</p>
          <ul class="gaps tc-gap-list">${R.room_gaps.map((g) => `<li class="wait"><strong>${esc(g.text)}</strong> <span class="why">${esc(g.why)}</span></li>`).join("")}</ul>
        </section>`;
    }
    app.innerHTML = `${header("readout", ["start", "the company URL"])}
      <h2 id="co-name" class="co-title">${esc(name)}</h2>
      ${R ? aboutHtml(R) : setupPanel()}
      <div class="masthead readout-head"><h2 class="sub-title">First readout</h2>
        ${R ? '<button class="link tc-link-btn" id="replay" type="button">Replay the research</button>' : ""}</div>
      <p class="note">Built from public sources.</p>
      ${body}
      <div class="actions"><button class="tc-btn primary" id="to-request" type="button">Draft the data-room request</button></div>`;
    bindSetup();
    document.getElementById("to-request").addEventListener("click", () => go("request"));
    if (R) {
      document.getElementById("replay").addEventListener("click", () => { S.streamed = false; renderReadout(); });
      arrive(R);
    }
  }

  // The research arrives: each section, then each claim, as if streaming in.
  function arrive(R) {
    const run = ++S.run;
    const overall = document.getElementById("overall");
    const sections = [...app.querySelectorAll(".section")];
    const steps = [];
    const show = (el) => { el.classList.remove("wait"); el.classList.add("arrive"); };
    const t = (ms) => ms * PACE;
    sections.forEach((sec, i) => {
      const s = R.sections[i];
      steps.push([t(500), () => { show(sec); sec.querySelector("[data-status]").textContent = "Reading the saved sources"; overall.textContent = `Researching: ${s.title.toLowerCase()}`; }]);
      sec.querySelectorAll(".wait").forEach((el) => steps.push([el.matches(".part, .card") ? t(250) : t(420), () => show(el)]));
      steps.push([t(300), () => { sec.querySelector("[data-status]").textContent = `Done: ${countOf(s)}`; }]);
    });
    const rg = document.getElementById("roomgaps");
    steps.push([t(500), () => show(rg)]);
    rg.querySelectorAll(".wait").forEach((el) => steps.push([t(300), () => show(el)]));
    app.querySelectorAll(".insight.wait").forEach((el) => steps.push([t(450), () => { overall.textContent = "Reading the evidence"; show(el); }]));
    steps.push([0, () => { overall.textContent = `Research done: ${R.sections.length} sections.`; S.streamed = true; }]);

    if (S.streamed || PACE === 0) {
      steps.forEach(([, f]) => f());
      app.querySelectorAll(".arrive").forEach((el) => el.classList.remove("arrive"));
      return;
    }
    let i = 0;
    const tick = () => {
      if (run !== S.run || i >= steps.length) return;
      const [, f] = steps[i++];
      f();
      setTimeout(tick, i < steps.length ? steps[i][0] : 0);
    };
    setTimeout(tick, t(300));
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

  function itemLi(it) {
    const g = it.guidance;
    const tags = [
      it.fromReadout ? '<span class="tc-mark warn">From the readout</span>' : "",
      it.firstTier ? `<span class="tc-mark">First tier at ${esc(STAGES[S.itemsStage])}</span>` : "",
      it.custom ? '<span class="tc-mark">Added by you</span>' : "",
    ].join("");
    return `<li class="ask">
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

  function renderRequest() {
    chipN = 0;
    if (!S.items || S.itemsStage !== S.fields.stage.value) buildItems();
    if (!S.by) S.by = defaultBy();
    const company = S.fields.name.value || "This company";
    const fromReadout = S.items.filter((i) => i.fromReadout).length;
    app.innerHTML = `${header("request", ["readout", "the first readout"])}
      <h2 class="co-title">${esc(company)}: the data-room request</h2>
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
          <ul class="asks" id="asks">${S.items.map(itemLi).join("")}</ul>
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
      </div>
      <div class="actions"><button class="tc-btn primary" type="button" id="to-received">The founder sends the room</button></div>`;
    bindRequest();
    refreshDraft(true);
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

  function bindRequest() {
    const asks = document.getElementById("asks");
    asks.addEventListener("change", (e) => {
      const key = e.target.dataset.item;
      const it = S.items.find((x) => x.key === key);
      if (it) { it.checked = e.target.checked; refreshDraft(); }
    });
    app.querySelectorAll("[data-pick]").forEach((b) => b.addEventListener("click", () => {
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
      asks.insertAdjacentHTML("beforeend", itemLi(it));
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
    document.getElementById("copy").addEventListener("click", () => {
      const text = `Subject: ${S.subject}\n\n${S.body}`;
      const done = (ok) => { document.getElementById("copied").textContent = ok ? "Copied." : "Copy did not work here. Select the text instead."; };
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => done(true), () => done(false));
    });
    document.getElementById("to-received").addEventListener("click", () => go("received"));
  }

  // Step 4: the room comes back -----------------------------------------------------------------
  function renderReceived() {
    const company = S.fields.name.value || "This company";
    const n = S.items ? S.items.filter((i) => i.checked).length : 0;
    app.innerHTML = `${header("received", ["request", "the data-room request"])}
      <h2 class="co-title">${esc(company)}: data room received</h2>
      <p class="banner tc-synthetic" role="note">This data room is synthetic. The team wrote it for the demo. It is not ${esc(company)}'s data.</p>
      <p>You asked for ${n} item${n === 1 ? "" : "s"}. Tricorder now checks what the room holds against that list, then reads the room for red and green flags.</p>
      <p>This is where the prototype joins the app that is already built: the readout with its flags, the gaps, and the requests for anything still missing.</p>
      <div class="actions"><a class="btn primary tc-btn" href="#flags">See the flags from the room</a> <a class="btn tc-btn tc-btn--secondary" href="http://localhost:5173/">Open the built readout page</a>
        <span class="note">Runs on this laptop at localhost:5173.</span></div>`;
  }

  // Steps 5 to 8 live in their own files and read state and helpers from here.
  window.TC = { D, S, app, esc, chip, sourcePanel, header, go, buildItems, render };

  // Start ------------------------------------------------------------------------------------------
  const fromAddress = params.get("company");
  if (fromAddress) {
    startCompany(fromAddress);
  } else {
    if (route() !== "start") history.replaceState(null, "", location.pathname + location.search + "#start");
    render();
  }
})();
