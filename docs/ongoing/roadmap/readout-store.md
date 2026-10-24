# readout-store

A persistent store of readouts, so a readout outlives one laptop.

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** skeleton (the Claim schema and the shape of `readout.json`); a host for the product, which Ken picks (the guardrails' deploy field is empty until then). Until there is a host, the store runs on the demo laptop.
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #8, store/ exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

A persistent store of readouts, so a readout outlives one laptop.

**Waits on:** skeleton (the Claim schema and the shape of `readout.json`); a host for the product, which Ken picks (the guardrails' deploy field is empty until then). Until there is a host, the store runs on the demo laptop.

**Joins on Saturday:** [readout](readout.md), whose `readout.json` it stores.

**Includes:** each readout, its sources and the files it read, stored per fund; a delete that removes all of them; a list of everything held for one company. This is the data rule from the brief: nothing is stored beyond the readout and its sources, and the investor can see and delete everything pulled.

**Done when:** a stored readout for Hollis Voice comes back with its sources and files; the list for that company shows everything held; and one delete leaves nothing for that company in the store or in `cache/`.

**Who:** agent.

**Judgment:** yes.

**Status:** done for every Done when check. Merged in PR #8 on 2026-10-23. The code is `store/` (`python -m store`) and `server/store_routes.py`. A delete leaves `out/<room>/` in place and lists it in its report; whether it should clear it is open for Ken (board row TRI-wave2-defaults). The page has no panel for list and delete yet. Feature folder: [20261023.01_readout_store](../../features/20261023.01_readout_store/00_progress.md).
