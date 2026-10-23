// Drive the steering page the way a first-time user does: click a line, type one sentence, press Enter.
// Run from a folder that has the playwright package installed (npm i --no-save playwright), outside the repo:
//   CHROME=<chrome binary> node <repo>/docs/features/20261023.05_steering/verify_drive_page.mjs <base url> <evidence dir>
// Launch the app with TRICORDER_OPERATOR=Ken so the tags name him. It steers the seed drop's retention line
// on /steer.html and Hollis Voice's traction piece on the readout page itself (/), so run it once per fresh run.
import { createRequire } from "node:module";
import { writeFileSync } from "node:fs";
import { join } from "node:path";
const { chromium } = createRequire(join(process.cwd(), "noop.js"))("playwright");
const [base, ev] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined, args: ["--no-sandbox"] });
const log = [];
const say = (s) => { log.push(s); console.log(s); };
const flat = (s) => s.replace(/\n/g, " | ");
const errors = [];

async function open(path, scheme, width = 1200) {
  const page = await browser.newPage({ viewport: { width, height: 1400 }, colorScheme: scheme });
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
  await page.goto(`${base}${path}`);
  await page.getByRole("region", { name: "Overview" }).waitFor();
  await page.locator("[data-piece]").first().waitFor();
  return page;
}

async function expand(page, piece) {
  const p = page.locator(`[data-piece="${piece}"]`);
  if ((await p.getByRole("button", { expanded: true }).count()) === 0) await p.getByRole("button", { expanded: false }).first().click();
  return p;
}

async function send(page, box, sentence, n) {
  await box.fill(sentence);
  await box.press("Enter");
  const diff = page.getByRole("status", { name: `Steer ${n}` });
  await diff.waitFor({ timeout: 60000 });
  return diff;
}

// 1. Seed drop, /steer.html: "read the full room" on the retention tab line.
let page = await open("/steer.html?room=hollis_voice_seed_drop", "light");
let p = await expand(page, "retention");
say(`seed drop retention before: ${flat(await p.locator(".piece-row").innerText())}`);
const tabLine = p.locator("li.claim", { hasText: "Cohorts tab states" }).first();
await tabLine.getByRole("button", { name: "steer this line" }).click();
const box = p.getByLabel("Steer in one sentence");
say(`first box placeholder: ${await box.getAttribute("placeholder")}`);
await p.screenshot({ path: `${ev}/steer_box_open_light.png` });
let diff = await send(page, box, "read the full room", 1);
say(`STEER retention line: "read the full room"`);
say(`  diff: ${flat(await diff.innerText())}`);
say(`  banner: ${flat(await page.locator(".banner.switch").innerText())}`);
say(`seed drop retention after: ${flat(await p.locator(".piece-row").innerText())}`);
say(`new tags in retention: ${await p.locator(".tag.new").count()}; on the page: ${await page.locator(".tag.new").count()}`);
// The rebuilt NRR line cites the customer file, which only the full room holds: open it from the seed drop page.
const nrr = p.locator("li.claim", { hasText: "Rebuilt from the customer file, 12-month net revenue retention" }).first();
await nrr.locator("sup button").first().click();
const src = nrr.getByRole("note").first();
await src.waitFor();
say(`source of the rebuilt NRR line: ${flat(await src.innerText()).slice(0, 300)}`);
say(`  quote shown ${await src.locator("q").count()} time(s), text block ${await src.locator("pre").count()}`);
await nrr.getByRole("button", { name: /show the rows/ }).click();
const table = nrr.getByRole("region", { name: "cohort retention rebuild" });
say(`rows table: ${await table.locator("tbody tr").count()} cohort rows; first: ${flat(await table.locator("tbody tr").first().innerText()).slice(0, 200)}`);
await p.screenshot({ path: `${ev}/steer_seed_retention_light.png` });
await page.screenshot({ path: `${ev}/steer_seed_page_light.png`, fullPage: true });
await page.close();

// 2. Hollis Voice on the readout page itself: the pilot steer on traction, then a number request on the piece.
page = await open("/", "light");
p = await expand(page, "traction_and_revenue");
await p.getByRole("button", { name: "Steer this piece" }).click();
diff = await send(page, p.getByLabel("Steer in one sentence"), "treat the pilot as non-recurring", 1);
say(`STEER traction piece on /: "treat the pilot as non-recurring"`);
say(`  reason: ${await p.locator(".reason").innerText()}`);
say(`  scenario line: ${flat(await p.locator("li.claim.scenario").first().innerText()).slice(0, 400)}`);
say(`  diff: ${flat(await diff.innerText())}`);
say(`  check line in the piece list: ${await p.locator("ul.claims > li.claim", { hasText: "a gap of 11.6%" }).count()}, in the diff as before: ${await diff.locator(".before", { hasText: "a gap of 11.6%" }).count()}`);
await p.getByRole("button", { name: "Steer this piece" }).click();
diff = await send(page, p.getByLabel("Steer in one sentence"), "make ARR 3 million", 2);
say(`STEER traction piece on /: "make ARR 3 million"`);
say(`  diff: ${flat(await diff.innerText())}`);
await p.screenshot({ path: `${ev}/steer_traction_light.png` });
await page.close();

// 3. Dark: reload both rooms; every revision is kept, so the diffs render from what the server holds.
for (const [path, piece, name] of [["/steer.html?room=hollis_voice_seed_drop", "retention", "steer_seed_retention_dark"], ["/", "traction_and_revenue", "steer_traction_dark"]]) {
  page = await open(path, "dark");
  p = await expand(page, piece);
  say(`reloaded ${path}: ${await p.locator(".diff").count()} diffs kept in ${piece}`);
  await p.screenshot({ path: `${ev}/${name}.png` });
  await page.close();
}

// 4. Phone width, light: the steered traction piece with its scenario line and diff.
page = await open("/", "light", 390);
p = await expand(page, "traction_and_revenue");
await p.screenshot({ path: `${ev}/steer_phone_traction_light.png` });
say(`phone width horizontal scroll: ${await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)}`);
say(`phone shows scenario line ${await p.locator("li.claim.scenario").count()}, diffs ${await p.locator(".diff").count()}`);
await page.close();

say(`page errors: ${JSON.stringify(errors)}`);
writeFileSync(`${ev}/page_drive.txt`, log.join("\n") + "\n");
await browser.close();
