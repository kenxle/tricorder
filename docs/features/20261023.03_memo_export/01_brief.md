# Brief: the memo and its PDF

Roadmap slice: [memo-export](../../ongoing/ROADMAP.md#memo-export). Template: [MEMO_TEMPLATE.md](../../ongoing/MEMO_TEMPLATE.md). Reasoning: [product_thinking.md](product_thinking.md). Progress: [00_progress.md](00_progress.md).

## Target users

- The associate who prepares the memo. They export it, edit it and send it.
- The partner who reads the memo. They open any line they doubt.

## Context

The readout (`out/<room>/readout.json`) holds every claim with its sources, the gaps, the ask list and the checklist coverage. Pieces and the top green and red flags are merge steps that are not built yet. The template sets 16 sections, five line kinds, and which sections stay the operator's.

## Problem

The partners' meeting runs on a memo, not on a readout page. Writing the memo by hand loses the sources, and a footnoted memo written by hand cannot be drilled.

## Desired outcome

1. `python -m memo <room>` writes a draft memo in the template's 16 sections, in order. Each section is filled from the readout as the template says, or it names the gap that leaves it empty.
2. An interactive page the partners open. It reads top to bottom. One click on any line opens its claims. One more opens a claim's source text and the claims that agree or disagree with it.
3. A PDF of the same memo. Every claim has a numbered note naming its file, locator, quote and date read.
4. The operator edits the draft. Each edit makes a numbered version with a change-log line. A sentence the operator writes with no claim behind it is marked as theirs, and a number in it with no claim is marked "operator's figure, no source".
5. Every claim in both forms passes the quote checker again on export. A claim that fails moves to the "could not verify" box.

## Known constraints

- The schema is frozen. The memo's own models live in `memo/`.
- Tricorder never writes the recommendation, the outcome cases or the judgement lines, and never says invest or pass ([BRAND.md](../../ongoing/BRAND.md)).
- The page works offline, with no CDN.
- No new dependency unless unavoidable.

## Open questions that affect the prototype

- Does a thin readout read as a memo at all, or as a list of gaps? The prototype shows both: the real Hollis Voice readout, and the same readout with pieces and top flags simulated and labelled.
- Section notes against page-bottom footnotes in the PDF.
