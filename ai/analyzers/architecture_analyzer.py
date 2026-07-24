"""
==========================================================
TripleSide AI Agent
Architecture Analyzer v1.0
==========================================================

Membaca:
    database/project_index.json
    database/project_analysis.json
    database/dependency_graph.json

Menghasilkan:
    database/architecture.json

Tugas:
    Menyimpulkan struktur arsitektur project.

Status:
    Development v1.0
"""

import json
from pathlib import Path
from datetime import datetime


class ArchitectureAnalyzer:

    def __init__(
        self,
        index_file="database/project_index.json",
        analysis_file="database/project_analysis.json",
        dependency_file="database/dependency_graph.json",
        output_file="database/architecture.json"
    ):

        self.index_file = Path(index_file)
        self.analysis_file = Path(analysis_file)
        self.dependency_file = Path(dependency_file)
        self.output_file = Path(output_file)

        self.index = self.load(self.index_file)
        self.analysis = self.load(self.analysis_file)
        self.dependencies = self.load(self.dependency_file)


    # --------------------------------------------------

    def load(self, file):

        with file.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    # --------------------------------------------------

    def detect_entry_points(self):

        candidates = [
            "app.py",
            "main.py",
            "run.py",
            "server.py"
        ]

        result = []

        for item in self.index["files"]:

            path = item["path"]

            if path in candidates:
                result.append(path)

        return result


    # --------------------------------------------------

    def detect_layers(self):

        layers = {
            "ai": [],
            "monitor": [],
            "database": [],
            "notifications": [],
            "scheduler": [],
            "events": [],
            "utils": []
        }


        for item in self.index["files"]:

            path = item["path"]

            parts = path.split("/")


            if len(parts) < 2:
                continue


            folder = parts[0]


            if folder in layers:

                layers[folder].append(path)


        return layers


    # --------------------------------------------------

    def detect_core_components(self):

        components = []

        layers = self.detect_layers()


        for name, files in layers.items():

            if len(files) > 0:

                components.append(name)


        return components


    # --------------------------------------------------

    def dependency_summary(self):

        return {
            "nodes": len(
                self.dependencies.get(
                    "nodes",
                    []
                )
            ),

            "edges": len(
                self.dependencies.get(
                    "edges",
                    []
                )
            )
        }


    # --------------------------------------------------

    def analyze(self):

        return {

            "generated_at":
                datetime.now().isoformat(),

            "architecture_type":
                "modular_python_application",

            "entry_points":
                self.detect_entry_points(),

            "layers":
                self.detect_layers(),

            "core_components":
                self.detect_core_components(),

            "dependency_summary":
                self.dependency_summary()
        }


    # --------------------------------------------------

    def save(self):

        result = self.analyze()


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

    analyzer = ArchitectureAnalyzer()

    output = analyzer.save()

    print(
        "Architecture created:",
        output
    )
