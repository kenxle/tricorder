"""The claims scan: every pitch figure, labelled against the room.

    python -m scans.claims <room_dir>

Script first, model second (FRAMEWORKS, "The order of work inside a scan").
The model only reads slides that hold no figure the script can parse, and only
when ANTHROPIC_API_KEY is set; without it those slides become a gap.
"""

from __future__ import annotations

from pathlib import Path

from schema.claim import ScanResult
from scans.base import Ids, gap, now_iso, room_inputs, room_name
from scans.claims import extract, label, read

NAME = "claims"
NEEDS = ("deck",)


def run(room_dir: Path) -> ScanResult:
    room = Path(room_dir)
    ids = Ids(NAME)
    gaps = []
    statements, notes, as_of, from_pdf = extract.deck_statements(room)
    if any("claims.json" in n for n in notes):
        gaps.append(gap("Not in the room: readable text in the pitch deck; its claims.json stands in, so only the claims page is read",
                        "the deck PDF has no text a reader can extract", "the pitch deck as a PDF with a text layer",
                        "the_pitch_itself"))
    if not statements and "no deck" in notes:
        gaps.append(gap("Not in the room: the pitch deck (01_overview/pitch_deck.pdf)", "file missing",
                        "the pitch deck as a PDF", "the_pitch_itself"))
    spoken, video_source = extract.video_statements(room)
    if video_source is None:
        gaps.append(gap("Not in the room: a transcript of the pitch video, or its script", "file missing",
                        "the pitch video with its transcript (pitch_video.transcript.json)", "the_pitch_itself"))
    elif video_source == "script":
        gaps.append(gap("Not in the room: a transcript of the pitch video; its script stands in, cited by line",
                        "the video is not recorded yet", "the pitch video with its transcript (pitch_video.transcript.json)",
                        "the_pitch_itself"))
    model_statements, model_gaps = read.read_slides(room, statements) if from_pdf else ([], [])
    gaps += model_gaps
    everything = statements + spoken + model_statements
    skipped = [s for s in everything if s.kind == "example"]
    items, label_gaps = label.label_all(room, everything, as_of, ids)
    gaps += label_gaps
    inputs = sorted({f for kind in ("deck", "deck_claims", "video", "video_script", "model", "cap_table", "metrics",
                                    "customers", "contracts", "hiring_plan", "bios")
                     for f in room_inputs(room).get(kind, [])})
    return ScanResult(scan=NAME, room=room_name(room), ran_at=now_iso(), inputs=inputs,
                      claims=[i.claim for i in items], gaps=gaps,
                      panels=label.panels(items, skipped, as_of, video_source))
