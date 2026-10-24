"""Headless check of the first-steps prototype. Saves one screenshot per step in shots/. Serve this folder first: python3 -m http.server 8766 --directory <this folder>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8766/index.html"
SHOTS = Path("/Users/kennethstclair/Documents/workspace/tricorder/docs/features/20261024.02_first_steps_ui/prototype/shots")
SHOTS.mkdir(exist_ok=True)
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
    pg.route("**/*", lambda route: route.continue_() if route.request.url.startswith("http://localhost:8766") else (errors.append("external request: " + route.request.url), route.abort()))

    # Step 1: URL entry
    pg.goto(BASE)
    check(pg.locator("#url").is_visible(), "step 1 shows the URL input")
    pg.screenshot(path=str(SHOTS / "1_company_url.png"), full_page=True)

    # Step 2: Ploy readout, streaming
    pg.fill("#url", "ploy.ai")
    pg.click("button[type=submit]")
    pg.wait_for_selector("#co-name")
    check("company=ploy.ai" in pg.url, "address bar carries ?company=")
    check(pg.locator("#co-name").inner_text() == "Ploy" and pg.locator(".about").count() == 1, "Ploy resolves, with its about paragraph and no setup fields")
    pg.wait_for_timeout(1500)
    early = pg.locator(".claim.wait").count()
    check(early > 0, f"claims arrive over time ({early} still waiting after 1.5s)")
    pg.wait_for_function("document.getElementById('overall').textContent.startsWith('Research done')", timeout=60000)
    pg.wait_for_timeout(600)
    check(pg.locator(".claim.wait").count() == 0, "all claims shown when research is done")
    chips = pg.locator(".claims .srcchip")
    check(chips.count() > 20, f"source chips present ({chips.count()})")
    pg.locator(".section[aria-label='The outside world'] .srcchip").nth(5).click()
    panel = pg.locator(".panel").first
    check(panel.is_visible() and "Saved copy" in panel.inner_text(), "a source chip opens its panel")
    href = panel.locator("a", has_text="Open the saved copy").get_attribute("href")
    r = pg.request.get("http://localhost:8766/" + href)
    check(r.ok and len(r.text()) > 100, f"saved copy {href} opens")
    check("linkedin" not in pg.content().lower(), "no LinkedIn on the readout")
    pg.screenshot(path=str(SHOTS / "2_first_readout_ploy.png"), full_page=True)

    # Step 3: request
    pg.click("#to-request")
    pg.wait_for_selector("#d-body")
    body0 = pg.locator("#d-body").input_value()
    check("Hi Bryant," in body0, "draft greets the founder")
    first_cb = pg.locator("#asks input[type=checkbox]").first
    first_cb.uncheck()
    body1 = pg.locator("#d-body").input_value()
    check(body1 != body0, "unchecking an item changes the draft")
    first_cb.check()
    pg.fill("#addtext", "your SOC 2 report")
    pg.click("#addform button")
    body2 = pg.locator("#d-body").input_value()
    check("Please send your SOC 2 report." in body2, "an added item reaches the draft")
    check(pg.locator(".banner").first.inner_text().startswith("For the demo, the data room"), "request labels the room synthetic")
    pg.screenshot(path=str(SHOTS / "3_data_room_request_ploy.png"), full_page=True)

    # Step 4: received
    pg.click("#to-received")
    pg.wait_for_selector("text=data room received")
    check(pg.locator("a[href='http://localhost:5173/']").count() == 1, "received step links to the app")
    check("synthetic" in pg.locator(".banner").inner_text(), "received step labels the room synthetic")
    pg.screenshot(path=str(SHOTS / "4_room_received.png"), full_page=True)

    # Sazabi by YC URL in the address bar, all at once for the shot
    pg.goto(BASE + "?company=https://www.ycombinator.com/companies/sazabi&pace=0")
    pg.wait_for_function("document.getElementById('overall') && document.getElementById('overall').textContent.startsWith('Research done')")
    check(pg.locator("#co-name").inner_text() == "Sazabi", "address-bar YC URL resolves Sazabi")
    pg.screenshot(path=str(SHOTS / "2b_first_readout_sazabi.png"), full_page=True)

    # A company in the list without cached research, and an unknown URL
    pg.goto(BASE + "?company=https://tester.army")
    pg.wait_for_selector(".empty")
    check(pg.locator("#f-name").input_value() == "TesterArmy", "list company resolves without research")
    pg.screenshot(path=str(SHOTS / "2c_not_cached.png"), full_page=True)
    pg.goto(BASE + "?company=https://example.com/about")
    pg.wait_for_selector(".empty")
    check(pg.locator("#f-name").input_value() == "", "unknown URL leaves the name blank")
    check("not in the saved" in pg.locator(".setup").inner_text(), "unknown URL says it is not in the list")

    # Phone width: no sideways scroll
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.goto(BASE + "?company=ploy.ai&pace=0")
    pg.wait_for_function("document.getElementById('overall').textContent.startsWith('Research done')")
    sw = pg.evaluate("document.documentElement.scrollWidth")
    check(sw <= 390, f"no sideways scroll at phone width ({sw}px)")
    b.close()

print("console errors:", errors or "none")
sys.exit(1 if failed or errors else 0)
