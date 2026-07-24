"""
==========================================================
TripleSide AI Agent
Diagnostic Engine v1.0
==========================================================

Membaca:
    logs/agent.log
    database/python_index.json
    database/dependency_graph.json
    database/architecture.json

Menghasilkan:
    database/diagnostics.json

Tugas:
    Mendeteksi masalah berdasarkan rule sederhana.

Status:
    Development v1.0
"""

import json
from pathlib import Path
from datetime import datetime


class DiagnosticEngine:

    def __init__(
        self,
        log_file="logs/agent.log",
        python_index="database/python_index.json",
        dependency_file="database/dependency_graph.json",
        architecture_file="database/architecture.json",
        output_file="database/diagnostics.json"
    ):

        self.log_file = Path(log_file)
        self.python_index_file = Path(python_index)
        self.dependency_file = Path(dependency_file)
        self.architecture_file = Path(architecture_file)
        self.output_file = Path(output_file)

        self.python_index = self.load_json(
            self.python_index_file
        )

        self.dependencies = self.load_json(
            self.dependency_file
        )

        self.architecture = self.load_json(
            self.architecture_file
        )


    # --------------------------------------------------

    def load_json(self, file):

        if not file.exists():

            return {}

        with file.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    # --------------------------------------------------

    def read_logs(self):

        if not self.log_file.exists():

            return ""

        return self.log_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )


    # --------------------------------------------------

    def detect_import_error(self, logs):

        patterns = [
            "ModuleNotFoundError",
            "ImportError",
            "No module named"
        ]

        for pattern in patterns:

            if pattern in logs:

                return {
                    "level": "error",
                    "category": "import_error",
                    "message": pattern + " detected",
                    "possible_causes": [
                        "missing dependency",
                        "wrong import path"
                    ],
                    "confidence": 0.80
                }

        return None


    # --------------------------------------------------

    def detect_runtime_error(self, logs):

        patterns = [
            "Traceback",
            "SyntaxError",
            "TypeError",
            "ValueError",
            "AttributeError"
        ]

        for pattern in patterns:

            if pattern in logs:

                return {
                    "level": "error",
                    "category": "runtime_error",
                    "message": pattern + " detected",
                    "possible_causes": [
                        "code exception",
                        "invalid data",
                        "unexpected state"
                    ],
                    "confidence": 0.70
                }

        return None


    # --------------------------------------------------

    def detect_service_failure(self, logs):

        patterns = [
            "stopped",
            "failed",
            "errored",
            "offline"
        ]

        for pattern in patterns:

            if pattern in logs.lower():

                return {
                    "level": "warning",
                    "category": "service_failure",
                    "message": pattern + " status detected",
                    "possible_causes": [
                        "application crash",
                        "service unavailable"
                    ],
                    "confidence": 0.65
                }

        return None


    # --------------------------------------------------

    def detect_configuration_issue(self, logs):

        patterns = [
            "token",
            "environment",
            ".env",
            "key missing"
        ]

        for pattern in patterns:

            if pattern.lower() in logs.lower():

                return {
                    "level": "warning",
                    "category": "configuration_error",
                    "message": pattern + " reference detected",
                    "possible_causes": [
                        "missing environment variable",
                        "invalid configuration"
                    ],
                    "confidence": 0.60
                }

        return None


    # --------------------------------------------------

    def analyze(self):

        logs = self.read_logs()

        issues = []


        detectors = [
            self.detect_import_error,
            self.detect_runtime_error,
            self.detect_service_failure,
            self.detect_configuration_issue
        ]


        for detector in detectors:

            result = detector(logs)

            if result:

                issues.append(result)


        return {

            "generated_at":
                datetime.now().isoformat(),

            "status":
                "completed",

            "issues":
                issues,

            "architecture":
                self.architecture.get(
                    "architecture_type",
                    "unknown"
                ),

            "dependency_summary":
                {
                    "nodes":
                        len(
                            self.dependencies.get(
                                "nodes",
                                []
                            )
                        ),

                    "edges":
                        len(
                            self.dependencies.get(
                                "edges",
                                []
                            )
                        )
                }
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

    engine = DiagnosticEngine()

    output = engine.save()

    print(
        "Diagnostics created:",
        output
    )
