import json
from pathlib import Path
from datetime import datetime

from ai.memory.feedback import MemoryFeedback


class DecisionEngine:

    def __init__(self, root="."):

        self.root = Path(root)

        self.memory = MemoryFeedback()

        self.brain = self.load_json(
            "system_brain.json"
        )

        self.report = {

            "generated_at":
                datetime.now().isoformat(),

            "system":
                "TripleSide AI Agent",

            "status":
                "completed",

            "decisions":
                []

        }


    def load_json(self, filename):

        path = (
            self.root /
            "database" /
            filename
        )


        if not path.exists():

            return {}


        try:

            return json.loads(
                path.read_text()
            )

        except Exception:

            return {}



    def save_report(self):

        path = (
            self.root /
            "database" /
            "decision_report.json"
        )


        path.write_text(
            json.dumps(
                self.report,
                indent=4
            )
        )



    def remember(
        self,
        problem,
        category,
        cause,
        solution
    ):

        try:

            return self.memory.save(
                {

                    "problem":problem,

                    "category":category,

                    "cause":cause,

                    "solution":solution

                }
            )

        except Exception:

            return {}



    def find_component(self, keyword):

        result=[]

        architecture = (
            self.brain
            .get("architecture",{})
        )


        for name,files in architecture.items():

            for f in files:

                if keyword in f.lower():

                    result.append(
                        f
                    )


        return result



    def analyze_logs(self):

        data = self.load_json(
            "log_analysis.json"
        )


        errors = data.get(
            "errors",
            []
        )


        for error in errors:


            signature = error.get(
                "signature"
            )


            if signature == "telegram_invalid_token":


                problem = (
                    "Telegram authentication failure"
                )


                decision = {


                    "problem":
                        problem,


                    "severity":
                        "warning",


                    "category":
                        "configuration_error",


                    "root_cause":
                        "Invalid Telegram bot token",


                    "affected_components":
                        [
                            "telegram",
                            "configuration"
                        ],


                    "related_modules":
                        self.find_component(
                            "telegram"
                        ),


                    "action_plan":
                        [
                            "Check TELEGRAM_BOT_TOKEN",
                            "Validate Telegram token",
                            "Restart Telegram Agent"
                        ],


                    "confidence":
                        error.get(
                            "confidence",
                            0.95
                        )

                }


                decision["memory"] = self.remember(

                    problem,

                    "configuration_error",

                    "Invalid Telegram bot token",

                    "Update TELEGRAM_BOT_TOKEN"

                )


                self.report["decisions"].append(
                    decision
                )



    def analyze_health(self):

        data = self.load_json(
            "health_report.json"
        )


        if data.get(
            "health_status"
        ) == "healthy":


            self.report["decisions"].append(

                {

                    "problem":
                        "System healthy",

                    "severity":
                        "info",

                    "category":
                        "system_health",

                    "action_plan":
                        [
                            "Continue monitoring"
                        ],

                    "confidence":
                        1.0

                }

            )



    def analyze(self):

        self.analyze_logs()

        self.analyze_health()

        self.save_report()

        return self.report



if __name__ == "__main__":

    engine = DecisionEngine()

    result = engine.analyze()

    print(
        json.dumps(
            result,
            indent=4
        )
    )
