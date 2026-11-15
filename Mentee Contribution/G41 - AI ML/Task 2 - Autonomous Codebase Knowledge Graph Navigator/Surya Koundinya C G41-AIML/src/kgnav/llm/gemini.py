"""Google Gemini Developer API adapter (REST generateContent) with free-tier resilience:
 * retries 429/5xx honouring the server's RetryInfo / Retry-After delay, else exponential backoff
 * fails fast (clear message) when the *daily* free quota is exhausted - retrying cannot help
 * optional client-side pacing (GEMINI_MIN_INTERVAL_S) to stay under requests-per-minute limits
 * retries MALFORMED_FUNCTION_CALL once; surfaces finishReason (e.g. MAX_TOKENS) to the agent
"""
from __future__ import annotations

import asyncio
import os
import random
import re
import time
import uuid
from typing import Any

import httpx

from .base import ChatResponse, LLMUnavailableError, TextBlock, ToolUseBlock

_RETRYABLE = {429, 500, 502, 503, 504}
_DELAY_RE = re.compile(r"^\s*([\d.]+)\s*s\s*$")


class QuotaExhaustedError(LLMUnavailableError):
    """Daily free-tier quota used up; retrying now is pointless."""


class GeminiProvider:
    """Translate the agent's provider-neutral message shape to Gemini REST."""

    API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: str | None = None, *, timeout: float = 90.0,
                 max_retries: int | None = None, min_interval_s: float | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Create a key at https://aistudio.google.com/apikey "
                "and add it to your .env file."
            )
        self._client = httpx.AsyncClient(timeout=timeout, headers={"x-goog-api-key": self.api_key})
        self._tool_names: dict[str, str] = {}
        self.max_retries = int(os.getenv("GEMINI_MAX_RETRIES", "6")) if max_retries is None else max_retries
        self.min_interval_s = float(os.getenv("GEMINI_MIN_INTERVAL_S", "0")) if min_interval_s is None else min_interval_s
        self._sleep = asyncio.sleep          # injectable for tests
        self._jitter = lambda d: d * (1.0 + random.random() * 0.25)  # injectable for tests
        self._lock = asyncio.Lock()
        self._last_request = 0.0

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------ schema
    @staticmethod
    def _gemini_schema(value: Any) -> Any:
        """Convert JSON Schema (as emitted by MCP/pydantic) to Gemini's REST schema subset."""
        if isinstance(value, list):
            return [GeminiProvider._gemini_schema(v) for v in value]
        if not isinstance(value, dict):
            return value
        converted: dict[str, Any] = {}
        for key, item in value.items():
            if key == "type" and isinstance(item, str):
                converted[key] = item.upper()
            elif key == "type" and isinstance(item, list):
                concrete = next((v for v in item if v != "null"), "string")
                converted[key] = concrete.upper()
            elif key == "anyOf" and isinstance(item, list):
                # Optional[X] is emitted as anyOf[X, null]; keep the concrete branch only.
                branches = [b for b in item if not (isinstance(b, dict) and b.get("type") == "null")]
                if branches:
                    converted.update(GeminiProvider._gemini_schema(branches[0]))
            elif key in {"$schema", "$id", "additionalProperties", "default", "examples"}:
                continue
            else:
                converted[key] = GeminiProvider._gemini_schema(item)
        return converted

    # ------------------------------------------------------------------ messages
    def _convert_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        contents: list[dict[str, Any]] = []
        for message in messages:
            role = message["role"]
            raw = message.get("content", "")
            parts: list[dict[str, Any]] = []
            if isinstance(raw, str):
                parts.append({"text": raw})
            else:
                for block in raw:
                    kind = block.get("type") if isinstance(block, dict) else getattr(block, "type", None)
                    get = block.get if isinstance(block, dict) else lambda k, d=None: getattr(block, k, d)
                    if kind == "text":
                        parts.append({"text": get("text", "")})
                    elif kind == "tool_use":
                        call_id = get("id") or f"call_{uuid.uuid4().hex}"
                        name = get("name")
                        self._tool_names[call_id] = name
                        part = {"functionCall": {"name": name, "args": get("input", {})}}
                        if get("thought_signature"):
                            part["thoughtSignature"] = get("thought_signature")
                        parts.append(part)
                    elif kind == "tool_result":
                        call_id = get("tool_use_id", "")
                        name = self._tool_names.get(call_id)
                        if not name:
                            raise ValueError(f"No tool name recorded for tool result {call_id!r}")
                        parts.append({
                            "functionResponse": {
                                "name": name,
                                "response": {"content": get("content", ""), "is_error": bool(get("is_error", False))},
                            }
                        })
            if parts:
                contents.append({"role": "model" if role == "assistant" else "user", "parts": parts})
        return contents

    # ------------------------------------------------------------------ transport
    async def _pace(self) -> None:
        if self.min_interval_s <= 0:
            return
        async with self._lock:
            wait = self._last_request + self.min_interval_s - time.monotonic()
            if wait > 0:
                await self._sleep(wait)
            self._last_request = time.monotonic()

    @staticmethod
    def _error_info(response) -> tuple[str, dict]:
        try:
            body = response.json()
        except ValueError:
            return response.text, {}
        err = body.get("error", {}) if isinstance(body, dict) else {}
        return err.get("message", response.text), err

    @staticmethod
    def _is_daily_quota(response) -> bool:
        flat = response.text.lower().replace(" ", "").replace("_", "")
        return "perday" in flat

    @staticmethod
    def _retry_delay(response, err: dict, attempt: int) -> float:
        for d in err.get("details", []) or []:
            if isinstance(d, dict) and str(d.get("@type", "")).endswith("RetryInfo"):
                m = _DELAY_RE.match(str(d.get("retryDelay", "")))
                if m:
                    return min(float(m.group(1)) + 1.0, 120.0)
        ra = response.headers.get("retry-after")
        if ra:
            try:
                return min(float(ra), 120.0)
            except ValueError:
                pass
        return -1.0  # sentinel: no server hint -> caller applies jittered exponential backoff

    async def _post(self, url: str, payload: dict, model: str) -> dict:
        attempt = 0
        while True:
            await self._pace()
            try:
                response = await self._client.post(url, json=payload)
            except httpx.TransportError as exc:
                if attempt >= self.max_retries:
                    raise LLMUnavailableError(f"Gemini network error after {attempt} retries: {exc}") from exc
                await self._sleep(self._jitter(min(2.0 ** (attempt + 1), 30.0)))
                attempt += 1
                continue
            if not response.is_error:
                return response.json()
            detail, err = self._error_info(response)
            status = response.status_code
            if status == 429 and self._is_daily_quota(response):
                raise QuotaExhaustedError(
                    f"Gemini daily free-tier quota exhausted for '{model}' (resets ~midnight Pacific). "
                    "Use a model with a bigger free allowance (e.g. a Flash-Lite model via "
                    "KGNAV_MODEL_INVESTIGATE), wait for the reset, or enable billing. Details: " + detail[:300]
                )
            if status in _RETRYABLE and attempt < self.max_retries:
                delay = self._retry_delay(response, err, attempt)
                if delay < 0:
                    delay = self._jitter(min(2.0 ** (attempt + 1), 60.0))
                await self._sleep(delay)
                attempt += 1
                continue
            hint = ""
            if status == 404:
                hint = f" (model '{model}' not found for this key - run `kgnav doctor` to list valid model IDs)"
            if status in _RETRYABLE:
                raise LLMUnavailableError(f"Gemini API error ({status}) persisted after {attempt} retries: {detail}")
            raise RuntimeError(f"Gemini API error ({status}): {detail}{hint}")

    @staticmethod
    def _parse(data: dict) -> tuple[list[TextBlock | ToolUseBlock], str | None]:
        candidates = data.get("candidates", [])
        if not candidates:
            raise RuntimeError(f"Gemini returned no candidates. Prompt feedback: {data.get('promptFeedback', {})}")
        cand = candidates[0]
        blocks: list[TextBlock | ToolUseBlock] = []
        for part in cand.get("content", {}).get("parts", []):
            if part.get("thought") is True:
                continue  # never surface thought summaries as answer text
            if "text" in part:
                blocks.append(TextBlock(text=part["text"]))
            elif "functionCall" in part:
                call = part["functionCall"]
                blocks.append(ToolUseBlock(
                    id=call.get("id") or f"call_{uuid.uuid4().hex}", name=call["name"],
                    input=call.get("args", {}), thought_signature=part.get("thoughtSignature"),
                ))
        return blocks, cand.get("finishReason")

    # ------------------------------------------------------------------ public
    async def create(
        self,
        *,
        model: str,
        max_tokens: int,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> ChatResponse:
        payload: dict[str, Any] = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": self._convert_messages(messages),
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.2},
        }
        if tools:
            declarations = []
            for tool in tools:
                decl: dict[str, Any] = {"name": tool["name"], "description": tool.get("description", "")}
                params = self._gemini_schema(tool.get("input_schema") or {})
                if params.get("properties"):  # Gemini rejects OBJECT schemas with empty properties
                    decl["parameters"] = params
                declarations.append(decl)
            payload["tools"] = [{"functionDeclarations": declarations}]

        url = f"{self.API_ROOT}/{model}:generateContent"
        blocks: list[TextBlock | ToolUseBlock] = []
        finish: str | None = None
        for _ in range(2):  # Gemini occasionally emits MALFORMED_FUNCTION_CALL with no parts; retry once
            data = await self._post(url, payload, model)
            blocks, finish = self._parse(data)
            if blocks or finish != "MALFORMED_FUNCTION_CALL":
                break
        for b in blocks:
            if b.type == "tool_use":
                self._tool_names[b.id] = b.name
        return ChatResponse(content=blocks, stop_reason=finish)
