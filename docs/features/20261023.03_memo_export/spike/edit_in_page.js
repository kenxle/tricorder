// Write an operator line in the served memo page, as the operator does, and capture the result.
//   NODE_PATH=<node_modules> node edit_in_page.js <memo.html url> <out_dir>
const { chromium } = require('playwright');
const path = require('path');
const [url, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    page.on('dialog', d => d.accept('Dana (verifier)'));       // the author prompt
    await page.goto(url);
    await page.click('#edit-toggle');
    await page.click('#s09 .op-add button');
    await page.fill('#s09 .op-add textarea', 'I met both founders on 2026-10-20; they have worked together for 6 years.');
    await Promise.all([page.waitForNavigation(), page.click('#s09 .op-add button:has-text("Save as a new version")')]);
    const line = page.locator('#s09 .line.kind-operator').last();
    const text = await line.innerText();
    await line.locator('.line-open').click();
    const drill = await line.locator('.drill').innerText();
    await line.scrollIntoViewIfNeeded();
    for (const scheme of ['light', 'dark']) {
      await page.emulateMedia({ colorScheme: scheme });
      await page.screenshot({ path: path.join(out, `memo_operator_line_${scheme}.png`) });
    }
    const version = await page.locator('.masthead .note').innerText();
    console.log(JSON.stringify({ version, line: text, drill }, null, 2));
  } finally { await browser.close(); }
})();
