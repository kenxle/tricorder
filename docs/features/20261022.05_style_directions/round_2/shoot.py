"""Screenshot a direction's home page, light and dark, at desktop width.

Run: python3 round_2/shoot.py direction_e_archivo
"""
import pathlib
import sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
d = HERE / sys.argv[1]
(d / "screens").mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for scheme in ("light", "dark"):
        pg = b.new_page(viewport={"width": 1440, "height": 900}, color_scheme=scheme)
        pg.goto((d / "home.html").as_uri(), wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(d / "screens" / f"home-desktop-{scheme}.png"), full_page=True)
    b.close()
print("ok")
