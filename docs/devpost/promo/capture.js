// Records promo.html. Usage:
//   node capture.js stills <outdir> <caps dir> [t1,t2]   -> one PNG at each shot's midpoint
//   node capture.js frames <outdir> <caps dir>  -> 1350 JPEG frames at 30 fps
const { chromium } = require(process.env.HOME + '/.claude/skills/playwright-skill/node_modules/playwright');
const path = require('path'); const fs = require('fs');
const MID = [2.5, 8.5, 14.5, 18.5, 21.5, 24.5, 27.5, 29.5, 33.5, 37, 39.5, 43];
(async () => {
  const mode = process.argv[2], out = path.resolve(process.argv[3] || 'frames');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const caps = path.resolve(process.argv[4]);
  const n = fs.readdirSync(caps).filter(f => /^s4_type_\d+\.png$/.test(f)).length;
  await p.goto('file://' + path.resolve(__dirname, 'promo.html') + '?t=0&typen=' + n + '&caps=' + encodeURIComponent('file://' + caps));
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => null))));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  if (mode === 'stills') {
    const ts = process.argv[5] ? process.argv[5].split(',').map(Number) : MID;
    for (const t of ts) { await p.evaluate(t => render(t), t); await p.screenshot({ path: `${out}/still_${t}.png` }); }
  } else {
    const fps = 30, total = 45 * fps;
    for (let i = 0; i < total; i++) {
      await p.evaluate(t => render(t), i / fps);
      await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 92 });
    }
  }
  await b.close();
})();
