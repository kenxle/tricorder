"""Response contracts for API dictionaries, shared through FastAPI's OpenAPI schema."""

from pydantic import BaseModel

from founder_requests.draft import Held, Item
from schema.claim import Panel, PieceRevision


class Health(BaseModel):
    ok: bool
    scans: list[str]


class ScanList(BaseModel):
    all: list[str]
    available: list[str]


class RoomInfo(BaseModel):
    id: str
    path: str
    inputs: list[str]
    has_readout: bool


class SourceText(BaseModel):
    text: str


class ClaimSource(SourceText):
    room: str


class RoomRevisions(BaseModel):
    room: str
    revisions: list[PieceRevision]
    changes: list[Panel]


class CompanyList(BaseModel):
    fund: str
    companies: list[str]


class FounderRequestList(BaseModel):
    room: str
    items: list[Item]
    default: list[int]
    held: list[Held]
    by: str
    reason: str
    sender: str
    fund: str
    synthetic: bool
    copy_command: str | None
    working_copy: str | None
    mailto_max: int
    upload_max_bytes: int
    accepted: list[str]


class ReceivedAnswer(BaseModel):
    checklist_id: str
    item: str
    status_before: str
    status_after: str


class ScanRerun(BaseModel):
    scan: str
    ok: bool
    error: str | None


class ReceivedFile(BaseModel):
    original_name: str
    saved: str
    bytes: int
    answers: list[ReceivedAnswer]
    checklist_id: str
    item: str
    at: str
    note: str | None = None
    summary: list[str]
    scans_rerun: list[ScanRerun]


class ReceivedLog(BaseModel):
    received: list[ReceivedFile]
