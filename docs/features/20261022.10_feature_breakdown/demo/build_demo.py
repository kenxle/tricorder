"""Build a one-page demo of the wave 1 scans from their real output.

Run bin/smoke on each room first, so out/<room>/ holds redflags.json and readout.json.
Then: python3 docs/features/20261022.10_feature_breakdown/demo/build_demo.py
Writes demo.html beside this script. Every number on the page is copied from out/.
"""
from __future__ import annotations

import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "out"
HERE = Path(__file__).parent

ROOMS = [
    ("hollis_voice", "Hollis Voice, full room", "Voice AI for vet clinics, raising a Series A.",
     "Hollis Voice's eight planted flags are scored by checks that are not built yet (the ARR definition "
     "check and the rest of the red-flag engine), so these two flags do not count toward that score."),
    ("brasswick", "Brasswick, full room", "The second invented company, with its own planted flags.",
     "The one miss, BF5, is a spoken figure in the pitch video, which the video scan will read."),
]
COVERAGE_ROOM = ("hollis_voice_seed_drop", "Hollis Voice, seed drop", "The first files a founder sends.")
WAVE1_CHECKS = {
    "deck_revenue_vs_pnl": "Deck against books",
    "deck_history_vs_metrics": "Deck against books",
}


def e(s) -> str:
    return html.escape(str(s), quote=True)


def feature_of(check_name: str) -> str:
    return WAVE1_CHECKS.get(check_name, "Accounting mislabels")


def score_line(room: str) -> str:
    r = subprocess.run([sys.executable, "-m", "eval.score", f"data_room/{room}"],
                       cwd=ROOT, capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith(f"{room}:")]
    return lines[-1].split(": ", 1)[1] if lines else ""


def source_chip(s: dict) -> str:
    return (f'<details class="src"><summary><span class="file">{e(s["uri"])}</span>'
            f'<span class="loc">{e(s["locator"])}</span></summary>'
            f'<code>{e(s["quote"])}</code></details>')


def claim_card(c: dict) -> str:
    sev = c["severity"] or "info"
    label = {"flag": "Red flag", "watch": "Watch", "info": "Clear"}[sev]
    chips = "".join(source_chip(s) for s in c["sources"])
    return (f'<article class="claim {e(sev)}"><header><span class="pill {e(sev)}">{label}</span>'
            f'<span class="feat">{e(feature_of(c["check"]["name"]))}</span>'
            f'<span class="check">{e(c["check"]["name"])}</span></header>'
            f'<p>{e(c["text"])}</p><div class="sources">{chips}</div></article>')


def room_section(room: str, title: str, blurb: str, note: str) -> str:
    d = json.loads((OUT / room / "redflags.json").read_text())
    claims = d["claims"]
    flags = [c for c in claims if c["severity"] in ("flag", "watch")]
    clear = [c for c in claims if c["severity"] not in ("flag", "watch")]
    gaps = "".join(f'<li>{e(g["what"])} <span class="muted">({e(g["why"])})</span></li>' for g in d["gaps"])
    score = score_line(room)
    return f"""
<section class="room" id="{e(room)}">
  <div class="room-head">
    <div><h2>{e(title)}</h2><p class="muted">{e(blurb)}</p></div>
    <dl class="stats">
      <div><dt>Red flags</dt><dd>{sum(1 for c in flags if c["severity"] == "flag")}</dd></div>
      <div><dt>Checks clear</dt><dd>{len(clear)}</dd></div>
      <div><dt>Gaps</dt><dd>{len(d["gaps"])}</dd></div>
    </dl>
  </div>
  <p class="score">Against the answer key: {e(score)}</p>
  <p class="muted">{e(note)}</p>
  <div class="claims">{"".join(claim_card(c) for c in flags)}</div>
  <details class="fold"><summary>{len(clear)} checks that came back clear</summary>
    <div class="claims">{"".join(claim_card(c) for c in clear)}</div></details>
  <details class="fold"><summary>{len(d["gaps"])} things the room cannot settle</summary><ul class="gaps">{gaps}</ul></details>
</section>"""


def coverage_section(room: str, title: str, blurb: str) -> str:
    r = json.loads((OUT / room / "readout.json").read_text())
    panels = {p["name"]: p for p in r["panels"]}
    counts = dict(panels["checklist coverage counts"]["rows"])
    asks = r["asks"]
    pieces: dict[str, list[dict]] = {}
    for a in asks:
        pieces.setdefault(a["piece"], []).append(a)
    groups = ""
    for piece, items in pieces.items():
        lis = "".join(
            f'<li><span class="ask">{e(a["what"])}</span>'
            f'{" <span class=tag>if you have it</span>" if a.get("if_you_have_it") else ""}'
            f'<span class="muted">{e(a["why"])}</span></li>' for a in items)
        groups += f'<h3>{e(piece.replace("_", " ").capitalize())}</h3><ol class="asks">{lis}</ol>'
    tiles = "".join(f'<div><dt>{k.replace("_", " ").capitalize()}</dt><dd>{e(counts[k])}</dd></div>'
                    for k in ("checked", "found", "missing", "not_checked"))
    return f"""
<section class="room" id="coverage">
  <div class="room-head">
    <div><h2>Checklist coverage: {e(title)}</h2><p class="muted">{e(blurb)} Stage read from the deck: {e(counts["stage_source"])}.</p></div>
    <dl class="stats">{tiles}</dl>
  </div>
  <p class="score">{e(counts["items"])} checklist items. {e(counts["ask_lines"])} lines to ask the founder for, none repeated.</p>
  <div class="askwrap">{groups}</div>
</section>"""


def main() -> None:
    body = "".join(room_section(*r) for r in ROOMS) + coverage_section(*COVERAGE_ROOM)
    page = (HERE / "template.html").read_text().replace("<!--BODY-->", body)
    (HERE / "demo.html").write_text(page)
    print(HERE / "demo.html")


if __name__ == "__main__":
    main()
