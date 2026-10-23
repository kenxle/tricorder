"""Spike: the readout store's interface, tried once on the Hollis Voice room.

Throwaway. It settles what save, list and delete return before the real
`store/` package is written test first. Run it after building a readout:

    S=<scratch>; export TRICORDER_OUT_DIR=$S/out
    python3 -m scans.redflags data_room/hollis_voice
    python3 -m scans.memo data_room/hollis_voice
    python3 docs/features/20261023.01_readout_store/spike/store_spike.py \
        data_room/hollis_voice $S/spike_store $S/spike_cache

It prints one JSON document with four parts: save, save_again, list, delete.
The store and the cache it uses are scratch folders given on the command line.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from schema.claim import Readout, ScanResult  # noqa: E402
from scans.base import out_dir  # noqa: E402


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj: dict, drop: str) -> bytes:
    obj = {k: v for k, v in obj.items() if k != drop}
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def files_read(readout: Readout, results: list[ScanResult]) -> list[str]:
    names = {s.uri for c in readout.claims + readout.unverified for s in c.sources if s.kind in ("file", "video")}
    for r in results:
        names.update(r.inputs)
    return sorted(names)


def save(store: Path, fund: str, company: str, room: Path) -> dict:
    folder = out_dir(room)
    readout = Readout.model_validate_json((folder / "readout.json").read_text())
    results = [ScanResult.model_validate_json((folder / f"{s}.json").read_text()) for s in readout.scans_run]
    files = []
    for rel in files_read(readout, results):
        path = (room / rel).resolve()
        if not path.is_relative_to(room.resolve()) or not path.is_file():
            continue
        data = path.read_bytes()
        files.append({"path": rel, "sha256": sha(data), "bytes": len(data)})
    h = hashlib.sha256()
    h.update(canonical(readout.model_dump(mode="json"), "built_at"))
    for r in results:
        h.update(canonical(r.model_dump(mode="json"), "ran_at"))
    for f in files:
        h.update(f"{f['path']}={f['sha256']}".encode())
    content = h.hexdigest()

    base = store / fund / company
    versions = sorted((base / "versions").glob("*")) if (base / "versions").is_dir() else []
    if versions:
        last = json.loads((versions[-1] / "version.json").read_text())
        if last["content_sha256"] == content:
            return {"version": last["version"], "new": False, "content_sha256": content}
    n = len(versions) + 1
    vdir = base / "versions" / f"{n:04d}"
    (vdir / "results").mkdir(parents=True)
    (vdir / "readout.json").write_text(readout.model_dump_json(indent=2))
    for r in results:
        (vdir / "results" / f"{r.scan}.json").write_text(r.model_dump_json(indent=2))
    (base / "files").mkdir(exist_ok=True)
    for f in files:
        blob = base / "files" / f["sha256"]
        if not blob.exists():
            shutil.copyfile(room / f["path"], blob)
    meta = {"version": n, "room": readout.room, "built_at": readout.built_at, "content_sha256": content,
            "claims": len(readout.claims), "unverified": len(readout.unverified), "gaps": len(readout.gaps),
            "results": [r.scan for r in results], "files": files}
    (vdir / "version.json").write_text(json.dumps(meta, indent=2))
    return {"version": n, "new": True, "content_sha256": content}


def listing(store: Path, cache: Path, fund: str, company: str) -> dict:
    base = store / fund / company
    held = []
    if base.is_dir():
        for p in sorted(base.rglob("*")):
            if p.is_file():
                held.append(str(p.relative_to(base)))
    cached = []
    cdir = cache / "outside" / company
    if cdir.is_dir():
        cached = sorted(str(p.relative_to(cache)) for p in cdir.rglob("*") if p.is_file())
    return {"fund": fund, "company": company, "store_files": len(held), "store": held, "cache": cached}


def delete(store: Path, cache: Path, fund: str, company: str) -> dict:
    before = listing(store, cache, fund, company)
    shutil.rmtree(store / fund / company, ignore_errors=True)
    shutil.rmtree(cache / "outside" / company, ignore_errors=True)
    index = cache / "index.json"
    pruned = 0
    if index.exists():
        entries = json.loads(index.read_text())
        keep = {k: v for k, v in entries.items() if not v["file"].startswith(f"outside/{company}/")}
        pruned = len(entries) - len(keep)
        index.write_text(json.dumps(keep, indent=2))
    after = listing(store, cache, fund, company)
    return {"removed_store_files": before["store_files"], "removed_cache_files": len(before["cache"]),
            "index_entries_pruned": pruned, "left_after": {"store": after["store"], "cache": after["cache"]}}


def main() -> None:
    room, store, cache = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    # A pretend outside pull for the company, so delete has something in cache/ to remove.
    # Labelled simulated: Hollis Voice is synthetic and has no real web pages.
    page = cache / "outside" / "hollis_voice" / "website" / "home.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("<p>Simulated saved page for the synthetic company Hollis Voice.</p>")
    (cache / "index.json").write_text(json.dumps({
        "https://hollisvoice.example.com/": {"file": "outside/hollis_voice/website/home.html", "read_at": "2026-10-23"},
        "https://competitor.example.com/pricing": {"file": "signals/competitor_pricing.html", "read_at": "2026-10-23"},
    }, indent=2))
    out = {"save": save(store, "demo", "hollis_voice", room)}
    out["save_again"] = save(store, "demo", "hollis_voice", room)
    full = listing(store, cache, "demo", "hollis_voice")
    out["list"] = {**full, "store": full["store"][:6] + [f"... {len(full['store']) - 6} more"]}
    out["delete"] = delete(store, cache, "demo", "hollis_voice")
    out["index_after"] = json.loads((cache / "index.json").read_text())
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
