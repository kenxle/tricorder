# Verification: steering in one sentence

Map: [.claude/skills/verify-tricorder/features/steering.md](../../../.claude/skills/verify-tricorder/features/steering.md). Page driver: [verify_drive_page.mjs](verify_drive_page.mjs). Evidence: [evidence/fix_round/](evidence/fix_round/) for this run; [evidence/](evidence/) holds the first round's.

## Fix round run

Run on 2026-10-23 at 03:05 UTC in a Linux cloud container, `TRICORDER_VERIFY_RUN=steering`, port 8815, `TRICORDER_OPERATOR=Ken`, on the merge of `claude/project-thread-ea11in` (claims scan and claim support included). Both readouts were rebuilt first with `scans.redflags`, `scans.claims` and `scans.memo` (`cli_20261023T030535Z_*` to `cli_20261023T030540Z_*`). Store `store_data_r2` and cache under the run folder. No model key: the wording rules read every sentence, and every note says so.

| Done when, and the fix-round items | Result | Evidence (in `evidence/fix_round/`) |
|---|---|---|
| "treat the pilot as non-recurring" on traction rewrites the piece, and the diff shows what changed | Pass. Headline "Added a scenario line." One line: "On Ken's steer, pilot not counted: ARR $2,060,868. The deck's $2,500,000 (slide 3) is 21.3% above it, measured on the books figure as the deck-against-books check measures its own gap ...", with the pilot agreement's notice clause (page 2, clause 7) as its fifth source. It is the piece's reason now. The check's line (`redflags-024`, $2,240,868, 11.6%) is the `replaced` row's before and stays in the readout. Note: "Your scenario line is new. The original check still shows $2,240,868." | `api_20261023T030557Z_13171_18390.json`; `steer_traction_light.png`, `steer_traction_dark.png`, `steer_phone_traction_light.png` |
| "read the full room" on the seed drop's retention line adds the second tier's claims marked new and names the mover | Pass. Headline "Read 5 new files; retention moved to Looking weak, customers moved to Looking weak, the pitch itself moved to Looking weak." Every piece reran on `hollis_voice`: 21 claims added (`.steer1`), and `claims-010` dropped (the claims scan's "Unsupported" contract-date line, which the full room supports). `verdict_moved_by` starts with the rebuilt NRR line. The page's banner states the switch. | `api_20261023T030556Z_13150_10816.json`; `page_drive.txt`; `steer_seed_retention_light.png`, `steer_seed_retention_dark.png`, `steer_seed_page_light.png` |
| Retention sources open the rows they sum | Pass. The NRR line cites the customer file's header row and the Cohorts tab cell, and names `scans/redflags/cohorts.py` and the panel "cohort retention rebuild". On the page, "show the rows it sums" opens 9 cohort rows with every row number. The source panel shows the quote once. | `page_drive.txt`; `steer_seed_retention_light.png` |
| A full-room line's source opens from the seed drop page | Pass. `GET /api/rooms/hollis_voice_seed_drop/claims/redflags-002.steer1/sources/0` returns the header text from `hollis_voice`; the room's own `POST /source` for the same file is 404. The page click shows "hollis_voice, the full room: 03_metrics/customer_mrr_by_month.csv · row 1". | `api_20261023T030606Z_13256_10360.json`, `api_20261023T030606Z_13267_26691.json`; `page_drive.txt` |
| A different script number is refused | Pass. Headline "Refused: computed numbers do not change on request."; head "Ken's instruction: ...", not "Rewritten"; nothing added or dropped; the note quotes the check's line. | `api_20261023T030558Z_13185_3475.json`; `page_drive.txt` |
| Every rewritten claim passes the quote checker | Pass. `python3 -m schema.check_quotes data_room/hollis_voice` on both steered readouts exits 0 (92 and 91 claims). | `cli_20261023T030605Z_13243_6465.txt` |
| A first-time user steers one line with one sentence and no other step | Pass, in Chromium, on `/steer.html` (seed drop) and on the readout page `/` (Hollis Voice, `SteerableSection` mounted in `App.tsx`). The first box's placeholder is "For example: treat the pilot as non-recurring". Tags read "Ken's steer, Oct 23, 03:06 AM" in blue, not the checks' red. The engineering footer is not on the page. Page errors: none. Phone width: no sideways scroll, the scenario line and both diffs visible. | `page_drive.txt`; `steer_box_open_light.png`; all `steer_*.png` |
| Revisions kept | Pass. `/revisions` lists both Hollis Voice steers with their panels; store versions 1 and 2 with revisions 1 and 2. | `api_20261023T030606Z_13278_30073.json`, `api_20261023T030606Z_13289_23240.json` |
| Named outside source | Pass. `python3 -m steering data_room/hollis_voice market "pull the competitor's pricing pages"` exits 0; the note starts "Not fetched:". | `cli_20261023T030606Z_13300_26983.txt` |

Seen in the screenshots, not steering's: the claims scan states "The pitch video script (line 19, beat 0:50) gives paying customers as 357 clinics ..." twice in traction (`steer_traction_dark.png`).

## First round (for the record)

### Done when, line by line

| Done when (ROADMAP "steering") | Result | Evidence |
|---|---|---|
| On Hollis Voice, "treat the pilot as non-recurring" on traction and revenue rewrites that piece, and the diff shows what changed | Pass. One line added: ARR $2,060,868 = 12 x ($186,739 less $15,000), against the deck's $2,500,000, 21.3%. The check's own $2,240,868 line stays. Verdict unchanged (looking weak). | `api_20261023T022529Z_19264_19402.json`; page `steer_traction_light.png`, `steer_traction_dark.png` |
| On the seed drop, "read the full room" on retention adds the second tier's claims marked new, and the diff names the claim that moved the verdict | Pass. Two lines added with `.steer1` ids, tagged "new": rebuilt NRR 87.3% over 68 customers against the tab's 102.6% over 57 (flag), and GRR 73.4% (watch). Verdict not enough in the room to looking weak, `verdict_moved_by` = the NRR line. Its source opens from the full room. | `api_20261023T022528Z_19249_12288.json`; `page_drive.txt`; `steer_seed_retention_light.png`, `steer_seed_retention_dark.png` |
| A request for a different script number leaves the number and the revision says so | Pass. "make ARR 3 million": nothing added or dropped; every claim value equal to before; note "You asked for 3 million. The check's number stays as it wrote it: ..." | `api_20261023T022529Z_19276_23066.json`; `page_drive.txt` |
| Every rewritten claim passes the quote checker | Pass. `python3 -m schema.check_quotes data_room/hollis_voice` on both steered readouts exits 0 (14 and 9 claims). `POST /api/rooms/hollis_voice/source` returns each new line's quote. | `cli_20261023T022540Z_19339_7353.txt`, `api_20261023T022540Z_19358_2626.json`, `api_20261023T022541Z_19369_31453.json` |
| A first-time user steers one line with one typed sentence and no other step, and the revised line appears where they typed | Pass, in Chromium: click "steer this line", type, Enter. `page_drive.txt` records the element right after the line typed on: the new lines (more info) and the diff (number request). Light, dark and phone width (no sideways scroll). | `page_drive.txt`, `steer_*_light.png`, `steer_*_dark.png`, `steer_phone_dark.png` |

### Other checks in the run

- Revisions kept: `GET /api/rooms/hollis_voice/revisions` lists both instructions and their two Panels. Store versions for `hollis_voice`: 1 to 5, with revision counts 1, 2, 3, then 1, 2 after the readout was rebuilt for the page steps (the store keeps all five).
- Named source: `python3 -m steering data_room/hollis_voice market "pull the competitor's pricing pages"` exits 0; the note says it was not fetched (`cli_20261023T022541Z_19429_5773.txt`).
- Found during the run and fixed: the first seed-drop save stored the full room's scan result, which copied full-room files no line cites (`expense_ledger.csv`, the three customer contracts) into the seed drop's version 1. The save now keeps the readout's own results; version 2 holds only the seed drop's files plus `customer_mrr_by_month.csv`. Test: `test_more_info_store_save_copies_the_full_rooms_files`.

## Limits

- **No model ran.** The model path (reading the sentence, rewording lines) is tested only on hand-built responses (`steering/tests/test_classify.py`, `test_engine.py::test_model_reword_*`), labelled as such. The live demo sentences all run on wording rules. "Pass the instruction to the scans' model readings" has nothing to pass to: no built scan has a model reading.
- **Verdicts are steering's copy of the FRAMEWORKS rules**, because `scans/memo/pieces.py` and `top_flags.py` are not built. Without the `link` step, nothing is corroborated, so no piece reads strong, and a weak piece's reason is its first flag where no conflicting claim gives a gap.
- **Retention claims come from the script half of entry 1.3**, written in this slice (`scans/redflags/cohorts.py`).
- `control.sh shot` cannot type, so the page step uses the Playwright driver in this folder. Since the fix round the page is also mounted on the readout page.
- The first round's store test asserted `expense_ledger.csv` was not copied into the seed drop's version. Since a full-room read reruns every piece, the mislabels lines cite it, so it is copied; the test now asserts every cited file is held.
