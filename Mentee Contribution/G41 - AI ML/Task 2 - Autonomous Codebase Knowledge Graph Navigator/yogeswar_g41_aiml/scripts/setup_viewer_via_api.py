import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:80"

# 1. Login as admin
with open("secrets/admin.password", "r", encoding="utf-8") as f:
    admin_pw = f.read().strip()

login_body = json.dumps({"username": "admin", "password": admin_pw}).encode("utf-8")
req = urllib.request.Request(f"{BASE_URL}/api/v1/auth/login", data=login_body, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    admin_token = json.loads(resp.read().decode("utf-8"))["access_token"]
print("Admin logged in successfully.")

# 2. List users via Admin API
users_req = urllib.request.Request(f"{BASE_URL}/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
with urllib.request.urlopen(users_req) as resp:
    users = json.loads(resp.read().decode("utf-8"))
print("Current users from API:")
for u in users:
    print(" ", u)

demo_user = next((u for u in users if u["username"] == "demo"), None)
if demo_user:
    demo_id = demo_user["user_id"]
    # 3. Reset demo password to viewer_secure_123 via API
    reset_body = json.dumps({"new_password": "viewer_secure_123"}).encode("utf-8")
    reset_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/users/{demo_id}/password",
        data=reset_body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {admin_token}"}
    )
    with urllib.request.urlopen(reset_req) as resp:
        print("Demo password reset response:", resp.read().decode("utf-8"))

    # 4. Add demo to repo 12fac9bd-0ebb-4844-a239-e518e812b6bb
    repo_id = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
    mem_body = json.dumps({"user_id": demo_id, "role": "viewer"}).encode("utf-8")
    mem_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/repos/{repo_id}/members",
        data=mem_body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {admin_token}"}
    )
    try:
        with urllib.request.urlopen(mem_req) as resp:
            print("Membership added response:", resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("Membership add response:", e.code, e.read().decode("utf-8"))
