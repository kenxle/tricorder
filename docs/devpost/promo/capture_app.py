"""Captures the real prototype screens for the promo, on Sazabi. Steps follow docs/devpost/shoot_gallery.py.

Serve the prototype first:  python3 -m http.server 8766 --directory docs/features/20261024.02_first_steps_ui/prototype
Run:                        python3 capture_app.py <out dir outside the repo> [dark|light]
Writes PNGs at 1600x900 (device scale 2) plus full-page PNGs, and positions.json with the y of the
elements the promo scrolls to.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8766/index.html"
URL = "https://www.sazabi.com/"
W, H = 1600, 900
OUT = Path(sys.argv[1]).resolve()
SCHEME = sys.argv[2] if len(sys.argv) > 2 else "dark"
OUT.mkdir(parents=True, exist_ok=True)
pos = {}
errors = []


def shot(pg, name, full=False):
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(OUT / f"{name}.png"), full_page=full)
    print("shot", name)


def y_of(pg, sel, nth=0):
    return pg.locator(sel).nth(nth).evaluate("el => el.getBoundingClientRect().top + window.scrollY")


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=2, color_scheme=SCHEME)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith("http://localhost:") else r.abort())

        # Shot 4: the start page, the URL typed in a few characters at a time.
        pg.goto(BASE)
        pg.wait_for_selector("#url")
        steps = list(range(0, len(URL) + 1, 2))
        if steps[-1] != len(URL):
            steps.append(len(URL))
        for i, n in enumerate(steps):
            pg.fill("#url", URL[:n])
            pg.wait_for_timeout(60)
            pg.screenshot(path=str(OUT / f"s4_type_{i:02d}.png"))
        pos["s4_type_count"] = len(steps)
        print("typed", len(steps))

        # Shot 5: the first readout, then the evidence tip.
        pg.click("button[type=submit]")
        pg.wait_for_function("document.getElementById('overall') && document.getElementById('overall').textContent.startsWith('Research done')", timeout=60000)
        pg.evaluate("window.scrollTo(0, 0)")
        shot(pg, "s5_readout")
        shot(pg, "s5_readout_full", full=True)
        ref = pg.locator(".insights .ev-ref").first
        ref.evaluate("el => el.scrollIntoView({block: 'center'})")
        ref.hover()
        pg.wait_for_selector(".ev-tip")
        shot(pg, "s5_evidence")
        pg.mouse.move(5, 5)

        # Shot 6: the data-room request dialog with the draft email.
        pg.click("#to-request")
        pg.wait_for_selector("dialog#req-modal[open] #d-body")
        pg.fill("#d-sender", "Ken St. Clair")
        shot(pg, "s6_request")
        pg.click("#mark-sent")
        pg.wait_for_selector("#open-room", timeout=15000)

        # Shot 7: the room, partly in then full; flags lead. Then a flag drilled down.
        pg.click("#open-room")
        pg.wait_for_selector(".x-roomview[data-room-state='partial']")
        pg.wait_for_selector("#open-more", timeout=15000)
        pg.click("#open-more")
        pg.wait_for_selector(".x-roomview[data-room-state='full']")
        pg.evaluate("window.scrollTo(0, 0)")
        shot(pg, "s7_room_full")
        shot(pg, "s7_room_full_page", full=True)
        pos["s7_page_height"] = pg.evaluate("document.documentElement.scrollHeight")
        try:
            pos["s7_red_flag_y"] = pg.locator("text=Red flag").first.evaluate(
                "el => el.closest('article, section, .tc-card, .tc-panel, div').getBoundingClientRect().top + window.scrollY")
        except Exception as e:
            errors.append("red flag y: " + str(e))
        pg.click("a[href='#flags']")
        pg.wait_for_selector(".x-drill")
        pg.locator(".x-drill").first.evaluate("el => el.scrollIntoView({block: 'start'})")
        pg.evaluate("window.scrollBy(0, -24)")
        shot(pg, "s7_drill")

        # Shot 8: the memo, then the partner's chat with one answered question.
        pg.click("#to-steer")
        pg.wait_for_selector(".x-piece")
        pg.click("#to-memo")
        pg.wait_for_selector(".x-memo")
        pg.select_option("#op-rec", "Invest")
        pg.evaluate("window.scrollTo(0, 0)")
        shot(pg, "s8_memo")
        pg.click("#send-memo")
        pg.wait_for_selector(".x-chat")
        pg.evaluate("window.scrollTo(0, 0)")
        shot(pg, "s8_partner_top")
        sug = pg.locator("[data-suggest]")
        sug.nth(min(2, sug.count() - 1)).click()
        pg.wait_for_selector(".x-msg--memo")
        pg.locator(".x-msg--memo").first.evaluate("el => el.scrollIntoView({block: 'center'})")
        shot(pg, "s8_partner_chat")
        b.close()
    (OUT / "positions.json").write_text(json.dumps(pos, indent=1))
    print("positions", pos)
    if errors:
        print("ERRORS", errors)
        sys.exit(1)


if __name__ == "__main__":
    main()
