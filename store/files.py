"""The store on disk, for the demo laptop.

    <root>/<fund>/<company>/versions/0001/version.json   VersionInfo with the file manifest
    <root>/<fund>/<company>/versions/0001/readout.json
    <root>/<fund>/<company>/versions/0001/results/<scan>.json
    <root>/<fund>/<company>/files/<sha256>               one copy per distinct content

The root is TRICORDER_STORE_DIR (default store_data/, ignored by git). Delete
also clears the company's outside pulls in TRICORDER_CACHE_DIR (default
cache/): the folder cache/outside/<company>/ and the cache/index.json entries
that point into it, but only when this fund held the company and no other
fund still does, because that folder is shared. The store never writes in
out/ or in a room.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import uuid
from pathlib import Path

from schema.claim import Readout, ScanResult
from scans.base import ROOT, now_iso, out_dir

from .base import BadId, NotHeld, check_id
from .models import (
    DeleteReport,
    HeldFile,
    Holding,
    Kept,
    NotCopied,
    Removed,
    SaveResult,
    StoredFile,
    StoredReadout,
    VersionInfo,
)

ROOM_SOURCE_KINDS = ("file", "video")
CACHE_SOURCE_KINDS = ("url", "api")


def default_root() -> Path:
    return Path(os.environ.get("TRICORDER_STORE_DIR") or ROOT / "store_data")


def default_cache() -> Path:
    return Path(os.environ.get("TRICORDER_CACHE_DIR") or ROOT / "cache")


def load_from_out(room_dir: Path) -> tuple[Readout, list[ScanResult]]:
    """The readout and the scan results it names, from the room's out folder.
    Read only; the store never writes there."""
    folder = out_dir(room_dir)
    target = folder / "readout.json"
    if not target.exists():
        raise NotHeld(f"no readout for {Path(room_dir).name}; run python -m scans.memo {room_dir} first")
    readout = Readout.model_validate_json(target.read_text(encoding="utf-8"))
    results = []
    for scan in readout.scans_run:
        path = folder / f"{scan}.json"
        if path.exists():
            results.append(ScanResult.model_validate_json(path.read_text(encoding="utf-8")))
    return readout, results


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(model, drop: str) -> bytes:
    data = model.model_dump(mode="json")
    data.pop(drop, None)
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def content_hash(readout: Readout, results: list[ScanResult], files: list[StoredFile]) -> str:
    """sha256 over the readout without built_at, each result without ran_at,
    and path=sha256 of every copied file. A rebuild that changes nothing but
    the time hashes the same."""
    h = hashlib.sha256()
    h.update(_canonical(readout, "built_at"))
    for result in sorted(results, key=lambda r: r.scan):
        h.update(b"\0" + _canonical(result, "ran_at"))
    for f in sorted(files, key=lambda f: (f.origin, f.path)):
        h.update(f"\0{f.origin}:{f.path}={f.sha256}".encode("utf-8"))
    return h.hexdigest()


def _index_file(value) -> str | None:
    """The saved file an index entry names: a path string, or an object with
    a 'file' or 'path' field."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("file", "path"):
            if isinstance(value.get(key), str):
                return value[key]
    return None


def _write_atomic(target: Path, data: bytes) -> None:
    tmp = target.with_name(f".tmp-{uuid.uuid4().hex}")
    tmp.write_bytes(data)
    os.replace(tmp, target)


