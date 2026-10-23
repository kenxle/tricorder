"""The readout store: each readout, its scan results and copies of the files
it read, per fund and company, every version kept, one delete for a company.

    from store import open_store
    store = open_store()
    store.save("demo", "hollis_voice", readout, room_dir, results)

Design: docs/features/20261023.01_readout_store/04_architecture.md.
"""

from .base import BadId, NotHeld, ReadoutStore, check_id, open_store
from .files import FileStore

__all__ = ["BadId", "FileStore", "NotHeld", "ReadoutStore", "check_id", "open_store"]
