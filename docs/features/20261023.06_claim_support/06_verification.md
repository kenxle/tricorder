# Verification: claim support

Method: pstack's verification method, through the repo's project skill `.claude/skills/verify-tricorder/`. This feature's map is [claim-support.md](../../../.claude/skills/verify-tricorder/features/claim-support.md), with one line in that folder's `README.md` index. Nothing else in the skill was touched.

## The run

- Run name `claim-support`, port 8816: `TRICORDER_VERIFY_RUN=claim-support TRICORDER_VERIFY_PORT=8816 .claude/skills/verify-tricorder/control.sh launch`, then `doctor` (`OK run=claim-support pid=23186 url=http://127.0.0.1:8816 ...`).
- Final pass at revision `5cd7f75` (the code at `727ff5b`; later commits are docs only), 2026-10-23 02:41Z: every command in the map's "Driving it" section, on all four rooms, through `control.sh cli` and `control.sh api`. The index of that pass, with the saved file for each step, is [evidence/final_pass.txt](evidence/final_pass.txt).
- The map's observable claims were checked against the saved responses: [evidence/recipe_check.txt](evidence/recipe_check.txt).
- Earlier passes in the same run, before two wording fixes, are also in `evidence/`. They found both fixes (below).

## What it showed

| Step | Result | Evidence |
|---|---|---|
| Scan Hollis Voice | `claims: 64 claims, 8 gaps`, exit 0 | `evidence/cli_20261023T024151Z_28442_8823.txt` |
| Spoken ARR contradicted | `spoken_arr_vs_claims_page`, flag, cites script line 15, `ARR_TOTAL`, metrics row 22, revenue row 1984, deck slide 3 | `evidence/api_20261023T024202Z_28769_1773.json` |
| Ceiling broken | "gives largest customer share as at most 9%, but revenue by customer (row 1984) says 21.0%" | same file |
| Source proven | `POST /api/rooms/hollis_voice/source` with `ARR_TOTAL` returns `2240868`; Brasswick slide 4 returns the slide text containing the quote | `evidence/api_20261023T024216Z_28829_2565.json`, `evidence/api_20261023T024216Z_28840_14585.json`; earlier deck and script sources in `api_20261023T0234*` |
| Memo step, Hollis | 64 claims: 39 supported, 8 contradicted, 17 unsupported, relabelled yes | `evidence/cli_20261023T024153Z_28480_16454.txt` |
| Memo step, Brasswick | 53 claims: 31, 7, 15; 6 not counted; five claims carry `conflicts_with` (slide 4 chart and $943K, slide 10 runway and burn, script line 15) | `evidence/cli_20261023T024155Z_28565_22797.txt`, `evidence/api_20261023T024202Z_28780_22536.json` |
| Score | Brasswick 5 of 5, 0 decoys; Hollis 1 of 8 (PF2b), 0 decoys; seed drop 1 of 8, 0 decoys; clean 0 of 0, 0 decoys | `evidence/cli_20261023T024156Z_28588_23131.txt` and the other `eval.score` files in final_pass.txt |
| Clean room | 0 contradicted | `evidence/cli_20261023T024159Z_28669_253.txt` |
| Seed drop | gap why `file missing: monthly revenue by customer` | `evidence/api_20261023T024202Z_28791_19423.json` |
| The page | The readout page for Hollis Voice shows the claims scan's gaps and, through checklist coverage, their ask lines. No component shows the claims table. Light and dark. | `evidence/claim_support_hollis_light.png`, `evidence/claim_support_hollis_dark.png` |
| Cleanup | `control.sh cleanup` stopped the run's own server by pid | see [00_progress.md](00_progress.md) |

Done-when counts per room, from `spike/count_done_when.py` at `727ff5b`: [evidence/done_when_counts.txt](evidence/done_when_counts.txt).

## Found while driving, and fixed

1. The PF5 claim said the deck gives the largest customer share "as above 9%", the opposite of "No customer above 9%". Now "at most 9%" (commit `f4e276d`, test `test_a_ceiling_written_as_no_customer_above_reads_at_most`).
2. "gives runway as 29" left the unit out on a big-number slide. Now "29 months" in the sentence; the table's stated column keeps the printed figure (commit `727ff5b`, test `test_a_bare_figure_reads_with_its_unit_in_the_claim_text`).

## Limits

- The video is not recorded. Spoken claims come from the script. The transcript path is proven only on hand-built transcripts in `scans/claims/tests/test_inputs.py`.
- No `ANTHROPIC_API_KEY`: the model reading ran only as its gap. Its parsing is tested on hand-built responses only.
- `POST /api/rooms/<room>/readout` rebuilds without the memo step until `scans/memo/merge.py` lists it, so the page's readout here came from the CLI pass, which ran the step by its own command.
- The page shows "No flags yet": there is no top-flags step on main, so the claims scan's flags do not reach the page's top section yet.
- Proven in a Linux cloud container only, not on Ken's Mac.
