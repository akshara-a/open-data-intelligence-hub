from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ..models import EntityNode, RelationshipEdge, UnresolvedCallNode


class ParseResult(BaseModel):
    entities: List[EntityNode] = Field(default_factory=list)
    relationships: List[RelationshipEdge] = Field(default_factory=list)
    unresolved_calls: List[UnresolvedCallNode] = Field(default_factory=list)
    syntax_errors: List[str] = Field(default_factory=list)


def format_line_range(start_row: int, end_row: int) -> str:
    """Format 1-indexed line range: 'start-end'"""
    s = start_row + 1
    e = end_row + 1
    return f"{s}-{e}" if s != e else f"{s}"


class BaseLanguageParser(ABC):
    @abstractmethod
    def parse_file(
        self,
        rel_file_path: str,
        code_bytes: bytes,
        repo_id: str,
        commit_sha: str,
    ) -> ParseResult:
        pass
