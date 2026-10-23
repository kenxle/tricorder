// Drive the steering page the way a first-time user does: click a line, type one sentence, press Enter.
// Run from a folder that has the playwright package installed (npm i --no-save playwright), outside the repo:
//   CHROME=<chrome binary> node <repo>/docs/features/20261023.05_steering/verify_drive_page.mjs <base url> <evidence dir>
// It steers the seed drop's retention line and Hollis Voice's traction piece and ARR line, so run it once per fresh run.
import { createRequire } from "node:module";
import { writeFileSync } from "node:fs";
import { join } from "node:path";
const { chromium } = createRequire(join(process.cwd(), "noop.js"))("playwright");
const [base, ev] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined, args: ["--no-sandbox"] });
const log = [];
const say = (s) => { log.push(s); console.log(s); };
const errors = [];

async function open(room, scheme) {
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 }, colorScheme: scheme });
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
  await page.goto(`${base}/steer.html?room=${room}`);
  await page.getByRole("region", { name: "Overview" }).waitFor();
  return page;
}

async function steerLine(page, piece, lineText, sentence) {
  const p = page.locator(`[data-piece="${piece}"]`);
  if ((await p.getByRole("button", { expanded: true }).count()) === 0) await p.getByRole("button", { expanded: false }).first().click();
  const line = p.locator("li.claim", { hasText: lineText }).first();
  const id = await line.getAttribute("data-claim");
  await line.getByRole("button", { name: "steer this line" }).click();
  const box = p.getByLabel("Steer in one sentence");
  await box.fill(sentence);
  await box.press("Enter");
  const diff = p.getByRole("status").filter({ hasText: sentence }).last();
  await diff.waitFor({ timeout: 30000 });
  // Where the answer landed: the element right after the line typed on.
  const next = await page.evaluate((cid) => {
    const li = document.querySelector(`li.claim[data-claim="${cid}"]`);
    let n = li.nextElementSibling;
    return n ? n.innerText.slice(0, 300) : "";
  }, id);
  say(`STEER line ${id} on ${piece}: "${sentence}"`);
  say(`  next to the line: ${next.replace(/\n/g, " | ")}`);
  say(`  diff: ${(await diff.innerText()).replace(/\n/g, " | ")}`);
  return id;
}

async function steerPiece(page, piece, sentence) {
  const p = page.locator(`[data-piece="${piece}"]`);
  await p.getByRole("button", { name: "Steer this piece" }).click();
  const box = p.getByLabel("Steer in one sentence");
  await box.fill(sentence);
  await box.press("Enter");
  const diff = p.getByRole("status").filter({ hasText: sentence }).last();
  await diff.waitFor({ timeout: 30000 });
  say(`STEER piece ${piece}: "${sentence}"`);
  say(`  diff: ${(await diff.innerText()).replace(/\n/g, " | ")}`);
}

// 1. Seed drop: "read the full room" on the retention line.
let page = await open("hollis_voice_seed_drop", "light");
say(`seed drop retention before: ${(await page.locator('[data-piece="retention"] .piece-row').innerText()).replace(/\n/g, " ")}`);
await steerLine(page, "retention", "Cohorts tab states", "read the full room");
say(`seed drop retention after: ${(await page.locator('[data-piece="retention"] .piece-row').innerText()).replace(/\n/g, " ")}`);
say(`new tags: ${await page.locator('[data-piece="retention"] .tag.new').count()}`);
// Open the first source of the first new line: its file is in the full room.
const fresh = page.locator('[data-piece="retention"] li.claim', { has: page.locator(".tag.new") }).first();
await fresh.locator("sup button").first().click();
const panel = fresh.getByRole("note");
await panel.waitFor();
say(`source of the new line: ${(await panel.innerText()).replace(/\n/g, " | ").slice(0, 300)}`);
await page.locator('[data-piece="retention"]').screenshot({ path: `${ev}/steer_seed_retention_light.png` });
await page.screenshot({ path: `${ev}/steer_seed_page_light.png`, fullPage: true });
await page.close();

// 2. Full room: "treat the pilot as non-recurring" on traction (the piece), then a number request on the ARR line.
page = await open("hollis_voice", "light");
await steerPiece(page, "traction_and_revenue", "treat the pilot as non-recurring");
await steerLine(page, "traction_and_revenue", "The deck's ARR of $2,500,000", "make ARR 3 million");
await page.locator('[data-piece="traction_and_revenue"]').screenshot({ path: `${ev}/steer_traction_light.png` });
await page.close();

// 3. Dark: reload both rooms; every revision is kept, so the diffs render from what the server holds.
for (const [room, piece, name] of [["hollis_voice_seed_drop", "retention", "steer_seed_retention_dark"], ["hollis_voice", "traction_and_revenue", "steer_traction_dark"]]) {
  page = await open(room, "dark");
  const p = page.locator(`[data-piece="${piece}"]`);
  if ((await p.getByRole("button", { expanded: true }).count()) === 0) await p.getByRole("button", { expanded: false }).first().click();
  say(`reloaded ${room}: ${await p.getByRole("status").count()} diffs kept`);
  await p.screenshot({ path: `${ev}/${name}.png` });
  await page.close();
}
// 4. Phone width, dark.
page = await browser.newPage({ viewport: { width: 390, height: 1600 }, colorScheme: "dark" });
await page.goto(`${base}/steer.html?room=hollis_voice_seed_drop`);
await page.getByRole("region", { name: "Overview" }).waitFor();
await page.locator('[data-piece="retention"] button[aria-expanded]').first().click();
await page.screenshot({ path: `${ev}/steer_phone_dark.png`, fullPage: true });
const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
say(`phone width horizontal scroll: ${overflow}`);
await page.close();

say(`page errors: ${JSON.stringify(errors)}`);
writeFileSync(`${ev}/page_drive.txt`, log.join("\n") + "\n");
await browser.close();
