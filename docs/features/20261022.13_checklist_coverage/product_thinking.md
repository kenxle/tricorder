# Product thinking: checklist coverage

Source note for [01_brief.md](01_brief.md). Written 2026-10-22.

## User job

**Who.** The associate who prepares the memo, at a seed or Series A fund ([PERSONAS.md](../../ongoing/PERSONAS.md), "The associate who spends days gathering"). The partner reads the result second.

**Trigger.** A data room arrives, often thin. A founder sends a first tier before a first meeting and the rest on request. Hollis Voice's own cover note says so: "We share the second tier on request after a first meeting" (`data_room/hollis_voice/00_welcome/cover_note_and_index.pdf`, page 1).

**What they want.** The user story in their words: "When a fact is missing from the room, I want to see it marked as missing and put on a list of what to ask the founder for, so I ask for it instead of trusting a guess" ([USER_STORIES.md](../../ongoing/USER_STORIES.md)).

**What they do today.** They work from a published checklist and their own memory, by hand. The checklists disagree on what each stage should hold, which is why the checklist marks stage per item ([CHECKLIST.md](../../ongoing/CHECKLIST.md), "How to read the rows").

## Evidence and assumptions

Observed:

- A thin first tier is normal. The seed drop holds 12 of the full room's 17 files (`data_room/answer_key.json`, `seed_drop_files` and `full_room_files`).
- The checklist exists and is complete enough to drive a script: 109 items, with a stage column for each of the three stages ([checklist_counts.py](../../ongoing/checklist_counts.py), output quoted in [CHECKLIST.md](../../ongoing/CHECKLIST.md), "Counts").
- Investors read a missing document as a question, not a verdict. The brand rule: "A missing document is a question for the operator, not a flag on its own" ([BRAND.md](../../ongoing/BRAND.md), "A gap").
- Every document guide carries a one-line request for when the document is missing. The spike maps all 33 guides to 41 checklist document rows and pulls a request line for each of the 41. Five document rows have no guide: C23, C97, C99, C100 and C101 (`spike/coverage_spike.py`, `load_guides`).

Assumptions that could change the recommendation:

- **A1. Stage marks are right enough.** The stage columns come from the data-room research's table. 13 items are "not stated" at Series A ([CHECKLIST.md](../../ongoing/CHECKLIST.md), "Counts"). The spike treats "not stated" as not expected, as FRAMEWORKS does. If Ken wants those asked "if you have it", the Series A ask list grows.
- **A2. The associate wants the long list.** On the seed drop at Series A the spike writes 23 ask lines (`spike/print_counts.py`). A partner may want the top five. The prototype asks this.
- **A3. "Checked" can wait for scans.** No scan exists yet, so "checked" is projected in the spike. The panel only becomes honest once scans write claims with their check names.

## Priority

The roadmap puts this slice before claim-support and founder-requests, which both wait on it ([ROADMAP.md](../../ongoing/ROADMAP.md), "claim-support" and "founder-requests", Waits on). It joins two Saturday slices: the readout (the ask list) and the readout page (the coverage panel). It is an agent slice, outside the captain's and the frontend's Saturday hours.

What it displaces: agent time on stage-views or claim-support. Stage-views shares the stage reading and the operator's stage choice, so building the stage reading once here helps it.

## Options

- **Do nothing.** The Saturday ask list comes from gaps and weak pieces only ([FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), "Ask list"). It would never ask for IP assignments, minutes or tax returns, because no Saturday scan reads them.
- **A checklist view with no ask list.** Cheaper, but the ask list is where the associate acts.
- **Build it as a merge step (chosen).** A script in the memo's merge, after verdicts and before the ask list. No model call. The skeleton already reserves the step name `coverage` in `scans/memo/merge.py` (`STEPS`, on branch `claude/project-thread-ce34ga`).

## Recommendation

Build the coverage step and the ask-list lines it adds as a script, with stage read from the deck and changeable by the operator. Ship the panel's counts as a Panel so the frozen schema does not change before Saturday. Ask Ken four product questions (listed in [02_prototype_decision.md](02_prototype_decision.md)). The biggest scope question is the guides' proposed checks: the spike counts 176 of them across 33 guides (`spike/count_proposed_checks.py`), far more than one slice can build before Saturday.
