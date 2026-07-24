from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict
import json

from ai.indexer.scanner import ProjectScanner


class ProjectAnalyzer:
    """
    Project Analyzer v1.0

    Membaca project_index.json kemudian
    menghasilkan project_analysis.json.

    Modul ini dianggap STABLE.
    """

    def __init__(self):
        self.index = ProjectScanner.load()

    def analyze(self) -> Dict:

        components = defaultdict(
            lambda: {
                "files": 0,
                "python_files": 0,
                "languages": set()
            }
        )

        for file in self.index["files"]:

            component = file["component"]

            components[component]["files"] += 1

            if file["language"] == "python":
                components[component]["python_files"] += 1

            components[component]["languages"].add(
                file["language"]
            )

        result = {
            "generated_at": datetime.now().isoformat(),
            "total_components": len(components),
            "components": {}
        }

        for name in sorted(components):

            info = components[name]

            result["components"][name] = {
                "files": info["files"],
                "python_files": info["python_files"],
                "languages": sorted(info["languages"])
            }

        return result

    def save(
        self,
        output="database/project_analysis.json"
    ) -> str:

        result = self.analyze()

        Path(output).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output, "w", encoding="utf-8") as f:
            json.dump(
                result,
                f,
                indent=4,
                ensure_ascii=False
            )

        return output

    @staticmethod
    def load(
        path="database/project_analysis.json"
    ) -> Dict:

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
