"""
Memory Enricher

Connects Decision Engine output with Diagnostic Memory.
Uses MemoryNormalizer so similar problems are recognized.
"""

from datetime import datetime

from ai.memory.memory_normalizer import MemoryNormalizer
from ai.memory.feedback import MemoryFeedback


class MemoryEnricher:

    def __init__(self):
        self.normalizer = MemoryNormalizer()
        self.memory = MemoryFeedback()


    def enrich(self, decision):

        problem = decision.get(
            "problem",
            "unknown_problem"
        )

        normalized_problem = self.normalizer.normalize(
            problem
        )

        memory_result = self.memory.save(
            {
                "problem": normalized_problem
            }
        )

        return {
            "problem": problem,
            "normalized_problem": normalized_problem,
            "category": decision.get(
                "category"
            ),
            "confidence": decision.get(
                "confidence",
                0
            ),
            "recommendation": decision.get(
                "recommendation",
                []
            ),
            "memory": memory_result
        }


    def load_decisions(self):

        try:
            import json

            with open(
                "database/decision_report.json",
                "r"
            ) as file:

                data = json.load(file)

                return data.get(
                    "decisions",
                    []
                )

        except Exception:

            return []


    def save(self):

        import json

        decisions = self.load_decisions()

        enriched = []

        for decision in decisions:

            enriched.append(
                self.enrich(
                    decision
                )
            )


        report = {
            "generated_at":
                datetime.now().isoformat(),

            "status":
                "completed",

            "decisions":
                enriched
        }


        with open(
            "database/memory_enriched_report.json",
            "w"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )


        return (
            "database/memory_enriched_report.json"
        )


if __name__ == "__main__":

    memory = MemoryEnricher()

    print(
        memory.save()
    )
