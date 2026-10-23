"""Derive three style directions for Tricorder from a datetime seed.

Ken asked for style directions inspired by a seed such as the hash of the
datetime. This script is that seed's only reader: it hashes the timestamp the
work started, cuts the digest into three slices, and uses each slice to pick
one entry from each table below. The tables are the design vocabulary; the
seed decides the mix. Run it again with the same timestamp and it prints the
same three directions.

    python3 seed_directions.py                       # the recorded seed
    python3 seed_directions.py 2026-10-22T19:51:56Z  # any other timestamp
"""

import hashlib
import json
import sys

SEED_TIME = "2026-10-22T19:51:56Z"  # when Ken's request reached this thread

# Worlds the look borrows its materials from. Each one belongs to the
# subject: a handheld scanner, an investor's paperwork, or a place where
# readings are checked against each other.
MOTIFS = [
    "field instrument: a handheld meter's display, bezel and engraved labels",
    "survey and cartography: contour lines, bench marks, grid references",
    "assay office: hallmarks, ledgers, the stamp that says a metal was tested",
    "air traffic strip board: paper flight strips in holders, one row per aircraft",
    "geological core log: a column of layers, each with its depth and reading",
    "oscilloscope and lab bench: graticule grids, phosphor traces, calibration marks",
    "court reporter's transcript: line numbers, exhibits, every statement cited",
    "weather service bulletin: station codes, observations, issued-at times",
    "museum conservation report: condition notes, object numbers, raking light",
    "shipping manifest and customs: declared against inspected, stamped lines",
    "medical chart and vitals monitor: ranges, normal bands, the out-of-range mark",
    "index card catalogue: drawers, call numbers, cross-references between cards",
]

# Type pairings, each with a display face, a body face and a data face, all
# on Google Fonts. None of them is Inter or Space Grotesk.
TYPE_PAIRS = [
    ("Fraunces", "Source Sans 3", "IBM Plex Mono"),
    ("Instrument Serif", "Instrument Sans", "JetBrains Mono"),
    ("Archivo", "Archivo", "Archivo Narrow"),
    ("Newsreader", "Public Sans", "Martian Mono"),
    ("Familjen Grotesk", "Literata", "DM Mono"),
    ("Bricolage Grotesque", "Atkinson Hyperlegible", "Fragment Mono"),
    ("Spectral", "Work Sans", "Red Hat Mono"),
    ("Sora", "Source Serif 4", "Azeret Mono"),
    ("Big Shoulders Display", "IBM Plex Sans", "IBM Plex Mono"),
    ("Libre Caslon Display", "Libre Franklin", "Cousine"),
]

DENSITY = ["airy: one idea per screen", "measured: a document's rhythm", "dense: a working instrument"]
GROUND = ["light ground", "dark ground", "light ground with one dark instrument band"]
SHAPE = ["square corners and hairlines", "soft 4px corners", "pill controls on square panels"]


def pick(table, number, taken=()):
    """Pick by the seed, stepping to the next entry if an earlier direction took it."""
    for step in range(len(table)):
        choice = table[(number + step) % len(table)]
        if choice not in taken:
            return choice
    return table[number % len(table)]


def spread_hue(hue, taken):
    """Keep each accent at least 60 degrees from the others: step by the golden angle."""
    for _ in range(12):
        if all(min(abs(hue - t), 360 - abs(hue - t)) >= 60 for t in taken):
            return hue
        hue = (hue + 137) % 360
    return hue


def directions(stamp):
    digest = hashlib.sha256(stamp.encode()).hexdigest()
    out = []
    # Three directions are only useful if they differ, so a direction never
    # repeats an earlier one's motif, type, density or ground.
    for i in range(3):
        cut = digest[i * 20:(i + 1) * 20]  # 20 hex digits per direction
        n = [int(cut[j:j + 4], 16) for j in range(0, 20, 4)]
        took = lambda key: [d[key] for d in out]
        type_names = pick(TYPE_PAIRS, n[2], [tuple(t.values()) for t in took("type")])
        out.append({
            "direction": "ABC"[i],
            "slice": cut,
            "motif": pick(MOTIFS, n[0], took("motif")),
            "accent_hue_deg": spread_hue(n[1] % 360, took("accent_hue_deg")),
            "type": dict(zip(("display", "body", "data"), type_names)),
            "density": pick(DENSITY, n[3], took("density")),
            "ground": pick(GROUND, n[4], took("ground")),
            "shape": pick(SHAPE, n[4] // 3),
        })
    return digest, out


if __name__ == "__main__":
    stamp = sys.argv[1] if len(sys.argv) > 1 else SEED_TIME
    digest, dirs = directions(stamp)
    print(json.dumps({"seed_time": stamp, "sha256": digest, "directions": dirs}, indent=2))
