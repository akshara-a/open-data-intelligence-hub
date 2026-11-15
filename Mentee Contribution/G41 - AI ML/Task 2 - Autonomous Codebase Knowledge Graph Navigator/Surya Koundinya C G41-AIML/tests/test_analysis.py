
from kgnav.analysis import (
    Edge,
    articulation_points,
    blast_radius,
    coupling_metrics,
    find_cycles,
    single_points_of_failure,
)
from kgnav.sample_data import EDGES
from kgnav.schema import DEPENDENCY_RELS


EDGE_OBJS = [
    Edge(s, sl, r, d, dl)
    for sl, s, r, dl, d in EDGES
    if r in DEPENDENCY_RELS
]

SVC_PAIRS = [
    (s, d)
    for _, s, r, _, d in EDGES
    if r == "DEPENDS_ON"
]


def names(radius, label):
    return {
        n
        for n, i in radius.items()
        if i["label"] == label
    }


# ---------------------------------------------------------------------------
# Blast radius tests


def test_blast_radius_legacy_auth_module():
    r = blast_radius(EDGE_OBJS, ["legacy-auth-module"])

    assert {
        "POST /auth/login",
        "GET /auth/validate",
        "POST /v2/auth/token",
    } <= names(r, "APIRoute")

    assert {
        "web-login-page",
        "web-checkout-page",
        "mobile-app-auth",
        "customer-portal",
    } <= names(r, "FrontendComponent")

    # Unaffected nodes.
    assert "admin-dashboard" not in r
    assert "report-builder" not in r

    # Hidden coupling: v2 session-manager reaches the legacy
    # module through the validator.
    assert r["session-manager"]["chain"] == [
        "session-manager",
        "legacy-token-validator",
        "legacy-auth-module",
    ]

    assert r["web-login-page"]["distance"] == 2


def test_blast_radius_depth_limit():
    r = blast_radius(
        EDGE_OBJS,
        ["legacy-auth-module"],
        max_depth=1,
    )

    assert all(i["distance"] <= 1 for i in r.values())


# ---------------------------------------------------------------------------
# Circular dependency tests


def test_cycle_detected():
    cycles = find_cycles(SVC_PAIRS)

    assert any(
        {
            "order-service",
            "inventory-service",
            "notification-service",
        } <= set(c["members"])
        for c in cycles
    )


def test_no_false_cycle():
    assert find_cycles([
        ("a", "b"),
        ("b", "c"),
    ]) == []

    components = find_cycles([
        ("a", "a"),
    ])

    assert components[0]["members"] == ["a"]


# ---------------------------------------------------------------------------
# Single points of failure tests


def test_spof_legacy_auth():
    spofs = {
        s["name"]: s
        for s in single_points_of_failure(SVC_PAIRS, 3)
    }

    assert "legacy-auth-service" in spofs
    assert spofs["legacy-auth-service"]["fan_in"] >= 3


def test_articulation_points_simple():
    assert articulation_points([
        ("a", "b"),
        ("b", "c"),
    ]) == {"b"}

    assert articulation_points([
        ("a", "b"),
        ("b", "c"),
        ("c", "a"),
    ]) == set()


# ---------------------------------------------------------------------------
# Coupling metrics tests


def test_coupling_metrics():
    m = {
        r["name"]: r
        for r in coupling_metrics([
            ("a", "b"),
            ("c", "b"),
        ])
    }

    assert m["b"]["afferent_ca"] == 2
    assert m["b"]["instability"] == 0.0
    assert m["a"]["instability"] == 1.0


# ---------------------------------------------------------------------------
# Strongly Connected Components (SCC) regression tests


def test_find_cycles_detects_multiple_sccs():
    pairs = [
        ("a", "b"),
        ("b", "a"),
        ("b", "c"),
        ("c", "b"),
        ("c", "d"),
        ("d", "e"),
        ("e", "d"),
        ("x", "y"),
        ("y", "x"),
    ]

    components = find_cycles(pairs)

    members = {
        frozenset(component["members"])
        for component in components
    }

    assert members == {
        frozenset({"a", "b", "c"}),
        frozenset({"d", "e"}),
        frozenset({"x", "y"}),
    }


def test_find_cycles_returns_exact_internal_edges():
    pairs = [
        ("a", "b"),
        ("b", "a"),
        ("b", "c"),
        ("c", "b"),
        ("c", "d"),
        ("d", "e"),
        ("e", "d"),
        ("outside", "a"),
    ]

    components = find_cycles(pairs)

    component = next(
        c
        for c in components
        if set(c["members"]) == {"a", "b", "c"}
    )

    assert component["size"] == 3

    assert set(component["internal_edges"]) == {
        "a -> b",
        "b -> a",
        "b -> c",
        "c -> b",
    }


def test_find_cycles_detects_self_loop_scc():
    components = find_cycles([
        ("a", "a"),
        ("b", "c"),
        ("c", "b"),
    ])

    members = {
        frozenset(component["members"])
        for component in components
    }

    assert members == {
        frozenset({"a"}),
        frozenset({"b", "c"}),
    }

    self_loop = next(
        c
        for c in components
        if c["members"] == ["a"]
    )

    assert self_loop["size"] == 1
    assert self_loop["internal_edges"] == ["a -> a"]


def test_find_cycles_excludes_one_way_connections():
    pairs = [
        ("a", "b"),
        ("b", "c"),
        ("c", "d"),
        ("d", "e"),
    ]

    assert find_cycles(pairs) == []
