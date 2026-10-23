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

The coordinator ran the two persona agents, `persona-partner` and `persona-associate`, cold on 2026-10-23, on the first round's evidence (the built page's screenshots and `page_drive.txt`) and on this prototype. Both met the work with no builder context. Their full reports stay with the coordinator; this section records what reached the builder and what the builder did with it. The builder's own inline self-read, which this replaces, is in git history (commit 15df69a).

### Ratings

| Persona | Rating |
|---|---|
| The partner who finds the disagreement too late | workable |
| The associate who spends days gathering | workable |

### What both trust

- The pilot steer: a formula with its cells, "12 x ('Recurring revenue (subscription plus pilot)' $186,739 less 'Pilot revenue' $15,000)", and the check's own line still on screen.
- The refusal: "make ARR 3 million" changes nothing and quotes the check back.

### What blocked both

- **Retention sources.** The rebuilt NRR and GRR figures opened one sample row of the customer file, not the rows they sum. The source panel also showed the quote twice, and one footnote pointed at nothing a reader could check.

### Other findings, as relayed

1. A rewrite should redo the piece: its reason should name the steered figure, labelled as the operator's assumption, and the check's line should move into the diff as "before".
2. The diff should say first what happened ("Added a scenario line", "Read 1 new file; retention moved to Looking weak", "Refused: ..."). The how-it-was-read footer is engineering talk. A refusal is not a rewrite.
3. "your steer" names nobody. Show a name and a time. The steered line must not share the checks' red.
4. "read the full room" changed one piece; the rest of the page still read the seed drop. Rerun every piece and say so at the top. A full-room line's source must open from the seed drop's page.
5. The pilot steer should cite the pilot agreement's notice clause.
6. A first-time user does not know what to type: show one example.
7. The page lives at `/steer.html`; mount it on the readout page.

### What I took

- All of the above. Retention: `scans/redflags/cohorts.py` now returns the panel "cohort retention rebuild" with every row it summed per cohort, the NRR and GRR lines name the script and the panel, and the page opens the panel's rows from the line. The source panel shows a quote once when the text at the locator is the quote.
- The scenario line becomes the piece's reason; the check's line is hidden from the piece list and shown in the diff as "Before, the check's line (kept)", with its sources.
- The diff's heading is the steer's headline row. The "Read as ..." and "Verdicts rebuilt by ..." sentences stay in `PieceRevision.note` and the panel, and the page leaves them off.
- `Steer.author` comes from the request, else the `TRICORDER_OPERATOR` setting. Tags read "Ken's steer, Oct 23, 02:47 AM"; scenario lines use a blue rule, not red.
- A full-room read reruns every available scan on the full room and rebuilds every piece; a banner states the switch; the claim-source route reads from the room the line reads.
- The pilot agreement's notice clause, read by `scans/redflags/contract_reader.py`, is the scenario line's last sentence and its fifth source.
- The text box's placeholder is "For example: treat the pilot as non-recurring" until the first steer.
- `SteerableSection` replaces the Overview section in `App.tsx`; `/steer.html` still works.

### What I left

- Folding older diffs under "Earlier steers" (from the first round's notes). Not in the relayed findings; still a page polish item.
- Fewer "steer this line" links. Not relayed as a blocker; left as is.

## Decisions

| Decision | Taken | Why |
|---|---|---|
| One box per piece and one per line, opened on click | yes | Roadmap Includes; both personas liked no menu |
| The revised line appears in place, tagged with who steered and when, or "new"; the check's line it replaces moves into the diff as "before" | yes | BRAND "Follow the steer, and show what changed"; persona reviews, fix round |
| Diff says when the reason line moved even if the verdict did not | yes | partner finding |
| The path wording: "Read as a rewrite (wording rules; no model key set)" kept in the note and the panel, hidden on the page | yes | the Done when asks the revision to say which path ran; both reviews call it engineering talk |
| Every added line carries its sources, with the same source chips as the readout | yes | both personas |
| A full-room read reruns every piece, and a banner says the page reads the full room | yes | persona reviews, fix round (replaces "other pieces still read the seed drop") |
| Older diffs folded | later | needs the real page; noted in the PRD |
| Pilot steer links the pilot agreement | yes | persona reviews; read with `scans/redflags/contract_reader.py` |

The prototype is throwaway. The real box is `readout/src/Steering.tsx`.
