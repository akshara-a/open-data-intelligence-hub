import os
import re
import json
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional
import neo4j

DEFAULT_NEO4J_URL = os.getenv("NEO4J_BOLT_URL", "bolt://neo4j:7687")
DEFAULT_NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD_FILE = os.getenv("NEO4J_PASSWORD_FILE", "/run/secrets/neo4j_admin_password")

KEY_SEARCH_PATHS = [
    Path("/run/secrets"),
    Path("./secrets"),
    Path("../secrets"),
    Path(__file__).resolve().parent.parent.parent / "secrets",
]


class ResultLimitExceededException(Exception):
    """Raised when query produces 501 records, triggering immediate rollback (AC-3.2)."""
    pass


class MemoryLimitExceededException(Exception):
    """Raised when query buffer exceeds 64 MiB (Section 6.3)."""
    pass


class QueryCancelledException(Exception):
    """Raised when query is safely aborted via cooperative cancellation (Section 6.3 / AC-3.5)."""
    pass


class InvalidQueryException(Exception):
    """Raised when an operation attempts arbitrary mutation or unapproved Cypher (Section 10.2)."""
    pass


def get_neo4j_password() -> str:
    path = Path(NEO4J_PASSWORD_FILE)
    if path.is_file():
        pwd = path.read_text(encoding="utf-8").strip()
        if pwd:
            return pwd

    for base in KEY_SEARCH_PATHS:
        sec_file = base / "neo4j_admin.password"
        if sec_file.is_file():
            pwd = sec_file.read_text(encoding="utf-8").strip()
            if pwd:
                return pwd

    if env_pwd := os.getenv("NEO4J_PASSWORD"):
        return env_pwd.strip()

    raise RuntimeError("Neo4j admin password secret not found in environment or secrets file")


# Global thread-safe cooperative cancellation registry
_cancellation_lock = threading.Lock()
_cancellation_events: Dict[str, threading.Event] = {}


def register_cancellation_event(query_id: str) -> threading.Event:
    event = threading.Event()
    with _cancellation_lock:
        _cancellation_events[query_id] = event
    return event


def unregister_cancellation_event(query_id: str):
    with _cancellation_lock:
        _cancellation_events.pop(query_id, None)


def cancel_query(query_id: str) -> bool:
    with _cancellation_lock:
        event = _cancellation_events.get(query_id)
    if event:
        event.set()
        return True
    return False


# Forbidden mutation keywords per AST defense-in-depth (Section 10.2)
FORBIDDEN_WRITE_KEYWORDS = re.compile(
    r"\b(CREATE|MERGE|SET|DELETE|DROP|ALTER|REMOVE|DETACH|FOREACH|TRUNCATE)\b",
    re.IGNORECASE,
)


def validate_read_only_cypher(query_string: str):
    """
    AST Defense Layer (Section 10.2):
    Verifies that no mutation or write clauses exist in the executed Cypher statement.
    """
    clean = re.sub(r"//.*$", "", query_string, flags=re.MULTILINE)
    clean = re.sub(r"/\*.*?\*/", "", clean, flags=re.DOTALL)
    if FORBIDDEN_WRITE_KEYWORDS.search(clean):
        raise InvalidQueryException(
            "Forbidden write or mutation clause detected. CGG is strictly read-only."
        )