class FileStore:
    def __init__(self, root: Path | None = None, cache_dir: Path | None = None):
        self.root = Path(root) if root is not None else default_root()
        self.cache_dir = Path(cache_dir) if cache_dir is not None else default_cache()

    # Paths ------------------------------------------------------------------

    def _fund_dir(self, fund: str) -> Path:
        check_id("fund", fund)
        return self.root / fund

    def _company_dir(self, fund: str, company: str) -> Path:
        check_id("fund", fund)
        check_id("company", company)
        folder = self.root / fund / company
        if folder.is_symlink() or (self.root / fund).is_symlink():
            raise BadId(f"{fund}/{company} is a link, not a folder the store made")
        if folder.exists() and not folder.resolve().is_relative_to(self.root.resolve()):
            raise BadId(f"{fund}/{company} resolves outside the store")
        return folder

    def _cache_company_dir(self, company: str) -> Path:
        return self.cache_dir / "outside" / company

    def _index(self) -> dict:
        path = self.cache_dir / "index.json"
        if not path.is_file():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    # Reading versions -------------------------------------------------------

    def _version_dirs(self, folder: Path) -> list[Path]:
        vdir = folder / "versions"
        if not vdir.is_dir():
            return []
        return sorted(d for d in vdir.iterdir() if d.is_dir() and d.name.isdigit() and (d / "version.json").is_file())

    def _info(self, vdir: Path) -> VersionInfo:
        return VersionInfo.model_validate_json((vdir / "version.json").read_text(encoding="utf-8"))

    def list_versions(self, fund: str, company: str) -> list[VersionInfo]:
        return [self._info(d) for d in self._version_dirs(self._company_dir(fund, company))]

    def _pick(self, fund: str, company: str, version: int | None) -> Path:
        dirs = self._version_dirs(self._company_dir(fund, company))
        if not dirs:
            raise NotHeld(f"nothing held for {fund}/{company}")
        if version is None:
            return dirs[-1]
        for d in dirs:
            if int(d.name) == version:
                return d
        raise NotHeld(f"{fund}/{company} has no version {version}")

    def get(self, fund: str, company: str, version: int | None = None) -> StoredReadout:
        vdir = self._pick(fund, company, version)
        info = self._info(vdir)
        readout = Readout.model_validate_json((vdir / "readout.json").read_text(encoding="utf-8"))
        results = [ScanResult.model_validate_json((vdir / "results" / f"{scan}.json").read_text(encoding="utf-8")) for scan in info.results]
        return StoredReadout(fund=fund, company=company, version=info, readout=readout, results=results)

    def read_file(self, fund: str, company: str, path: str, version: int | None = None) -> bytes:
        """A stored file by the path its manifest names. The path is only ever
        compared with the manifest, never joined onto a folder."""
        vdir = self._pick(fund, company, version)
        for f in self._info(vdir).files:
            if f.path == path:
                return (vdir.parent.parent / "files" / f.sha256).read_bytes()
        raise NotHeld(f"{fund}/{company} holds no file {path!r}")

    def companies(self, fund: str) -> list[str]:
        folder = self._fund_dir(fund)
        if not folder.is_dir():
            return []
        return sorted(d.name for d in folder.iterdir() if d.is_dir() and not d.is_symlink() and self._version_dirs(d))

    def list_company(self, fund: str, company: str) -> Holding:
        folder = self._company_dir(fund, company)
        versions = [self._info(d) for d in self._version_dirs(folder)]
        held: dict[tuple[str, str, str], HeldFile] = {}
        results: set[str] = set()
        for v in versions:
            results.update(v.results)
            for f in v.files:
                key = (f.origin, f.path, f.sha256)
                if key not in held:
                    held[key] = HeldFile(path=f.path, origin=f.origin, sha256=f.sha256, bytes=f.bytes, versions=[])
                held[key].versions.append(v.version)
        cache_files = self._cache_files(company)
        total = sum(p.stat().st_size for p in folder.rglob("*") if p.is_file()) if folder.is_dir() else 0
        total += sum((self.cache_dir / rel).stat().st_size for rel in cache_files)
        return Holding(
            fund=fund, company=company, versions=versions,
            files=sorted(held.values(), key=lambda f: (f.origin, f.path, f.versions)),
            results=sorted(results), cache=cache_files, total_bytes=total,
        )

    def _cache_files(self, company: str) -> list[str]:
        folder = self._cache_company_dir(company)
        if not folder.is_dir() or folder.is_symlink():
            return []
        return sorted(str(p.relative_to(self.cache_dir)) for p in folder.rglob("*") if p.is_file())

    # Saving -----------------------------------------------------------------

    def _gather(self, readout: Readout, room_dir: Path, results: list[ScanResult]):
        """The files the readout read: (files, sources on disk, not_copied)."""
        room = Path(room_dir).resolve()
        room_names: set[str] = set()
        cache_names: set[str] = set()
        for claim in readout.claims + readout.unverified:
            for s in claim.sources:
                if s.kind in ROOM_SOURCE_KINDS:
                    room_names.add(s.uri)
                elif s.kind in CACHE_SOURCE_KINDS:
                    cache_names.add(s.uri)
        for r in results:
            room_names.update(r.inputs)

        files: list[tuple[StoredFile, Path]] = []
        not_copied: list[NotCopied] = []
        for name in sorted(room_names):
            target = (room / name).resolve()
            if Path(name).is_absolute() or not target.is_relative_to(room):
                not_copied.append(NotCopied(name=name, why="outside the room"))
            elif not target.is_file():
                not_copied.append(NotCopied(name=name, why="not a file in the room"))
            else:
                data = target.read_bytes()
                files.append((StoredFile(path=name, origin="room", sha256=_sha(data), bytes=len(data)), target))

        index = self._index() if cache_names else {}
        cache_root = self.cache_dir.resolve()
        for name in sorted(cache_names):
            rel = _index_file(index.get(name))
            if rel is None:
                not_copied.append(NotCopied(name=name, why="not in cache/index.json"))
                continue
            target = (cache_root / rel).resolve()
            if Path(rel).is_absolute() or not target.is_relative_to(cache_root):
                not_copied.append(NotCopied(name=name, why="outside cache/"))
            elif not target.is_file():
                not_copied.append(NotCopied(name=name, why="saved copy missing from cache/"))
            else:
                data = target.read_bytes()
                files.append((StoredFile(path=rel, origin="cache", sha256=_sha(data), bytes=len(data)), target))
        # One entry per (origin, path).
        unique = {(f.origin, f.path): (f, p) for f, p in files}
        return [unique[k] for k in sorted(unique)], not_copied

    def save(self, fund: str, company: str, readout: Readout, room_dir: Path, results: list[ScanResult]) -> SaveResult:
        folder = self._company_dir(fund, company)
        by_scan = {r.scan: r for r in results}
        kept = [by_scan[s] for s in readout.scans_run if s in by_scan]
        missing = [s for s in readout.scans_run if s not in by_scan]
        files, not_copied = self._gather(readout, room_dir, kept)
        manifest = [f for f, _ in files]
        digest = content_hash(readout, kept, manifest)

        latest = self._version_dirs(folder)
        if latest and self._info(latest[-1]).content_sha256 == digest:
            info = self._info(latest[-1])
            return SaveResult(fund=fund, company=company, version=info.version, new=False, content_sha256=digest,
                              files_copied=0, bytes_copied=0, not_copied=info.not_copied, results_missing=info.results_missing)

        blobs = folder / "files"
        versions = folder / "versions"
        blobs.mkdir(parents=True, exist_ok=True)
        versions.mkdir(parents=True, exist_ok=True)
        copied = 0
        for f, source in files:
            blob = blobs / f.sha256
            if not blob.exists():
                _write_atomic(blob, source.read_bytes())
                copied += f.bytes

        tmp = versions / f".tmp-{uuid.uuid4().hex}"
        (tmp / "results").mkdir(parents=True)
        (tmp / "readout.json").write_text(readout.model_dump_json(indent=2) + "\n", encoding="utf-8")
        for r in kept:
            (tmp / "results" / f"{r.scan}.json").write_text(r.model_dump_json(indent=2) + "\n", encoding="utf-8")
        while True:
            dirs = self._version_dirs(folder)
            number = int(dirs[-1].name) + 1 if dirs else 1
            info = VersionInfo(
                version=number, saved_at=now_iso(), room=readout.room, built_at=readout.built_at,
                content_sha256=digest, claims=len(readout.claims), unverified=len(readout.unverified),
                gaps=len(readout.gaps), revisions=len(readout.revisions), results=[r.scan for r in kept],
                results_missing=missing, files=manifest, not_copied=not_copied,
            )
            (tmp / "version.json").write_text(info.model_dump_json(indent=2) + "\n", encoding="utf-8")
            try:
                os.rename(tmp, versions / f"{number:04d}")
                break
            except OSError:
                if not (versions / f"{number:04d}").exists():
                    raise
        return SaveResult(fund=fund, company=company, version=number, new=True, content_sha256=digest,
                          files_copied=len(manifest), bytes_copied=copied, not_copied=not_copied, results_missing=missing)

    # Delete -----------------------------------------------------------------

    def _index_entries_for(self, company: str) -> list[str]:
        prefix = f"outside/{company}/"
        out = []
        for key, value in self._index().items():
            rel = _index_file(value)
            if rel is not None and os.path.normpath(rel).replace(os.sep, "/").startswith(prefix):
                out.append(key)
        return out

    def _left(self, fund: str, company: str, cache_kept: bool) -> list[str]:
        """What is still on disk for this fund's company. The company's cache
        pulls count only when this delete was meant to remove them."""
        left = []
        folder = self.root / fund / company
        if folder.exists() or folder.is_symlink():
            left.append(str(folder))
        if not cache_kept:
            cache_folder = self._cache_company_dir(company)
            if cache_folder.exists() or cache_folder.is_symlink():
                left.append(str(cache_folder))
            left += [f"cache/index.json: {key}" for key in self._index_entries_for(company)]
        return left

    def _other_funds_holding(self, fund: str, company: str) -> list[str]:
        if not self.root.is_dir():
            return []
        others = []
        for d in sorted(self.root.iterdir()):
            if d.name == fund or d.is_symlink() or not d.is_dir():
                continue
            try:
                check_id("fund", d.name)
            except BadId:
                continue
            held = d / company
            if not held.is_symlink() and self._version_dirs(held):
                others.append(d.name)
        return others

    def delete_company(self, fund: str, company: str) -> DeleteReport:
        folder = self._company_dir(fund, company)
        cache_folder = self._cache_company_dir(company)
        if cache_folder.is_symlink():
            raise BadId(f"cache/outside/{company} is a link; not removing it")
        held = self.list_company(fund, company)
        rooms = sorted({v.room for v in held.versions})
        nothing_held = not held.versions
        # cache/outside/<company>/ is shared by every fund that looked at the
        # company (the outside-in scans write it without a fund). It goes only
        # when this fund held the company and no other fund still does.
        others = self._other_funds_holding(fund, company)
        kept: list[Kept] = []
        if cache_folder.exists() or self._index_entries_for(company):
            if nothing_held:
                kept.append(Kept(path=str(cache_folder), why=f"fund {fund} holds nothing for {company}, so its outside pulls in cache/ stay"))
            elif others:
                kept.append(Kept(path=str(cache_folder), why=f"still held for {company} by fund {', '.join(others)}, so the shared outside pulls in cache/ stay"))
        removed = Removed(
            versions=len(held.versions),
            files=len({f.sha256 for f in held.files}),
            results=sum(len(v.results) for v in held.versions),
            cache_files=0 if kept else len(held.cache),
        )
        if folder.exists():
            shutil.rmtree(folder)
        if not kept and cache_folder.exists():
            shutil.rmtree(cache_folder)
        doomed = set() if kept else set(self._index_entries_for(company))
        if doomed:
            index = self._index()
            keep = {k: v for k, v in index.items() if k not in doomed}
            _write_atomic(self.cache_dir / "index.json", (json.dumps(keep, indent=2) + "\n").encode("utf-8"))
            removed.index_entries = len(doomed)
        fund_dir = self.root / fund
        also = [str(out_dir(Path(room))) for room in rooms if out_dir(Path(room)).is_dir()]
        report = DeleteReport(fund=fund, company=company, nothing_held=nothing_held, removed=removed, kept=kept,
                              left=self._left(fund, company, cache_kept=bool(kept)), also_on_this_laptop=also)
        if fund_dir.is_dir() and not any(fund_dir.iterdir()):
            fund_dir.rmdir()
        return report
