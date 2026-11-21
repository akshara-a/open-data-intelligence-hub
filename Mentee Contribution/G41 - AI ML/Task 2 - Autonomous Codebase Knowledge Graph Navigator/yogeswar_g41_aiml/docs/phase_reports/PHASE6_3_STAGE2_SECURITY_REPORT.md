# Phase 6.3 — Stage 2 Security Preparation & Stage 3 Tailscale Setup Report

**Project:** Autonomous Codebase Knowledge Graph Navigator
**Execution Date:** 2026-11-14
**Audit Phase:** Phase 6.3 (Stage 2 Security Implementation & Stage 3 Tailscale Setup)
**Status:** **Pre-Flight Security Hardening Complete. Stopped at Mandatory Checkpoint Awaiting User Approval.**
**Public Deployment Status:** **NOT YET DEPLOYED (Local Only - No Funnel active).**

---

## 1. Summary of Changes & Files Modified

Four files were modified to eliminate wildcard CORS, secure authentication cookies over HTTPS, and map perimeter protocol headers without disrupting local development or existing test suites:

| File Path | Component | Scope of Change |
|---|---|---|
| `nginx/nginx.conf` | Ingress Reverse Proxy | Added `$http_x_forwarded_proto` mapping to `$forwarded_proto` for port 80; passes real HTTPS protocol to backend while preserving local HTTP. |
| `backend/app/main.py` | FastAPI Application | Replaced wildcard `allow_origins=["*"]` with explicit allowlist (local origins + configurable `CORS_ALLOWED_ORIGINS`); added `is_cookie_secure()` helper for HTTPS `Secure` cookie flag. |
| `docker-compose.yml` | Container Topology | Exposed `CORS_ALLOWED_ORIGINS` and `COOKIE_SECURE` environment variables to `backend` container. |
| `.env.production.example` | Environment Configuration | Added template variables for `CORS_ALLOWED_ORIGINS` and `COOKIE_SECURE`. |

---

## 2. Exact Security Changes Implemented

### 2.1 Perimeter Protocol Forwarding (`nginx/nginx.conf`)
- **Problem:** Nginx on port 80 previously set `proxy_set_header X-Forwarded-Proto $scheme;`. When Tailscale Funnel terminates public HTTPS and forwards to local port 80, `$scheme` is `http`, causing the backend to misidentify the client as insecure HTTP.
- **Implementation:** Added an Nginx mapping:
  ```nginx
  # Map forwarded protocol from trusted perimeter reverse proxy (e.g. Tailscale Funnel)
  # Defaults to $scheme for direct local connections
  map $http_x_forwarded_proto $forwarded_proto {
      default $http_x_forwarded_proto;
      ''      $scheme;
  }
  ```
  Updated all proxy locations on port 80 (`/api/v1/`, `/.well-known/`, `/`) to use:
  ```nginx
  proxy_set_header X-Forwarded-Proto $forwarded_proto;
  ```
- **Security Guarantee:** Does not force an HTTP-to-HTTPS redirect on local loopback (which would cause an infinite loop with Tailscale Funnel), but accurately conveys external HTTPS state to internal services.

### 2.2 Backend CORS Lockdown (`backend/app/main.py`)
- **Problem:** Wildcard `allow_origins=["*"]` with `allow_credentials=True` violates browser CORS specifications and permits cross-site requests to pass credentials.
- **Implementation:** Restricted allowed origins to an explicit whitelist of local development addresses plus any external domain supplied via `CORS_ALLOWED_ORIGINS`:
  ```python
  raw_cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
  default_origins = [
      "http://localhost", "http://localhost:80", "http://localhost:3000", "http://localhost:5173",
      "http://127.0.0.1", "http://127.0.0.1:80", "http://127.0.0.1:3000", "http://127.0.0.1:5173",
      "https://localhost", "https://localhost:443", "https://127.0.0.1", "https://127.0.0.1:443",
  ]
  allowed_origins = list(default_origins)
  if raw_cors_origins.strip():
      for origin in raw_cors_origins.split(","):
          cleaned = origin.strip().rstrip("/")
          if cleaned and cleaned not in allowed_origins:
              allowed_origins.append(cleaned)

  app.add_middleware(
      CORSMiddleware,
      allow_origins=allowed_origins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- **Verification:**
  - Request with `Origin: http://localhost:5173` returns `Access-Control-Allow-Origin: http://localhost:5173` and `Access-Control-Allow-Credentials: true`.
  - Request with `Origin: http://malicious-site.com` returns `Access-Control-Allow-Origin: None` (CORS headers suppressed).

