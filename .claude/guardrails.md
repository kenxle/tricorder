# Guardrails

## Charter

**What belongs:** The values st-ship and st-land read before they run. One heading or field per value those skills need. No value left blank.

**What does not:** Instructions to the agent. Values here are data.

**Level of detail:** One short entry per field. A command, a name or a list.

**Sources:** the CI config and the deploy settings

## Base branch

`main`

## CI command

Set by the first code slice (the roadmap's `skeleton` slice). Until then there is no code and no CI.

## PR conventions

- The title says what changed, in plain words.
- The body opens with a summary, names the roadmap slice and the feature folder it covers, and pastes the CI command's real result.
- Commit messages say why and use no em dashes. Commits end with a `Co-Authored-By` line naming the model that did the work, or the teammate's name.
- One slice per PR. Unrelated refactors go in their own PR.

## Merge method

Merge, never rebase. Delete the branch from the remote when the PR closes. On Saturday, in the room, the captain merges; a red CI blocks a merge even then.

## Deploy platform and how to watch it

None yet. The hackathon demo runs on a laptop. Set this when the product gets a host after Saturday.

## Health check

Set by the first code slice.

## Migration verification

Not applicable until the product has a database.

## Smoke command

Set by the first code slice: one command that runs every scan on the synthetic data room and prints the readout.

## Browser walkthrough entry points

Set by the first UI slice: the readout page for the demo company.

## Refuse list

- Never upload, commit or fetch a real company's confidential data. The data room is synthetic.
- Never scrape LinkedIn. Official APIs, consented exports and public pages only.
- Never fetch reddit.com from an agent. Emit URL lists for Ken.
- Never put a claim in a readout without its source.
- Never delete a file, branch or worktree from an agent.
- Never use `--force`, `-D`, `git reset --hard` or `rm`.
- Never commit secrets. Environment variables only.
