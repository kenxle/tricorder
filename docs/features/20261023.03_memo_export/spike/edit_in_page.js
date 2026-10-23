// Edit the served memo page in one sitting, as the operator does, and capture each step.
//   NODE_PATH=<node_modules> node edit_in_page.js <memo.html url> <out_dir> [author]
// 1. Switch to the operator view and type a name in the edit bar.
// 2. Queue three changes in place: a line in section 9, the recommendation in section 15,
//    and a rewrite of a claim line in section 10 with a figure of the operator's own.
// 3. Before saving, someone else saves a version through the API, so the page's version is stale.
// 4. Save: the server answers 409, the page keeps the three changes and offers to reapply them.
// 5. Reapply: one new version with all three. The recommendation now opens the summary.
// Writes <out_dir>/edit_in_page.json and memo_edit_{light,dark}.png, memo_edit_conflict.png,
// memo_edit_saved_{light,dark}.png.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [url, out, author = 'Priya Shah'] = process.argv.slice(2);
const api = url.replace(/\.html$/, '');

async function keep(page, scope, text) {
  await page.fill(`${scope} textarea.op-text`, text);
  await page.click(`${scope} .op-tools button:has-text("Keep")`);
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const report = { author, failures: [] };
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    await page.goto(url);
    await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
    await page.reload();
    report.start_version = (await (await fetch(api + '/versions')).json()).slice(-1)[0];
    await page.click('#view-toggle');
    await page.fill('#edit-author', author);
    // Section 9: a line of the operator's own.
    await page.click('#s09 .op-add button');
    await keep(page, '#s09 .op-add', 'I met both founders on 2026-10-20; they have worked together for 6 years.');
    // Section 15: the recommendation.
    const rec = '.line[data-line-id="s15-recommendation"]';
    await page.click(`${rec} .op-tools button:has-text("Write this")`);
    await keep(page, rec, 'Wait. Ask for the bank statements and the ARR walk before the partners meet.');
    // Section 10: rewrite Tricorder's cash line with a different figure.
    const cashId = await page.$eval('#s10 .line.kind-claim', l => l.getAttribute('data-line-id'));
    const cash = `.line[data-line-id="${cashId}"]`;
    await page.click(`${cash} .op-tools button:has-text("Rewrite")`);
    await keep(page, cash, 'Cash is $2,100,000 after the March wire, by the founder\'s count.');
    report.save_button = await page.innerText('#edit-save');
    await page.locator(cash).scrollIntoViewIfNeeded();
    for (const scheme of ['light', 'dark']) {
      await page.emulateMedia({ colorScheme: scheme });
      await page.screenshot({ path: path.join(out, `memo_edit_${scheme}.png`) });
    }
    await page.emulateMedia({ colorScheme: 'light' });
    // Someone else saves first.
    const other = await fetch(api + '/edits', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ author: 'Sam Okafor', base_version: report.start_version,
                             edits: [{ action: 'add', section: 12, text: 'Ask about the Marlow pilot first.' }] }) });
    report.other_save = other.status;
    await page.click('#edit-save');
    await page.waitForSelector('#edit-reapply');
    report.conflict_status = await page.innerText('#edit-status');
    report.pending_after_conflict = await page.locator('.line.pending').count();
    await page.locator('.edit-bar').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(out, 'memo_edit_conflict.png') });
    await Promise.all([page.waitForNavigation(), page.click('#edit-reapply')]);
    // Saved. The page reloads in the partner view.
    const memo = await (await fetch(api)).json();
    report.saved_version = memo.version;
    const lines = memo.sections.flatMap(s => s.lines.map(l => ({ ...l, section: s.number })));
    const ops = lines.filter(l => l.kind === 'operator');
    report.operator_lines = ops.map(l => ({ section: l.section, author: l.author, version: l.version, claim_ids: l.claim_ids,
                                            unsourced_numbers: l.unsourced_numbers, text: l.text }));
    report.change_log = memo.changes.map(c => `${c.version} ${c.author}: ${c.what}`);
    report.summary_first_line = await page.innerText('#s02 .line[data-line-id]:first-child');
    report.withdrawn = memo.withdrawn_lines;
    if (ops.length !== 4) report.failures.push(`expected 4 operator lines (Sam's and three of ${author}'s), found ${ops.length}`);
    if (!ops.every(l => l.author === author || l.author === 'Sam Okafor')) report.failures.push('an operator line has the wrong author');
    const cashOp = ops.find(l => l.section === 10);
    if (!cashOp || cashOp.claim_ids.length || !cashOp.unsourced_numbers.includes('$2,100,000')) report.failures.push('the rewritten cash line is not marked as the operator\'s');
    if (!report.summary_first_line.startsWith('Recommendation.')) report.failures.push('the recommendation does not open the summary');
    await page.evaluate(() => window.scrollTo(0, 0));
    for (const scheme of ['light', 'dark']) {
      await page.emulateMedia({ colorScheme: scheme });
      await page.screenshot({ path: path.join(out, `memo_edit_saved_${scheme}.png`) });
    }
  } finally { await browser.close(); }
  fs.writeFileSync(path.join(out, 'edit_in_page.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.failures.length ? 1 : 0);
})();
