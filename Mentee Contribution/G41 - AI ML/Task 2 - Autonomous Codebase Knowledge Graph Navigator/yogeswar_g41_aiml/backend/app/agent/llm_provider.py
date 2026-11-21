"""
Phase 5 - LLM Provider Abstraction
Decouples LLM inference from workflow logic with strict Pydantic validation,
bounded retries, timeout management, and safe secret handling.
"""
import os
import re
import json
import time
import asyncio
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, TypeVar, Optional, Dict, Any, List
import httpx
from pydantic import BaseModel, ValidationError

from .models import IntentOutput, AnswerOutput, Finding

logger = logging.getLogger("agent.llm_provider")
T = TypeVar("T", bound=BaseModel)

SECRET_SEARCH_PATHS = [
    Path("/run/secrets"),
    Path("./secrets"),
    Path("../secrets"),
    Path(__file__).resolve().parent.parent.parent.parent / "secrets",
]


def load_secret(secret_name: str) -> Optional[str]:
    """Resolves secret from environment variable or Docker secret mount."""
    env_val = os.getenv(secret_name)
    if env_val and env_val.strip():
        return env_val.strip()

    for base in SECRET_SEARCH_PATHS:
        candidate = base / secret_name
        if candidate.is_file():
            val = candidate.read_text(encoding="utf-8").strip()
            if val:
                return val
    return None


class LLMProviderError(Exception):
    """Base exception for LLM provider failures."""
    pass


class LLMUnavailableError(LLMProviderError):
    """Raised when an LLM provider is unconfigured or unreachable."""
    pass


class LLMRateLimitError(LLMProviderError):
    """Raised when provider returns HTTP 429 rate limit."""
    pass


class LLMTimeoutError(LLMProviderError):
    """Raised when provider call times out."""
    pass


class LLMOutputValidationError(LLMProviderError):
    """Raised when structured response cannot be parsed into expected Pydantic model."""
    pass


# ============================================================================
# Abstract Base Class
# ============================================================================

