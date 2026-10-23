# Product thinking: readout store and delete

Source note for [01_brief.md](01_brief.md). Written 2026-10-23.

## User job

**Who.** The associate who builds the readout, and the partner who reads it later on another machine ([PERSONAS.md](../../ongoing/PERSONAS.md)). The founder is the third party: their files are what gets held.

**Trigger.** A readout is built on one laptop from one room. Today it lives in `out/<room>/readout.json`, which git ignores and which the next scan run overwrites. A steer (wave 2) needs every revision kept. A fund that is asked "what do you hold on us?" needs one answer and one delete.

**What they want.** The roadmap's words: "The investor can see and delete everything pulled" ([ROADMAP.md](../../ongoing/ROADMAP.md), the 11:20 AM row of the requirements table). The data rule in the slice: "nothing is stored beyond the readout and its sources".

## Evidence and assumptions

Observed:

- The Hollis Voice readout cites 5 room files in its claim sources, and the red-flag scan's `inputs` names 16 files (spike, `spike/store_spike.py`; numbers from the scan output in `spike/spike_output.json`).
- A readout's `built_at` and a scan's `ran_at` change on every rebuild, so a byte compare of `readout.json` would make every rebuild a new version. The spike's content hash leaves those two fields out, and a second save of the same readout returned version 1 with `"new": false` (`spike/spike_output.json`).
- `readout.json` does not carry `ScanResult.inputs`, so the files a scan read are only known from the scan results. The store has to keep the scan results beside the readout.
- `cache/` does not exist yet. The roadmap sets its layout for outside pulls: "`cache/outside/<company>/<tab>/`", with "`cache/index.json` maps each URL ... to its saved file and date" ([ROADMAP.md](../../ongoing/ROADMAP.md), the outside-in slice).

Assumptions:

- **A1. The company id in `cache/outside/<company>/` is the same id the store uses.** The store defaults the company id to the room name (`hollis_voice`). If the outside-in builder keys the cache by another name, delete misses those files. This goes in Attention needed.
- **A2. Copies, not hashes.** A readout must "outlive one laptop" and come back "with its sources and files". A hash proves which file was read but cannot show it. So the store copies the files it read, and only those.
- **A3. One laptop until Ken picks a host.** Files on disk behind a small interface, so a hosted store can replace it.

## Priority

Steering waits on this slice ("readout-store, so a revision outlives the session", ROADMAP steering, Waits on). The outside-in slice waits on it for delete. Founder requests, the memo and contract terms want to save into it. It is small and has no model call.

## Options

- **Do nothing.** `out/` is overwritten by the next run; steering has nowhere to keep revisions; delete is "find the folders by hand".
- **Store hashes only.** Smallest, but a readout opened on another machine cannot show its sources. Rejected by A2.
- **Store the readout, its scan results and copies of the files it read, per fund, versioned (chosen).**
