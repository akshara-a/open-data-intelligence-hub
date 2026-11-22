"""Zero-dependency cloud-to-local text generation routing."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen


class RouterError(RuntimeError):
    """Raised when neither configured text-generation route is available."""


@dataclass(frozen=True)
class Generation:
    text: str
    provider: str
    fallback_reason: str | None = None


class LLMRouter:
    """Try a configured OpenAI-compatible endpoint, then a local Ollama server."""

    def __init__(self, timeout_seconds: float = 3.0) -> None:
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str) -> Generation:
        cloud_url = os.getenv("TAX_CLOUD_BASE_URL", "").strip()
        cloud_error: str | None = None
        if cloud_url:
            try:
                return Generation(self._cloud_generate(prompt, cloud_url), "cloud")
            except (
                URLError, TimeoutError, ValueError, KeyError, IndexError, TypeError
            ) as exc:
                cloud_error = type(exc).__name__

        try:
            text = self._local_generate(prompt)
        except (
            URLError, TimeoutError, ValueError, KeyError, IndexError, TypeError
        ) as exc:
            local_error = type(exc).__name__
            if cloud_error:
                raise RouterError(
                    f"cloud generation failed ({cloud_error}); "
                    f"local generation failed ({local_error})"
                ) from exc
            raise RouterError(f"local generation failed ({local_error})") from exc
        return Generation(text, "local", cloud_error)

    def _cloud_generate(self, prompt: str, base_url: str) -> str:
        url = base_url.rstrip("/")
        if not url.startswith("https://"):
            raise ValueError("cloud base URL must use HTTPS")
        if not url.endswith("/chat/completions"):
            url += "/chat/completions"
        payload = {
            "model": os.getenv("TAX_CLOUD_MODEL", "gpt-4o-mini"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        headers = {"Content-Type": "application/json"}
        api_key = os.getenv("TAX_CLOUD_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        response = self._post_json(url, payload, headers)
        text = response["choices"][0]["message"]["content"]
        if not isinstance(text, str) or not text.strip():
            raise ValueError("cloud endpoint returned empty content")
        return text.strip()

    def _local_generate(self, prompt: str) -> str:
        url = os.getenv("TAX_LOCAL_URL", "http://127.0.0.1:11434").rstrip("/")
        payload = {
            "model": os.getenv("TAX_LOCAL_MODEL", "llama3"),
            "prompt": prompt,
            "stream": False,
        }
        response = self._post_json(
            f"{url}/api/generate",
            payload,
            {"Content-Type": "application/json"},
        )
        text = response["response"]
        if not isinstance(text, str) or not text.strip():
            raise ValueError("local endpoint returned empty content")
        return text.strip()

    def _post_json(
        self,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str],
    ) -> dict[str, object]:
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:
            decoded = json.loads(response.read().decode("utf-8"))
        if not isinstance(decoded, dict):
            raise ValueError("generation endpoint returned a non-object response")
        return decoded
