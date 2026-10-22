# C2: Buildability critique

Written 2026-10-22 by the buildability critic. I read the plan as the engineer who has to make it work in the room. Counts and hours come from the read-only scripts named in "Local check results".

## Verdict

It builds by 3:30 only with changes. The data room is solid: its checker passes 188 of 188, and the deck and workbook parse cleanly. The plan around it has no slack: every role is budgeted at 4.5 of 4.5 build hours. The never-cut red-flag engine sits with the junior teammate, at 0.43 hours per check. And the score on stage would read 2 of 8 even if the engine worked, because six check names differ between the answer key and FRAMEWORKS. **The one change that most raises the odds: make Saturday's red-flag engine script-only.** Design-and-finance writes pandas checks and parses the deck's claims page by script (my regex read 14 of 14 rows). Backend-and-data owns the shared file readers and any model readings. Market signals is cut before 10:30 to pay for it.

## Findings, ranked by how much they change the outcome

**1. Six of eight check names disagree, so the score on stage would be wrong.** Severity: must fix before Saturday. Concerns [answer_key.json](../../../data_room/answer_key.json) and [FRAMEWORKS.md, "Where each planted flag is caught"](../../ongoing/FRAMEWORKS.md#where-each-planted-flag-is-caught).
- What is wrong: `eval/score.py` counts a flag as found by matching check names. Only `arr_from_subscription_rows` and `top_customer_share` match. The key says `deck_claim_vs_named_cell` where FRAMEWORKS says `deck_model_match`, and five more pairs differ the same way.
- Fix: pick one set of names and rename the other set this week. Then rerun `check.py`.

**2. The red-flag engine breaks first.** Severity: must fix before Saturday. Concerns [ROADMAP.md, redflag-engine](../../ongoing/ROADMAP.md#redflag-engine).
- What is wrong: a junior Python-and-Excel person has 3.0 hours for 7 checks. FRAMEWORKS gives Scan 1 eleven entries, each with a script, a prompt, a schema and label rules. The slice also needs a model call to read the deck, and a way to feed files to the model. Nobody else owns either.
- Fix: make Saturday's engine scripts only. The deck's claims page (slide 14) parses cleanly by regex. Every planted flag already has a script check (feasibility 3.2). Model readings, such as the pilot contract and the cohort note, move to backend-and-data after the video slice, or to after Saturday.

**3. Nobody owns the shared file readers.** Severity: must fix before Saturday. Concerns [FRAMEWORKS.md, "How documents reach the model"](../../ongoing/FRAMEWORKS.md#how-documents-reach-the-model) and [ARCHITECTURE.md, folder layout](../../ongoing/ARCHITECTURE.md#folder-layout).
- What is wrong: every scan and the quote checker need the same readers (PDF by page, xlsx by cell, CSV by row, markdown by line, transcript by segment). No folder owner has them. The captain has 0.5 hours for a quote checker across all five formats.
- Fix: one `schema/readers.py`, owned by backend-and-data from 10:30 to 11:30. The quote checker and every scan import it.

**4. The docs name paths that do not exist.** Severity: must fix before Saturday. Concerns [ARCHITECTURE.md, the data room and the answer key](../../ongoing/ARCHITECTURE.md#the-data-room-and-the-answer-key) and [ROADMAP.md, data-room and skeleton](../../ongoing/ROADMAP.md#data-room).
- What is wrong: both docs say `data_room/out/hollis_series_a/`, `out/hollis_seed_drop/`, `answer_key/planted_flags.json` and a `claims.json` sidecar. On disk the rooms are `hollis_voice/` and `hollis_voice_seed_drop/`, the key is `answer_key.json`, and there is no sidecar. So the skeleton's smoke test points at a missing folder, and the PDF fallback is absent.
- Fix: correct the paths in both docs. Have the generator write `01_overview/claims.json` into both rooms from the same list.

**5. Teammates cannot clone the repo.** Severity: must fix before Saturday. Concerns [BULLETIN.md, TRI-team-status (who accepted the invites)](../../BULLETIN.md).
- What is wrong: `kenxle/tricorder` is private and lists one collaborator, Ken.
- Fix: invite the three teammates' GitHub accounts as soon as they confirm.

**6. The Claim schema is the same model in both docs, but it is not ready to freeze.** Severity: should fix. Concerns [ARCHITECTURE.md, the Claim schema](../../ongoing/ARCHITECTURE.md#the-claim-schema) and [FRAMEWORKS.md, "Open points for builders"](../../ongoing/FRAMEWORKS.md#open-points-for-builders).
- What is wrong: the field names match in all five models (checked by script). The types do not:
  - ARCHITECTURE writes `unit` and `label` as free text, with "ARR" in capitals. FRAMEWORKS fixes them as lists: 8 units and 34 lowercase labels such as "arr".
  - `retrieved_at` is required in one and may be empty in the other.
  - ScanResult has no place for each entry's label and tables. The page needs those for the comps table, the signals grid and the video moments.
- Fix: make the FRAMEWORKS JSON Schema the single source and decide where the tables live this week. Then it is small enough to freeze.

**7. The skeleton card should go to option B.** Severity: should fix. Concerns [ROADMAP.md, skeleton-card](../../ongoing/ROADMAP.md#skeleton-card).
- What is wrong: with zero slack, option A spends the first half hour of two people and puts the team behind an 11:00 freeze. Example files cannot be checked against a schema that does not exist yet.
- Fix: choose B, limited to the card's list with no scan logic. Ken asks the organisers first and tells the judges plainly. If the organisers say no, keep A and cut market signals at 10:20.

**8. The captain carries too much.** Severity: should fix. Concerns [ROADMAP.md, who owns what](../../ongoing/ROADMAP.md#who-owns-what).
- What is wrong: Ken works in Rails, yet owns the Python schema, the quote checker, the memo and its model pass, the score script, every merge, the organiser questions and a social post at each integration point.
- Fix: option B removes the schema. Finding 3 removes the readers. An agent drafts the social posts this week, and Ken posts them at 11:00 and 3:30 only.

**9. Market signals cannot show much, so cut it before the day starts.** Severity: should fix. Concerns [FRAMEWORKS.md, Scan 3](../../ongoing/FRAMEWORKS.md#scan-3-market-signals-saturday).
- What is wrong: the demo company has no outside footprint. Akta's pay-as-you-go plan returns 403 on hiring, traffic and reviews. With one reading taken this week, every signal is labelled `one_reading`.
- Fix: show the cached competitor files as a static panel. Backend-and-data's 1.5 hours go to findings 2 and 3.

**10. The cache list misses what the comp prompts read.** Severity: should fix. Concerns [ROADMAP.md, cached-data](../../ongoing/ROADMAP.md#cached-data).
- What is wrong: entry 2.1 reads each candidate's 10-K Item 1 text, and 2.2 reads a saved page describing each Form D issuer. The slice lists neither. No rule maps a URL to its saved copy, which the quote checker needs.
- Fix: add both, plus a `cache/index.json` from URL to file.

**11. The demo laptop is never named, and the live step needs the venue's network.** Severity: should fix. Concerns [ROADMAP.md, run of show](../../ongoing/ROADMAP.md#run-of-show) and [the one workflow we demo](../../ongoing/ROADMAP.md#the-one-workflow-we-demo).
- What is wrong: no doc says which laptop is the demo laptop. The demo body runs the full room live, which makes model calls over venue wifi.
- Fix: use Ken's laptop (M2 Max, with ffmpeg, Python 3.13 and Node 20). The live step runs script checks only, which need no network. Model-backed panels show frozen output. Bring a phone hotspot. The forwarded email stays a screenshot.

**12. The pitch video has file traps.** Severity: should fix. Concerns [ROADMAP.md, record-pitch-video](../../ongoing/ROADMAP.md#record-pitch-video).
- What is wrong:
  - No rule keeps the video out of git, and [GitHub blocks files over 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
  - A phone recording may be HEVC, which not every browser plays.
  - whisper.cpp is not installed on Ken's laptop.
- Fix: convert the video once with ffmpeg to H.264 MP4 and share it outside git. Add the path to `.gitignore`. Install whisper.cpp and save the transcript.

**13 to 16. Notes.** Severity: note. Concerns [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md#open-points-for-builders), [ARCHITECTURE.md, folder layout](../../ongoing/ARCHITECTURE.md#folder-layout) and [ROADMAP.md, cut order](../../ongoing/ROADMAP.md#cut-order).
- `GM_PCT` holds 0.8 while the deck says 80% and FRAMEWORKS stores percent points. Add one conversion line to the check list, or the deck-against-model check reports a false conflict.
- Merge traps: `prompts/` is the captain's but every scan edits its prompts, so keep each prompt in its scan folder. List every package in the root file up front. `bin/ci` runs the React build, so a red TypeScript build blocks Python merges; split it into `bin/ci-py` and `bin/ci-web`, run by the captain before each merge. No hosted CI workflow exists.
- No structured-output schema has been sent once. Each Saturday schema has 7 to 11 fields that allow more than one type, under the API's documented 16 per request. Two entries in one request could pass it. Send one call per schema this week, and one schema per request on Saturday.
- The cut order (signals, comps, video) is right. Cut the memo's model pass and the red-flag model readings before any of them; ordering by script is enough for the demo.

## Prepare this week

- [ ] **Invite the three teammates to the GitHub repo.** Who: Ken. Waits on: TRI-team-status (who accepted the invites) and their GitHub usernames.
- [ ] **Align the check names and rerun `check.py`.** Who: agent. Waits on: nothing.
- [ ] **Have the generator write the `claims.json` sidecar into both rooms, and fix the paths in ARCHITECTURE and ROADMAP.** Who: agent. Waits on: nothing.
- [ ] **Settle one Claim schema, where entry tables live, and `spoken_tolerance`.** Who: agent drafts, Ken decides. Waits on: the overview card.
- [ ] **Decide the skeleton card.** If the answer is B, an agent writes the scaffold, schema and `readers.py` stub with no scan logic. Who: Ken. Waits on: the organisers' answer.
- [ ] **Write one `sample_out/` file per Saturday scan and validate each against the schema by script.** Who: agent. Waits on: the schema decision.
- [ ] **Test each Saturday prompt once against the real room files and save the outputs.** Also check which request settings Opus 5.5 refuses. Who: agent. Waits on: Ken's Anthropic key.
- [ ] **Fill `cache/`.** That means the Form D zips, XBRL facts, 10-K Item 1 text, issuer description pages, competitor pricing pages, Akta pulls and `cache/index.json`. Who: agent, with Ken for keyed calls. Waits on: keys and the competitor list.
- [ ] **Record the pitch video, convert it to H.264, and share it outside git.** Then install whisper.cpp and save the transcript. Who: Ken. Waits on: nothing.
- [ ] **Set up each laptop** with Python 3.13, uv, Node 20 and ffmpeg. Install the dependency list once in a throwaway folder outside the repo, so venue wifi is not the first download. Who: each teammate. Waits on: the dependency list.
- [ ] **Share `.env` through a password manager, not chat.** Who: Ken. Waits on: TRI-sponsor-keys (get the sponsor API keys).
- [ ] **Name the demo laptop and the backup laptop, and pack a hotspot.** Who: Ken. Waits on: nothing.
- [ ] **Draft the social posts in the brand voice.** Who: agent. Waits on: nothing.

## Local check results

Run on Ken's laptop on 2026-10-22, read only. Output is real, abridged with `...` and with short lines joined by `|`. The scripts (`facts.py`, `parse_check.py`, `claims_page.py`, `budget.py`, `union_count.py`) are in `/private/tmp/claude-501/-Users-kennethstclair-Documents-workspace-personal/084ee931-da9d-4fe6-8f9e-b5f26fa08a8a/scratchpad/c2/`.

```
Python 3.13.0 | node v20.19.0 | npm 10.8.2 | uv 0.10.4 | Apple M2 Max
ffmpeg version 8.0 (/opt/homebrew/bin/ffmpeg)
whisper-cli not found | whisper-cpp not found
==> whisper.cpp: stable 1.9.5 (bottled), HEAD ... Not installed
anthropic: ModuleNotFoundError | fastapi: ModuleNotFoundError
pydantic 2.12.5 | pandas 3.0.1
```

```
$ data_room/.venv/bin/python data_room/check.py
...
PASS  02_financials/financial_model.xlsx: 442 formula cells all carry stored values
...
188 passed, 0 failed
All planted flags and decoys are in the room exactly as the answer key says.
exit=0
```

```
parse_check.py
defined names include ARR_TOTAL, RUNWAY_MONTHS, GM_PCT
  ARR_TOTAL -> ARR_Build!$E$15 = 2240868
  RUNWAY_MONTHS -> Cash_Runway!$B$3 = 37
  GM_PCT -> P&L!$W$17 = 0.8
formula cells: 442 | formula cells with no cached value: 0
pitch_deck.pdf pages: 14 | slides with no text: [] | slides with images: [3, 6]
pilot agreement: found '2. Term and fees.' p1, '7. Termination.' p2, '8. No duty to convert.' p2

claims_page.py (seed drop deck, slide 14): rows parsed: 14
  three rows need a better label split, e.g. ('Calls handled, September', '2026 72,149', 3)
```

```
facts.py
key names missing from FRAMEWORKS: cumulative_column_shown_as_active,
  deck_claim_vs_named_cell, gross_margin_from_ledger,
  payroll_from_hiring_plan_and_rerun_cash, rebuild_cohorts_from_customer_file,
  spoken_arr_vs_claims_page
Saturday entries: 18 | red-flag entries: 11
Claim, Source, Value, Check, Gap: same field set in ARCHITECTURE and FRAMEWORKS: True (all five)
MISSING: data_room/out/hollis_seed_drop, data_room/out/hollis_series_a,
  data_room/answer_key/planted_flags.json, data_room/src, data_room/tests,
  hollis_voice/01_overview/claims.json, hollis_voice/01_overview/pitch_video.mp4,
  cache, sample_out, schema, scans
```

```
budget.py
build hours per person, 10:30 to 3:30 less lunch: 4.5
captain 4.5 | frontend 4.5 | backend-and-data 4.5 | design-and-finance 4.5
quote checker budget (11:00 to 11:30): 0.5
red-flag hours per Saturday check (7 checks in roadmap): 0.43

union_count.py: shared $defs 7; per Saturday schema with $defs: 7 to 11; none over 16

gh repo view kenxle/tricorder: {"isPrivate":true,"visibility":"PRIVATE"}; collaborators: kenxle
```
