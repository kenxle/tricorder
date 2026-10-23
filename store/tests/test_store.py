"""The disk store, on the real Hollis Voice readout (STORE-R1 to R12)."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest

from schema.claim import Claim, Readout, ScanResult, Source
from scans.base import out_dir
from store import BadId, FileStore, NotHeld, open_store
from store.files import load_from_out

from .conftest import ROOM


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot(folder: Path) -> dict[str, tuple[int, int]]:
    return {str(p.relative_to(folder)): (p.stat().st_size, p.stat().st_mtime_ns) for p in folder.rglob("*") if p.is_file()}


@pytest.fixture()
def store(tmp_path, cache_dir) -> FileStore:
    return FileStore(root=tmp_path / "store_data", cache_dir=cache_dir)


@pytest.fixture()
def saved(store, out_env):
    readout, results = load_from_out(ROOM)
    return store.save("demo", "hollis_voice", readout, ROOM, results)


# Done when 1 -----------------------------------------------------------------

def test_saved_readout_comes_back_with_sources_and_files(store, out_env):
    readout, results = load_from_out(ROOM)
    result = store.save("demo", "hollis_voice", readout, ROOM, results)
    assert result.version == 1 and result.new

    back = store.get("demo", "hollis_voice")
    assert back.readout.model_dump(mode="json") == readout.model_dump(mode="json")
    assert [r.scan for r in back.results] == ["redflags"]
    assert back.results[0].inputs == results[0].inputs

    stored = {f.path for f in back.version.files}
    cited = {s.uri for c in readout.claims for s in c.sources if s.kind == "file"}
    assert cited and cited <= stored
    assert set(results[0].inputs) <= stored
    for path in stored:
        assert store.read_file("demo", "hollis_voice", path) == (ROOM / path).read_bytes()


def test_only_the_files_it_read_are_stored(store, out_env, tmp_path):
    room = tmp_path / "hollis_voice"
    shutil.copytree(ROOM, room)
    extra = room / "07_extra" / "not_read.txt"
    extra.parent.mkdir()
    extra.write_text("No claim and no scan read this file.", encoding="utf-8")
    readout, results = load_from_out(ROOM)
    store.save("demo", "hollis_voice", readout, room, results)

    held = store.list_company("demo", "hollis_voice")
    assert "07_extra/not_read.txt" not in {f.path for f in held.files}
    blobs = {p.name for p in (store.root / "demo" / "hollis_voice" / "files").iterdir()}
    assert _sha(extra) not in blobs
    readable = {p for p in room.rglob("*") if p.is_file()}
    expected = {f.path for f in held.files if f.origin == "room"}
    assert len(expected) < len(readable)


# Revisions and idempotence (STORE-R3) ---------------------------------------

def test_saving_the_same_readout_twice_adds_no_version(store, out_env):
    readout, results = load_from_out(ROOM)
    first = store.save("demo", "hollis_voice", readout, ROOM, results)
    rebuilt = readout.model_copy(update={"built_at": "2026-10-24T09:00:00Z"})
    rerun = [r.model_copy(update={"ran_at": "2026-10-24T09:00:00Z"}) for r in results]
    again = store.save("demo", "hollis_voice", rebuilt, ROOM, rerun)
    assert again.version == 1 and not again.new
    assert again.content_sha256 == first.content_sha256
    assert [v.version for v in store.list_versions("demo", "hollis_voice")] == [1]


def test_a_changed_readout_is_a_new_version_and_every_version_is_kept(store, saved, out_env):
    readout, results = load_from_out(ROOM)
    blobs_before = sorted((store.root / "demo" / "hollis_voice" / "files").iterdir())
    steered = readout.model_copy(update={"connecting": ["A steered sentence, citing redflags-001."]})
    second = store.save("demo", "hollis_voice", steered, ROOM, results)
    assert second.version == 2 and second.new
    assert store.get("demo", "hollis_voice").readout.connecting == steered.connecting
    assert store.get("demo", "hollis_voice", version=1).readout.connecting == readout.connecting
    assert [v.version for v in store.list_versions("demo", "hollis_voice")] == [1, 2]
    assert sorted((store.root / "demo" / "hollis_voice" / "files").iterdir()) == blobs_before
    # A, B, A: the third save is real history, not a duplicate of the latest.
    third = store.save("demo", "hollis_voice", readout, ROOM, results)
    assert third.version == 3 and third.new


# Done when 2 -----------------------------------------------------------------

def test_the_list_for_a_company_shows_everything_held(store, saved, cache_dir):
    held = store.list_company("demo", "hollis_voice")
    assert [v.version for v in held.versions] == [1]
    assert held.results == ["redflags"]
    assert {f.path for f in held.files} == {f.path for f in store.get("demo", "hollis_voice").version.files}
    assert all(f.versions == [1] for f in held.files)
    assert held.cache == ["outside/hollis_voice/hn/search.json", "outside/hollis_voice/website/home.html"]
    on_disk = [p for p in (store.root / "demo" / "hollis_voice").rglob("*") if p.is_file()]
    on_disk += [p for p in (cache_dir / "outside" / "hollis_voice").rglob("*") if p.is_file()]
    assert held.total_bytes == sum(p.stat().st_size for p in on_disk)
    assert store.companies("demo") == ["hollis_voice"]


# Done when 3 -----------------------------------------------------------------

def test_one_delete_leaves_nothing_for_that_company(store, out_env, cache_dir):
    readout, results = load_from_out(ROOM)
    store.save("demo", "hollis_voice", readout, ROOM, results)
    store.save("demo", "other_co", readout, ROOM, results)
    store.save("fund_b", "hollis_voice", readout, ROOM, results)

    report = store.delete_company("demo", "hollis_voice")
    assert report.left == []
    assert report.removed.versions == 1 and report.removed.cache_files == 2 and report.removed.index_entries == 2
    assert not (store.root / "demo" / "hollis_voice").exists()
    assert not (cache_dir / "outside" / "hollis_voice").exists()
    index = json.loads((cache_dir / "index.json").read_text())
    assert set(index) == {"https://other.example.com/", "https://competitor.example.com/pricing"}
    assert not any("hollis_voice" in json.dumps(v) for v in index.values())

    empty = store.list_company("demo", "hollis_voice")
    assert empty.versions == [] and empty.files == [] and empty.cache == [] and empty.total_bytes == 0
    with pytest.raises(NotHeld):
        store.get("demo", "hollis_voice")
    # Other companies and other funds stay.
    assert store.get("demo", "other_co").version.version == 1
    assert store.get("fund_b", "hollis_voice").version.version == 1
    assert (cache_dir / "outside" / "other_co" / "website" / "home.html").exists()
    assert (cache_dir / "signals" / "competitor_pricing.html").exists()


def test_deleting_a_company_with_nothing_held_removes_nothing(store, cache_dir):
    before = _snapshot(cache_dir)
    report = store.delete_company("demo", "never_saved")
    assert report.left == [] and report.removed.versions == 0 and report.removed.cache_files == 0
    assert _snapshot(cache_dir) == before


def test_delete_names_out_folders_it_leaves_alone(store, saved, out_env):
    report = store.delete_company("demo", "hollis_voice")
    assert report.also_on_this_laptop == [str(out_dir(ROOM))]
    assert (out_dir(ROOM) / "readout.json").exists()


def test_delete_refuses_a_symlinked_company_folder(store, tmp_path):
    outside = tmp_path / "precious"
    outside.mkdir()
    (outside / "keep.txt").write_text("keep", encoding="utf-8")
    (store.root / "demo").mkdir(parents=True)
    (store.root / "demo" / "evil").symlink_to(outside, target_is_directory=True)
    with pytest.raises(BadId):
        store.delete_company("demo", "evil")
    assert (outside / "keep.txt").exists()


# The store writes nothing in out/ or the room (STORE-R10) -------------------

def test_the_store_writes_nothing_in_out_or_the_room(store, out_env):
    out_before, room_before = _snapshot(out_env), _snapshot(ROOM)
    readout, results = load_from_out(ROOM)
    store.save("demo", "hollis_voice", readout, ROOM, results)
    store.get("demo", "hollis_voice")
    store.list_company("demo", "hollis_voice")
    store.delete_company("demo", "hollis_voice")
    assert _snapshot(out_env) == out_before
    assert _snapshot(ROOM) == room_before


# Ids and paths (STORE-R6, R2, R4) -------------------------------------------

BAD_IDS = ["", "..", ".", "../x", "a/b", "a\\b", "/etc", ".hidden", "Hollis", "x" * 65, "a b", "a.b", "-lead"]


@pytest.mark.parametrize("bad", BAD_IDS)
def test_a_bad_fund_or_company_id_is_refused_before_any_path(store, tmp_path, bad, out_env):
    readout, results = load_from_out(ROOM)
    before = sorted(str(p) for p in tmp_path.rglob("*"))
    calls = [
        lambda f, c: store.save(f, c, readout, ROOM, results),
        lambda f, c: store.get(f, c),
        lambda f, c: store.read_file(f, c, "01_overview/claims.json"),
        lambda f, c: store.list_company(f, c),
        lambda f, c: store.list_versions(f, c),
        lambda f, c: store.delete_company(f, c),
    ]
    for call in calls:
        with pytest.raises(BadId):
            call(bad, "hollis_voice")
        with pytest.raises(BadId):
            call("demo", bad)
    with pytest.raises(BadId):
        store.companies(bad)
    assert sorted(str(p) for p in tmp_path.rglob("*")) == before


def test_a_source_outside_the_room_is_never_read(store, out_env):
    readout, results = load_from_out(ROOM)
    crafted = readout.claims[0].model_copy(update={
        "id": "crafted-001",
        "sources": [Source(kind="file", uri="../answer_key.json", locator="line 1", quote="x")],
    })
    readout = readout.model_copy(update={"claims": readout.claims + [crafted]})
    result = store.save("demo", "hollis_voice", readout, ROOM, results)
    assert {"name": "../answer_key.json", "why": "outside the room"} in [n.model_dump() for n in result.not_copied]
    blobs = {p.name for p in (store.root / "demo" / "hollis_voice" / "files").iterdir()}
    assert _sha(ROOM.parent / "answer_key.json") not in blobs


@pytest.mark.parametrize("path", ["../../version.json", "../versions/0001/readout.json", "/etc/passwd", "02_financials/not_there.csv"])
def test_read_file_serves_only_the_manifest(store, saved, path):
    with pytest.raises(NotHeld):
        store.read_file("demo", "hollis_voice", path)


def test_get_an_unknown_company_or_version_is_not_held(store, saved):
    with pytest.raises(NotHeld):
        store.get("demo", "nobody")
    with pytest.raises(NotHeld):
        store.get("demo", "hollis_voice", version=9)


# URL sources and cache copies (STORE-R2) ------------------------------------

def test_a_url_source_is_copied_from_its_cache_copy(store, out_env, cache_dir):
    readout, results = load_from_out(ROOM)
    web = Claim(
        id="outside-001", scan="outside", text="The website says it answers every call.",
        check={"kind": "script", "name": "website_copy"}, confidence="quoted",
        sources=[
            Source(kind="url", uri="https://hollisvoice.example.com/", locator="p 1", quote="answers the phone"),
            Source(kind="url", uri="https://never-saved.example.com/", locator="p 1", quote="x"),
        ],
    )
    readout = readout.model_copy(update={"claims": readout.claims + [web]})
    result = store.save("demo", "hollis_voice", readout, ROOM, results)
    files = {f.path: f for f in store.get("demo", "hollis_voice").version.files}
    assert files["outside/hollis_voice/website/home.html"].origin == "cache"
    assert store.read_file("demo", "hollis_voice", "outside/hollis_voice/website/home.html") == (cache_dir / "outside/hollis_voice/website/home.html").read_bytes()
    assert {"name": "https://never-saved.example.com/", "why": "not in cache/index.json"} in [n.model_dump() for n in result.not_copied]


def test_a_scan_named_in_the_readout_with_no_result_is_recorded(store, out_env):
    readout, results = load_from_out(ROOM)
    readout = readout.model_copy(update={"scans_run": readout.scans_run + ["comps"]})
    result = store.save("demo", "hollis_voice", readout, ROOM, results)
    assert result.results_missing == ["comps"]
    assert store.get("demo", "hollis_voice").version.results_missing == ["comps"]


def test_load_from_out_without_a_readout_says_how_to_build_one(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(tmp_path))
    with pytest.raises(NotHeld, match="python -m scans.memo"):
        load_from_out(ROOM)


# All or nothing (STORE-R11) and configuration (STORE-R9, R12) ---------------

def test_a_half_written_version_is_ignored(store, out_env):
    junk = store.root / "demo" / "hollis_voice" / "versions" / ".tmp-crashed"
    junk.mkdir(parents=True)
    (junk / "readout.json").write_text("{half", encoding="utf-8")
    assert store.list_versions("demo", "hollis_voice") == []
    readout, results = load_from_out(ROOM)
    assert store.save("demo", "hollis_voice", readout, ROOM, results).version == 1


def test_open_store_reads_the_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("TRICORDER_STORE_DIR", str(tmp_path / "s"))
    monkeypatch.setenv("TRICORDER_CACHE_DIR", str(tmp_path / "c"))
    s = open_store()
    assert s.root == tmp_path / "s" and s.cache_dir == tmp_path / "c"
    monkeypatch.delenv("TRICORDER_STORE_DIR")
    monkeypatch.delenv("TRICORDER_CACHE_DIR")
    s = open_store()
    assert s.root.name == "store_data" and s.cache_dir.name == "cache"


def test_store_data_is_ignored_by_git():
    from scans.base import ROOT

    assert "store_data/" in (ROOT / ".gitignore").read_text().splitlines()


def test_saved_files_are_plain_json_a_person_can_read(store, saved):
    vdir = store.root / "demo" / "hollis_voice" / "versions" / "0001"
    Readout.model_validate_json((vdir / "readout.json").read_text())
    ScanResult.model_validate_json((vdir / "results" / "redflags.json").read_text())
    meta = json.loads((vdir / "version.json").read_text())
    assert meta["version"] == 1 and meta["room"] == "hollis_voice"
    assert os.listdir(vdir.parent) == ["0001"]
