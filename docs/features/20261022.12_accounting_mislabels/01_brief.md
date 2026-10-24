# Short brief: accounting mislabels

Roadmap slice: [accounting-mislabels](../../ongoing/roadmap/accounting-mislabels.md). Rules: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), entry 1.12. Reasoning: [product_thinking.md](product_thinking.md). Progress: [00_progress.md](00_progress.md).

## Target users

- The associate who prepares the memo. They check every headline number against its label before writing.
- The partner who reads the memo. They drill into a flag and want both numbers and both places.

## Context

The Saturday red-flag engine checks two mislabel kinds: a pilot booked as ARR (kind a, entry 1.2) and delivery costs filed as operating expense (kind d, entry 1.7). Entry 1.12 lists six more that the rooms can test, plus kind c, gross against net revenue. The engine's 3.0 hours cannot hold them, so an agent builds them before Saturday and they join the engine's output on the day.

## Problem

A number can carry a label it does not earn: MRR that holds a pilot, revenue that is really cash invoiced, revenue that includes money passed on to someone else, burn that leaves out contractors, revenue booked for service not yet delivered. Each one makes the company look bigger or cheaper to run. Finding them by hand means rebuilding totals from the customer file and the ledger.

## Desired outcome

For each kind, the readout says one of four things, with sources: flag (here is the claimed number, the recomputed number and where each sits), clear (the tie-out ran and matched), cannot check (this file is missing, ask for it), or not run (the room has nothing of this kind). The decoys stay clear. One cause found by two checks reads as one cause.

## Known constraints

- Scripts only. No model call, no network ([ROADMAP.md](../../ongoing/ROADMAP.md), redflag-engine).
- Output is the shared Claim and Gap from the skeleton's `schema/claim.py`. The module returns `(list[Claim], list[Gap])` and nothing else.
- Every claim passes the quote checker. Every number comes from a script.
- The rooms are fixed. `data_room/generate.py` is not changed by this slice unless the coordinator decides the resale option must live there.

## The prototype

Nonvisual, so the prototype is an interface example: the Claim JSON each sub-check emits, written by the spike. See [02_interface_example.md](02_interface_example.md). The spike is throwaway; the real module is rebuilt test first.

What the spike settled:

- Every sub-check runs on the rooms as entry 1.12 describes, except kind e on Brasswick, which needs a plan test entry 1.12 does not have.
- Kind c has a real room: Brasswick (BF1). The resale test room is still useful as an on and off pair.
- The link to the pilot-as-ARR flag can be a shared source, with no schema change.

## Open questions

Tracked in [00_progress.md](00_progress.md), "Attention needed", and in [03_prd.md](03_prd.md), "Open questions".
