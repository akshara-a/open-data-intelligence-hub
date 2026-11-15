"""Demo microservice graph with deliberately planted architectural debt:
 * deprecated legacy-auth-module still on the critical path (also via auth-service-v2 fallback)
 * circular dependency order -> inventory -> notification -> order
 * shared database auth-sessions-db between legacy and v2 auth
 * legacy-auth-service as a high fan-in single point of failure
"""
from __future__ import annotations

NODES: dict[str, list[dict]] = {
    "Service": [
        {"name": "api-gateway", "team": "platform", "language": "Go", "tier": 0},
        {"name": "legacy-auth-service", "team": "identity", "language": "Java", "tier": 0, "deprecated": True},
        {"name": "auth-service-v2", "team": "identity", "language": "Kotlin", "tier": 0},
        {"name": "user-service", "team": "identity", "language": "Java", "tier": 1},
        {"name": "order-service", "team": "commerce", "language": "Java", "tier": 1},
        {"name": "inventory-service", "team": "commerce", "language": "Python", "tier": 1},
        {"name": "payment-service", "team": "payments", "language": "Java", "tier": 0},
        {"name": "notification-service", "team": "comms", "language": "Node", "tier": 2},
        {"name": "reporting-service", "team": "data", "language": "Python", "tier": 2},
    ],
    "Module": [
        {"name": "gateway-router"},
        {"name": "legacy-auth-module", "deprecated": True},
        {"name": "legacy-token-validator", "deprecated": True},
        {"name": "session-manager"},
        {"name": "user-profile-module"},
        {"name": "order-processing-module"},
        {"name": "stock-manager"},
        {"name": "payment-processor"},
        {"name": "email-dispatcher"},
        {"name": "report-builder"},
    ],
    "APIRoute": [
        {"name": "POST /auth/login", "method": "POST", "path": "/auth/login"},
        {"name": "GET /auth/validate", "method": "GET", "path": "/auth/validate"},
        {"name": "POST /v2/auth/token", "method": "POST", "path": "/v2/auth/token"},
        {"name": "GET /users/{id}", "method": "GET", "path": "/users/{id}"},
        {"name": "POST /orders", "method": "POST", "path": "/orders"},
        {"name": "GET /orders/{id}", "method": "GET", "path": "/orders/{id}"},
        {"name": "POST /inventory/reserve", "method": "POST", "path": "/inventory/reserve"},
        {"name": "POST /payments/charge", "method": "POST", "path": "/payments/charge"},
        {"name": "POST /notifications/send", "method": "POST", "path": "/notifications/send"},
        {"name": "GET /reports/sales", "method": "GET", "path": "/reports/sales"},
    ],
    "Database": [
        {"name": "auth-sessions-db"}, {"name": "users-db"}, {"name": "orders-db"},
        {"name": "inventory-db"}, {"name": "payments-db"},
    ],
    "FrontendComponent": [
        {"name": "web-login-page"}, {"name": "web-checkout-page"}, {"name": "mobile-app-auth"},
        {"name": "admin-dashboard"}, {"name": "customer-portal"},
    ],
}

# (src_label, src, rel, dst_label, dst)
_S, _M, _R, _D, _F = "Service", "Module", "APIRoute", "Database", "FrontendComponent"
EDGES: list[tuple[str, str, str, str, str]] = []


def _add(sl, s, rel, dl, d):
    EDGES.append((sl, s, rel, dl, d))


for svc, mod in [
    ("api-gateway", "gateway-router"), ("legacy-auth-service", "legacy-auth-module"),
    ("legacy-auth-service", "legacy-token-validator"), ("auth-service-v2", "session-manager"),
    ("user-service", "user-profile-module"), ("order-service", "order-processing-module"),
    ("inventory-service", "stock-manager"), ("payment-service", "payment-processor"),
    ("notification-service", "email-dispatcher"), ("reporting-service", "report-builder"),
]:
    _add(_S, svc, "CONTAINS", _M, mod)

