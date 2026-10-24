# memo-export

Tricorder helps the operator write the memo for the partners' meeting ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:58 PM and 2:00 PM blocks).

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** saturday-specs (the example readout files). The template is written: [MEMO_TEMPLATE.md](../MEMO_TEMPLATE.md), built from real published memos and memo templates.
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #8, memo/ exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Tricorder helps the operator write the memo for the partners' meeting ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:58 PM and 2:00 PM blocks). The memo is interactive. It reads as a normal memo top to bottom, and behind every line sit the same two clicks the operator has in the readout. An agent builds it before Saturday, outside the captain's and the frontend's Saturday hours.

**Waits on:** saturday-specs (the example readout files). The template is written: [MEMO_TEMPLATE.md](../MEMO_TEMPLATE.md), built from real published memos and memo templates.

**Joins on Saturday:** [readout](readout.md), whose `readout.json` fills the memo.

**Includes:**

- The export: a draft memo in the template's sections, in order, filled from the readout's pieces, the checklist items, the top green and red flags, the gaps and the ask list, as the template says.
- The interactive memo: a page the partners open. From any line, one click opens the claims behind it. From any claim, one more opens its source and the sources that agree or disagree.
- A static PDF of the same memo for funds that need one, with every claim footnoted to its source.
- The operator edits the draft. A sentence the operator writes with no claim behind it is marked as theirs.

**Done when:**

- On Hollis Voice, the export fills every template section, or names the gap that leaves one empty.
- In the interactive memo, every line reaches its claims in one click and a claim's source in two.
- In the PDF, every claim carries a footnote that names its source and locator.
- Every claim in both forms passes the quote checker.

**Who:** agent.

**Judgment:** yes.

**Status:** done for every Done when check. Merged in PR #8 on 2026-10-23. The code is `memo/` and `server/memo_routes.py`; the page is `/api/rooms/<room>/memo.html` and the PDF `/api/rooms/<room>/memo.pdf`. Reader copies and scenarios are not built; they wait on the financial-model slice. Sections whose scans are not built yet show one gap line. Feature folder: [20261023.03_memo_export](../../features/20261023.03_memo_export/00_progress.md).
