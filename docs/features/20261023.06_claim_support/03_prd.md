# PRD: claim support

## Problem, user, context

See [01_brief.md](01_brief.md) and [product_thinking.md](product_thinking.md). The associate needs every pitch figure labelled against the rest of the room, with both sides shown when they disagree and an ask line when nothing backs it. Roadmap slice: [claim-support](../../ongoing/roadmap/claim-support.md).

## Scope

In:

- Every slide of `01_overview/pitch_deck.pdf`, including the claims page (the appendix).
- Every sentence of the pitch video's transcript (`01_overview/pitch_video.transcript.json`), or, until it exists, of `01_overview/pitch_video_script.md`.
- The room's own documents as evidence: the financial model, the cap table, the metrics export, revenue by customer, the hiring plan, customer contracts, founder bios.
- An optional model reading of each slide through `clients/llm.py`, for figures the script misses.
- A memo step that relabels claims against other scans' flags.

Out (non-goals for this slice):

- Claims in the company overview, the one-pager and the website copy. They are the same voice as the deck, so they can never support it; extracting them would only add repeats. A later slice can extract them to find figures the deck does not state.
- Outside sources (EDGAR, comps, signals). The evidence map names the room documents only; outside sources belong to scans 2 and 3.
- Rendering the table on the readout page. No page component renders Panels yet (Attention needed in [00_progress.md](00_progress.md)).
- Editing `scans/memo/merge.py`'s step list. The orchestrator adds the step.

## Requirements

| ID | Requirement |
|---|---|
| CS-R1 | Extract every figure (money, percent, count, year, date, month range, spelled-out number) from every content slide, with its slide as locator and the exact words as quote. |
| CS-R2 | Extract every figure from the claims page and fold each into the content-slide figure it repeats, listed as a repeat in the row and as a second source, never as support. |
| CS-R3 | Extract every figure from every transcript segment (locator `seg N`, with `start_s` and `end_s`) or, when there is no transcript, every script sentence (locator `line N`, with its beat), and say in the claim's text that it is the script and the video is not recorded yet. |
| CS-R4 | Normalise each figure to a kind with a unit, a period (as of the deck date, plan, last 12 months, or none) and a definition. Mark spoken figures spoken; mark a spoken figure rounded when it carries a hedge ("about", "close to") or has precision coarser than one unit. |
| CS-R5 | Keep an evidence map per kind: which documents should back it, with the checklist id of the document to ask for. |
| CS-R6 | Read each mapped document by script and compare within `match_tolerance` (printed figures widen by their printed precision), or within `spoken_tolerance` for rounded speech only. |
| CS-R7 | Label each claim: contradicted when an independent document disagrees (both shown); otherwise supported when one agrees; otherwise contradicted when the founder's own statements disagree with each other (both shown); otherwise unsupported. |
| CS-R8 | Treat the deck, the video and its script, the overview, the website, the one-pager and the claims.json export as one source. They never support each other. |
| CS-R9 | Write an unsupported kind as one Gap naming the document to ask for (with its checklist id), and give each unsupported row an ask line. Give each contradicted row an ask line to walk from the source data to the figure. |
| CS-R10 | Show the table as Panels: "claims table" (one row per claim), "claims table counts", and "claims not counted" (worked-example figures). |
| CS-R11 | Every claim passes the quote checker. |
| CS-R12 | Without `ANTHROPIC_API_KEY`, the model reading is a Gap, never a crash. A model fact whose quote is not on its slide, or whose number does not parse back, is dropped and counted in a Gap. |
| CS-R13 | The memo step relabels a supported or unsupported claim to contradicted when another scan's flag shares its pitch source or comes from a check that settles its kind, and shows the flag's sources. It records corroborating claims in `corroborated_by`, and shows a claim the quote checker moved as "could not verify". |
| CS-R14 | A row that only the financial model backs says, in its ask column, which rebuild check would test it, while that check has not run on the room. |
| CS-R15 | Use a planted entry's check name where the key expects one from this workflow: `spoken_arr_vs_claims_page` and `spoken_number_vs_claims_page` for a spoken figure the deck contradicts. |

## Failure cases

| ID | Case | Behavior |
|---|---|---|
| CS-F1 | No deck | No claims; one Gap asking for the deck. |
| CS-F2 | The deck's text cannot be read | `claims.json` stands in, with a Gap saying so. |
| CS-F3 | No transcript and no script | Deck claims only; a Gap for the video. |
| CS-F4 | Script but no transcript | Script lines stand in, cited by line; a Gap asks for the transcript. |
| CS-F5 | A mapped document is missing (seed drop) | The claim reads unsupported; its Gap says "file missing: ..." and names the document. |
| CS-F6 | A named cell or column is missing | That reading returns nothing; the claim falls through to the next document, or reads unsupported. Never a crash. |
| CS-F7 | Empty room | The scan exits 0 with Gaps. |
| CS-F8 | The model refuses or returns a bad shape | A Gap; script claims stand. |
| CS-F9 | A worked example on a slide | Its figures go to "claims not counted", never labelled. |

## Applicable UX

The words a person reads are the claim texts, the "where", "spoken", "agrees", "disagrees" and "ask" columns, and the gap lines. They follow BRAND.md: plain words, the figure as stated, the source named. The page layout is out of scope.

## Analytics, logging, rollout

None. The scan is on for every room once merged; the memo step is on once the orchestrator lists it.

## Questions

Open:

1. **Ken:** should the overview, one-pager and website be extracted too, to find figures the deck leaves out? Default: no for Saturday.
2. **Captain:** should the claims scan's deck-against-model contradictions take the check name `deck_claim_vs_named_cell`, so the key credits PF2, if FRAMEWORKS 1.5 is not built? Default: no; 1.5 owns that name.

Resolved:

- A figure only the model backs reads supported, with a note (CS-R14). The model is a separate document, but it is the company's own work.
- The claims page is a repeat, not a source (CS-R2, CS-R8).
