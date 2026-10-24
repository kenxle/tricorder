# typescript-port

Move Tricorder from Python to TypeScript, with a React web app and a React Native app on the same shared code.

- **Status today:** not started. Decided by Ken on 2026-10-24 at 11:00 AM.
- **Who builds it:** Ben (Benjamin Schachter), with his agents.
- **Waits on:** nothing. The Python code keeps running the demo until the TypeScript version passes the same checks.
- **Checked against:** `git ls-files` line counts by [typescript_port_inventory.py](typescript_port_inventory.py) (run from the repo root), run 2026-10-24.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

### What exists today

The stack is in [ARCHITECTURE.md](../ARCHITECTURE.md), "The stack" and "Folder layout". In short: Python scans, a merge step and a FastAPI server, with a React 19 and Vite page in `readout/`.

Lines of code by folder, from [typescript_port_inventory.py](typescript_port_inventory.py) (tests counted apart):

| Folder | What it is | Python lines | Python test lines |
|---|---|---|---|
| `schema/` | The Claim schema and the file readers (PDF, xlsx, CSV, Markdown, transcript) | 733 | 204 |
| `scans/` | Every scan: red flags, claims, the memo merge, checklist coverage | 6,515 | 3,745 |
| `memo/` | The interactive memo and its PDF | 2,696 | 1,283 |
| `steering/` | Operator steering and what-ifs | 1,044 | 773 |
| `founder_requests/` | Messages to the company asking for missing items | 1,362 | 870 |
| `store/` | Readouts saved per fund | 678 | 480 |
| `server/` | The API the page reads | 708 | 615 |
| `eval/` | Scoring a run against the room's answer key | 102 | 43 |
| `clients/` | The model client | 102 | 16 |
| **Total** | | **13,940** | **8,029** |

The page in `readout/` is already TypeScript and React: 1,100 lines, plus 177 lines of generated types in `schema/`.

### Includes

- One shared TypeScript core the web app and the native app both import: the Claim schema, the file readers, the scans, the merge and the scoring.
- A React web app. The current `readout/` page is the starting point.
- A React Native app that shows the same readout.
- The rules that make Tricorder trustworthy carry over unchanged: every number comes from code, a model only reads words, every claim carries the quote it relied on, and a script finds that quote again in the source ([PRODUCT_BRIEF.md](../PRODUCT_BRIEF.md), principles and commitments).

### Done when

- The TypeScript version runs on all four data rooms and scores the same against each answer key as the Python version does (`eval/score.py`).
- The ported tests pass in CI.
- The web app and the native app both open the Hollis Voice readout.

### For Ben to decide

Ben picks the tools. These are the choices his agents will hit first:

- The repo layout: for example one workspace with a shared core package, a web app and a native app.
- The PDF and spreadsheet libraries that replace pdfplumber, openpyxl and pandas.
- The server: keep an API, or run the core inside each app.
- The port order. A suggestion: the schema and readers first, since everything imports them, then the scans the demo shows first ([roadmap](../ROADMAP.md), "Up next").

### For Ben and Ken together

- **What the 3:30 PM demo freeze runs.** The Python version is complete today. Recommended: the freeze runs whichever version passes the answer-key check at 3:30, and the Python one stays the fallback.
- **Who keeps building Python slices meanwhile.** Fixes to the Python scans after the port starts have to be made twice. Recommended: Ben's agents port what is merged, and the board says when each folder moves, so nobody edits a folder after it has moved.
