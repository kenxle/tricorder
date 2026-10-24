# founder-requests

Quick requests to the company while the room is being compiled ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 3:15 PM block).

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** [checklist-coverage](checklist-coverage.md).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #8, founder_requests/ exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Quick requests to the company while the room is being compiled ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 3:15 PM block). Ken: "While compiling the data room, there are quick ways to send messages to the company asking them for information, with guidance on what they should submit."

**Waits on:** [checklist-coverage](checklist-coverage.md).

**Joins on Saturday:** [readout](readout.md), whose ask list it drafts from.

**Includes:**

- From the ask list, one click drafts a message to the founder for any missing item or group of items, in plain words.
- Each request carries guidance on what to submit, taken from the document guides: what the document is, the form that works best, and what a good one shows (for example, monthly revenue by customer as a CSV with one row per customer per month).
- The operator reviews and sends it from their own email; Tricorder never sends anything itself.
- When the founder replies with files, they land in the room and the scans that waited on them start.

**Done when:** on the Brasswick room, the ask list produces a request for its missing documents with guidance for each, the operator can copy or open it in their email client, and a reply's attachment added to the room starts the waiting scans.

**Who:** agent.

**Judgment:** yes.

**Status:** done for every Done when check. Merged in PR #8 on 2026-10-23. The code is `founder_requests/`, `server/founder_requests_routes.py` and `readout/src/FounderRequests.tsx`. Tricorder never sends the message. A reply is added to a working copy of a sample room, `rooms/<room>_live`. Feature folder: [20261023.02_founder_requests](../../features/20261023.02_founder_requests/00_progress.md).
