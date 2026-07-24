import ast
import json
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path("/home/triplesidestudio/tripleside-ai-agent")
OUTPUT = Path("database/project_graph.json")


class ProjectAnalyzer(ast.NodeVisitor):

    def __init__(self, filepath):
        self.filepath = str(filepath)

        self.classes = []
        self.functions = []
        self.async_functions = []
        self.imports = []
        self.from_imports = []
        self.decorators = []

        self.api_routes = []
        self.database_usage = []
        self.environment = []


    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)


    def visit_FunctionDef(self, node):

        self.functions.append(node.name)

        self.scan_decorators(node)

        self.generic_visit(node)


    def visit_AsyncFunctionDef(self, node):

        self.async_functions.append(node.name)

        self.scan_decorators(node)

        self.generic_visit(node)


    def visit_Import(self, node):

        for item in node.names:
            self.imports.append(item.name)


    def visit_ImportFrom(self, node):

        if node.module:
            self.from_imports.append(node.module)


    def scan_decorators(self, node):

        for dec in node.decorator_list:

            name = self.get_name(dec)

            if name:
                self.decorators.append(name)

            self.detect_api(dec, node)


    def visit_Call(self, node):

        name = self.get_name(node.func)

        if name:

            # ENV
            if name in [
                "getenv",
                "os.getenv"
            ]:

                if node.args:

                    value = self.get_string(node.args[0])

                    if value:
                        self.environment.append(value)


            # DATABASE
            if any(
                x in name
                for x in [
                    "find",
                    "insert_one",
                    "update_one",
                    "delete_one",
                    "find_one"
                ]
            ):

                self.database_usage.append({
                    "operation": name
                })


            # Mongo client
            if "AsyncIOMotorClient" in name:

                self.database_usage.append({
                    "type": "mongodb",
                    "client": name
                })


        self.generic_visit(node)



    def detect_api(self, decorator, node):

        if not isinstance(decorator, ast.Call):
            return

        name = self.get_name(decorator.func)

        if not name:
            return


        if name.endswith(
            (
                "get",
                "post",
                "put",
                "delete",
                "patch"
            )
        ):

            path = None

            if decorator.args:
                path = self.get_string(
                    decorator.args[0]
                )


            self.api_routes.append({

                "method": name.split(".")[-1].upper(),

                "path": path,

                "function": node.name

            })



    def get_name(self,node):

        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):

            value = self.get_name(node.value)

            if value:
                return value+"."+node.attr

        return None



    def get_string(self,node):

        if isinstance(node, ast.Constant):
            return str(node.value)

        return None



def scan_file(filepath):

    try:

        source = filepath.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

    except Exception:

        return None


    analyzer = ProjectAnalyzer(filepath)

    analyzer.visit(tree)


    return {

        "path":str(filepath),

        "language":"python",

        "classes": analyzer.classes,

        "functions": analyzer.functions,

        "async_functions": analyzer.async_functions,

        "imports": analyzer.imports,

        "from_imports": analyzer.from_imports,

        "decorators": analyzer.decorators,

        "api_routes": analyzer.api_routes,

        "database_usage": analyzer.database_usage,

        "environment": list(
            set(analyzer.environment)
        )

    }



def build_graph():

    files=[]


    for file in PROJECT_ROOT.rglob("*.py"):

        if "venv" in str(file):
            continue

        if "__pycache__" in str(file):
            continue


        result = scan_file(file)

        if result:
            files.append(result)



    graph={

        "generated_at":
            datetime.now().isoformat(),

        "total_files":
            len(files),

        "files":
            files

    }


    OUTPUT.parent.mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            graph,
            f,
            indent=4
        )


    print("AST Parser v2 selesai")

    print(
        f"Files scanned: {len(files)}"
    )

    print(
        f"Output: {OUTPUT}"
    )



if __name__=="__main__":

    build_graph()
