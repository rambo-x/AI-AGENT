import json
from pathlib import Path
from datetime import datetime


class HealthAnalyzer:

    def __init__(self, root="."):
        self.root = Path(root)

        self.report = {
            "generated_at": datetime.now().isoformat(),
            "status": "completed",
            "checks": []
        }


    def check_file(self, path):
        file = self.root / path

        if file.exists():
            return {
                "check": "file_exists",
                "target": path,
                "status": "ok"
            }

        return {
            "check": "file_exists",
            "target": path,
            "status": "missing"
        }


    def check_structure(self):

        required = [
            "app.py",
            "config.py",
            "database",
            "monitor",
            "notifications",
            "scheduler"
        ]

        for item in required:
            self.report["checks"].append(
                self.check_file(item)
            )


    def check_python_environment(self):

        python = self.root / "venv"

        self.report["checks"].append({
            "check": "python_environment",
            "target": "venv",
            "status": "ok" if python.exists() else "missing"
        })


    def analyze(self):

        self.check_structure()
        self.check_python_environment()

        failed = [
            x for x in self.report["checks"]
            if x["status"] != "ok"
        ]

        if failed:
            self.report["health_status"] = "warning"
        else:
            self.report["health_status"] = "healthy"

        return self.report


    def save(self):

        data = self.analyze()

        output = self.root / "database/health_report.json"

        output.write_text(
            json.dumps(
                data,
                indent=4
            )
        )

        return str(output)
