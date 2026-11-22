import os
import re
import socket
import ipaddress
import urllib.parse
import subprocess
import tarfile
import shutil
from pathlib import Path
from typing import Optional, List, Tuple

UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

BLOCKED_IPV4_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]

BLOCKED_IPV6_NETWORKS = [
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

MAX_REPO_PACK_SIZE_BYTES = 500 * 1024 * 1024       # 500 MiB
MAX_EXTRACTED_SIZE_BYTES = 1024 * 1024 * 1024      # 1 GiB
MAX_FILE_COUNT = 25000
MAX_INDIVIDUAL_FILE_BYTES = 2 * 1024 * 1024        # 2 MiB
GIT_TIMEOUT_SECONDS = 120


class GitSecurityError(Exception):
    pass


class CommitNotFoundError(Exception):
    pass


def validate_repo_id(repo_id: str) -> None:
    """Strict UUIDv4 check per Section 8.2"""
    if not repo_id or not UUID_REGEX.match(repo_id):
        raise GitSecurityError(f"Invalid repo_id '{repo_id}': Must be a valid UUIDv4 string.")


def is_ip_blocked(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip.version == 4:
            return any(ip in net for net in BLOCKED_IPV4_NETWORKS)
        elif ip.version == 6:
            return any(ip in net for net in BLOCKED_IPV6_NETWORKS)
    except ValueError:
        return True
    return False


def validate_egress_target(url: str, allow_local: bool = False) -> None:
    """
    Enforces anti-SSRF and egress network validation per Section 8.2.
    Blocks localhost, private, and reserved IP ranges.
    """
    parsed = urllib.parse.urlparse(url)
    if allow_local or parsed.scheme in ("file", "") or os.path.exists(url):
        return

    hostname = parsed.hostname
    if not hostname:
        raise GitSecurityError(f"Invalid Git URL: missing hostname in '{url}'")

    try:
        addr_info = socket.getaddrinfo(hostname, parsed.port or 443)
        for _, _, _, _, sockaddr in addr_info:
            ip = sockaddr[0]
            if is_ip_blocked(ip):
                raise GitSecurityError(f"Egress blocked: target {hostname} resolved to private/loopback IP {ip}")
    except socket.gaierror as e:
        raise GitSecurityError(f"DNS resolution failure for host '{hostname}': {e}")


def get_git_storage_root() -> Path:
    storage_root = os.getenv("GIT_STORAGE_ROOT", "./git_storage")
    path = Path(storage_root).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_bare_repo_path(repo_id: str) -> Path:
    validate_repo_id(repo_id)
    return get_git_storage_root() / f"{repo_id}.git"


def run_git_command(cmd: List[str], cwd: Optional[Path] = None, timeout: int = GIT_TIMEOUT_SECONDS) -> subprocess.CompletedProcess:
    env = {
        "PATH": os.getenv("PATH", "/usr/bin:/bin"),
        "GIT_TERMINAL_PROMPT": "0",
    }
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )


def sync_bare_repository(repo_id: str, git_url: str, allow_local: bool = False) -> Path:
    """
    Ensures persistent bare mirror exists at /app/git_storage/<repo_id>.git per Section 8.1.
    Clones if not present; fetches origin if already present.
    """
    validate_repo_id(repo_id)
    validate_egress_target(git_url, allow_local=allow_local)
    bare_path = get_bare_repo_path(repo_id)

    # Base security arguments neutralizing hooks and filters
    sec_args = [
        "-c", "core.hooksPath=/dev/null",
        "-c", "protocol.ext.allow=never",
        "-c", "filter.lfs.smudge=",
        "-c", "filter.lfs.clean=",
        "-c", "http.followRedirects=false",
    ]

    is_local = os.path.exists(git_url) or git_url.startswith("file://")

    if not bare_path.exists():
        if is_local:
            # For local repositories / fixtures, safely copy .git database to bare repo
            # avoiding MSYS subshell sh.exe invocation on Windows Sandbox
            source_dir = Path(git_url.removeprefix("file://")).resolve()
            source_git = source_dir / ".git" if (source_dir / ".git").is_dir() else source_dir
            if not source_git.is_dir():
                raise GitSecurityError(f"Local source directory {source_dir} is not a valid git repository")

            shutil.copytree(str(source_git), str(bare_path), dirs_exist_ok=True)
            # Configure bare mode on destination
            cmd = ["git", f"--git-dir={str(bare_path)}"] + sec_args + ["config", "core.bare", "true"]
            run_git_command(cmd)
        else:
            sec_args.extend(["-c", "protocol.file.allow=never"])
            cmd = ["git"] + sec_args + ["clone", "--bare", git_url, str(bare_path)]
            try:
                run_git_command(cmd)
            except subprocess.CalledProcessError as e:
                if bare_path.exists():
                    shutil.rmtree(str(bare_path), ignore_errors=True)
                raise GitSecurityError(f"Failed to clone bare repository for {repo_id}: {e.stderr}")
    else:
        if is_local:
            source_dir = Path(git_url.removeprefix("file://")).resolve()
            source_git = source_dir / ".git" if (source_dir / ".git").is_dir() else source_dir
            if source_git.is_dir():
                shutil.copytree(str(source_git), str(bare_path), dirs_exist_ok=True)
                cmd = ["git", f"--git-dir={str(bare_path)}"] + sec_args + ["config", "core.bare", "true"]
                run_git_command(cmd)
        else:
            cmd = ["git", f"--git-dir={str(bare_path)}"] + sec_args + ["fetch", "origin", "+refs/heads/*:refs/heads/*"]
            try:
                run_git_command(cmd)
            except subprocess.CalledProcessError as e:
                raise GitSecurityError(f"Failed to fetch updates for {repo_id}: {e.stderr}")

    return bare_path


def verify_commit(repo_id: str, commit_sha: str) -> bool:
    """
    Verifies target commit exists in the bare repository via:
    git --git-dir=... cat-file -e <commit_sha>^{commit}
    If missing, attempts fetch; returns True if commit exists, False otherwise.
    """
    bare_path = get_bare_repo_path(repo_id)
    if not bare_path.exists():
        return False

    cmd = ["git", f"--git-dir={str(bare_path)}", "cat-file", "-e", f"{commit_sha}^{{commit}}"]
    try:
        run_git_command(cmd)
        return True
    except subprocess.CalledProcessError:
        fetch_cmd = [
            "git", f"--git-dir={str(bare_path)}",
            "-c", "core.hooksPath=/dev/null",
            "fetch", "origin", commit_sha
        ]
        try:
            run_git_command(fetch_cmd)
            run_git_command(cmd)
            return True
        except subprocess.CalledProcessError:
            return False


def extract_commit_tree(
    repo_id: str,
    commit_sha: str,
    scratch_dir: Path,
) -> List[Path]:
    bare_path = get_bare_repo_path(repo_id)
    if not verify_commit(repo_id, commit_sha):
        raise CommitNotFoundError(f"Commit {commit_sha} not found in repository {repo_id}")

    scratch_dir.mkdir(parents=True, exist_ok=True)
    resolved_scratch = scratch_dir.resolve()

    archive_cmd = ["git", f"--git-dir={str(bare_path)}", "archive", "--format=tar", commit_sha]
    env = {
        "PATH": os.getenv("PATH", "/usr/bin:/bin"),
        "GIT_TERMINAL_PROMPT": "0",
    }
    proc = subprocess.Popen(archive_cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=GIT_TIMEOUT_SECONDS)
    if proc.returncode != 0:
        raise GitSecurityError(f"git archive failed for {commit_sha}: {stderr.decode('utf-8', errors='replace')}")

    tar_path = scratch_dir / "tree.tar"
    tar_path.write_bytes(stdout)

    extracted_files: List[Path] = []
    total_size = 0
    file_count = 0

    try:
        with tarfile.open(str(tar_path), "r:") as tar:
            for member in tar.getmembers():
                if not member.isreg():
                    continue

                file_count += 1
                if file_count > MAX_FILE_COUNT:
                    raise GitSecurityError(f"Extracted file count exceeded maximum limit of {MAX_FILE_COUNT}")

                if member.size > MAX_INDIVIDUAL_FILE_BYTES:
                    continue

                total_size += member.size
                if total_size > MAX_EXTRACTED_SIZE_BYTES:
                    raise GitSecurityError(f"Total extracted size exceeded limit of {MAX_EXTRACTED_SIZE_BYTES} bytes")

                target_path = (resolved_scratch / member.name).resolve()
                try:
                    target_path.relative_to(resolved_scratch)
                except ValueError:
                    raise GitSecurityError(f"Path traversal detected in archive member: {member.name}")

                target_path.parent.mkdir(parents=True, exist_ok=True)
                f = tar.extractfile(member)
                if f:
                    target_path.write_bytes(f.read())
                    extracted_files.append(Path(member.name))
    finally:
        if tar_path.exists():
            tar_path.unlink()

    return extracted_files


def _remove_readonly(func, path, exc_info):
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


def purge_bare_repository(repo_id: str) -> bool:
    validate_repo_id(repo_id)
    bare_path = get_bare_repo_path(repo_id)
    if bare_path.exists():
        shutil.rmtree(str(bare_path), onerror=_remove_readonly)
        return True
    return False
