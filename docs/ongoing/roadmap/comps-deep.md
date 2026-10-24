# comps-deep

Comps from Form D and EDGAR in depth.

- **Status today:** not started. Left: Form D and EDGAR comps in depth.
- **Who builds it:** agent.
- **Waits on:** cached-data (the Form D quarters and XBRL facts already saved); saturday-specs (the selection rules).
- **Horizon:** Now to Friday night
- **Checked against:** no scans/comps/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Comps from Form D and EDGAR in depth.

**Waits on:** cached-data (the Form D quarters and XBRL facts already saved); saturday-specs (the selection rules).

**Joins on Saturday:** [comps](comps.md), whose table it extends.

**Includes:** every Form D quarter, ranking by the selection rules; EDGAR full-text search for business descriptions (the JSON endpoint is undocumented, so the scan falls back to cached results when it breaks, per feasibility Part 2); XBRL frames for public revenue. Crunchbase only with an arrangement for apps, per the landscape research.

**Done when:** on Hollis Voice, the ranked list draws on every saved Form D quarter, each comp's business description comes from full-text search or its cached copy, and every number passes the quote checker.

**Who:** agent.

**Judgment:** yes.
