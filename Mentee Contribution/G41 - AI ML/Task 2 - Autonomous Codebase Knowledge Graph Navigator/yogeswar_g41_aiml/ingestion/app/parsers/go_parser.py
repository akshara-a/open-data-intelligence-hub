import uuid
from typing import List, Optional
from tree_sitter import Language, Parser, Node
import tree_sitter_go as go_lang

from .base import BaseLanguageParser, ParseResult, format_line_range
from ..models import EntityNode, RelationshipEdge, UnresolvedCallNode
from ..id_generator import (
    generate_entity_ids,
    compute_signature_hash,
    compute_content_hash,
)

GO_LANG = Language(go_lang.language())


class GoParser(BaseLanguageParser):
    def __init__(self):
        self.parser = Parser(GO_LANG)

    def parse_file(
        self,
        rel_file_path: str,
        code_bytes: bytes,
        repo_id: str,
        commit_sha: str,
    ) -> ParseResult:
        result = ParseResult()
        try:
            tree = self.parser.parse(code_bytes)
        except Exception as e:
            result.syntax_errors.append(f"Failed to parse {rel_file_path}: {e}")
            return result

        root = tree.root_node
        if root.has_error:
            result.syntax_errors.append(f"Syntax error detected in {rel_file_path}, parsing available AST")

        code_text = code_bytes.decode("utf-8", errors="replace")
        lines = code_text.splitlines()
        total_lines = len(lines) if lines else 1

        # File Entity
        file_ent_id, file_logical_id = generate_entity_ids(
            repo_id, commit_sha, "File", rel_file_path
        )
        file_node = EntityNode(
            entity_id=file_ent_id,
            logical_entity_id=file_logical_id,
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=rel_file_path,
            name=rel_file_path.split("/")[-1],
            entity_type="File",
            content_hash=compute_content_hash(code_text),
            line_start=1,
            line_end=total_lines,
        )
        result.entities.append(file_node)

        def get_node_text(node: Node) -> str:
            return code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()

        # Extract package name
        pkg_name = "main"
        for child in root.children:
            if child.type == "package_clause":
                pkg_id = child.child_by_field_name("name") or [c for c in child.children if c.type == "package_identifier"]
                if pkg_id:
                    target = pkg_id if not isinstance(pkg_id, list) else pkg_id[0]
                    pkg_name = get_node_text(target)
                break

        pkg_ent_id, pkg_logical_id = generate_entity_ids(repo_id, commit_sha, "Module", pkg_name)
        result.entities.append(
            EntityNode(
                entity_id=pkg_ent_id,
                logical_entity_id=pkg_logical_id,
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=rel_file_path,
                name=pkg_name,
                entity_type="Module",
                content_hash=compute_content_hash(code_text),
                line_start=1,
                line_end=total_lines,
            )
        )
        result.relationships.append(
            RelationshipEdge(
                source_entity_id=file_ent_id,
                target_entity_id=pkg_ent_id,
                rel_type="CONTAINS",
                repo_id=repo_id,
                commit_sha=commit_sha,
            )
        )

        def traverse_calls(scope_node: Node, source_entity_id: str):
            for child in scope_node.children:
                if child.type == "call_expression":
                    func_n = child.child_by_field_name("function")
                    if func_n:
                        invoked_name = get_node_text(func_n)
                        simple_name = invoked_name.split(".")[-1]
                        l_range = format_line_range(child.start_point.row, child.end_point.row)
                        call_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{repo_id}::{commit_sha}::{source_entity_id}::{simple_name}::{rel_file_path}::{l_range}"))
                        uc = UnresolvedCallNode(
                            call_id=f"{repo_id}::{commit_sha}::UnresolvedCall::{call_uuid}",
                            repo_id=repo_id,
                            commit_sha=commit_sha,
                            source_entity_id=source_entity_id,
                            invoked_symbol_name=simple_name,
                            file_path=rel_file_path,
                            line_range=l_range,
                        )
                        result.unresolved_calls.append(uc)
                elif child.type not in ("function_declaration", "method_declaration"):
                    traverse_calls(child, source_entity_id)

        for child in root.children:
            if child.type == "function_declaration":
                name_n = child.child_by_field_name("name")
                fn_name = get_node_text(name_n) if name_n else "anonymous"
                qual_name = f"{pkg_name}.{fn_name}"

                params = []
                param_n = child.child_by_field_name("parameters")
                if param_n:
                    for p in param_n.named_children:
                        params.append(get_node_text(p))
                res_n = child.child_by_field_name("result")
                ret_type = get_node_text(res_n) if res_n else ""

                sig_hash = compute_signature_hash(params, ret_type)
                fn_ent_id, fn_logical_id = generate_entity_ids(
                    repo_id, commit_sha, "Function", qual_name, signature_hash=sig_hash
                )
                fn_entity = EntityNode(
                    entity_id=fn_ent_id,
                    logical_entity_id=fn_logical_id,
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                    file_path=rel_file_path,
                    name=fn_name,
                    entity_type="Function",
                    content_hash=compute_content_hash(get_node_text(child)),
                    line_start=child.start_point.row + 1,
                    line_end=child.end_point.row + 1,
                    signature_hash=sig_hash,
                )
                result.entities.append(fn_entity)
                result.relationships.append(
                    RelationshipEdge(
                        source_entity_id=file_ent_id,
                        target_entity_id=fn_ent_id,
                        rel_type="CONTAINS",
                        repo_id=repo_id,
                        commit_sha=commit_sha,
                    )
                )
                traverse_calls(child, fn_ent_id)

            elif child.type == "method_declaration":
                name_n = child.child_by_field_name("name")
                fn_name = get_node_text(name_n) if name_n else "anonymous"

                # Receiver
                rec_n = child.child_by_field_name("receiver")
                rec_type = get_node_text(rec_n).replace("*", "").replace("(", "").replace(")", "").split()[-1] if rec_n else "Unknown"
                qual_name = f"{pkg_name}.{rec_type}.{fn_name}"

                params = []
                param_n = child.child_by_field_name("parameters")
                if param_n:
                    for p in param_n.named_children:
                        params.append(get_node_text(p))
                res_n = child.child_by_field_name("result")
                ret_type = get_node_text(res_n) if res_n else ""

                sig_hash = compute_signature_hash(params, ret_type)
                fn_ent_id, fn_logical_id = generate_entity_ids(
                    repo_id, commit_sha, "Function", qual_name, signature_hash=sig_hash
                )
                fn_entity = EntityNode(
                    entity_id=fn_ent_id,
                    logical_entity_id=fn_logical_id,
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                    file_path=rel_file_path,
                    name=fn_name,
                    entity_type="Function",
                    content_hash=compute_content_hash(get_node_text(child)),
                    line_start=child.start_point.row + 1,
                    line_end=child.end_point.row + 1,
                    signature_hash=sig_hash,
                )
                result.entities.append(fn_entity)

                # Link to class / struct if known
                struct_ent_id, _ = generate_entity_ids(repo_id, commit_sha, "Class", f"{pkg_name}.{rec_type}")
                result.relationships.append(
                    RelationshipEdge(
                        source_entity_id=struct_ent_id,
                        target_entity_id=fn_ent_id,
                        rel_type="DEFINES",
                        repo_id=repo_id,
                        commit_sha=commit_sha,
                    )
                )
                traverse_calls(child, fn_ent_id)

            elif child.type == "type_declaration":
                for spec in child.named_children:
                    if spec.type == "type_spec":
                        name_n = spec.child_by_field_name("name")
                        type_n = spec.child_by_field_name("type")
                        t_name = get_node_text(name_n) if name_n else "anonymous"
                        qual_t = f"{pkg_name}.{t_name}"

                        is_interface = type_n and type_n.type == "interface_type"
                        concrete_label = "Interface" if is_interface else "Class"

                        t_ent_id, t_logical_id = generate_entity_ids(
                            repo_id, commit_sha, concrete_label, qual_t
                        )
                        t_entity = EntityNode(
                            entity_id=t_ent_id,
                            logical_entity_id=t_logical_id,
                            repo_id=repo_id,
                            commit_sha=commit_sha,
                            file_path=rel_file_path,
                            name=t_name,
                            entity_type=concrete_label,
                            content_hash=compute_content_hash(get_node_text(spec)),
                            line_start=spec.start_point.row + 1,
                            line_end=spec.end_point.row + 1,
                        )
                        result.entities.append(t_entity)
                        result.relationships.append(
                            RelationshipEdge(
                                source_entity_id=file_ent_id,
                                target_entity_id=t_ent_id,
                                rel_type="CONTAINS",
                                repo_id=repo_id,
                                commit_sha=commit_sha,
                            )
                        )

            elif child.type == "import_declaration":
                for spec in child.named_children:
                    if spec.type == "import_spec":
                        path_n = spec.child_by_field_name("path")
                        if path_n:
                            imp_pkg = get_node_text(path_n).strip('"')
                            imp_id, _ = generate_entity_ids(repo_id, commit_sha, "Module", imp_pkg)
                            result.relationships.append(
                                RelationshipEdge(
                                    source_entity_id=file_ent_id,
                                    target_entity_id=imp_id,
                                    rel_type="IMPORTS",
                                    repo_id=repo_id,
                                    commit_sha=commit_sha,
                                )
                            )

        return result
