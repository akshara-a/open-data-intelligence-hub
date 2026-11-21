import os
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from .models import CodeChunk
from .embedding_engine import get_embedding_engine, EmbeddingEngine

DEFAULT_SQLITE_PATH = os.getenv("SQLITE_DB_PATH", "./data/app_state.db")


class SQLiteChunkStorage:
    def __init__(self, db_path: Optional[str] = None):
        raw_path = db_path or os.getenv("SQLITE_DB_PATH", DEFAULT_SQLITE_PATH)
        self.db_path = Path(raw_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # File-level embeddings table (Section 9.1)
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
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_lookup ON embeddings(repo_id, commit_sha);")

            # Fine-grained source code chunks embeddings table (Section 2 & 3)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunk_embeddings (
                chunk_id TEXT PRIMARY KEY,
                repo_id TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                entity_id TEXT,
                file_path TEXT NOT NULL,
                line_start INTEGER NOT NULL,
                line_end INTEGER NOT NULL,
                content TEXT NOT NULL,
                vector BLOB NOT NULL,
                model_version TEXT NOT NULL,
                preprocess_version TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_snapshot ON chunk_embeddings(repo_id, commit_sha);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_file ON chunk_embeddings(repo_id, commit_sha, file_path);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_cache ON chunk_embeddings(repo_id, content_hash, model_version);")
            conn.commit()

    def persist_chunks(
        self,
        chunks: List[CodeChunk],
        force_reindex: bool = False,
    ) -> Tuple[int, int]:
        """
        Persists chunks into SQLite with cross-commit cache reuse.
        Returns (reused_cache_count, newly_embedded_count).
        """
        if not chunks:
            return 0, 0

        engine = get_embedding_engine()
        reused_count = 0
        new_count = 0

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Identify current files in the snapshot to prevent stale chunks from deleted files
            repo_id = chunks[0].repo_id
            commit_sha = chunks[0].commit_sha
            current_chunk_ids = [c.chunk_id for c in chunks]

            for chunk in chunks:
                vector_blob: Optional[bytes] = None

                if not force_reindex:
                    # Cache lookup across commits per Section 9.2:
                    # content_hash == existing.content_hash AND model_version == existing.model_version
                    cursor.execute(
                        """
                        SELECT vector FROM chunk_embeddings
                        WHERE repo_id = ?
                          AND content_hash = ?
                          AND model_version = ?
                        LIMIT 1
                        """,
                        (chunk.repo_id, chunk.content_hash, engine.model_version),
                    )
                    cached_row = cursor.fetchone()
                    if cached_row:
                        vector_blob = cached_row["vector"]
                        reused_count += 1

                if vector_blob is None:
                    # Compute fresh embedding
                    vec = engine.embed_text(chunk.indexed_text)
                    vector_blob = engine.vector_to_blob(vec)
                    new_count += 1

                # Upsert chunk record
                cursor.execute(
                    """
                    INSERT INTO chunk_embeddings (
                        chunk_id, repo_id, commit_sha, entity_id, file_path,
                        line_start, line_end, content, vector, model_version,
                        preprocess_version, content_hash, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(chunk_id) DO UPDATE SET
                        content = excluded.content,
                        vector = excluded.vector,
                        content_hash = excluded.content_hash,
                        model_version = excluded.model_version,
                        preprocess_version = excluded.preprocess_version,
                        created_at = CURRENT_TIMESTAMP;
                    """,
                    (
                        chunk.chunk_id,
                        chunk.repo_id,
                        chunk.commit_sha,
                        chunk.entity_id,
                        chunk.file_path,
                        chunk.line_start,
                        chunk.line_end,
                        chunk.content,
                        vector_blob,
                        engine.model_version,
                        engine.preprocess_version,
                        chunk.content_hash,
                    ),
                )

            # Purge stale chunks belonging to deleted files in this snapshot
            active_files = list({c.file_path for c in chunks})
            if active_files:
                placeholders = ",".join("?" for _ in active_files)
                cursor.execute(
                    f"""
                    DELETE FROM chunk_embeddings
                    WHERE repo_id = ?
                      AND commit_sha = ?
                      AND file_path NOT IN ({placeholders})
                    """,
                    [repo_id, commit_sha] + active_files,
                )

            conn.commit()

        return reused_count, new_count

    def scan_semantic_candidates(
        self,
        repo_id: str,
        commit_sha: str,
        query_vector: np.ndarray,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Executes a reliable linear scan over unit-normalized chunk vectors
        scoped exclusively to (repo_id, commit_sha) per Section 9.2.
        """
        engine = get_embedding_engine()
        candidates: List[Dict[str, Any]] = []

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT chunk_id, repo_id, commit_sha, entity_id, file_path,
                       line_start, line_end, content, vector, content_hash
                FROM chunk_embeddings
                WHERE repo_id = ? AND commit_sha = ?
                """,
                (repo_id, commit_sha),
            )
            rows = cursor.fetchall()

            for row in rows:
                chunk_vec = engine.blob_to_vector(row["vector"])
                sim = engine.compute_cosine_similarity(query_vector, chunk_vec)
                candidates.append({
                    "chunk_id": row["chunk_id"],
                    "repo_id": row["repo_id"],
                    "commit_sha": row["commit_sha"],
                    "entity_id": row["entity_id"],
                    "file_path": row["file_path"],
                    "line_start": row["line_start"],
                    "line_end": row["line_end"],
                    "content": row["content"],
                    "content_hash": row["content_hash"],
                    "semantic_similarity": sim,
                })

        # Deterministic sorting: similarity DESC, then file_path ASC, line_start ASC
        candidates.sort(key=lambda x: (-x["semantic_similarity"], x["file_path"], x["line_start"]))
        return candidates[:top_k]