class LLMProvider(ABC):
    """Abstract interface for LLM completion and structured output."""

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.0,
    ) -> str:
        """Generate raw text completion."""
        pass

    @abstractmethod
    async def structured_completion(
        self,
        prompt: str,
        schema: Type[T],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> T:
        """Generate structured completion strictly validated against Pydantic schema."""
        pass

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Report provider health and configuration status."""
        pass


# ============================================================================
# Mock LLM Provider (Offline & Testing Grounding Engine)
# ============================================================================

class MockLLMProvider(LLMProvider):
    """
    Deterministic, offline provider for test execution and environments without
    outbound internet or external API keys.
    Interprets intent and synthesizes grounded answers strictly from supplied evidence.
    """

    def __init__(self):
        self.provider_name = "mock"

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "provider": "mock",
            "mode": "deterministic_offline",
            "configured": True,
        }

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.0,
    ) -> str:
        return f"[MockLLM response for prompt: {prompt[:100]}...]"

    async def structured_completion(
        self,
        prompt: str,
        schema: Type[T],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> T:
        # 1. Intent Classification
        if schema == IntentOutput:
            q_lower = prompt.lower()
            intent: str = "general"
            symbols: List[str] = []
            files: List[str] = []

            # Detect symbols & files
            file_matches = re.findall(r"[\w_./\\-]+\.(?:py|ts|tsx|js|go|java|cpp|h)", prompt)
            files.extend(list(set(file_matches)))
            file_stems = {f.split(".")[0].split("/")[-1].split("\\")[-1] for f in files}

            tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", prompt)
            excluded = {
                "what", "where", "how", "when", "does", "call", "calls", "calling", "the", "this", "that",
                "show", "find", "explain", "code", "repo", "snapshot", "dependency", "dependencies",
                "chain", "between", "and", "including", "any", "dynamic", "router", "route", "service",
                "investigate", "unresolved", "coupling", "architecture", "overview", "structure",
                "repository", "question", "file", "files", "which", "database", "method", "methods",
                "directly", "invoke", "invokes", "invoking", "class", "classes", "function", "functions",
                "definition", "declared", "declarations", "give", "list"
            }
            candidates = [t for t in tokens if t.lower() not in excluded and t not in file_stems]
            # Prioritize identifier patterns (e.g. verify_credentials, DatabasePool, issue_jwt_token)
            code_symbols = [t for t in candidates if "_" in t or any(c.isupper() for c in t[1:])]
            other_symbols = [t for t in candidates if t not in code_symbols]
            candidates = code_symbols + other_symbols

            if any(k in q_lower for k in ["dependency", "dependencies", "depend", "chain", "call", "calls", "called", "caller", "callee", "invoke", "invokes", "invoked", "invoking", "impact"]):
                intent = "dependency_analysis"
            elif any(k in q_lower for k in ["unresolved", "dynamic", "eval", "dispatch", "runtime"]):
                intent = "unresolved_investigation"
            elif any(k in q_lower for k in ["lookup", "find", "locate", "where is", "search"]):
                intent = "entity_lookup"
            elif any(k in q_lower for k in ["api", "endpoint", "route", "handler"]):
                intent = "api_discovery"
            elif any(k in q_lower for k in ["architecture", "overview", "structure", "components"]):
                intent = "architecture_exploration"
            elif any(k in q_lower for k in ["explain", "how does", "what does"]):
                intent = "code_explanation"

            symbols = candidates[:4]

            return IntentOutput(
                intent_category=intent,
                target_symbols=symbols,
                target_files=files,
                constraints=[],
                reasoning=f"Mock intent classification based on architectural keywords and tokens ({len(symbols)} symbols extracted).",
            )  # type: ignore

        # 2. Answer Synthesis
        if schema == AnswerOutput:
            # Parse prompt for retrieved evidence references
            ev_refs = re.findall(r"E-[\w\-]+", prompt)
            unique_evs = sorted(list(set(ev_refs)))

            # Check if prompt contains simulated insufficient evidence signal
            if "NO_EVIDENCE_FOUND" in prompt or "INSUFFICIENT_EVIDENCE" in prompt or (not unique_evs and "dynamic" not in prompt.lower() and "empty" in prompt.lower()):
                return AnswerOutput(
                    summary="Insufficient evidence found in active snapshot to answer the query.",
                    verified_findings=[],
                    uncertain_findings=[],
                    recommendations=["Verify symbol spelling or ingest a snapshot containing the target component."],
                    evidence_references=[],
                    insufficient_evidence=True,
                    insufficient_evidence_reason="No matching entities, files, or syntactic relationships were located in the active snapshot graph.",
                    markdown_response="### Investigation Result\n\n**Insufficient Evidence**: No matching components or evidence records were identified for this query in the active snapshot.",
                )  # type: ignore

            verified: List[Finding] = []
            uncertain: List[Finding] = []

            # Collect uncertain evidence IDs explicitly mentioned in uncertain lines/sections
            uncertain_ev_ids = set()
            in_uncertain_section = False
            for line in prompt.splitlines():
                if "Uncertain / Dynamic Couplings:" in line:
                    in_uncertain_section = True
                elif line.endswith(":") and in_uncertain_section:
                    in_uncertain_section = False
                if in_uncertain_section or line.strip().startswith("- [Potential / Uncertain]") or "dynamic coupling" in line.lower() or "unresolvable call" in line.lower():
                    for ev in re.findall(r"E-[\w\-]+", line):
                        uncertain_ev_ids.add(ev)

            # 1. Parse structured findings from prompt if present
            for line in prompt.splitlines():
                line = line.strip()
                if line.startswith("- [Verified Dependency]") or line.startswith("- [Verified Declaration]") or line.startswith("- Verified") or line.startswith("- Entity"):
                    file_match = re.search(r"\(File:\s*([^,]+),\s*Lines:\s*([^\)]+)\)", line)
                    ev_match = re.search(r"\[Evidence:\s*([^\]]+)\]", line)
                    fp = file_match.group(1).strip() if file_match and file_match.group(1).strip() not in ("None", "") else None
                    lr = file_match.group(2).strip() if file_match and file_match.group(2).strip() not in ("None", "None-None", "") else None
                    raw_evs = [e.strip() for e in ev_match.group(1).split(",")] if ev_match else re.findall(r"E-[\w\-]+", line)
                    evs = [e for e in raw_evs if e not in uncertain_ev_ids]
                    stmt = re.sub(r"\s*\[Evidence:.*?\]", "", line[2:])
                    stmt = re.sub(r"\s*\(File:.*?\)", "", stmt).strip()
                    verified.append(
                        Finding(
                            statement=stmt,
                            finding_type="verified_static",
                            evidence_ids=evs,
                            file_path=fp,
                            line_range=lr,
                            confidence=1.0,
                        )
                    )
                elif line.startswith("- [Potential / Uncertain]") or line.startswith("- Dynamic unresolvable") or line.startswith("- Uncertain or dynamic"):
                    file_match = re.search(r"\(File:\s*([^,]+),\s*Lines:\s*([^\)]+)\)", line) or re.search(r"at\s+([\w_./\\-]+):([0-9\-]+)", line) or re.search(r"in\s+([\w_./\\-]+):([0-9\-]+)", line)
                    ev_match = re.search(r"\[Evidence:\s*([^\]]+)\]", line)
                    fp = file_match.group(1).strip() if file_match and file_match.group(1).strip() not in ("None", "") else None
                    lr = file_match.group(2).strip() if file_match and file_match.group(2).strip() not in ("None", "None-None", "") else None
                    conf_match = re.search(r"Confidence:\s*([0-9.]+)", line)
                    conf = float(conf_match.group(1)) if conf_match else 0.3
                    stmt = re.sub(r"\s*\(Confidence:.*?\)", "", line[2:])
                    stmt = re.sub(r"\s*\[Evidence:.*?\]", "", stmt).strip()
                    stmt = re.sub(r"\s*\(File:.*?\)", "", stmt).strip()
                    raw_evs = [e.strip() for e in ev_match.group(1).split(",")] if ev_match else []
                    if not raw_evs:
                        raw_evs = [e for e in re.findall(r"E-[\w\-]+", line)]
                    uncertain.append(
                        Finding(
                            statement=stmt,
                            finding_type="potential_uncertain",
                            evidence_ids=raw_evs or (list(uncertain_ev_ids)[:1] if uncertain_ev_ids else []),
                            file_path=fp,
                            line_range=lr,
                            confidence=conf,
                        )
                    )

            # 2. Fallback to token-based synthesis if no structured lines were parsed
            if not verified and not uncertain:
                has_dynamic = any(w in prompt.lower() for w in ["unresolved", "dynamic", "eval", "dispatch", "potential_uncertain"])
                if has_dynamic:
                    uncertain.append(
                        Finding(
                            statement="Detected dynamic or unresolvable call invocation site. Target cannot be verified statically and remains potential/uncertain.",
                            finding_type="potential_uncertain",
                            evidence_ids=list(uncertain_ev_ids)[:1] if uncertain_ev_ids else ["E-mock-unresolved"],
                            confidence=0.3,
                        )
                    )

                if unique_evs:
                    for ev in unique_evs:
                        if ev in uncertain_ev_ids:
                            if not any(ev in u.evidence_ids for u in uncertain):
                                uncertain.append(
                                    Finding(
                                        statement=f"Uncertain or unresolvable call site citation [{ev}].",
                                        finding_type="potential_uncertain",
                                        evidence_ids=[ev],
                                        confidence=0.3,
                                    )
                                )
                        else:
                            verified.append(
                                Finding(
                                    statement=f"Verified static code entity/relationship grounded in citation [{ev}].",
                                    finding_type="verified_static",
                                    evidence_ids=[ev],
                                    confidence=1.0,
                                )
                            )
                elif not has_dynamic:
                    verified.append(
                        Finding(
                            statement="General architectural analysis for snapshot context.",
                            finding_type="verified_static",
                            evidence_ids=[],
                            confidence=0.8,
                        )
                    )

            md = [
                "### Architectural Analysis",
                "",
                "#### Executive Summary",
                f"Analysis completed against active snapshot context. Evaluated {len(verified)} verified findings and {len(uncertain)} uncertain/dynamic relationships.",
                "",
                "#### Verified Findings",
            ]
            for v in verified:
                loc = f" (`{v.file_path}:{v.line_range}`)" if v.file_path and v.line_range else ""
                ev_str = f" Citations: {', '.join([f'[{e}]' for e in v.evidence_ids])}" if v.evidence_ids else ""
                md.append(f"- **[Verified Fact]** {v.statement}{loc}{ev_str}")

            if uncertain:
                md.extend(["", "#### Potential / Uncertain Relationships"])
                for u in uncertain:
                    loc = f" (`{u.file_path}:{u.line_range}`)" if u.file_path and u.line_range else ""
                    md.append(f"- **[Potential / Uncertain]** {u.statement}{loc} (Confidence: {u.confidence})")

            md.extend([
                "",
                "#### Engineering Recommendations",
                "- Keep statically verified components isolated from unresolvable dynamic invocation paths.",
                "- Verify all cited line ranges directly via commit-pinned bare Git storage reader.",
            ])

            return AnswerOutput(
                summary="Architectural analysis grounded in snapshot knowledge graph and static analysis evidence.",
                verified_findings=verified,
                uncertain_findings=uncertain,
                recommendations=[
                    "Keep statically verified components isolated from dynamic call paths.",
                    "Verify cited evidence line ranges via commit-pinned reader.",
                ],
                evidence_references=unique_evs,
                insufficient_evidence=False,
                markdown_response="\n".join(md),
            )  # type: ignore

        raise LLMOutputValidationError(f"MockLLMProvider does not support schema {schema}")


# ============================================================================
# OpenAI-Compatible Provider
# ============================================================================

class OpenAILLMProvider(LLMProvider):
    """OpenAI API provider with structured JSON outputs and bounded retries."""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = os.getenv("OPENAI_MODEL", model)

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy" if self.api_key else "unconfigured",
            "provider": "openai",
            "model": self.model,
            "configured": bool(self.api_key),
        }

    async def _post_with_retry(self, endpoint: str, payload: Dict[str, Any], max_retries: int = 2) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{endpoint}"
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 429:
                        raise LLMRateLimitError(f"OpenAI rate limit exceeded: {resp.text}")
                    if resp.status_code >= 500:
                        raise LLMProviderError(f"OpenAI server error HTTP {resp.status_code}: {resp.text}")
                    if resp.status_code >= 400:
                        raise LLMProviderError(f"OpenAI client error HTTP {resp.status_code}: {resp.text}")
                    return resp.json()
            except (httpx.TimeoutException, httpx.ConnectTimeout) as e:
                last_error = LLMTimeoutError(f"OpenAI timeout: {str(e)}")
            except LLMRateLimitError as e:
                last_error = e
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
            except Exception as e:
                last_error = LLMProviderError(f"OpenAI request failed: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(1)

        raise last_error or LLMProviderError("OpenAI call failed after retries")

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.0,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = await self._post_with_retry(
            "/chat/completions",
            {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        return data["choices"][0]["message"]["content"]

    async def structured_completion(
        self,
        prompt: str,
        schema: Type[T],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> T:
        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        augmented_sys = (
            f"{system_prompt or ''}\n\n"
            f"You MUST return ONLY a valid JSON object strictly matching this JSON schema:\n{schema_json}\n"
            "Do not include code markdown fences or conversational preambles."
        )

        messages = [
            {"role": "system", "content": augmented_sys},
            {"role": "user", "content": prompt},
        ]

        data = await self._post_with_retry(
            "/chat/completions",
            {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.0,
                "response_format": {"type": "json_object"},
            },
        )
        raw_content = data["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(raw_content)
            return schema.model_validate(parsed)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error("Failed to parse structured response from OpenAI: %s\nRaw: %s", str(e), raw_content)
            raise LLMOutputValidationError(f"Invalid structured LLM output: {str(e)}")


# ============================================================================
# Anthropic Provider
# ============================================================================

class AnthropicLLMProvider(LLMProvider):
    """Anthropic Claude API provider."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.model = os.getenv("ANTHROPIC_MODEL", model)

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy" if self.api_key else "unconfigured",
            "provider": "anthropic",
            "model": self.model,
            "configured": bool(self.api_key),
        }

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.0,
    ) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{self.base_url}/messages", json=payload, headers=headers)
            if resp.status_code >= 400:
                raise LLMProviderError(f"Anthropic error HTTP {resp.status_code}: {resp.text}")
            data = resp.json()
            return data["content"][0]["text"]

    async def structured_completion(
        self,
        prompt: str,
        schema: Type[T],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> T:
        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        sys_msg = (
            f"{system_prompt or ''}\n\n"
            f"You MUST return ONLY a valid JSON object strictly conforming to this schema:\n{schema_json}"
        )
        raw_text = await self.complete(prompt, system_prompt=sys_msg, max_tokens=max_tokens)
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
        try:
            parsed = json.loads(cleaned)
            return schema.model_validate(parsed)
        except Exception as e:
            raise LLMOutputValidationError(f"Anthropic structured parse failed: {str(e)}")


# ============================================================================
# Provider Factory
# ============================================================================

_current_provider: Optional[LLMProvider] = None


def get_llm_provider(force_provider: Optional[str] = None) -> LLMProvider:
    """
    Resolves the configured LLM provider according to environment variables and secrets.
    Does not expose API secrets.
    If no valid provider is configured, returns MockLLMProvider in development or
    raises LLMUnavailableError if a real provider was explicitly configured without credentials.
    """
    global _current_provider
    if _current_provider is not None and not force_provider:
        return _current_provider

    provider_name = (force_provider or os.getenv("LLM_PROVIDER", "auto")).lower().strip()

    if provider_name == "mock":
        _current_provider = MockLLMProvider()
        return _current_provider

    if provider_name == "openai":
        api_key = load_secret("OPENAI_API_KEY")
        if not api_key:
            raise LLMUnavailableError("LLM_PROVIDER is configured as 'openai', but OPENAI_API_KEY is missing.")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        _current_provider = OpenAILLMProvider(api_key=api_key, base_url=base_url)
        return _current_provider

    if provider_name == "anthropic":
        api_key = load_secret("ANTHROPIC_API_KEY")
        if not api_key:
            raise LLMUnavailableError("LLM_PROVIDER is configured as 'anthropic', but ANTHROPIC_API_KEY is missing.")
        _current_provider = AnthropicLLMProvider(api_key=api_key)
        return _current_provider

    # Auto mode: inspect available keys
    if openai_key := load_secret("OPENAI_API_KEY"):
        _current_provider = OpenAILLMProvider(api_key=openai_key)
        return _current_provider

    if anthropic_key := load_secret("ANTHROPIC_API_KEY"):
        _current_provider = AnthropicLLMProvider(api_key=anthropic_key)
        return _current_provider

    # Default to robust MockLLMProvider for offline / test environments
    logger.info("No external LLM credentials found. Defaulting to MockLLMProvider.")
    _current_provider = MockLLMProvider()
    return _current_provider
