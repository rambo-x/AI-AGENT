import json
from pathlib import Path
from datetime import datetime


class DecisionEngine:

    def __init__(self, root="."):
        self.root = Path(root)

        self.report = {
            "generated_at": datetime.now().isoformat(),
            "status": "completed",
            "decisions": []
        }


    def load_json(self, filename):

        path = self.root / "database" / filename

        if not path.exists():
            return {}

        try:
            return json.loads(
                path.read_text()
            )
        except Exception:
            return {}


    def analyze_logs(self):

        data = self.load_json(
            "log_analysis.json"
        )

        errors = data.get(
            "errors",
            []
        )

        grouped = {}

        for error in errors:

            signature = error.get(
                "signature",
                "unknown"
            )

            if signature not in grouped:
                grouped[signature] = {
                    "count": 0,
                    "error": error
                }

            grouped[signature]["count"] += 1


        for signature, item in grouped.items():

            error = item["error"]

            if signature == "telegram_invalid_token":

                self.report["decisions"].append({

                    "problem":
                        "Telegram authentication failure",

                    "category":
                        "configuration_error",

                    "root_cause":
                        "Invalid Telegram bot token",

                    "occurrences":
                        item["count"],

                    "affected_components":
                        error.get(
                            "component",
                            []
                        ),

                    "evidence":
                        [
                            "telegram_invalid_token detected",
                            f"{item['count']} similar errors found"
                        ],

                    "recommendation":
                        [
                            "Check TELEGRAM_BOT_TOKEN in .env",
                            "Update invalid token",
                            "Restart AI Agent"
                        ],

                    "confidence":
                        error.get(
                            "confidence",
                            0
                        )
                })


    def analyze_health(self):

        data = self.load_json(
            "health_report.json"
        )

        status = data.get(
            "health_status"
        )

        if status == "healthy":

            self.report["decisions"].append({

                "problem":
                    "System structure healthy",

                "category":
                    "system_health",

                "recommendation":
                    [
                        "No structural issue detected"
                    ],

                "confidence":
                    1.0
            })


    def analyze(self):

        self.analyze_logs()
        self.analyze_health()

        return self.report


    def save(self):

        result = self.analyze()

        output = (
            self.root /
            "database/decision_report.json"
        )

        output.write_text(
            json.dumps(
                result,
                indent=4
            )
        )

        return str(output)
