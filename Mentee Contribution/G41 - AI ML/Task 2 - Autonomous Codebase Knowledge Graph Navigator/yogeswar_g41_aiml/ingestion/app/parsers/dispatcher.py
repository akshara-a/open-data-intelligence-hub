from pathlib import Path
from typing import Optional, Dict

from .base import BaseLanguageParser
from .python_parser import PythonParser
from .javascript_parser import JavaScriptTypeScriptParser
from .go_parser import GoParser
from .java_parser import JavaParser

# Single shared instances
_py_parser = PythonParser()
_ts_parser = JavaScriptTypeScriptParser(is_tsx=False)
_tsx_parser = JavaScriptTypeScriptParser(is_tsx=True)
_go_parser = GoParser()
_java_parser = JavaParser()

EXTENSION_MAP: Dict[str, BaseLanguageParser] = {
    ".py": _py_parser,
    ".js": _ts_parser,
    ".jsx": _tsx_parser,
    ".mjs": _ts_parser,
    ".cjs": _ts_parser,
    ".ts": _ts_parser,
    ".tsx": _tsx_parser,
    ".go": _go_parser,
    ".java": _java_parser,
}


def get_parser_for_file(file_path: str) -> Optional[BaseLanguageParser]:
    p = Path(file_path)
    ext = p.suffix.lower()
    return EXTENSION_MAP.get(ext)
