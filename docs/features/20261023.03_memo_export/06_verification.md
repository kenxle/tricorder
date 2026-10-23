# Verification: the memo and its PDF

Method: pstack's create-verification-skill and maintain-verification-skill, through the project skill `.claude/skills/verify-tricorder/`. This feature's map is [features/memo-export.md](../../../.claude/skills/verify-tricorder/features/memo-export.md), with one line added to its index. It was driven once by that recipe, end to end, as a user would.

## The fix-round run (current)

Run `memo-export-final2`, port 8813, revision 2f4aea9, 2026-10-23, Linux cloud container, after the claims scan, the cohort checks, steering and the per-module claim ids were merged in. Copied into [evidence/fix_round/](evidence/fix_round/).

| Step | Command | Result |
|---|---|---|
| Launch, doctor | `control.sh launch`, `control.sh doctor` | `OK run=memo-export-final2 pid=2108 url=http://127.0.0.1:8813 ... rev=2f4aea9` |
| Readout | `control.sh cli python3 -m scans.redflags`, `scans.claims` (no model key), `scans.memo` on `data_room/hollis_voice` | exit 0 each |
| Export | `control.sh cli python3 -m memo data_room/hollis_voice` | exit 0; version 1, 16 sections, 91 claims, 0 could not verify |
| Quote check | `control.sh cli python3 -m schema.check_quotes ...` | exit 0 |
| Two clicks, both views | `spike/drive_memo.js` on the served page | [memo_drive.json](evidence/fix_round/memo_drive.json): 307 lines, 88 shown to a partner; partner view's visible text has no plumbing; operator view: 295 of 295 lines opened in one click, 411 of 411 claims opened their sources in the second with the quote marked; first screen is the round and the red flags; no horizontal scroll at 390 px |
| Edit in the page | `spike/edit_in_page.js ... "Priya Shah"` | [edit_in_page.json](evidence/fix_round/edit_in_page.json): three changes queued, "Save 3 changes as version 2"; another author saved version 2 first through the API; the page answered "Someone saved version 2 first. Your 3 changes are kept." and reapplied them as version 3; the cash line rewritten with $2,100,000 has no claims and is marked as Priya Shah's figure; the recommendation opens section 2 |
| PDF | `curl .../memo.pdf`, then [pdf_check.txt](evidence/fix_round/pdf_check.txt) | 10 pages, 95 notes; no claim id, check name, checklist number, command, blank or ask list; no unformatted number; CSV rows read with their column names; section 2 opens with the recommendation |
| Versions | `control.sh api GET .../memo/versions` | `[1,2,3]` |
| Cleanup | `control.sh cleanup` | stopped pid 2108; evidence kept |

Screenshots: partner view [light top](evidence/fix_round/memo_light_top.png), [dark top](evidence/fix_round/memo_dark_top.png), [light drill](evidence/fix_round/memo_light_drill.png), [dark drill](evidence/fix_round/memo_dark_drill.png), [phone dark](evidence/fix_round/memo_phone_dark.png); edit mode [light](evidence/fix_round/memo_edit_light.png), [dark](evidence/fix_round/memo_edit_dark.png), [the 409 offer](evidence/fix_round/memo_edit_conflict.png), saved [light](evidence/fix_round/memo_edit_saved_light.png) and [dark](evidence/fix_round/memo_edit_saved_dark.png); PDF pages 1 and 2 as PNG.

Full suite at 2f4aea9: 552 passed, 0 failed (`bin/ci-py`, exit 0). Memo tests: 44 passed.

Limits of this run: no steered room was driven, so the "before" of a replaced claim is proven by `test_a_claim_the_steer_replaced_is_the_new_lines_before` only. The pieces and top flags steps are still not built, so the summary's piece line reads "No verdicts yet".

## The first run (history)

Run `memo-export-final`, port 8813, revision 8ab2ea2, 2026-10-23, Linux cloud container. `TRICORDER_VERIFY_DIR` was this session's scratchpad; everything below is copied into [evidence/](evidence/).

| Step | Command | Result |
|---|---|---|
| Launch, doctor | `control.sh launch`, `control.sh doctor` | `OK run=memo-export-final pid=13040 url=http://127.0.0.1:8813 ... rev=8ab2ea2` |
| Readout | `control.sh cli python3 -m scans.redflags data_room/hollis_voice`, then `scans.memo` | exit 0, 10 claims |
| Export | `control.sh cli python3 -m memo data_room/hollis_voice` | exit 0; version 1, 16 sections, 10 claims, 0 could not verify; 7 sections name their gap ([cli transcript](evidence/)) |
| Quote check | `control.sh cli python3 -m schema.check_quotes data_room/hollis_voice <run>/out/hollis_voice/readout.json` | exit 0, "10 claims checked" |
| Read back | `control.sh api GET /api/rooms/hollis_voice/memo` | HTTP 200, 16 sections |
| Two clicks | `node spike/drive_memo.js http://127.0.0.1:8813/api/rooms/hollis_voice/memo.html` | [memo_drive.json](evidence/memo_drive.json): 128 lines, 113 with something behind them, 113 opened in one click; 40 claims shown, 40 opened their sources in the second click with the quote marked, 40 showed the agree and disagree lists; no failures; no horizontal scroll at 390 px |
| PDF | `curl .../memo.pdf`, then [pdf_check.txt](evidence/pdf_check.txt) | v1 and v3: 10 of 10 claims footnoted, every source's file and locator named, every claim passes the quote checker, all 16 section titles present |
| Edit by API | `control.sh api POST /api/rooms/hollis_voice/memo/edits` (base 1) | HTTP 200, version 2, section 15 is an operator line by Verifier with "$1.5M" marked as the operator's figure; the same call again: HTTP 409 |
| Edit in the page | `node spike/edit_in_page.js` | [edit_in_page.json](evidence/edit_in_page.json): version 3, the line marked Operator, "Dana (verifier), version 3", "operator's figure, no source: 6" (the date is not counted) |
| Versions | `control.sh api GET /api/rooms/hollis_voice/memo/versions` | `[1,2,3]` |
| Cleanup | `control.sh cleanup` | stopped pid 13040; evidence kept (19 files). uvicorn processes before and after: 2 and 2 (neither is this run's) |

Screenshots: [memo_light_top.png](evidence/memo_light_top.png), [memo_dark_top.png](evidence/memo_dark_top.png), [memo_light_drill.png](evidence/memo_light_drill.png), [memo_dark_drill.png](evidence/memo_dark_drill.png), [memo_phone_dark.png](evidence/memo_phone_dark.png), [memo_operator_line_light.png](evidence/memo_operator_line_light.png), [memo_operator_line_dark.png](evidence/memo_operator_line_dark.png). The PDFs: [memo_v1.pdf](evidence/memo_v1.pdf), [memo_v3.pdf](evidence/memo_v3.pdf), and pages 1 to 3 of v3 as PNG. The versions: `evidence/memo_v1.json` to `memo_v3.json`, and the page `memo_v3.html`.

## Limits

- The readout on main has no pieces, top flags or links, so on Hollis Voice "agree" and "disagree" are empty and the page says the link step is not built. The second click's agree and disagree lists with real entries are proven only on the prototype's simulated links (`02_prototype/prototype_simulated_drive.json`: 62 of 62) and in `test_with_pieces_and_flags_the_summary_and_openers_fill`.
- `control.sh shot` captures only `/`, so the memo page is driven by `spike/drive_memo.js` with a scratch Node Playwright, not by the helper.
- Proven in a Linux container, not on Ken's Mac.
- The first round's persona review was the builder's; the fix round records the coordinator's independent reviews (02_prototype_decision.md).
