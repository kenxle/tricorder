# saturday-specs

The [FRAMEWORKS.md](../FRAMEWORKS.md) entries and the hand-written examples that the team types in on Saturday.

- **Status today:** partly built. Left: example result files in sample_out/, the static readout mock, one test call per schema.
- **Who builds it:** agent.
- **Waits on:** FRAMEWORKS.md (written by the frameworks writer) and the Claim schema in [ARCHITECTURE.md](../ARCHITECTURE.md).
- **Horizon:** Now to Friday night
- **Checked against:** FRAMEWORKS.md entries exist, no sample_out/ folder.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The [FRAMEWORKS.md](../FRAMEWORKS.md) entries and the hand-written examples that the team types in on Saturday. These are specs, not code.

**Waits on:** FRAMEWORKS.md (written by the frameworks writer) and the Claim schema in [ARCHITECTURE.md](../ARCHITECTURE.md).

**Includes:**

- The red-flag check list: for each check, a name, the inputs it reads, the formula, the tolerance and the sentence a person would write (feasibility 1.1). The names match the answer key's `check` field.
- The prompt that pulls claims out of the deck, and the prompt that pulls claims out of the video transcript with segment ids.
- The comp selection rules, the "why this is a fair comp" prompt and the comp schema (feasibility 1.2).
- The signals schema and the "what changed" prompt (feasibility 1.3).
- The memo's piece table, verdict rule, top-flags rule and ask-list rule ([FRAMEWORKS.md](../FRAMEWORKS.md), "Piece verdicts", "Top green and red flags" and "Ask list"), and the prompt for its connecting sentences.
- One hand-written example result file per Saturday scan, in the Claim schema, so the readout page can be built from 10:30 before any scan runs.
- A static mock of the readout layout that Ken can edit (feasibility 1.8).
- Each structured-output schema sent once this week in a real call, so any refusal shows up before Saturday. On Saturday each request carries one schema.

**Done when:** each Saturday slice below names the spec entry it types in, and each example file validates against the Claim schema by eye and by the frameworks writer's check.

**Who:** agent. Ken reviews.

**Judgment:** yes.
