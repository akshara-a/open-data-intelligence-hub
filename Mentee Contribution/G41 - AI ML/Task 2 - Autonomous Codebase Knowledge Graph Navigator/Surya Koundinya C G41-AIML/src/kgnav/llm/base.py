"""Provider-neutral chat response types and interface."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class LLMUnavailableError(RuntimeError):
    """Provider temporarily unavailable (retries exhausted on 429/5xx/network, or quota used up).
    The agent may fall back to another model or resume later."""


@dataclass
class TextBlock:
    type: str = "text"
    text: str = ""


@dataclass
class ToolUseBlock:
    type: str = "tool_use"
    id: str = ""
    name: str = ""
    input: dict[str, Any] = field(default_factory=dict)
    thought_signature: str | None = None


@dataclass
class ChatResponse:
    content: list[TextBlock | ToolUseBlock]
    stop_reason: str | None = None  # provider finish reason, e.g. STOP / MAX_TOKENS


class ChatProvider(Protocol):
    """Small compatibility surface used by NavigatorAgent."""

    async def create(
        self,
        *,
        model: str,
        max_tokens: int,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> ChatResponse: ...

    async def close(self) -> None: ...
