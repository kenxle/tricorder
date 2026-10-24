# Brief: checklist coverage

Roadmap slice: [checklist-coverage](../../ongoing/roadmap/checklist-coverage.md). Rules: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), "Checklist coverage". Reasoning: [product_thinking.md](product_thinking.md). Progress: [00_progress.md](00_progress.md).

## Target users

- The associate who prepares the memo. They act on the ask list.
- The partner who reads the memo. They glance at the coverage counts to see how much of the room exists.

Both from [PERSONAS.md](../../ongoing/PERSONAS.md) and [USER_STORIES.md](../../ongoing/USER_STORIES.md).

## Context

A room arrives in tiers. The first tier is the deck, the model, the cap table and a few exports. The detail behind the numbers comes later, on request (`data_room/hollis_voice/00_welcome/cover_note_and_index.pdf`, page 1). What a room should hold depends on the stage: [CHECKLIST.md](../../ongoing/CHECKLIST.md) marks each of its 109 items yes, lighter, no or not stated for pre-seed, seed and Series A.

## Problem

The scans only notice what they need. Nothing tells the associate that the room has no IP assignments, no board minutes or no tax returns, because no Saturday scan reads them. So the Saturday ask list would miss them.

## Desired outcome

At the end of the readout:

1. A coverage panel. For the company's stage, each checklist item shows as checked, found, missing, not checked yet or not expected, with counts.
2. An ask list that also draws on the checklist. Every missing item the stage expects becomes a request, written in the words of its document guide. An item the stage only sometimes has is asked "if you have it". An item only a later stage expects is not asked for.
3. No request appears twice, even when a scan's gap and a checklist item name the same document.
4. The stage comes from the deck's round slide. The operator can change it, and the ask list changes with it.

## Known constraints

- No model call. The merge's steps are scripts ([FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), "Checklist coverage", Model reading: "None").
- The Claim schema is frozen before Saturday (`schema/claim.py` on branch `claude/project-thread-ce34ga`, docstring). Coverage has to fit `Readout`, `AskItem` and `Panel` as they are, or propose a change for the captain.
- A missing document is a question, never a red flag ([BRAND.md](../../ongoing/BRAND.md), "A gap").
- Every room is synthetic. Every count comes from a script.

## Open questions that affect the prototype

Answered by trying them in the [prototype](02_prototype/prototype.html); the rest wait on Ken in [02_prototype_decision.md](02_prototype_decision.md).

- How long is the ask list? Seed drop at Series A: 23 lines, 2 of them "if you have it" and 3 for after the term sheet (`spike/print_counts.py`).
- What changes when the operator moves the stage? Seed drop, pre-seed: 11 lines, and 5 gap requests are held back because pre-seed does not expect them (`spike/print_counts.py`).

## What the prototype review settled

Persona review and Ken's review are pending. See [02_prototype_decision.md](02_prototype_decision.md).
