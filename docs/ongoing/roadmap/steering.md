# steering

The operator steers the readout: a comment or short instruction on a piece makes Tricorder rewrite that piece, or get more info for it from new sources ([writers' brief, 1:12 PM block](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** readout-store, so a revision outlives the session; saturday-specs (the example readout files and the piece rules it rebuilds by).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #8, steering/ exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The operator steers the readout: a comment or short instruction on a piece makes Tricorder rewrite that piece, or get more info for it from new sources ([writers' brief, 1:12 PM block](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). It must be easy enough for a partner who runs diligence alone: one plain sentence on the line that looks wrong, with no setup and no menus, and the answer comes back on that line (Ken's 2:21 PM edit, [PRODUCT_BRIEF.md](../PRODUCT_BRIEF.md), "Steering the readout").

**Waits on:** readout-store, so a revision outlives the session; saturday-specs (the example readout files and the piece rules it rebuilds by).

**Joins on Saturday:** [readout](readout.md), whose piece and top-flag rules rebuild a steered piece, and [readout-page](readout-page.md), which shows the instruction box and the diff.

**Includes:** an instruction box on every piece and on every line, for either kind of steer. The operator types one plain sentence and nothing else: no form, no menu, no choice of steer type. Tricorder tells the two kinds apart from the sentence. A rewrite reruns the scans that feed the piece on its inputs, with the instruction passed to their model readings. A request for more info first fetches or opens the new sources it names (the full room instead of the seed drop, another filing, a competitor's pages), under the same data and terms rules as any input, then runs the piece's scans with them; the new claims are marked new. The memo rebuilds the piece and the top green and red flags by the same script rules. The new piece replaces the old one with a visible diff: claims added and dropped, wording changed, and the verdict before and after with the claims that moved it. Every revision is kept.

**Done when:**

- On Hollis Voice, "treat the pilot as non-recurring" on traction and revenue rewrites that piece, and the diff shows what changed.
- On the Hollis Voice seed drop, "read the full room" on retention adds the claims from the second tier, marked new, and the diff names the claim that moved the verdict.
- An instruction that asks for a different script number leaves the number as the script computed it, and the revision says so.
- Every rewritten claim still passes the quote checker.
- A first-time user steers one line with one typed sentence and no other step, and the revised line appears where they typed.

**Who:** agent.

**Judgment:** yes.

**Status:** done for every Done when check. Merged in PR #8 on 2026-10-23. The code is `steering/`, `server/steering_routes.py` and `readout/src/Steering.tsx`, mounted in the readout page's overview. The [shared verdicts slice](../../features/20261023.07_readout_verdicts/00_spec.md), merged in PR #14, moved verdicts and headline flags to `scans/memo/pieces.py` and `top_flags.py`, replacing steering's temporary rules. Feature folder: [20261023.05_steering](../../features/20261023.05_steering/00_progress.md).
