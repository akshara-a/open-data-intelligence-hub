import hashlib
import urllib.parse
from typing import Optional, Tuple


def canonical_encode(raw_string: str) -> str:
    """
    Encodes sub-components using RFC 3986 percent-encoding per Section 7.1.
    All colons (:), slashes (/), and spaces are percent-encoded.
    Double colon (::) is strictly reserved as the structural field delimiter.
    """
    if raw_string is None:
        return ""
    # safe="" ensures '/' and other standard chars are percent-encoded
    return urllib.parse.quote(str(raw_string), safe="")


def compute_signature_hash(parameters: list[str], return_type: str = "") -> str:
    """
    Computes first 12 hex characters of SHA-256 of normalized parameter types and return type
    per Section 7.1. Distinguishes overloaded signatures without hashing function body.
    """
    norm_params = [p.strip() for p in parameters if p.strip()]
    norm_return = return_type.strip()
    signature_str = f"({','.join(norm_params)})->{norm_return}"
    digest = hashlib.sha256(signature_str.encode("utf-8")).hexdigest()
    return digest[:12]


def compute_content_hash(code_body: str) -> str:
    """
    Computes SHA-256 (head 16 hex chars per Section 7.2) of entity source body.
    """
    if code_body is None:
        code_body = ""
    return hashlib.sha256(code_body.encode("utf-8")).hexdigest()[:16]


def generate_entity_ids(
    repo_id: str,
    commit_sha: str,
    entity_type: str,
    qualified_name: str,
    signature_hash: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Generates (entity_id, logical_entity_id) per Section 7.1:
    - logical_entity_id: <repo_id>::<entity_type>::<encoded_qualified_name>[::<signature_hash>]
    - entity_id: <repo_id>::<commit_sha>::<entity_type>::<encoded_qualified_name>[::<signature_hash>]
    """
    encoded_name = canonical_encode(qualified_name)
    if signature_hash:
        logical_id = f"{repo_id}::{entity_type}::{encoded_name}::{signature_hash}"
        snapshot_id = f"{repo_id}::{commit_sha}::{entity_type}::{encoded_name}::{signature_hash}"
    else:
        logical_id = f"{repo_id}::{entity_type}::{encoded_name}"
        snapshot_id = f"{repo_id}::{commit_sha}::{entity_type}::{encoded_name}"

    return snapshot_id, logical_id
