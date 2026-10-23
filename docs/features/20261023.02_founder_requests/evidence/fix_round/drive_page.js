// Fix-round drive of the founder-requests panel on this run's server, the way an operator does.
// node drive_page2.js <base url> <evidence dir> <hiring plan csv> <reference list pdf> <working room>
const fs = require("fs");
const { chromium } = require("playwright");
const [, , url, ev, plan, refs, work] = process.argv;
(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 }, colorScheme: "light", permissions: ["clipboard-read", "clipboard-write"] });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  const shoot = async (name) => {
    await page.emulateMedia({ colorScheme: "light" });
    await page.screenshot({ path: `${ev}/${name}_light.png` });
    await page.emulateMedia({ colorScheme: "dark" });
    await page.screenshot({ path: `${ev}/${name}_dark.png` });
    await page.emulateMedia({ colorScheme: "light" });
  };
  await page.goto(url);
  await page.getByRole("combobox", { name: "Room" }).selectOption("brasswick");
  const panel = page.getByRole("region", { name: "Requests to the founder" });
  await panel.waitFor();
  await panel.getByRole("button", { name: /Draft request for 5 selected/ }).click();
  const drawer = page.getByRole("complementary", { name: "Draft to the founder" });
  await drawer.waitFor();
  const trust = await drawer.locator(".fr-trust").innerText();
  await drawer.getByLabel("To").fill("celia@example.com");
  await drawer.getByLabel("Your name").fill("Sam Ortiz");
  await drawer.getByLabel("Fund").fill("Example Ventures");
  await drawer.getByLabel("Ask for it by").fill("2026-11-06");
  await page.waitForFunction(() => /Example Ventures/.test(document.querySelector("#fr-body").value), null, { timeout: 10000 });
  await drawer.getByRole("button", { name: "Copy text" }).click();
  await page.getByRole("status").filter({ hasText: "Copied." }).waitFor();
  const copied = await page.evaluate(() => navigator.clipboard.readText());
  const href = await drawer.getByRole("link", { name: "Open in mail app" }).getAttribute("href");
  const longWarning = await drawer.getByText("long for a mail link").count();
  fs.writeFileSync(`${ev}/r2_page_copied_text.txt`, copied);
  fs.writeFileSync(`${ev}/r2_page_mailto.txt`, href + "\n");
  const panelText = await panel.innerText();
  await panel.scrollIntoViewIfNeeded();
  await shoot("r2_page_draft");

  // The founder replies with two files, in the working copy.
  await page.getByRole("combobox", { name: "Room" }).selectOption(work);
  await panel.waitFor();
  await page.waitForTimeout(500);
  const intake = page.getByLabel("Add the founder's reply");
  const intakeTop = await intake.evaluate((el) => el.getBoundingClientRect().top - document.querySelector(".fr-asks").getBoundingClientRect().top);
  await intake.getByLabel("Files from the reply").setInputFiles([plan, refs]);
  const files = intake.locator(".fr-pending");
  await files.nth(0).getByLabel("It answers").selectOption({ label: "Hiring plan" });
  await files.nth(1).getByLabel("It answers").selectOption({ label: "People we can call: Reference list: management, customers, current investors, advisors" });
  await files.nth(1).getByLabel("It also answers").selectOption({ label: "People we can call: Founder reference calls" });
  await intake.scrollIntoViewIfNeeded();
  await shoot("r2_page_two_files_ready");
  await intake.getByRole("button", { name: "Add 2 files to the room" }).click();
  const changed = page.getByRole("status", { name: "What changed" });
  await changed.waitFor({ timeout: 90000 });
  const receipt = await changed.innerText();
  fs.writeFileSync(`${ev}/r2_page_receipt.txt`, receipt + "\n");
  await changed.scrollIntoViewIfNeeded();
  await shoot("r2_page_reply_added");
  await page.waitForTimeout(800);
  const titles = await panel.locator(".fr-ask .fr-title").allInnerTexts();

  // Phone width: the add box and the draft come before the list.
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("combobox", { name: "Room" }).selectOption("brasswick");
  await page.waitForTimeout(500);
  await panel.getByRole("button", { name: "Draft request for Hiring plan" }).click();
  await drawer.waitFor();
  await page.waitForTimeout(300);
  await drawer.scrollIntoViewIfNeeded();
  const phoneOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  await shoot("r2_page_draft_phone");
  await intake.scrollIntoViewIfNeeded();
  await shoot("r2_page_add_phone");
  console.log(JSON.stringify({
    trust, mailto_length: href.length, long_warning_shown: longWarning > 0, copied_head: copied.slice(0, 300),
    signed: copied.trim().endsWith("Sam Ortiz\nExample Ventures"), dated: copied.includes("by Friday 6 November"),
    codes_in_panel: (panelText.match(/\bC\d{2,3}\b/g) || []), intake_above_list_px: intakeTop,
    receipt, lines_after: titles.length, hiring_plan_left: titles.includes("Hiring plan"),
    phone_horizontal_scroll: phoneOverflow, errors,
  }, null, 1));
  await browser.close();
})();
