// Report sections read through Kimmy's expert knowledge: traction and revenue, burn and runway.
// The text and every chart number come from synthetic_rooms.py (room.reports); this file draws them.
// Charts are interactive Plotly (vendor/plotly-2.35.2.min.js, pinned and local) in the style's tokens.
//   X.reportBlock(room, rep, state)  a report section for the working page (numbered evidence, what to ask)
//   X.reportChart(rep)               the chart placeholder, for the memo
//   X.drawCharts(root)               draws every chart placeholder under root; call after inserting HTML
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;

  const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const money = (n) => `$${Math.round(n).toLocaleString("en-US")}`;

  X.reportChart = (rep) => `<div class="x-chart" data-chart="${esc(rep.key)}" role="img" aria-label="${esc(chartLabel(rep))}"></div>`;
  function chartLabel(rep) {
    const c = rep.chart;
    if (c.kind === "revenue") {
      return `Monthly revenue from ${c.months[0]} to ${c.months[c.months.length - 1]}: recurring ${money(c.recurring[0])} rising to ${money(c.recurring[c.recurring.length - 1])}, `
        + `against the deck's stated ${money(c.deck_monthly)} a month.`;
    }
    return `Cash over time. ${c.series.map((s) => `${s.name}: runs out after ${s.points[s.points.length - 1][0]} months`).join(". ")}. ${c.baseline_label}.`;
  }

  function monthLabel(asOf, k) {
    let y = Number(asOf.slice(0, 4));
    let m = Number(asOf.slice(5, 7)) + k;
    y += Math.floor((m - 1) / 12);
    m = ((m - 1) % 12) + 1;
    return new Date(y, m - 1, 1).toLocaleDateString("en-US", { month: "short", year: "numeric" });
  }

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

  function revenueChart(el, c) {
    const L = layoutBase();
    const traces = [
      { type: "bar", name: c.recurring_label, x: c.months, y: c.recurring, marker: { color: token("--tc-mixed") },
        hovertemplate: "%{x}<br>Recurring: $%{y:,.0f}<extra></extra>" },
      { type: "bar", name: c.one_time_label, x: c.months, y: c.one_time,
        marker: { color: token("--tc-thin-bg") || "rgba(0,0,0,0.1)", line: { color: token("--tc-thin"), width: 1 }, pattern: { shape: "/", fgcolor: token("--tc-thin"), size: 6 } },
        hovertemplate: "%{x}<br>Not recurring: $%{y:,.0f}<extra></extra>" },
    ];
    const layout = {
      ...L, barmode: "stack", bargap: 0.35,
      xaxis: { ...L.xaxis, type: "category" },
      yaxis: { ...L.yaxis, tickprefix: "$", tickformat: ",.0f", rangemode: "tozero" },
      shapes: [{ type: "line", xref: "paper", x0: 0, x1: 1, yref: "y", y0: c.deck_monthly, y1: c.deck_monthly,
        line: { color: token("--tc-weak"), width: 2, dash: "dash" } }],
      annotations: [{ xref: "paper", x: 0, xanchor: "left", y: c.deck_monthly, yanchor: "bottom", text: c.deck_label, showarrow: false,
        font: { family: token("--tc-font-mono"), size: 12, color: token("--tc-weak") } }],
    };
    window.Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
  }

  function cashChart(el, c) {
    const L = layoutBase();
    const style = {
      plan: { color: token("--tc-ink-3"), dash: "dot", width: 2 },
      hires: { color: token("--tc-weak"), dash: "solid", width: 3 },
      round: { color: token("--tc-mixed"), dash: "solid", width: 3 },
    };
    const end = Math.ceil(Math.max(...c.series.map((s) => s.points[s.points.length - 1][0]), c.baseline) + 1);
    const ticks = [];
    for (let k = 0; k <= end; k += 6) ticks.push(k);
    const traces = c.series.map((s) => ({
      type: "scatter", mode: "lines", name: s.name, x: s.points.map((p) => p[0]), y: s.points.map((p) => p[1]),
      line: { ...style[s.style], shape: "linear" },
      customdata: s.points.map((p) => monthLabel(c.as_of, Math.floor(p[0]))),
      hovertemplate: `${s.name}<br>%{customdata}: $%{y:,.0f}<extra></extra>`,
    }));
    const layout = {
      ...L,
      xaxis: { ...L.xaxis, range: [0, end], tickvals: ticks, ticktext: ticks.map((k) => monthLabel(c.as_of, k)) },
      yaxis: { ...L.yaxis, tickprefix: "$", tickformat: "~s", rangemode: "tozero" },
      shapes: [{ type: "line", x0: c.baseline, x1: c.baseline, yref: "paper", y0: 0, y1: 1, line: { color: token("--tc-accent"), width: 1.5, dash: "dot" } }],
      annotations: [{ x: c.baseline, xanchor: "right", xshift: -6, yref: "paper", y: 1, yanchor: "top", text: c.baseline_label, showarrow: false, align: "right",
        font: { family: token("--tc-font-mono"), size: 12, color: token("--tc-accent") } },
        ...c.series.map((s, i) => { const p = s.points[s.points.length - 1]; return { x: p[0], y: 0, yanchor: "bottom", yshift: 6 + 16 * i, text: s.end, showarrow: false,
          font: { family: token("--tc-font-mono"), size: 11, color: style[s.style].color } }; })],
    };
    window.Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
  }

  X.drawCharts = (root) => {
    const room = X.room();
    if (!room || !window.Plotly) return;
    (root || document).querySelectorAll(".x-chart[data-chart]").forEach((el) => {
      const rep = (room.reports || []).find((r) => r.key === el.dataset.chart);
      if (!rep) return;
      el.innerHTML = "";
      if (rep.chart.kind === "revenue") revenueChart(el, rep.chart);
      else cashChart(el, rep.chart);
    });
  };
  // Charts redraw in the right colours when the theme changes.
  if (window.matchMedia) window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => X.drawCharts(document));

  X.kimmyLine = (rep) => `<p class="x-kimmy">Read with Kimmy's expert knowledge: <code>${esc(rep.knowledge)}</code></p>`;

  // A report on the working page. Evidence is numbered within the report; hover a number for the fact and its source.
  X.reportBlock = (room, rep, state) => {
    const s = state && room.states ? room.states[state] : null;
    const missing = s ? rep.needs.filter((f) => !s.arrived.includes(f)) : [];
    if (missing.length) {
      return `<section class="x-section x-report" aria-label="${esc(rep.title)}" data-report="${esc(rep.key)}"><h2 class="x-h">${esc(rep.title)}</h2>${X.kimmyLine(rep)}
        <p class="x-wait"><span class="tc-label tc-label--gap">Waiting on ${esc(missing.map((f) => f.split("/").pop()).join(", "))}</span></p>
        <p class="note">The report runs when the file arrives.</p></section>`;
    }
    const order = [];
    rep.paras.forEach((p) => p.refs.forEach((id) => { if (room.claims[id] && !order.includes(id)) order.push(id); }));
    const num = (id) => order.indexOf(id) + 1;
    const srcText = (c) => c.sources.map((x) => (x.public ? x.uri : `${x.uri}, ${x.locator}`)).join("; ");
    const ref = (id) => { const c = room.claims[id]; return c ? `<button type="button" class="x-ev x-rev" data-text="${esc(c.text)}" data-src="${esc(srcText(c))}" data-n="${num(id)}" aria-label="Evidence ${num(id)}">${num(id)}</button>` : ""; };
    return `<section class="x-section x-report" aria-label="${esc(rep.title)}" data-report="${esc(rep.key)}">
      <h2 class="x-h">${esc(rep.title)}</h2>${X.kimmyLine(rep)}
      ${X.reportChart(rep)}
      <div class="x-report-body">${rep.paras.map((p) => `<p><strong>${esc(p.lead)}</strong> ${esc(p.body)} <span class="x-refs">${p.refs.map(ref).join("")}</span></p>`).join("")}
        <h3 class="x-sub">What to ask</h3><ul class="x-asks">${rep.asks.map((a) => `<li>${esc(a)}</li>`).join("")}</ul>
        <details class="x-report-ev"><summary>Evidence (${order.length})</summary><ol class="x-evlist">${order.map((id) => `<li class="x-claim">${X.claimBody(room.claims[id])}<div class="x-pickrow">${X.pick(`room:${id}`)}</div></li>`).join("")}</ol></details>
      </div></section>`;
  };

  // Hover or focus on a report's evidence number shows the fact and its source.
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
  document.addEventListener("mouseover", (e) => { const b = e.target.closest(".x-rev"); if (b) show(b); });
  document.addEventListener("mouseout", (e) => { if (e.target.closest(".x-rev")) hide(); });
  document.addEventListener("focusin", (e) => { const b = e.target.closest(".x-rev"); if (b) show(b); });
  document.addEventListener("focusout", (e) => { if (e.target.closest(".x-rev")) hide(); });
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".x-rev");
    if (!b) return;
    const d = b.closest(".x-report").querySelector(".x-report-ev");
    if (d) { d.open = true; const li = d.querySelectorAll("li")[Number(b.dataset.n) - 1]; if (li) li.scrollIntoView({ behavior: "smooth", block: "center" }); }
  });
})();
