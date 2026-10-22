import json
from pathlib import Path

from eval.score import key_for, score
from schema.claim import Claim, Readout

DATA_ROOM = Path(__file__).resolve().parents[2] / "data_room"
KEY = json.loads((DATA_ROOM / "answer_key.json").read_text())


def _flag(check, uri, locator):
    return Claim.model_validate({
        "id": f"t-{check}", "scan": "redflags", "text": "A test flag.", "severity": "flag",
        "check": {"kind": "script", "name": check}, "confidence": "computed",
        "sources": [{"kind": "file", "uri": uri, "locator": locator, "quote": "x"}],
    })


def test_each_room_finds_its_key():
    assert key_for(DATA_ROOM / "hollis_voice").name == "answer_key.json"
    assert key_for(DATA_ROOM / "hollis_voice_seed_drop").name == "answer_key.json"
    assert key_for(DATA_ROOM / "hollis_voice_clean").name == "answer_key_clean.json"


def test_an_empty_readout_finds_nothing_and_flags_no_decoy():
    line, _ = score(Readout(room="hollis_voice", built_at="x"), KEY, "hollis_voice")
    assert line.found == 0 and line.planted == len(KEY["flags"]) and line.decoys_flagged == 0


def test_a_flag_with_the_check_name_and_a_key_file_counts_as_found():
    pf2 = next(f for f in KEY["flags"] if f["id"] == "PF2")
    loc = pf2["locations"][0]
    readout = Readout(room="hollis_voice", built_at="x", claims=[_flag(pf2["check"], loc["file"], "ARR_TOTAL")])
    line, lines = score(readout, KEY, "hollis_voice")
    assert line.found == 1 and any(l.startswith("found  PF2") for l in lines)


def test_a_flag_on_a_decoy_location_counts_against():
    dc1 = next(d for d in KEY["decoys"] if d["id"] == "DC1")
    loc = dc1["locations"][0]
    readout = Readout(room="hollis_voice", built_at="x", claims=[_flag("arr_from_subscription_rows", loc["file"], f"{loc['sheet']}!{loc['cell']}")])
    line, _ = score(readout, KEY, "hollis_voice")
    assert line.decoys_flagged == 1
