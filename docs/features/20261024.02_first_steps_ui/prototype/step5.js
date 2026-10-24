// Step 5: the readout of the synthetic room. Flags first, then the overview of every piece, then a
// drill-down into one weak piece and one strong one, then what the room settled from the earlier steps.
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;

  const STATUS = {
    confirms: '<span class="tc-mark tc-mark--strong">Confirms</span>',
    answers: '<span class="tc-mark">Answers a gap</span>',
    differs: '<span class="tc-mark tc-mark--disagreement">Differs</span>',
    "not settled": '<span class="tc-mark tc-mark--thin">Not settled</span>',
  };

  function requestRows(room) {
    const T = window.TC;
    if (!T.S.items) T.buildItems();
    const asked = T.S.items.filter((i) => i.checked);
    const rows = asked.map((it) => {
      const files = it.id ? room.holds[it.id] : null;
      return { it, files };
    });
    return { rows, held: rows.filter((r) => r.files).length, total: rows.length };
  }

  function render() {
    const T = window.TC;
    const room = X.room();
    if (!room) return X.noRoom("flags", ["received", "room received"]);
    const company = X.company();
    const req = requestRows(room);
    const confirmed = room.prechecks.filter((p) => p.status === "confirms").length;
    const drillHtml = room.drill.map((d) => {
      const p = X.pieceOf(room, d.piece);
      return `<section class="x-drill" id="drill-${esc(d.piece)}" aria-label="Drill-down: ${esc(p.label)}">
        <div class="x-drill-head"><h3 class="tc-h4">${esc(p.label)}</h3>${X.verdictMark(p.verdict)}
          <span class="tc-meta">${X.counts(p)}</span></div>
        <p class="x-reason">${esc(p.reason)}</p>
        <ul class="x-claims">${d.claim_ids.map((id) => `<li class="x-claim">${X.claimBody(room.claims[id])}</li>`).join("")}</ul>
        ${d.panel ? X.table(d.panel) : ""}
        ${d.gaps.length ? `<ul class="tc-gap-list x-gaps">${d.gaps.map((g) => `<li>${esc(g)}</li>`).join("")}</ul>` : ""}
      </section>`;
    }).join("");
    const drillSet = new Set(room.drill.map((d) => d.piece));

    T.app.innerHTML = `${T.header("flags", ["received", "room received"])}
      <h2 class="co-title">${esc(company)}: flags from the data room</h2>
      ${X.notice(room)}
      <p class="x-lede">The room holds <button type="button" class="tc-link-btn" data-scroll="x-request">${req.held} of the ${req.total} items you asked for</button>.
        It <button type="button" class="tc-link-btn" data-scroll="x-pre">confirms ${confirmed} claims from the first readout</button>.</p>

      <section class="x-section" aria-label="Top green and red flags">
        <h2 class="x-h">The best green flags and the worst red flags</h2>
        <div class="x-flags">${[...room.top_flags.green, ...room.top_flags.red].map((f) => X.flagCard(room, f)).join("")}</div>
      </section>

      <section class="x-section" aria-label="Overview">
        <h2 class="x-h">Each piece of the company</h2>
        <div class="x-verdicts">${room.pieces.map((p) => X.verdictRow(p, drillSet.has(p.name) ? `<button type="button" class="tc-link-btn x-open" data-scroll="drill-${esc(p.name)}">Open the drill-down</button>` : "")).join("")}</div>
      </section>

      <section class="x-section" aria-label="Drill-down">
        <h2 class="x-h">Drill-down: one weak piece, one strong</h2>
        ${drillHtml}
      </section>

      <section class="x-section" id="x-request" aria-label="Your request, ticked off">
        <h2 class="x-h">Your request, ticked off</h2>
        <p class="note">${req.held} of ${req.total} are in the room. The rest stay on the list.</p>
        <ul class="x-ticks">${req.rows.map(({ it, files }) => `<li class="x-tick" data-held="${files ? "yes" : "no"}">
          ${files ? '<span class="tc-label tc-label--clean">In the room</span>' : '<span class="tc-label tc-label--gap">Still missing</span>'}
          <span class="x-tick-title">${esc(it.title)}</span>
          ${files ? `<div class="tc-chips">${files.map((f) => X.roomChip({ uri: f.split(", ")[0], locator: f.split(", ")[1] || "whole file", quote: "Received with the room." })).join("")}</div>` : ""}
        </li>`).join("")}</ul>
      </section>

      <section class="x-section" id="x-pre" aria-label="The first readout, checked against the room">
        <h2 class="x-h">The first readout, checked against the room</h2>
        <div class="tc-table-wrap"><table class="tc-table tc-table--stack x-pre">
          <thead><tr><th>Before the room</th><th>Room</th><th>What the room shows</th></tr></thead>
          <tbody>${room.prechecks.map((p) => {
            const pre = T.S.research.pre[p.pre];
            return `<tr data-status="${esc(p.status)}"><td data-label="Before the room">${esc(pre.text)} ${T.chip(pre.source, pre)}</td>
              <td data-label="Room">${STATUS[p.status]}</td>
              <td data-label="What the room shows">${esc(p.room)} ${X.roomChip(p.source)}</td></tr>`;
          }).join("")}</tbody></table></div>
      </section>

      <div class="actions"><button class="tc-btn primary" type="button" id="to-steer">Steer the readout</button>
        <a class="btn tc-btn tc-btn--secondary" href="http://localhost:5173/">Open the built readout page</a></div>`;
    document.getElementById("to-steer").addEventListener("click", () => T.go("steer"));
  }

  window.TC_STEPS.flags = render;
})();
