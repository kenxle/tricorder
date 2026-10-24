# Now to Friday night

Back to the [roadmap](../ROADMAP.md). This was the first horizon's introduction and its list of what was left before Saturday, as written on 2026-10-22 and 2026-10-23. Today's status of each slice is on the roadmap.

Building starts now, by agents and the team ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 3:32 PM block). Everything in the product brief and [FEATURES.md](../FEATURES.md) is built by the end of Saturday. This horizon holds the research, people work, data and documents, the [skeleton](skeleton.md), and every product slice that is not one of the team's Saturday slices. The organisers wrote that Saturday is build-only. Whether code written before Saturday is allowed is still asked on Ken's board row TRI-ask-organisers; until they answer, Ken has chosen to build now. The data room generator lives in `data_room/`, and no product folder imports it.

Most product slices here extend one of the team's Saturday slices. Each of those carries a **Joins on Saturday** line ([How to read a slice](how_to_read.md)). The product slices are listed in the order of their Waits on lines, after the setup slices.

**What is left before Saturday.** Nothing here waits on interviews; there are none (brief, 1:34 PM block). Checked against the repo on 2026-10-22.

- Done: [research-gaps](research-gaps.md), [checklist](checklist.md) and [data-room](data-room.md). The memo template ([MEMO_TEMPLATE.md](../MEMO_TEMPLATE.md)) is written too. Merged on 2026-10-23: [skeleton](skeleton.md) (PR #2), and [deck-vs-books](deck-vs-books.md), [accounting-mislabels](accounting-mislabels.md) and [checklist-coverage](checklist-coverage.md) (PR #4).
- [skeleton](skeleton.md): built by an agent and merged in PR #2 on 2026-10-23. It goes past the stub: the file readers and the quote checker are implemented and tested, so the [readers](readers.md) hour and the quote checker in [claim-result](claim-result.md) are free on Saturday unless Ken moves them.
- [blind-room](blind-room.md): Ken finds the person outside the build, who follows [SEALING.md](../../../data_room/SEALING.md) with their own seed and keeps the key. The plants-off switch, the clean room and the seed option are built.
- [keys](keys.md): Ken.
- [cached-data](cached-data.md): an agent, once Ken's keys are in. Not started: there is no `cache/` folder yet.
- [signals-readings](signals-readings.md): an agent, after cached-data and the skeleton's Claim schema.
- [saturday-specs](saturday-specs.md): an agent. The FRAMEWORKS entries exist. The example result files, the static readout mock and one test call per schema are still to do.
- [social-posts](social-posts.md): an agent drafts, Ken edits. Not drafted yet.
- [demo-script](demo-script.md): the beat sheet is below. Ken reads the core aloud against a timer.
- [yc-rooms](yc-rooms.md): Ken approves the list of real YC companies on the overview page's demo-company card. Then an agent generates a synthetic room for each approved company, and cached-data saves each company's outside-world calls.
- [record-pitch-video](record-pitch-video.md): Ken reads each room's script flatly, then installs whisper.cpp and saves the transcript.
- [founder-brief](founder-brief.md): Ken edits it in his own words.
- The product slices from [readout-store](readout-store.md) to [product](product.md): agents, in the order of their Waits on lines, with Ken where a slice names him.
