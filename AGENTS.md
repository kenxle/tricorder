# Tricorder (Agent Guide)

This file is the source of truth for any AI agent working in this repo: Claude Code, Codex, Cursor, or anything else. `CLAUDE.md` is a link to this file. If you are a human teammate, read it too; it is how the team's agents coordinate.

Point it at a startup, get a readout. Tricorder is the team and the product Ken St. Clair is captaining at Deal Flow, NYC's first VC hackathon, at Betaworks on Saturday 2026-10-24, Track 2: diligence. The product takes a company (a data room, a deck, a pitch video, a URL, founder names) and runs a set of scans that end in a first-pass diligence readout and memo with every claim sourced.

## Start every session here

1. `git pull origin main`.
2. Read `.agent-owner` (see "Know your identity" below).
3. Read [`docs/BULLETIN.md`](docs/BULLETIN.md). Look for messages that @-mention your owner.
4. Archive any resolved messages (see "Archiving" below).
5. Then start work, or take direction from your human.

## Workflow rules

- **Commit and push often.** After a change, commit and push to `main` without being asked. Several agents push to the same repo at once; unpushed work is invisible work. Small commits beat big ones.
- **Test as you go.** The cycle is: write code, write or update tests, run tests, fix failures, commit and push. Every commit should leave tests passing. New function: add a test. Bug fix: add a regression test.
- **Know your identity.** At the start of every session, read `.agent-owner` in the repo root. It holds one line: the name of the teammate you are working for (for example `Ken`). Use that name on the Bulletin Board. If the file does not exist, ask your human who they are right away, then create it. The file is gitignored, so each machine has its own.
- **Keep the architecture current.** When you change a component, a contract between parts, or a status, update your section of [docs/ongoing/ARCHITECTURE.md](docs/ongoing/ARCHITECTURE.md) in the same commit. Post on the bulletin board when a contract changes.
- **Stay in your lane.** If your work touches another teammate's domain (see Core Domains), do not silently change their code. Leave a Bulletin Board message @-mentioning them with what you need and why. Let them make the change, or at least get their go-ahead first.

## Bulletin Board

The board lives in [`docs/BULLETIN.md`](docs/BULLETIN.md). It is how agents talk to each other across machines.

- **After every pull**, re-read the board. Look for new messages @-mentioning your owner (for example `@Ken`). These are requests or handoffs meant for you. Skim the rest to see what changed.
- **At session end**, add a row with the date, the current time, your owner's name, and a short message covering:
  1. what you got done
  2. anything left unfinished or broken
  3. what the next agent needs to know
- **Use @-mentions** when you need something from someone or are handing off work (for example `@Ken: the API route is ready for the front end`).
- **Timestamps are required.** Date as `YYYY-MM-DD`, time as `HH:MM` (24-hour, local). Use the time from your system clock, not a guess.
- **Mark open items.** End any message that still needs action with `**OPEN:**` and what is outstanding.
- **Newest messages go at the top** of the table, so the freshest news is first.

The task list sits below the messages on the same page, under "Tasks". Claim a task (`[>] @yourhandle`) before working it. "What's next" means: the top open task for your handle.

### Archiving

When a message's action items are all resolved, move it from `docs/BULLETIN.md` to [`docs/BULLETIN-ARCHIVE.md`](docs/BULLETIN-ARCHIVE.md). This keeps the live board short.

- **Archive:** messages whose action items are done; informational notes everyone mentioned has seen; status updates that a later update replaced.
- **Keep:** anything with an open action item, an unfilled request, or an unanswered question.
- **How:** cut the rows from the board and paste them into the archive under a dated header (for example `## Archived 2026-10-24`). Add a `**RESOLVED:**` note saying why. Keep the original message text as written.
- **When:** at session start and at session end.

## Pull constantly

Several agents push to `main` at once. If you go a while without pulling, you will drift and hit merge conflicts. Run `git pull origin main`:

1. At session start, before reading code or making plans.
2. Before starting any new task.
3. Right before committing.
4. Between tasks.
5. Every so often during long stretches of work.
6. Whenever you read the Bulletin Board.
7. When code does not look the way you expect. Someone may have changed it.

## Parallel coding agents

- Pull before assigning work, between integration batches, and immediately before committing. During long tasks, check upstream at natural checkpoints, aiming for every 5 to 10 minutes.
- Re-read the bulletin after each pull. Reconcile new ownership or interface decisions before continuing.
- One coordinating agent owns Git mutations in a shared checkout. Workers do not pull, commit, or push independently. This is the worker exception to the session and commit rules above.
- Assign each worker a concrete task, acceptance criteria, owned files, and a starting commit. Use separate checkouts for overlapping edits. Never overwrite or stash another worker's work to make a pull succeed.
- Run reviewers against a stable revision. Integrate incoming changes at a safe checkpoint and rerun affected checks before publishing. If a push is rejected, reconcile upstream changes before retrying; never force-push shared main.
- Claude profiles live in `.claude/agents/`: `tricorder-implementer`, `tricorder-reviewer`, and `tricorder-debugger`. Reviewers are read-only. The coordinator validates findings and integrates changes. The `persona-*` agents there review designs and drafts as investors; see [PERSONA_REVIEWS.md](docs/ongoing/PERSONA_REVIEWS.md).
- Use Fable for complex implementation, decisions, and debugging. Use Claude Opus for independent review. Report model availability issues instead of silently substituting.

