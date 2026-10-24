# skeleton-card

A decision card for the overview page: does an empty repo skeleton count as code?

- **Status today:** done.
- **Who builds it:** Ken.
- **Waits on:** nothing. The critics weigh it ([brief, 10:18 AM block](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).
- **Horizon:** Now to Friday night
- **Checked against:** slice Status line: Ken's 3:32 PM decision settles it as option B.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

A decision card for the overview page: does an empty repo skeleton count as code?

**Waits on:** nothing. The critics weigh it ([brief, 10:18 AM block](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

**The two options:**

- **A. The skeleton is code. Build it on Saturday.** The folder layout, the CI command and the typed Claim result are the first Saturday slices. They take the first half hour of two people. Before Saturday the repo holds only documents, `data_room/` and `cache/`. To a judge who asks what was built today, the answer is every line of product code.
- **B. The skeleton is setup. An agent writes it this week.** Empty folders and packages, `bin/ci-py`, `bin/ci-web`, the CI config, the dependency list, `.env.example`, the Claim schema typed in from the FRAMEWORKS JSON Schema, and the `schema/readers.py` stub, with no scan logic. The captain and backend-and-data each get half an hour back on Saturday. The risk: the organisers wrote "On Saturday you only build" and "Everything a founder does before writing code happens this week", and commits dated before Saturday are visible to anyone who looks.

**Status:** Ken's 3:32 PM decision to build now settles this as option B. The organisers' answer is still asked on the board row.

**This roadmap is written to option B**, as the buildability critic recommends ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), finding 7). Its condition: Ken asks the organisers first and tells the judges plainly. The [skeleton](skeleton.md) slice sits in this week, and the freed half hours go to the slices the critics name: the captain's to the quote checker ([claim-result](claim-result.md)), and backend-and-data's to the shared file readers ([readers](readers.md)). If the organisers say no, the skeleton slice says what moves back.

**Who:** agent writes the card. Ken decides.

**Judgment:** n/a.
