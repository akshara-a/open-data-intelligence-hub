
import asyncio
import dataclasses
import json
import sys
import tempfile
from pathlib import Path

import pytest

from kgnav.agent import (
    NavigatorAgent,
    SynthesisFailedError,
    TargetNotFoundError,
)
from kgnav.config import load_config
from kgnav.llm.base import (
    ChatResponse,
    LLMUnavailableError,
    TextBlock,
)

EVIDENCE = [{
    "tool": "find_nodes",
    "input": {"text": "payment"},
    "is_error": False,
    "output": json.dumps({
        "matches": [{
            "label": "Service",
            "name": "payment-service",
        }]
    }),
}]

REPORT = "# Report\nThe `payment-service` was found."


class FakeLLM:
    def __init__(self, behaviour):
        self.behaviour = behaviour
        self.models = []

    async def create(self, *, model, **kw):
        self.models.append(model)
        result = self.behaviour(model)

        if isinstance(result, Exception):
            raise result

        return ChatResponse(
            content=[TextBlock(text=result)]
        )

    async def close(self):
        pass


def make_agent(behaviour):
    agent = object.__new__(NavigatorAgent)

    agent.cfg = dataclasses.replace(
        load_config(),
        model_synth="primary",
        synth_fallbacks=("backup",),
        max_grounding_retries=0,
    )

    agent.llm = FakeLLM(behaviour)
    agent.verbose = False
    agent.synth_model_used = None

    return agent


# ---------------------------------------------------------------------------
# Existing synthesis recovery tests


def test_falls_back_when_primary_overloaded():
    agent = make_agent(
        lambda model: (
            LLMUnavailableError("503 busy")
            if model == "primary"
            else REPORT
        )
    )

    body, bad = asyncio.run(
        agent._synthesize("q", EVIDENCE)
    )

    assert "# Report" in body
    assert bad == []
    assert agent.llm.models == ["primary", "backup"]
    assert agent.synth_model_used == "backup"


def test_synthesis_failure_keeps_evidence_and_explains_resume():
    agent = make_agent(
        lambda model: LLMUnavailableError("503 busy")
    )

    directory = Path(tempfile.mkdtemp())

    checkpoint = agent._save_checkpoint(
        directory,
        "which modules depend on payment-service?",
        EVIDENCE,
    )

    message = ""

    try:
        asyncio.run(
            agent._finish(
                "q",
                EVIDENCE,
                directory,
                checkpoint,
            )
        )
    except SynthesisFailedError as exc:
        message = str(exc)

    assert str(checkpoint) in message
    assert "kgnav resume" in message

    saved = json.loads(
        checkpoint.read_text()
    )

    assert saved["ledger"][0]["tool"] == "find_nodes"


def test_resume_regenerates_report_from_checkpoint_without_mcp():
    agent = make_agent(lambda model: REPORT)

    directory = Path(tempfile.mkdtemp())

    checkpoint = agent._save_checkpoint(
        directory,
        "which modules depend on payment-service?",
        EVIDENCE,
    )

    result = asyncio.run(
        agent.resume(checkpoint, directory)
    )

    assert result.path.exists()
    assert "payment-service" in result.path.read_text()
    assert result.ungrounded == []


# ---------------------------------------------------------------------------
# Exact target resolution tests


def test_resolves_exact_target_from_preflight_results():
    resolution = json.dumps({
        "matches": [
            {
                "label": "Service",
                "name": "legacy-auth-service",
            },
            {
                "label": "Service",
                "name": "auth-service-v2",
            },
        ]
    })

    targets = NavigatorAgent._resolve_exact_targets(
        "If I deprecate legacy-auth-service, what breaks?",
        resolution,
    )

    assert targets == ["legacy-auth-service"]


def test_does_not_match_partial_graph_identifier():
    resolution = json.dumps({
        "matches": [
            {
                "label": "Service",
                "name": "auth-service",
            },
            {
                "label": "Service",
                "name": "auth-service-v2",
            },
        ]
    })

    targets = NavigatorAgent._resolve_exact_targets(
        "What happens if I deprecate auth-service-v2?",
        resolution,
    )

    assert targets == ["auth-service-v2"]