### 2.3 Authentication Cookie Security (`backend/app/main.py`)
- **Problem:** Refresh token cookies had `secure=False` hardcoded.
- **Implementation:** Added helper function:
  ```python
  def is_cookie_secure(request: Optional[Request] = None) -> bool:
      env_setting = os.getenv("COOKIE_SECURE", "").strip().lower()
      if env_setting in ("true", "1", "yes"):
          return True
      if env_setting in ("false", "0", "no"):
          return False
      if request is not None and hasattr(request, "headers"):
          forwarded_proto = request.headers.get("x-forwarded-proto", "").lower()
          if forwarded_proto == "https":
              return True
      return False
  ```
  Applied to `login`, `refresh_token_endpoint`, and `logout`:
  ```python
  cookie_secure = is_cookie_secure(raw_request)
  response.set_cookie(
      key="refresh_token",
      value=raw_refresh_token,
      httponly=True,
      samesite="lax",
      secure=cookie_secure,
      path="/api/v1/auth",
      max_age=7 * 24 * 3600,
  )
  ```
- **Verification:**
  - Normal HTTP request: `Set-Cookie: refresh_token=...; HttpOnly; Max-Age=604800; Path=/api/v1/auth; SameSite=lax` (no Secure flag, local HTTP works).
  - HTTPS-forwarded request (`X-Forwarded-Proto: https`): `Set-Cookie: refresh_token=...; HttpOnly; Max-Age=604800; Path=/api/v1/auth; SameSite=lax; Secure` (Secure flag automatically enforced).

---

## 3. Test & Verification Results

### 3.1 Automated Regression Test Suite
- **Command:** `$env:ALLOW_EMBEDDING_FALLBACK="1"; python -m pytest -o pythonpath=. tests/`
- **Result:** **77 passed, 0 failed in 25.21s (100% pass rate)**
  - `tests/test_frontend_pages.py`: 3 passed
  - `tests/test_phase1_infrastructure.py`: 8 passed
  - `tests/test_phase2_ingestion.py`: 7 passed
  - `tests/test_phase3_cgg.py`: 12 passed
  - `tests/test_phase4_rag.py`: 9 passed
  - `tests/test_phase5_agent.py`: 24 passed
  - `tests/test_phase6_impact_reports_eval.py`: 14 passed

### 3.2 Frontend Production Build
- **Command:** `npm run build --prefix frontend`
- **Result:** `tsc && vite build` built cleanly with **0 errors in 2.08s**:
  - `dist/index.html` (0.78 kB)
  - `dist/assets/index-BImOWwh4.js` (233.17 kB)
- Bundle copied and live inside `frontend-1` container.

### 3.3 Live Docker Container Health Matrix
- All 7 microservices verified running and healthy:
  - `autonomous_codebase_knowledge_graph_navigator-nginx-1`: Up (Ports 80, 443)
  - `autonomous_codebase_knowledge_graph_navigator-frontend-1`: Up (Port 80 internal)
  - `autonomous_codebase_knowledge_graph_navigator-backend-1`: Up (Port 8000 internal, `sqlite_wal_wal` healthy)
  - `autonomous_codebase_knowledge_graph_navigator-mcp-1`: Up (Port 8000 internal, `neo4j_connected: true`, `git_storage_mounted: true`)
  - `autonomous_codebase_knowledge_graph_navigator-rag-1`: Up (Port 8000 internal, `active_transformer`, `all-mpnet-base-v2@9a32259`)
  - `autonomous_codebase_knowledge_graph_navigator-neo4j-1`: Up (healthy, 464 graph nodes)
  - `autonomous_codebase_knowledge_graph_navigator-ingestion-1`: Up (worker active)

