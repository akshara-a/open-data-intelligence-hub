import uuid
from typing import List, Optional, Set
from tree_sitter import Language, Parser, Node
import tree_sitter_python as py_lang

from .base import BaseLanguageParser, ParseResult, format_line_range
from ..models import EntityNode, RelationshipEdge, UnresolvedCallNode
from ..id_generator import (
    generate_entity_ids,
    compute_signature_hash,
    compute_content_hash,
)

PY_LANGUAGE = Language(py_lang.language())


class PythonParser(BaseLanguageParser):
    def __init__(self):
        self.parser = Parser(PY_LANGUAGE)

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

        # 1. File Entity
        code_text = code_bytes.decode("utf-8", errors="replace")
        lines = code_text.splitlines()
        total_lines = len(lines) if lines else 1
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

        # 2. Module Entity (derived from path)
        norm_path = rel_file_path.replace("\\", "/")
        mod_name = norm_path.replace("/", ".").removesuffix(".py").removesuffix(".__init__")
        mod_ent_id, mod_logical_id = generate_entity_ids(
            repo_id, commit_sha, "Module", mod_name
        )
        mod_node = EntityNode(
            entity_id=mod_ent_id,
            logical_entity_id=mod_logical_id,
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=rel_file_path,
            name=mod_name,
            entity_type="Module",
            content_hash=compute_content_hash(code_text),
            line_start=1,
            line_end=total_lines,
        )
        result.entities.append(mod_node)
        result.relationships.append(
            RelationshipEdge(
                source_entity_id=file_ent_id,
                target_entity_id=mod_ent_id,
                rel_type="CONTAINS",
                repo_id=repo_id,
                commit_sha=commit_sha,
            )
        )

        # Walk AST to extract classes, functions, variables, imports, calls
        declared_entity_ids_in_file: List[str] = [file_ent_id, mod_ent_id]

        def get_node_text(node: Node) -> str:
            return code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()

        def extract_decorators(node: Node) -> List[str]:
            decorators = []
            if node.parent and node.parent.type == "decorated_definition":
                for child in node.parent.children:
                    if child.type == "decorator":
                        decorators.append(get_node_text(child))
            return decorators

        def process_function(
            fn_node: Node,
            parent_scope: str,
            parent_id: str,
        ) -> EntityNode:
            name_node = fn_node.child_by_field_name("name")
            fn_name = get_node_text(name_node) if name_node else "anonymous"
            qual_name = f"{parent_scope}.{fn_name}" if parent_scope else fn_name

            # Parameters
            params = []
            param_list = fn_node.child_by_field_name("parameters")
            if param_list:
                for p in param_list.named_children:
                    params.append(get_node_text(p))

            # Return type
            ret_type = ""
            ret_node = fn_node.child_by_field_name("return_type")
            if ret_node:
                ret_type = get_node_text(ret_node)

            sig_hash = compute_signature_hash(params, ret_type)
            fn_body = get_node_text(fn_node)
            fn_ent_id, fn_logical_id = generate_entity_ids(
                repo_id, commit_sha, "Function", qual_name, signature_hash=sig_hash
            )

            decorators = extract_decorators(fn_node)
            is_api = any(
                any(verb in d for verb in ["get(", "post(", "put(", "delete(", "patch(", "route("])
                for d in decorators
            )

            fn_entity = EntityNode(
                entity_id=fn_ent_id,
                logical_entity_id=fn_logical_id,
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path=rel_file_path,
                name=fn_name,
                entity_type="API" if is_api else "Function",
                content_hash=compute_content_hash(fn_body),
                line_start=fn_node.start_point.row + 1,
                line_end=fn_node.end_point.row + 1,
                signature_hash=sig_hash,
                properties={"parameters": params, "return_type": ret_type, "decorators": decorators},
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
            declared_entity_ids_in_file.append(fn_ent_id)

            # Traverse calls inside function
            traverse_calls(fn_node, fn_ent_id)

            return fn_entity

        def process_class(
            class_node: Node,
            parent_scope: str,
            parent_id: str,
        ) -> EntityNode:
            name_node = class_node.child_by_field_name("name")
            class_name = get_node_text(name_node) if name_node else "anonymous"
            qual_name = f"{parent_scope}.{class_name}" if parent_scope else class_name

            class_body = get_node_text(class_node)
            c_ent_id, c_logical_id = generate_entity_ids(
                repo_id, commit_sha, "Class", qual_name
            )

            superclasses = []
            super_node = class_node.child_by_field_name("superclasses")
            if super_node:
                for arg in super_node.named_children:
                    superclasses.append(get_node_text(arg))

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
            declared_entity_ids_in_file.append(c_ent_id)

            # Class body: functions and inner classes
            body = class_node.child_by_field_name("body")
            if body:
                for child in body.children:
                    if child.type == "function_definition":
                        process_function(child, qual_name, c_ent_id)
                    elif child.type == "decorated_definition":
                        for sub in child.children:
                            if sub.type == "function_definition":
                                process_function(sub, qual_name, c_ent_id)
                    elif child.type == "class_definition":
                        process_class(child, qual_name, c_ent_id)

            return c_entity

        def traverse_calls(scope_node: Node, source_entity_id: str):
            for child in scope_node.children:
                if child.type == "call":
                    func_node = child.child_by_field_name("function")
                    if func_node:
                        invoked_name = get_node_text(func_node)
                        # Normalize method calls: e.g. self.do_something() -> do_something
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
                elif child.type not in ("function_definition", "class_definition"):
                    traverse_calls(child, source_entity_id)

        # Traverse top level
        for child in root.children:
            if child.type == "function_definition":
                process_function(child, mod_name, file_ent_id)
            elif child.type == "decorated_definition":
                for sub in child.children:
                    if sub.type == "function_definition":
                        process_function(sub, mod_name, file_ent_id)
                    elif sub.type == "class_definition":
                        process_class(sub, mod_name, file_ent_id)
            elif child.type == "class_definition":
                process_class(child, mod_name, file_ent_id)
            elif child.type in ("import_statement", "import_from_statement"):
                import_text = get_node_text(child)
                # Record as file-level import
                mod_target = ""
                if child.type == "import_statement":
                    for name_n in child.named_children:
                        mod_target = get_node_text(name_n)
                else:
                    mod_n = child.child_by_field_name("module_name")
                    if mod_n:
                        mod_target = get_node_text(mod_n)

                if mod_target:
                    target_ent_id, _ = generate_entity_ids(repo_id, commit_sha, "Module", mod_target)
                    result.relationships.append(
                        RelationshipEdge(
                            source_entity_id=file_ent_id,
                            target_entity_id=target_ent_id,
                            rel_type="IMPORTS",
                            repo_id=repo_id,
                            commit_sha=commit_sha,
                            properties={"statement": import_text},
                        )
                    )
            elif child.type == "expression_statement":
                # Check for top-level variable assignment
                for sub in child.children:
                    if sub.type == "assignment":
                        left = sub.child_by_field_name("left")
                        if left and left.type == "identifier":
                            var_name = get_node_text(left)
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
                                content_hash=compute_content_hash(get_node_text(sub)),
                                line_start=child.start_point.row + 1,
                                line_end=child.end_point.row + 1,
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
