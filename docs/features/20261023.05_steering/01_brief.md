# Brief: steering in one sentence

Roadmap slice: [steering](../../ongoing/ROADMAP.md#steering). Architecture: [ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md), "Steering". Product brief: [PRODUCT_BRIEF.md](../../ongoing/PRODUCT_BRIEF.md) and [FEATURES.md](../../ongoing/FEATURES.md), "Steering the readout". Reasoning: [product_thinking.md](product_thinking.md). Progress: [00_progress.md](00_progress.md).

## Target users

- The associate who prepares the memo and steers the readout into it.
- The partner who runs diligence alone. The bar is theirs: one plain sentence, no setup, the answer on the line they typed on.

## Problem

The readout is read-only. When the operator knows something the scans did not read (the pilot is not recurring revenue; the second tier of the room has arrived), there is no way to say so and see the readout follow.

## Desired outcome

1. On any piece or any line, the operator types one sentence and presses Enter. Nothing else: no form, no menu, no choice of kind.
2. Tricorder decides whether it is a rewrite or a request for more information, and says which reading path ran (model, or wording rules when no key is set).
3. The revised piece appears where they typed, with a diff: claims added and dropped, wording changed, the verdict before and after, and the claims that moved it.
4. A request for a different number leaves the number as the script computed it, and the revision says so.
5. Every revision is kept, in the readout and in the readout store.

## Known constraints

- `schema/` is frozen. `Steer` and `PieceRevision` exist; anything more goes in a proposal.
- `scans/memo/merge.py` is not edited. Verdicts come from its steps when they exist.
- No model call in a test, and no key in this container.
- Every rewritten claim passes `schema/check_quotes.py`.

## Questions the prototype answers

- Where does the box live: on every line, or one per piece? (Both, per the roadmap. The prototype tries a box that opens on the line clicked.)
- How much diff does a partner read before trusting the change?
- Is the new figure on a definition steer clear enough as the operator's, beside the check's own?
