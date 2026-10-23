// Drive the interactive memo in Chromium the way a partner does, and prove the two clicks.
//   NODE_PATH=<folder with node_modules> node drive_memo.js <url or file path> <out_dir> [name]
// For every line with something behind it: one click on the line must show its claims (or, for a
// gap, its checklist item and ask line). For every claim shown: one more click on its source button
// must show the source text with the quote marked, and the "agree" and "disagree" lists.
// It first reads the partner view (the default) and checks that what a partner sees holds no plumbing:
// no claim ids, check names, checklist numbers, commands or blanks. Then it switches to the operator
// view, where every line shows, and drills every line. Screenshots are of the partner view.
// Writes <out_dir>/<name>_drive.json and light and dark screenshots.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const target = process.argv[2];
const out = process.argv[3];
const name = process.argv[4] || 'memo';
const url = target.startsWith('http') ? target : 'file://' + path.resolve(target);
const exe = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const browser = await chromium.launch({ executablePath: exe });
  const report = { url, lines: 0, drillable: 0, opened_in_one_click: 0, claim_lines: 0, claims_seen: 0,
                   sources_opened_in_two_clicks: 0, quotes_marked: 0, agree_disagree_shown: 0, failures: [] };
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    await page.goto(url);
    report.lines = await page.locator('.line[data-line-id]').count();
    // The partner view: what shows, and that none of it is plumbing.
    const firstScreen = pg => pg.evaluate(() => {
      window.scrollTo(0, 0); const out = [];
      document.querySelectorAll('.line[data-line-id]').forEach(l => {
        const r = l.getBoundingClientRect(); if (l.offsetParent !== null && r.top < window.innerHeight && r.bottom > 0) out.push(l.getAttribute('data-line-id')); });
      return out; });
    report.partner_first_screen = await firstScreen(page);
    report.partner_visible_lines = await page.$$eval('.line[data-line-id]', ls => ls.filter(l => l.offsetParent !== null).length);
    const partnerOpen = await page.$$eval('.line .line-open', bs => bs.filter(b => b.offsetParent !== null).map(b => b.closest('.line').getAttribute('data-line-id')));
    for (const id of partnerOpen) await page.locator(`.line[data-line-id="${id}"] > .line-open`).click();
    await page.$$eval('.claim .source-open', bs => bs.filter(b => b.offsetParent !== null).forEach(b => b.click()));
    const partnerText = await page.evaluate(() => document.body.innerText);
    const plumbing = partnerText.match(/redflags-\d+|(?<![!\w])C\d\d\b|python -m|scans\/|Who writes|not built|[Vv]erifier|Operator writes|\b[a-z]+_vs_[a-z_]+\b/g) || [];
    report.partner_plumbing = [...new Set(plumbing)];
    for (const p of report.partner_plumbing) report.failures.push(`partner view shows plumbing: ${p}`);
    await page.reload();
    // The operator view: every line shows; drill them all.
    await page.click('#view-toggle');
    const ids = await page.$$eval('.line .line-open', bs => bs.map(b => b.closest('.line').getAttribute('data-line-id')));
    report.drillable = ids.length;
    for (const id of ids) {
      const li = page.locator(`.line[data-line-id="${id}"]`);
      const kind = await li.getAttribute('data-kind');
      const btn = li.locator(':scope > .line-open');
      await btn.click();                                        // click 1
      const drill = li.locator(':scope > .drill');
      if (!(await drill.isVisible()) || (await btn.getAttribute('aria-expanded')) !== 'true') {
        report.failures.push(`${id}: drill did not open`); continue;
      }
      const claims = drill.locator(':scope > .claim[data-claim-id]');
      const nClaims = await claims.count();
      const other = await drill.locator(':scope > .checklist-item, :scope > .ask-item, :scope > .meta').count();
      if (nClaims + other === 0) { report.failures.push(`${id} (${kind}): nothing behind the line`); continue; }
      report.opened_in_one_click++;
      if (nClaims) report.claim_lines++;
      for (let i = 0; i < nClaims; i++) {
        const card = claims.nth(i);
        report.claims_seen++;
        const sb = card.locator(':scope > .source-open');
        await sb.click();                                       // click 2
        const panel = card.locator(':scope > .sources');
        const texts = panel.locator(':scope > .source > .source-text');
        if (!(await panel.isVisible()) || (await texts.count()) === 0) {
          report.failures.push(`${id}/${await card.getAttribute('data-claim-id')}: source did not open`); continue;
        }
        report.sources_opened_in_two_clicks++;
        const marks = await panel.locator(':scope > .source > .source-text mark').count();
        if (marks === await texts.count()) report.quotes_marked++;
        else report.failures.push(`${id}/${await card.getAttribute('data-claim-id')}: ${marks} of ${await texts.count()} quotes marked`);
        if (await panel.locator(':scope > .agree').count() && await panel.locator(':scope > .disagree').count()) report.agree_disagree_shown++;
        await sb.click();
      }
      await btn.click();
    }
    // A drilled-open state for the screenshots: the first claim line with a linked claim, else the first claim line.
    await page.reload();   // back to the partner view
    const pick = await page.$$eval('.line.kind-claim', ls => ls.map(l => l.getAttribute('data-line-id')));
    const first = pick.find(i => i.startsWith('s07')) || pick[0];
    if (first) {
      const li = page.locator(`.line[data-line-id="${first}"]`);
      await li.locator(':scope > .line-open').click();
      await li.locator('.claim .source-open').first().click();
      await li.scrollIntoViewIfNeeded();
    }
    for (const scheme of ['light', 'dark']) {
      await page.emulateMedia({ colorScheme: scheme });
      await page.screenshot({ path: path.join(out, `${name}_${scheme}_drill.png`) });
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({ path: path.join(out, `${name}_${scheme}_top.png`) });
      if (first) await page.locator(`.line[data-line-id="${first}"]`).scrollIntoViewIfNeeded();
    }
    const phone = await browser.newPage({ viewport: { width: 390, height: 844 }, colorScheme: 'dark' });
    await phone.goto(url);
    await phone.screenshot({ path: path.join(out, `${name}_phone_dark.png`) });
    report.phone_first_screen = await firstScreen(phone);
    report.phone_horizontal_scroll = await phone.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  } finally {
    await browser.close();
  }
  fs.writeFileSync(path.join(out, `${name}_drive.json`), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.failures.length ? 1 : 0);
})();
