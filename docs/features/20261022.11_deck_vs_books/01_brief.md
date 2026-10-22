# Short brief: deck-vs-books

Roadmap slice: [deck-vs-books](../../ongoing/ROADMAP.md#deck-vs-books). Feature: "Deck against the books" in [FEATURES.md](../../ongoing/FEATURES.md). Reasoning: [product_thinking.md](product_thinking.md).

## Who it is for

The associate who prepares the memo, first. The partner who reads it, second ([PERSONAS.md](../../ongoing/PERSONAS.md), [USER_STORIES.md](../../ongoing/USER_STORIES.md)).

## Context

A founder sends a deck and a data room. The deck shows revenue as a headline number, a chart and a growth line. The room holds the financial model, whose P&L tab has revenue by month. On Saturday the red-flag engine already compares the deck's claims with the model's named cells (`deck_claim_vs_named_cell`, [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) entry 1.5). It does not look at periods or at the chart.

## The problem

Two things go unchecked. A deck revenue figure can disagree with the P&L for its own period. A deck chart can start after the first revenue month and hide a fall. The associate's rule says either one makes everything else questionable.

## Desired outcome

Every revenue figure in the deck is matched to a P&L period, or listed as unmatched with a reason. A chart that starts late, skips months or shows quarters is flagged as "shows part of the history", with the months it leaves out and what they hold. Each result is a Claim with sources on both sides, so the readout can show it and the quote checker can confirm it.

## Known constraints

- Scripts only. No model call in the main path ([ROADMAP.md](../../ongoing/ROADMAP.md#redflag-engine), "Scripts only on Saturday").
- Files are read through `schema/readers.py`. Thresholds come from `schema.settings.load()`.
- It runs offline on the demo laptop.
- It must not double the engine's work. The ARR-against-`ARR_TOTAL` flag stays the engine's (PF2).

## The prototype and what it settled

This feature has no screen. The prototype is [02_interface_example.md](02_interface_example.md): the real Claim JSON the spike wrote on Hollis Voice, on three test decks, with the P&L hidden, and on Brasswick. It settled:

- The real Hollis Voice deck has no partial history. A test deck is needed, and the spike makes one from the room's own P&L without changing the room.
- Brasswick's planted BF2 is this feature's to catch, under the key's check name `deck_history_vs_metrics`.
- Chart bars can be read by script from pixels, scale free, with no new dependency.
- The P&L and the revenue rows disagree in some months for reasons that belong to other slices (BF4 on Brasswick, the pilot in the clean room). This feature reads the revenue rows as a cross-check only.

## Open questions

Carried to the PRD: Q1 (the ARR overlap with PF2), Q2 (flag or watch when the hidden months hold nothing bad), Q3 (a `revenue` value label).
