# comps

Comparable companies and recent rounds, each with the reason it is a fair comp.

- **Status today:** not started. Left: the comps panel.
- **Who builds it:** design-and-finance.
- **Waits on:** claim-result, cached-data, saturday-specs (the selection rules, prompt and schema).
- **Horizon:** Saturday
- **Checked against:** no scans/comps/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Comparable companies and recent rounds, each with the reason it is a fair comp. Fourth in the feasibility research's ranking. It stays a Saturday slice, ranked by script from this week's cached filings, so all three of Track 2's asks (market signals, comps, red flags) are on screen ([critique_judge.md](../../features/20261022.01_hackathon_plan/critique_judge.md), finding 2).

**Waits on:** claim-result, cached-data, saturday-specs (the selection rules, prompt and schema).

**Includes:**

- 5 to 8 comps in two groups: recent private rounds from the cached Form D files, and public companies from the cached XBRL facts (feasibility 1.2).
- The selection rules from FRAMEWORKS.md applied by script. The model writes only the "why this is a fair comp" sentence, and the demo laptop shows that sentence as frozen output.
- Each comp's number carries its source: the filing or the Form D row.
- Reads `cache/` only on Saturday, so EDGAR being slow changes nothing on screen.
- `python -m scans.comps <room>` writes `out/<room>/comps.json`.

**Done when:** the table has at least five comps, each with a reason and a source that passes the checker.

**Who:** design-and-finance.

**Hours:** 1.5 (2:00 to 3:30 PM).

**Judgment:** yes.
