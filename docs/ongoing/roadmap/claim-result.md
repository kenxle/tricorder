# claim-result

The script that checks every quote against its source.

- **Status today:** partly built. Left: check URL sources against their saved copies (needs cache/).
- **Who builds it:** captain.
- **Waits on:** skeleton (the frozen schema and the readers stub), readers. The captain builds against the readers stub from 10:30 and switches to the real readers when they merge at 11:30.
- **Horizon:** Saturday
- **Checked against:** schema/check_quotes.py exists, no cache/index.json.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The script that checks every quote against its source. The typed Claim schema itself is written this week in the [skeleton](skeleton.md) slice.

**Waits on:** skeleton (the frozen schema and the readers stub), readers. The captain builds against the readers stub from 10:30 and switches to the real readers when they merge at 11:30.

**Includes:**

- `schema/check_quotes.py`: opens each claim's source at its locator through `schema/readers.py` and confirms the quote is there. URL sources are checked against their saved copies through `cache/index.json`. A claim that fails gets the confidence label `unverified` and moves to the "could not verify" box.

**Done when:**

- Tests show a real quote passing, an invented quote failing, and a claim with no source refused.
- Every example file in `sample_out/` passes the checker.

**Who:** captain.

**Hours:** 1.0 (10:30 to 11:30 AM).

**Judgment:** yes.
