# Voiceover for the Tricorder promo. Adapted from the Quote Desk promo's vo_v2.py.
# OPENAI_API_KEY comes from the shell environment. Never write it to a file.
# Writes audio/<name>_raw.wav, then audio/<name>.wav trimmed and fitted to its shot window.
# Run from this folder:  python3 vo.py           -> all lines
#                        python3 vo.py vo1 vo4   -> regenerate only those
import json, os, subprocess, sys, urllib.request

# (name, start second, max length in seconds, API speed, text). Text is verbatim from SHOT_LIST.md.
LINES = [
    ("vo1", 0.30, 4.75, 1.10, "Before an associate opens a data room, they already have ten tabs open."),
    ("vo2", 5.70, 4.00, 1.05, "Days go to gathering, before any thinking starts."),
    ("vo3", 10.50, 5.60, 1.10, "And when the deck, the model and the books disagree, it damages the deal."),
    ("vo4", 16.60, 2.80, 1.10, "Tricorder starts from a company's website."),
    ("vo5", 19.80, 5.50, 1.10, "It reads public sources and writes a first readout. Every point names its source."),
    ("vo6", 25.60, 2.60, 1.10, "Then it drafts the data room request."),
    ("vo7", 28.80, 6.20, 1.12, "When the room comes in, red and green flags lead: what the founder stated, beside what the room shows."),
    ("vo8", 35.60, 4.00, 1.10, "The partner reads an interactive memo, and can ask it questions."),
    ("vo9", 40.90, 2.80, 1.00, "Point it at a startup, get a readout."),
]
INSTR = ("Calm, plain, confident narrator for a short product film about investment research software. "
         "Even pacing with no long pauses. American accent. No hype, no sales voice.")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout.strip())


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for name, start, maxlen, speed, text in LINES:
        raw = f"audio/{name}_raw.wav"
        if (not only or name in only) or not os.path.exists(raw):
            body = json.dumps({"model": "gpt-4o-mini-tts", "voice": "ash", "input": text, "instructions": INSTR,
                               "response_format": "wav", "speed": speed}).encode()
            req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=body,
                                         headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
                                                  "Content-Type": "application/json"})
            open(raw, "wb").write(urllib.request.urlopen(req).read())
        trimmed = f"audio/{name}_trim.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse", trimmed], check=True)
        d = dur(trimmed)
        tempo = max(1.0, d / maxlen)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", trimmed, "-af", f"atempo={tempo:.4f}", f"audio/{name}.wav"],
                       check=True)
        print(name, f"raw {d:.2f}s", f"tempo {tempo:.3f}", f"final {dur(f'audio/{name}.wav'):.2f}s (window {maxlen})")
