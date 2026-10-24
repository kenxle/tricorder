# room-requests

The first thing Tricorder does with a data room: see what is in it, work out what is missing, and draft the request for it automatically. The associate edits the list before anything goes out.

- **Status today:** not started. Asked for by Ken on 2026-10-24 at 11:17 AM, on [his desk](../../KEN_DESK.md).
- **Who builds it:** Benjamin (Ken, 11:17 AM: "ben can work on this").
- **Waits on:** nothing new. It joins two built pieces: [checklist-coverage](checklist-coverage.md) (what the room holds and what it lacks, by stage) and [founder-requests](founder-requests.md) (the drafted message with guidance on what to send).
- **Checked against:** `scans/memo/coverage.py` marks each checklist item found, missing, not checked or not expected; `founder_requests/draft.py` drafts from the ask list. No page lets the associate edit the list yet, and nothing runs on its own when a room arrives.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Ken, 11:16 AM: "first thing is what's in the data room and what do we need to ask for, and automate this". 11:17 AM: "put together a roadmap item for checking what's in the data room and requesting automatically what is missing. the associate can say what is needed and what is not, checking and unchecking things, or adding things".

It is step 3 of the [demo workflow](../diagrams/demo_workflow.md), and it runs again each time the room grows (step 4).

**Includes:**

- When a room arrives or grows, Tricorder runs checklist coverage on its own and shows the result first: what the room holds, and what is missing for the company's stage.
- The missing items become a request list, each item checked by default.
- The associate unchecks what is not needed, checks what is, and adds items of their own in plain words. Their choices are kept for that company.
- Tricorder drafts the request from the checked items, with the guidance founder-requests already writes for each (what the document is, the form that works best, what a good one shows). An added item gets a plain request with no guidance.
- The associate sends it from their own email, as today. Tricorder never sends anything.
- When files come back, coverage runs again and the list updates: received items drop off, and anything still missing stays checked.

**Done when:**

- On the Brasswick room, opening the room shows what it holds and the missing items as a checked list, with no click needed to start it.
- Unchecking an item removes it from the draft; adding one puts it in; both survive a reload.
- Adding a reply's file to the room's working copy removes that item from the list.

**Judgment:** yes. It decides what the associate sees first.
