# pitch-video

The pitch video broken into claims with timestamps, third in the feasibility research's ranking.

- **Status today:** not started. Left: transcribe the video and pull its claims with timestamps.
- **Who builds it:** backend-and-data.
- **Waits on:** claim-result, readers (transcript by segment), record-pitch-video, keys (whisper.cpp on the demo laptop).
- **Horizon:** Saturday
- **Checked against:** no scans/video/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The pitch video broken into claims with timestamps, third in the feasibility research's ranking.

**Waits on:** claim-result, readers (transcript by segment), record-pitch-video, keys (whisper.cpp on the demo laptop).

**Includes:**

- ffmpeg makes a 16 kHz mono WAV; whisper.cpp transcribes it with timestamps (feasibility 1.5).
- The video prompt returns claims with the segment ids they came from, so start and end seconds are copied from the transcript, not guessed.
- Keyframes at scene changes for thumbnails, if the budget allows.
- `python -m scans.video <room>` writes `out/<room>/video.json`. If the live run fails, the scan reads this week's saved transcript and says so in the result.

**Done when:** `video.json` holds the ARR claim from the planted line, its time range covers the spoken sentence, and its quote passes the checker.

**Who:** backend-and-data.

**Hours:** 2.5 (11:30 AM to 2:30 PM, less lunch).

**Judgment:** no.
