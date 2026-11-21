import os
import json
import pytest
from starlette.requests import Request
from backend.app.main import is_cookie_secure, allowed_origins


def make_test_request(headers_dict, scheme="http", path="/api/v1/auth/login"):
    raw_headers = [(k.lower().encode(), v.encode()) for k, v in headers_dict.items()]
    scope = {
        "type": "http",
        "method": "POST",
        "scheme": scheme,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "server": ("127.0.0.1", 80),
        "headers": raw_headers,
    }
    return Request(scope)


def test_is_cookie_secure_direct_http():
    """Test 1: Direct HTTP request with no forwarded header yields secure=False."""
    req = make_test_request({"Host": "127.0.0.1", "Content-Type": "application/json"})
    assert is_cookie_secure(req) is False


def test_is_cookie_secure_forged_forwarded_proto_on_localhost():
    """Test 2: Direct HTTP request with forged X-Forwarded-Proto on localhost is rejected."""
    req = make_test_request({
        "Host": "localhost",
        "X-Forwarded-Proto": "https",
        "Content-Type": "application/json",
    })
    # Host is 'localhost', so dynamic detection MUST NOT trust X-Forwarded-Proto
    assert is_cookie_secure(req) is False


def test_is_cookie_secure_trusted_tailscale_proxy():
    """Test 3: Legitimate HTTPS request through trusted Tailscale proxy (*.ts.net) yields secure=True."""
    req = make_test_request({
        "Host": "my-node.tailnet123.ts.net",
        "X-Forwarded-Proto": "https",
        "Content-Type": "application/json",
    })
    assert is_cookie_secure(req) is True


def test_is_cookie_secure_production_env_override(monkeypatch):
    """Test 4a: Explicit COOKIE_SECURE=true forces secure=True unconditionally."""
    monkeypatch.setenv("COOKIE_SECURE", "true")
    req = make_test_request({"Host": "127.0.0.1"})
    assert is_cookie_secure(req) is True


def test_is_cookie_secure_local_dev_override(monkeypatch):
    """Test 4b: Explicit COOKIE_SECURE=false forces secure=False unconditionally."""
    monkeypatch.setenv("COOKIE_SECURE", "false")
    req = make_test_request({
        "Host": "my-node.tailnet123.ts.net",
        "X-Forwarded-Proto": "https",
    })
    assert is_cookie_secure(req) is False


def test_cors_origin_allowlist_filtering():
    """Test 5: Explicit CORS whitelist permits localhost and rejects untrusted origins."""
    assert "http://localhost" in allowed_origins
    assert "http://127.0.0.1:80" in allowed_origins
    assert "http://localhost:5173" in allowed_origins
    assert "http://malicious-attacker.com" not in allowed_origins
    assert "*" not in allowed_origins