def test_does_not_resolve_fuzzy_candidate_as_exact_target():
    resolution = json.dumps({
        "matches": [
            {
                "label": "Service",
                "name": "payment-service",
            }
        ]
    })

    targets = NavigatorAgent._resolve_exact_targets(
        "What happens if I deprecate nonexistent-payment-service?",
        resolution,
    )

    assert targets == []


def test_ignores_unsupported_graph_labels():
    resolution = json.dumps({
        "matches": [
            {
                "label": "UnknownLabel",
                "name": "payment-service",
            }
        ]
    })

    targets = NavigatorAgent._resolve_exact_targets(
        "What happens if I deprecate payment-service?",
        resolution,
    )

    assert targets == []


def test_requested_target_extracts_hyphenated_identifier():
    target = NavigatorAgent._requested_target(
        "What happens if I deprecate nonexistent-payment-service?"
    )

    assert target == "nonexistent-payment-service"


# ---------------------------------------------------------------------------
# Missing target and suggestion tests


def test_suggestions_are_collected_without_becoming_targets():
    ledger = [
        {
            "tool": "find_nodes",
            "input": {"text": "nonexistent-payment-service"},
            "is_error": False,
            "output": json.dumps({
                "matches": [
                    {
                        "label": "Service",
                        "name": "payment-service",
                    },
                    {
                        "label": "Service",
                        "name": "order-payment-service",
                    },
                ]
            }),
        }
    ]

    suggestions = NavigatorAgent._suggestions_from_ledger(
        ledger,
        "nonexistent-payment-service",
    )

    assert suggestions == [
        "payment-service",
        "order-payment-service",
    ]

    # Suggestions do not modify the requested target.
    assert NavigatorAgent._requested_target(
        "deprecate nonexistent-payment-service"
    ) == "nonexistent-payment-service"


def test_missing_target_error_contains_suggestions():
    error = TargetNotFoundError(
        requested_target="nonexistent-payment-service",
        suggestions=["payment-service"],
    )

    assert error.requested_target == "nonexistent-payment-service"
    assert error.suggestions == ["payment-service"]
    assert "TARGET NOT FOUND" in str(error)
    assert "payment-service" in str(error)
    assert "not selected automatically" in str(error)


def test_missing_target_error_without_suggestions():
    error = TargetNotFoundError(
        requested_target="nonexistent-payment-service",
    )

    assert error.requested_target == "nonexistent-payment-service"
    assert error.suggestions == []
    assert "TARGET NOT FOUND" in str(error)
    assert "No exact matching graph node exists" in str(error)


def test_postflight_rejects_missing_exact_target_even_if_fuzzy_match_exists():
    agent = make_agent(lambda model: REPORT)

    ledger = [
        {
            "tool": "find_nodes",
            "input": {"text": "What happens if I deprecate nonexistent-payment-service?"},
            "is_error": False,
            "output": json.dumps({
                "matches": [{
                    "label": "Service",
                    "name": "payment-service",
                }]
            }),
        }
    ]

    tools = [
        {"name": "impact_analysis"},
        {"name": "detect_circular_dependencies"},
        {"name": "find_single_points_of_failure"},
        {"name": "coupling_metrics"},
    ]

    async def run_postflight():
        await agent._mandatory_postflight(
            session=None,
            tools=tools,
            question=(
                "What happens if I deprecate "
                "nonexistent-payment-service?"
            ),
            resolution_output=ledger[0]["output"],
            ledger=ledger,
        )

    with pytest.raises(TargetNotFoundError) as exc_info:
        asyncio.run(run_postflight())

    error = exc_info.value

    assert error.requested_target == "nonexistent-payment-service"
    assert "payment-service" in error.suggestions

    # No impact-analysis call is executed for the fuzzy candidate.
    assert not any(
        entry["tool"] == "impact_analysis"
        for entry in ledger
    )


