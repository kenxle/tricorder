# inbound-unasked

Diligence that starts on the inbound, before the investor asks.

- **Status today:** not started. Left: diligence that starts on the inbound email before the investor asks.
- **Who builds it:** agent.
- **Waits on:** inbox-forward.
- **Horizon:** Now to Friday night
- **Checked against:** no inbox code.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Diligence that starts on the inbound, before the investor asks.

**Waits on:** inbox-forward.

**Joins on Saturday:** [readout](readout.md) and [readout-page](readout-page.md), which fill in as results land.

**Includes:**

- The scans run when a deck arrives; the readout is one click away from the email, or the readout link is the reply. This is the brief's "before you even ask" moment.
- **Speed first** ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:19 PM block). Each scan starts the moment its input exists, not after the whole room is in: the outside-world tabs start on the company name, the deck scan on the deck, the model checks when the model lands. The readout fills in as results arrive, and each piece shows whether it is still running, done, or waiting on an input (which goes on the ask list).
- The operator sees the first green and red flags within the first scans' run, and is told when the readout is complete.

**Done when:** a forwarded email with only a deck produces a partial readout with the deck and outside-world pieces filled and the rest marked waiting; adding the model to the same company fills the financial pieces without rerunning the finished scans.

**Who:** agent.

**Judgment:** yes.
