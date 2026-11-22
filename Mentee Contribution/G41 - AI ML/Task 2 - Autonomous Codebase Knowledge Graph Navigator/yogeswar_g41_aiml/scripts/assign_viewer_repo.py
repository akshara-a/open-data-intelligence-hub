import sqlite3
import uuid
import datetime

conn = sqlite3.connect('data/app_state.db')
cursor = conn.cursor()

# Find repo_member and rbac_viewer user_ids
users_to_assign = cursor.execute("SELECT user_id, username FROM users WHERE username IN ('repo_member', 'rbac_viewer')").fetchall()
print("Found users to assign:", users_to_assign)

repo_target = '12fac9bd-0ebb-4844-a239-e518e812b6bb'
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

for u_id, u_name in users_to_assign:
    existing = cursor.execute("SELECT id FROM repo_memberships WHERE user_id = ? AND repo_id = ?", (u_id, repo_target)).fetchone()
    if not existing:
        mem_id = f"mem_viewer_{uuid.uuid4().hex[:8]}"
        cursor.execute(
            "INSERT INTO repo_memberships (id, user_id, repo_id, role, created_at) VALUES (?, ?, ?, 'viewer', ?)",
            (mem_id, u_id, repo_target, now)
        )
        print(f"Assigned {u_name} ({u_id}) as viewer to {repo_target}")
    else:
        print(f"{u_name} already assigned to {repo_target}")

conn.commit()
conn.close()
