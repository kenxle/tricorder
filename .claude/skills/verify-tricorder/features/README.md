# Tricorder verification map

This folder is the maintained source for proving Tricorder's user-facing behavior. Read this index before driving, then use the matching feature file as the recipe.

## Baseline preconditions

- Python dependencies from `requirements.txt` are installed, and Node 20 is on `PATH` for the page build.
- Set `TRICORDER_VERIFY_RUN` to a name for this run, so its results and evidence stay apart from other runs.
- Run `control.sh launch`, then `control.sh doctor`, and require an `OK` line naming this run.
- A fresh run has no scan results. Each recipe runs the scans it reads.
- Never drive an instance this run did not start.

## Driving conventions

- `control.sh` means `.claude/skills/verify-tricorder/control.sh`.
- Run commands through `control.sh cli`, API calls through `control.sh api`, and page captures through `control.sh shot`.
- Treat every room name, check name and route as literal.
- Read a stored result back through the API after the command that wrote it.

## Proof and skip reporting

- CLI proof is the saved transcript: the command, its output and its exit code.
- A claim is proven when its stored result is read back and `POST /api/rooms/<room>/source` returns text containing its quote.
- An answer-key result is proven by the `eval.score` transcript from this run. `eval.score` reads the readout, so run `scans.memo` on the room first, or it exits 2 with "no readout".
- Record the feature ID and entry point with every artifact.
- Report an unreachable path with the command tried and the missing precondition. Never report a skipped entry point as verified through another one.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph on what the user sees. Then exactly four H2 sections, in this order: `Sub-features`, `How to get to it (user POV)`, `Driving it with control.sh` (starting with `Preconditions:`), and `Gotchas`. Keep implementation details out; name only user paths, stable handles, required state, commands and observable proof.

## Features

- [Deck against books](./deck-vs-books.md) covers the deck's revenue figures against the P&L, and charts that leave out part of the history.
- [Accounting mislabels](./accounting-mislabels.md) covers the entry 1.12 sub-checks: non-recurring money in MRR, billings shown as revenue, pass-through money, contractors left out of burn, and the rest.
- [Checklist coverage and the ask list](./checklist-coverage.md) covers what the room holds for the company's stage and the lines to ask the founder for.
- [Readout page](./readout-page.md) covers the built page: flags, overview, gaps and the ask list for a room.
- [Readout store and delete](./readout-store.md) covers saving a readout with its sources and files per fund, listing everything held for a company, and the one confirmed delete.
