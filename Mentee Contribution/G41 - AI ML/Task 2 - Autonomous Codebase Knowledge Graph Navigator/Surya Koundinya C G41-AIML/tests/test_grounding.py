
import json

from kgnav.grounding import collect_known, find_ungrounded


EV = [
    {
        "tool": "impact_analysis",
        "input": {"target": "legacy-auth-module"},
        "output": json.dumps({
            "affected": [
                {
                    "name": "POST /auth/login",
                    "chain": [
                        "POST /auth/login",
                        "legacy-auth-module",
                    ],
                },
                {"name": "GET /users/{id}"},
            ]
        }),
    }
]


def test_grounded_ok():
    known = collect_known(EV)

    md = (
        "Deprecating `legacy-auth-module` breaks "
        "`POST /auth/login` and `GET /users/{id}` "
        "(`POST /auth/login` → `legacy-auth-module`). "
        "Distance `2`."
    )

    assert find_ungrounded(md, known) == []


def test_hallucination_caught():
    known = collect_known(EV)

    assert find_ungrounded(
        "Also breaks `billing-service`.", known
    ) == ["billing-service"]

    assert find_ungrounded(
        "```cypher\nMATCH (n) RETURN n\n```\n"
        "Use *auth-adapter* (new).",
        known,
    ) == []


def test_nested_arrays_and_objects():
    evidence = [{
        "input": {},
        "output": json.dumps({
            "services": [
                {
                    "name": "payment-service",
                    "routes": [
                        "POST /payments/charge",
                        "GET /payments/status",
                    ],
                }
            ]
        }),
    }]

    known = collect_known(evidence)

    assert "payment-service" in known
    assert "post /payments/charge" in known
    assert "get /payments/status" in known


def test_null_values_do_not_create_identifiers():
    evidence = [{
        "input": {},
        "output": json.dumps({
            "service": "payment-service",
            "owner": None,
            "dependencies": [None, "auth-service"],
        }),
    }]

    known = collect_known(evidence)

    assert "payment-service" in known
    assert "auth-service" in known
    assert "none" not in known


def test_structured_python_output():
    evidence = [{
        "input": {"target": "legacy-auth-module"},
        "output": {
            "affected": ["payment-service", "order-service"],
            "metadata": {"owner": None},
        },
    }]

    known = collect_known(evidence)

    assert "payment-service" in known
    assert "order-service" in known
    assert "none" not in known


def test_invalid_json_fallback():
    evidence = [{
        "input": {},
        "output": "payment-service",
    }]

    known = collect_known(evidence)

    assert "payment-service" in known


def test_case_insensitive_matching():
    known = collect_known(EV)

    assert find_ungrounded(
        "Service `LEGACY-AUTH-MODULE` is affected.",
        known,
    ) == []


def test_duplicate_ungrounded_identifiers():
    known = collect_known(EV)

    assert find_ungrounded(
        "`billing-service` depends on `billing-service`.",
        known,
    ) == ["billing-service"]

def test_numeric_lists_are_not_flagged():
    known = collect_known(EV)
    md = "Components after removal: `[7]` and `[7, 8]`."
    assert find_ungrounded(md, known) == []
    assert find_ungrounded("Also `[fake-service]`.", known) == ["[fake-service]"]
