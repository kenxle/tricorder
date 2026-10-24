# readout

The top green and red flags, the overview and its drill-downs, assembled from the scans' claims: every piece of the company with a verdict, every sentence sourced.

- **Status today:** partly built. Left: source linking (board task TRI-readout-link), the ask-list step, the model pass for connecting sentences.
- **Who builds it:** captain.
- **Waits on:** claim-result. It is built against `sample_out/` until the real scans land at the 1:00 PM integration point.
- **Horizon:** Saturday
- **Checked against:** scans/memo/ merge, pieces, top_flags exist (PR #14).

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The top green and red flags, the overview and its drill-downs, assembled from the scans' claims: every piece of the company with a verdict, every sentence sourced. Second in the feasibility research's ranking.

**Progress:** the merge, claim-support step, and coverage step are built. The [shared verdicts slice](../../features/20261023.07_readout_verdicts/00_spec.md), merged in PR #14 on 2026-10-23, adds the piece verdicts and headline selection and moves steering to the same code. General source linking, the ask-list step, and connecting prose remain open. The current scans also need to emit linked numeric peers before the framework's full headline example can appear. The board's TRI-readout-link (source linking and numeric evidence peers) is the next readout task.

**Waits on:** claim-result. It is built against `sample_out/` until the real scans land at the 1:00 PM integration point.

**Includes:**

- `scans/memo/` reads every `out/<room>/*.json` that exists, runs the quote checker again, and links claims that disagree (same label, unit and period, values apart by more than the tolerance) into `conflicts_with`.
- Links claims from independent sources that agree (same label, unit and period, values within the tolerance) into `corroborated_by`.
- Groups the claims into the nine pieces and gives each piece its verdict by the stated script rule ([FRAMEWORKS.md](../FRAMEWORKS.md), "Piece verdicts"): looking strong, looking weak, mixed or not enough in the room, with a one-line reason and the counts of corroborating and contradicting sources. Pieces go in a fixed order, strong and weak alike.
- Picks the best green flags and the worst red flags from the piece verdicts and the flags, by the stated script rule ([FRAMEWORKS.md](../FRAMEWORKS.md), "Top green and red flags"), and puts them first in `readout.json`.
- One model pass that writes connecting sentences. Each sentence must cite claim ids; a sentence with none is dropped. If it is not working at the fallback call, the demo shows the script's top flags, pieces and verdicts without it; it is first in the [demo fallback order](saturday.md#demo-fallback-order). On the demo laptop it shows as frozen output.
- A missing scan becomes a gap in the readout, not an error.
- The ask list at the end of `readout.json`: what the operator should request from the founder ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:54 PM block; [FRAMEWORKS.md](../FRAMEWORKS.md), "Ask list"). A script builds it from each gap's `would_need` field and each weak piece's reason. Each line says what to ask for, the claim or gap it would settle, and the piece it feeds. No model call.
- Writes `out/<room>/readout.json`.

**Done when:**

- The four ARR figures in the data room research's Part 3.4 (the model's $2,240,868, the deck's $2,500,000, the video's spoken figure of about $3,000,000, and the recurring ARR the scan computes) show as one conflict group inside traction and revenue, and that piece reads looking weak.
- On the full room, the pitch itself reads looking strong, with `corroborated_by` linking slide 13 to the cap table's Series A rows (DC3, the clean cap table).
- Every piece has a verdict, including "not enough in the room" where no number has a second source.
- On the full room, the green flag is the round (the pitch itself), and the red flags come out in the order the rule gives: runway, clinics, largest customer, gross margin, retention ([FRAMEWORKS.md](../FRAMEWORKS.md), "Top green and red flags", worked example).
- The video-against-deck flag is found here.
- Deleting one scan's output file leaves a gap in the readout and no crash.
- On the Hollis Voice seed drop, the ask list names the files the seed drop leaves out, each with the gap or weak-piece claim it would settle: the expense ledger (actual monthly spend, which settles current burn and gross margin), monthly revenue by customer (retention and the largest customer's share), the Marlow pilot agreement, and the largest customer's order form (their contract language). The seed drop's file list is in [data_room_files.csv](../../reports/20261022.02_research/data_room_files.csv).

**Who:** captain.

**Hours:** 1.5 (11:30 AM to 12:30 PM, and 1:30 to 2:00 PM).

**Judgment:** yes.
