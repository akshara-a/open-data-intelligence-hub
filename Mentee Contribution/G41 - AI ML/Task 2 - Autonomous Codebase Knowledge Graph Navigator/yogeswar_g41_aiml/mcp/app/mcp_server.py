import uuid
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .cgg_engine import (
    get_cgg_engine,
    ResultLimitExceededException,
    MemoryLimitExceededException,
    QueryCancelledException,
    InvalidQueryException,
)
from .templates import get_template, QUERY_TEMPLATES
from .git_reader import read_file_from_git
from .auth import enforce_scope


TOOL_DEFINITIONS = [
    {
        "name": "graph.run_query",
        "description": "Executes an approved, parameterized Cypher template within the authorized repository snapshot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "Approved template ID (e.g. impact_downstream_2hop, entity_lookup, direct_neighbors, etc.)",
                    "enum": list(QUERY_TEMPLATES.keys()),
                },
                "parameters": {
                    "type": "object",
                    "description": "Named parameters for the query template.",
                },
            },
            "required": ["operation", "parameters"],
        },
    },
    {
        "name": "graph.get_evidence",
        "description": "Retrieves source code provenance evidence by evidence ID within the authorized repository snapshot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "evidence_id": {
                    "type": "string",
                    "description": "Evidence node identifier (e.g. E-<uuid>)",
                },
            },
            "required": ["evidence_id"],
        },
    },
    {
        "name": "graph.get_evidence_for_entities",
        "description": "Retrieves connected entity and relationship evidence for a batch of entity IDs (max 50) within the active snapshot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of snapshot entity IDs (max 50)",
                },
            },
            "required": ["entity_ids"],
        },
    },
    {
        "name": "repo.read_file",
        "description": "Retrieves commit-pinned source code lines strictly from the bare Git storage volume at the authorized commit SHA.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Canonical relative file path within the repository",
                },
                "start_line": {
                    "type": "integer",
                    "description": "1-indexed starting line number",
                },
                "end_line": {
                    "type": "integer",
                    "description": "1-indexed ending line number",
                },
            },
            "required": ["file_path", "start_line", "end_line"],
        },
    },
    {
        "name": "cgg.snapshot_info",
        "description": "Returns snapshot metadata and repository information for the active authorized snapshot.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "cgg.entity_lookup",
        "description": "Looks up entities by name, concrete type, file path, or stable ID within the snapshot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "entity_type": {"type": "string"},
                "file_path": {"type": "string"},
                "entity_id": {"type": "string"},
            },
        },
    },
    {
        "name": "cgg.entity_details",
        "description": "Retrieves entity attributes and declaration provenance for a specified entity ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string"},
            },
            "required": ["entity_id"],
        },
    },
    {
        "name": "cgg.direct_neighbors",
        "description": "Retrieves direct outgoing dependencies and incoming dependents for a specified entity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string"},
            },
            "required": ["entity_id"],
        },
    },
    {
        "name": "cgg.multi_hop_dependencies",
        "description": "Bounded multi-hop dependency traversal (1 to 3 hops) with strict all-node and all-edge snapshot validation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_entity_id": {"type": "string"},
                "max_depth": {"type": "integer", "enum": [1, 2, 3], "default": 2},
                "direction": {"type": "string", "enum": ["downstream", "upstream"], "default": "downstream"},
            },
            "required": ["start_entity_id"],
        },
    },
    {
        "name": "cgg.relationship_evidence",
        "description": "Retrieves relationship evidence records by evidence ID or by source and target entity IDs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "evidence_id": {"type": "string"},
                "source_entity_id": {"type": "string"},
                "target_entity_id": {"type": "string"},
            },
        },
    },
    {
        "name": "cgg.unresolved_calls",
        "description": "Retrieves unresolvable dynamic call sites and potential uncertain candidate targets within the snapshot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_entity_id": {"type": "string"},
                "file_path": {"type": "string"},
            },
        },
    },
    {
        "name": "cgg.graph_statistics",
        "description": "Aggregates total entity, relationship, evidence, and unresolved call counts for the active snapshot.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def list_tools() -> List[Dict[str, Any]]:
    return TOOL_DEFINITIONS


def execute_tool(
    tool_name: str,
    arguments: Dict[str, Any],
    claims: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Dispatches and executes an approved tool with scope binding and validation.
    """
    repo_id = claims.get("authorized_repo_id")
    commit_sha = claims.get("authorized_commit_sha")

    if not repo_id or not commit_sha:
        raise ValueError("Token claims missing authorized_repo_id or authorized_commit_sha")

    engine = get_cgg_engine()
    query_id = f"qry_{uuid.uuid4().hex[:12]}"

    if tool_name == "graph.run_query":
        op = arguments.get("operation")
        params = arguments.get("parameters", {})
        template = get_template(op)
        if not template:
            raise ValueError(f"Unknown or unapproved query operation: '{op}'")

        # Inject authorized scope parameters
        bound_params = dict(params)
        bound_params["repo_id"] = repo_id
        bound_params["commit_sha"] = commit_sha

        # Fill optional keys if not supplied
        for k in ["entity_id", "name", "file_path", "entity_type", "start_entity_id", "source_entity_id", "target_entity_id", "evidence_id", "limit", "skip"]:
            bound_params.setdefault(k, None)

        records = engine.execute_cgg_query(query_id, template, bound_params)
        return {"operation": op, "records": records, "record_count": len(records), "query_id": query_id}

    elif tool_name == "graph.get_evidence":
        ev_id = arguments.get("evidence_id")
        if not ev_id:
            raise ValueError("evidence_id parameter is required")

        template = get_template("get_evidence")
        records = engine.execute_cgg_query(
            query_id,
            template,
            {"evidence_id": ev_id, "repo_id": repo_id, "commit_sha": commit_sha},
        )
        return {"evidence_id": ev_id, "evidence": records[0] if records else None}

    elif tool_name == "graph.get_evidence_for_entities":
        ent_ids = arguments.get("entity_ids", [])
        if not ent_ids or not isinstance(ent_ids, list):
            raise ValueError("entity_ids must be a non-empty list of entity IDs")
        if len(ent_ids) > 50:
            raise ValueError("entity_ids list cannot exceed 50 items")

        template = get_template("evidence_for_entities")
        records = engine.execute_cgg_query(
            query_id,
            template,
            {"entity_ids": ent_ids, "repo_id": repo_id, "commit_sha": commit_sha},
        )
        return {"records": records, "count": len(records)}

    elif tool_name == "repo.read_file":
        fp = arguments.get("file_path")
        sl = int(arguments.get("start_line", 1))
        el = int(arguments.get("end_line", sl))
        if not fp:
            raise ValueError("file_path is required")
        return read_file_from_git(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=fp,
            start_line=sl,
            end_line=el,
        )

    elif tool_name == "cgg.snapshot_info":
        template = get_template("snapshot_info")
        records = engine.execute_cgg_query(query_id, template, {"repo_id": repo_id, "commit_sha": commit_sha})
        return {"snapshot": records[0] if records else None}

    elif tool_name == "cgg.entity_lookup":
        template = get_template("entity_lookup")
        raw_limit = arguments.get("limit")
        try:
            limit = min(max(int(raw_limit), 1), 500) if raw_limit is not None else 500
        except (ValueError, TypeError):
            limit = 500
        raw_skip = arguments.get("skip")
        try:
            skip = max(int(raw_skip), 0) if raw_skip is not None else 0
        except (ValueError, TypeError):
            skip = 0

        params = {
            "repo_id": repo_id,
            "commit_sha": commit_sha,
            "name": arguments.get("name"),
            "entity_type": arguments.get("entity_type"),
            "file_path": arguments.get("file_path"),
            "entity_id": arguments.get("entity_id"),
            "limit": limit,
            "skip": skip,
        }
        records = engine.execute_cgg_query(query_id, template, params)
        return {"entities": records, "count": len(records), "limit": limit, "skip": skip}

    elif tool_name == "cgg.entity_details":
        ent_id = arguments.get("entity_id")
        if not ent_id:
            raise ValueError("entity_id is required")
        template = get_template("entity_details")
        records = engine.execute_cgg_query(
            query_id,
            template,
            {"entity_id": ent_id, "repo_id": repo_id, "commit_sha": commit_sha},
        )
        return {"entity": records[0] if records else None}

    elif tool_name == "cgg.direct_neighbors":
        ent_id = arguments.get("entity_id")
        if not ent_id:
            raise ValueError("entity_id is required")
        template = get_template("direct_neighbors")
        records = engine.execute_cgg_query(
            query_id,
            template,
            {"entity_id": ent_id, "repo_id": repo_id, "commit_sha": commit_sha},
        )
        return records[0] if records else {"outgoing_dependencies": [], "incoming_dependents": []}

    elif tool_name == "cgg.multi_hop_dependencies":
        start_id = arguments.get("start_entity_id")
        depth = int(arguments.get("max_depth", 2))
        direction = arguments.get("direction", "downstream").lower()

        # Clamp max depth strictly to 1..3 per Section 10.1
        if depth < 1:
            depth = 1
        elif depth > 3:
            depth = 3

        op_name = f"impact_downstream_{depth}hop" if direction == "downstream" else f"dependencies_upstream_{depth}hop"
        template = get_template(op_name)
        records = engine.execute_cgg_query(
            query_id,
            template,
            {"start_entity_id": start_id, "repo_id": repo_id, "commit_sha": commit_sha},
        )
        return {
            "start_entity_id": start_id,
            "direction": direction,
            "max_depth": depth,
            "traversal_results": records,
            "count": len(records),
        }

    elif tool_name == "cgg.relationship_evidence":
        ev_id = arguments.get("evidence_id")
        src_id = arguments.get("source_entity_id")
        tgt_id = arguments.get("target_entity_id")

        if ev_id:
            template = get_template("get_evidence")
            records = engine.execute_cgg_query(
                query_id,
                template,
                {"evidence_id": ev_id, "repo_id": repo_id, "commit_sha": commit_sha},
            )
            return {"evidence": records[0] if records else None}
        elif src_id and tgt_id:
            template = get_template("relationship_evidence_lookup")
            records = engine.execute_cgg_query(
                query_id,
                template,
                {
                    "source_entity_id": src_id,
                    "target_entity_id": tgt_id,
                    "repo_id": repo_id,
                    "commit_sha": commit_sha,
                },
            )
            return {"relationship_evidences": records, "count": len(records)}
        else:
            raise ValueError("Either evidence_id or both source_entity_id and target_entity_id must be provided")

    elif tool_name == "cgg.unresolved_calls":
        template = get_template("unresolved_calls")
        raw_limit = arguments.get("limit")
        try:
            limit = min(max(int(raw_limit), 1), 500) if raw_limit is not None else 500
        except (ValueError, TypeError):
            limit = 500
        raw_skip = arguments.get("skip")
        try:
            skip = max(int(raw_skip), 0) if raw_skip is not None else 0
        except (ValueError, TypeError):
            skip = 0

        params = {
            "repo_id": repo_id,
            "commit_sha": commit_sha,
            "source_entity_id": arguments.get("source_entity_id"),
            "file_path": arguments.get("file_path"),
            "limit": limit,
            "skip": skip,
        }
        records = engine.execute_cgg_query(query_id, template, params)
        return {"unresolved_calls": records, "count": len(records), "limit": limit, "skip": skip}

    elif tool_name == "cgg.graph_statistics":
        template = get_template("graph_statistics")
        records = engine.execute_cgg_query(query_id, template, {"repo_id": repo_id, "commit_sha": commit_sha})
        return records[0] if records else {}

    elif tool_name == "cgg.snapshot_relationships":
        template = get_template("snapshot_relationships")
        raw_limit = arguments.get("limit")
        try:
            limit = min(max(int(raw_limit), 1), 500) if raw_limit is not None else 500
        except (ValueError, TypeError):
            limit = 500
        raw_skip = arguments.get("skip")
        try:
            skip = max(int(raw_skip), 0) if raw_skip is not None else 0
        except (ValueError, TypeError):
            skip = 0

        params = {
            "repo_id": repo_id,
            "commit_sha": commit_sha,
            "relationship_type": arguments.get("relationship_type"),
            "limit": limit,
            "skip": skip,
        }
        records = engine.execute_cgg_query(query_id, template, params)
        return {"relationships": records, "count": len(records), "limit": limit, "skip": skip}

    else:
        raise ValueError(f"Unknown tool: '{tool_name}'")


def handle_json_rpc(request_data: Dict[str, Any], claims: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standard Model Context Protocol JSON-RPC 2.0 processor.
    """
    rpc_id = request_data.get("id")
    method = request_data.get("method")
    params = request_data.get("params", {})

    if not method:
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {"code": -32600, "message": "Invalid Request: missing method"},
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {"tools": list_tools()},
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            result = execute_tool(tool_name, arguments, claims)
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, default=str),
                        }
                    ]
                },
            }
        except (ResultLimitExceededException, MemoryLimitExceededException, QueryCancelledException, InvalidQueryException) as e:
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32000, "message": str(e)},
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32603, "message": f"Tool execution failed: {str(e)}"},
            }

    else:
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {"code": -32601, "message": f"Method '{method}' not found"},
        }
