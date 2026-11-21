"""
Phase 5 - Assistant Thread and Message Checkpoint Persistence
Stores thread metadata and conversation history in the shared SQLite database.
"""
import uuid
import json
import sqlite3
import datetime
from typing import List, Dict, Any, Optional
from ..database import get_db_connection


def init_assistant_tables():
    """Initializes tables for assistant thread and message management."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
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
        conn.commit()


def get_or_create_thread(
    thread_id: Optional[str],
    user_id: str,
    repo_id: str,
    commit_sha: str,
    initial_title: str = "New Investigation",
) -> str:
    """Retrieves an existing thread or creates a new one bound to user and snapshot."""
    init_assistant_tables()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if thread_id:
            cursor.execute(
                "SELECT thread_id, user_id, repo_id, commit_sha FROM assistant_threads WHERE thread_id = ?",
                (thread_id,),
            )
            row = cursor.fetchone()
            if row:
                if row["user_id"] != user_id or row["repo_id"] != repo_id or row["commit_sha"] != commit_sha:
                    raise PermissionError("Thread does not match current user, repository, or commit snapshot.")
                return thread_id

        # Create new thread
        new_thread_id = thread_id or f"th_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        cursor.execute(
            """
            INSERT INTO assistant_threads (thread_id, user_id, repo_id, commit_sha, title, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'ACTIVE', ?, ?)
            """,
            (new_thread_id, user_id, repo_id, commit_sha, initial_title[:100], now, now),
        )
        conn.commit()
        return new_thread_id


def save_assistant_message(
    thread_id: str,
    role: str,
    content: str,
    findings: Optional[Dict[str, Any]] = None,
    evidence: Optional[List[Dict[str, Any]]] = None,
    tool_trace: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Appends a message to the thread history."""
    init_assistant_tables()
    msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    findings_json = json.dumps(findings) if findings else None
    evidence_json = json.dumps(evidence) if evidence else None
    tool_trace_json = json.dumps(tool_trace) if tool_trace else None

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO assistant_messages (message_id, thread_id, role, content, findings_json, evidence_json, tool_trace_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (msg_id, thread_id, role, content, findings_json, evidence_json, tool_trace_json, now),
        )
        cursor.execute(
            "UPDATE assistant_threads SET updated_at = ? WHERE thread_id = ?",
            (now, thread_id),
        )
        conn.commit()
    return msg_id


def get_thread_history(thread_id: str, user_id: str) -> List[Dict[str, Any]]:
    """Retrieves all messages for a thread, verifying user ownership."""
    init_assistant_tables()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM assistant_threads WHERE thread_id = ?",
            (thread_id,),
        )
        thread = cursor.fetchone()
        if not thread:
            raise KeyError(f"Thread {thread_id} not found.")
        if thread["user_id"] != user_id:
            raise PermissionError("Access to thread denied.")

        cursor.execute(
            """
            SELECT message_id, role, content, findings_json, evidence_json, tool_trace_json, created_at
            FROM assistant_messages
            WHERE thread_id = ?
            ORDER BY created_at ASC
            """,
            (thread_id,),
        )
        rows = cursor.fetchall()

    messages = []
    for r in rows:
        messages.append({
            "message_id": r["message_id"],
            "role": r["role"],
            "content": r["content"],
            "findings": json.loads(r["findings_json"]) if r["findings_json"] else None,
            "evidence": json.loads(r["evidence_json"]) if r["evidence_json"] else None,
            "tool_trace": json.loads(r["tool_trace_json"]) if r["tool_trace_json"] else None,
            "created_at": r["created_at"],
        })
    return messages


def list_snapshot_threads(user_id: str, repo_id: str, commit_sha: str) -> List[Dict[str, Any]]:
    """Lists all active threads for the authenticated user in the current snapshot."""
    init_assistant_tables()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.thread_id, t.repo_id, t.commit_sha, t.user_id, t.title, t.created_at, t.updated_at,
                   COUNT(m.message_id) AS message_count
            FROM assistant_threads t
            LEFT JOIN assistant_messages m ON t.thread_id = m.thread_id
            WHERE t.user_id = ? AND t.repo_id = ? AND t.commit_sha = ?
            GROUP BY t.thread_id
            ORDER BY t.updated_at DESC
            """,
            (user_id, repo_id, commit_sha),
        )
        rows = cursor.fetchall()

    return [
        {
            "thread_id": r["thread_id"],
            "repo_id": r["repo_id"],
            "commit_sha": r["commit_sha"],
            "user_id": r["user_id"],
            "title": r["title"],
            "message_count": r["message_count"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
        }
        for r in rows
    ]


def mark_thread_cancelled(thread_id: str, user_id: Optional[str] = None) -> bool:
    """Sets a thread status to CANCELLED. If user_id is provided, enforces thread ownership."""
    init_assistant_tables()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute(
                "UPDATE assistant_threads SET status = 'CANCELLED', updated_at = CURRENT_TIMESTAMP WHERE thread_id = ? AND user_id = ?",
                (thread_id, user_id),
            )
        else:
            cursor.execute(
                "UPDATE assistant_threads SET status = 'CANCELLED', updated_at = CURRENT_TIMESTAMP WHERE thread_id = ?",
                (thread_id,),
            )
        conn.commit()
        return cursor.rowcount > 0
