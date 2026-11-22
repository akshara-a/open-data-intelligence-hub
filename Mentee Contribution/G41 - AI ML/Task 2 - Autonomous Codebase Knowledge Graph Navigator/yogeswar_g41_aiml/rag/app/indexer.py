import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from .models import IndexRequest, IndexResponse, CodeChunk
from .chunker import CodeChunker
from .sqlite_storage import SQLiteChunkStorage
from .cgg_client import CGGClient, get_cgg_client

DEFAULT_GIT_STORAGE = os.getenv("GIT_STORAGE_ROOT", "/app/git_storage")

GIT_STORAGE_SEARCH_PATHS = [
    Path(DEFAULT_GIT_STORAGE),
    Path("./git_storage"),
    Path("../git_storage"),
    Path(__file__).resolve().parent.parent.parent / "git_storage",
]


def find_bare_git_dir(repo_id: str) -> Optional[Path]:
    for base in GIT_STORAGE_SEARCH_PATHS:
        p = base / f"{repo_id}.git"
        if p.is_dir():
            return p
    return None


def extract_files_from_git(repo_id: str, commit_sha: str) -> Dict[str, str]:
    bare_dir = find_bare_git_dir(repo_id)
    if not bare_dir:
        raise FileNotFoundError(f"Bare Git repository for repo_id '{repo_id}' not found")

    # List all files at commit
    ls_cmd = ["git", f"--git-dir={str(bare_dir)}", "ls-tree", "-r", "--name-only", commit_sha]
    res = subprocess.run(ls_cmd, capture_output=True, text=True, check=True)
    all_files = [line.strip() for line in res.stdout.splitlines() if line.strip()]

    # Supported source extensions
    supported_exts = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".md", ".json", ".yml", ".yaml"}
    source_files = [f for f in all_files if Path(f).suffix.lower() in supported_exts]

    file_contents: Dict[str, str] = {}
    for f in source_files:
        show_cmd = ["git", f"--git-dir={str(bare_dir)}", "show", f"{commit_sha}:{f}"]
        show_res = subprocess.run(show_cmd, capture_output=True, text=True, errors="replace")
        if show_res.returncode == 0:
            file_contents[f] = show_res.stdout

    return file_contents


class SnapshotIndexer:
    def __init__(self, db_path: Optional[str] = None, cgg_client: Optional[CGGClient] = None):
        self.storage = SQLiteChunkStorage(db_path)
        self.chunker = CodeChunker()
        self.cgg = cgg_client or get_cgg_client()

    def index_snapshot(
        self,
        repo_id: str,
        commit_sha: str,
        force_reindex: bool = False,
        file_contents: Optional[Dict[str, str]] = None,
    ) -> IndexResponse:
        repo_id = repo_id.strip()
        commit_sha = commit_sha.strip()

        if file_contents is None:
            file_contents = extract_files_from_git(repo_id, commit_sha)

        known_entities: List[Dict[str, Any]] = []
        try:
            known_entities = self.cgg.lookup_entities(repo_id, commit_sha)
        except Exception:
            pass

        all_chunks: List[CodeChunk] = []
        for file_path, content in file_contents.items():
            chunks = self.chunker.chunk_file(
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=file_path,
                content=content,
                known_entities=known_entities,
            )
            all_chunks.extend(chunks)

        reused, newly_embedded = self.storage.persist_chunks(all_chunks, force_reindex=force_reindex)

        return IndexResponse(
            repo_id=repo_id,
            commit_sha=commit_sha,
            total_files=len(file_contents),
            total_chunks=len(all_chunks),
            cached_chunks_reused=reused,
            new_chunks_embedded=newly_embedded,
            status="completed",
        )
