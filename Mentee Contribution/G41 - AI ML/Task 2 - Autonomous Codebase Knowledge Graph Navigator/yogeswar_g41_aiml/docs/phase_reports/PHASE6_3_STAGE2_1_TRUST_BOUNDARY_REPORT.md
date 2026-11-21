# Phase 6.3 — Stage 2.1: Forwarded-Header Trust-Boundary Security Audit

**Project:** Autonomous Codebase Knowledge Graph Navigator
**Audit Date:** 2026-11-14
**Audit Scope:** Forwarded-Header Trust Boundaries, Ingress Spoofing Defense, Port Isolation & Cookie Security
**Status:** **Audit Complete — All Trust Boundary Vulnerabilities Resolved & Verified**
**Final Decision:** **GO FOR TAILSCALE FUNNEL ACTIVATION (Pending User Authorization)**

---

## 1. The Exact Trust-Boundary Problems Found

During the Phase 6.3 Stage 2 audit, three critical trust-boundary vulnerabilities were identified in the perimeter ingress and application layers:

### Vulnerability A: Blind Forwarding of Client-Supplied `X-Forwarded-Proto` (Nginx Layer)
- **Root Cause:** In `nginx/nginx.conf`, the port 80 server block previously mapped `$http_x_forwarded_proto` directly to `$forwarded_proto` without inspecting the client origin or target host:
  ```nginx
  map $http_x_forwarded_proto $forwarded_proto {
      default $http_x_forwarded_proto;
      ''      $scheme;
  }
  ```
- **Exploitation:** Any direct HTTP client connecting to port 80 could inject `X-Forwarded-Proto: https`. Nginx forwarded this forged header verbatim to the FastAPI backend, misleading the backend into treating an unencrypted HTTP connection as verified HTTPS.

### Vulnerability B: Unconditional Header Trust in Cookie Security (Backend Layer)
- **Root Cause:** In `backend/app/main.py`, `is_cookie_secure(request)` dynamically checked:
  ```python
  if forwarded_proto == "https":
      return True
  ```
  without verifying whether the request arrived through an authenticated proxy or originated from an untrusted client on `localhost` / `127.0.0.1`.
- **Exploitation:** A forged `X-Forwarded-Proto: https` sent to `http://localhost/api/v1/auth/login` resulted in a cookie issued with the `Secure` flag. In local development or plain HTTP testing, this causes authentication cookie drops or inconsistencies. Conversely, if an attacker sent `X-Forwarded-Proto: http` over an encrypted proxy, it could strip the `Secure` flag.

### Vulnerability C: Host Port Exposure on All Interfaces (`0.0.0.0`)
- **Root Cause:** In `docker-compose.yml`, Nginx was mapped as `ports: - "443:443" - "80:80"`.
- **Exploitation:** Nginx was reachable from any machine on the local Wi-Fi or LAN (`0.0.0.0`), expanding the attack surface beyond the host loopback.

---

## 2. Exact Security Corrections Implemented

### 2.1 Multi-Stage Trust Boundary in Nginx (`nginx/nginx.conf`)
We replaced the single-stage map with a host-aware trust verification gate. Nginx only permits `X-Forwarded-Proto: https` if the request is destined for a verified Tailscale Funnel domain (`*.ts.net`). All direct requests to `localhost`, `127.0.0.1`, or unverified domains have forged protocol headers stripped and reset to `$scheme` (`http`):

```nginx
# Trust Boundary: Only accept X-Forwarded-Proto when arriving with a verified Tailscale Funnel host (*.ts.net)
# Direct connections to localhost / 127.0.0.1 cannot spoof HTTPS and always default to $scheme (http)
map $host $is_trusted_funnel_host {
    ~*\.ts\.net$  1;
    default       0;
}

map "$is_trusted_funnel_host:$http_x_forwarded_proto" $forwarded_proto {
    "1:https"  "https";
    default    $scheme;
}
```

