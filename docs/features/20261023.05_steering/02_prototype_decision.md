# Prototype decision: steering in one sentence

Prototype: [02_prototype/prototype.html](02_prototype/prototype.html), built by `spike/build_prototype.py` from `spike/out/spike.json`, which `spike/steer_spike.py` printed from the rooms. Screenshots, taken by clicking through it in Chromium: [traction_light.png](02_prototype/traction_light.png), [traction_dark.png](02_prototype/traction_dark.png), [retention_light.png](02_prototype/retention_light.png), [retention_dark.png](02_prototype/retention_dark.png).

## What it shows

- The overview's pieces, each with "Steer this piece", and "steer this line" on every claim. A click opens one text box on that spot. Enter sends. Escape closes. Nothing else to choose.
- Three steers, with figures from the spike:
  - "treat the pilot as non-recurring" on traction (full room): a new line, tagged "your steer", with ARR of $2,060,868 (12 x ('Recurring revenue (subscription plus pilot)' $186,739 less 'Pilot revenue' $15,000)) against the deck's $2,500,000, a gap of 21.3%. The check's own line ($2,240,868, 11.6%) stays.
  - "read the full room" on the retention line (seed drop): two lines tagged "new" (rebuilt NRR 87.3% over 68 customers against the tab's 102.6% over 57; GRR 73.4%), one new source, and "Verdict: Not enough in the room to Looking weak, moved by" the rebuilt NRR line.
  - "make ARR 3 million": no claim changes, and "The check's number stays: $2,240,868 (...)".
- Each diff says how the sentence was read (rewrite or more info) and by which path (wording rules, no model key).
- Simulated, and labelled on the page: the wording of the revised lines, the diff layout and the store save.

## Persona review

Run inline by the builder on 2026-10-23, from the screenshots above and the prototype file. This session has no subagent tool, so the persona agent files (`.claude/agents/persona-partner.md`, `persona-associate.md`) were followed by hand: their PERSONAS.md sections and the PERSONA_REVIEWS.md rules were read first, then the prototype. This is simulated judgment, weaker than a separate agent meeting it cold. Run the two agents on the built page when a subagent tool is available.

### The partner who finds the disagreement too late (primary)

**Verdict:** I would keep going: I typed one sentence on the ARR line and got the number I care about with its cells, and the company's number stayed beside it.
**Rating:** workable

#### What works for me
- "On your steer (pilot treated as non-recurring): ARR is $2,060,868 ..." shows the arithmetic and the two P&L lines. That is the ARR definition question I distrust most. [Grounded: "Beware of ARR ... every company calculates its own ARR in the absence of a uniform standard."]
- One box, on the line, no menu. I run diligence myself and have no time to learn a tool. [Grounded: Do, "our partners run diligence themselves without handing it to junior staff."]
- "The check's number stays" when I ask for 3 million. I trust a tool that refuses to tell me what I want to hear. [Inferred]

#### Where I get stuck
- "Verdict unchanged" on traction, while the reason line above it changed to my steer's line. I read "unchanged" and miss that the headline moved. Say the reason changed. [Inferred]
- "Read as a rewrite, by wording rules (no model key)" is engineering talk. I want to know whether to trust it, not how it was parsed. [Inferred]
- The pilot line does not link the pilot agreement's notice clause. That is my proof moment. [Grounded: "The proof we can show ... links the pilot agreement's notice clause."]

#### What would change my mind
- Show which source each added line rests on, one click away, as every other line does.
- Say plainly when the headline reason moved, even if the verdict did not.

#### What I could not judge
- The memo: whether my steer carries into what I send the partnership.

### The associate who spends days gathering (primary)

**Verdict:** I would use it: "read the full room" on the retention line did the second pass I would spend a day on, and named the line that turned the verdict.
**Rating:** strong

#### What works for me
- The "new" tags and "Read 1 new source" tell me exactly what tier two added. [Grounded: "It took us weeks to sift through the data ..."]
- "moved by" names the claim. I can say in the partners' meeting why retention turned weak. [Grounded: "I still need to write a memo, walk into a partners' meeting, and convince people ..."]
- Every revision is "kept". If I steer wrong, I can show what it was before. [Grounded: the objection, "If it is wrong, I am the one who looks bad in the partners' meeting."]

#### Where I get stuck
- The diff box is long and sits between lines. After three steers the piece is mostly diffs. Collapse older diffs. [Inferred]
- Nothing says the rest of the readout still reads the seed drop. I would assume every piece now reads the full room. [Inferred]
- "steer this line" on every line is a lot of underlined text. [Inferred]

#### What would change my mind
- A short line on more-info diffs: which pieces read the new source and which did not.
- Older revisions folded under "Earlier steers".

### Where they agree

Both want the source of an added line one click away, and both read the diff text before trusting the change. Both like the single box with no menu.

## Decisions

| Decision | Taken | Why |
|---|---|---|
| One box per piece and one per line, opened on click | yes | Roadmap Includes; both personas liked no menu |
| The revised line appears in place, tagged "your steer" or "new"; the old line stays | yes | BRAND "Follow the steer, and show what changed": the scripts' numbers stay on screen |
| Diff says when the reason line moved even if the verdict did not | yes | partner finding |
| The path wording: "Read as a rewrite (wording rules; no model key set)" kept, but last and in muted text | yes, softened | the Done when asks the revision to say which path ran; the partner finding asks it not to lead |
| Every added line carries its sources, with the same source chips as the readout | yes | both personas |
| More-info diff says which piece read the new source and that other pieces did not | yes | associate finding |
| Older diffs folded | later | needs the real page; noted in the PRD |
| Pilot steer links the pilot agreement | no, for now | the definition rule reads the P&L lines; the agreement is a 1.13 contract check's source. Noted in the PRD questions |

The prototype is throwaway. The real box is `readout/src/Steering.tsx`.
