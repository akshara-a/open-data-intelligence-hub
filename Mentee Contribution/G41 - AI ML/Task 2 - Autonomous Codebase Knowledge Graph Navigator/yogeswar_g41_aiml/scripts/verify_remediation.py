import urllib.request
import urllib.error
import ssl
import json
import subprocess

print("--- 1. Loopback HTTP Probe (127.0.0.1:80) ---")
try:
    req = urllib.request.Request("http://127.0.0.1:80/")
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8')
        print(f"Status: {resp.status}")
        if "/assets/index-AUPvDliH.js" in html:
            print("Latest bundle index-AUPvDliH.js successfully served on 127.0.0.1:80")
        else:
            print("Bundle check failed or mismatched!")
except Exception as e:
    print(f"Loopback probe error: {e}")

print("\n--- 2. Backend Health via Ingress ---")
try:
    req = urllib.request.Request("http://127.0.0.1:80/api/v1/health")
    with urllib.request.urlopen(req, timeout=5) as resp:
        print(f"Status: {resp.status}, Body: {resp.read().decode('utf-8')}")
except Exception as e:
    print(f"Health probe error: {e}")

print("\n--- 3. Tailscale Funnel Status ---")
try:
    ts_out = subprocess.check_output(["tailscale", "funnel", "status"]).decode('utf-8')
    print(ts_out.strip())
except Exception as e:
    print(f"Tailscale error: {e}")

print("\n--- 4. Public HTTPS Funnel Probe ---")
ctx = ssl.create_default_context()
try:
    req = urllib.request.Request("https://desktop-jd1g89s.tail6038c7.ts.net/")
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        print(f"Public HTTPS Status: {resp.status}")
        if "/assets/index-AUPvDliH.js" in html:
            print("Public HTTPS serves latest bundle!")
except Exception as e:
    print(f"Public HTTPS probe error: {e}")

print("\n--- 5. Authenticated Login Test via Ingress ---")
try:
    # Read admin password from secrets
    with open("secrets/admin.password", "r", encoding="utf-8") as f:
        pw = f.read().strip()
    login_data = json.dumps({"username": "admin", "password": pw}).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:80/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        login_res = json.loads(resp.read().decode('utf-8'))
        token = login_res.get("access_token")
        print(f"Login success! Access token acquired: {bool(token)}")

        # Test authenticated endpoint
        repos_req = urllib.request.Request(
            "http://127.0.0.1:80/api/v1/repos",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(repos_req, timeout=5) as rresp:
            repos = json.loads(rresp.read().decode('utf-8'))
            print(f"Authenticated /repos access success! Monitored repos count: {len(repos)}")
except Exception as e:
    print(f"Login / auth error: {e}")
