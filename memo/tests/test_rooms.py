"""memo/rooms.py: the rooms a readout's sources resolve in, and nothing outside them (review wave 2b, B1 and S2).

The switch marker is read by scans.memo.merge.reads_room (steering's); these tests pin what the memo relies on."""

from __future__ import annotations

import pytest

from schema.claim import Panel, Readout
from schema.readers import LocatorError
from scans.base import ROOT

from scans.memo.merge import reads_room

from memo.rooms import OutsideRoom, resolve, source_rooms

FULL = ROOT / "data_room" / "hollis_voice"
SEED = ROOT / "data_room" / "hollis_voice_seed_drop"
AT = "2026-10-23T12:00:00Z"


def _readout(*panels: Panel) -> Readout:
    return Readout(room=SEED.name, built_at=AT, panels=list(panels))


def _steer_row(to: str) -> Panel:
    return Panel(name="steer 1: what changed", columns=["Change", "Claim", "Before", "After"],
                 rows=[["source", "", SEED.name, to]])


def test_a_readout_reads_its_own_room_until_a_steer_switches_it():
    assert reads_room(None, SEED) == SEED
    assert reads_room(_readout(), SEED) == SEED
    assert source_rooms(reads_room(_readout(), SEED), SEED) == [SEED]


@pytest.mark.parametrize("marker", [
    Panel(name="reads room", columns=["Room", "Since"], rows=[["hollis_voice", "steer 1"]]),
    _steer_row("hollis_voice"),
])
def test_either_switch_marker_reads_the_full_room(marker):
    assert reads_room(_readout(marker), SEED).resolve() == FULL.resolve()
    assert [p.resolve() for p in source_rooms(reads_room(_readout(marker), SEED), SEED)] == [FULL.resolve(), SEED.resolve()]


@pytest.mark.parametrize("named", ["brasswick", "hollis_voice_clean", "../../", "/etc"])
def test_a_marker_naming_any_other_folder_is_ignored(named):
    marker = Panel(name="reads room", columns=["Room", "Since"], rows=[[named, "steer 1"]])
    assert reads_room(_readout(marker, _steer_row(named)), SEED) == SEED
    # A full room switches nothing on a room that is not a seed drop.
    assert reads_room(_readout(Panel(name="reads room", columns=["Room", "Since"], rows=[["brasswick", "steer 1"]])), FULL) == FULL


@pytest.mark.parametrize("uri", ["../../CLAUDE.md", "../answer_key.json", "/etc/hosts", str(FULL / "01_overview" / "claims.json"),
                                 "../brasswick/01_overview/claims.json", "", "."])
def test_resolve_never_leaves_the_rooms(uri):
    with pytest.raises(OutsideRoom):
        resolve(uri, [FULL, SEED])


def test_resolve_finds_a_file_in_the_first_room_that_holds_it():
    assert resolve("03_metrics/customer_mrr_by_month.csv", [FULL, SEED]).is_relative_to(FULL.resolve())
    with pytest.raises(LocatorError):
        resolve("03_metrics/customer_mrr_by_month.csv", [SEED])
