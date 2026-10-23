# PRD: steering in one sentence

Brief: [01_brief.md](01_brief.md). Prototype and persona review: [02_prototype_decision.md](02_prototype_decision.md). Roadmap slice: [steering](../../ongoing/ROADMAP.md#steering).

## Problem, user, context

The operator (the associate, or a partner who runs diligence alone) reads a readout line that is wrong, thin or framed badly. Today they cannot tell Tricorder so. This feature lets them type one sentence on that line or piece and see the piece rebuilt in place, with what changed.

## Scope

In: the rewrite steer and the more-info steer on one piece, the classifier with a model path and a wording-rule path, the number guard, the definition reread for "treat X as non-recurring", the full room as a more-info source, the verdict rebuild, the diff, the revision kept in the readout and the store, a server route, a page component and a standalone page that mounts it.

Out: fetching outside sources (filings, competitor pages) on a more-info steer; those wait on the outside-in clients and say so. Reader copies (reader-scenarios). Undoing a steer (every revision is kept, so a later slice can restore one). Folding older diffs on the page.

## Requirements

| ID | Requirement |
|---|---|
| STEER-R1 | The operator gives one sentence and a piece, and optionally the claim id of the line they typed on. Nothing else is asked: no kind, no form. |
| STEER-R2 | Tricorder reads the sentence as `rewrite` or `more_info`. With a model key set and not offline, a model reading through `clients/llm.py` decides; otherwise wording rules do. The revision says which path ran. |
| STEER-R3 | A model reading that names a term or number not in the sentence is refused, and the wording rules decide instead; the revision says so. A model refusal or error falls back the same way. |
| STEER-R4 | A sentence that asks for a different number (a number and no definition or source) changes no claim. The revision's note says the check's numbers stay, and quotes the line as the check wrote it. |
| STEER-R5 | A rewrite reruns the scans that feed the piece on the piece's room and takes the piece's claims from the fresh merge. |
| STEER-R6 | "Treat X as non-recurring" (and its plain variants) rereads each ARR line in the piece whose P&L line counts X as recurring: a script computes 12 x (that line less the P&L revenue line named for X) for the same month, from the room's cells, and adds one scenario claim that names the operator ("On Ken's steer, pilot not counted: ARR $2,060,868 ..."), states its gap against the deck on the books figure as the check measures its own, and cites the agreement's notice clause when `scans/redflags/contract_reader.py` finds an agreement for X. The scenario line becomes the piece's reason; the check's own line stays in the readout and moves into the diff as "before". The note says "Your scenario line is new. The original check still shows $2,240,868." With no P&L line named for X, nothing is added and the note says so. |
| STEER-R7 | A more-info steer that names the full room (or the second tier, or the rest of the room) on a seed drop opens the full room beside it as the new source, reruns every available scan there and rebuilds every piece, and adds the new claims marked new (their ids end `.steerN`). Claims the full room states the same way keep their ids. From then on the readout reads the full room: every line's source opens from it, and a second "read the full room" reads nothing new. The steer may be typed on the overview (piece `overview`), which accepts only a more-info steer. |
| STEER-R8 | A more-info steer that names a source Tricorder cannot open yet changes nothing and the note says what was asked for and that it is not fetched yet. |
| STEER-R9 | With a model path, a rewrite may reword the piece's lines. A rewording that adds, drops or changes a number, or drops "Reading:" from a judged line, is refused and the line keeps its words. |
| STEER-R10 | Every added or reworded claim is put through `schema/check_quotes.py` against the room its sources are in. One that fails goes to the could-not-verify box, and the note names it. |
| STEER-R11 | The piece verdicts and the top flags are rebuilt by the merge's `pieces` and `top_flags` steps when they exist, and by steering's copy of the FRAMEWORKS rules until they do. The revision says which ran. |
| STEER-R12 | The revision records the steer, the piece before and after, claims added and dropped, sources added, and the claims that moved the verdict when it moved. Wording changes, the reason line and the path go in a Panel named `steer N: what changed`. |
| STEER-R13 | The revision is appended to `Readout.revisions`, the readout is written back to `out/<room>/readout.json`, and the readout store saves it as a new version (`open_store().save`). |
| STEER-R14 | `POST /api/rooms/{room}/steer` runs a steer and returns the readout, the revision and the changes. `GET /api/rooms/{room}/steerable` returns the readout with verdicts. `GET /api/rooms/{room}/revisions` lists the revisions. `GET /api/rooms/{room}/claims/{claim_id}/sources/{i}` returns the text at a line's source, read from the room the line reads. |
| STEER-R15 | The page shows one box on the overview, one per piece and one per line, opened by a click. Enter sends. Until the first steer the box shows "For example: treat the pilot as non-recurring". The revised line appears where the operator typed, tagged with the author and time ("Ken's steer, Oct 23, 02:47 AM") or "new", in a colour that is not the checks' red, with the diff under it. A figure that names a panel opens the panel's rows. The page is mounted in `App.tsx` in place of the Overview section. |
| STEER-R16 | The diff's first line says what happened: "Added a scenario line.", "Read 5 new files; retention moved to Looking weak ...", "Refused: computed numbers do not change on request.", "Not fetched: ...", "Nothing changed: ...". It says when the reason line moved even if the verdict did not. The page states a room switch at the top. How the sentence was read and who rebuilt the verdicts stay in the note and the panel, and the page leaves them off. |
| STEER-R17 | `Steer.author` is the request's author, else the `TRICORDER_OPERATOR` setting, else empty ("the operator's"). |

## Failure cases

| Case | Behavior |
|---|---|
| Empty sentence, or over 500 characters | 422, nothing runs |
| Unknown piece, or a claim id not in the readout | 422 |
| No readout and no scan results for the room | 404 naming `python -m scans.redflags` and `python -m scans.memo` |
| "Read the full room" on a room with no seed-drop sibling | No change; the note says this room is already the full room or has no second tier beside it |
| A scan crashes on rerun | 500 naming the scan; the readout is not written |
| The store refuses the company id | The steer still applies; the response says the store did not save and why |

## Logging

The revision and its Panel are the log. Nothing else is written.

## Rollout

No flag. `SteerableSection` replaces the Overview section in `App.tsx`; `/steer.html` still serves it alone.

## Questions for Ken

1. **The definition steer makes a new figure.** Answer, from the coordinator on 2026-10-23: a definition steer may add a new figure, shown beside the check's, labelled as the steer's. The coordinator made that call; Ken can reverse it. So "treat the pilot as non-recurring" adds ARR of $2,060,868, computed by a script from two P&L cells and labelled "On Ken's steer", and the check's own $2,240,868 stays, shown as "before" in the diff. A check's number never changes because someone asked. To reverse it, the definition steer would only reword and point at mislabels' existing subscription-only line.
2. **Where the second tier comes from.** The full room is found as the seed drop's sibling folder (`hollis_voice_seed_drop` beside `hollis_voice`). On Saturday a second tier arrives by upload or inbox; it should land as that sibling.
3. **The pilot agreement.** Done: the scenario line cites the agreement's notice clause, read by `scans/redflags/contract_reader.py` (read-only).
