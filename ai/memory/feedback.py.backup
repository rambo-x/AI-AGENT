"""
Memory Feedback

Long term diagnostic memory.
Uses Storage Layer and Normalization Engine.
"""

from datetime import datetime

from ai.storage.storage import Storage
from ai.normalization.manager import NormalizationManager


DEFAULT_MEMORY = {
    "created_at": datetime.now().isoformat(),
    "cases": []
}


class MemoryFeedback:

    def __init__(self, root="."):

        self.storage = Storage(root)

        self.normalizer = NormalizationManager(root)

        if not self.storage.exists(
            "diagnostic_memory.json"
        ):
            self.storage.save(
                "diagnostic_memory.json",
                DEFAULT_MEMORY
            )


    def load(self):

        return self.storage.load(
            "diagnostic_memory.json",
            DEFAULT_MEMORY
        )


    def save_database(
        self,
        data
    ):

        self.storage.save(
            "diagnostic_memory.json",
            data
        )


    def normalize(
        self,
        problem
    ):

        return self.normalizer.normalize(
            problem
        )


    def search(
        self,
        problem
    ):

        normalized = self.normalize(
            problem
        )

        data = self.load()

        matches = []

        for case in data.get(
            "cases",
            []
        ):

            if case.get(
                "problem"
            ) == normalized:

                matches.append(
                    case
                )

        return matches


    def save_case(
        self,
        problem,
        category=None,
        cause=None,
        solution=None
    ):

        normalized = self.normalize(
            problem
        )

        data = self.load()

        case = {

            "timestamp":
                datetime.now().isoformat(),

            "problem":
                normalized,

            "category":
                category,

            "cause":
                cause,

            "solution":
                solution

        }

        data["cases"].append(
            case
        )

        self.save_database(
            data
        )

        return case


    def save(
        self,
        problem_data
    ):

        problem = problem_data.get(
            "problem",
            "unknown_problem"
        )

        category = problem_data.get(
            "category"
        )

        cause = problem_data.get(
            "cause"
        )

        solution = problem_data.get(
            "solution"
        )

        existing = self.search(
            problem
        )

        if existing:

            return {

                "problem":
                    self.normalize(
                        problem
                    ),

                "previous_cases_found":
                    len(existing),

                "previous_cases":
                    existing,

                "memory_status":
                    "known_problem"
            }

        case = self.save_case(
            problem,
            category,
            cause,
            solution
        )

        return {

            "problem":
                case["problem"],

            "previous_cases_found":
                0,

            "previous_cases":
                [],

            "memory_status":
                "new_problem"
        }


    def all_cases(self):

        return self.load().get(
            "cases",
            []
        )


    def statistics(self):

        cases = self.all_cases()

        return {

            "total_cases":
                len(cases),

            "known_problems":

                len(

                    set(

                        case["problem"]

                        for case in cases

                    )

                )

        }


if __name__ == "__main__":

    memory = MemoryFeedback()

    print(
        memory.statistics()
    )
