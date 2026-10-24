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
    pg.evaluate("window.__maxSkel = 0; new MutationObserver(() => { window.__maxSkel = Math.max(window.__maxSkel, document.querySelectorAll('.loading > .skel').length); }).observe(document.body, {childList: true, subtree: true, attributes: true})")
    pg.click("button[type=submit]")
    pg.wait_for_selector("#co-name")
    pg.wait_for_function("window.__maxSkel > 0", polling="raf")
    check("company=ploy.ai" in pg.url, "address bar carries ?company=")
    check(pg.locator("#co-name").inner_text() == "Ploy" and pg.locator(".about").count() == 1, "Ploy resolves, with its about paragraph and no setup fields")
    blocks = pg.locator(".insights, .section, #roomgaps").count()
    skels = pg.evaluate("window.__maxSkel")
    check(blocks >= 5 and skels == blocks, f"skeletons show first ({skels} of {blocks} sections showed a skeleton at once)")
    check(pg.locator(".loading .claim:visible").count() == 0, "a loading section shows no claims, only its skeleton")
    pg.wait_for_function("document.getElementById('overall').textContent.startsWith('Research done')", timeout=60000)
    pg.wait_for_timeout(300)
    check(pg.locator(".loading").count() == 0 and pg.locator(".skel").count() == 0, "every skeleton is gone when research is done")
    check(pg.locator(".section .claim:visible").count() > 20 and pg.locator(".insights:visible").count() == 1 and pg.locator("#roomgaps li:visible").count() > 0,
          "every section filled in whole")
    check(pg.locator(".steps, .back, .stepbar, .step-bar").count() == 0, "no step bar or back links")
    check("prototype" not in pg.locator("body").inner_text().lower(), "no Prototype label on the readout")
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
    check("prototype" not in pg.locator("body").inner_text().lower() and pg.locator(".steps, .back").count() == 0, "no Prototype label, step bar or back links on the request")
    check(pg.locator(".banner").first.inner_text().startswith("For the demo, the data room"), "request labels the room synthetic")
    pg.screenshot(path=str(SHOTS / "3_data_room_request_ploy.png"), full_page=True)

    # Step 4: received
    pg.click("#to-received")
    pg.wait_for_selector("text=data room received")
    check(pg.locator("a[href='http://localhost:5173/']").count() == 1, "received step links to the app")
    check("prototype" not in pg.locator("body").inner_text().lower() and pg.locator(".steps, .back").count() == 0, "no Prototype label, step bar or back links on room received")
    check("synthetic" in pg.locator(".banner").inner_text(), "received step labels the room synthetic")
    pg.screenshot(path=str(SHOTS / "4_room_received.png"), full_page=True)

    # Step 5: flags from Ploy's synthetic room (steps 5 to 8: step5.js, step6.js, memo.js)
    pg.click("a[href='#flags']")
    pg.wait_for_selector(".x-flag")
    check("Synthetic data room" in pg.locator(".x-synthetic").inner_text(), "step 5 labels the room synthetic")
    greens, reds = pg.locator(".x-flag[data-flag='green']").count(), pg.locator(".x-flag[data-flag='red']").count()
    order = pg.eval_on_selector_all(".x-flag", "els => els.map(e => e.dataset.flag)")
    check(greens >= 1 and reds >= 1 and order == sorted(order, key=lambda k: k != "green"), f"green flags first, then red ({greens} green, {reds} red)")
    check(pg.locator(".x-flag .tc-pair").count() == greens + reds and pg.locator(".x-flag .tc-strip").count() == greens + reds,
          "every flag shows stated beside found and a range strip")
    check(pg.locator(".x-flag[data-flag='red'] .tc-strip-tick.is-out").count() >= reds, "each red flag's stated figure sits outside the band")
    check(pg.locator(".x-verdicts .tc-verdict").count() == 10, "the overview has ten pieces with a verdict")
    check(pg.locator(".x-drill").count() == 2, "two drill-downs, one weak and one strong")
    pg.locator(".x-flag .roomchip").first.click()
    check("synthetic room" in pg.locator(".x-flag .panel").first.inner_text(), "a room source chip opens its synthetic excerpt")
    pg.locator(".x-flag .srcchip").first.click()
    check("Saved copy" in pg.locator(".x-flag .panel").nth(1).inner_text(), "an outside source chip opens the saved public page")
    held, missing = pg.locator(".x-tick[data-held='yes']").count(), pg.locator(".x-tick[data-held='no']").count()
    check(held > 0 and missing > 0, f"request ticked off: {held} in the room, {missing} still missing")
    check(pg.locator(".x-pre tr[data-status='confirms']").count() >= 3 and "26,571,989" in pg.locator(".x-pre").inner_text(),
          "first-readout claims confirmed by the room, the Form D amount among them")
    pg.click("[data-ask]")
    check(pg.locator("[data-ask]").first.is_disabled(), "a founder question goes onto the request")
    pg.locator(".x-flag .roomchip").first.click()
    pg.locator(".x-flag .srcchip").first.click()
    pg.screenshot(path=str(SHOTS / "5_flags_from_the_room.png"), full_page=True)

    # Step 6: steering
    pg.click("#to-steer")
    pg.wait_for_selector(".x-piece")
    pg.click("[data-example='0']")
    check(pg.locator(".x-result[data-kind='figure'] .tc-pair").count() == 1 and "$2,442,000" in pg.locator(".x-result[data-kind='figure']").inner_text(),
          "a figure steer sits beside the check's figure, which stays")
    pg.click("[data-example='1']")
    check(pg.evaluate("TC.S.items.some(i => i.title.startsWith('Model inference invoices'))"), "a more-information steer goes onto the request")
    pg.click("[data-example='2']")
    check(pg.locator(".x-piece.tc-steered").count() == 1 and pg.locator(".x-piece.tc-steered .x-before").count() == 1, "a rewrite marks the piece steered and keeps the before")
    check(pg.locator(".x-piece[data-piece='market'] .tc-mark--mixed").count() == 1, "the steered piece keeps the script's verdict")
    pg.click("[data-lines='team']")
    pg.click("[data-disagree='te-1']")
    pg.fill(".x-steerbox input", "I disagree because two of the 14 are contractors.")
    pg.press(".x-steerbox input", "Enter")
    check(pg.locator(".x-result[data-kind='note']").count() == 1, "disagreeing with a line keeps a note on it")
    pg.screenshot(path=str(SHOTS / "6_steer_the_readout.png"), full_page=True)

    # Step 7: the associate's memo
    pg.click("#to-memo")
    pg.wait_for_selector(".x-memo")
    check(pg.locator(".x-memo-sec").count() >= 10, f"the memo has its sections ({pg.locator('.x-memo-sec').count()})")
    check("v5" in pg.locator(".x-head-facts").inner_text(), "the memo's version counts the four steers")
    pg.select_option("#op-rec", "Invest")
    pg.fill("#op-amount", "$2,000,000, if the pilot comes out of ARR")
    pg.press("#op-amount", "Tab")
    line = pg.locator("[data-mline]").first
    line.click()
    check(pg.locator(".x-mline-claims:not([hidden]) .x-claim").count() >= 1, "one click on a memo line opens its claims")
    pg.locator(".x-mline-claims:not([hidden]) .tc-chip").first.click()
    check(pg.locator(".x-mline-claims:not([hidden]) .panel").count() >= 1, "a second click opens a claim's source")
    pg.screenshot(path=str(SHOTS / "7_make_the_memo.png"), full_page=True)

    # Step 8: the principal's view
    pg.click("#to-principal")
    pg.wait_for_selector(".x-whatif")
    first_sections = pg.eval_on_selector_all("main section[aria-label]", "els => els.slice(0, 2).map(e => e.getAttribute('aria-label'))")
    check(first_sections == ["The round", "The flags"], f"the principal's view opens on the round and the flags ({first_sections})")
    check("Invest" in pg.locator("section[aria-label='The round']").inner_text(), "the associate's recommendation reaches the principal")
    row = lambda: pg.locator(".x-wtable tbody tr").first.inner_text().split("\t")
    check(row()[2] == row()[3], "the what-if starts at Tricorder's rebuilt figures")
    pg.check("#w-pilot")
    check(row()[3] == "$2,802,000" and row()[2] == "$2,442,000", "counting the pilot changes only the scenario column")
    pg.locator("[data-view='agree']").first.click()
    check("1 agree" in pg.locator("#x-yourview").inner_text(), "the principal can agree with a line")
    pg.screenshot(path=str(SHOTS / "8_principals_view.png"), full_page=True)

    # Sazabi, lighter: steps 5 and 8 work
    pg.goto(BASE + "?company=sazabi.com&pace=0")
    pg.evaluate("location.hash = 'flags'")
    pg.wait_for_selector(".x-flag")
    check(pg.locator(".x-verdicts .tc-verdict").count() == 10, "Sazabi's room shows its flags and ten pieces")
    pg.screenshot(path=str(SHOTS / "5b_flags_from_the_room_sazabi.png"), full_page=True)
    pg.evaluate("location.hash = 'principal'")
    pg.wait_for_selector(".x-whatif")
    check(pg.locator("#w-pilot").count() == 0, "Sazabi's what-if has no pilot to count")

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
    for step in ("flags", "steer", "memo", "principal"):
        pg.evaluate(f"location.hash = '{step}'")
        pg.wait_for_timeout(200)
        sw = pg.evaluate("document.documentElement.scrollWidth")
        check(sw <= 390, f"no sideways scroll at phone width on {step} ({sw}px)")
    b.close()

print("console errors:", errors or "none")
sys.exit(1 if failed or errors else 0)
