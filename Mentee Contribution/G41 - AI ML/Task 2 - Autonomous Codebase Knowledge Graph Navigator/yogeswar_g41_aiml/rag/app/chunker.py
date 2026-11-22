import re
import hashlib
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

from .models import CodeChunk

# Try importing Phase 2 parser dispatcher if available in PYTHONPATH
try:
    from ingestion.app.parsers.dispatcher import get_parser_for_file
except ImportError:
    get_parser_for_file = None

MAX_CHUNK_LINES = 80
CHUNK_OVERLAP_LINES = 10


def canonical_encode(component: str) -> str:
    """RFC 3986 percent-encoding per Section 7.1"""
    return urllib.parse.quote(component, safe="")


def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]


class CodeChunker:
    """
    Deterministic language-aware source code chunker.
    Preserves exact file paths, line ranges, and parsed entity boundaries.
    """

    def __init__(self, max_chunk_lines: int = MAX_CHUNK_LINES, overlap_lines: int = CHUNK_OVERLAP_LINES):
        self.max_chunk_lines = max_chunk_lines
        self.overlap_lines = overlap_lines

    def chunk_file(
        self,
        repo_id: str,
        commit_sha: str,
        file_path: str,
        content: str,
        known_entities: Optional[List[Dict[str, Any]]] = None,
    ) -> List[CodeChunk]:
        clean_path = file_path.strip().lstrip("/").replace("\\", "/")
        lines = content.splitlines()
        total_lines = len(lines)
        if total_lines == 0:
            return []

        chunks: List[CodeChunk] = []
        covered_line_ranges: List[tuple[int, int]] = []

        # 1. Prefer parsed entity boundaries (Function, Class, Method)
        entity_spans = []
        if known_entities:
            for ent in known_entities:
                ent_fp = str(ent.get("file_path", "")).strip().lstrip("/").replace("\\", "/")
                if (ent_fp == clean_path or ent_fp.endswith("/" + clean_path) or clean_path.endswith("/" + ent_fp)) and ent.get("line_start") and ent.get("line_end"):
                    ent_dict = dict(ent)
                    if "entity_type" not in ent_dict:
                        types = ent_dict.get("entity_types") or []
                        ent_dict["entity_type"] = types[0] if types else "Code"
                    entity_spans.append(ent_dict)
        elif get_parser_for_file is not None:
            parser = get_parser_for_file(clean_path)
            if parser is not None:
                try:
                    parsed_entities, _, _ = parser.parse(clean_path, content)
                    for e in parsed_entities:
                        if e.entity_type in ("Function", "Class", "Method", "Interface") and e.line_start <= e.line_end:
                            entity_spans.append({
                                "entity_id": getattr(e, "entity_id", None),
                                "name": e.name,
                                "entity_type": e.entity_type,
                                "line_start": e.line_start,
                                "line_end": min(e.line_end, total_lines),
                            })
                except Exception:
                    pass

        # Sort entity spans by line_start
        entity_spans.sort(key=lambda x: (x["line_start"], -x["line_end"]))

        for ent in entity_spans:
            l_start = max(1, ent["line_start"])
            l_end = min(total_lines, ent["line_end"])
            span_len = l_end - l_start + 1

            if span_len <= self.max_chunk_lines:
                # Bounded entity chunk
                chunk_lines = lines[l_start - 1 : l_end]
                chunk_text = "\n".join(chunk_lines)
                if chunk_text.strip():
                    c_hash = compute_content_hash(chunk_text)
                    chunk_id = f"{repo_id}::{commit_sha}::Chunk::{canonical_encode(clean_path)}::{l_start}_{l_end}"
                    idx_text = f"[{ent.get('entity_type', 'Code')}] {ent.get('name', '')} in {clean_path}:{l_start}-{l_end}\n{chunk_text}"
                    chunks.append(
                        CodeChunk(
                            chunk_id=chunk_id,
                            repo_id=repo_id,
                            commit_sha=commit_sha,
                            file_path=clean_path,
                            line_start=l_start,
                            line_end=l_end,
                            entity_id=ent.get("entity_id"),
                            entity_name=ent.get("name"),
                            entity_type=ent.get("entity_type"),
                            content=chunk_text,
                            content_hash=c_hash,
                            indexed_text=idx_text,
                        )
                    )
                    covered_line_ranges.append((l_start, l_end))
            else:
                # Sub-chunk large entity into bounded overlapping windows
                curr_start = l_start
                while curr_start <= l_end:
                    curr_end = min(curr_start + self.max_chunk_lines - 1, l_end)
                    chunk_lines = lines[curr_start - 1 : curr_end]
                    chunk_text = "\n".join(chunk_lines)
                    if chunk_text.strip():
                        c_hash = compute_content_hash(chunk_text)
                        chunk_id = f"{repo_id}::{commit_sha}::Chunk::{canonical_encode(clean_path)}::{curr_start}_{curr_end}"
                        idx_text = f"[{ent.get('entity_type', 'Code')}] {ent.get('name', '')} (part {curr_start}-{curr_end}) in {clean_path}\n{chunk_text}"
                        chunks.append(
                            CodeChunk(
                                chunk_id=chunk_id,
                                repo_id=repo_id,
                                commit_sha=commit_sha,
                                file_path=clean_path,
                                line_start=curr_start,
                                line_end=curr_end,
                                entity_id=ent.get("entity_id"),
                                entity_name=ent.get("name"),
                                entity_type=ent.get("entity_type"),
                                content=chunk_text,
                                content_hash=c_hash,
                                indexed_text=idx_text,
                            )
                        )
                        covered_line_ranges.append((curr_start, curr_end))
                    curr_start += (self.max_chunk_lines - self.overlap_lines)

        # 2. Chunk un-covered code regions or non-entity lines
        curr_line = 1
        while curr_line <= total_lines:
            # Check if line is already within a covered entity range
            is_covered = any(start <= curr_line <= end for start, end in covered_line_ranges)
            if is_covered:
                curr_line += 1
                continue

            # Form a linear chunk
            win_start = curr_line
            win_end = min(win_start + self.max_chunk_lines - 1, total_lines)
            chunk_lines = lines[win_start - 1 : win_end]
            chunk_text = "\n".join(chunk_lines)
            if chunk_text.strip():
                c_hash = compute_content_hash(chunk_text)
                chunk_id = f"{repo_id}::{commit_sha}::Chunk::{canonical_encode(clean_path)}::{win_start}_{win_end}"
                idx_text = f"[SourceCode] {clean_path}:{win_start}-{win_end}\n{chunk_text}"
                chunks.append(
                    CodeChunk(
                        chunk_id=chunk_id,
                        repo_id=repo_id,
                        commit_sha=commit_sha,
                        file_path=clean_path,
                        line_start=win_start,
                        line_end=win_end,
                        entity_id=None,
                        entity_name=Path(clean_path).stem,
                        entity_type="FileChunk",
                        content=chunk_text,
                        content_hash=c_hash,
                        indexed_text=idx_text,
                    )
                )
            curr_line = win_end + 1

        # Deduplicate and sort deterministically by line_start
        seen_ids = set()
        unique_chunks: List[CodeChunk] = []
        for c in sorted(chunks, key=lambda x: (x.line_start, x.line_end)):
            if c.chunk_id not in seen_ids:
                seen_ids.add(c.chunk_id)
                unique_chunks.append(c)

        return unique_chunks
