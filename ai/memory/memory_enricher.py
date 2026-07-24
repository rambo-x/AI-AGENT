import json
from pathlib import Path
from datetime import datetime

from ai.memory.memory_normalizer import MemoryNormalizer
from ai.memory.feedback import MemoryFeedback


class MemoryEnricher:

    def __init__(self, root="."):

        self.root = Path(root)

        self.normalizer = MemoryNormalizer()

        self.memory = MemoryFeedback()


    def load_decisions(self):

        path = (
            self.root /
            "database/decision_report.json"
        )

        if not path.exists():
            return []

        try:

            data = json.loads(
                path.read_text()
            )

            return data.get(
                "decisions",
                []
            )

        except Exception:

            return []


    def enrich(self, decision):

        problem = decision.get(
            "problem",
            "unknown_problem"
        )


        normalized_problem = (
            self.normalizer.normalize(
                problem
            )
        )


        memory_result = self.memory.save(
            {
                "problem": normalized_problem,

                "category":
                    decision.get(
                        "category",
                        "unknown"
                    ),

                "cause":
                    decision.get(
                        "root_cause",
                        ""
                    ),

                "solution":
                    decision.get(
                        "recommendation",
                        []
                    )[0]
                    if decision.get(
                        "recommendation"
                    )
                    else ""
            }
        )


        return {

            "problem":
                problem,

            "normalized_problem":
                normalized_problem,

            "category":
                decision.get(
                    "category"
                ),

            "confidence":
                decision.get(
                    "confidence",
                    0
                ),

            "recommendation":
                decision.get(
                    "recommendation",
                    []
                ),

            "memory":
                memory_result

        }


    def analyze(self):

        decisions = self.load_decisions()

        enriched = []


        for decision in decisions:

            enriched.append(
                self.enrich(
                    decision
                )
            )


        return {

            "generated_at":
                datetime.now().isoformat(),

            "status":
                "completed",

            "decisions":
                enriched

        }



    def save(self):

        result = self.analyze()


        output = (
            self.root /
            "database/memory_enriched_report.json"
        )


        output.write_text(

            json.dumps(
                result,
                indent=4
            )

        )


        return str(output)
