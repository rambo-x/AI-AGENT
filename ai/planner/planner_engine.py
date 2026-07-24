"""
Planner Engine

Creates an execution plan for a detected problem.
"""

from ai.normalization.manager import NormalizationManager
from ai.recommendation.recommendation_engine import RecommendationEngine
from ai.experience.experience_engine import ExperienceEngine

from ai.planner.planner_rules import PLANNER_RULES


class PlannerEngine:

    def __init__(self, root="."):

        self.normalizer = NormalizationManager(root)

        self.recommendation = RecommendationEngine(root)

        self.experience = ExperienceEngine(root)


    def plan(
        self,
        problem
    ):

        signature = self.normalizer.normalize(
            problem
        )

        rule = PLANNER_RULES.get(
            signature,
            {
                "priority": "unknown",
                "estimated_time": "unknown",
                "steps": [
                    "Manual investigation required"
                ],
                "rollback": []
            }
        )

        recommendation = self.recommendation.recommend(
            signature
        )

        statistics = self.experience.statistics(
            signature
        )

        return {

            "problem":
                signature,

            "priority":
                rule["priority"],

            "estimated_time":
                rule["estimated_time"],

            "steps":
                rule["steps"],

            "rollback":
                rule["rollback"],

            "recommendation":
                recommendation,

            "experience":
                statistics

        }


if __name__ == "__main__":

    planner = PlannerEngine()

    print(

        planner.plan(
            "Telegram authentication failure"
        )

    )
