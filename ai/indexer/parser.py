"""
==========================================================
TripleSide AI Agent
Python Parser v1.0
==========================================================

Parser bertugas membaca seluruh file Python
berdasarkan project_index.json kemudian
menghasilkan python_index.json.

Scanner  -> project_index.json
Parser   -> python_index.json

Parser TIDAK melakukan analisis.

Parser hanya mengambil metadata Python menggunakan AST.

Status :
Stable v1.0
"""


import ast
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from ai.indexer.scanner import ProjectScanner


class ProjectParser:
    """
    Python Parser v1.0
    """

    def __init__(self):

        self.project_root = Path(".").resolve()

        self.index = ProjectScanner.load()

    # -----------------------------------------------------

    def _imports(self, tree: ast.AST) -> List[str]:

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                imports.append(module)

        return sorted(set(imports))

    # -----------------------------------------------------

    def _classes(self, tree: ast.AST) -> List[str]:

        result = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):
                result.append(node.name)

        return sorted(result)

    # -----------------------------------------------------

    def _functions(self, tree: ast.AST) -> List[str]:

        result = []

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                result.append(node.name)

        return sorted(result)

    # -----------------------------------------------------

    def _async_functions(self, tree: ast.AST) -> List[str]:

        result = []

        for node in ast.walk(tree):

            if isinstance(node, ast.AsyncFunctionDef):
                result.append(node.name)

        return sorted(result)

    # -----------------------------------------------------

    def parse_file(self, relative_path: str) -> Dict:

        full_path = self.project_root / relative_path

        info = {
            "path": relative_path,
            "imports": [],
            "classes": [],
            "functions": [],
            "async_functions": [],
            "syntax_error": None
        }

        try:

            source = full_path.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(source)

            info["imports"] = self._imports(tree)

            info["classes"] = self._classes(tree)

            info["functions"] = self._functions(tree)

            info["async_functions"] = self._async_functions(tree)

        except SyntaxError as e:

            info["syntax_error"] = str(e)

        except Exception as e:

            info["syntax_error"] = str(e)

        return info

    # -----------------------------------------------------

    def parse(self) -> Dict:

        results = []
        errors = []

        python_files = [
            file
            for file in self.index["files"]
            if file["language"] == "python"
        ]

        for file in python_files:

            parsed = self.parse_file(file["path"])

            results.append(parsed)

            if parsed["syntax_error"] is not None:
                errors.append({
                    "path": parsed["path"],
                    "error": parsed["syntax_error"]
                })

        return {
            "generated_at": datetime.now().isoformat(),
            "total_files": len(results),
            "parsed_files": len(results) - len(errors),
            "error_files": len(errors),
            "files": sorted(
                results,
                key=lambda item: item["path"]
            ),
            "errors": errors
        }

    # -----------------------------------------------------

    def save(
        self,
        output="database/python_index.json"
    ) -> str:

        data = self.parse()

        output_path = Path(output)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with output_path.open(
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return str(output_path)

    # -----------------------------------------------------

    @staticmethod
    def load(
        path="database/python_index.json"
    ) -> Dict:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)
# -----------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("TripleSide AI Agent")
    print("Python Parser v1.0")
    print("=" * 50)

    parser = ProjectParser()

    output = parser.save()

    print(f"Output : {output}")

    data = ProjectParser.load()

    print(f"Python Files : {data['total_files']}")
    print(f"Parsed       : {data['parsed_files']}")
    print(f"Errors       : {data['error_files']}")

    print("=" * 50)

