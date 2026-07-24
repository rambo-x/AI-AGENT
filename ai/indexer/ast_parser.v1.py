import ast
import json
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path("/home/triplesidestudio")


OUTPUT_FILE = Path(
    "database/project_graph.json"
)


PYTHON_EXTENSIONS = [
    ".py"
]


IGNORE_DIRS = {
    "venv",
    "__pycache__",
    "node_modules",
    ".git",
}


class ASTParser:


    def __init__(self, root):

        self.root = Path(root)

        self.graph = {
            "generated_at": datetime.now().isoformat(),
            "files": []
        }



    def should_ignore(self, path):

        return any(
            part in IGNORE_DIRS
            for part in path.parts
        )



    def parse_file(self, file):

        try:

            source = file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(source)


        except Exception as e:

            return {
                "path": str(file),
                "error": str(e)
            }


        data = {

            "path": str(file),

            "language": "python",

            "classes": [],

            "functions": [],

            "async_functions": [],

            "imports": [],

            "from_imports": [],

            "decorators": []

        }



        for node in ast.walk(tree):


            if isinstance(node, ast.ClassDef):

                data["classes"].append(
                    node.name
                )



            elif isinstance(node, ast.FunctionDef):

                data["functions"].append(
                    node.name
                )



            elif isinstance(node, ast.AsyncFunctionDef):

                data["async_functions"].append(
                    node.name
                )



            elif isinstance(node, ast.Import):

                for item in node.names:

                    data["imports"].append(
                        item.name
                    )



            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    data["from_imports"].append(
                        node.module
                    )



            elif isinstance(node, ast.Call):

                if isinstance(
                    node.func,
                    ast.Attribute
                ):

                    if isinstance(
                        node.func.value,
                        ast.Name
                    ):

                        name = (
                            node.func.value.id
                            + "."
                            + node.func.attr
                        )

                        if name not in data["decorators"]:

                            data["decorators"].append(
                                name
                            )


        return data



    def scan(self):


        for file in self.root.rglob("*.py"):


            if self.should_ignore(file):

                continue


            result = self.parse_file(file)


            self.graph["files"].append(
                result
            )


        return self.graph



    def save(self):

        OUTPUT_FILE.parent.mkdir(
            exist_ok=True
        )


        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.graph,
                f,
                indent=4
            )



if __name__ == "__main__":


    parser = ASTParser(
        PROJECT_ROOT
    )


    parser.scan()

    parser.save()


    print(
        "AST Parser selesai"
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )
