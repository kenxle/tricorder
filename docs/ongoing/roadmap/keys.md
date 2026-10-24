# keys

Every key and account Saturday needs, in a local `.env` that is never committed, plus the demo laptop's tools.

- **Status today:** waiting on Ken. Left: the .env keys and the demo laptop's tools.
- **Who builds it:** Ken.
- **Waits on:** nothing. This is the board row TRI-sponsor-keys (get the sponsor API keys before Saturday).
- **Horizon:** Now to Friday night
- **Checked against:** no .env in the repo checkout.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Every key and account Saturday needs, in a local `.env` that is never committed, plus the demo laptop's tools.

**Waits on:** nothing. This is the board row TRI-sponsor-keys (get the sponsor API keys before Saturday).

**Includes**, from the feasibility research's Part 5:

- Anthropic API key. Required for every scan.
- Tavily key. Free 1,000 credits a month, no card.
- You.com key, or the keyless MCP profile (100 queries a day).
- GitHub token. Free; 5,000 requests an hour.
- Akta key, which comes on the day (see [sponsor-adapters](sponsor-adapters.md)), plus a question to the sponsor about the paid plan. Pay-as-you-go returns 403 on headcount, web traffic, jobs and reviews; those need the Subscription plan or a sponsor coupon.
- Product Hunt token. Optional; its terms say non-commercial use.
- OpenAI key. Optional; only for the Whisper API fallback.
- A declared EDGAR User-Agent string with a real contact address. No key.
- Not needed: HN Algolia, arXiv, Apple, ffmpeg, whisper.cpp. Skipped: Crunchbase (sales only), X (paid), Facebook (app review).
- whisper.cpp installed from Homebrew on the demo laptop, a model downloaded, and one run on a test clip, so the first run is not on stage.
- Each teammate runs the feasibility research's Part 0 checks on their own laptop.
- One test request to the Anthropic API from the command line, to find which request settings Opus 5.5 refuses (feasibility 1.10 says the bundled skill lists them, and no public page confirmed it).

**Done when:** the board row says which keys Ken has, and the EDGAR User-Agent test has run once without being blocked (feasibility 1.2).

**Who:** Ken.

**Judgment:** n/a.
