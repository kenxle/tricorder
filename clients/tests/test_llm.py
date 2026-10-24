from pathlib import Path

from pydantic import BaseModel

import clients.llm as llm
from clients.llm import SYSTEM_PROMPT, model_id
from scans import knowledge

FRAMEWORKS = Path(__file__).resolve().parents[2] / "docs" / "ongoing" / "FRAMEWORKS.md"


def test_the_system_prompt_is_the_one_in_frameworks():
    assert SYSTEM_PROMPT.strip() in FRAMEWORKS.read_text(encoding="utf-8")


def test_model_routes_default_and_override(monkeypatch):
    monkeypatch.delenv("TRICORDER_MODEL_READ", raising=False)
    assert model_id("read") == "claude-opus-5-5" and model_id("bulk") == "claude-haiku-5-5"
    monkeypatch.setenv("TRICORDER_MODEL_READ", "claude-sonnet-5-5")
    assert model_id("read") == "claude-sonnet-5-5"


# Expert knowledge (docs/ongoing/roadmap/expert-knowledge.md). No network: the
# fake client below stands in for clients.llm.client() and records the call.

KNOWLEDGE = Path(__file__).resolve().parents[2] / "knowledge"


class _Out(BaseModel):
    ok: bool


class _FakeClient:
    def __init__(self):
        self.calls = []
        self.messages = self

    def parse(self, **kwargs):
        self.calls.append(kwargs)

        class _Response:
            stop_reason = "end_turn"
            parsed_output = _Out(ok=True)
        return _Response()


def _sent(monkeypatch, **kwargs) -> str:
    fake = _FakeClient()
    monkeypatch.setattr(llm, "_client", fake)
    llm.read(_Out, check_name="t", scan="t", task="Task: test.", **kwargs)
    return fake.calls[0]["messages"][0]["content"]


def test_the_knowledge_files_text_reaches_the_prompt(monkeypatch):
    for piece in ("traction_and_revenue", "burn_and_runway"):
        body = (KNOWLEDGE / f"{piece}.md").read_text(encoding="utf-8").strip()
        sent = _sent(monkeypatch, knowledge=knowledge.block([piece]))
        assert body in sent
        assert f'<expert_knowledge piece="{piece}">' in sent
        assert "never quote it, cite it, or take a number from it" in sent


def test_a_missing_knowledge_file_means_no_knowledge_not_an_error(monkeypatch, tmp_path):
    assert knowledge.text("retention", root=tmp_path) == ""
    assert knowledge.block(["retention", None], root=tmp_path) is None
    assert knowledge.text("../AGENTS", root=KNOWLEDGE) == ""
    assert "expert_knowledge" not in _sent(monkeypatch, knowledge=knowledge.block(["retention"], root=tmp_path))


def test_the_slide_reader_and_the_rewording_load_their_pieces_knowledge():
    from scans.claims.read import KNOWLEDGE_PIECES
    from steering.models import RewordReading
    from steering.reword import reword

    assert "traction_and_revenue" in KNOWLEDGE_PIECES
    seen = []
    reword([], "say it plainly", lambda output, **kw: seen.append(kw) or RewordReading(lines=[]), piece="burn_and_runway")
    assert (KNOWLEDGE / "burn_and_runway.md").read_text(encoding="utf-8").strip() in seen[0]["knowledge"]
