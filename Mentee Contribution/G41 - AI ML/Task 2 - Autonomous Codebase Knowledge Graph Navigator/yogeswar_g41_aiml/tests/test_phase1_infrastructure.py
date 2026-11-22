import os
import sys
import yaml
import sqlite3
import pytest
from pathlib import Path
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Response, HTTPException

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

TEST_DB_PATH = ROOT_DIR / "data" / "test_app_state.db"
os.environ["SQLITE_DB_PATH"] = str(TEST_DB_PATH)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass
    from backend.app.database import init_db
    init_db()
    yield


def test_secret_files_integrity():
    """Validates Section 19.2 & 19.3 Secrets Provisioning"""
    secrets_dir = ROOT_DIR / "secrets"
    assert secrets_dir.is_dir(), "secrets directory must exist"

    # 1. JWT RS256 Keys
    jwt_priv = secrets_dir / "jwt_private_key.pem"
    jwt_pub = secrets_dir / "jwt_public_key.pem"
    assert jwt_priv.is_file(), "jwt_private_key.pem missing"
    assert jwt_pub.is_file(), "jwt_public_key.pem missing"

    priv_key = serialization.load_pem_private_key(jwt_priv.read_bytes(), password=None)
    assert isinstance(priv_key, rsa.RSAPrivateKey)
    assert priv_key.key_size >= 2048

    pub_key = serialization.load_pem_public_key(jwt_pub.read_bytes())
    assert isinstance(pub_key, rsa.RSAPublicKey)

    # 2. Internal Service Auth Keys
    svc_priv = secrets_dir / "internal_service_key.pem"
    svc_pub = secrets_dir / "internal_service_pubkey.pem"
    assert svc_priv.is_file(), "internal_service_key.pem missing"
    assert svc_pub.is_file(), "internal_service_pubkey.pem missing"

    # 3. Neo4j & Admin Passwords (min 12 chars per Section 19.2)
    neo_admin = secrets_dir / "neo4j_admin.password"
    neo_read = secrets_dir / "neo4j_read.password"
    neo_write = secrets_dir / "neo4j_write.password"
    admin_pwd_file = secrets_dir / "admin.password"

    for pwd_file in [neo_admin, neo_read, neo_write, admin_pwd_file]:
        assert pwd_file.is_file(), f"{pwd_file.name} missing"
        pwd = pwd_file.read_text(encoding="utf-8").strip()
        assert len(pwd) >= 12, f"Password {pwd_file.name} must be >= 12 characters"


def test_nginx_and_tls_config():
    """Validates Section 19.2 Nginx reverse proxy configuration"""
    nginx_conf = ROOT_DIR / "nginx" / "nginx.conf"
    assert nginx_conf.is_file(), "nginx.conf missing"
    content = nginx_conf.read_text(encoding="utf-8")

    assert "proxy_pass http://backend:8000" in content
    assert "proxy_pass http://frontend:80" in content
    assert "listen 443 ssl" in content

    # Check TLS certs
    tls_crt = ROOT_DIR / "nginx" / "certs" / "tls.crt"
    tls_key = ROOT_DIR / "nginx" / "certs" / "tls.key"
    assert tls_crt.is_file(), "tls.crt missing"
    assert tls_key.is_file(), "tls.key missing"


def test_sqlite_wal_pragmas_and_schemas():
    """Validates Section 15.1 Shared Persistent SQLite Architecture"""
    from backend.app.database import get_db_connection, check_wal_mode

    assert check_wal_mode() == "WAL", "SQLite must operate in WAL mode"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA busy_timeout;")
        row = cursor.fetchone()
        assert row[0] == 5000, "busy_timeout must be 5000 ms"

        cursor.execute("PRAGMA synchronous;")
        row = cursor.fetchone()
        assert row[0] == 1, "synchronous pragma must be NORMAL (1)"

        # Check required tables existence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {r[0] for r in cursor.fetchall()}
        required_tables = {"users", "refresh_tokens", "repositories", "repo_memberships", "jobs", "reports", "embeddings"}
        assert required_tables.issubset(tables), f"Missing tables: {required_tables - tables}"


def test_auth_login_rs256_tokens():
    """Validates AC-1.1: User can authenticate via /api/v1/auth/login and receive valid RS256 JWT tokens."""
    from backend.app.main import login
    from backend.app.schemas import LoginRequest
    from backend.app.auth import load_public_key
    from backend.app.database import get_admin_password

    admin_pwd = get_admin_password()
    response = Response()
    request = LoginRequest(username="admin", password=admin_pwd)
    token_resp = login(request, response)

    assert token_resp.access_token is not None
    assert token_resp.token_type == "bearer"
    assert token_resp.expires_in == 900

    # Verify old hardcoded credential no longer works
    with pytest.raises(HTTPException) as exc_info:
        login(LoginRequest(username="admin", password="AdminPass123!"), Response())
    assert exc_info.value.status_code == 401
    assert "Invalid username or password" in exc_info.value.detail

    # Verify RS256 signature and claims
    pub_key_pem = load_public_key()
    payload = jwt.decode(
        token_resp.access_token,
        pub_key_pem,
        algorithms=["RS256"],
        audience="kg_navigator_clients",
        issuer="autonomous_kg_navigator",
    )
    assert payload["username"] == "admin"
    assert payload["role"] == "admin"

    # Verify HTTP-only refresh cookie is set
    cookie_headers = response.headers.getlist("set-cookie")
    assert any("refresh_token=" in c and "HttpOnly" in c for c in cookie_headers), "HTTP-only refresh_token cookie must be set"


