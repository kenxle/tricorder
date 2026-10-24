# inbox-forward

The first inbox input: a forwarding address such as deals@ through a mail-receiving service.

- **Status today:** not started. Left: a forwarding address such as deals@ that starts a readout.
- **Who builds it:** agent.
- **Waits on:** readout-store; a domain and a mail-receiving service, which Ken picks.
- **Horizon:** Now to Friday night
- **Checked against:** no inbox code.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The first inbox input: a forwarding address such as deals@ through a mail-receiving service.

**Waits on:** readout-store; a domain and a mail-receiving service, which Ken picks.

**Joins on Saturday:** [readout](readout.md), which builds the readout for each new company folder.

**Includes:** PDF attachments go into a new company folder. DocSend, Google Drive, Dropbox and Notion links are fetched only when they open without a sign-in; otherwise the readout records a gap that says what the investor must do. It needs no OAuth review, which is why the brief recommends it first.

**Done when:** an email with a deck attached, sent to the forwarding address, creates a company folder holding the deck; an email with a DocSend link that needs a sign-in produces the gap that says what the investor must do; and the investor's delete removes the folder.

**Who:** agent.

**Judgment:** yes.
