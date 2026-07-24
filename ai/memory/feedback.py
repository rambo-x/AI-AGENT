"""
Memory Feedback

Long term diagnostic memory storage.
Stores previous problems and retrieves known solutions.
"""

import json
from datetime import datetime
from pathlib import Path

from ai.memory.memory_normalizer import MemoryNormalizer


MEMORY_FILE = Path(
    "database/diagnostic_memory.json"
)


class MemoryFeedback:

    def __init__(self):

        self.normalizer = MemoryNormalizer()

        self.ensure_storage()


    def ensure_storage(self):

        if not MEMORY_FILE.exists():

            MEMORY_FILE.parent.mkdir(
                exist_ok=True
            )

            with open(
                MEMORY_FILE,
                "w"
            ) as file:

                json.dump(
                    {
                        "created_at":
                            datetime.now().isoformat(),

                        "cases": []
                    },
                    file,
                    indent=4
                )


    def load(self):

        with open(
            MEMORY_FILE,
            "r"
        ) as file:

            return json.load(file)


    def save_case(
        self,
        problem,
        category=None,
        cause=None,
        solution=None
    ):

        normalized = self.normalizer.normalize(
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


        with open(
            MEMORY_FILE,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )


        return case



    def search(
        self,
        problem
    ):

        normalized = self.normalizer.normalize(
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
                    self.normalizer.normalize(problem),

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
