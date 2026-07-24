import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    def __init__(self):
        self.database = Path("database")
        self.output = self.database / "final_report.json"

    def load_json(self, filename):
        path = self.database / filename

        if not path.exists():
            return {}

        try:
            with open(path, "r") as file:
                return json.load(file)
        except Exception:
            return {}

    def analyze_status(self, health):
        if health.get("health_status") == "healthy":
            return "HEALTHY"

        return "WARNING"

    def collect_issues(self, decisions):
        issues = []

        for item in decisions.get("decisions", []):
            if item.get("category") != "system_health":
                issues.append(
                    {
                        "problem": item.get("problem"),
                        "category": item.get("category"),
                        "root_cause": item.get("root_cause"),
                        "confidence": item.get("confidence"),
                        "recommendation": item.get("recommendation", [])
                    }
                )

        return issues

    def generate(self):
        health = self.load_json("health_report.json")
        decisions = self.load_json("decision_report.json")
        reasoning = self.load_json("reasoning_report.json")

        report = {
            "generated_at": datetime.now().isoformat(),
            "status": "completed",
            "system_status": self.analyze_status(health),
            "summary": {
                "total_issues": len(
                    self.collect_issues(decisions)
                )
            },
            "issues": self.collect_issues(decisions),
            "reasoning_summary": {
                "architecture": reasoning.get("architecture"),
                "status": reasoning.get("status")
            }
        }

        return report

    def save(self):
        report = self.generate()

        self.database.mkdir(exist_ok=True)

        with open(self.output, "w") as file:
            json.dump(
                report,
                file,
                indent=4
            )

        return str(self.output)


if __name__ == "__main__":
    generator = ReportGenerator()
    print(generator.save())
