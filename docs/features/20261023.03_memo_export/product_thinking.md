# Product thinking: the memo and its PDF

Source note for [01_brief.md](01_brief.md). Written 2026-10-23.

## User job

**Who.** Two people at a seed or Series A fund ([PERSONAS.md](../../ongoing/PERSONAS.md)). The associate prepares the memo. The partner reads it and decides.

**Trigger.** The readout is built. The partners' meeting is the next step, and the partners never met the founder.

**What they want.** In their own words, from [USER_STORIES.md](../../ongoing/USER_STORIES.md):

- The associate: "When I write the memo for the partners' meeting, I want every claim tied to its source, so I can defend it to people who never met the founder."
- The partner: "When I read a memo on a deal I did not work, I want to drill from any line to its sources and try my own what-ifs on the model, so I can trust it without redoing the work." The what-ifs are the next slice, [reader-scenarios](../../ongoing/ROADMAP.md#reader-scenarios).

**What they do today.** The associate copies numbers from ten tabs into a document by hand and adds footnotes by hand. The partner either trusts the memo or reopens the data room ([BRAND.md](../../ongoing/BRAND.md), "How we describe Tricorder", the associate's quote).

## Evidence and assumptions

Observed:

- The order of a memo is known. [MEMO_TEMPLATE.md](../../ongoing/MEMO_TEMPLATE.md) sets 16 sections from 28 published memos and 6 templates.
- The readout already holds what the memo needs, as data: claims with sources, gaps, the ask list, coverage panels. On Hollis Voice today, with only the red-flag scan built, the readout holds 10 claims, 19 gaps, 27 ask items and 7 panels, and no pieces and no top flags (`python3 -m scans.memo data_room/hollis_voice`, 2026-10-23).
- So on Saturday morning most sections will be thin. The memo has to say plainly which part of the readout leaves a section empty, or it reads as finished when it is not.

Assumptions that could change the recommendation:

- **A1. Partners want a memo, not the readout page.** The template research says the published memos read top to bottom. The drill-down keeps the readout's two clicks inside that shape.
- **A2. Section notes are good enough as footnotes in the PDF.** Notes collected at the end of each section read like a footnoted memo. True page-bottom footnotes need a layout engine we do not have. The persona review checks whether a partner minds.
- **A3. The operator edits in the page or by a small JSON file.** A full rich-text editor is out of scope for one sitting.

## Priority

The roadmap puts memo-export now to Friday night, waiting only on example readout files. Reader-scenarios waits on it ([ROADMAP.md](../../ongoing/ROADMAP.md), "reader-scenarios", Waits on). It is an agent slice.

## Options

- **Do nothing.** The partner reads the readout page. It answers the drill-down but not the memo the partners' meeting runs on.
- **A Markdown export.** Cheap, but no drill-down and no footnotes.
- **A memo built from the readout's data, with an interactive page and a PDF from the same data (chosen).** One data shape, versioned, so reader copies can lay over it later.
