// Copies the clickable prototype into public/prototype so Expo web serves it at /prototype/index.html.
// Re-run (pnpm sync:prototype) whenever the prototype changes. Copies files only; no symlinks, no deletes.
import { cpSync, mkdirSync, lstatSync } from "node:fs";
import { dirname, join, basename, extname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "../../../docs/features/20261024.02_first_steps_ui/prototype");
const dest = join(here, "../public/prototype");

const skipNames = new Set(["__pycache__", "shots", "style", "data.json"]);
const skipExts = new Set([".py", ".pyc"]);

mkdirSync(dest, { recursive: true });
cpSync(src, dest, {
  recursive: true,
  force: true,
  filter: (from) => {
    const name = basename(from);
    if (skipNames.has(name) || skipExts.has(extname(name))) return false;
    return !lstatSync(from).isSymbolicLink();
  },
});
console.log(`Synced prototype to ${dest}`);
