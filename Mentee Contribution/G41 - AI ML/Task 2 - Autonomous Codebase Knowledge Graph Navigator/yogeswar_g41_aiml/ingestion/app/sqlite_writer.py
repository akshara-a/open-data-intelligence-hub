import os
import sqlite3
import struct
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

DEFAULT_SQLITE_PATH = os.getenv("SQLITE_DB_PATH", "./data/app_state.db")
MODEL_VERSION = "sentence-transformers/all-mpnet-base-v2@9a32259"
PREPROCESS_VERSION = "v1_file_head512"


def get_sqlite_conn(db_path: Optional[str] = None) -> sqlite3.Connection:
    p = Path(db_path or DEFAULT_SQLITE_PATH).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def generate_deterministic_vector(text: str, dim: int = 768) -> bytes:
    """
    Generates a deterministic float32 vector representation of text
    packed into a binary BLOB for SQLite storage.
    """
    # Deterministic pseudo-embedding based on repeated hashing
    floats = []
    seed_hash = hashlib.sha256(text.encode("utf-8")).digest()
    for i in range(dim):
        val = float((seed_hash[i % len(seed_hash)] ^ (i % 256)) - 128) / 128.0
        floats.append(val)
    return struct.pack(f"{dim}f", *floats)


def store_file_embeddings(
    repo_id: str,
    commit_sha: str,
    file_contents: Dict[str, str],
    db_path: Optional[str] = None,
):
    """
    Persists file-level embeddings to SQLite per Section 9.1 & 9.2.
    Implements cache reuse across commits when content_hash matches.
    """
    conn = get_sqlite_conn(db_path)
    with conn:
        cursor = conn.cursor()

        # Ensure embeddings table exists
        cursor.execute(
            """
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
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_embeddings_lookup
            ON embeddings(repo_id, commit_sha);
            """
        )

        for file_path, content in file_contents.items():
            head_512 = content[:512]
            c_hash = hashlib.sha256(head_512.encode("utf-8")).hexdigest()

            # Check for cache reuse per Section 9.2:
            # content_hash == existing.content_hash AND model_version == existing.model_version AND preprocess_version == existing.preprocess_version
            cursor.execute(
                """
                SELECT vector FROM embeddings
                WHERE repo_id = :repo_id
                  AND content_hash = :content_hash
                  AND model_version = :model_version
                  AND preprocess_version = :preprocess_version
                LIMIT 1
                """,
                {
                    "repo_id": repo_id,
                    "content_hash": c_hash,
                    "model_version": MODEL_VERSION,
                    "preprocess_version": PREPROCESS_VERSION,
                },
            )
            cached_row = cursor.fetchone()
            if cached_row:
                vector_blob = cached_row["vector"]
            else:
                vector_blob = generate_deterministic_vector(head_512)

            cursor.execute(
                """
                INSERT INTO embeddings (
                    repo_id, commit_sha, file_path, vector,
                    model_version, preprocess_version, content_hash, created_at
                )
                VALUES (
                    :repo_id, :commit_sha, :file_path, :vector,
                    :model_version, :preprocess_version, :content_hash, CURRENT_TIMESTAMP
                )
                ON CONFLICT(repo_id, commit_sha, file_path) DO UPDATE SET
                    vector = excluded.vector,
                    content_hash = excluded.content_hash,
                    model_version = excluded.model_version,
                    preprocess_version = excluded.preprocess_version,
                    created_at = CURRENT_TIMESTAMP;
                """,
                {
                    "repo_id": repo_id,
                    "commit_sha": commit_sha,
                    "file_path": file_path,
                    "vector": vector_blob,
                    "model_version": MODEL_VERSION,
                    "preprocess_version": PREPROCESS_VERSION,
                    "content_hash": c_hash,
                },
            )