## Team

Teammates: add yourself here and in Core Domains when you join. Your @-handle is your first name.

| Name | Handle | Area(s) |
|------|--------|---------|
| Ken | `@Ken` | Product design, user research, product management, the demo and the pitch |
| Benjamin | `@Benjamin` | The TypeScript port: shared core, React web, React Native; room-requests |
| Kimmy | `@Kimmy` | Expert knowledge in each analysis |

## Core Domains

Each teammate owns a domain. Respect these boundaries and use the Bulletin Board for cross-domain requests.

| Name | Core Domain | Owns (files, folders, systems) |
|------|-------------|--------------------------------|
| Ken | Product (design, research, PM) | What we build and why: the product brief, features, roadmap, personas, research, the brand, the demo story and the synthetic data rooms. Lives in `docs/ongoing/`, `docs/reports/`, `data_room/`. Agents: check with @Ken before changing scope, the readout's words, or the demo story. |
| Benjamin | The TypeScript port | The shared TypeScript core, the React web app and the React Native app. See [typescript-port](docs/ongoing/roadmap/typescript-port.md). Agents: once Benjamin's port of a folder is announced on the board, change that folder in TypeScript, not Python. |

## Project overview

**Read the [product brief](docs/ongoing/PRODUCT_BRIEF.md) before you build anything.** It says what Tricorder is, who it is for, and the commitments every part of the build keeps. Then pick work from the [roadmap](docs/ongoing/ROADMAP.md): everything on it is built by the end of Saturday. The plan this repo started from is [the hackathon plan overview](docs/features/20261022.01_hackathon_plan/00_overview.md); the writers' brief beside it holds Ken's words and every decision so far.

### Rules that always apply

- Every claim in a readout carries its source: a URL, a timestamp in the video, a line in the deck. A readout line with no source is a bug.
- No number in a document comes from a model's head. Counts, percentages and date math come from a script or from calc-mcp, and the document names the script.
- A quote attributed to a real person needs a link to that person's own words right after it. No link, no quotation marks.
- Reddit blocks agents. A Reddit page enters this repo only when Ken saves it from his browser into a `reddit_corpus/raw/` folder. Agents emit URL lists for him and never fetch reddit.com.
- Never upload or commit a real company's confidential data. Every data room in the repo is synthetic.
- Never delete files, branches or worktrees from an agent. List paths for Ken's cleanup instead.
- Secrets come from environment variables only. Never commit a key, a token, or a teammate's personal data.

### Documentation map

Read what your work touches. Seneschal keeps the table current. Add your new documents to it when you create them.

<!-- seneschal:doc-table -->
| Document | Read when |
|---|---|
| `docs/ongoing/PRODUCT_BRIEF.md` | Any feature: what Tricorder is, who it is for, the scans, the principles. |
| `docs/ongoing/ROADMAP.md` | Picking what to build next and who builds it. Each slice's detail, what it must include and how we know it is done, is in `docs/ongoing/roadmap/<slice>.md`. |
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

## Repo structure

```
tricorder/
├── AGENTS.md              # This file (source of truth for agents)
├── CLAUDE.md              # Link to this file
├── data_room/             # Synthetic data rooms and their answer keys
├── schema/                # Shared shapes: Claim, readout, pieces
├── scans/                 # The scans (red flags, claims, memo, checklist)
├── steering/              # Operator steering and what-ifs
├── memo/                  # The interactive memo export
├── founder_requests/      # Requests to the company for missing items
├── store/                 # The readout store
├── server/                # The API (FastAPI)
├── readout/               # The readout page (Vite)
├── eval/                  # Scoring against the answer keys
├── clients/               # Outside data clients
├── bin/                   # serve, smoke, ci-py, ci-web
└── docs/
    ├── BULLETIN.md        # Live bulletin board (read every pull)
    ├── BULLETIN-ARCHIVE.md
    ├── ongoing/           # Product brief, roadmap, features, architecture, diagrams
    ├── features/          # One folder per feature
    └── reports/           # Research
```

## Development commands

- `bin/serve`: the API (and the built page) at http://127.0.0.1:8787. `bin/serve --dev` also starts the page's dev server on :5173.
- `bin/ci-py`: the Python tests and checks CI runs.
- `bin/ci-web`: the readout page's build and tests CI runs.
- `bin/smoke`: a quick end-to-end check.

## Git conventions

- Work on `main` and push often (this is a hackathon). Pull right before you commit.
- For a one-line message: `git commit -m "Short summary"`.
- For a longer message, write it to a gitignored scratch file and use `-F`:
  - Claude: `.claude-commitYYYYMMDDHHMM`, then `git commit -F .claude-commitYYYYMMDDHHMM`
  - Codex: `.codex-commitYYYYMMDDHHMM`, then `git commit -F .codex-commitYYYYMMDDHHMM`
- Do not add Codex, Claude, or other AI author marks or co-author trailers to commits. Use the human's configured Git identity.
- Never commit secrets. API keys go in `.env`, which is gitignored.

## Documentation

- All docs are Markdown.
- Diagrams use Mermaid, never ASCII art. Prefer top-down (`graph TD`).
- Keep diagrams in `docs/ongoing/diagrams/` current. When you change a flow that crosses module boundaries, update its diagram. If a diagram and the code disagree, fix the diagram.

## Writing style

- No em dashes. Use a comma, colon, semicolon, or period.
- Write plainly. One idea per sentence.
