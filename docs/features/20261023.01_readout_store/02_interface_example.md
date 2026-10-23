# Interface example: readout store

Nonvisual feature, so the prototype is this example. Every JSON block below was printed by a real run of [spike/store_spike.py](spike/store_spike.py) on the Hollis Voice room, never typed by hand. The run, on 2026-10-23:

```sh
S=<scratch>; export TRICORDER_OUT_DIR=$S/out
python3 -m scans.redflags data_room/hollis_voice     # redflags: 10 claims, 4 gaps
python3 -m scans.memo data_room/hollis_voice         # 10 claims, 0 unverified, 19 gaps
python3 docs/features/20261023.01_readout_store/spike/store_spike.py data_room/hollis_voice $S/spike_store $S/spike_cache
```

Simulated part, labelled: Hollis Voice is synthetic and has no outside pulls, so the spike writes one pretend saved page at `cache/outside/hollis_voice/website/home.html` and a two-entry `cache/index.json` (one entry for the company, one shared `signals/` entry that must survive). Everything else is the real readout, the real scan result and the real room files.

## The output

```json
{
  "save": {
    "version": 1,
    "new": true,
    "content_sha256": "03fa58fe28b0b7dbf364a170a6606d851cd4479104626a7384bd8d9637a1fbaf"
  },
  "save_again": {
    "version": 1,
    "new": false,
    "content_sha256": "03fa58fe28b0b7dbf364a170a6606d851cd4479104626a7384bd8d9637a1fbaf"
  },
  "list": {
    "fund": "demo",
    "company": "hollis_voice",
    "store_files": 19,
    "store": [
      "files/327789cd88034377bd1f8480a9a29806fd7dae40ad1ccaf8156f03958d4f7e93",
      "files/385c6dfd0f5407ca43c104bad3222071fa4ab02a3008e1f196414d693ae35af9",
      "files/42e14c40aba418d556f2970fb57c5e34812f64b363d48436fa5e9d4ac09d6ed5",
      "files/522507006f5491c6f7512c618963ff4d2c509feac45bce73e4a0f2ce8ef6e9d7",
      "files/5419371b7018da7a4fe7ffab443a523b202708b1d3294a6c1d1108831534c943",
      "files/5fe1ed10a203cb83357651fe94da404b6e480c76a7f7d21f38363b1f5b5a86ea",
      "... 13 more"
    ],
    "cache": [
      "outside/hollis_voice/website/home.html"
    ]
  },
  "delete": {
    "removed_store_files": 19,
    "removed_cache_files": 1,
    "index_entries_pruned": 1,
    "left_after": {
      "store": [],
      "cache": []
    }
  },
  "index_after": {
    "https://competitor.example.com/pricing": {
      "file": "signals/competitor_pricing.html",
      "read_at": "2026-10-23"
    }
  }
}
```

## What the spike settled

| Question | Answer from the run | Carried into |
|---|---|---|
| Is a rebuilt readout a new version? | No. The content hash leaves out `Readout.built_at` and `ScanResult.ran_at`, and the second save returned version 1 with `"new": false`. | STORE-R3 |
| What are "the files it read"? | Claim sources (5 files) plus `ScanResult.inputs` (16 files): 16 distinct room files, all copied. | STORE-R2 |
| Does the store need the scan results? | Yes. `readout.json` has no `inputs`; only `redflags.json` names the 16 files. | STORE-R1 |
| Can a delete clear `cache/` for one company without touching shared entries? | Yes: the company folder `cache/outside/<company>/` goes, the index entry pointing into it goes, and the `signals/` entry stays (`index_after`). | STORE-R7 |
| Is the listing readable? | No. It listed 19 store files by blob hash ("files/3277..."), which tells an investor nothing. The real `list` names each file by its room path, with its size and the versions that use it. | STORE-R5 |
| Same-file dedupe across versions? | Blobs are named by sha256, so a second version that read the same files copies nothing new. | STORE-R2 |

## Changes from the spike to the real interface

- The listing is built from the version manifests, not a folder walk, so it names room paths (`02_financials/financial_model.xlsx`), not blob hashes. The folder walk stays as the delete's check that nothing is left.
- Ids are validated before any path is built (the spike trusted them).
- A source uri that resolves outside the room is recorded as "not copied" and never read (the spike skipped it silently).
- Delete asks for confirmation on the CLI and needs `{"confirm": "<company id>"}` on the route.
- URL and API sources whose saved copy is in `cache/index.json` are copied too, so a readout with web sources also comes back with its files.
