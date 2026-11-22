import os
import sqlite3
import hashlib
from pathlib import Path
from contextlib import contextmanager

DEFAULT_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/app_state.db")


def get_db_path() -> Path:
    raw_path = os.getenv("SQLITE_DB_PATH", DEFAULT_DB_PATH)
    path = Path(raw_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def hash_password(password: str, salt: str = "salt_cgg_nav") -> str:
    return hashlib.sha256(f"{password}:{salt}".encode("utf-8")).hexdigest()


@contextmanager
def get_db_connection(timeout: float = 5.0):
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path), timeout=timeout, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        # Apply strict concurrency pragmas per Section 15.1
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
    finally:
        conn.close()


def init_db():
    db_path = get_db_path()
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'viewer',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Schema migration for existing users table
        cursor.execute("PRAGMA table_info(users);")
        existing_user_cols = {row["name"] for row in cursor.fetchall()}
        if "is_active" not in existing_user_cols:
            cursor.execute("ALTER TABLE users ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1;")

        # Normalize any legacy or test roles to canonical set ('admin', 'reviewer', 'viewer')
        cursor.execute("""
        UPDATE users
        SET role = 'viewer'
        WHERE role NOT IN ('admin', 'reviewer', 'viewer');
        """)

        # Refresh tokens table with family tracking for reuse detection (AC-1.3)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS refresh_tokens (
            token_id TEXT PRIMARY KEY,
            family_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            token_hash TEXT NOT NULL UNIQUE,
            is_revoked INTEGER NOT NULL DEFAULT 0,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_refresh_tokens_family ON refresh_tokens(family_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_refresh_tokens_hash ON refresh_tokens(token_hash);")

        # Repositories table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            repo_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            git_url TEXT NOT NULL,
            default_branch TEXT DEFAULT 'main',
            status TEXT DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Authoritative Tenant Access (Section 4.2 / 14.2)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS repo_memberships (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            repo_id TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, repo_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(repo_id) REFERENCES repositories(repo_id) ON DELETE CASCADE
        );
        """)

        # Ingestion & worker jobs table (Section 15.1)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            repo_id TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            job_type TEXT NOT NULL,
            status TEXT NOT NULL,
            worker_id TEXT,
            progress INTEGER DEFAULT 0,
            log_output TEXT,
            claimed_at TIMESTAMP,
            lease_expires_at TIMESTAMP,
            retry_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status_lease ON jobs(status, lease_expires_at);")

        # Evidence-Backed Technical Reports table (Section 13.2 / Phase 6.2)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id TEXT PRIMARY KEY,
            query_id TEXT NOT NULL,
            repo_id TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            report_type TEXT NOT NULL DEFAULT 'repository_architecture',
            title TEXT NOT NULL DEFAULT 'Technical Analysis Report',
            query_text TEXT NOT NULL,
            executive_summary TEXT NOT NULL DEFAULT '',
            verified_findings_json TEXT DEFAULT '[]',
            uncertain_findings_json TEXT DEFAULT '[]',
            recommendations_json TEXT DEFAULT '[]',
            risk_assessment_json TEXT DEFAULT '{}',
            evidence_json TEXT DEFAULT '[]',
            limitations TEXT DEFAULT '',
            markdown_body TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'COMPLETED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reports_query ON reports(query_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reports_snapshot ON reports(repo_id, commit_sha);")

        # Migrate existing reports table if columns are missing
        cursor.execute("PRAGMA table_info(reports);")
        existing_report_cols = {row["name"] for row in cursor.fetchall()}
        cols_to_add = [
            ("report_type", "TEXT NOT NULL DEFAULT 'repository_architecture'"),
            ("title", "TEXT NOT NULL DEFAULT 'Technical Analysis Report'"),
            ("executive_summary", "TEXT NOT NULL DEFAULT ''"),
            ("verified_findings_json", "TEXT DEFAULT '[]'"),
            ("uncertain_findings_json", "TEXT DEFAULT '[]'"),
            ("recommendations_json", "TEXT DEFAULT '[]'"),
            ("risk_assessment_json", "TEXT DEFAULT '{}'"),
            ("evidence_json", "TEXT DEFAULT '[]'"),
            ("limitations", "TEXT DEFAULT ''"),
            ("status", "TEXT NOT NULL DEFAULT 'COMPLETED'"),
        ]
        for col_name, col_def in cols_to_add:
            if col_name not in existing_report_cols:
                cursor.execute(f"ALTER TABLE reports ADD COLUMN {col_name} {col_def};")

        # Evaluation & Benchmark Runs table (Phase 6.3)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS benchmark_runs (
            run_id TEXT PRIMARY KEY,
            repo_id TEXT DEFAULT '12fac9bd-0ebb-4844-a239-e518e812b6bb',
            dataset_version TEXT NOT NULL,
            provider_name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'COMPLETED',
            sample_count INTEGER NOT NULL DEFAULT 0,
            metrics_json TEXT NOT NULL DEFAULT '{}',
            failure_analysis_json TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_benchmark_runs_date ON benchmark_runs(created_at);")

        # Migrate benchmark_runs table columns if missing
        cursor.execute("PRAGMA table_info(benchmark_runs);")
        bm_cols = {row["name"] for row in cursor.fetchall()}
        if "repo_id" not in bm_cols:
            cursor.execute("ALTER TABLE benchmark_runs ADD COLUMN repo_id TEXT DEFAULT '12fac9bd-0ebb-4844-a239-e518e812b6bb';")

        # Benchmark query level granular predictions & metrics table (Phase 6.3)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS benchmark_query_results (
            result_id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            test_id TEXT NOT NULL,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            passed INTEGER NOT NULL DEFAULT 1,
            metrics_json TEXT NOT NULL DEFAULT '{}',
            ground_truth_json TEXT NOT NULL DEFAULT '{}',
            actual_result_json TEXT NOT NULL DEFAULT '{}',
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(run_id) REFERENCES benchmark_runs(run_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_benchmark_query_run ON benchmark_query_results(run_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_benchmark_query_cat ON benchmark_query_results(category);")

        # Vector embeddings table (Section 9.1 / 15.1)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            repo_id TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            file_path TEXT NOT NULL,
            vector BLOB NOT NULL,
            model_version TEXT NOT NULL,
            preprocess_version TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (repo_id, commit_sha, file_path)
        );
        """)

        # Assistant conversation threads table (Phase 5 / Section 15.1)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assistant_threads (
            thread_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            repo_id TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assistant_threads_user ON assistant_threads(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assistant_threads_snapshot ON assistant_threads(repo_id, commit_sha);")

        # Assistant conversation messages table (Phase 5)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assistant_messages (
            message_id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            findings_json TEXT,
            evidence_json TEXT,
            tool_trace_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(thread_id) REFERENCES assistant_threads(thread_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assistant_messages_thread ON assistant_messages(thread_id);")

        # Seed or safely update administrative user credential
        admin_pwd = get_admin_password()
        admin_hash = hash_password(admin_pwd)
        cursor.execute("SELECT user_id, password_hash FROM users WHERE username = 'admin'")
        existing_admin = cursor.fetchone()
        if not existing_admin:
            default_uid = "usr_admin_default"
            cursor.execute(
                "INSERT INTO users (user_id, username, password_hash, role) VALUES (?, ?, ?, ?)",
                (default_uid, "admin", admin_hash, "admin")
            )
            # Seed a default demo repository
            demo_repo_id = "repo_demo_sample"
            cursor.execute(
                "INSERT OR IGNORE INTO repositories (repo_id, name, git_url) VALUES (?, ?, ?)",
                (demo_repo_id, "knowledge-graph-sample", "https://github.com/example/sample-repo.git")
            )
            cursor.execute(
                "INSERT OR IGNORE INTO repo_memberships (id, user_id, repo_id, role) VALUES (?, ?, ?, ?)",
                ("mem_admin_sample", default_uid, demo_repo_id, "owner")
            )
        else:
            # Safely migrate/update existing admin if password hash differs (e.g. replacing hardcoded default)
            if existing_admin["password_hash"] != admin_hash:
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE username = 'admin'",
                    (admin_hash,)
                )

        conn.commit()


def get_admin_password() -> str:
    """
    Securely resolves the administrative password from:
    1. ADMIN_PASSWORD environment variable
    2. Container secret mount (/run/secrets/admin_password)
    3. Host secret file (secrets/admin.password)

    Raises RuntimeError if no configured secret exists.
    Silent runtime password generation is strictly prohibited.
    """
    if env_pwd := os.getenv("ADMIN_PASSWORD"):
        pwd = env_pwd.strip()
        if pwd:
            return pwd

    container_secret = Path("/run/secrets/admin_password")
    if container_secret.is_file():
        pwd = container_secret.read_text(encoding="utf-8").strip()
        if pwd:
            return pwd

    search_paths = [
        Path("./secrets/admin.password"),
        Path("../secrets/admin.password"),
        Path(__file__).resolve().parent.parent.parent / "secrets" / "admin.password",
    ]
    for p in search_paths:
        if p.is_file():
            pwd = p.read_text(encoding="utf-8").strip()
            if pwd:
                return pwd

    raise RuntimeError(
        "Administrative password secret is not configured. "
        "A valid secret must be provided via the ADMIN_PASSWORD environment variable, "
        "the Docker secret mount (/run/secrets/admin_password), or the host secret file (secrets/admin.password). "
        "Runtime generation of administrator credentials is disallowed."
    )


def check_wal_mode() -> str:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        row = cursor.fetchone()
        return row[0].upper() if row else "UNKNOWN"
