// Which claims go into the final memo. One shared list for every page: the first readout, the room view and the memo.
// State is kept per company, in memory and (wrapped in try/catch) in localStorage.
//
//   TC_MEMO.get(key)            true if the claim is in the memo. Unset keys use the default: insights, flags and piece analyses are in, everything else is out.
//   TC_MEMO.set(key, bool)      put a claim in or out. Fires the change event.
//   TC_MEMO.list()              every key seen so far, as [{ key, in }]. list(true) gives only the ones in.
//   TC_MEMO.toggleHtml(key)     the "In memo" toggle button, as an HTML string. The click and the on/off state are handled here, on every page.
//   TC_MEMO.on(fn)              fn({ key, in }) after any change. The same change fires window event "tc-memo-change" with detail { key, in, company }.
//   TC_MEMO.reset()             clear this company's choices back to the defaults.
//
// Keys, by prefix:
//   insight:<n>     a card under What stands out on the first readout (n counts from 0)
//   claim:<n>       a numbered evidence row on the first readout (the number shown beside the row)
//   flag:<claim_id> a flag from the data room (the claim id in the room data)
//   report:<piece> a piece analysis in the completed room (piece_reports.js), shown in the memo
// A key with any other prefix defaults to out. Pages call get(key) for each of their rows; that is what makes list() know them.
(function () {
  "use strict";
  const KEY = "tricorder.proto.memo.";
  const mem = {};
  const seen = {};
  const listeners = [];

  const company = () => {
    const T = window.TC;
    return (T && T.S && ((T.S.research && T.S.research.slug) || T.S.url)) || "default";
  };
  const defaultIn = (key) => /^(insight|flag|report):/.test(key);
  function load(c) {
    if (mem[c]) return mem[c];
    let o = {};
    try { o = JSON.parse(localStorage.getItem(KEY + c) || "{}") || {}; } catch (e) { o = {}; }
    mem[c] = o;
    seen[c] = seen[c] || {};
    return o;
  }
  function save(c) {
    try { localStorage.setItem(KEY + c, JSON.stringify(mem[c])); } catch (e) { /* no storage */ }
  }

  function get(key) {
    const c = company();
    const o = load(c);
    seen[c][key] = true;
    return Object.prototype.hasOwnProperty.call(o, key) ? !!o[key] : defaultIn(key);
  }
  function set(key, value) {
    const c = company();
    const o = load(c);
    seen[c][key] = true;
    const v = !!value;
    if (get(key) === v && Object.prototype.hasOwnProperty.call(o, key)) return;
    o[key] = v;
    save(c);
    const detail = { key, in: v, company: c };
    listeners.slice().forEach((fn) => { try { fn({ key, in: v }); } catch (e) { /* a listener must not break the page */ } });
    window.dispatchEvent(new CustomEvent("tc-memo-change", { detail }));
  }
  function list(onlyIn) {
    const c = company();
    load(c);
    const all = Object.keys(Object.assign({}, seen[c], mem[c])).map((key) => ({ key, in: get(key) }));
    return onlyIn ? all.filter((x) => x.in) : all;
  }
  function reset() {
    const c = company();
    const changed = Object.keys(load(c));
    mem[c] = {};
    save(c);
    changed.forEach((key) => window.dispatchEvent(new CustomEvent("tc-memo-change", { detail: { key, in: get(key), company: c } })));
  }
  const esc = (s) => String(s).replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));

  // The toggle: a checkbox-style button. Filled box with a tick means in the memo; an empty box means out.
  function toggleHtml(key) {
    const on = get(key);
    return `<button type="button" class="memo-pick${on ? " on" : ""}" role="checkbox" aria-checked="${on}" data-memo="${esc(key)}">` +
      `<span class="memo-box" aria-hidden="true">${on ? "&#10003;" : ""}</span><span class="memo-pick-label">In memo</span></button>`;
  }
  function paint(key, on) {
    document.querySelectorAll("[data-memo]").forEach((b) => {
      if (b.dataset.memo !== key) return;
      b.classList.toggle("on", on);
      b.setAttribute("aria-checked", String(on));
      b.querySelector(".memo-box").innerHTML = on ? "&#10003;" : "";
    });
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".memo-pick[data-memo]");
    if (!b) return;
    set(b.dataset.memo, !get(b.dataset.memo));
  });
  window.addEventListener("tc-memo-change", (e) => paint(e.detail.key, e.detail.in));

  window.TC_MEMO = { get, set, list, reset, toggleHtml, on: (fn) => listeners.push(fn) };
})();
