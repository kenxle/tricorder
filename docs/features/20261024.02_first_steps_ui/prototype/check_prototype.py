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

    def walk(cfg):
        # Step 1: URL entry
        pg.goto(BASE)
        check(pg.locator("#url").is_visible() and pg.locator("#url").get_attribute("placeholder") == "https://www.sazabi.com/" and pg.locator(".start h2").inner_text() == "Diligence on whom?", "step 1 asks Diligence on whom? with a Sazabi placeholder")
        pg.screenshot(path=str(SHOTS / "1_company_url.png"), full_page=True)

        # Step 2: Ploy readout, streaming
        pg.fill("#url", cfg["host"])
        pg.evaluate("window.__maxSkel = 0; new MutationObserver(() => { window.__maxSkel = Math.max(window.__maxSkel, document.querySelectorAll('.loading > .skel').length); }).observe(document.body, {childList: true, subtree: true, attributes: true})")
        pg.click("button[type=submit]")
        pg.wait_for_selector("#co-name")
        pg.wait_for_function("window.__maxSkel > 0", polling="raf")
        check("company=" in pg.url and cfg["slug"] in pg.url.lower(), "address bar carries ?company=")
        check(pg.locator("#co-name").inner_text() == cfg["name"] and pg.locator(".about").count() == 1, f"{cfg['name']} resolves, with its about paragraph and no setup fields")
        blocks = pg.locator(".insights, .section, #roomgaps").count()
        skels = pg.evaluate("window.__maxSkel")
        check(blocks >= 5 and skels == blocks, f"skeletons show first ({skels} of {blocks} sections showed a skeleton at once)")
        check(pg.locator(".loading .claim:visible").count() == 0, "a loading section shows no claims, only its skeleton")
        pg.wait_for_function("document.getElementById('overall').textContent.startsWith('Research done')", timeout=60000)
        pg.wait_for_timeout(300)
        check(pg.locator(".loading").count() == 0 and pg.locator(".skel").count() == 0, "every skeleton is gone when research is done")
        check(pg.locator(".section .claim:visible").count() > 5 and pg.locator(".insights:visible").count() == 1 and pg.locator("#roomgaps li:visible").count() > 0,
              "every section filled in whole")
        check(pg.locator(".steps, .back, .stepbar, .step-bar").count() == 0, "no step bar or back links")
        check("prototype" not in pg.locator("body").inner_text().lower(), "no Prototype label on the readout")
        chips = pg.locator(".claims .srcchip")
        check(chips.count() > 5, f"source chips present ({chips.count()})")
        pg.locator(".section[aria-label='The outside world'] .srcchip").nth(2).click()
        panel = pg.locator(".panel").first
        check(panel.is_visible() and "Saved copy" in panel.inner_text(), "a source chip opens its panel")
        href = panel.locator("a", has_text="Open the saved copy").get_attribute("href")
        r = pg.request.get("http://localhost:8766/" + href)
        check(r.ok and len(r.text()) > 100, f"saved copy {href} opens")
        check("linkedin" not in pg.content().lower(), "no LinkedIn on the readout")
        pg.screenshot(path=str(SHOTS / f"2_first_readout_{cfg['slug']}.png"), full_page=True)

        # Step 3: the data-room request is a dialog over the working page
        check(pg.locator("#roomgaps #to-request").count() == 1 and pg.locator("#roomgaps h2").inner_text() == "Up Next: Data Room Requests", "the Draft button sits inside the Up Next box")
        pg.click("#to-request")
        pg.wait_for_selector("dialog#req-modal[open] #d-body")
        check(pg.evaluate("document.querySelector('#req-modal').contains(document.activeElement) || document.activeElement === document.querySelector('#req-modal')"), "focus moves into the dialog")
        for _ in range(40):
            pg.keyboard.press("Tab")
        check(pg.evaluate("document.querySelector('#req-modal').contains(document.activeElement)"), "focus stays trapped inside the dialog after 40 tabs")
        pg.keyboard.press("Escape")
        check(pg.locator("dialog#req-modal[open]").count() == 0, "Esc closes the dialog")
        check(pg.evaluate("document.activeElement.id") == "to-request", "focus returns to the Draft button")
        pg.click("#to-request")
        pg.wait_for_selector("dialog#req-modal[open] #req-close")
        pg.click("#req-close")
        check(pg.locator("dialog#req-modal[open]").count() == 0 and pg.evaluate("document.activeElement.id") == "to-request", "the Close button closes the dialog and returns focus")
        pg.click("#to-request")
        pg.wait_for_selector("dialog#req-modal[open] #d-body")
        body0 = pg.locator("#d-body").input_value()
        check(f"Hi {cfg['first']}," in body0, "draft greets the founder")
        first_cb = pg.locator("#asks input[type=checkbox]").first
        first_cb.uncheck()
        body1 = pg.locator("#d-body").input_value()
        check(body1 != body0, "unchecking an item changes the draft")
        first_cb.check()
        pg.fill("#addtext", "your SOC 2 report")
        pg.click("#addform button")
        body2 = pg.locator("#d-body").input_value()
        check("Please send your SOC 2 report." in body2, "an added item reaches the draft")
        check(pg.locator("dialog .guidance, dialog details").count() > 0, "guidance is in the dialog")
        check("prototype" not in pg.locator("body").inner_text().lower() and pg.locator(".steps, .back").count() == 0, "no Prototype label, step bar or back links with the dialog open")
        check(pg.locator("dialog .banner").first.inner_text().startswith("For the demo, the data room"), "dialog labels the room synthetic")
        pg.screenshot(path=str(SHOTS / f"3_data_room_request_{cfg['slug']}.png"))
        pg.click("#mark-sent")

        # Step 4: the working page lists the requests, then the room arrives
        check(pg.locator("dialog#req-modal[open]").count() == 0, "Mark as sent closes the dialog")
        asked = pg.evaluate("TC.S.items.filter(i => i.checked).length")
        check(pg.locator(".req[data-state='open']").count() == asked and pg.locator(".req[data-state='answered']").count() == 0 and asked > 0, f"every requested item shows as Open ({asked})")
        check("Asked" in pg.locator(".req").first.inner_text() and f"Request sent to {cfg['founder']}" in pg.locator("#req-note").inner_text() and f"waiting for {cfg['name']}'s data room" in pg.locator("#req-note").inner_text(),
              "each item shows when it was asked, and the page says the request went to the founder")
        pg.wait_for_selector("#open-room", timeout=10000)
        note = pg.locator(".notice").inner_text()
        first = pg.evaluate("TC.S.research.room.states.partial.arrived.length")
        total = pg.evaluate("TC.S.research.room.states.full.files_total")
        check(f"{cfg['name']} shared its data room" in note and f"{first} files" in note and "just now" in note, f"first notification counts the files that arrived ({first} of {total})")
        pg.screenshot(path=str(SHOTS / f"4a_requests_open_notification_{cfg['slug']}.png"), full_page=True)
        pg.click("#open-room")
        pg.wait_for_selector(".x-roomview[data-room-state='partial']")
        ans = lambda st: pg.evaluate(f"TC.S.items.filter(i => i.checked && i.id && TC.S.research.room.states.{st}.answered.includes(i.id)).length")
        exp_partial = ans("partial")
        got = pg.locator(".x-roomview .req[data-state='answered']").count()
        check(got == exp_partial and 0 < got < asked and pg.locator(".x-roomview .req[data-state='open']").count() == asked - got,
              f"opening the room shows the partial view ({got} answered, {asked - got} open)")
        check(pg.locator(".x-roomview .req[data-state='answered'] .roomchip").count() >= got, "each answered item names the file that answered it")
        check("synthetic" in pg.locator("#notify .banner").inner_text(), "the partial room is labelled synthetic")
        pg.wait_for_selector("#open-more", timeout=10000)
        more = pg.locator("#notify .notice").inner_text()
        check(f"{cfg['name']} added {total - first} more files" in more and "just now" in more, f"second notification: {total - first} more files")
        pg.screenshot(path=str(SHOTS / f"4_room_received_{cfg['slug']}.png"), full_page=True)
        pg.click("#open-more")
        pg.wait_for_selector(".x-roomview[data-room-state='full']")
        answered = pg.locator(".x-roomview .req[data-state='answered']").count()
        check(answered == ans("full") and answered > got and pg.locator("#open-more").count() == 0, f"the full view answers more ({answered} answered, {asked - answered} still open: nothing in the room settles them)")
        check(pg.locator("a[href='http://localhost:5173/']").count() == 1, "the working page links to the built app")
        check("prototype" not in pg.locator("body").inner_text().lower() and "simulate" not in pg.locator("body").inner_text().lower() and pg.locator(".steps, .back").count() == 0, "no Prototype label, step bar or back links on the working page")
        # A founder question from a flag card: on the request, in the requests box as Open, and TC_OPEN_REQUEST shows it
        if pg.locator(".x-roomview [data-ask]:not([disabled])").count() == 0:
            return
        pg.locator(".x-roomview [data-ask]:not([disabled])").first.click()
        qkey = pg.evaluate("TC.S.items.find(i => i.key.startsWith('ask-')).key")
        check(pg.locator(".x-roomview .req[data-state='open']").filter(has_text="Question:").count() == 1, "a founder question appears in the Data room requests box as Open")
        pg.evaluate(f"TC_OPEN_REQUEST('{qkey}')")
        pg.wait_for_selector("dialog#req-modal[open] #ask-group")
        check("Questions for the founder" in pg.locator("#ask-group").inner_text() and pg.locator("dialog li.ask.flash").count() == 1 and pg.locator("dialog li.ask.flash").get_attribute("data-key") == qkey,
              "TC_OPEN_REQUEST opens the dialog on the question, under Questions for the founder, highlighted")
        check(pg.locator("dialog li.ask.flash").is_visible(), "the highlighted question is scrolled into view")
        pg.keyboard.press("Escape")
        pg.evaluate("TC_OPEN_REQUEST()")
        check(pg.locator("dialog#req-modal[open]").count() == 1 and pg.locator("dialog li.ask.flash").count() == 0, "TC_OPEN_REQUEST with no id just opens the dialog")
        pg.click("#req-close")
        pg.screenshot(path=str(SHOTS / f"4b_room_full_{cfg['slug']}.png"), full_page=True)

        if cfg["slug"] != "ploy":
            return
        # Step 5: flags from Ploy's synthetic room (steps 5 to 8: step5.js, step6.js, memo.js)
        pg.click("a[href='#flags']")
        pg.wait_for_selector(".x-drill")
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
        pg.locator(".x-smallflag .srcchip").first.click()
        check("Saved copy" in pg.locator(".x-smallflag .panel").first.inner_text(), "an outside source chip opens the saved public page")
        held, missing = pg.locator(".x-tick[data-held='yes']").count(), pg.locator(".x-tick[data-held='no']").count()
        check(held > 0 and missing > 0 and held == answered and missing == asked + 1 - answered, f"request ticked off: {held} in the room, {missing} still missing, same as the working page")
        check(pg.locator(".x-pre tr[data-status='confirms']").count() >= 3 and "26,571,989" in pg.locator(".x-pre").inner_text(),
              "first-readout claims confirmed by the room, the Form D amount among them")
        pg.locator("[data-ask]").first.click()
        check(pg.locator(".tc-ask [data-viewreq]").count() >= 2, "a second founder question goes onto the request, and each offers View in the request")
        small = pg.locator(".x-smallflag").count()
        after = pg.evaluate("""(() => { const reds = [...document.querySelectorAll(".x-flag[data-flag='red']")]; const s = document.querySelector(".x-smallflag");
          return !!s && reds.length > 0 && !!(reds[reds.length - 1].compareDocumentPosition(s) & Node.DOCUMENT_POSITION_FOLLOWING); })()""")
        check(small >= 1 and after and pg.locator(".x-flag", has_text="matches the SEC Form D").count() == 0,
              f"sources that agree are small green flags, listed after the red flags ({small})")
        check(pg.locator(".x-flag .x-why").count() == pg.locator(".x-flag").count(), "every big flag says in a line or two why it matters")
        check(pg.locator(".x-flag[data-flag='red']", has_text="disagree on how many companies").count() == 1,
              "sources that disagree are a big red flag with stated beside found")
        pg.locator(".x-flag .roomchip").first.click()
        pg.locator(".x-smallflag .srcchip").first.click()
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
        check(pg.locator(".x-piece[data-piece='market'] .tc-mark--weak").count() == 1, "the steered piece keeps the script's verdict")
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


    walk(dict(slug="sazabi", host="https://www.sazabi.com/", name="Sazabi", founder="Sherwood Callaway", first="Sherwood"))
    walk(dict(slug="ploy", host="ploy.ai", name="Ploy", founder="Bryant Chou", first="Bryant"))

    # The working page with the room's data in, by URL: partial, then full (room_view.js)
    for state in ("partial", "full"):
        pg.goto(BASE + f"?company=https://ploy.ai&room={state}")
        pg.wait_for_selector(f".x-roomview[data-room-state='{state}']")
        answered, still = pg.locator("[data-request='answered']").count(), pg.locator("[data-request='open']").count()
        flags, waiting = pg.locator(".x-roomview .x-flag").count(), pg.locator(".x-roomview .x-waiting").count()
        check(flags >= 2 and pg.locator("section[aria-label='What stands out'] .x-flag").count() == flags, f"{state}: what stands out leads with the room's flags ({flags})")
        check(pg.locator(".x-roomview .tc-verdict").count() == 10, f"{state}: ten pieces carry the room's verdicts")
        check(pg.locator(".x-roomsays .tc-mark--strong").count() >= 3, f"{state}: pre-room claims show as confirmed by the room")
        if state == "partial":
            check(waiting >= 1 and pg.locator(".x-waiting .tc-mark--running").count() >= 1, f"partial: checks waiting on a file show their open request ({waiting})")
            check(pg.locator(".tc-verdict .tc-mark--thin", has_text="not enough yet").count() >= 1, "partial: pieces that need the rest say not enough yet")
            part = answered
        else:
            check(waiting == 0 and answered > part, f"full: nothing waits on a file, and more requests are answered ({part} then {answered})")
        check("synthetic" in pg.locator(".x-roomview .x-synthetic").inner_text(), f"{state}: the room is labelled synthetic")
        pg.screenshot(path=str(SHOTS / f"room_{state}.png"), full_page=True)
    pg.click("[data-room-go='steer']")
    pg.wait_for_selector(".x-piece")
    check(pg.locator(".x-piece").count() == 10, "steering works from the full room")

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
    for state in ("partial", "full"):
        pg.goto(BASE + f"?company=https://ploy.ai&room={state}")
        pg.wait_for_selector(".x-roomview")
        sw = pg.evaluate("document.documentElement.scrollWidth")
        check(sw <= 390, f"no sideways scroll at phone width on the {state} room ({sw}px)")
    pg.goto(BASE + "?company=ploy.ai&pace=0")
    pg.wait_for_timeout(300)
    for step in ("flags", "steer", "memo", "principal"):
        pg.evaluate(f"location.hash = '{step}'")
        pg.wait_for_timeout(200)
        sw = pg.evaluate("document.documentElement.scrollWidth")
        check(sw <= 390, f"no sideways scroll at phone width on {step} ({sw}px)")
    b.close()

print("console errors:", errors or "none")
sys.exit(1 if failed or errors else 0)
