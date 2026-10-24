# readers

The shared file readers every scan and the quote checker import.

- **Status today:** done.
- **Who builds it:** backend-and-data.
- **Waits on:** skeleton (the `schema/readers.py` stub, written this week).
- **Horizon:** Saturday
- **Checked against:** schema/readers.py implemented and tested in the skeleton (PR #2).

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The shared file readers every scan and the quote checker import. Before this slice nobody owned them, and the captain had half an hour for a quote checker across all five formats ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), finding 3).

**Waits on:** skeleton (the `schema/readers.py` stub, written this week).

**Includes:**

- `schema/readers.py` filled in: PDF by page, xlsx by cell, CSV by row, Markdown by line, transcript by segment. Each returns the text at a locator, so a scan can quote it and the quote checker can find it again.
- The quote checker and every scan import these readers. No scan writes its own.

**Done when:** a test reads one known locator from each of the five formats in `data_room/hollis_voice/` and gets the expected text, and the readers are merged at 11:30 AM.

**Who:** backend-and-data.

**Hours:** 1.0 (10:30 to 11:30 AM).

**Judgment:** no.
