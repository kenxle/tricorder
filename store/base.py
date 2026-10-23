"""The store's interface, so a hosted store can replace the disk one.

Every caller goes through `open_store()` and the seven calls of
`ReadoutStore`. Nothing outside `store/` builds a store path.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol

from schema.claim import Readout, ScanResult

from .models import DeleteReport, Holding, SaveResult, StoredReadout, VersionInfo

_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


class BadId(ValueError):
    """A fund or company id that could name a path outside the store."""


class NotHeld(LookupError):
    """The store holds no such company, version or file."""


def check_id(kind: str, value: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise BadId(f"{kind} id {value!r} must be 1 to 64 of a-z, 0-9, '_' or '-', starting with a letter or digit")
    return value


class ReadoutStore(Protocol):
    def save(self, fund: str, company: str, readout: Readout, room_dir: Path, results: list[ScanResult]) -> SaveResult: ...

    def get(self, fund: str, company: str, version: int | None = None) -> StoredReadout: ...

    def read_file(self, fund: str, company: str, path: str, version: int | None = None) -> bytes: ...

    def list_company(self, fund: str, company: str) -> Holding: ...

    def list_versions(self, fund: str, company: str) -> list[VersionInfo]: ...

    def companies(self, fund: str) -> list[str]: ...

    def delete_company(self, fund: str, company: str) -> DeleteReport: ...


def open_store() -> ReadoutStore:
    """The configured store: files under TRICORDER_STORE_DIR (default
    store_data/), with TRICORDER_CACHE_DIR (default cache/) for delete."""
    from .files import FileStore

    return FileStore()
