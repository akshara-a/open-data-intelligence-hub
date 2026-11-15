"""Static safety validation for LLM-generated Cypher (defence-in-depth layer 1).

Layer 2: sessions are opened with READ_ACCESS + managed read transactions.
Layer 3 (recommended): a read-only Neo4j role/DB (see README).
"""
from __future__ import annotations

import re
from dataclasses import dataclass


class UnsafeCypherError(ValueError):
    pass


@dataclass
class GuardResult:
    ok: bool
    reason: str = ""


_STRIP = re.compile(
    r"""//[^\n]*|/\*.*?\*/|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|`[^`]*`""",
    re.S,
)
_WRITE_KW = re.compile(
    r"(?<![.:\w$`])(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|FOREACH|GRANT|DENY|REVOKE|ALTER|"
    r"LOAD\s+CSV|TERMINATE|DBMS)(?![\w`])",
    re.I,
)
_CALL = re.compile(r"\bCALL\b\s*(\{|[\w.]+)", re.I)
_ALLOWED_PROCS = {
    "db.labels",
    "db.relationshiptypes",
    "db.propertykeys",
    "db.schema.visualization",
    "db.schema.nodetypeproperties",
    "db.schema.reltypeproperties",
}


def validate_cypher(cypher: str) -> GuardResult:
    if not cypher or not cypher.strip():
        return GuardResult(False, "Empty query.")
    body = _STRIP.sub("''", cypher).strip()
    if ";" in body.rstrip(";"):
        return GuardResult(False, "Only a single Cypher statement is allowed.")
    m = _WRITE_KW.search(body)
    if m:
        return GuardResult(False, f"Write/admin keyword not allowed in read-only mode: {m.group(1).upper()}")
    if re.search(r"\bapoc\s*\.", body, re.I):
        return GuardResult(False, "APOC procedures/functions are not allowed.")
    for target in _CALL.findall(body):
        if target != "{" and target.lower() not in _ALLOWED_PROCS:
            return GuardResult(False, f"Procedure not allow-listed: {target}")
    if not re.search(r"\b(RETURN|CALL)\b", body, re.I):
        return GuardResult(False, "Query must contain a RETURN clause.")
    return GuardResult(True)
