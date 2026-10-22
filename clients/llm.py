"""The one door to the model, so routing, the gateway and the prompt live in one place.

    from clients.llm import read
    out = read(MyOutput, check_name="deck_claim_vs_named_cell", scan="redflags", docs=..., task=...)

Structured outputs only: every call passes a Pydantic class and gets a
validated instance back. Citations are never used; they cannot be combined
with structured output, so each claim carries its own quote and the quote
checker confirms it (FRAMEWORKS.md, "The shared Claim").

Settings, all from the environment:
    TRICORDER_MODEL_READ   reading and the memo pass (default claude-opus-5-5)
    TRICORDER_MODEL_BULK   bulk classification (default claude-haiku-5-5)
    TRICORDER_LLM_BASE_URL a gateway such as Nicrron's, if it passes structured
                           outputs through; unset means Anthropic's API
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, TypeVar

from pydantic import BaseModel

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.txt").read_text(encoding="utf-8")

T = TypeVar("T", bound=BaseModel)


class ModelRefused(RuntimeError):
    """The model declined. The scan turns this into a gap, never a guess."""


def model_id(route: Literal["read", "bulk"] = "read") -> str:
    if route == "bulk":
        return os.environ.get("TRICORDER_MODEL_BULK", "claude-haiku-5-5")
    return os.environ.get("TRICORDER_MODEL_READ", "claude-opus-5-5")


_client = None


def client():
    global _client
    if _client is None:
        import anthropic

        base_url = os.environ.get("TRICORDER_LLM_BASE_URL") or None
        _client = anthropic.Anthropic(base_url=base_url)
    return _client


def docs_block(docs: list[str]) -> str:
    """Documents already rendered as <doc> blocks by schema.readers callers."""
    return "\n".join(docs)


def read(
    output: type[T],
    *,
    check_name: str,
    scan: str,
    task: str,
    docs: list[str] | None = None,
    script_results: str | None = None,
    route: Literal["read", "bulk"] = "read",
    effort: Literal["low", "medium", "high", "xhigh", "max"] = "high",
    max_tokens: int = 16000,
) -> T:
    """One model reading. The user message is the entry's prompt from FRAMEWORKS.md,
    with the two header lines the system prompt expects."""
    parts = [f"Scan: {scan}", f"Check name: {check_name}", "", task]
    if docs:
        parts += ["", docs_block(docs)]
    if script_results:
        parts += ["", "<script_results>", script_results, "</script_results>"]
    response = client().messages.parse(
        model=model_id(route),
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        output_config={"effort": effort},
        messages=[{"role": "user", "content": "\n".join(parts)}],
        output_format=output,
    )
    if response.stop_reason == "refusal":
        raise ModelRefused(getattr(response.stop_details, "category", None) or "refused")
    return response.parsed_output
