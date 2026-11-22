import os
import uuid
import datetime
import logging
import httpx
from contextlib import asynccontextmanager

logger = logging.getLogger("backend.main")
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, check_wal_mode, get_db_connection, hash_password
from .auth import (
    create_access_token,
    mint_refresh_token,
    rotate_refresh_token,
    revoke_token_family,
    revoke_user_tokens,
    verify_access_token,
    create_internal_service_token,
    get_jwks,
    ACCESS_TOKEN_LIFETIME_SECONDS,
    VALID_ROLES,
)
from .schemas import (
    LoginRequest,
    TokenResponse,
    MessageResponse,
    CreateRepoRequest,
    IngestRequest,
    RepoResponse,
    SnapshotResponse,
    JobStatusResponse,
    HealthResponse,
    UserResponse,
    CreateUserRequest,
    UpdateUserStatusRequest,
    UpdateUserRoleRequest,
    ResetPasswordRequest,
    RepoMemberResponse,
    AddRepoMemberRequest,
)
from .agent import (
    AssistantChatRequest,
    AssistantChatResponse,
    AssistantThreadSummary,
    run_supervisor_workflow,
    get_llm_provider,
)
from .agent.checkpoint_store import (
    list_snapshot_threads,
    get_thread_history,
    mark_thread_cancelled,
)
from .impact import (
    ChangeImpactRequest,
    ChangeImpactResponse,
    run_change_impact_analysis,
)
from .reports import (
    GenerateReportRequest,
    ReportSummary,
    ReportDetail,
    generate_technical_report,
    list_reports,
    get_report_by_id,
    delete_report_by_id,
)
from .evaluation import (
    ExecuteBenchmarkRequest,
    BenchmarkRunSummary,
    BenchmarkRunResponse,
    execute_benchmark_suite,
    list_benchmark_runs,
    get_benchmark_run_by_id,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database with strict WAL mode on startup
    init_db()
    yield


app = FastAPI(
    title="Autonomous Codebase Knowledge Graph Navigator - Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS: explicit allowlist preserving local development origins
# Additional production origins (e.g., Tailscale Funnel FQDN) can be configured via CORS_ALLOWED_ORIGINS
raw_cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
default_origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://localhost",
    "https://localhost:443",
    "https://127.0.0.1",
    "https://127.0.0.1:443",
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


def is_cookie_secure(request: Optional[Request] = None) -> bool:
    """Determine whether authentication cookies should have the Secure flag.
    
    Security rules:
    1. Explicit COOKIE_SECURE environment variable always takes precedence:
       - 'true' / '1' / 'yes' => True
       - 'false' / '0' / 'no' => False
    2. Explicit production mode (APP_ENV=production) enforces True.
    3. For dynamic resolution:
       - A request is only considered HTTPS if the scheme is 'https', OR
         if X-Forwarded-Proto is 'https' AND the Host header represents a trusted proxy domain (*.ts.net).
       - Direct requests to localhost or 127.0.0.1 cannot spoof HTTPS cookies.
    """
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


@app.get("/health", response_model=HealthResponse)
@app.get("/api/v1/health", response_model=HealthResponse)
def health_check():
    wal_status = check_wal_mode()
    return HealthResponse(
        status="healthy",
        service="backend",
        database=f"sqlite_wal_{wal_status.lower()}",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )


@app.get("/.well-known/jwks.json")
def jwks_endpoint():
    return get_jwks()


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(request: LoginRequest, response: Response, raw_request: Request = None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username, password_hash, role, is_active FROM users WHERE username = ?",
            (request.username,),
        )
        user = cursor.fetchone()

    if not user or user["password_hash"] != hash_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if user["is_active"] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    access_token = create_access_token(
        user_id=user["user_id"],
        username=user["username"],
        role=user["role"],
    )
    raw_refresh_token, family_id = mint_refresh_token(user_id=user["user_id"])

    # Set secure HTTP-only refresh cookie per Section 14.1
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

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_LIFETIME_SECONDS,
    )


@app.post("/api/v1/auth/refresh", response_model=TokenResponse)
def refresh_token_endpoint(
    request: Request,
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
):
    token_to_rotate = refresh_token or request.headers.get("X-Refresh-Token")
    if not token_to_rotate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )

    new_access_token, new_refresh_token, _ = rotate_refresh_token(token_to_rotate)

    cookie_secure = is_cookie_secure(request)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=cookie_secure,
        path="/api/v1/auth",
        max_age=7 * 24 * 3600,
    )

    return TokenResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_LIFETIME_SECONDS,
    )


