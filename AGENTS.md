# Tricorder

Point it at a startup, get a readout. Tricorder is the team and the product Ken St. Clair is captaining at Deal Flow, NYC's first VC hackathon, at Betaworks on Saturday 2026-10-24. Track: sourcing and diligence. The product takes a company (a URL, a deck, a pitch video, founder names) and runs a set of scans that end in a first-pass diligence memo with every claim sourced.

This file is the source of truth for every agent and every tool that opens this repo. `CLAUDE.md` is a link to it, so Claude Code, Codex, Cursor and anything else read the same rules. Teammates: read this once, then the board.

## Start every session here

1. Read `docs/BULLETIN.md`, the board. Newest rows first. Claim a row (`[>] @yourhandle`) before working it. If the work is not on the board, put it there first. "What's next" means: the top open row for your handle.
2. Read the ongoing docs the task touches (table below).
3. For a module or feature, start from `docs/ongoing/ROADMAP.md`: pick the top unblocked slice, open a feature folder under `docs/features/YYYYMMDD.NN_<slice>/`, and build it on a `feat/<slice>` branch. Slices are written so one person or one agent can finish one in one sitting.
4. The plan this repo started from is `docs/features/20261022.01_hackathon_plan/00_overview.md`. The writers' brief behind it, with Ken's words and every decision so far, is `00_brief_for_writers.md` in the same folder.

## Rules that always apply

- The hackathon is one day. Every slice says what it is for: before Saturday (groundwork), Saturday (the team, in the room), or after (productizing). A Saturday slice is sized in hours, not days.
- Every claim in a readout carries its source: a URL, a timestamp in the video, a line in the deck. A readout line with no source is a bug, not a feature.
- No number in a document comes from a model's head. Counts, percentages and date math come from a script or from calc-mcp, and the document names the script.
- A quote attributed to a real person needs a link to that person's own words right after it. No link, no quotation marks.
- Reddit blocks agents. A Reddit page enters this repo only when Ken saves it from his browser into a `reddit_corpus/raw/` folder. Agents emit URL lists for him and never fetch reddit.com.
- Plain words, one idea per sentence, no em dashes, in anything a person reads.
- Never delete files, branches or worktrees from an agent. List paths for Ken's cleanup instead.
- Commit by path, often. Docs-only changes push at once. Code changes land through a PR to `main`.
- Secrets come from environment variables only. Never commit a key, a token, or a teammate's personal data.

## Documents

Read these when the task touches them. Seneschal keeps the table current.

<!-- seneschal:doc-table -->
| Document | Read when |
|---|---|
| `docs/ongoing/PRODUCT_BRIEF.md` | Any feature: what Tricorder is, who it is for, the scans, the principles. |
| `docs/ongoing/ROADMAP.md` | Picking the next slice to build, or checking what a slice must include. |
| `docs/ongoing/FRAMEWORKS.md` | Building or changing a scan: the frameworks each scan runs, their inputs, their output shape. |
| `docs/ongoing/CHECKLIST.md` | Building or changing a scan, the coverage panel or the ask list: every item Tricorder looks for, by stage. |
| `docs/ongoing/MEMO_TEMPLATE.md` | Building the memo export, the interactive memo, reader copies or scenarios: the memo's sections in order, what fills each, and what stays the operator's. |
| `docs/ongoing/PERSONAS.md` | Writing for or building for a kind of investor: their problem in their words, the proof. |
| `docs/ongoing/BRAND.md` | Writing any copy: the readout, the pitch, the demo, posts. |
| `docs/ongoing/ARCHITECTURE.md` | Touching code structure, module boundaries, data sources, environment variables. |
| `docs/ongoing/STYLE_GUIDE.md` | Any frontend work. |
| `docs/ongoing/TESTING.md` | Writing or running tests, or reading what the CI command runs. |
| `docs/ongoing/diagrams/INDEX.md` | Finding a diagram of a flow before changing it. |
| `data_room/README.md` | Running any scan: the synthetic Hollis Voice room, how to regenerate it, and the answer key of planted flags. |
<!-- /seneschal:doc-table -->