for svc, route, mod in [
    ("legacy-auth-service", "POST /auth/login", "legacy-auth-module"),
    ("legacy-auth-service", "GET /auth/validate", "legacy-token-validator"),
    ("auth-service-v2", "POST /v2/auth/token", "session-manager"),
    ("user-service", "GET /users/{id}", "user-profile-module"),
    ("order-service", "POST /orders", "order-processing-module"),
    ("order-service", "GET /orders/{id}", "order-processing-module"),
    ("inventory-service", "POST /inventory/reserve", "stock-manager"),
    ("payment-service", "POST /payments/charge", "payment-processor"),
    ("notification-service", "POST /notifications/send", "email-dispatcher"),
    ("reporting-service", "GET /reports/sales", "report-builder"),
]:
    _add(_S, svc, "EXPOSES", _R, route)
    _add(_R, route, "IMPLEMENTED_BY", _M, mod)

# module -> module (hidden coupling: v2 falls back to legacy validator)
_add(_M, "legacy-token-validator", "CALLS", _M, "legacy-auth-module")
_add(_M, "session-manager", "CALLS", _M, "legacy-token-validator")

CALLS_ROUTE = {
    "gateway-router": ["POST /auth/login", "GET /auth/validate", "POST /v2/auth/token", "POST /orders", "GET /users/{id}", "GET /reports/sales"],
    "user-profile-module": ["GET /auth/validate"],
    "order-processing-module": ["GET /auth/validate", "POST /inventory/reserve", "POST /payments/charge"],
    "stock-manager": ["POST /notifications/send"],
    "email-dispatcher": ["GET /orders/{id}"],
    "payment-processor": ["GET /auth/validate", "POST /notifications/send"],
}
for mod, routes in CALLS_ROUTE.items():
    for r in routes:
        _add(_M, mod, "CALLS_ROUTE", _R, r)

for mod, db, rel in [
    ("legacy-auth-module", "auth-sessions-db", "WRITES_TO"), ("session-manager", "auth-sessions-db", "READS_FROM"),
    ("user-profile-module", "users-db", "WRITES_TO"), ("order-processing-module", "orders-db", "WRITES_TO"),
    ("stock-manager", "inventory-db", "WRITES_TO"), ("payment-processor", "payments-db", "WRITES_TO"),
    ("report-builder", "orders-db", "READS_FROM"),
]:
    _add(_M, mod, rel, _D, db)

for comp, routes in {
    "web-login-page": ["POST /auth/login"], "web-checkout-page": ["POST /orders", "GET /auth/validate"],
    "mobile-app-auth": ["POST /v2/auth/token"], "admin-dashboard": ["GET /reports/sales"],
    "customer-portal": ["GET /users/{id}", "GET /orders/{id}"],
}.items():
    for r in routes:
        _add(_F, comp, "CONSUMES", _R, r)


def derived_service_deps() -> list[tuple[str, str, str, str, str]]:
    """Service-level DEPENDS_ON derived from module-level calls (mirrors what a real graph often stores)."""
    owner_mod = {d: s for (_, s, rel, _, d) in EDGES if rel == "CONTAINS"}
    owner_route = {d: s for (_, s, rel, _, d) in EDGES if rel == "EXPOSES"}
    owner_mod_by_route = {}
    deps = set()
    for (_, a, rel, _, b) in EDGES:
        if rel == "CALLS_ROUTE":
            sa, sb = owner_mod.get(a), owner_route.get(b)
        elif rel == "CALLS":
            sa, sb = owner_mod.get(a), owner_mod.get(b)
        else:
            continue
        if sa and sb and sa != sb:
            deps.add((sa, sb))
    return [(_S, a, "DEPENDS_ON", _S, b) for a, b in sorted(deps)]


EDGES.extend(derived_service_deps())