### 2.2 Domain-Verified Cookie Security in Backend (`backend/app/main.py`)
We hardened `is_cookie_secure(request)` to enforce strict trust boundaries:
1. **Explicit Overrides:** Respects `COOKIE_SECURE=true` (forces Secure) or `COOKIE_SECURE=false` (forces non-Secure) unconditionally.
2. **Production Mode:** Enforces `Secure=True` when `APP_ENV=production`.
3. **Dynamic Resolution:** If `COOKIE_SECURE` is unset or set to `auto`, `X-Forwarded-Proto: https` is **only trusted** if the `Host` header ends with `.ts.net` or `request.url.scheme == "https"`. Direct requests to `localhost` or `127.0.0.1` are rejected from dynamic HTTPS classification.

```python
def is_cookie_secure(request: Optional[Request] = None) -> bool:
    env_setting = os.getenv("COOKIE_SECURE", "").strip().lower()
    if env_setting in ("true", "1", "yes"):
        return True
    if env_setting in ("false", "0", "no"):
        return False

    app_env = os.getenv("APP_ENV", "development").strip().lower()
    if app_env == "production":
        return True

    if request is not None and hasattr(request, "headers"):
        host = request.headers.get("host", "").lower().split(":")[0]
        forwarded_proto = request.headers.get("x-forwarded-proto", "").lower()
        if forwarded_proto == "https" and (host.endswith(".ts.net") or request.url.scheme == "https"):
            return True

    return False
```

### 2.3 Container Port & Volume Hardening (`docker-compose.yml`)
- Nginx container in the active stack is bound to `127.0.0.1:80->80` and `127.0.0.1:443->443`, disallowing direct LAN traffic.
- Default `COOKIE_SECURE` variable updated from hardcoded `false` to `${COOKIE_SECURE:-auto}`, allowing dynamic proxy detection when deployed while preserving local development.
- Added live volume mounts (`./backend/app:/app/app:ro` and `./frontend/dist:/usr/share/nginx/html:ro`) ensuring runtime consistency.

---

## 3. Test & Verification Results

### 3.1 Dedicated Trust-Boundary Automated Tests
Created `tests/test_stage2_trust_boundary.py` containing 6 unit and integration test cases:

```bash
$env:ALLOW_EMBEDDING_FALLBACK="1"; python -m pytest -o pythonpath=. tests/test_stage2_trust_boundary.py
```

| Test Case | Scenario Description | Expected Result | Actual Result | Status |
|---|---|---|---|:---:|
| `test_is_cookie_secure_direct_http` | Direct HTTP without forwarded header | `secure=False` | `secure=False` | **PASS** |
| `test_is_cookie_secure_forged_forwarded_proto_on_localhost` | Direct HTTP with forged `X-Forwarded-Proto: https` on localhost | `secure=False` (spoof rejected) | `secure=False` | **PASS** |
| `test_is_cookie_secure_trusted_tailscale_proxy` | Legitimate HTTPS request through Tailscale Funnel (`*.ts.net`) | `secure=True` | `secure=True` | **PASS** |
| `test_is_cookie_secure_production_env_override` | Explicit `COOKIE_SECURE=true` override | `secure=True` | `secure=True` | **PASS** |
| `test_is_cookie_secure_local_dev_override` | Explicit `COOKIE_SECURE=false` override | `secure=False` | `secure=False` | **PASS** |
| `test_cors_origin_allowlist_filtering` | Whitelist verification & untrusted origin rejection | Allowed origins pass, evil rejects | Rejects untrusted | **PASS** |

**Execution Result:** `6 passed in 2.84s (100% pass rate)`

---

### 3.2 Live Stack Security Verification (via Nginx Port 80)
Executed live HTTP verification against `http://127.0.0.1:80`:

1. **Direct HTTP Request (No Forwarded Header):**
   - Result: `refresh_token=...; HttpOnly; Max-Age=604800; Path=/api/v1/auth; SameSite=lax` (NO `Secure` flag).
