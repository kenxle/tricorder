# Verification: steering in one sentence

Map: [.claude/skills/verify-tricorder/features/steering.md](../../../.claude/skills/verify-tricorder/features/steering.md). Page driver: [verify_drive_page.mjs](verify_drive_page.mjs). Evidence: [evidence/](evidence/), copied from `/tmp/tricorder-verify/steering/evidence/`.

Run on 2026-10-23 in a Linux cloud container, `TRICORDER_VERIFY_RUN=steering`, port 8815, revisions `bde676f` (API steps) and `5185dc7` (page steps, after the store fix below). Store and cache under the run folder. No model key: every sentence was read by the wording rules, and every note says so.

## Done when, line by line

| Done when (ROADMAP "steering") | Result | Evidence |
|---|---|---|
| On Hollis Voice, "treat the pilot as non-recurring" on traction and revenue rewrites that piece, and the diff shows what changed | Pass. One line added: ARR $2,060,868 = 12 x ($186,739 less $15,000), against the deck's $2,500,000, 21.3%. The check's own $2,240,868 line stays. Verdict unchanged (looking weak). | `api_20261023T022529Z_19264_19402.json`; page `steer_traction_light.png`, `steer_traction_dark.png` |
| On the seed drop, "read the full room" on retention adds the second tier's claims marked new, and the diff names the claim that moved the verdict | Pass. Two lines added with `.steer1` ids, tagged "new": rebuilt NRR 87.3% over 68 customers against the tab's 102.6% over 57 (flag), and GRR 73.4% (watch). Verdict not enough in the room to looking weak, `verdict_moved_by` = the NRR line. Its source opens from the full room. | `api_20261023T022528Z_19249_12288.json`; `page_drive.txt`; `steer_seed_retention_light.png`, `steer_seed_retention_dark.png` |
| A request for a different script number leaves the number and the revision says so | Pass. "make ARR 3 million": nothing added or dropped; every claim value equal to before; note "You asked for 3 million. The check's number stays as it wrote it: ..." | `api_20261023T022529Z_19276_23066.json`; `page_drive.txt` |
| Every rewritten claim passes the quote checker | Pass. `python3 -m schema.check_quotes data_room/hollis_voice` on both steered readouts exits 0 (14 and 9 claims). `POST /api/rooms/hollis_voice/source` returns each new line's quote. | `cli_20261023T022540Z_19339_7353.txt`, `api_20261023T022540Z_19358_2626.json`, `api_20261023T022541Z_19369_31453.json` |
| A first-time user steers one line with one typed sentence and no other step, and the revised line appears where they typed | Pass, in Chromium: click "steer this line", type, Enter. `page_drive.txt` records the element right after the line typed on: the new lines (more info) and the diff (number request). Light, dark and phone width (no sideways scroll). | `page_drive.txt`, `steer_*_light.png`, `steer_*_dark.png`, `steer_phone_dark.png` |

## Other checks in the run

- Revisions kept: `GET /api/rooms/hollis_voice/revisions` lists both instructions and their two Panels. Store versions for `hollis_voice`: 1 to 5, with revision counts 1, 2, 3, then 1, 2 after the readout was rebuilt for the page steps (the store keeps all five).
- Named source: `python3 -m steering data_room/hollis_voice market "pull the competitor's pricing pages"` exits 0; the note says it was not fetched (`cli_20261023T022541Z_19429_5773.txt`).
- Found during the run and fixed: the first seed-drop save stored the full room's scan result, which copied full-room files no line cites (`expense_ledger.csv`, the three customer contracts) into the seed drop's version 1. The save now keeps the readout's own results; version 2 holds only the seed drop's files plus `customer_mrr_by_month.csv`. Test: `test_more_info_store_save_copies_the_full_rooms_files`.

## Limits

- **No model ran.** The model path (reading the sentence, rewording lines) is tested only on hand-built responses (`steering/tests/test_classify.py`, `test_engine.py::test_model_reword_*`), labelled as such. The live demo sentences all run on wording rules. "Pass the instruction to the scans' model readings" has nothing to pass to: no built scan has a model reading.
- **Verdicts are steering's copy of the FRAMEWORKS rules**, because `scans/memo/pieces.py` and `top_flags.py` are not built. Without the `link` step, nothing is corroborated, so no piece reads strong, and a weak piece's reason is its first flag where no conflicting claim gives a gap.
- **Retention claims come from the script half of entry 1.3**, written in this slice (`scans/redflags/cohorts.py`).
- The page is `/steer.html`, not the readout page; `control.sh shot` cannot type, so the page step uses the Playwright driver in this folder.
