import uuid
from typing import List, Optional
from tree_sitter import Language, Parser, Node
import tree_sitter_typescript as ts_lang

from .base import BaseLanguageParser, ParseResult, format_line_range
from ..models import EntityNode, RelationshipEdge, UnresolvedCallNode
from ..id_generator import (
    generate_entity_ids,
    compute_signature_hash,
    compute_content_hash,
)

TS_LANG = Language(ts_lang.language_typescript())
TSX_LANG = Language(ts_lang.language_tsx())


class JavaScriptTypeScriptParser(BaseLanguageParser):
    def __init__(self, is_tsx: bool = False):
        self.parser = Parser(TSX_LANG if is_tsx else TS_LANG)

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

        # 1. File Entity
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

        # 2. Module Name
        norm_path = rel_file_path.replace("\\", "/")
        for ext in [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"]:
            norm_path = norm_path.removesuffix(ext)
        mod_name = norm_path.replace("/", ".")

        def get_node_text(node: Node) -> str:
            return code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()

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
                elif child.type not in ("function_declaration", "class_declaration", "method_definition"):
                    traverse_calls(child, source_entity_id)

        def process_function(fn_node: Node, parent_scope: str, parent_id: str):
            name_node = fn_node.child_by_field_name("name")
            fn_name = get_node_text(name_node) if name_node else "anonymous"
            qual_name = f"{parent_scope}.{fn_name}" if parent_scope else fn_name

            params = []
            param_node = fn_node.child_by_field_name("parameters")
            if param_node:
                for p in param_node.named_children:
                    params.append(get_node_text(p))

            ret_type = ""
            ret_node = fn_node.child_by_field_name("return_type")
            if ret_node:
                ret_type = get_node_text(ret_node)

            sig_hash = compute_signature_hash(params, ret_type)
            fn_body = get_node_text(fn_node)
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
                content_hash=compute_content_hash(fn_body),
                line_start=fn_node.start_point.row + 1,
                line_end=fn_node.end_point.row + 1,
                signature_hash=sig_hash,
                properties={"parameters": params, "return_type": ret_type},
            )
            result.entities.append(fn_entity)
            result.relationships.append(
                RelationshipEdge(
                    source_entity_id=parent_id,
                    target_entity_id=fn_ent_id,
                    rel_type="DEFINES" if parent_id != file_ent_id else "CONTAINS",
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                )
            )
            traverse_calls(fn_node, fn_ent_id)

        def process_class(class_node: Node, parent_scope: str, parent_id: str):
            name_node = class_node.child_by_field_name("name")
            class_name = get_node_text(name_node) if name_node else "anonymous"
            qual_name = f"{parent_scope}.{class_name}" if parent_scope else class_name

            class_body = get_node_text(class_node)
            c_ent_id, c_logical_id = generate_entity_ids(
                repo_id, commit_sha, "Class", qual_name
            )

            superclasses = []
            heritage = [c for c in class_node.children if c.type in ("class_heritage", "extends_clause")]
            for h in heritage:
                for c in h.named_children:
                    superclasses.append(get_node_text(c))

            c_entity = EntityNode(
                entity_id=c_ent_id,
                logical_entity_id=c_logical_id,
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=rel_file_path,
                name=class_name,
                entity_type="Class",
                content_hash=compute_content_hash(class_body),
                line_start=class_node.start_point.row + 1,
                line_end=class_node.end_point.row + 1,
                properties={"superclasses": superclasses},
            )
            result.entities.append(c_entity)
            result.relationships.append(
                RelationshipEdge(
                    source_entity_id=parent_id,
                    target_entity_id=c_ent_id,
                    rel_type="CONTAINS",
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                )
            )

            body = class_node.child_by_field_name("body")
            if body:
                for child in body.children:
                    if child.type == "method_definition":
                        process_function(child, qual_name, c_ent_id)

        def process_interface(iface_node: Node, parent_scope: str):
            name_node = iface_node.child_by_field_name("name")
            iface_name = get_node_text(name_node) if name_node else "anonymous"
            qual_name = f"{parent_scope}.{iface_name}" if parent_scope else iface_name

            body_text = get_node_text(iface_node)
            i_ent_id, i_logical_id = generate_entity_ids(
                repo_id, commit_sha, "Interface", qual_name
            )
            i_entity = EntityNode(
                entity_id=i_ent_id,
                logical_entity_id=i_logical_id,
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=rel_file_path,
                name=iface_name,
                entity_type="Interface",
                content_hash=compute_content_hash(body_text),
                line_start=iface_node.start_point.row + 1,
                line_end=iface_node.end_point.row + 1,
            )
            result.entities.append(i_entity)
            result.relationships.append(
                RelationshipEdge(
                    source_entity_id=file_ent_id,
                    target_entity_id=i_ent_id,
                    rel_type="CONTAINS",
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                )
            )

        for child in root.children:
            curr = child
            if curr.type == "export_statement":
                # Child under export
                for sc in curr.named_children:
                    if sc.type in ("class_declaration", "function_declaration", "interface_declaration", "lexical_declaration"):
                        curr = sc
                        break

            if curr.type == "function_declaration":
                process_function(curr, mod_name, file_ent_id)
            elif curr.type == "class_declaration":
                process_class(curr, mod_name, file_ent_id)
            elif curr.type == "interface_declaration":
                process_interface(curr, mod_name)
            elif curr.type == "import_statement":
                # Find source string
                source_n = curr.child_by_field_name("source")
                if source_n:
                    import_src = get_node_text(source_n).strip("'\"")
                    tgt_id, _ = generate_entity_ids(repo_id, commit_sha, "Module", import_src)
                    result.relationships.append(
                        RelationshipEdge(
                            source_entity_id=file_ent_id,
                            target_entity_id=tgt_id,
                            rel_type="IMPORTS",
                            repo_id=repo_id,
                            commit_sha=commit_sha,
                            properties={"statement": get_node_text(curr)},
                        )
                    )
            elif curr.type in ("lexical_declaration", "variable_declaration"):
                for decl in curr.named_children:
                    if decl.type == "variable_declarator":
                        name_n = decl.child_by_field_name("name")
                        val_n = decl.child_by_field_name("value")
                        if name_n:
                            var_name = get_node_text(name_n)
                            # Check if value is an arrow function
                            if val_n and val_n.type == "arrow_function":
                                process_function(val_n, mod_name, file_ent_id)
                            else:
                                qual_var = f"{mod_name}.{var_name}"
                                v_ent_id, v_logical_id = generate_entity_ids(
                                    repo_id, commit_sha, "Variable", qual_var
                                )
                                v_entity = EntityNode(
                                    entity_id=v_ent_id,
                                    logical_entity_id=v_logical_id,
                                    repo_id=repo_id,
                                    commit_sha=commit_sha,
                                    file_path=rel_file_path,
                                    name=var_name,
                                    entity_type="Variable",
                                    content_hash=compute_content_hash(get_node_text(decl)),
                                    line_start=curr.start_point.row + 1,
                                    line_end=curr.end_point.row + 1,
                                )
                                result.entities.append(v_entity)
                                result.relationships.append(
                                    RelationshipEdge(
                                        source_entity_id=file_ent_id,
                                        target_entity_id=v_ent_id,
                                        rel_type="CONTAINS",
                                        repo_id=repo_id,
                                        commit_sha=commit_sha,
                                    )
                                )

        return result
