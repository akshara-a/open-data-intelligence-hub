
"""Autonomous multi-step agent: deterministic MCP investigation,
grounded synthesis, and evidence verification.
"""
from __future__ import annotations

import json
import re
import sys
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .config import Config, load_config
from .grounding import collect_known, find_ungrounded
from .llm import LLMUnavailableError, create_provider
from .prompts import INVESTIGATE_SYSTEM, SYNTH_SYSTEM

MAX_TOOL_CHARS = 30_000
MAX_EVIDENCE_CHARS = 150_000

SUPPORTED_IMPACT_LABELS = {
    "Service",
    "Module",
    "APIRoute",
    "Database",
    "FrontendComponent",
}


IMPACT_KEYWORDS = re.compile(
    r"\b(deprecat\w*|remov\w*|delet\w*|chang\w*|"
    r"migrat\w*|impact|blast[\s-]*radius|"
    r"downstream|affected|dependenc\w*)\b",
    re.IGNORECASE,
)

# Verbs that propose changing a specific component. A question using one
# of these needs an exact target. Analysis-wide wording such as
# "circular dependencies" does not.
ACTION_KEYWORDS = re.compile(
    r"\b(deprecat\w*|remov\w*|delet\w*|chang\w*|migrat\w*)\b",
    re.IGNORECASE,
)

# Identifiers such as payment-service or legacy_auth_module.
GRAPH_IDENTIFIER = re.compile(
    r"(?<![a-zA-Z0-9_-])"
    r"[a-zA-Z][a-zA-Z0-9]*"
    r"(?:[-_][a-zA-Z0-9]+)+"
    r"(?![a-zA-Z0-9_-])"
)


class SynthesisFailedError(RuntimeError):
    """Report generation failed after graph investigation succeeded."""


class InvestigationFailedError(RuntimeError):
    """Mandatory graph investigation could not be completed."""


class TargetNotFoundError(InvestigationFailedError):
    """The requested target has no exact matching node in the graph.

    Impact analysis is never run for an unresolved target. Any fuzzy
    matches are listed as suggestions only and are never selected
    automatically.
    """

    def __init__(
        self,
        requested_target: str | None,
        suggestions: list[str] | None = None,
    ):
        self.requested_target = requested_target
        self.suggestions = suggestions or []

        target_text = (
            f"'{requested_target}'"
            if requested_target
            else "the requested target"
        )

        message = (
            f"TARGET NOT FOUND: No exact matching graph node exists "
            f"for {target_text}. Impact analysis was not executed "
            "and no report was generated."
        )

        if self.suggestions:
            message += (
                "\nPossible matches (suggestions only; "
                "not selected automatically):\n"
                + "\n".join(f"- {name}" for name in self.suggestions)
            )

        message += (
            "\nCheck the target name or retry with an exact "
            "service, module, API route, database or component name."
        )

        super().__init__(message)

@dataclass
class AgentResult:
    report_md: str
    evidence: list[dict] = field(default_factory=list)
    ungrounded: list[str] = field(default_factory=list)
    path: Path | None = None


def _text(blocks) -> str:
    return "".join(
        b.text for b in blocks
        if getattr(b, "type", "") == "text"
    )


