# Tricorder

Point it at a startup, get a readout. Tricorder is the team and the product Ken St. Clair is captaining at Deal Flow, NYC's first VC hackathon, at Betaworks on Saturday 2026-10-24. Track: sourcing and diligence. The product takes a company (a URL, a deck, a pitch video, founder names) and runs a set of scans that end in a first-pass diligence memo with every claim sourced.

This file is the source of truth for every agent and every tool that opens this repo. `CLAUDE.md` is a link to it, so Claude Code, Codex, Cursor and anything else read the same rules. Teammates: read this once, then the board.

## Start every session here

1. `git pull origin main`.
2. Read `.who-am-i` in the repo root to learn whose agent you are (see "Know who you are" below). If it is missing, set it up before anything else.
3. Read `docs/BULLETIN.md`. First the Messages table: look for messages that @-mention your handle and answer them. Then the Board: newest rows first. Claim a row (`[>] @yourhandle`) before working it. If the work is not on the board, put it there first. "What's next" means: the top open row for your handle.
4. Read the ongoing docs the task touches (table below).
5. For a module or feature, start from `docs/ongoing/ROADMAP.md`: pick the top unblocked slice, open a feature folder under `docs/features/YYYYMMDD.NN_<slice>/`, and build it on `main`. Slices are written so one person or one agent can finish one in one sitting.
6. The plan this repo started from is `docs/features/20261022.01_hackathon_plan/00_overview.md`. The writers' brief behind it, with Ken's words and every decision so far, is `00_brief_for_writers.md` in the same folder.

## Know who you are

`.who-am-i` in the repo root holds one line: the handle of the teammate you work for, in lowercase (for example `ken`). Sign every message and every board row with it. The file is gitignored, so each laptop has its own.

If the file does not exist, your teammate has not been set up yet. Before any other work:

1. Ask your human for their first name and what they are working on today.
2. Create `.who-am-i` with their first name in lowercase as the only line.
3. Add them to the Team table below, in the same commit as step 4.
4. Post a hello in the Messages table of `docs/BULLETIN.md`: who they are and what they are taking on.
5. Commit and push those two files at once, so the other agents see the new teammate on their next pull.

## Talking to each other

Agents on different laptops talk through `docs/BULLETIN.md`. Nothing else carries a message between machines, so an unpushed message was never sent.

- **Messages go in the Messages table** at the top of the board: date, time, from, message. Newest first.
- **Use @-mentions** for a request or a handoff, for example `@sumit: the readout API returns flags now, see server/readout_routes.py`.
- **Take times from the clock** (`date +%H:%M`), never a guess. Dates as `YYYY-MM-DD`, times as 24-hour local.
- **End a message that still needs action with `**OPEN:**`** and what is outstanding. When it is answered, move the row to `docs/BULLETIN-ARCHIVE.md` under a dated heading with a `**RESOLVED:**` note.
- **Work goes on the Board, talk goes in Messages.** A request that is a piece of work becomes a board row for that handle; the message links to it.
- **Stay in your lane.** If your change touches a teammate's area (Team table), do not change their code quietly. Message them with what you need and why, and wait for their go-ahead or let them make it.
- **Contracts are news.** When you change a shape another part reads (an API route, a schema in `schema/`, a scan's output), post a message the same commit.
- **At session end**, post what you finished, what is unfinished or broken, and what the next agent needs to know.

## Pull constantly

Several agents push at once. Run `git pull origin main` at session start, before each new task, right before committing, between tasks, every 5 to 10 minutes on long work, whenever you read the board, and when the code does not look the way you expect. Re-read the Messages table after every pull.

When several agents share one checkout, one coordinating agent owns pull, commit and push; the workers do not. Give overlapping work separate worktrees. Never stash, reset or overwrite another agent's work to make a pull succeed. If a push is rejected, pull and reconcile, never force-push.

## Team

Add yourself here when you join. Your handle is your first name in lowercase.

| Name | Handle | Working on |
|---|---|---|
| Ken St. Clair | `@ken` | Captain. Product, research, the demo and the pitch. Check with @ken before changing scope, the readout's words, or the demo story. |

## Rules that always apply

- Everything on the roadmap is built by the end of Saturday. There is no later horizon.
- Every claim in a readout carries its source: a URL, a timestamp in the video, a line in the deck. A readout line with no source is a bug, not a feature.
- No number in a document comes from a model's head. Counts, percentages and date math come from a script or from calc-mcp, and the document names the script.
- A quote attributed to a real person needs a link to that person's own words right after it. No link, no quotation marks.
- Reddit blocks agents. A Reddit page enters this repo only when Ken saves it from his browser into a `reddit_corpus/raw/` folder. Agents emit URL lists for him and never fetch reddit.com.
- Plain words, one idea per sentence, no em dashes, in anything a person reads.
- Never delete files, branches or worktrees from an agent. List paths for Ken's cleanup instead.
- Work on `main` and push straight to it. No branches, no pull requests: this is a hackathon. Commit by path, small and often. Pull right before you commit. Before pushing code, run the checks for the part you touched (`bin/ci-py` for Python, `bin/ci-web` for the readout page) and push only when they pass. If `main` goes red in CI, whoever broke it fixes it first.
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
| `docs/ongoing/FEATURES.md` | Building or changing a feature: what each feature does in detail, its inputs and outputs, and the slice that builds it. |
| `docs/ongoing/USER_STORIES.md` | Building or changing a feature: the user story it serves, for the associate or the partner. |
| `docs/ongoing/PERSONAS.md` | Writing for or building for a kind of investor: their problem in their words, the proof. |
| `docs/ongoing/PERSONA_REVIEWS.md` | Reviewing a design, page or draft with the persona agents in `.claude/agents/`: which panel, how to run it, the report shape. |
| `docs/ongoing/BRAND.md` | Writing any copy: the readout, the pitch, the demo, posts. |
| `docs/ongoing/DEMO.md` | Preparing or rehearsing the Saturday demo: the rooms, the beat sheet, what runs live, the fallbacks. |
| `docs/ongoing/ARCHITECTURE.md` | Touching code structure, module boundaries, data sources, environment variables. |
| `docs/ongoing/STYLE_GUIDE.md` | Any frontend work. |
| `docs/ongoing/TESTING.md` | Writing or running tests, or reading what the CI command runs. |
| `docs/ongoing/diagrams/INDEX.md` | Finding a diagram of a flow before changing it. |
| `data_room/README.md` | Running any scan: the synthetic Hollis Voice room, how to regenerate it, and the answer key of planted flags. |
<!-- /seneschal:doc-table -->
