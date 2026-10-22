from pathlib import Path

from clients.llm import SYSTEM_PROMPT, model_id

FRAMEWORKS = Path(__file__).resolve().parents[2] / "docs" / "ongoing" / "FRAMEWORKS.md"


def test_the_system_prompt_is_the_one_in_frameworks():
    assert SYSTEM_PROMPT.strip() in FRAMEWORKS.read_text(encoding="utf-8")


def test_model_routes_default_and_override(monkeypatch):
    monkeypatch.delenv("TRICORDER_MODEL_READ", raising=False)
    assert model_id("read") == "claude-opus-5-5" and model_id("bulk") == "claude-haiku-5-5"
    monkeypatch.setenv("TRICORDER_MODEL_READ", "claude-sonnet-5-5")
    assert model_id("read") == "claude-sonnet-5-5"