def test_refresh_token_rotation_and_reuse_family_revocation():
    """Validates AC-1.3: Re-using an already rotated refresh token immediately invalidates the entire token family."""
    from backend.app.auth import mint_refresh_token, rotate_refresh_token

    # 1. Mint initial refresh token
    token_1, family_id = mint_refresh_token(user_id="usr_admin_default")
    assert token_1 and family_id

    # 2. Rotate token_1 -> returns (access_token, token_2, user_id)
    new_acc_1, token_2, uid_1 = rotate_refresh_token(token_1)
    assert token_2 != token_1
    assert uid_1 == "usr_admin_default"

    # 3. Rotate token_2 -> returns (access_token, token_3, user_id)
    new_acc_2, token_3, uid_2 = rotate_refresh_token(token_2)
    assert token_3 != token_2

    # 4. Attempt to REUSE token_1 (which was already rotated)
    # AC-1.3: "Re-using an already rotated refresh token immediately invalidates the entire token family."
    with pytest.raises(HTTPException) as exc_info:
        rotate_refresh_token(token_1)
    assert exc_info.value.status_code == 401
    assert "Entire token family has been invalidated" in exc_info.value.detail

    # 5. Verify that token_3 (which was previously valid) is NOW also invalid because the family was revoked!
    with pytest.raises(HTTPException) as exc_info_2:
        rotate_refresh_token(token_3)
    assert exc_info_2.value.status_code == 401
    assert "Entire token family has been invalidated" in exc_info_2.value.detail


def test_service_health_endpoints():
    """Validates health endpoints of backend, mcp, and rag services"""
    from backend.app.main import health_check as backend_health
    bh = backend_health()
    assert bh.status == "healthy"
    assert "wal" in bh.database

    from mcp.app.main import health_check as mcp_health
    mh = mcp_health()
    assert mh.status == "healthy"
    assert mh.neo4j_configured is True

    from rag.app.main import health_check as rag_health
    rh = rag_health()
    assert rh.status == "healthy"


def test_docker_compose_topology():
    """Validates Section 19.1 & 19.2 Docker Compose topology and network isolation"""
    compose_path = ROOT_DIR / "docker-compose.yml"
    assert compose_path.is_file()

    with open(compose_path, "r", encoding="utf-8") as f:
        compose = yaml.safe_load(f)

    # Networks
    networks = compose.get("networks", {})
    assert "ingress_net" in networks
    assert "app_net" in networks
    assert "mcp_net" in networks
    assert "db_net" in networks
    assert networks["mcp_net"].get("internal") is True
    assert networks["db_net"].get("internal") is True

    # Services
    services = compose.get("services", {})
    required_services = {"nginx", "frontend", "backend", "mcp", "ingestion", "rag", "neo4j"}
    assert required_services.issubset(set(services.keys()))

    # Verify Neo4j & MCP ports are NOT published to host
    assert "ports" not in services["neo4j"], "Neo4j must not publish host ports directly"
    assert "ports" not in services["mcp"], "MCP must not publish host ports directly"

    # Verify Nginx securely binds ports 80 and 443 to loopback
    nginx_ports = services["nginx"].get("ports", [])
    assert "127.0.0.1:443:443" in nginx_ports or "443:443" in nginx_ports
    assert "127.0.0.1:80:80" in nginx_ports or "80:80" in nginx_ports
    # Specifically enforce loopback binding for security
    assert any(p in nginx_ports for p in ["127.0.0.1:443:443", "443:443"])
    assert "127.0.0.1:443:443" in nginx_ports
    assert "127.0.0.1:80:80" in nginx_ports


def test_neo4j_service_configuration():
    """Validates Neo4j 5.18 Community service configuration and absence of invalid AUTH.FILE"""
    compose_path = ROOT_DIR / "docker-compose.yml"
    with open(compose_path, "r", encoding="utf-8") as f:
        compose = yaml.safe_load(f)

    neo4j_svc = compose["services"]["neo4j"]
    assert neo4j_svc["image"] == "neo4j:5.18-community"

    # Verify invalid AUTH.FILE is NOT introduced in environment
    env_vars = neo4j_svc.get("environment", [])
    env_keys = [e.split("=")[0] if "=" in e else e for e in env_vars]
    assert "NEO4J_AUTH_FILE" not in env_keys, "NEO4J_AUTH_FILE must not be present as it translates to invalid AUTH.FILE"

    # Verify entrypoint reads secret safely into NEO4J_AUTH
    entrypoint = neo4j_svc.get("entrypoint", [])
    assert len(entrypoint) >= 3
    assert "bash" in entrypoint[0]
    entrypoint_script = entrypoint[2]
    assert "NEO4J_AUTH" in entrypoint_script
    assert "/run/secrets/neo4j_admin_password" in entrypoint_script
    assert "/startup/docker-entrypoint.sh" in entrypoint_script

    # Verify secrets and volumes
    assert "neo4j_admin_password" in neo4j_svc.get("secrets", [])
    assert "neo4j_data:/data" in neo4j_svc.get("volumes", [])
    assert any("apoc" in e for e in env_vars), "APOC plugin must be configured"
