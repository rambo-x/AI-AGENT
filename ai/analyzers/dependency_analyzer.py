"""
==========================================================
TripleSide AI Agent
Dependency Analyzer v1.0
==========================================================

Membaca:
    database/python_index.json

Menghasilkan:
    database/dependency_graph.json

Tugas:
    Membuat hubungan antar file Python berdasarkan import.

Status:
    Development v1.0
"""

import json
from pathlib import Path
from datetime import datetime


class DependencyAnalyzer:

    def __init__(
        self,
        input_file="database/python_index.json",
        output_file="database/dependency_graph.json"
    ):

        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

        self.data = self.load()


    # --------------------------------------------------

    def load(self):

        with self.input_file.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    # --------------------------------------------------

    def python_modules(self):

        modules = {}

        for item in self.data["files"]:

            path = item["path"]

            if not path.endswith(".py"):
                continue

            module = (
                path
                .replace("/", ".")
                .replace("\\", ".")
                .removesuffix(".py")
            )

            if module.endswith(".__init__"):
                module = module.replace(
                    ".__init__",
                    ""
                )

            modules[module] = path

        return modules


    # --------------------------------------------------

    def resolve_import(
        self,
        imported,
        modules
    ):

        matches = []

        for module, path in modules.items():

            if (
                imported == module
                or module.startswith(imported + ".")
                or imported.startswith(module + ".")
            ):
                matches.append(path)

        return matches


    # --------------------------------------------------

    def build_graph(self):

        modules = self.python_modules()

        nodes = list(
            modules.values()
        )

        edges = []


        for item in self.data["files"]:

            source = item["path"]

            for imported in item["imports"]:

                targets = self.resolve_import(
                    imported,
                    modules
                )

                for target in targets:

                    if target == source:
                        continue

                    edges.append(
                        {
                            "source": source,
                            "target": target
                        }
                    )


        return {
            "generated_at": datetime.now().isoformat(),

            "nodes": sorted(nodes),

            "edges": edges
        }


    # --------------------------------------------------

    def save(self):

        result = self.build_graph()

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.output_file.open(
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )


        return str(
            self.output_file
        )


# ------------------------------------------------------

if __name__ == "__main__":

    analyzer = DependencyAnalyzer()

    output = analyzer.save()

    print(
        "Dependency graph created:",
        output
    )