class ControlledGraphGatewayEngine:
    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.uri = uri or DEFAULT_NEO4J_URL
        self.user = user or DEFAULT_NEO4J_USER
        self.password = password or get_neo4j_password()
        self._driver: Optional[neo4j.Driver] = None

    def get_driver(self) -> neo4j.Driver:
        if self._driver is None:
            self._driver = neo4j.GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=30 * 60,
                max_connection_pool_size=50,
            )
        return self._driver

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    def ensure_schema(self):
        """
        Idempotent schema initialization per Section 7.3:
        Creates all required uniqueness constraints and performance indexes.
        """
        driver = self.get_driver()
        schema_statements = [
            # 1. Uniqueness Constraints
            "CREATE CONSTRAINT repo_pk IF NOT EXISTS FOR (r:Repo) REQUIRE r.repo_id IS UNIQUE;",
            "CREATE CONSTRAINT snapshot_pk IF NOT EXISTS FOR (s:Snapshot) REQUIRE s.snapshot_id IS UNIQUE;",
            "CREATE CONSTRAINT entity_pk IF NOT EXISTS FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE;",
            "CREATE CONSTRAINT evidence_pk IF NOT EXISTS FOR (ev:Evidence) REQUIRE ev.evidence_id IS UNIQUE;",
            "CREATE CONSTRAINT unresolved_call_pk IF NOT EXISTS FOR (uc:UnresolvedCall) REQUIRE uc.call_id IS UNIQUE;",
            # 2. Performance Composite & Lookup Indexes
            "CREATE INDEX entity_snapshot_idx IF NOT EXISTS FOR (e:Entity) ON (e.repo_id, e.commit_sha);",
            "CREATE INDEX entity_logical_idx IF NOT EXISTS FOR (e:Entity) ON (e.logical_entity_id);",
            "CREATE INDEX entity_name_idx IF NOT EXISTS FOR (e:Entity) ON (e.name);",
            "CREATE INDEX entity_file_idx IF NOT EXISTS FOR (e:Entity) ON (e.file_path);",
            "CREATE INDEX evidence_snapshot_idx IF NOT EXISTS FOR (ev:Evidence) ON (ev.repo_id, ev.commit_sha);",
            "CREATE INDEX unresolved_call_snapshot_idx IF NOT EXISTS FOR (uc:UnresolvedCall) ON (uc.repo_id, uc.commit_sha);",
        ]

        with driver.session(database="neo4j", default_access_mode=neo4j.WRITE_ACCESS) as session:
            for stmt in schema_statements:
                session.run(stmt)

    def execute_cgg_query(
        self,
        query_id: str,
        query_string: str,
        parameters: Dict[str, Any],
        timeout_seconds: float = 5.0,
    ) -> List[Dict[str, Any]]:
        """
        Thread-safe query execution per Section 6.3:
        - AST read-only validation
        - Cooperative thread-safe cancellation
        - Server-side 5.0s transaction timeout
        - Hard 500-row limit rollback (AC-3.2)
        - 64 MiB memory accounting
        """
        validate_read_only_cypher(query_string)

        cancel_event = register_cancellation_event(query_id)
        current_buffer_bytes = 0
        records: List[Dict[str, Any]] = []

        driver = self.get_driver()

        # Ensure parameters has limit and skip defaults if query uses them
        bound_params = dict(parameters)
        bound_params.setdefault("limit", 500)
        bound_params.setdefault("skip", 0)

        try:
            with driver.session(database="neo4j", default_access_mode=neo4j.READ_ACCESS) as session:
                tx = session.begin_transaction(timeout=timeout_seconds)
                try:
                    result = tx.run(query_string, bound_params)
                    for record in result:
                        # 1. Cooperative cancellation check (safely handled by the owning thread)
                        if cancel_event.is_set():
                            raise QueryCancelledException(f"Query '{query_id}' was cancelled by client")

                        # 2. Hard 500-row limit check (AC-3.2)
                        if len(records) >= 500:
                            raise ResultLimitExceededException(
                                "Query exceeded 500 records. Transaction rolled back."
                            )

                        # 3. Accurate memory accounting
                        record_data = record.data()
                        chunk_size = len(json.dumps(record_data, default=str).encode("utf-8"))
                        current_buffer_bytes += chunk_size
                        if current_buffer_bytes > 64 * 1024 * 1024:
                            raise MemoryLimitExceededException(
                                "Result payload exceeded 64 MiB limit. Transaction rolled back."
                            )

                        records.append(record_data)

                    tx.commit()
                    return records
                except Exception:
                    try:
                        tx.rollback()
                    except Exception:
                        pass
                    raise
        finally:
            unregister_cancellation_event(query_id)
            current_buffer_bytes = 0


# Global CGG Engine singleton
_engine_instance: Optional[ControlledGraphGatewayEngine] = None


def get_cgg_engine() -> ControlledGraphGatewayEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ControlledGraphGatewayEngine()
    return _engine_instance
