import json
from pathlib import Path
from datetime import datetime


class ImprovementEngine:

    def __init__(self, root="."):
        self.root = Path(root)

        self.output = (
            self.root /
            "database/learning_history.json"
        )


    def load_memory(self):

        path = (
            self.root /
            "database/diagnostic_memory.json"
        )

        if not path.exists():
            return {
                "cases": []
            }

        try:
            return json.loads(
                path.read_text()
            )

        except Exception:
            return {
                "cases": []
            }



    def analyze_learning(self):

        memory = self.load_memory()

        cases = memory.get(
            "cases",
            []
        )


        improvements = []


        for case in cases:

            improvements.append(

                {
                    "problem":
                        case.get(
                            "problem"
                        ),

                    "category":
                        case.get(
                            "category"
                        ),

                    "known_solution":
                        case.get(
                            "solution"
                        ),

                    "learning_status":
                        "learned",

                    "confidence":
                        1.0
                }

            )


        return {

            "generated_at":
                datetime.now().isoformat(),

            "status":
                "completed",

            "total_learning":
                len(improvements),

            "knowledge_updates":
                improvements
        }



    def save(self):

        result = self.analyze_learning()


        self.output.write_text(

            json.dumps(
                result,
                indent=4
            )

        )


        return str(self.output)