def test_successful_impact_for_wrong_target_does_not_resolve_missing_target():
    agent = make_agent(lambda model: REPORT)

    ledger = [
        {
            "tool": "find_nodes",
            "input": {"text": "nonexistent-payment-service"},
            "is_error": False,
            "output": json.dumps({
                "matches": [{
                    "label": "Service",
                    "name": "payment-service",
                }]
            }),
        },
        {
            "tool": "impact_analysis",
            "input": {"target": "payment-service"},
            "is_error": False,
            "output": json.dumps({
                "target": "payment-service",
                "affected_nodes": [],
            }),
        },
    ]

    tools = [
        {"name": "impact_analysis"},
        {"name": "detect_circular_dependencies"},
        {"name": "find_single_points_of_failure"},
        {"name": "coupling_metrics"},
    ]

    async def run_postflight():
        await agent._mandatory_postflight(
            session=None,
            tools=tools,
            question=(
                "What happens if I deprecate "
                "nonexistent-payment-service?"
            ),
            resolution_output=ledger[0]["output"],
            ledger=ledger,
        )

    with pytest.raises(TargetNotFoundError):
        asyncio.run(run_postflight())


# ---------------------------------------------------------------------------
# CLI behavior tests


def test_cli_prints_clean_target_not_found_message(
    monkeypatch,
    capsys,
):
    from kgnav import agent as agent_module
    from kgnav import cli

    class FakeAgent:
        def __init__(self, verbose=False):
            pass

        async def run(self, question, out_dir):
            raise TargetNotFoundError(
                requested_target="nonexistent-payment-service",
                suggestions=["payment-service"],
            )

    monkeypatch.setattr(
        agent_module,
        "NavigatorAgent",
        FakeAgent,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "kgnav",
            "ask",
            "What happens if I deprecate nonexistent-payment-service?",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2

    captured = capsys.readouterr()

    assert "TARGET NOT FOUND" in captured.err
    assert "nonexistent-payment-service" in captured.err
    assert "payment-service" in captured.err
    assert "Impact analysis: NOT EXECUTED" in captured.err
    assert "Report: NOT GENERATED" in captured.err
    assert "Traceback" not in captured.err


def test_cli_handles_investigation_error_without_traceback(
    monkeypatch,
    capsys,
):
    from kgnav import agent as agent_module
    from kgnav import cli

    class FakeAgent:
        def __init__(self, verbose=False):
            pass

        async def run(self, question, out_dir):
            from kgnav.agent import InvestigationFailedError

            raise InvestigationFailedError(
                "Mandatory get_schema call failed."
            )

    monkeypatch.setattr(
        agent_module,
        "NavigatorAgent",
        FakeAgent,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "kgnav",
            "ask",
            "Which services depend on payment-service?",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2

    captured = capsys.readouterr()

    assert "INVESTIGATION ERROR" in captured.err
    assert "Mandatory get_schema call failed" in captured.err
    assert "Traceback" not in captured.err
def test_architecture_wide_question_does_not_require_a_target():
    agent = make_agent(lambda model: REPORT)
    question = "Are there circular dependencies between our services?"
    ledger = []

    tools = [
        {"name": "impact_analysis"},
        {"name": "detect_circular_dependencies"},
        {"name": "find_single_points_of_failure"},
        {"name": "coupling_metrics"},
    ]

    async def fake_exec(session, ledger, name, args, tool_use_id=None):
        ledger.append({"tool": name, "input": args,
                       "is_error": False, "output": "{}"})

    agent._execute_tool = fake_exec

    asyncio.run(agent._mandatory_postflight(
        session=None, tools=tools, question=question,
        resolution_output=json.dumps({"matches": []}), ledger=ledger,
    ))

    assert not any(e["tool"] == "impact_analysis" for e in ledger)
    assert any(e["tool"] == "detect_circular_dependencies" for e in ledger)