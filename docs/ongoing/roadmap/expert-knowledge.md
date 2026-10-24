# expert-knowledge

Give each of Tricorder's analyses what an expert investor knows: what they check first, what good and bad look like at seed and Series A, and what they ask the founder. Each analysis then reads its knowledge when it runs.

- **Status today:** not started. Asked for by Ken on 2026-10-24 at 11:18 AM, on [his desk](../../KEN_DESK.md): "let's get kimmy working on embedding expert knowledge for the different analyses".
- **Who builds it:** Kimmy, with her agents.
- **Waits on:** nothing. The raw material is written.
- **Checked against:** the 33 [document guides](../../reports/20261022.03_document_guides/INDEX.md) hold green flags, red flags and checks per document, with sources. The analyses read none of them at run time today; the checks' rules sit in code and in [FRAMEWORKS.md](../FRAMEWORKS.md).

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

### The analyses

The readout's pieces, as the code names them in `scans/memo/pieces.py` and `schema/claim.py` (`PIECE_ORDER`): traction and revenue, retention, burn and runway, unit economics, customers, market, comps, team, the pitch itself, legal and cap table, and the outside world.

### What exists to draw on

- The [document guides](../../reports/20261022.03_document_guides/INDEX.md): per document, what a first pass checks, green flags, red flags, what a script can check, what a model must read, and what to ask for if it is missing. Every point is sourced.
- [FRAMEWORKS.md](../FRAMEWORKS.md): the checks and their formulas, and how piece verdicts are set.
- [CHECKLIST.md](../CHECKLIST.md): every item Tricorder looks for, by stage.
- The research: [voice of the customer](../../reports/20261022.02_research/research_voice_of_customer.md) and [the gaps](../../reports/20261022.02_research/research_gaps.md), with investors' own words.
- Ken's notes from Kimmy on [the desk](../../KEN_DESK.md): testimonials on the B2B side, social traction for B2C, and the hard part, checking founders who know more than the VC.

### Includes

- One knowledge file per analysis, in a folder the code reads (for example `knowledge/<piece>.md`). Each holds, by stage: what an expert checks first, the benchmarks that separate strong from weak (each with a source), the green flags, the red flags, and the questions to ask the founder.
- Where the expert knowledge disagrees with a check's current threshold or a piece's verdict rule, the file says so, and the change goes on the board for the check's owner.
- The model's prompts for each analysis load that analysis's file, so the words a model reads carry the expertise. Numbers still come from scripts.
- The knowledge Ken heard from Kimmy today goes in: B2B testimonials, B2C social traction, and how a VC checks a founder who knows the field better.

### Done when

- Every analysis has its knowledge file, with a source on every benchmark.
- At least the analyses on the demo path (traction and revenue, retention, burn and runway, customers) load their file when they run, and a test shows the file's text reaches the prompt.
- The readout on Hollis Voice still scores the same or better on its answer key (`eval/score.py`).

### For Kimmy to decide

- The file layout and how much each holds.
- Which analyses to do first. A suggestion: the four on the demo path above.

**Judgment:** yes.

### Added 13:03: it feeds our own financial models and the red flags

Ken, on the prototype: "we also will want to start integrating kimmy's expert knowledge to build our own financial models and identify red flags".

- **Our own financial models.** The knowledge files give [financial-model](financial-model.md) its assumptions and benchmarks by stage, so Tricorder can rebuild a company's model its own way and set it beside the founder's.
- **Red flags.** The knowledge files give the [redflag-engine](redflag-engine.md) its thresholds and the patterns an expert looks for, each with a source. A threshold still runs as a script; the knowledge says what it should be and why.
