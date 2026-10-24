"""Headless check of the piece analyses (piece_reports.js) in the completed data room view, for Ploy and Sazabi.

Serves this folder itself on port 8767. If index.html does not load the piece analyses yet, the check adds the two
script tags and inserts TC_PIECE_REPORTS.html(state) where room_view.js would, so it runs before and after the wiring.

Run: python3 check_piece_reports.py
"""
import functools
import http.server
import json
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PORT = 8767
BASE = f"http://localhost:{PORT}/index.html"
SHOTS = HERE / "shots"
COMPANIES = [("ploy", "https://ploy.ai"), ("sazabi", "https://www.sazabi.com/")]


def expected() -> dict:
    text = (HERE / "piece_reports_data.js").read_text()
    return json.loads(re.search(r"=\s*(\{.*\});\s*$", text, re.S).group(1))


def check_piece_reports(pg, check, errors) -> None:
    """The completed room shows every piece's analysis, each chart draws, and nothing logs an error."""
    data = expected()
    for slug, company in COMPANIES:
        reps = data[slug]
        for state in ("full", "partial"):
            pg.goto(f"{BASE}?company={company}&room={state}")
            pg.wait_for_selector(".x-roomview")
            wired = pg.evaluate("!!window.TC_PIECE_REPORTS") and pg.locator("[data-piece-report]").count() > 0
            print(f"INFO {slug} {state}: " + ("index.html and room_view.js load the analyses" if wired else "not wired yet; the check inserts them"))
            if not pg.evaluate("!!window.TC_PIECE_REPORTS"):
                pg.add_script_tag(url="piece_reports_data.js")
                pg.add_script_tag(url="piece_reports.js")
                pg.wait_for_function("!!window.TC_PIECE_REPORTS")
            if pg.locator("[data-piece-report]").count() == 0:
                pg.evaluate("""(st) => {
                    const at = document.querySelector('.x-analyses') || document.querySelector('.x-roomview');
                    at.insertAdjacentHTML('beforeend', TC_PIECE_REPORTS.html(st));
                }""", state)
            shown = pg.locator("[data-piece-report]")
            check(shown.count() == len(reps), f"{slug} {state}: {shown.count()} of {len(reps)} piece analyses show")
            if state == "partial":
                continue
            pg.wait_for_function("[...document.querySelectorAll('[data-piece-chart]')].every(e => e.querySelector('.main-svg'))", timeout=15000)
            for rep in reps:
                sec = pg.locator(f"[data-piece-report='{rep['piece']}']")
                txt = sec.inner_text()
                check(rep["knowledge"] in txt and "built from expert knowledge" in txt.lower() and "kimmy" not in txt.lower(),
                      f"{slug} {rep['piece']}: labelled with {rep['knowledge']}")
                check(sec.locator(".x-chart .main-svg").count() >= 1, f"{slug} {rep['piece']}: its chart draws")
                check(sec.locator(".x-report-body > p").count() == len(rep["paras"]) and sec.locator(".x-asks li").count() == len(rep["asks"]),
                      f"{slug} {rep['piece']}: {len(rep['paras'])} paragraphs and {len(rep['asks'])} things to ask")
                n_refs = len({r for p in rep["paras"] for r in p["refs"]})
                check(sec.locator(".x-prev").count() >= n_refs and (n_refs == 0 or sec.locator(".x-evlist li").count() == n_refs),
                      f"{slug} {rep['piece']}: {n_refs} numbered evidence rows with sources")
                key = f"report:{rep['piece']}"
                tog = sec.locator(f".memo-pick[data-memo='{key}']")
                check(tog.count() == 1, f"{slug} {rep['piece']}: In memo toggle keyed {key}")
                before = pg.evaluate("(k) => TC_MEMO.get(k)", key)
                tog.click()
                check(pg.evaluate("(k) => TC_MEMO.get(k)", key) is (not before), f"{slug} {rep['piece']}: the toggle flips {key}")
                tog.click()
            check(pg.locator(".x-report").count() == 2, f"{slug}: Kimmy's two reports still count two (.x-report)")
            first = pg.locator("[data-piece-report] .x-prev").first
            first.hover()
            check(pg.locator(".ev-tip").count() == 1 and "Source:" in pg.locator(".ev-tip").inner_text(), f"{slug}: hovering an evidence number shows the fact and its source")
            first.click()
            check(pg.locator("[data-piece-report] .x-report-ev[open]").count() == 1, f"{slug}: clicking an evidence number opens the evidence list")
            r = pg.request.get(f"http://localhost:{PORT}/{reps[0]['knowledge']}")
            check(r.ok and "expert knowledge" in r.text(), f"{slug}: the knowledge file link opens")
            pg.locator("[data-piece-report]").first.scroll_into_view_if_needed()
            pg.screenshot(path=str(SHOTS / f"piece_reports_{slug}.png"), full_page=True)
    # Phone width: no sideways scroll with the analyses in.
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.goto(f"{BASE}?company=https://www.sazabi.com/&room=full")
    pg.wait_for_selector(".x-roomview")
    if not pg.evaluate("!!window.TC_PIECE_REPORTS"):
        pg.add_script_tag(url="piece_reports_data.js")
        pg.add_script_tag(url="piece_reports.js")
        pg.wait_for_function("!!window.TC_PIECE_REPORTS")
    if pg.locator("[data-piece-report]").count() == 0:
        pg.evaluate("document.querySelector('.x-analyses').insertAdjacentHTML('beforeend', TC_PIECE_REPORTS.html('full'))")
    pg.wait_for_function("[...document.querySelectorAll('[data-piece-chart]')].every(e => e.querySelector('.main-svg'))", timeout=15000)
    sw = pg.evaluate("document.documentElement.scrollWidth")
    check(sw <= 390, f"no sideways scroll at phone width with the analyses in ({sw}px)")
    pg.set_viewport_size({"width": 1280, "height": 900})


def main() -> int:
    SHOTS.mkdir(exist_ok=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(HERE))
    srv = http.server.ThreadingHTTPServer(("localhost", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    errors, failed = [], []

    def check(ok, what):
        print(("PASS " if ok else "FAIL ") + what)
        if not ok:
            failed.append(what)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("requestfailed", lambda r: errors.append("request failed: " + r.url))
        check_piece_reports(pg, check, errors)
        b.close()
    srv.shutdown()
    print("console errors:", errors or "none")
    return 1 if failed or errors else 0


if __name__ == "__main__":
    sys.exit(main())
