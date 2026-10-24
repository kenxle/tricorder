# Saturday

Back to the [roadmap](../ROADMAP.md).

Saturday is finishing, integration, the demo freeze and the demo. The four people build the slices below in the six-hour window, and the agent slices from the first horizon join them at the integration points in the run of show.

## The window

The schedule gives 10:30 AM to 4:30 PM for hacking, with lunch, so the plan uses six hours. The Luma page also says "9 hours of focused building" ([research_landscape.md](../../reports/20261022.02_research/research_landscape.md), summary). That gap is three hours, by [check_saturday_hours.py](../../features/20261022.01_hackathon_plan/check_saturday_hours.py). The board row TRI-ask-organisers asks which is right. If the room opens for longer, the extra time goes to the pieces that are showing saved results, in the reverse of the [demo fallback order](#demo-fallback-order), so more of the demo runs live. The freeze still sits one hour before judging.

## Who owns what

Each person owns folders, so pull requests do not touch the same files. This follows the feasibility research's Part 4.1, with the shared file readers and the contract-terms reading given to backend-and-data, and the market-signals panel to frontend. The full layout is in [ARCHITECTURE.md](../ARCHITECTURE.md).

| Role | Folders | Slices | Build hours |
|---|---|---|---|
| captain | `schema/` except `readers.py`, `scans/memo/`, `eval/`, `demo/` | claim-result, readout, demo-freeze | 4.5 |
| frontend | `readout/`, and on Saturday the live re-run in `scans/signals/` | readout-page, market-signals | 4.5 |
| backend-and-data | repo root files, `server/`, `schema/readers.py`, `scans/video/`, `scans/readings/` | readers, pitch-video, contract-terms-saturday | 4.5 |
| design-and-finance | `scans/redflags/`, `scans/comps/` | redflag-engine, comps | 4.5 |

Build hours run from 10:30 AM to the 3:30 PM freeze, less a half-hour lunch: 4.5 hours each, 18 person-hours in all, from [check_saturday_hours.py](../../features/20261022.01_hackathon_plan/check_saturday_hours.py). The same script checks that each role's slices fill its window and that the run of show below gives each slice its stated hours. Rehearsal adds 45 minutes for all four.

The captain carries no schema typing (an agent writes it this week), no readers (backend-and-data owns them) and no post drafting (an agent drafts the posts this week). The captain posts at 11:00 and 3:30 only.

The agent slices from the first horizon are merged to `main` before Saturday. Each joins its Saturday slice at the integration points in the run of show.

`schema/` is frozen before Saturday, in the [skeleton](skeleton.md) slice. On Saturday only the captain changes it, and only to fix a bug. The exception is `schema/readers.py`, which backend-and-data fills in from 10:30 to 11:30. A new Python dependency goes through the captain, because the dependency list sits in a root file.

## A steer on stage (a card)

Ken's 1:12 PM and 1:15 PM comments let the operator steer the readout: an instruction on a piece rewrites it, or gets more info for it from new sources, with a visible diff ([steering](steering.md)). An agent builds steering before Saturday, and it joins the readout and the readout page on Saturday. Whether the three-minute core shows one steer live (one piece rewritten from one instruction, such as "treat the pilot as non-recurring") is the overview page's card. It has no owner or hours in the table above, because the build is done before Saturday. Showing it costs demo seconds, not build hours.

## The demo laptop

From the buildability critique's finding 11 and the demo critique's "What else goes wrong live":

- **The demo laptop is Ken's:** M2 Max, with ffmpeg, Python 3.13 and Node 20. Backend-and-data's laptop is the backup, on `demo/frozen/`.
- **The live step runs script checks only.** They need no network. Panels that need a model (the memo's connecting sentences, the comp reasons, the contract-terms readings) show frozen output. Nothing on screen calls a model at render time. A live steer, if the card puts one on stage, is the exception: it calls a model and needs the network, and its fallback is a saved steer from `demo/frozen/`.
- **Only the live beat needs the network.** The page and the frozen files are served from localhost, with no fonts or scripts from a CDN. The real company's outside-world panel needs venue wifi or the phone hotspot. Without either, it shows this week's saved copies with their dates, and Ken says so.
- **Display.** Every laptop brings a USB-C to HDMI adapter. Rehearse at 1280 by 720 at 150% zoom.

## Run of show

| Time | captain | frontend | backend-and-data | design-and-finance | Integration point |
|---|---|---|---|---|---|
| 9:00 to 10:00 | Breakfast and team formation. Confirm roles and folders. Ask the organisers about the track change and the board's open questions (TRI-track-fix, TRI-ask-organisers). Ask Akta's people for a coupon. | Clone, install, run the Part 0 checks. | Clone, check whisper.cpp runs on the demo laptop. | Clone, open the data room, read the check list. | Every laptop has the `.env` keys and a USB-C to HDMI adapter. |
| 10:00 to 10:20 | Organisers' intros and demos. Note any sponsor offer. | Listen. | Listen. | Listen. | |
| 10:20 to 10:30 | Read this table aloud. Name the demo fallback order. | Huddle. | Huddle. | Huddle. | |
| 10:30 to 11:30 | claim-result: quote checker, against the readers stub. At 11:00, post the first social post. | readout-page on the example files. | readers. | redflag-engine: pure checks on the CSVs and the model. | |
| 11:30 | Merge the readers and the quote checker. | Pull. | Pull. | Pull. | **1. Readers merged.** If they are late, the memo's model pass shows saved output on stage. |
| 11:30 to 12:30 | readout: memo. | readout-page. | pitch-video. | redflag-engine: the deck's claims page by regex, the green-flag cells, and the seed drop. | |
| 12:30 to 1:00 | Lunch at desks. | Lunch. | Lunch. | Lunch. | |
| 1:00 to 1:30 | demo-freeze: merge, first full run on the seed drop. | readout-page on real outputs. | pitch-video. | redflag-engine: the full room. | **2. First end-to-end run.** If the red-flag engine does not find the seed drop's flags, backend-and-data pairs with design-and-finance after the video slice, and contract-terms-saturday falls back if the pairing runs past 2:30. |
| 1:30 to 2:00 | readout: finish the piece verdicts, the top green and red flags, conflicts and corroborations, and the ask list. | readout-page: in-page source panels. | pitch-video. | redflag-engine: the clean room. | |
| 2:00 to 2:30 | demo-freeze: score script, frozen outputs. | readout-page: source panels and video jump. | pitch-video. | comps. | |
| 2:30 | Run the full room, the clean room and the approved real company's room, read the score. | | | | **3. Fallback call.** Whatever is not producing claims shows saved results on stage, in the demo fallback order. Nothing is dropped from the build. The agent slices that joined today run on the full room. |
| 2:30 to 3:30 | demo-freeze. | readout-page polish: the ask list's copy button and the reorder buttons, and the market-signals panel with its live run on the approved real company. | contract-terms-saturday. | comps. | |
| 3:30 | Tag `demo-freeze`. Post the second social post. The outside person sends the variant room's key. | | | | **4. Demo freeze.** |
| 3:30 to 4:15 | Rehearse, presenting: the three-minute core, then the five-minute extension. | Rehearse, driving the laptop. | Rehearse on the backup laptop. | Rehearse, ready for numbers questions. | Two run-throughs. |
| 4:15 to 4:30 | Fresh runs on the variant room and the clean room, close tabs. | Page ready on all rooms. Test the live outside panel on the approved real company on the demo network. | Backup laptop on the frozen files, including the variant and clean runs. | Answer key scores checked for the full room and the variant room. | |
| 4:30 to 5:30 | Judging: presents. | Drives. | Backup. | Answers questions on the numbers. | |
| 5:30 to 6:00 | Demos and the winner: presents. | Drives. | Backup. | Ready. | |

**Who presents:** the captain. The frontend drives the readout page. Backend-and-data holds the backup laptop with the frozen files. Design-and-finance answers questions on the numbers. For the $150 social content prize, the captain posts at 11:00 and 3:30 only, from this week's drafts ([social-posts](social-posts.md)), in the voice of [BRAND.md](../BRAND.md).

## Demo fallback order

Nobody drops a feature because the day runs long. This list says what the demo skips, or shows from saved results, when a piece is not working at the 2:30 PM fallback call or the 3:30 PM freeze. The piece is still built; it just does not run live in the three minutes. The order is the feasibility research's demo-value ranking reversed (red-flag engine, readout, pitch video, comps, market signals), with the memo's model pass first, because the script's top flags, pieces and verdicts carry the demo on their own ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), notes):

1. **The memo's model pass.** The readout shows its script-set top flags, pieces and verdicts without the connecting sentences.
2. **Market signals.** The panel shows this week's saved readings. If the panel itself is not working, the demo skips it.
3. **Comps.** The panel shows the cached comp list without the live ranking, or the demo skips it.
4. **Contract terms** (contract-terms-saturday). The pilot flag still shows from the engine's script check, without clause quotes.
5. **Pitch video.** The demo plays the captioned clip and shows this week's saved transcript and claims, which the feasibility research already plans as the fallback.
6. **An agent slice that joined today.** Steering, the memo export, the outside-in tabs, the bank check and the rest each show their last passing run from `demo/frozen/`, or the demo skips them.

The red-flag engine, the readout and the readout page are always shown; they are the demo. Inside the readout page, the reorder buttons fall back first, to the default order; the ask list and its copy button stay. When a piece falls back, its owner pairs with the owner of the slice that is behind, in that owner's folder and branch, so pairing never causes a merge conflict.
