import os
import secrets
import string
import subprocess
from pathlib import Path


def rotate_neo4j_password():
    admin_pwd_file = Path("secrets/neo4j_admin.password")
    if not admin_pwd_file.exists():
        raise RuntimeError("secrets/neo4j_admin.password does not exist")

    old_pwd = admin_pwd_file.read_text(encoding="utf-8").strip()

    # Generate cryptographically secure 32-character password
    # Exclude characters that could cause shell or cypher syntax issues (', ", \, `)
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_+="
    new_pwd = "".join(secrets.choice(alphabet) for _ in range(32))

    # Cypher statement
    cypher_stmt = f"ALTER CURRENT USER SET PASSWORD FROM '{old_pwd}' TO '{new_pwd}';"

    cmd = [
        "docker", "exec", "autonomous_codebase_knowledge_graph_navigator-neo4j-1",
        "cypher-shell", "-u", "neo4j", "-p", old_pwd,
        cypher_stmt
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to rotate password via cypher-shell: {res.stderr.strip()}")

    print("Successfully rotated password in active Neo4j database instance.")

    # Update secret files with POSIX LF
    for fname in ["neo4j_admin.password", "neo4j_read.password", "neo4j_write.password"]:
        target_path = Path("secrets") / fname
        target_path.write_bytes(f"{new_pwd}\n".encode("utf-8"))
        print(f"Updated secret file: {target_path}")

    return new_pwd


if __name__ == "__main__":
    rotate_neo4j_password()
