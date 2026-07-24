import json
from pathlib import Path

from ai.memory.feedback import MemoryFeedback
from ai.knowledge.knowledge_base import KnowledgeBase
from ai.memory.memory_normalizer import MemoryNormalizer


class RecommendationEngine:

    def __init__(self, root="."):

        self.root = Path(root)

        self.memory = MemoryFeedback(root)
        self.knowledge = KnowledgeBase(root)
        self.normalizer = MemoryNormalizer()


    def recommend(self, problem):

        normalized = self.normalizer.normalize(problem)

        memory = self.memory.save(
            {
                "problem": normalized
            }
        )

        knowledge = self.knowledge.search(
            normalized
        )

        recommendation = []

        confidence = 0.50

        source = []


        if knowledge:

            recommendation.append(
                knowledge.get(
                    "solution"
                )
            )

            confidence += 0.30

            source.append(
                "knowledge"
            )


        if memory.get(
            "previous_cases_found",
            0
        ) > 0:

            for case in memory.get(
                "previous_cases",
                []
            ):

                solution = case.get(
                    "solution"
                )

                if (
                    solution and
                    solution not in recommendation
                ):

                    recommendation.append(
                        solution
                    )

            confidence += 0.20

            source.append(
                "memory"
            )


        return {

            "problem":
                normalized,

            "recommended_solution":
                recommendation,

            "confidence":
                round(
                    min(confidence, 1.0),
                    2
                ),

            "source":
                source
        }


    def save(self):

        result = self.recommend(
            "Telegram authentication failure"
        )

        output = (
            self.root /
            "database/recommendation_report.json"
        )

        output.write_text(
            json.dumps(
                result,
                indent=4
            )
        )

        return str(output)
