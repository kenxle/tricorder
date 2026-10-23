"""The store's own records. They are not part of the Claim schema: the store
holds Readouts and ScanResults as they are and describes them with these."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from schema.claim import Readout, ScanResult


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StoredFile(_Strict):
    path: str = Field(description="The room path, or the path inside cache/ for a URL source's saved copy.")
    origin: Literal["room", "cache"]
    sha256: str
    bytes: int


class NotCopied(_Strict):
    name: str
    why: str


class VersionInfo(_Strict):
    version: int
    saved_at: str
    room: str
    built_at: str
    content_sha256: str
    claims: int
    unverified: int
    gaps: int
    revisions: int
    results: list[str]
    results_missing: list[str] = Field(default_factory=list)
    files: list[StoredFile] = Field(default_factory=list)
    not_copied: list[NotCopied] = Field(default_factory=list)


class SaveResult(_Strict):
    fund: str
    company: str
    version: int
    new: bool
    content_sha256: str
    files_copied: int
    bytes_copied: int
    not_copied: list[NotCopied]
    results_missing: list[str]


class StoredReadout(_Strict):
    fund: str
    company: str
    version: VersionInfo
    readout: Readout
    results: list[ScanResult]


class HeldFile(_Strict):
    path: str
    origin: Literal["room", "cache"]
    sha256: str
    bytes: int
    versions: list[int]


class Holding(_Strict):
    """Everything held for one company in one fund."""

    fund: str
    company: str
    versions: list[VersionInfo]
    files: list[HeldFile]
    results: list[str]
    cache: list[str] = Field(description="The company's outside pulls in cache/, relative to cache/.")
    total_bytes: int


class Removed(_Strict):
    versions: int = 0
    files: int = 0
    results: int = 0
    cache_files: int = 0
    index_entries: int = 0


class DeleteReport(_Strict):
    fund: str
    company: str
    removed: Removed
    left: list[str] = Field(description="Paths still on disk for the company after the delete. Empty when it worked.")
    also_on_this_laptop: list[str] = Field(default_factory=list, description="out/ folders for the company's rooms. The store never wrote them and does not remove them.")
