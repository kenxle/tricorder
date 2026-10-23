# Product thinking: requests to the founder

Source note for [01_brief.md](01_brief.md). Roadmap slice: [founder-requests](../../ongoing/ROADMAP.md#founder-requests).

## User job

The associate has a readout with an ask list: 31 lines on the Brasswick room (real merge, `python3 -m scans.memo data_room/brasswick`, 2026-10-23). The job is to turn some of those lines into a message the founder can act on without a call, send it from the associate's own email, and see the readout fill in when the files come back.

Today the readout gives the associate a list of what is missing, written as a list. Turning it into a message means rewriting each line for an outsider, explaining what kind of file works, chasing the reply, saving the attachments in the room, and rerunning the scans by hand.

## Evidence and assumptions

- **Ken asked for it** (writers' brief, 3:15 PM block): "While compiling the data room, there are quick ways to send messages to the company asking them for information, with guidance on what they should submit."
- **A messy room costs weeks.** The associate persona's evidence: "It took us weeks to sift through the data, ultimately which led to us losing momentum and conviction in the founders ability to execute" ([junior VC, Dec 2022](https://williamleonard.substack.com/p/learnings-from-year-2-in-venture)). A request that says exactly what form to send shortens the second round trip. That last step is an inference, not evidence.
- **The guidance already exists.** The 33 document guides (`docs/reports/20261022.03_document_guides/`) each say what the document is, the form it arrives in, and what a good one shows (their "What it is" and "Green flags" sections), and most end with a one-line ask for the founder. Every checklist row names its guide (`docs/ongoing/checklist.csv`, column `guide`).
- **Assumption: the operator sends, never Tricorder.** The roadmap says so. It also keeps Tricorder out of the operator's mailbox, which the inbox research says needs restricted scopes (ARCHITECTURE.md, "Inputs beyond the room").
- **Assumption: replies arrive as attachments the operator saves.** The inbox slice will later post them in by itself. Until then the operator adds each file by hand, so that step must be one action.
- **Risk found in wave 1:** the ask list's gap lines carry cell references and fragments (review U8: "the option grant records for every holder (02_financials/cap_table.xlsx, Cap_Table!A7)"). A founder must never see internal locations or checklist ids.

## Priority

It is a "Now to Friday night" slice that waits only on checklist coverage, which is merged. It joins the readout on Saturday. The demo does not depend on it, but it closes the loop the product brief promises: the gaps become requests, and the answers become claims.

## Options

1. **Copy-paste text only.** Cheapest. Leaves the reply side manual: save files, rerun scans.
2. **Draft plus `mailto:` plus a file intake that reruns waiting scans.** What the roadmap asks for. The intake is new attack surface (file names, sizes, kinds, paths).
3. **Send through a mail API.** Out of scope: the roadmap says Tricorder never sends.

## Recommendation

Option 2. The draft is a pure script over the readout and the guides: no model call, so it is instant and testable. The intake is a small, strict upload: one file at a time, for one named request, into a room under `rooms/`, then the scans whose inputs changed, then the merge.
