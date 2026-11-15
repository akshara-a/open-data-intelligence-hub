"""LLM provider factory. Add providers here without changing agent logic."""
from __future__ import annotations

from .base import ChatProvider, LLMUnavailableError


def create_provider(name: str) -> ChatProvider:
    normalized = name.strip().lower()
    if normalized == "gemini":
        from .gemini import GeminiProvider
        return GeminiProvider()
    raise ValueError(
        f"Unsupported KGNAV_PROVIDER={name!r}. Available provider: gemini. "
        "The provider interface is ready for additional adapters."
    )


__all__ = ["ChatProvider", "LLMUnavailableError", "create_provider"]
