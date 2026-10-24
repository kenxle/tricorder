# record-pitch-video

Ken reads a few pitch scripts into video himself, flatly ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:51 PM block): "for the data room prep, we'll need to ask me to read a few scripts into a video. i'll just read them flatly, nothing crazy." One script per room: Hollis Voice, the second invented company, and each approved real-company room.

- **Status today:** not started. Left: Ken reads each script into pitch_video.mp4.
- **Who builds it:** Ken.
- **Waits on:** data-room (the script is written after the deck's claims page exists, research Part 3.6, step 7).
- **Horizon:** Now to Friday night
- **Checked against:** no pitch_video.mp4 in data_room/hollis_voice/01_overview/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Ken reads a few pitch scripts into video himself, flatly ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:51 PM block): "for the data room prep, we'll need to ask me to read a few scripts into a video. i'll just read them flatly, nothing crazy." One script per room: Hollis Voice, the second invented company, and each approved real-company room. The demo critic had suggested someone off stage record it, since judges who see the presenter play the founder may stop believing the room ([critique_demo.md](../../features/20261022.01_hackathon_plan/critique_demo.md), finding 5). Ken's decision stands; showing the clip as audio over the deck slides with captions, rather than his face, keeps that risk small.

**Waits on:** data-room (the script is written after the deck's claims page exists, research Part 3.6, step 7).

**Includes:**

- Ken's flat reading of each room's script (Hollis Voice: `01_overview/pitch_video_script.md`), over the deck slides, with the planted line at about 0:35 saying about three million dollars in ARR, against the deck's $2,500,000 (research Part 3.4, PF2b).
- A five-second clip of the 0:35 sentence, with burned-in captions, as an H.264 MP4. This clip is what plays on stage. The line is framed as the ladder: against the billing rows' $2,060,868, three million is 46% more (demo critique, finding 5).
- The video file copied into both rooms beside the script.
- A transcript made once by hand with whisper.cpp on the demo laptop and saved next to the video, so the demo has a result if the live run fails ([research_feasibility.md](../../reports/20261022.02_research/research_feasibility.md), 1.5).
- whisper.cpp is not installed on the demo laptop yet. Install it this week and save the transcript.
- A phone recording may be HEVC, which not every browser plays. Convert it once to H.264 MP4: `ffmpeg -i phone_recording.mov -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart pitch_video.mp4`.
- The video file stays out of git, because GitHub blocks files over 100 MiB. `.gitignore` lists `pitch_video.mp4` and `*.mov` under `data_room/`. Share the file outside git.

**Done when:** the video and the captioned clip play in the browser on the demo laptop, and the saved transcript contains the ARR sentence with its timestamp.

**Who:** Ken reads each script himself, flatly. On stage the clip plays as audio over the deck slides, with captions. For a real company's room, the clip carries the same synthetic label as the room, so Ken's reading never stands in for that company's founders.

**Judgment:** n/a.
