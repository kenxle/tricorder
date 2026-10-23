# Brief: readout store and delete

Roadmap slice: [readout-store](../../ongoing/ROADMAP.md#readout-store). Reasoning: [product_thinking.md](product_thinking.md). Progress: [00_progress.md](00_progress.md).

## Target users

- The associate who builds and steers a readout.
- The partner who opens it later.
- Other Tricorder code: steering, founder requests, the memo and contract terms save into the store.

## Context

A readout is a file in `out/<room>/`, rebuilt and overwritten by every run. There is no host yet; the demo runs on one laptop.

## Problem

A readout does not outlive the run that made it, its revisions are not kept, and there is no one place that answers "what do we hold on this company?" or deletes it.

## Desired outcome

1. Save a readout, its scan results and copies of the room files it read, under a fund and a company. Each save that changes something is a new numbered version; saving the same readout again changes nothing.
2. Get the latest version (or any version) back, with its sources and files.
3. List everything held for one company: versions, files, scan results, and the company's outside pulls in `cache/`.
4. One delete removes all of it, and the listing afterwards is empty.
5. The same five calls from a terminal (`python -m store ...`) and from the page (`/api/store/...`). Delete asks for confirmation.

## Known constraints

- Nothing stored beyond the readout and its sources (the slice's data rule).
- No schema change before Saturday. The store's own records are its own models in `store/`.
- No path can leave the store, whatever a fund id, company id or source uri says.
- Files on disk now; a hosted store later behind the same interface ([ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md), "The stack").

## Open questions that affect the interface

Answered by the spike in [02_interface_example.md](02_interface_example.md).
