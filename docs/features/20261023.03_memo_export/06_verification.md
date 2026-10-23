# Verification: the memo and its PDF

Method: pstack's create-verification-skill and maintain-verification-skill, through the project skill `.claude/skills/verify-tricorder/`. This feature's map is [features/memo-export.md](../../../.claude/skills/verify-tricorder/features/memo-export.md), with one line added to its index. It was driven once by that recipe, end to end, as a user would.

## The run

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
- The persona review was run by the builder, not by independent agents (02_prototype_decision.md).
