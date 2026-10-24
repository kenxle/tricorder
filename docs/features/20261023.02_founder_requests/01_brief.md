# Brief: requests to the founder

Roadmap slice: [founder-requests](../../ongoing/roadmap/founder-requests.md). Reasoning: [product_thinking.md](product_thinking.md). Progress: [00_progress.md](00_progress.md).

## Target users

- The associate who prepares the memo. They pick the lines, read the draft, send it, and add the founder's files when they come back.
- The founder, who reads the message. They are not a Tricorder user, but every word they read comes from here.

## Context

The readout's ask list is built by the merge (checklist coverage, `scans/memo/coverage.py`). Each line has plain words (`AskItem.what`), a reason for the operator (`why`), a piece, and usually a checklist id. Each checklist id names a document guide. Rooms that arrive by upload live in `rooms/`; the synthetic rooms in `data_room/` are checked in and must not change.

## Problem

The ask list is written for the operator. Sending it means rewriting each line for the founder, adding what form of file to send, and later saving files and rerunning the scans by hand.

## Desired outcome

1. From the ask list, one click drafts a message for one line, and one more drafts it for any group of lines the operator ticks.
2. Each item in the message carries guidance from its document guide: what the document is, the form that works best, and what a good one shows.
3. The operator copies the text or opens it in their own mail app. Tricorder never sends.
4. When a reply comes, the operator adds each file for the request it answers. It lands in the right numbered folder of the room, the scans that were waiting on it run again, and the readout is rebuilt.

## Known constraints

- No model call: the draft is a script over the readout and the guides.
- No schema change (`schema/` is frozen for this wave).
- No new dependency. FastAPI's form upload needs `python-multipart`, which is not in `requirements.txt`, so the upload takes the raw file body.
- The founder text has no file path, cell reference, claim id or checklist id (wave 1 review, U8).
- Uploads never write into `data_room/`. A synthetic room is copied to `rooms/` first.

## Open questions that affect the prototype

- One message for all ticked lines, or one per line? Recommendation: one message per click; the operator chooses the group.
- Which lines are ticked by default? Recommendation: the pinned top five.
- How long can a `mailto:` link be? Some mail apps cut long links, so a long draft offers copy first.

## What the prototype review settled

See [02_prototype_decision.md](02_prototype_decision.md).
