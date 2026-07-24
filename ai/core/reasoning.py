import json
from pathlib import Path
from datetime import datetime


class ReasoningEngine:

    def __init__(self, root="."):

        self.root = Path(root)

        self.report = {
            "generated_at": datetime.now().isoformat(),
            "status": "completed",
            "diagnoses": []
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



    def analyze_decisions(self):

        data = self.load_json(
            "decision_report.json"
        )


        decisions = data.get(
            "decisions",
            []
        )


        for item in decisions:

            diagnosis = {

                "problem":
                    item.get(
                        "problem",
                        "unknown"
                    ),

                "category":
                    item.get(
                        "category",
                        "unknown"
                    ),

                "affected_components":
                    item.get(
                        "affected_components",
                        []
                    ),

                "evidence":
                    item.get(
                        "evidence",
                        []
                    ),

                "recommendation":
                    item.get(
                        "recommendation",
                        []
                    ),

                "confidence":
                    item.get(
                        "confidence",
                        0
                    )

            }


            self.report["diagnoses"].append(
                diagnosis
            )



    def analyze_architecture(self):

        data = self.load_json(
            "architecture.json"
        )


        self.report["architecture"] = (
            data.get(
                "architecture_type",
                "unknown"
            )
        )



    def analyze(self):

        self.analyze_decisions()

        self.analyze_architecture()

        return self.report



    def save(self):

        result = self.analyze()


        output = (
            self.root /
            "database/reasoning_report.json"
        )


        output.write_text(

            json.dumps(
                result,
                indent=4
            )

        )


        return str(output)



if __name__ == "__main__":

    engine = ReasoningEngine()

    print(
        engine.save()
    )
