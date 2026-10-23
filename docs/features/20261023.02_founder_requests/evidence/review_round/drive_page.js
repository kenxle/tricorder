// Review-round drive: same-origin page through the local guard, reply from the sample room,
// the page follows the reply to the working copy, /health answers during the upload.
// node drive_page3.js <base url> <evidence dir> <hiring plan csv> <reference list pdf>
const fs = require("fs");
const http = require("http");
const { chromium } = require("playwright");
const [, , url, ev, plan, refs] = process.argv;
const health = () => new Promise((ok) => { const t = Date.now(); http.get(`${url}/health`, (r) => { r.resume(); r.on("end", () => ok({ status: r.statusCode, ms: Date.now() - t })); }); });
(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 }, colorScheme: "light", permissions: ["clipboard-read", "clipboard-write"] });
  const page = await ctx.newPage();
  const errors = [], refused = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("response", (r) => { if ([403, 415].includes(r.status())) refused.push(`${r.status()} ${r.url()}`); });
  const shoot = async (name) => {
    for (const scheme of ["light", "dark"]) { await page.emulateMedia({ colorScheme: scheme }); await page.screenshot({ path: `${ev}/${name}_${scheme}.png` }); }
    await page.emulateMedia({ colorScheme: "light" });
  };
  await page.goto(url);
  await page.getByRole("combobox", { name: "Room" }).selectOption("brasswick");
  const panel = page.getByRole("region", { name: "Requests to the founder" });
  await panel.waitFor();
  await panel.getByRole("button", { name: /Draft request for 5 selected/ }).click();
  const drawer = page.getByRole("complementary", { name: "Draft to the founder" });
  await drawer.waitFor();
  await drawer.getByLabel("To").fill("celia@example.com");
  await drawer.getByRole("button", { name: "Copy text" }).click();
  await page.getByRole("status").filter({ hasText: "Copied." }).waitFor();

  const intake = page.getByLabel("Add the founder's reply");
  await intake.getByLabel("Files from the reply").setInputFiles([plan, refs]);
  const files = intake.locator(".fr-pending");
  await files.nth(0).getByLabel("It answers").selectOption({ label: "Hiring plan" });
  await files.nth(1).getByLabel("It answers").selectOption({ label: "People we can call: Reference list: management, customers, current investors, advisors" });
  await intake.getByRole("button", { name: "Add 2 files to the room" }).click();
  await page.waitForTimeout(700);
  const during = await health();
  const changed = page.getByRole("status", { name: "What changed" });
  await changed.waitFor({ timeout: 120000 });
  await page.waitForTimeout(1500);
  const roomAfter = await page.getByRole("combobox", { name: "Room" }).inputValue();
  const receipt = await page.getByRole("status", { name: "What changed" }).innerText();
  fs.writeFileSync(`${ev}/r3_page_receipt.txt`, receipt + "\n");
  const lines = await panel.locator(".fr-ask .fr-title").allInnerTexts();
  await page.getByRole("status", { name: "What changed" }).scrollIntoViewIfNeeded();
  await shoot("r3_page_reply_on_copy");
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("status", { name: "What changed" }).scrollIntoViewIfNeeded();
  await shoot("r3_page_reply_on_copy_phone");
  console.log(JSON.stringify({ health_during_upload: during, room_after_reply: roomAfter, receipt,
    hiring_plan_left: lines.includes("Hiring plan"), refused_by_guard: refused, errors }, null, 1));
  await browser.close();
})();
