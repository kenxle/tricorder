# demo-freeze

Integration, the score, the freeze and the rehearsal.

- **Status today:** partly built. Left: frozen outputs in demo/frozen/, the demo-freeze tag, rehearsal.
- **Who builds it:** captain.
- **Waits on:** every slice above, and the agent slices that join them on Saturday.
- **Horizon:** Saturday
- **Checked against:** eval/score.py and bin/smoke exist, no demo/ folder.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Integration, the score, the freeze and the rehearsal.

**Waits on:** every slice above, and the agent slices that join them on Saturday.

**Includes:**

- The captain merges at the integration points and runs `bin/smoke` on both rooms.
- `eval/score.py` reads the readout and the answer key and prints how many of the 8 planted entries were found and how many of the 3 decoys were wrongly flagged. The score goes on the page as one line, with the real number, even if it is 7 ([critique_demo.md](../../features/20261022.01_hackathon_plan/critique_demo.md), finding 7).
- The clean-room run: the readout on the plants-off room from [blind-room](blind-room.md). `eval/score.py` prints how many flags it raised.
- The variant run: at the 3:30 PM freeze the outside person sends the sealed key. The readout runs on the variant room, and `eval/score.py` prints the real numbers against that key. Nobody changes a check after the key opens.
- The approved real company's room, run like Hollis Voice's, with its outside-world panel's live re-run tested on the network the demo will use.
- The frozen outputs saved under `demo/frozen/` as the fallback for every step of the script, including the variant and clean runs, the real company's readout with this week's saved outside copies, and the last passing run of each agent slice shown on stage.
- A `demo-freeze` git tag at 3:30 PM. After it, nothing merges except a fix for a crash found in rehearsal, and only on the captain's call.
- The rehearsal: a three-minute core with a five-minute extension, from the beat sheet in [demo-script](demo-script.md). At least two run-throughs, one of them on the backup laptop from the frozen files. The schedule gives 5:30 to 6:00 for every team's demo plus the winner, so the slot is likely three minutes or less (demo critique, finding 1).

**Done when:** the three-minute core on the frozen build fits three minutes, the core plus the extension fits five, and the backup laptop can show every step from saved files.

**Who:** captain. All four rehearse.

**Hours:** 2.0 for the captain (1:00 to 1:30 PM and 2:00 to 3:30 PM), plus 0.75 for all four (3:30 to 4:15 PM).

**Judgment:** n/a.