class NavigatorAgent:

    def __init__(
        self,
        cfg: Config | None = None,
        verbose: bool = False,
    ):
        self.cfg = cfg or load_config()
        self.llm = create_provider(self.cfg.provider)
        self.verbose = verbose
        self.synth_model_used: str | None = None

    def _log(self, msg: str):
        if self.verbose:
            print(msg, file=sys.stderr)

    # --------------------------------------------------------------
    # Tool result helpers

    @staticmethod
    def _parse_output(output: str):
        try:
            return json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return None

    @classmethod
    def _output_has_error(cls, output: str) -> bool:
        data = cls._parse_output(output)

        return (
            isinstance(data, dict)
            and bool(data.get("error"))
        )

    @classmethod
    def _successful(cls, entry: dict) -> bool:
        return (
            not entry["is_error"]
            and not cls._output_has_error(entry["output"])
        )

    @staticmethod
    def _has_tool(
        ledger: list[dict],
        name: str,
        expected_input: dict | None = None,
    ) -> bool:
        for entry in ledger:
            if entry["tool"] != name:
                continue

            if expected_input is not None:
                if any(
                    entry["input"].get(k) != v
                    for k, v in expected_input.items()
                ):
                    continue

            if NavigatorAgent._successful(entry):
                return True

        return False

    async def _execute_tool(
        self,
        session: ClientSession,
        ledger: list[dict],
        name: str,
        arguments: dict,
        tool_use_id: str | None = None,
    ) -> dict:
        """Execute one MCP tool and record its complete evidence."""

        self._log(
            f"[mandatory/tool] {name}({json.dumps(arguments)[:200]})"
        )

        try:
            result = await session.call_tool(name, arguments)

            output = "".join(
                item.text
                for item in result.content
                if getattr(item, "type", "") == "text"
            )

            is_error = bool(result.isError)

        except Exception as exc:
            output = json.dumps({
                "error": type(exc).__name__,
                "message": str(exc)[:1500],
            })
            is_error = True

        entry = {
            "tool": name,
            "input": arguments,
            "output": output,
            "is_error": is_error,
        }

        ledger.append(entry)

        status = (
            "ERROR"
            if not self._successful(entry)
            else "OK"
        )

        self._log(f"[tool result] {name}: {status}")

        tool_result = {
            "type": "tool_result",
            "content": (
                output[:MAX_TOOL_CHARS]
                + (
                    "\n...[truncated]"
                    if len(output) > MAX_TOOL_CHARS
                    else ""
                )
            ),
            "is_error": is_error,
        }

        if tool_use_id is not None:
            tool_result["tool_use_id"] = tool_use_id

        return tool_result

    @staticmethod
    def _is_impact_question(question: str) -> bool:
        return bool(IMPACT_KEYWORDS.search(question))

    @staticmethod
    def _requested_target(question: str) -> str | None:
        """Extract a likely explicitly named graph identifier.

        This is used for an error message only. It never resolves
        a graph node or authorizes an impact-analysis call.
        """

        matches = GRAPH_IDENTIFIER.findall(question)

        if not matches:
            return None

        return matches[0]

    @staticmethod
    def _resolve_exact_targets(
        question: str,
        resolution_output: str,
    ) -> list[str]:
        """Resolve targets only when their exact graph names occur
        in the question. Never guess between fuzzy matches.
        """

        try:
            data = json.loads(resolution_output)
        except (json.JSONDecodeError, TypeError):
            return []

        matches = data.get("matches", []) if isinstance(data, dict) else []

        question_normalized = question.casefold()

        targets = []

        for match in matches:
            if not isinstance(match, dict):
                continue

            name = match.get("name")
            label = match.get("label")

            if (
                not isinstance(name, str)
                or not name
                or label not in SUPPORTED_IMPACT_LABELS
            ):
                continue

            # Treat hyphens and underscores as part of graph names
            # to avoid matching auth-service inside auth-service-v2.
            pattern = (
                r"(?<![a-zA-Z0-9_-])"
                + re.escape(name)
                + r"(?![a-zA-Z0-9_-])"
            )

            if re.search(
                pattern,
                question_normalized,
                re.IGNORECASE,
            ):
                targets.append(name)

        return list(dict.fromkeys(targets))

    @staticmethod
    def _suggestions_from_ledger(
        ledger: list[dict],
        requested_target: str | None,
        limit: int = 5,
    ) -> list[str]:
        """Collect possible names from find_nodes results.

        Suggestions are informational only. They are never passed
        to impact_analysis automatically.
        """

        suggestions = []
        seen = set()

        requested_normalized = (
            requested_target.casefold()
            if requested_target
            else None
        )

        for entry in ledger:
            if entry.get("tool") != "find_nodes":
                continue

            if not NavigatorAgent._successful(entry):
                continue

            data = NavigatorAgent._parse_output(
                entry.get("output", "")
            )

            if not isinstance(data, dict):
                continue

            matches = data.get("matches", [])

            if not isinstance(matches, list):
                continue

            for match in matches:
                if not isinstance(match, dict):
                    continue

                name = match.get("name")
                label = match.get("label")

                if (
                    not isinstance(name, str)
                    or not name
                    or label not in SUPPORTED_IMPACT_LABELS
                ):
                    continue

                normalized = name.casefold()

                if normalized == requested_normalized:
                    continue

                if normalized in seen:
                    continue

                seen.add(normalized)
                suggestions.append(name)

                if len(suggestions) >= limit:
                    return suggestions

        return suggestions

    # --------------------------------------------------------------
    # Deterministic mandatory investigation

    async def _mandatory_preflight(
        self,
        session: ClientSession,
        tools: list[dict],
        question: str,
        ledger: list[dict],
    ) -> str:
        """Always obtain the live schema and resolve graph entities."""

        available = {tool["name"] for tool in tools}

        required = {"get_schema", "find_nodes"}

        missing = required - available

        if missing:
            raise InvestigationFailedError(
                f"Required MCP tools unavailable: {sorted(missing)}"
            )

        await self._execute_tool(
            session,
            ledger,
            "get_schema",
            {},
        )

        if not self._successful(ledger[-1]):
            raise InvestigationFailedError(
                "Mandatory get_schema call failed. "
                "Cannot safely continue investigation."
            )

        await self._execute_tool(
            session,
            ledger,
            "find_nodes",
            {"text": question},
        )

        if not self._successful(ledger[-1]):
            raise InvestigationFailedError(
                "Mandatory find_nodes call failed. "
                "Cannot safely resolve the requested entities."
            )

        # Give Gemini the deterministic preflight evidence.
        return (
            "MANDATORY PREFLIGHT EVIDENCE:\n\n"
            "The following tools have already been executed successfully.\n"
            "Use their results; do not assume their output.\n\n"
            f"GET_SCHEMA:\n{ledger[-2]['output'][:MAX_TOOL_CHARS]}\n\n"
            f"FIND_NODES:\n{ledger[-1]['output'][:MAX_TOOL_CHARS]}\n\n"
            "Continue the investigation using the available MCP tools."
        )

    async def _mandatory_postflight(
        self,
        session: ClientSession,
        tools: list[dict],
        question: str,
        resolution_output: str,
        ledger: list[dict],
    ):
        """Guarantee independent architectural analysis evidence.

        Impact analysis is permitted only for exact target names
        returned by preflight resolution and present in the question.
        Fuzzy candidates are suggestions, never automatic substitutes.
        """

        available = {tool["name"] for tool in tools}

        if not self._is_impact_question(question):
            return

        targets = self._resolve_exact_targets(
            question,
            resolution_output,
        )

        # Do not accept an arbitrary successful impact_analysis call
        # as a substitute for exact target resolution. The model may
        # have selected a fuzzy candidate, so it is not authoritative.
        requested_target = self._requested_target(question)
        target_required = (
            requested_target is not None
            or bool(ACTION_KEYWORDS.search(question))
        )

        if not targets and target_required:
            suggestions = self._suggestions_from_ledger(
                ledger,
                requested_target,
            )

            self._log(
                "[verification] No exact target found; "
                "impact analysis will not run."
            )

            raise TargetNotFoundError(
                requested_target=requested_target,
                suggestions=suggestions,
            )

        # Ensure every exact target is investigated.
        for target in targets:

            expected = {"target": target}

            if self._has_tool(
                ledger,
                "impact_analysis",
                expected,
            ):
                continue

            if "impact_analysis" not in available:
                raise InvestigationFailedError(
                    "Required MCP tool impact_analysis is unavailable."
                )

            await self._execute_tool(
                session,
                ledger,
                "impact_analysis",
                {
                    "target": target,
                    "max_depth": 8,
                },
            )

        # Independent architectural-debt analysis.
        mandatory_calls = [
            ("detect_circular_dependencies", {"level": "service"}),
            ("detect_circular_dependencies", {"level": "module"}),
            ("find_single_points_of_failure", {"min_fan_in": 3}),
            ("coupling_metrics", {"level": "service", "top": 15}),
            ("coupling_metrics", {"level": "module", "top": 15}),
        ]

        for name, arguments in mandatory_calls:

            if name not in available:
                raise InvestigationFailedError(
                    f"Required architectural tool unavailable: {name}"
                )

            if self._has_tool(
                ledger,
                name,
                arguments,
            ):
                continue

            await self._execute_tool(
                session,
                ledger,
                name,
                arguments,
            )

        # Do not synthesize a report with missing mandatory evidence.
        failures = [
            entry
            for entry in ledger
            if (
                entry["tool"] in {
                    "impact_analysis",
                    "detect_circular_dependencies",
                    "find_single_points_of_failure",
                    "coupling_metrics",
                }
                and not self._successful(entry)
            )
        ]

        if failures:
            failed_names = [
                entry["tool"]
                for entry in failures
            ]

            raise InvestigationFailedError(
                "Mandatory architectural analysis returned errors: "
                + ", ".join(failed_names)
            )

        for name, arguments in mandatory_calls:
            if not self._has_tool(ledger, name, arguments):
                raise InvestigationFailedError(
                    f"Mandatory evidence missing: {name} {arguments}"
                )

        self._log(
            "[verification] All mandatory architectural "
            "analysis tools completed successfully."
        )

    # --------------------------------------------------------------
    # Phase 1: Investigation

    async def _investigate(
        self,
        session: ClientSession,
        question: str,
    ) -> list[dict]:

        listed = await session.list_tools()

        tools = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,
            }
            for tool in listed.tools
        ]

        ledger: list[dict] = []

        # Mandatory schema and entity-resolution preflight.
        preflight = await self._mandatory_preflight(
            session,
            tools,
            question,
            ledger,
        )

        resolution_output = ledger[-1]["output"]

        messages: list[dict] = [
            {
                "role": "user",
                "content": (
                    f"DEVELOPER QUESTION:\n{question}\n\n"
                    f"{preflight}"
                ),
            }
        ]

        # Gemini's investigation loop remains available for
        # additional queries, verification and exploration.
        for step in range(self.cfg.max_steps):

            resp = await self.llm.create(
                model=self.cfg.model,
                max_tokens=4096,
                system=INVESTIGATE_SYSTEM,
                tools=tools,
                messages=messages,
            )

            messages.append({
                "role": "assistant",
                "content": resp.content,
            })

            calls = [
                block
                for block in resp.content
                if getattr(block, "type", "") == "tool_use"
            ]

            if not calls:
                self._log(
                    f"[step {step}] done: "
                    f"{_text(resp.content)[:120]}"
                )
                break

            results = []

            for call in calls:

                result = await self._execute_tool(
                    session,
                    ledger,
                    call.name,
                    call.input,
                    tool_use_id=call.id,
                )

                results.append(result)

            messages.append({
                "role": "user",
                "content": results,
            })

        else:
            self._log(
                "max_steps reached; checking mandatory evidence"
            )

        # Mandatory architectural analysis is executed independently
        # of Gemini's tool-selection decisions.
        await self._mandatory_postflight(
            session,
            tools,
            question,
            resolution_output,
            ledger,
        )

        return ledger

    # --------------------------------------------------------------
    # Phase 2: Evidence collection

    def _evidence_blob(self, ledger: list[dict]) -> str:

        items = []
        total = 0

        for entry in ledger:

            if not self._successful(entry):
                continue

            output = entry["output"][:MAX_TOOL_CHARS]

            item = {
                "tool": entry["tool"],
                "input": entry["input"],
                "output": output,
            }

            serialized = json.dumps(item, indent=1)

            if total + len(serialized) > MAX_EVIDENCE_CHARS:
                break

            items.append(item)
            total += len(serialized)

        return json.dumps(items, indent=1)

    # --------------------------------------------------------------
    # Phase 3: Grounded synthesis

    async def _synthesize(
        self,
        question: str,
        ledger: list[dict],
    ) -> tuple[str, list[str]]:

        known = collect_known([
            entry
            for entry in ledger
            if self._successful(entry)
        ])

        msgs: list[dict] = [
            {
                "role": "user",
                "content": (
                    f"DEVELOPER QUESTION:\n{question}\n\n"
                    "EVIDENCE (tool results from the Neo4j graph):\n"
                    f"{self._evidence_blob(ledger)}\n\n"
                    "Write the report now."
                ),
            }
        ]

        body = ""
        bad = []

        for attempt in range(
            self.cfg.max_grounding_retries + 1
        ):

            resp = await self._generate(msgs)

            body = _text(resp.content).strip()

            bad = find_ungrounded(body, known)

            self._log(
                f"[synthesis attempt {attempt}] "
                f"ungrounded identifiers: {bad}"
            )

            if not bad:
                break

            msgs += [
                {
                    "role": "assistant",
                    "content": body,
                },
                {
                    "role": "user",
                    "content": (
                        "Grounding check FAILED. These backticked "
                        "identifiers do not exist in the evidence: "
                        + ", ".join(f"`{item}`" for item in bad)
                        + ". Rewrite the full report: remove or "
                        "correct them. New proposed artefacts must "
                        "be in *italics* (not backticks) and marked "
                        "(new)."
                    ),
                },
            ]

        if getattr(resp, "stop_reason", None) == "MAX_TOKENS":
            body += (
                "\n\n> ⚠️ Report was cut off by the output-token "
                "limit; raise KGNAV_SYNTH_MAX_TOKENS and re-run."
            )

        return body, bad

    async def _generate(self, msgs: list[dict]):
        """Try the report model and configured fallbacks."""

        models = (
            [self.cfg.model_synth]
            + [
                model
                for model in self.cfg.synth_fallbacks
                if model != self.cfg.model_synth
            ]
        )

        last: Exception | None = None

        for model in models:

            try:
                resp = await self.llm.create(
                    model=model,
                    max_tokens=self.cfg.synth_max_tokens,
                    system=SYNTH_SYSTEM,
                    messages=msgs,
                )

                self.synth_model_used = model

                if model != models[0]:
                    self._log(
                        f"[synthesis] fell back to {model}"
                    )

                return resp

            except LLMUnavailableError as exc:
                self._log(
                    f"[synthesis] {model} unavailable: "
                    f"{str(exc)[:160]}"
                )
                last = exc

        assert last is not None
        raise last

    # --------------------------------------------------------------
    # Phase 4: Collection and checkpointing

    async def _collect(self, question: str) -> list[dict]:

        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "kgnav.mcp_server"],
            env=None,
        )

        pending_error: Exception | None = None
        ledger: list[dict] = []

        async with AsyncExitStack() as stack:

            read, write = await stack.enter_async_context(
                stdio_client(params)
            )

            session = await stack.enter_async_context(
                ClientSession(read, write)
            )

            await session.initialize()

            # Catch expected investigation failures before leaving
            # the MCP context. This prevents async cleanup from
            # wrapping them in an ExceptionGroup.
            try:
                ledger = await self._investigate(
                    session,
                    question,
                )

            except (
                TargetNotFoundError,
                InvestigationFailedError,
            ) as exc:
                pending_error = exc

        # Re-raise only after MCP resources have closed cleanly.
        if pending_error is not None:
            raise pending_error

        if not any(
            self._successful(entry)
            for entry in ledger
        ):
            raise InvestigationFailedError(
                "The investigation produced no successful "
                "graph evidence."
            )

        return ledger

    @staticmethod
    def _slug(question: str) -> str:
        return (
            re.sub(
                r"[^a-z0-9]+",
                "-",
                question.lower(),
            )[:60].strip("-")
            or "report"
        )

    def _save_checkpoint(
        self,
        out: Path,
        question: str,
        ledger: list[dict],
    ) -> Path:

        directory = out / ".checkpoints"
        directory.mkdir(parents=True, exist_ok=True)

        path = (
            directory
            / (
                f"{datetime.now():%Y%m%d-%H%M%S}-"
                f"{self._slug(question)}.json"
            )
        )

        path.write_text(
            json.dumps(
                {
                    "question": question,
                    "ledger": ledger,
                },
                default=str,
                indent=1,
            ),
            encoding="utf-8",
        )

        return path

    async def _finish(
        self,
        question: str,
        ledger: list[dict],
        out: Path,
        checkpoint: Path,
    ) -> AgentResult:

        try:
            body, bad = await self._synthesize(
                question,
                ledger,
            )

        except LLMUnavailableError as exc:
            raise SynthesisFailedError(
                f"{exc}\n\n"
                "The graph investigation succeeded and its "
                f"evidence is saved at:\n  {checkpoint}\n\n"
                "Re-run ONLY the report step with:\n"
                f"  kgnav resume {checkpoint}"
            ) from exc

        report = self._assemble(
            question,
            body,
            ledger,
            bad,
        )

        out.mkdir(parents=True, exist_ok=True)

        path = (
            out
            / (
                f"{datetime.now():%Y%m%d-%H%M%S}-"
                f"{self._slug(question)}.md"
            )
        )

        path.write_text(
            report,
            encoding="utf-8",
        )

        return AgentResult(
            report,
            ledger,
            bad,
            path,
        )

    # --------------------------------------------------------------
    # Public interface

    async def run(
        self,
        question: str,
        out_dir: str | Path = "reports",
    ) -> AgentResult:

        out = Path(out_dir)

        try:
            ledger = await self._collect(question)

            checkpoint = self._save_checkpoint(
                out,
                question,
                ledger,
            )

            return await self._finish(
                question,
                ledger,
                out,
                checkpoint,
            )

        finally:
            await self.llm.close()

    async def resume(
        self,
        checkpoint: str | Path,
        out_dir: str | Path = "reports",
    ) -> AgentResult:

        """Regenerate the report from saved evidence only."""

        ckpt = Path(checkpoint)

        data = json.loads(
            ckpt.read_text(encoding="utf-8")
        )

        try:
            return await self._finish(
                data["question"],
                data["ledger"],
                Path(out_dir),
                ckpt,
            )

        finally:
            await self.llm.close()

    # --------------------------------------------------------------
    # Report assembly

    def _assemble(
        self,
        question: str,
        body: str,
        ledger: list[dict],
        bad: list[str],
    ) -> str:

        head = (
            f"> **Query:** {question}  \n"
            f"> **Generated:** "
            f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} "
            f"· **Models:** `{self.cfg.model}` (investigate) / "
            f"`{self.synth_model_used or self.cfg.model_synth}` "
            f"(report) · "
            f"**Grounding check:** "
            f"{'PASSED' if not bad else 'FAILED (see warning)'}\n\n"
        )

        warn = ""

        if bad:
            warn = (
                "> ⚠️ **Unverified identifiers** "
                "(not found in graph evidence, treat with caution): "
                + ", ".join(f"`{item}`" for item in bad)
                + "\n\n"
            )

        lines = [
            "\n---\n"
            "## Appendix A — Evidence trail (tool calls executed)\n"
        ]

        for index, entry in enumerate(ledger, 1):

            status = (
                "ok"
                if self._successful(entry)
                else "ERROR"
            )

            lines.append(
                f"**{index}. `{entry['tool']}`** — {status}"
            )

            if entry["tool"] == "run_cypher":
                lines.append(
                    "```cypher\n"
                    f"{entry['input'].get('query', '')}\n"
                    "```"
                )

            elif entry["input"]:
                lines.append(
                    "```json\n"
                    f"{json.dumps(entry['input'])}\n"
                    "```"
                )

        return (
            head
            + warn
            + body
            + "\n"
            + "\n".join(lines)
            + "\n"
        )