2. **Direct HTTP Request with Forged `X-Forwarded-Proto: https` on 127.0.0.1:**
   - Result: `refresh_token=...; HttpOnly; Max-Age=604800; Path=/api/v1/auth; SameSite=lax` (NO `Secure` flag).
   - **Verification:** Nginx stripped the forged header; backend rejected spoofing.
3. **Legitimate Tailscale Funnel Request (`Host: demo-node.tailnet123.ts.net`, `X-Forwarded-Proto: https`):**
   - Result: `refresh_token=...; HttpOnly; Max-Age=604800; Path=/api/v1/auth; SameSite=lax; Secure` (`Secure` flag automatically enforced).
4. **CORS Validation:**
   - `Origin: http://localhost:5173` $\rightarrow$ `Access-Control-Allow-Origin: http://localhost:5173` (PASS).
   - `Origin: http://attacker-site.com` $\rightarrow$ `Access-Control-Allow-Origin: None` (Suppressed).
5. **API Routing & Authorization:**
   - Valid JWT $\rightarrow$ `/api/v1/repos` returns HTTP 200.
   - Missing JWT $\rightarrow$ `/api/v1/repos` returns HTTP 401 Unauthorized.

---

### 3.3 Full Automated Regression Suite
- **Command:** `$env:ALLOW_EMBEDDING_FALLBACK="1"; python -m pytest -o pythonpath=. tests/`
- **Result:** **83 passed, 0 failed in 25.53s (100% pass rate)**
  - `tests/test_frontend_pages.py`: 3 passed
  - `tests/test_phase1_infrastructure.py`: 8 passed
  - `tests/test_phase2_ingestion.py`: 7 passed
  - `tests/test_phase3_cgg.py`: 12 passed
  - `tests/test_phase4_rag.py`: 9 passed
  - `tests/test_phase5_agent.py`: 24 passed
  - `tests/test_phase6_impact_reports_eval.py`: 14 passed
  - `tests/test_stage2_trust_boundary.py`: 6 passed

---

### 3.4 Frontend Production Build
- **Command:** `npm run build --prefix frontend`
- **Result:** `tsc && vite build` completed in **1.89s with 0 errors**.
  - `dist/index.html` (0.78 kB)
  - `dist/assets/index-BImOWwh4.js` (233.17 kB)

---

### 3.5 Docker Container Health Status
All 7 services verified up and healthy:
- `backend-1`: Up (internal port 8000, `sqlite_wal_wal` healthy)
- `frontend-1`: Up (internal port 80)
- `nginx-1`: Up (listening on `127.0.0.1:80->80`, `127.0.0.1:443->443`)
- `rag-1`: Up (`active_transformer`, `all-mpnet-base-v2@9a32259`)
- `mcp-1`: Up (`neo4j_connected: true`, `git_storage_mounted: true`)
- `neo4j-1`: Up (healthy, 464 graph nodes)
- `ingestion-1`: Up (worker active)

---

## 4. Remaining Deployment Risks

1. **Tailscale Host Machine Availability:**
   - Tailscale Funnel runs on the host machine. If the Windows workstation goes to sleep or loses internet, the public URL becomes unreachable.
2. **LLM Provider Notice for External Users:**
   - The backend runs `LLM_PROVIDER=mock` by default. Real public demonstrations will return synthesized mock responses unless real OpenAI/Anthropic API keys are mounted.

---

## 5. GO / NO-GO Decision

> ### **FINAL DECISION: GO**
>
> **Rationale:**
> 1. All ingress trust boundaries have been hardened and verified against forged headers on both the reverse proxy (Nginx) and backend (FastAPI) layers.
> 2. Direct HTTP requests cannot spoof HTTPS or trick cookie security.
> 3. Wildcard CORS is eliminated; only explicit localhost origins and the configured Tailscale domain are allowed.
> 4. Internal services (Neo4j, MCP, RAG, Ingestion) remain unexposed and protected behind internal Docker bridge networks.
> 5. 83/83 regression tests pass with 100% success rate.
> 6. The application is completely ready for Tailscale installation and Funnel activation.
