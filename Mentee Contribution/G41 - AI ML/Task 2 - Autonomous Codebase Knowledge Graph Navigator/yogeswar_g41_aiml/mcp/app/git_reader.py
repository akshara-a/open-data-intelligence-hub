import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

DEFAULT_GIT_STORAGE = os.getenv("GIT_STORAGE_ROOT", "/app/git_storage")

GIT_STORAGE_SEARCH_PATHS = [
    Path(DEFAULT_GIT_STORAGE),
    Path("./git_storage"),
    Path("../git_storage"),
    Path(__file__).resolve().parent.parent.parent / "git_storage",
]

REPO_ID_REGEX = re.compile(r"^[0-9a-zA-Z\-_.]+$")
SHA_REGEX = re.compile(r"^[0-9a-fA-F]{4,64}$")


def get_git_repo_path(repo_id: str) -> Path:
    if not REPO_ID_REGEX.match(repo_id) or ".." in repo_id or "/" in repo_id or "\\" in repo_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid repo_id: path traversal characters disallowed",
        )

    for base in GIT_STORAGE_SEARCH_PATHS:
        candidate = base / f"{repo_id}.git"
        if candidate.is_dir():
            return candidate

    # Return primary default if not yet found
    return Path(DEFAULT_GIT_STORAGE) / f"{repo_id}.git"


def read_file_from_git(
    repo_id: str,
    commit_sha: str,
    file_path: str,
    start_line: int,
    end_line: int,
) -> Dict[str, Any]:
    """
    Extracts commit-pinned source code from the bare Git mirror per Section 6.4 / AC-3.3.
    Executes 'git show <commit_sha>:<file_path>' in bare repo.
    """
    if not SHA_REGEX.match(commit_sha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid commit_sha format",
        )

    clean_file_path = file_path.strip().lstrip("/").replace("\\", "/")
    if ".." in clean_file_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file_path: path traversal not permitted",
        )

    if start_line < 1:
        start_line = 1
    if end_line < start_line:
        end_line = start_line

    repo_dir = get_git_repo_path(repo_id)
    if not repo_dir.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bare Git repository for repo_id '{repo_id}' not found at {repo_dir}",
        )

    cmd = [
        "git",
        f"--git-dir={str(repo_dir)}",
        "show",
        f"{commit_sha}:{clean_file_path}",
    ]

    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5.0,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Git source extraction timed out",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute git show: {str(e)}",
        )

    if res.returncode != 0:
        err = res.stderr.strip()
        if "does not exist in" in err or "fatal: path" in err:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File '{clean_file_path}' not found at commit '{commit_sha}'",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Git command failed: {err}",
        )

    all_lines = res.stdout.splitlines()
    total_lines = len(all_lines)

    # 1-indexed line extraction [start_line - 1 : end_line]
    sliced_lines = all_lines[start_line - 1 : end_line]
    content = "\n".join(sliced_lines)

    return {
        "repo_id": repo_id,
        "commit_sha": commit_sha,
        "file_path": clean_file_path,
        "start_line": start_line,
        "end_line": min(end_line, total_lines),
        "total_file_lines": total_lines,
        "lines": sliced_lines,
        "content": content,
    }
