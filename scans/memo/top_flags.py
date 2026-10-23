"""Pick one headline per piece using FRAMEWORKS, 'Top green and red flags'."""

from pathlib import Path

from schema.claim import PIECE_ORDER, Readout, TopFlag
from schema.settings import load
from scans.memo.pieces import corroborated, independent_sources, red_gap


def apply(readout: Readout, room_dir: Path) -> Readout:
    settings = load()
    by_id = {c.id: c for c in readout.claims if c.confidence != "unverified"}
    green_candidates, red_candidates = [], []
    for i, name in enumerate(PIECE_ORDER):
        piece = next((p for p in readout.pieces if p.name == name), None)
        if piece is None:
            continue
        claims = [by_id[cid] for cid in piece.claim_ids if cid in by_id]
        if piece.verdict == "looking_strong":
            candidates = [c for c in claims if corroborated(c, by_id)]
            if candidates:
                best = max(candidates, key=lambda c: len(independent_sources(c, by_id)))
                green_candidates.append((len(independent_sources(best, by_id)), i, best, name))
        ranked = [(red_gap(c, by_id), c) for c in claims if c.severity == "flag"]
        ranked = [(gap, c) for gap, c in ranked if gap is not None]
        if ranked:
            gap, worst = max(ranked, key=lambda item: item[0])
            red_candidates.append((gap, i, worst, name))
    green_candidates.sort(key=lambda row: (-row[0], row[1]))
    red_candidates.sort(key=lambda row: (-row[0], row[1]))
    flags = [TopFlag(kind="green", piece=name, rank=n, text=c.text, claim_ids=[c.id])
             for n, (_, _, c, name) in enumerate(green_candidates[:int(settings["top_green_flags"])], 1)]
    flags += [TopFlag(kind="red", piece=name, rank=n, text=c.text, claim_ids=[c.id])
              for n, (_, _, c, name) in enumerate(red_candidates[:int(settings["top_red_flags"])], 1)]
    return readout.model_copy(update={"top_flags": flags})
