import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:

    def __init__(self, root="."):

        self.root = Path(root)


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



    def generate(self):

        decision = self.load_json(
            "decision_report.json"
        )

        reasoning = self.load_json(
            "reasoning_report.json"
        )

        health = self.load_json(
            "health_report.json"
        )


        issues = []


        for item in decision.get(
            "decisions",
            []
        ):

            if item.get(
                "category"
            ) != "system_health":

                issues.append(

                    {

                        "problem":
                            item.get(
                                "problem"
                            ),

                        "category":
                            item.get(
                                "category"
                            ),

                        "root_cause":
                            item.get(
                                "root_cause",
                                ""
                            ),

                        "confidence":
                            item.get(
                                "confidence",
                                0
                            ),

                        "recommendation":
                            item.get(
                                "recommendation",
                                []
                            )

                    }

                )



        system_status = "UNKNOWN"


        if health.get(
            "health_status"
        ) == "healthy":

            system_status = "HEALTHY"



        report = {

            "generated_at":
                datetime.now().isoformat(),

            "status":
                "completed",

            "system_status":
                system_status,

            "summary":
                {
                    "total_issues":
                        len(issues)
                },

            "issues":
                issues,

            "reasoning_summary":
                {

                    "architecture":
                        reasoning.get(
                            "architecture",
                            "unknown"
                        ),

                    "status":
                        reasoning.get(
                            "status",
                            "unknown"
                        )

                }

        }


        return report



    def save(self):

        result = self.generate()


        output = (
            self.root /
            "database/final_report.json"
        )


        output.write_text(

            json.dumps(
                result,
                indent=4
            )

        )


        return str(output)



if __name__ == "__main__":

    report = ReportGenerator()

    print(
        report.save()
    )
