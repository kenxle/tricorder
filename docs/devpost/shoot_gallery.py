"""Shoots the Devpost image gallery from the running prototype: Sazabi, 1500x1000 (3:2), light theme, viewport shots.

Serve the prototype first:  python3 -m http.server 8766 --directory docs/features/20261024.02_first_steps_ui/prototype
Run:                        python3 docs/devpost/shoot_gallery.py
Writes docs/devpost/gallery/NN_name.png and CAPTIONS.md, then checks every file is under 5 MB and exactly 3:2.
"""
import struct
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "gallery"
OUT.mkdir(exist_ok=True)
BASE = "http://localhost:8766/index.html"
W, H = 1500, 1000
LIMIT = 5 * 1024 * 1024

CAPTIONS = {
    "01_start": "Tricorder opens on one question. Paste a company's website and the research starts.",
    "02_first_readout": "The first readout: what the company does, then What stands out, each point read from public sources only.",
    "03_evidence": "Every point carries numbered evidence. Hover a number to see the fact and its source.",
    "04_data_room_request": "The data-room request is a dialog over the working page. It lists what to ask for, with a draft email the associate sends from their own mail.",
    "05_request_sent": "Once the request goes out, every item shows as open with the time it was asked. The founder's data room arrives as a notification.",
    "06_room_partly_in": "The first files arrive and the working page updates. A red flag from the room leads, with a question to put to the founder.",
    "07_room_in_full": "With the whole room in, Tricorder has read every file. Green and red flags lead, each with the stated figure beside what the room shows.",
    "08_flag_drilled_down": "One piece drilled down: each line from the room with its sources, which ones agree and which disagree, and the figures side by side.",
    "09_steering": "The associate steers the readout in a plain sentence. Here a steer asks for more: it goes onto the data-room request and waits on the founder. A steer never changes a check's own number.",
    "10_memo": "The associate's memo is a document about the company, with the evidence behind each number a click away.",
    "11_partner_review": "The partner reads the memo and asks questions in a chat. Answers come from the memo and link to the paragraph.",
}
errors = []
SHOT = []


def shoot(pg, name):
    pg.wait_for_timeout(350)
    pg.screenshot(path=str(OUT / f"{name}.png"))
    SHOT.append(name)
    print("shot", name)


def into_view(loc, block="start", nudge=0):
    loc.evaluate(f"el => el.scrollIntoView({{block: '{block}'}})")
    if nudge:
        loc.page.evaluate(f"window.scrollBy(0, {nudge})")


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": W, "height": H}, color_scheme="light")
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith("http://localhost:") else r.abort())

        pg.goto(BASE)
        pg.fill("#url", "https://www.sazabi.com/")
        shoot(pg, "01_start")

        pg.click("button[type=submit]")
        pg.wait_for_function("document.getElementById('overall') && document.getElementById('overall').textContent.startsWith('Research done')", timeout=60000)
        pg.evaluate("window.scrollTo(0, 0)")
        shoot(pg, "02_first_readout")

        ref = pg.locator(".insights .ev-ref").first
        into_view(ref, "center")
        ref.hover()
        pg.wait_for_selector(".ev-tip")
        shoot(pg, "03_evidence")
        pg.mouse.move(5, 5)

        pg.click("#to-request")
        pg.wait_for_selector("dialog#req-modal[open] #d-body")
        pg.fill("#d-sender", "Ken St. Clair")
        shoot(pg, "04_data_room_request")
        pg.click("#mark-sent")
        pg.wait_for_selector("#open-room", timeout=15000)
        into_view(pg.locator("#roomgaps"), "start", -150)
        shoot(pg, "05_request_sent")

        pg.click("#open-room")
        pg.wait_for_selector(".x-roomview[data-room-state='partial']")
        pg.evaluate("window.scrollTo(0, 0)")
        shoot(pg, "06_room_partly_in")
        pg.wait_for_selector("#open-more", timeout=15000)
        pg.click("#open-more")
        pg.wait_for_selector(".x-roomview[data-room-state='full']")
        pg.evaluate("window.scrollTo(0, 0)")
        shoot(pg, "07_room_in_full")

        pg.click("a[href='#flags']")
        pg.wait_for_selector(".x-drill")
        into_view(pg.locator(".x-drill").first, "start", -110)
        shoot(pg, "08_flag_drilled_down")

        pg.click("#to-steer")
        pg.wait_for_selector(".x-piece")
        n = pg.locator("[data-example]").count()
        for i in range(min(n, 2)):
            pg.locator("[data-example]").nth(i).click()
        if pg.locator(".x-result").count():
            into_view(pg.locator(".x-result").first, "center")
        shoot(pg, "09_steering")

        pg.click("#to-memo")
        pg.wait_for_selector(".x-memo")
        pg.select_option("#op-rec", "Invest")
        pg.evaluate("window.scrollTo(0, 0)")
        shoot(pg, "10_memo")

        pg.click("#send-memo")
        pg.wait_for_selector(".x-chat")
        sug = pg.locator("[data-suggest]")
        sug.nth(min(2, sug.count() - 1)).click()
        pg.wait_for_selector(".x-msg--memo")
        into_view(pg.locator(".x-msg--memo").first, "center")
        shoot(pg, "11_partner_review")

        b.close()


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def verify():
    bad = []
    files = [OUT / f"{n}.png" for n in SHOT]
    for f in files:
        w, h = png_size(f)
        size = f.stat().st_size
        ok = w * 2 == h * 3 and size < LIMIT
        print(("ok   " if ok else "BAD  ") + f"{f.name} {w}x{h} {size / 1024:.0f} KB")
        if not ok:
            bad.append(f.name)
    if len(files) > 15:
        bad.append("more than 15 images")
    lines = ["# Devpost gallery captions", ""]
    for f in files:
        lines.append(f"- {f.name}: {CAPTIONS.get(f.stem, '')}")
    (OUT / "CAPTIONS.md").write_text("\n".join(lines) + "\n")
    return bad


if __name__ == "__main__":
    main()
    bad = verify()
    print("page errors:", errors or "none")
    sys.exit(1 if bad or errors else 0)
