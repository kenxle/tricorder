# Product thinking: claim support

## The job

An associate opens a data room on Monday. The founder's deck and pitch video make about sixty checkable statements: ARR, customer counts, the largest customer's share, runway, burn, hires, the market, the round. The associate's job is to say, for each one, whether the rest of the room backs it, contradicts it, or says nothing. Today that is a spreadsheet built by hand over a day, and the figures the associate does not get to are the ones nobody checks.

Tricorder's job here: list every figure the founder states, say for each one which documents agree and which disagree, and turn every figure nothing backs into a line the associate can send to the founder.

## Evidence

- Ken's words in the writers' brief, 2:41 PM block: every claim in the deck and the pitch video, checked against every other document and the outside world ([00_brief_for_writers.md](../20261022.01_hackathon_plan/00_brief_for_writers.md)).
- The two demo rooms plant the job. Hollis Voice's deck says $2.5M ARR while the model says $2,240,868, the script says "about three million dollars", and the deck says "No customer above 9%" while one customer is 21.0% of subscription revenue. Brasswick's script says "close to three years" of runway while the deck says 29 months.
- The checklist (`docs/ongoing/checklist.csv`) already names the document that should back each kind of figure (C02 metrics export, C03 revenue by customer, C19 the model, C34 contracts). That is the evidence map's backbone.

## Who it is for

- **The associate**, first. They need the table: every figure, its label, both sides when two documents disagree, and an ask line when nothing backs it.
- **The partner**, second. They read the top flags. A contradicted pitch figure is a flag; a supported one is quiet.

## Assumptions

- Founder documents (the deck, the video, the overview, the website, the one-pager) are one voice. A figure repeated on the claims page or in the video is not a second source. Ken's rule, from the feature brief.
- The financial model is the company's own calculation but it is a different document from the pitch, so it counts as a source. When only the model backs a figure, the table says so, because the model can carry the same mistake as the deck (PF3 and PF6 live in the model).
- The pitch video is not recorded yet. The script stands in for the transcript, cited by line and labelled as the script, until `pitch_video.transcript.json` lands.

## Priority

High for Saturday. The claims table is the drill-down behind the top flags, and two planted entries (PF2b, BF5) are found only by comparing the spoken figure with the deck.

## Alternatives considered

- **Let the model read every slide and label every claim.** Rejected as the main path: no key in this container, the labels must be reproducible, and the done-when needs the quote checker to pass on every claim. The model reading is kept as an optional second pass that catches figures the script misses.
- **Only check the claims page (the appendix).** That is the Saturday baseline. It misses figures on content slides that the appendix leaves out (Hollis slide 4's 40 locations, slide 12's department hires) and every spoken figure.

## Corrections from Ken kept here

- "Independence: the deck, video, overview, website and one-pager count as one source" (feature brief).
- "Only tests and eval read the answer keys" (feature brief). No scan or memo step opens `answer_key*.json`.
