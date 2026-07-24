"""
Experience Engine

Stores execution experience and calculates statistics.
Uses Storage Layer and Normalization Engine.
"""

from datetime import datetime

from ai.storage.storage import Storage
from ai.normalization.manager import NormalizationManager


DEFAULT_EXPERIENCE = {
    "created_at": datetime.now().isoformat(),
    "experiences": []
}


class ExperienceEngine:

    def __init__(self, root="."):

        self.storage = Storage(root)

        self.normalizer = NormalizationManager(root)

        if not self.storage.exists(
            "experience.json"
        ):
            self.storage.save(
                "experience.json",
                DEFAULT_EXPERIENCE
            )

    def load(self):

        return self.storage.load(
            "experience.json",
            DEFAULT_EXPERIENCE
        )

    def save_database(
        self,
        data
    ):

        self.storage.save(
            "experience.json",
            data
        )

    def normalize(
        self,
        problem
    ):

        return self.normalizer.normalize(
            problem
        )

    def record(
        self,
        problem,
        solution,
        result
    ):

        normalized = self.normalize(
            problem
        )

        data = self.load()

        entry = {

            "timestamp":
                datetime.now().isoformat(),

            "problem":
                normalized,

            "solution":
                solution,

            "result":
                result,

            "confidence":
                1.0 if result == "success"
                else 0.0

        }

        data["experiences"].append(
            entry
        )

        self.save_database(
            data
        )

        return entry

    def history(
        self,
        problem=None
    ):

        history = self.load().get(
            "experiences",
            []
        )

        if problem is None:
            return history

        normalized = self.normalize(
            problem
        )

        return [

            item

            for item in history

            if item.get(
                "problem"
            ) == normalized

        ]

    def statistics(
        self,
        problem
    ):

        history = self.history(
            problem
        )

        total = len(
            history
        )

        success = len(

            [

                item

                for item in history

                if item.get(
                    "result"
                ) == "success"

            ]

        )

        failed = total - success

        rate = (

            success / total

            if total

            else 0

        )

        return {

            "problem":
                self.normalize(
                    problem
                ),

            "total":
                total,

            "success":
                success,

            "failed":
                failed,

            "success_rate":
                round(
                    rate,
                    2
                )

        }

    def save(self):

        self.save_database(
            self.load()
        )

        return "database/experience.json"


if __name__ == "__main__":

    engine = ExperienceEngine()

    print(
        engine.statistics(
            "telegram_token"
        )
    )
