// Analyses for every other piece of the company, each read through a knowledge file the Tricorder team wrote
// (knowledge/<piece>.md). The text and every chart number come from piece_reports.py (piece_reports_data.js);
// this file draws them with the same markup and classes as reports.js, so they look the same.
//
//   TC_PIECE_REPORTS.html(state)   every piece analysis for the open company's room, as an HTML string ("partial" or "full")
//   TC_PIECE_REPORTS.list()        the open company's analyses, as data
//   TC_PIECE_REPORTS.draw(root)    draws every piece chart under root. It also runs by itself whenever a chart placeholder appears.
//   TC_PIECE_REPORTS.memoHead(rep) the knowledge-file label and chart placeholder that open a piece's memo section (memo.js)
//
// Each analysis carries an In memo toggle with the key report:<piece> (TC_MEMO), in by default; memo.js shows the ones that are in.
// Load after data.js, steps_shared.js, vendor/plotly, reports.js and memo_picks.js; then piece_reports_data.js and this file.
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;
  const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  function list() {
    const T = window.TC;
    const slug = T && T.S && T.S.research && T.S.research.slug;
    return ((window.TC_PIECE_REPORTS_DATA || {})[slug]) || [];
  }

  const knowledgeLine = (rep) => `<p class="x-knowledge"><span class="tc-label tc-label--steered">Built from expert knowledge</span>
    <a href="${esc(rep.knowledge)}" target="_blank" rel="noopener"><code>${esc(rep.knowledge)}</code></a></p>`;
  const chartHtml = (rep) => `<div class="x-chart" data-piece-chart="${esc(rep.key)}" role="img" aria-label="${esc(rep.chart.label)}"></div>`;
  const pick = (rep) => (window.TC_MEMO ? `<div class="x-pickrow">${window.TC_MEMO.toggleHtml(`report:${rep.piece}`)}</div>` : "");

  // One analysis. The markup mirrors X.reportBlock in reports.js. The section class is x-piece-report, so checks that count
  // Kimmy's two reports (.x-report) still count two; the evidence buttons get their own hover and click below.
  function block(room, rep, state) {
    const s = state && room.states ? room.states[state === "partial" ? "partial" : "full"] : null;
    const missing = s ? rep.needs.filter((f) => !s.arrived.includes(f)) : [];
    const head = `<h2 class="x-h">${esc(rep.title)}</h2>${knowledgeLine(rep)}`;
    if (missing.length) {
      return `<section class="x-section x-piece-report" aria-label="${esc(rep.title)}" data-report="${esc(rep.key)}" data-piece-report="${esc(rep.piece)}">${head}
        <p class="x-wait"><span class="tc-label tc-label--gap">Waiting on ${esc(missing.map((f) => f.split("/").pop()).join(", "))}</span></p>
        <p class="note">The analysis runs when the file arrives.</p></section>`;
    }
    const order = [];
    rep.paras.forEach((p) => p.refs.forEach((id) => { if (room.claims[id] && !order.includes(id)) order.push(id); }));
    const n = (id) => order.indexOf(id) + 1;
    const srcText = (c) => c.sources.map((x) => (x.public ? x.uri : `${x.uri}, ${x.locator}`)).join("; ");
    const ref = (id) => { const c = room.claims[id]; return c ? `<button type="button" class="x-ev x-prev" data-text="${esc(c.text)}" data-src="${esc(srcText(c))}" data-n="${n(id)}" aria-label="Evidence ${n(id)}">${n(id)}</button>` : ""; };
    const ev = order.length ? `<details class="x-report-ev"><summary>Evidence (${order.length})</summary><ol class="x-evlist">${order.map((id) => `<li class="x-claim">${X.claimBody(room.claims[id])}<div class="x-pickrow">${X.pick(`room:${id}`)}</div></li>`).join("")}</ol></details>` : "";
    return `<section class="x-section x-piece-report" aria-label="${esc(rep.title)}" data-report="${esc(rep.key)}" data-piece-report="${esc(rep.piece)}">
      ${head}${pick(rep)}
      ${chartHtml(rep)}
      <div class="x-report-body">${rep.paras.map((p) => `<p><strong>${esc(p.lead)}</strong> ${esc(p.body)}${p.refs.length ? ` <span class="x-refs">${p.refs.map(ref).join("")}</span>` : ""}</p>`).join("")}
        <h3 class="x-sub">What to ask</h3><ul class="x-asks">${rep.asks.map((a) => `<li>${esc(a)}</li>`).join("")}</ul>
        ${ev}
      </div></section>`;
  }

  // Hover or focus on an evidence number shows the fact and its source; a click opens the evidence list at that row.
  // The same tooltip markup and class as reports.js, so it looks the same.
  let tip = null;
  const hide = () => { if (tip) { tip.remove(); tip = null; } };
  function show(b) {
    hide();
    tip = document.createElement("div");
    tip.className = "ev-tip";
    tip.setAttribute("role", "tooltip");
    tip.innerHTML = `<span class="ev-tip-n">${esc(b.dataset.n)}</span> ${esc(b.dataset.text)}<span class="ev-tip-src">Source: ${esc(b.dataset.src)}</span>`;
    document.body.appendChild(tip);
    const r = b.getBoundingClientRect();
    const w = Math.min(380, window.innerWidth - 32);
    tip.style.width = `${w}px`;
    tip.style.left = `${Math.max(16, Math.min(window.scrollX + r.left, window.scrollX + window.innerWidth - w - 16))}px`;
    tip.style.top = `${window.scrollY + r.bottom + 8}px`;
  }
  document.addEventListener("mouseover", (e) => { const b = e.target.closest(".x-prev"); if (b) show(b); });
  document.addEventListener("mouseout", (e) => { if (e.target.closest(".x-prev")) hide(); });
  document.addEventListener("focusin", (e) => { const b = e.target.closest(".x-prev"); if (b) show(b); });
  document.addEventListener("focusout", (e) => { if (e.target.closest(".x-prev")) hide(); });
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".x-prev");
    if (!b) return;
    const d = b.closest(".x-piece-report").querySelector(".x-report-ev");
    if (d) { d.open = true; const li = d.querySelectorAll("li")[Number(b.dataset.n) - 1]; if (li) li.scrollIntoView({ behavior: "smooth", block: "center" }); }
  });

  function html(state) {
    const room = X.room();
    if (!room) return "";
    return list().map((rep) => block(room, rep, state)).join("");
  }

  // Charts: the same look as reports.js (layoutBase there), from the style's tokens.
  function layoutBase() {
    const ink = token("--tc-ink");
    const ink2 = token("--tc-ink-2");
    const ink3 = token("--tc-ink-3");
    const rule = token("--tc-rule");
    const sans = token("--tc-font-sans");
    const mono = token("--tc-font-mono");
    return {
      paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
      font: { family: sans, size: 13, color: ink2 },
      margin: { l: 64, r: 16, t: 40, b: 48 },
      height: 340,
      legend: { orientation: "h", x: 0, y: 1.14, font: { size: 12, color: ink2 } },
      hoverlabel: { bgcolor: token("--tc-surface"), bordercolor: token("--tc-rule-2"), font: { family: sans, color: ink, size: 13 } },
      xaxis: { gridcolor: rule, linecolor: token("--tc-rule-2"), tickfont: { family: mono, size: 11, color: ink3 }, zeroline: false, fixedrange: true },
      yaxis: { gridcolor: rule, linecolor: token("--tc-rule-2"), tickfont: { family: mono, size: 11, color: ink3 }, zeroline: false, fixedrange: true },
    };
  }
  // Series styles: plan (the company's figure, muted), good (holds up), bad (does not), thin (one-time or unsigned), accent.
  function colour(style) {
    return {
      plan: token("--tc-ink-3"), good: token("--tc-strong"), bad: token("--tc-weak"), mixed: token("--tc-mixed"),
      thin: token("--tc-thin"), accent: token("--tc-accent"),
    }[style] || token("--tc-mixed");
  }
  const AXIS = {
    usd: { tickprefix: "$", tickformat: "~s", hover: "$%{VAL:,.0f}" },
    percent: { ticksuffix: "%", tickformat: ",.0f", hover: "%{VAL:.1f}%" },
    count: { tickformat: ",.0f", hover: "%{VAL:,.0f}" },
    multiple: { ticksuffix: "x", tickformat: ",.0f", hover: "%{VAL:.1f}x" },
  };
  const mono = () => token("--tc-font-mono");

  // Reference lines: c.lines (or one c.line), each {y, label, style}. A line marks a cited benchmark or the deck's own figure.
  function lineShape(c, horizontal) {
    const lines = c.lines || (c.line ? [c.line] : []);
    const shapes = [];
    const annotations = [];
    lines.forEach((ln, i) => {
      const col = colour(ln.style || "bad");
      const font = { family: mono(), size: 12, color: col };
      const box = { bgcolor: token("--tc-surface") || "#fff", borderpad: 2 };
      if (horizontal) {
        shapes.push({ type: "line", yref: "paper", y0: 0, y1: 1, x0: ln.y, x1: ln.y, line: { color: col, width: 2, dash: "dash" } });
        annotations.push({ ...box, text: ln.label, showarrow: false, font, yref: "paper", y: 1 + 0.08 * i, yanchor: "bottom", x: ln.y, xanchor: "left", xshift: 4 });
      } else {
        shapes.push({ type: "line", xref: "paper", x0: 0, x1: 1, y0: ln.y, y1: ln.y, line: { color: col, width: 2, dash: "dash" } });
        annotations.push({ ...box, text: ln.label, showarrow: false, font, xref: "paper", x: ln.right ? 1 : 0, xanchor: ln.right ? "right" : "left", y: ln.y, yanchor: ln.below ? "top" : "bottom" });
      }
    });
    return { shapes, annotations };
  }

  function bars(el, c) {
    const L = layoutBase();
    const h = c.orientation === "h";
    const ax = AXIS[c.unit] || AXIS.count;
    const hover = ax.hover.replace("VAL", h ? "x" : "y");
    const traces = c.series.map((s) => {
      const col = colour(s.style);
      const marker = s.styles ? { color: s.styles.map(colour) }
        : s.style === "thin"
          ? { color: token("--tc-thin-bg") || "rgba(0,0,0,0.1)", line: { color: col, width: 1 }, pattern: { shape: "/", fgcolor: col, size: 6 } }
          : { color: col };
      const t = { type: "bar", name: s.name, marker, orientation: h ? "h" : "v",
        hovertemplate: `${esc(s.name)}<br>%{${h ? "y" : "x"}}: ${hover}<extra></extra>` };
      if (h) { t.y = c.x; t.x = s.y; } else { t.x = c.x; t.y = s.y; }
      if (s.hover) { t.customdata = s.hover; t.hovertemplate = `%{${h ? "y" : "x"}}: %{customdata}<extra></extra>`; }
      if (s.text) {
        t.text = s.text; t.textposition = s.textposition || "outside"; t.cliponaxis = false;
        if (s.textanchor) t.insidetextanchor = s.textanchor;
        t.textfont = t.textposition === "outside" ? { family: mono(), size: 12, color: token("--tc-ink-2") } : { family: mono(), size: 12 };
      }
      return t;
    });
    const valueAxis = { ...L.yaxis, tickprefix: ax.tickprefix, ticksuffix: ax.ticksuffix, tickformat: ax.tickformat, rangemode: "tozero" };
    if (c.range) valueAxis.range = c.range;
    const catAxis = { ...L.xaxis, type: "category", automargin: true };
    const extra = lineShape(c, h);
    const layout = {
      ...L, barmode: c.barmode || "group", bargap: 0.35, showlegend: c.series.length > 1, legend: { ...L.legend, traceorder: "normal" },
      xaxis: h ? { ...valueAxis, gridcolor: L.xaxis.gridcolor } : catAxis,
      yaxis: h ? { ...catAxis, autorange: "reversed" } : valueAxis,
      margin: h ? { ...L.margin, l: 16 } : L.margin,
      shapes: extra.shapes, annotations: extra.annotations,
    };
    if (c.height) layout.height = Math.max(L.height, c.height);
    window.Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
  }

  function line(el, c) {
    const L = layoutBase();
    const ax = AXIS[c.unit] || AXIS.count;
    const traces = c.series.map((s) => ({ type: "scatter", mode: "lines+markers", name: s.name, x: c.x, y: s.y,
      line: { color: colour(s.style), width: 3 }, marker: { size: 5, color: colour(s.style) },
      hovertemplate: `${esc(s.name)}<br>Month %{x}: ${ax.hover.replace("VAL", "y")}<extra></extra>` }));
    const extra = lineShape(c, false);
    const shapes = [...extra.shapes];
    const annotations = [...extra.annotations];
    if (c.mark) {
      shapes.push({ type: "line", x0: c.mark.x, x1: c.mark.x, yref: "paper", y0: 0, y1: 1, line: { color: token("--tc-accent"), width: 1.5, dash: "dot" } });
      annotations.push({ x: c.mark.x, xanchor: "right", xshift: -6, yref: "paper", y: 0.02, yanchor: "bottom", text: c.mark.label, showarrow: false,
        font: { family: mono(), size: 12, color: token("--tc-accent") } });
    }
    if (c.end) {
      const s = c.series[0];
      annotations.push({ x: c.x[c.x.length - 1], y: s.y[s.y.length - 1], xanchor: "right", yanchor: "top", yshift: -8, text: c.end, showarrow: false,
        font: { family: mono(), size: 12, color: colour(s.style) } });
    }
    const layout = {
      ...L, showlegend: true,
      xaxis: { ...L.xaxis, title: { text: c.x_title || "", font: { size: 12, color: token("--tc-ink-3") } }, dtick: 1 },
      yaxis: { ...L.yaxis, ticksuffix: ax.ticksuffix, tickprefix: ax.tickprefix, tickformat: ax.tickformat, range: c.range || [0, 105] },
      shapes, annotations,
    };
    window.Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
  }

  // Dated events on one line, labels alternating above and below.
  function timeline(el, c) {
    const L = layoutBase();
    const ev = c.events;
    const traces = [{ type: "scatter", mode: "markers", x: ev.map((e) => e.date), y: ev.map(() => 0), showlegend: false,
      marker: { size: 12, color: ev.map((e) => colour(e.style)), line: { color: token("--tc-surface"), width: 2 } },
      customdata: ev.map((e) => e.label), hovertemplate: "%{x|%b %-d, %Y}<br>%{customdata}<extra></extra>" }];
    const shapes = [{ type: "line", xref: "paper", x0: 0, x1: 1, y0: 0, y1: 0, line: { color: token("--tc-rule-2"), width: 2 } }];
    if (c.gap) {
      shapes.push({ type: "rect", x0: c.gap.from, x1: c.gap.to, yref: "paper", y0: 0.38, y1: 0.62, fillcolor: token("--tc-weak-bg") || "rgba(0,0,0,0.06)", line: { width: 0 }, layer: "below" });
    }
    const annotations = ev.map((e, i) => ({ x: e.date, y: 0, yanchor: i % 2 ? "top" : "bottom", yshift: i % 2 ? -14 : 14, text: e.short || e.label,
      showarrow: false, align: "center", font: { family: mono(), size: 11, color: colour(e.style) } }));
    if (c.gap && c.gap.label) {
      annotations.push({ x: c.gap.mid, y: 0, yshift: 46, yanchor: "bottom", text: c.gap.label, showarrow: false,
        font: { family: mono(), size: 12, color: token("--tc-weak") } });
    }
    const layout = {
      ...L, showlegend: false, height: c.height || 300, margin: { ...L.margin, l: 24, r: 24, t: 16 },
      xaxis: { ...L.xaxis, type: "date", tickformat: "%b %Y", range: c.range },
      yaxis: { ...L.yaxis, visible: false, range: [-1, 1] },
      shapes, annotations,
    };
    window.Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
  }

  function draw(root) {
    if (!window.Plotly) return;
    const reps = list();
    (root || document).querySelectorAll(".x-chart[data-piece-chart]").forEach((el) => {
      const rep = reps.find((r) => r.key === el.dataset.pieceChart);
      if (!rep || el.dataset.drawn === "1") return;
      el.dataset.drawn = "1";
      el.innerHTML = "";
      const c = rep.chart;
      if (c.kind === "line") line(el, c);
      else if (c.kind === "timeline") timeline(el, c);
      else bars(el, c);
    });
  }

  // Draw whenever a placeholder appears, so the page that inserts the HTML needs no second call.
  let queued = false;
  function soon() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; draw(document); });
  }
  new MutationObserver((muts) => {
    if (muts.some((m) => [...m.addedNodes].some((n) => n.nodeType === 1 && (n.matches("[data-piece-chart]") || n.querySelector("[data-piece-chart]"))))) soon();
  }).observe(document.documentElement, { childList: true, subtree: true });
  // Charts redraw in the right colours when the theme changes.
  if (window.matchMedia) window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    document.querySelectorAll(".x-chart[data-piece-chart]").forEach((el) => { el.dataset.drawn = ""; });
    draw(document);
  });

  // For the memo: the knowledge-file label and the chart placeholder that open a piece's section.
  const memoHead = (rep) => knowledgeLine(rep) + chartHtml(rep);

  window.TC_PIECE_REPORTS = { html, list, draw, memoHead };
})();
