import uuid
from typing import List, Optional
from tree_sitter import Language, Parser, Node
import tree_sitter_java as java_lang

from .base import BaseLanguageParser, ParseResult, format_line_range
from ..models import EntityNode, RelationshipEdge, UnresolvedCallNode
from ..id_generator import (
    generate_entity_ids,
    compute_signature_hash,
    compute_content_hash,
)

JAVA_LANG = Language(java_lang.language())


class JavaParser(BaseLanguageParser):
    def __init__(self):
        self.parser = Parser(JAVA_LANG)

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

        # Package declaration
        pkg_name = "default"
        for child in root.children:
            if child.type == "package_declaration":
                for sub in child.named_children:
                    if sub.type in ("scoped_identifier", "identifier"):
                        pkg_name = get_node_text(sub)
                        break
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
                if child.type == "method_invocation":
                    name_n = child.child_by_field_name("name")
                    if name_n:
                        invoked_name = get_node_text(name_n)
                        l_range = format_line_range(child.start_point.row, child.end_point.row)
                        call_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{repo_id}::{commit_sha}::{source_entity_id}::{invoked_name}::{rel_file_path}::{l_range}"))
                        uc = UnresolvedCallNode(
                            call_id=f"{repo_id}::{commit_sha}::UnresolvedCall::{call_uuid}",
                            repo_id=repo_id,
                            commit_sha=commit_sha,
                            source_entity_id=source_entity_id,
                            invoked_symbol_name=invoked_name,
                            file_path=rel_file_path,
                            line_range=l_range,
                        )
                        result.unresolved_calls.append(uc)
                elif child.type not in ("method_declaration", "constructor_declaration", "class_declaration", "interface_declaration"):
                    traverse_calls(child, source_entity_id)

        def process_method(m_node: Node, parent_scope: str, parent_id: str):
            name_n = m_node.child_by_field_name("name")
            method_name = get_node_text(name_n) if name_n else "anonymous"
            qual_name = f"{parent_scope}.{method_name}"

            params = []
            param_n = m_node.child_by_field_name("parameters")
            if param_n:
                for p in param_n.named_children:
                    # e.g., int x -> extract type
                    type_n = p.child_by_field_name("type")
                    if type_n:
                        params.append(get_node_text(type_n))
                    else:
                        params.append(get_node_text(p))

            ret_n = m_node.child_by_field_name("type")
            ret_type = get_node_text(ret_n) if ret_n else "void"

            sig_hash = compute_signature_hash(params, ret_type)
            m_ent_id, m_logical_id = generate_entity_ids(
                repo_id, commit_sha, "Function", qual_name, signature_hash=sig_hash
            )
            m_entity = EntityNode(
                entity_id=m_ent_id,
                logical_entity_id=m_logical_id,
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=rel_file_path,
                name=method_name,
                entity_type="Function",
                content_hash=compute_content_hash(get_node_text(m_node)),
                line_start=m_node.start_point.row + 1,
                line_end=m_node.end_point.row + 1,
                signature_hash=sig_hash,
                properties={"parameters": params, "return_type": ret_type},
            )
            result.entities.append(m_entity)
            result.relationships.append(
                RelationshipEdge(
                    source_entity_id=parent_id,
                    target_entity_id=m_ent_id,
                    rel_type="DEFINES",
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                )
            )
            traverse_calls(m_node, m_ent_id)

        def process_class_or_interface(c_node: Node, parent_scope: str):
            name_n = c_node.child_by_field_name("name")
            class_name = get_node_text(name_n) if name_n else "anonymous"
            qual_name = f"{parent_scope}.{class_name}"

            is_iface = c_node.type == "interface_declaration"
            concrete_label = "Interface" if is_iface else "Class"

            superclasses = []
            superclass_n = c_node.child_by_field_name("superclass")
            if superclass_n:
                superclasses.append(get_node_text(superclass_n))

            interfaces_n = c_node.child_by_field_name("interfaces")
            if interfaces_n:
                for iface_type in interfaces_n.named_children:
                    superclasses.append(get_node_text(iface_type))

            c_ent_id, c_logical_id = generate_entity_ids(
                repo_id, commit_sha, concrete_label, qual_name
            )
            c_entity = EntityNode(
                entity_id=c_ent_id,
                logical_entity_id=c_logical_id,
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=rel_file_path,
                name=class_name,
                entity_type=concrete_label,
                content_hash=compute_content_hash(get_node_text(c_node)),
                line_start=c_node.start_point.row + 1,
                line_end=c_node.end_point.row + 1,
                properties={"superclasses": superclasses},
            )
            result.entities.append(c_entity)
            result.relationships.append(
                RelationshipEdge(
                    source_entity_id=file_ent_id,
                    target_entity_id=c_ent_id,
                    rel_type="CONTAINS",
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                )
            )

            # Record extends / implements
            for base in superclasses:
                base_clean = base.split()[-1]
                base_ent_id, _ = generate_entity_ids(repo_id, commit_sha, "Class", base_clean)
                result.relationships.append(
                    RelationshipEdge(
                        source_entity_id=c_ent_id,
                        target_entity_id=base_ent_id,
                        rel_type="EXTENDS",
                        repo_id=repo_id,
                        commit_sha=commit_sha,
                    )
                )

            body = c_node.child_by_field_name("body")
            if body:
                for child in body.children:
                    if child.type in ("method_declaration", "constructor_declaration"):
                        process_method(child, qual_name, c_ent_id)
                    elif child.type in ("class_declaration", "interface_declaration"):
                        process_class_or_interface(child, qual_name)

        for child in root.children:
            if child.type in ("class_declaration", "interface_declaration"):
                process_class_or_interface(child, pkg_name)
            elif child.type == "import_declaration":
                for sub in child.named_children:
                    if sub.type in ("scoped_identifier", "identifier"):
                        imp_name = get_node_text(sub)
                        imp_id, _ = generate_entity_ids(repo_id, commit_sha, "Module", imp_name)
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