### 3.4 Baseline Benchmark Preservation
- Curated 12-case benchmark suite results from Phase 6.1 (Run ID: `bm_9d36243d2937`) remain preserved as historical baseline in `app_state.db` and documented in `README.md`:
  - Pass Rate: **100.0% (12 / 12)**
  - Grounding Coverage: **95.83%**
  - Unsupported Claim Rate: **0.00%**
  - Unanswerable Query Detection: **100.00%**
  - Retrieval Recall@5: **66.67%**

---

## 4. Remaining Security Risks & Mitigations

1. **Self-Signed Certificate on Port 443:**
   - *Risk:* Accessing `https://localhost:443` directly still presents a self-signed certificate warning.
   - *Mitigation:* Tailscale Funnel will terminate public TLS on port 443 with an official Let's Encrypt certificate, proxying traffic over local loopback to `http://127.0.0.1:80`. External users will never see certificate warnings.
2. **Offline Mock LLM Provider Notice:**
   - *Risk:* External users querying the assistant will receive responses synthesized by `MockLLMProvider` rather than live OpenAI/Anthropic APIs.
   - *Mitigation:* Fully documented in UI and API; provides deterministic, offline-grounded responses with zero recurring token cost.

---

## 5. Stage 3 — Tailscale Setup Instructions (Windows 11)

The following step-by-step instructions are prepared for execution in Windows Command Prompt (CMD) or PowerShell:

### Step 1: Install Tailscale
Open Windows Command Prompt (as Administrator) and run:
```cmd
winget install tailscale.tailscale
```
*(Alternatively, download and run the installer from https://tailscale.com/download/windows).*

### Step 2: Sign In to Your Personal Account
After installation, start Tailscale and authenticate:
```cmd
tailscale up
```
*Effect:* Opens your default browser prompting you to log into your personal Google, GitHub, or Microsoft account. Once authenticated, your machine joins your private Tailnet.

### Step 3: Enable MagicDNS and HTTPS Certificates
1. Open your Tailscale Admin Console: **https://login.tailscale.com/admin/dns**
2. Ensure **MagicDNS** is toggled **ON**.
3. Under **HTTPS Certificates**, click **Enable HTTPS Certificates**.
   *Effect:* Allows Tailscale to automatically provision a free Let's Encrypt certificate for your node.

### Step 4: Authorize Funnel in Tailnet Policy (ACL)
1. Open the Tailscale Access Controls page: **https://login.tailscale.com/admin/acls**
2. In your `huJSON` policy file, ensure the `nodeAttrs` section permits Funnel (or add it if missing):
   ```json
   "nodeAttrs": [
     {
       "target": ["*"],
       "attr": ["funnel"]
     }
   ]
   ```
3. Click **Save**.

### Step 5: Verify Node Connectivity & Hostname
In Windows CMD, check your node status:
```cmd
tailscale status
```
*Effect:* Displays your node name and Tailscale IP (e.g. `100.x.y.z`).
To see your full MagicDNS domain name:
```cmd
tailscale cert
```
*(This displays `<your-machine-name>.<your-tailnet-name>.ts.net`).*

---

## 6. Exact Funnel Command (Awaiting User Approval)

Once Tailscale is authenticated and HTTPS/Funnel are enabled in your admin console, the exact command to publicly expose the application through Nginx on local port 80 is:

```cmd
tailscale funnel --bg 80
```
*Or with explicit loopback target:*
```cmd
tailscale funnel --bg http://127.0.0.1:80
```

### To Check Public URL Status:
```cmd
tailscale funnel status
```
*Output will display:*
```text
https://<your-machine-name>.<your-tailnet-name>.ts.net (funnel on)
|-- / proxy http://127.0.0.1:80
```

---

## 7. Mandatory Checkpoint

> **STATUS: STOPPED AT CHECKPOINT.**
> - No software has been automatically installed.
> - No Funnel command has been executed.
> - No public exposure or DNS modifications have taken place.
> - Awaiting explicit user instruction before proceeding to Stage 4.
