// Step 6: the associate steers the readout. One plain sentence on a piece or a line, nothing else.
// A steer never changes a script's number. Tricorder reads the sentence as one of three kinds:
//   rewrite: the piece's wording changes, marked as the associate's, and the verdict stays the script's;
//   figure:  the associate's figure sits beside the check's, labelled as the steer's;
//   more:    a request for more information goes onto the data-room request.
// Modelled on the built steering (docs/ongoing/roadmap/steering.md, apps/web/src/Steering.tsx).
(function () {
  "use strict";
  const X = window.TCX;
  const esc = X.esc;

  function classify(sentence, piece, room) {
    const ex = room.steer_examples.find((e) => e.sentence === sentence && e.piece === piece);
    if (ex) return { ...ex };
    if (/^(i disagree|this piece is wrong|this line is wrong)/i.test(sentence)) return { kind: "rewrite" };
    if (/^(get|ask|send|fetch|request|find|read|pull)\b|\b(more information|more info|invoices?|statements?)\b/i.test(sentence)) {
      return { kind: "more", request: sentence.replace(/^(get|ask for|ask|send|fetch|request|find|read|pull)\s+/i, "").replace(/\.$/, "") };
    }
    const nums = [...sentence.matchAll(/\$?\d[\d,]*(\.\d+)?\s*(%|M\b|k\b|months?\b)?/gi)];
    if (nums.length) {
      const pick = nums.filter((m) => m[2] || m[0].startsWith("$")).pop() || nums[nums.length - 1];
      return { kind: "figure", steer_value: pick[0].trim(), label: "Your figure" };
    }
    return { kind: "rewrite" };
  }

  function apply(room, piece, line, sentence) {
    const st = X.st();
    const s = { piece, line, sentence: sentence.trim(), at: new Date(), ...classify(sentence.trim(), piece, room) };
    const p = X.pieceOf(room, piece);
    if (s.kind === "rewrite" && line) s.kind = "note";
    if (s.kind === "rewrite") {
      s.before = p.reason;
      s.after = s.reworded || `Steered: ${s.sentence.replace(/^this piece is wrong:?\s*/i, "")} The script's reading stays below for the record.`;
      s.wrong = /^this piece is wrong/i.test(s.sentence);
    }
    if (s.kind === "figure" && !s.check_value) {
      const ids = p.claim_ids.map((id) => room.claims[id]);
      const c = line ? room.claims[line] : ids.find((x) => x.severity === "flag") || ids.find((x) => p.reason === x.text) || ids[0];
      s.check_value = c ? c.display : "";
      s.label = s.label || "Figure";
    }
    if (s.kind === "more") {
      const T = window.TC;
      if (!T.S.items) T.buildItems();
      const key = `steer-${st.steers.length + 1}`;
      T.S.items.push({ key, id: null, title: s.request[0].toUpperCase() + s.request.slice(1), ask: `Please send ${s.request[0].toLowerCase() + s.request.slice(1)}.`,
        includes: null, guide: null, guidance: null, fromReadout: false, firstTier: false, custom: true, reasons: [`From a steer on ${p.label.toLowerCase()}.`], checked: true });
    }
    st.steers.push(s);
  }

  function lastRewrite(piece) {
    return X.st().steers.filter((s) => s.piece === piece && s.kind === "rewrite").pop();
  }

  function resultHtml(s, room) {
    const who = `Your steer, ${s.at.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
    const said = `<p><span class="tc-label tc-label--steered">${esc(who)}</span> "${esc(s.sentence)}"</p>`;
    if (s.kind === "figure") {
      return `<div class="x-result" data-kind="figure">${said}
        <div class="tc-pair tc-pair--small"><div><div class="tc-pair-key">The check's figure</div><div class="tc-pair-value">${esc(s.check_value)}</div><div class="tc-pair-source">Computed by the script</div></div>
        <div><div class="tc-pair-key">${esc(s.label === "Your figure" ? "Your steer" : `${s.label}, your steer`)}</div><div class="tc-pair-value">${esc(s.steer_value)}</div><div class="tc-pair-source">Marked as yours. No source in the room yet.</div></div></div>
        <p>The check's number stays as the script computed it. Yours sits beside it until a file in the room supports it.</p></div>`;
    }
    if (s.kind === "more") {
      return `<div class="x-result" data-kind="more">${said}
        <p><span class="tc-mark tc-mark--running">Waiting on the founder</span> Added to the data-room request: ${esc(s.request)}.</p></div>`;
    }
    if (s.kind === "note") {
      const c = room.claims[s.line];
      return `<div class="x-result" data-kind="note">${said}<p>A note on the line "${esc(c.text)}" Kept with the readout and the memo. The line's figure stays.</p></div>`;
    }
    return `<div class="x-result" data-kind="rewrite">${said}<p>The wording changed. The verdict stays the script's.</p></div>`;
  }

  function pieceHtml(room, p) {
    const st = X.st();
    const rw = lastRewrite(p.name);
    const steers = st.steers.filter((s) => s.piece === p.name);
    const open = st.linesOpen[p.name];
    const disagrees = rw && rw.wrong ? '<span class="tc-mark tc-mark--disagreement">You say it is wrong</span>' : "";
    const lines = open ? `<ul class="x-claims">${p.claim_ids.map((id) => {
      const c = room.claims[id];
      const v = st.lineViews[id];
      return `<li class="x-claim" data-line="${esc(id)}">${X.claimBody(c)}
        <div class="x-line-tools">
          <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-agree="${esc(id)}" aria-pressed="${v === "agree"}">Agree</button>
          <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-disagree="${esc(id)}" aria-pressed="${v === "disagree"}">Disagree</button>
          <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-steerline="${esc(id)}" data-piece="${esc(p.name)}">Steer this line</button>
          ${v === "agree" ? '<span class="tc-mark">You agree</span>' : v === "disagree" ? '<span class="tc-mark tc-mark--disagreement">You disagree</span>' : ""}
        </div><div class="x-boxslot" data-slot="${esc(p.name)}:${esc(id)}"></div></li>`;
    }).join("")}</ul>` : "";
    return `<article class="x-piece${rw ? " tc-steered" : ""}" data-piece="${esc(p.name)}">
      <div class="x-piece-head"><h3>${esc(p.label)}</h3>${X.verdictMark(p.verdict)}${disagrees}
        ${rw ? '<span class="tc-label tc-label--steered">Steered</span>' : ""}<span class="tc-meta">${X.counts(p)}</span></div>
      <p class="x-reason">${esc(rw ? rw.after : p.reason)}</p>
      ${rw ? `<p class="x-before">Before: <s>${esc(rw.before)}</s></p>` : ""}
      <div class="x-piece-tools">
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-steer="${esc(p.name)}">Steer this piece</button>
        <button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-wrong="${esc(p.name)}">This piece is wrong</button>
        ${p.claim_ids.length ? `<button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-lines="${esc(p.name)}" aria-expanded="${!!open}">${open ? "Hide the lines" : `Show the ${p.claim_ids.length} line${p.claim_ids.length === 1 ? "" : "s"}`}</button>` : ""}
      </div>
      <div class="x-boxslot" data-slot="${esc(p.name)}:"></div>
      ${steers.map((s) => resultHtml(s, room)).join("")}
      ${lines}</article>`;
  }

  function boxHtml(prefill) {
    return `<form class="x-steerbox"><input class="tc-input" type="text" aria-label="Your steer, one sentence" placeholder="One plain sentence, then Enter" value="${esc(prefill || "")}" />
      <button class="tc-btn tc-btn--small" type="submit">Steer</button><button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-cancel>Cancel</button></form>`;
  }

  function render() {
    const T = window.TC;
    const room = X.room();
    if (!room) return X.noRoom("steer", ["flags", "the flags from the room"]);
    const st = X.st();
    const company = X.company();
    const log = st.steers.length ? `<ol class="x-log">${st.steers.map((s, i) => `<li><span class="tc-meta">v${i + 2} · ${esc(s.at.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }))}</span>
        ${esc(X.pieceOf(room, s.piece).label)}: "${esc(s.sentence)}" <span class="tc-mark">${{ rewrite: "Reworded", figure: "Your figure beside the check's", more: "Sent to the request", note: "A note on a line" }[s.kind]}</span></li>`).join("")}</ol>`
      : '<p class="note">No steers yet. Every steer is kept here, and the memo\'s change log reads it.</p>';
    T.app.innerHTML = `${T.header("steer", ["flags", "the flags from the room"])}
      <h2 class="co-title">${esc(company)}: steer the readout</h2>
      ${X.notice(room)}
      <p class="x-lede">Type one plain sentence on a piece or a line. A steer never changes a script's number. It rewords the piece, adds your figure beside the check's, or sends a request to the founder.</p>
      <div class="x-steer-try"><span class="tc-label">Try</span>${room.steer_examples.map((e, i) => `<button class="tc-btn tc-btn--secondary tc-btn--small" type="button" data-example="${i}">${esc(X.pieceOf(room, e.piece).label)}: "${esc(e.sentence)}"</button>`).join("")}</div>
      <section class="x-section" aria-label="Each piece, steerable"><h2 class="x-h">Each piece of the company</h2>
        <div id="x-pieces">${room.pieces.map((p) => pieceHtml(room, p)).join("")}</div></section>
      <section class="x-section" aria-label="Change log"><h2 class="x-h">Change log</h2>${log}</section>
      <div class="actions"><button class="tc-btn primary" type="button" id="to-memo">Make the memo</button></div>`;
    document.getElementById("to-memo").addEventListener("click", () => T.go("memo"));
  }

  function openBox(slot, piece, line, prefill) {
    document.querySelectorAll(".x-steerbox").forEach((f) => f.remove());
    const el = document.querySelector(`[data-slot="${CSS.escape(`${piece}:${line || ""}`)}"]`);
    if (!el) return;
    el.innerHTML = boxHtml(prefill);
    const form = el.querySelector("form");
    const input = form.querySelector("input");
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!input.value.trim()) return;
      apply(X.room(), piece, line, input.value);
      render();
      const target = document.querySelector(`.x-piece[data-piece="${CSS.escape(piece)}"]`);
      if (target) target.scrollIntoView({ block: "center" });
    });
    form.querySelector("[data-cancel]").addEventListener("click", () => form.remove());
  }

  document.addEventListener("click", (e) => {
    if (location.hash !== "#steer") return;
    const room = X.room();
    if (!room) return;
    const t = e.target.closest("button");
    if (!t) return;
    const st = X.st();
    if (t.dataset.example !== undefined) {
      const ex = room.steer_examples[Number(t.dataset.example)];
      apply(room, ex.piece, null, ex.sentence);
      render();
      const target = document.querySelector(`.x-piece[data-piece="${CSS.escape(ex.piece)}"]`);
      if (target) target.scrollIntoView({ block: "center" });
    } else if (t.dataset.steer) openBox(null, t.dataset.steer, null, "");
    else if (t.dataset.wrong) openBox(null, t.dataset.wrong, null, "This piece is wrong: ");
    else if (t.dataset.steerline) openBox(null, t.dataset.piece, t.dataset.steerline, "");
    else if (t.dataset.lines) { st.linesOpen[t.dataset.lines] = !st.linesOpen[t.dataset.lines]; render(); }
    else if (t.dataset.agree) { st.lineViews[t.dataset.agree] = st.lineViews[t.dataset.agree] === "agree" ? null : "agree"; render(); }
    else if (t.dataset.disagree) {
      const id = t.dataset.disagree;
      st.lineViews[id] = st.lineViews[id] === "disagree" ? null : "disagree";
      render();
      if (st.lineViews[id] === "disagree") openBox(null, room.claims[id].piece, id, "I disagree because ");
    }
  });

  window.TC_STEPS.steer = render;
})();