@app.post("/api/v1/auth/logout", response_model=MessageResponse)
def logout(
    request: Request,
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
):
    token_to_revoke = refresh_token or request.headers.get("X-Refresh-Token")
    if token_to_revoke:
        revoke_token_family(token_to_revoke)

    cookie_secure = is_cookie_secure(request)
    response.delete_cookie(key="refresh_token", path="/api/v1/auth", secure=cookie_secure)
    return MessageResponse(message="Successfully logged out and session revoked")


def get_authenticated_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split(" ", 1)[1]
    payload = verify_access_token(token)
    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload["user_id"] = user_id

    # Authoritative active check & role refresh from database (prevents privilege escalation & honors immediate deactivation)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, role, is_active FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row and payload.get("username"):
            cursor.execute("SELECT user_id, role, is_active FROM users WHERE username = ?", (payload["username"],))
            row = cursor.fetchone()
            if row:
                user_id = row["user_id"]
                payload["user_id"] = user_id

        if not row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account no longer exists",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if row["is_active"] != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )
        payload["role"] = row["role"]
    return payload


def require_admin(user: dict):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required",
        )


@app.get("/api/v1/repos", response_model=List[RepoResponse])
def list_repositories(request: Request):
    user = get_authenticated_user(request)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if user.get("role") == "admin":
            cursor.execute("SELECT repo_id, name, git_url, default_branch, status, created_at FROM repositories")
        else:
            cursor.execute(
                """
                SELECT r.repo_id, r.name, r.git_url, r.default_branch, r.status, r.created_at
                FROM repositories r
                JOIN repo_memberships m ON r.repo_id = m.repo_id
                WHERE m.user_id = ?
                """,
                (user["user_id"],),
            )
        rows = cursor.fetchall()
        return [
            RepoResponse(
                repo_id=row["repo_id"],
                name=row["name"],
                git_url=row["git_url"],
                default_branch=row["default_branch"],
                status=row["status"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


@app.post("/api/v1/repos", response_model=RepoResponse, status_code=status.HTTP_201_CREATED)
def create_repository(req: CreateRepoRequest, request: Request):
    user = get_authenticated_user(request)
    require_admin(user)
    repo_id = str(uuid.uuid4())
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO repositories (repo_id, name, git_url, default_branch, status)
            VALUES (?, ?, ?, ?, 'ACTIVE')
            """,
            (repo_id, req.name, req.git_url, req.default_branch),
        )
        # Grant owner membership to authenticated admin
        user_id = user.get("sub", "usr_admin_default")
        cursor.execute(
            """
            INSERT OR IGNORE INTO repo_memberships (id, user_id, repo_id, role)
            VALUES (?, ?, ?, 'owner')
            """,
            (f"mem_{uuid.uuid4()}", user_id, repo_id),
        )
        conn.commit()

    return RepoResponse(
        repo_id=repo_id,
        name=req.name,
        git_url=req.git_url,
        default_branch=req.default_branch,
        status="ACTIVE",
        created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )


@app.post("/api/v1/repos/{repo_id}/ingest", response_model=JobStatusResponse)
def trigger_ingest(repo_id: str, req: IngestRequest, request: Request):
    user = get_authenticated_user(request)
    require_admin(user)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM repositories WHERE repo_id = ?", (repo_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Repository not found")
        if row["status"] == "DELETING":
            raise HTTPException(status_code=409, detail="REPOSITORY_LOCKED")

        job_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO jobs (id, repo_id, commit_sha, job_type, status, progress)
            VALUES (?, ?, ?, 'INGEST', 'PENDING', 0)
            """,
            (job_id, repo_id, req.commit_sha),
        )
        conn.commit()

    return JobStatusResponse(
        job_id=job_id,
        repo_id=repo_id,
        commit_sha=req.commit_sha,
        job_type="INGEST",
        status="PENDING",
        progress=0,
    )


@app.get("/api/v1/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, request: Request):
    user = get_authenticated_user(request)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, repo_id, commit_sha, job_type, status, progress, log_output FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")

        # Non-admins must have access to the job's repository
        if user.get("role") != "admin":
            verify_repo_access(user, row["repo_id"])

        return JobStatusResponse(
            job_id=row["id"],
            repo_id=row["repo_id"],
            commit_sha=row["commit_sha"],
            job_type=row["job_type"],
            status=row["status"],
            progress=row["progress"],
            log_output=row["log_output"],
        )


@app.delete("/api/v1/repos/{repo_id}", response_model=MessageResponse)
def delete_repository(repo_id: str, request: Request):
    user = get_authenticated_user(request)
    require_admin(user)
    """
    Privileged repository deletion lifecycle per Section 8.1 / AC-5.3:
    1. Sets status = 'DELETING'
    2. Enqueues privileged cleanup job REPO_PURGE
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM repositories WHERE repo_id = ?", (repo_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Repository not found")

        cursor.execute("UPDATE repositories SET status = 'DELETING' WHERE repo_id = ?", (repo_id,))
        job_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO jobs (id, repo_id, commit_sha, job_type, status, progress)
            VALUES (?, ?, 'N/A', 'REPO_PURGE', 'PENDING', 0)
            """,
            (job_id, repo_id),
        )
        conn.commit()

    return MessageResponse(message=f"Repository {repo_id} deletion initiated. Enqueued purge job {job_id}")


def verify_repo_access(user: dict, repo_id: str, write: bool = False):
    """
    Authoritative tenant-level repository membership check (Section 4.2 / 14.2).
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (repo_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository '{repo_id}' not found",
            )
        if user.get("role") == "admin":
            return
        user_id = user.get("sub") or user.get("user_id")
        cursor.execute(
            "SELECT role FROM repo_memberships WHERE user_id = ? AND repo_id = ?",
            (user_id, repo_id),
        )
        membership = cursor.fetchone()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: user is not a member of this repository",
            )
        if write and user.get("role") == "viewer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Read-only access: viewers cannot modify repository resources",
            )


@app.get("/api/v1/repos/{repo_id}/snapshots", response_model=List[SnapshotResponse])
def list_snapshots(repo_id: str, request: Request):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    # Retrieve distinct commits ingested for this repository
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT commit_sha, created_at FROM jobs
            WHERE repo_id = ? AND job_type = 'INGEST' AND status = 'COMPLETED'
            ORDER BY created_at DESC
            """,
            (repo_id,),
        )
        rows = cursor.fetchall()
        if rows:
            return [
                SnapshotResponse(repo_id=repo_id, commit_sha=r["commit_sha"], created_at=r["created_at"])
                for r in rows
            ]

    # Baseline snapshot
    return [
        SnapshotResponse(
            repo_id=repo_id,
            commit_sha="c0ffee1234567890abcdef1234567890abcdef12",
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
    ]


MCP_SERVICE_URL = os.getenv("MCP_SERVICE_URL", "http://mcp:8000")


async def forward_to_cgg(
    path: str,
    repo_id: str,
    commit_sha: str,
    method: str = "POST",
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    service_token = create_internal_service_token(repo_id=repo_id, commit_sha=commit_sha)
    headers = {"X-Internal-Service-Auth": service_token}
    url = f"{MCP_SERVICE_URL}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            if method == "POST":
                resp = await client.post(url, json=json_data, headers=headers)
            else:
                resp = await client.get(url, params=params, headers=headers)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to communicate with CGG service: {str(e)}",
            )
        if resp.status_code >= 400:
            err_body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            raise HTTPException(status_code=resp.status_code, detail=err_body)
        return resp.json()


class GraphQueryRequest(BaseModel):
    operation: str
    parameters: Dict[str, Any] = {}


@app.post("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/query")
async def run_graph_query(
    repo_id: str,
    commit_sha: str,
    req: GraphQueryRequest,
    request: Request,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_cgg(
        "/api/v1/tools/run_query",
        repo_id,
        commit_sha,
        method="POST",
        json_data={
            "operation": req.operation,
            "parameters": req.parameters,
            "repo_id": repo_id,
            "commit_sha": commit_sha,
        },
    )


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/statistics")
async def get_snapshot_graph_statistics(
    repo_id: str,
    commit_sha: str,
    request: Request,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_cgg(
        "/api/v1/cgg/statistics",
        repo_id,
        commit_sha,
        method="POST",
        json_data={"repo_id": repo_id, "commit_sha": commit_sha},
    )


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities")
async def get_snapshot_entities(
    repo_id: str,
    commit_sha: str,
    request: Request,
    name: Optional[str] = None,
    entity_type: Optional[str] = None,
    file_path: Optional[str] = None,
    entity_id: Optional[str] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)

    # If caller explicitly provided pagination parameters, forward directly
    if limit is not None or skip is not None:
        return await forward_to_cgg(
            "/api/v1/cgg/entity_lookup",
            repo_id,
            commit_sha,
            method="POST",
            json_data={
                "name": name,
                "entity_type": entity_type,
                "file_path": file_path,
                "entity_id": entity_id,
                "limit": limit,
                "skip": skip if skip is not None else 0,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            },
        )

    # Otherwise (e.g. dashboard browsing), safely aggregate pages up to a reasonable cap
    # Each individual CGG query is bounded to <= 500 per AC-3.1 / AC-3.2
    all_entities = []
    current_skip = 0
    page_limit = 500
    max_total_entities = 5000

    while len(all_entities) < max_total_entities:
        page_res = await forward_to_cgg(
            "/api/v1/cgg/entity_lookup",
            repo_id,
            commit_sha,
            method="POST",
            json_data={
                "name": name,
                "entity_type": entity_type,
                "file_path": file_path,
                "entity_id": entity_id,
                "limit": page_limit,
                "skip": current_skip,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            },
        )
        entities = page_res.get("entities", [])
        all_entities.extend(entities)
        if len(entities) < page_limit:
            break
        current_skip += page_limit

    return {"entities": all_entities, "count": len(all_entities)}


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities/{entity_id}")
async def get_snapshot_entity_details(
    repo_id: str,
    commit_sha: str,
    entity_id: str,
    request: Request,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_cgg(
        "/api/v1/cgg/entity_details",
        repo_id,
        commit_sha,
        method="POST",
        json_data={
            "entity_id": entity_id,
            "repo_id": repo_id,
            "commit_sha": commit_sha,
        },
    )


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities/{entity_id}/neighbors")
async def get_snapshot_entity_neighbors(
    repo_id: str,
    commit_sha: str,
    entity_id: str,
    request: Request,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_cgg(
        "/api/v1/cgg/direct_neighbors",
        repo_id,
        commit_sha,
        method="POST",
        json_data={
            "entity_id": entity_id,
            "repo_id": repo_id,
            "commit_sha": commit_sha,
        },
    )


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/evidence/{evidence_id}")
async def get_snapshot_evidence(
    repo_id: str,
    commit_sha: str,
    evidence_id: str,
    request: Request,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_cgg(
        f"/api/v1/tools/evidence/{evidence_id}",
        repo_id,
        commit_sha,
        method="GET",
        params={"repo_id": repo_id, "commit_sha": commit_sha},
    )


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/relationships")
async def get_snapshot_relationships(
    repo_id: str,
    commit_sha: str,
    request: Request,
    relationship_type: Optional[str] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)

    if limit is not None or skip is not None:
        return await forward_to_cgg(
            "/api/v1/cgg/relationships",
            repo_id,
            commit_sha,
            method="POST",
            json_data={
                "relationship_type": relationship_type,
                "limit": limit,
                "skip": skip if skip is not None else 0,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            },
        )

    all_relationships = []
    current_skip = 0
    page_limit = 500
    max_total = 5000

    while len(all_relationships) < max_total:
        page_res = await forward_to_cgg(
            "/api/v1/cgg/relationships",
            repo_id,
            commit_sha,
            method="POST",
            json_data={
                "relationship_type": relationship_type,
                "limit": page_limit,
                "skip": current_skip,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            },
        )
        rels = page_res.get("relationships", [])
        all_relationships.extend(rels)
        if len(rels) < page_limit:
            break
        current_skip += page_limit

    return {"relationships": all_relationships, "count": len(all_relationships)}


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/unresolved_calls")
async def get_snapshot_unresolved_calls(
    repo_id: str,
    commit_sha: str,
    request: Request,
    source_entity_id: Optional[str] = None,
    file_path: Optional[str] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)

    if limit is not None or skip is not None:
        return await forward_to_cgg(
            "/api/v1/cgg/unresolved_calls",
            repo_id,
            commit_sha,
            method="POST",
            json_data={
                "source_entity_id": source_entity_id,
                "file_path": file_path,
                "limit": limit,
                "skip": skip if skip is not None else 0,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            },
        )

    all_calls = []
    current_skip = 0
    page_limit = 500
    max_total_calls = 5000

    while len(all_calls) < max_total_calls:
        page_res = await forward_to_cgg(
            "/api/v1/cgg/unresolved_calls",
            repo_id,
            commit_sha,
            method="POST",
            json_data={
                "source_entity_id": source_entity_id,
                "file_path": file_path,
                "limit": page_limit,
                "skip": current_skip,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            },
        )
        calls = page_res.get("unresolved_calls", [])
        all_calls.extend(calls)
        if len(calls) < page_limit:
            break
        current_skip += page_limit

    return {"unresolved_calls": all_calls, "count": len(all_calls)}


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/file")
async def read_snapshot_file(
    repo_id: str,
    commit_sha: str,
    file_path: str,
    request: Request,
    start_line: int = 1,
    end_line: int = 100,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_cgg(
        "/api/v1/tools/file",
        repo_id,
        commit_sha,
        method="GET",
        params={
            "file_path": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "repo_id": repo_id,
            "commit_sha": commit_sha,
        },
    )


RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag:8000")


async def forward_to_rag(
    path: str,
    method: str = "POST",
    json_data: Optional[Dict[str, Any]] = None,
) -> Any:
    url = f"{RAG_SERVICE_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "POST":
                resp = await client.post(url, json=json_data)
            else:
                resp = await client.get(url)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to communicate with RAG service: {str(e)}",
            )
        if resp.status_code >= 400:
            err_body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            raise HTTPException(status_code=resp.status_code, detail=err_body)
        return resp.json()


@app.get("/api/v1/rag/health")
async def get_rag_health():
    raw_data = await forward_to_rag("/health", method="GET")
    return {
        "status": raw_data.get("status", "healthy"),
        "service": raw_data.get("service", "graph_rag"),
        "model_status": raw_data.get("model_status", "active"),
        "timestamp": raw_data.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
    }


class BackendRAGIndexRequest(BaseModel):
    force_reindex: bool = False


@app.post("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/index")
async def trigger_snapshot_rag_index(
    repo_id: str,
    commit_sha: str,
    req: BackendRAGIndexRequest,
    request: Request,
):
    user = get_authenticated_user(request)
    require_admin(user)
    verify_repo_access(user, repo_id)
    return await forward_to_rag(
        "/api/v1/rag/index",
        method="POST",
        json_data={
            "repo_id": repo_id,
            "commit_sha": commit_sha,
            "force_reindex": req.force_reindex,
        },
    )


class BackendRAGRetrieveRequest(BaseModel):
    query: str
    top_k: int = 10
    include_graph: bool = True
    max_graph_hops: int = 2


@app.post("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/retrieve")
async def trigger_snapshot_rag_retrieve(
    repo_id: str,
    commit_sha: str,
    req: BackendRAGRetrieveRequest,
    request: Request,
):
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await forward_to_rag(
        "/api/v1/rag/retrieve",
        method="POST",
        json_data={
            "repo_id": repo_id,
            "commit_sha": commit_sha,
            "query": req.query,
            "top_k": req.top_k,
            "include_graph": req.include_graph,
            "max_graph_hops": req.max_graph_hops,
        },
    )


# ============================================================================
# Phase 5: AI Assistant & LangGraph Supervisor Endpoints
# ============================================================================

@app.get("/api/v1/assistant/health")
def get_assistant_health():
    """Health check for AI Assistant LLM provider configuration (sanitized)."""
    provider = get_llm_provider()
    raw = provider.health()
    return {
        "status": raw.get("status", "healthy"),
        "service": "assistant",
        "configured": raw.get("configured", True),
    }


@app.post(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/chat",
    response_model=AssistantChatResponse,
)
async def assistant_chat_endpoint(
    repo_id: str,
    commit_sha: str,
    req: AssistantChatRequest,
    request: Request,
):
    """
    Submits an architectural or codebase question to the LangGraph supervisor workflow.
    Executes bounded multi-stage reasoning against GraphRAG and MCP tools, returning
    a grounded, evidence-backed answer.
    """
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)

    # Execute LangGraph supervisor workflow
    try:
        final_state = await run_supervisor_workflow(
            repo_id=repo_id,
            commit_sha=commit_sha,
            user_id=user["user_id"],
            question=req.question,
            thread_id=req.thread_id,
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except Exception as e:
        logger.error("Supervisor workflow execution error: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assistant workflow failed: {str(e)}",
        )

    if final_state.get("status") in ("FAILED", "FORBIDDEN"):
        status_code = status.HTTP_403_FORBIDDEN if final_state.get("status") == "FORBIDDEN" else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=final_state.get("error", "Workflow failed"))

    answer = final_state.get("answer")
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workflow did not generate an answer output.",
        )

    return AssistantChatResponse(
        thread_id=final_state["thread_id"],
        repo_id=repo_id,
        commit_sha=commit_sha,
        question=req.question,
        status=final_state.get("status", "COMPLETED"),
        answer=answer,
        evidence=final_state.get("retrieved_evidence", []),
        tool_trace=final_state.get("tool_results", []),
        execution_time_ms=final_state.get("execution_time_ms", 0.0),
    )


@app.get(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/threads",
    response_model=List[AssistantThreadSummary],
)
def get_snapshot_threads_endpoint(
    repo_id: str,
    commit_sha: str,
    request: Request,
):
    """Lists conversation threads for the authenticated user and snapshot."""
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    threads = list_snapshot_threads(user["user_id"], repo_id, commit_sha)
    return [AssistantThreadSummary(**t) for t in threads]


@app.get("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/threads/{thread_id}")
def get_thread_history_endpoint(
    repo_id: str,
    commit_sha: str,
    thread_id: str,
    request: Request,
):
    """Retrieves conversation message history for a specific thread."""
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    try:
        messages = get_thread_history(thread_id, user["user_id"])
        return {"thread_id": thread_id, "messages": messages}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


@app.post("/api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/threads/{thread_id}/cancel")
def cancel_thread_endpoint(
    repo_id: str,
    commit_sha: str,
    thread_id: str,
    request: Request,
):
    """Cancels an active assistant thread (thread owner or admin only)."""
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    if user.get("role") != "admin":
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM assistant_threads WHERE thread_id = ?", (thread_id,))
            thread_row = cursor.fetchone()
            if not thread_row:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
            if thread_row["user_id"] != user["user_id"]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot cancel another user's assistant thread")

    success = mark_thread_cancelled(thread_id, user["user_id"] if user.get("role") != "admin" else None)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found or already completed")
    return {"status": "CANCELLED", "thread_id": thread_id}


# ---------------------------------------------------------
# Phase 6: Change Impact Analysis Endpoints
# ---------------------------------------------------------

@app.post(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/impact/analyze",
    response_model=ChangeImpactResponse,
)
async def analyze_change_impact_endpoint(
    repo_id: str,
    commit_sha: str,
    req: ChangeImpactRequest,
    request: Request,
):
    """
    Executes change impact analysis for a target entity using CGG-approved templates.
    Dynamically identifies direct callers, transitive callers, and unresolved calls
    without modifying the persistent Neo4j knowledge graph.
    """
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await run_change_impact_analysis(
        repo_id=repo_id,
        commit_sha=commit_sha,
        request=req,
    )


# ---------------------------------------------------------
# Phase 6: Technical Report Generation Endpoints
# ---------------------------------------------------------

@app.post(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports",
    response_model=ReportDetail,
    status_code=status.HTTP_201_CREATED,
)
async def create_report_endpoint(
    repo_id: str,
    commit_sha: str,
    req: GenerateReportRequest,
    request: Request,
):
    """
    Generates an evidence-grounded technical report (architecture, impact, migration, onboarding, vulnerability)
    and persists it in SQLite.
    """
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return await generate_technical_report(
        repo_id=repo_id,
        commit_sha=commit_sha,
        request=req,
        created_by=user.get("user_id", user.get("sub", "system")),
    )


@app.get(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports",
    response_model=List[ReportSummary],
)
def list_reports_endpoint(
    repo_id: str,
    commit_sha: str,
    request: Request,
    report_type: Optional[str] = None,
):
    """Lists generated technical reports for a specific repository snapshot."""
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    return list_reports(repo_id=repo_id, commit_sha=commit_sha, report_type=report_type)


@app.get(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports/{report_id}",
    response_model=ReportDetail,
)
def get_report_endpoint(
    repo_id: str,
    commit_sha: str,
    report_id: str,
    request: Request,
):
    """Retrieves a specific technical report by ID with snapshot isolation checks."""
    user = get_authenticated_user(request)
    verify_repo_access(user, repo_id)
    report = get_report_by_id(report_id)
    if not report or report.repo_id != repo_id or report.commit_sha != commit_sha:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found for this snapshot")
    return report


@app.delete(
    "/api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports/{report_id}",
    response_model=MessageResponse,
)
def delete_report_endpoint(
    repo_id: str,
    commit_sha: str,
    report_id: str,
    request: Request,
):
    """Deletes a generated technical report (Admin only)."""
    user = get_authenticated_user(request)
    require_admin(user)
    verify_repo_access(user, repo_id)
    existing = get_report_by_id(report_id)
    if not existing or existing.repo_id != repo_id or existing.commit_sha != commit_sha:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    deleted = delete_report_by_id(report_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return MessageResponse(message="Report deleted successfully")


# ---------------------------------------------------------
# Phase 6: Evaluation & Benchmarking Endpoints
# ---------------------------------------------------------

@app.post(
    "/api/v1/evaluation/run",
    response_model=BenchmarkRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def run_evaluation_benchmark_endpoint(
    req: ExecuteBenchmarkRequest,
    request: Request,
):
    """
    Executes the comprehensive 12-case benchmark evaluation suite (Admin only).
    """
    user = get_authenticated_user(request)
    require_admin(user)
    verify_repo_access(user, req.repo_id)
    return await execute_benchmark_suite(
        request=req,
        created_by=user.get("user_id", user.get("sub", "system")),
    )


@app.get(
    "/api/v1/evaluation/runs",
    response_model=List[BenchmarkRunSummary],
)
def list_benchmark_runs_endpoint(
    request: Request,
    repo_id: Optional[str] = None,
):
    """Lists historical benchmark runs with summary metrics."""
    user = get_authenticated_user(request)
    if repo_id:
        verify_repo_access(user, repo_id)
    return list_benchmark_runs(repo_id=repo_id)


@app.get(
    "/api/v1/evaluation/runs/{run_id}",
    response_model=BenchmarkRunResponse,
)
def get_benchmark_run_endpoint(
    run_id: str,
    request: Request,
):
    """Retrieves full benchmark run details including per-query scores and failure diagnoses."""
    user = get_authenticated_user(request)
    run = get_benchmark_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Benchmark run not found")
    verify_repo_access(user, run.repo_id)
    return run


# ============================================================================
# Phase 7.3: Admin-Only User Management Endpoints
# ============================================================================

@app.get("/api/v1/users", response_model=List[UserResponse])
def list_users_endpoint(request: Request):
    """Lists all user accounts in the system (Admin only). Password hashes are never exposed."""
    user = get_authenticated_user(request)
    require_admin(user)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role, is_active, created_at FROM users ORDER BY created_at ASC")
        rows = cursor.fetchall()
        return [
            UserResponse(
                user_id=row["user_id"],
                username=row["username"],
                role=row["role"],
                is_active=bool(row["is_active"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]


@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(req: CreateUserRequest, request: Request):
    """Creates a new user account with designated role (Admin only)."""
    user = get_authenticated_user(request)
    require_admin(user)

    clean_username = req.username.strip()
    clean_role = req.role.strip().lower()
    if clean_role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role '{clean_role}'. Must be one of: {', '.join(sorted(VALID_ROLES))}",
        )

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    pwd_hash = hash_password(req.password)
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (clean_username,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{clean_username}' already exists",
            )

        cursor.execute(
            """
            INSERT INTO users (user_id, username, password_hash, role, is_active, created_at)
            VALUES (?, ?, ?, ?, 1, ?)
            """,
            (user_id, clean_username, pwd_hash, clean_role, now_str),
        )
        conn.commit()

    return UserResponse(
        user_id=user_id,
        username=clean_username,
        role=clean_role,
        is_active=True,
        created_at=now_str,
    )


@app.put("/api/v1/users/{target_user_id}/status", response_model=MessageResponse)
def update_user_status_endpoint(target_user_id: str, req: UpdateUserStatusRequest, request: Request):
    """Activates or deactivates a user account (Admin only). Revokes active sessions upon deactivation."""
    user = get_authenticated_user(request)
    require_admin(user)

    if target_user_id == user["user_id"] and not req.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own administrative account",
        )

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role FROM users WHERE user_id = ?", (target_user_id,))
        target_row = cursor.fetchone()
        if not target_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        cursor.execute("UPDATE users SET is_active = ? WHERE user_id = ?", (1 if req.is_active else 0, target_user_id))
        conn.commit()

    if not req.is_active:
        revoke_user_tokens(target_user_id)

    status_str = "activated" if req.is_active else "deactivated"
    return MessageResponse(message=f"User '{target_row['username']}' has been {status_str}")


@app.put("/api/v1/users/{target_user_id}/role", response_model=MessageResponse)
def update_user_role_endpoint(target_user_id: str, req: UpdateUserRoleRequest, request: Request):
    """Assigns a new role to an existing user (Admin only). Validates role strictly."""
    user = get_authenticated_user(request)
    require_admin(user)

    clean_role = req.role.strip().lower()
    if clean_role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role '{clean_role}'. Must be one of: {', '.join(sorted(VALID_ROLES))}",
        )

    if target_user_id == user["user_id"] and clean_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot demote your own administrative account",
        )

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users WHERE user_id = ?", (target_user_id,))
        target_row = cursor.fetchone()
        if not target_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        cursor.execute("UPDATE users SET role = ? WHERE user_id = ?", (clean_role, target_user_id))
        conn.commit()

    return MessageResponse(message=f"Role for user '{target_row['username']}' updated to '{clean_role}'")


@app.post("/api/v1/users/{target_user_id}/password", response_model=MessageResponse)
def reset_user_password_endpoint(target_user_id: str, req: ResetPasswordRequest, request: Request):
    """Admin-managed password reset for a target user (Admin only). Invalides active sessions."""
    user = get_authenticated_user(request)
    require_admin(user)

    new_hash = hash_password(req.new_password)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users WHERE user_id = ?", (target_user_id,))
        target_row = cursor.fetchone()
        if not target_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        cursor.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_hash, target_user_id))
        conn.commit()

    # Invalidate existing refresh tokens to force re-login with new password
    revoke_user_tokens(target_user_id)
    return MessageResponse(message=f"Password for user '{target_row['username']}' has been reset. All active sessions invalidated.")


# ============================================================================
# Phase 7.3: Admin-Only Repository Membership Management Endpoints
# ============================================================================

@app.get("/api/v1/repos/{repo_id}/members", response_model=List[RepoMemberResponse])
def list_repo_members_endpoint(repo_id: str, request: Request):
    """Lists all user memberships for a given repository (Admin only)."""
    user = get_authenticated_user(request)
    require_admin(user)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (repo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

        cursor.execute(
            """
            SELECT m.id, m.user_id, u.username, m.role, m.created_at
            FROM repo_memberships m
            JOIN users u ON m.user_id = u.user_id
            WHERE m.repo_id = ?
            ORDER BY m.created_at ASC
            """,
            (repo_id,),
        )
        rows = cursor.fetchall()
        return [
            RepoMemberResponse(
                id=row["id"] or f"mem_{row['user_id']}",
                user_id=row["user_id"],
                username=row["username"],
                role=row["role"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


@app.post("/api/v1/repos/{repo_id}/members", response_model=MessageResponse)
def add_repo_member_endpoint(repo_id: str, req: AddRepoMemberRequest, request: Request):
    """Assigns or updates repository membership for a user (Admin only)."""
    user = get_authenticated_user(request)
    require_admin(user)

    clean_role = req.role.strip().lower()
    if clean_role not in ("reviewer", "viewer", "owner"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Membership role must be 'reviewer' or 'viewer'",
        )

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (repo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

        cursor.execute("SELECT user_id, username FROM users WHERE user_id = ?", (req.user_id,))
        target_user = cursor.fetchone()
        if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found")

        mem_id = f"mem_{uuid.uuid4().hex[:12]}"
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        cursor.execute(
            """
            INSERT INTO repo_memberships (id, user_id, repo_id, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, repo_id) DO UPDATE SET role = excluded.role
            """,
            (mem_id, req.user_id, repo_id, clean_role, now_str),
        )
        conn.commit()

    return MessageResponse(message=f"User '{target_user['username']}' assigned role '{clean_role}' for repository {repo_id}")


@app.delete("/api/v1/repos/{repo_id}/members/{target_user_id}", response_model=MessageResponse)
def remove_repo_member_endpoint(repo_id: str, target_user_id: str, request: Request):
    """Revokes repository membership for a user (Admin only)."""
    user = get_authenticated_user(request)
    require_admin(user)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (repo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

        cursor.execute("DELETE FROM repo_memberships WHERE repo_id = ? AND user_id = ?", (repo_id, target_user_id))
        conn.commit()

    return MessageResponse(message=f"Membership revoked for user {target_user_id} on repository {repo_id}")





