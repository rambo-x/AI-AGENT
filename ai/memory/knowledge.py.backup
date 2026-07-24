"""
==========================================================
TripleSide AI Agent
Diagnostic Knowledge Layer v1.0
==========================================================

Menyimpan pengalaman diagnosis.

Input:
    diagnostic result

Output:
    database/diagnostic_memory.json

Fungsi:
    - save experience
    - search previous cases
    - load history

Status:
    Development v1.0
"""

import json
from pathlib import Path
from datetime import datetime


class DiagnosticKnowledge:

    def __init__(
        self,
        memory_file="database/diagnostic_memory.json"
    ):

        self.memory_file = Path(memory_file)

        self.memory = self.load()


    # --------------------------------------------------

    def load(self):

        if not self.memory_file.exists():

            return {
                "created_at":
                    datetime.now().isoformat(),

                "cases": []
            }


        with self.memory_file.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    # --------------------------------------------------

    def save_file(self):

        self.memory_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.memory_file.open(
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.memory,
                f,
                indent=4
            )


    # --------------------------------------------------

    def add_case(
        self,
        problem,
        category,
        cause,
        solution
    ):

        case = {

            "timestamp":
                datetime.now().isoformat(),

            "problem":
                problem,

            "category":
                category,

            "cause":
                cause,

            "solution":
                solution
        }


        self.memory["cases"].append(
            case
        )


        self.save_file()


        return case


    # --------------------------------------------------

    def search(
        self,
        keyword
    ):

        keyword = keyword.lower()

        results = []


        for case in self.memory.get(
            "cases",
            []
        ):

            text = json.dumps(
                case
            ).lower()


            if keyword in text:

                results.append(
                    case
                )


        return results


    # --------------------------------------------------

    def all_cases(self):

        return self.memory.get(
            "cases",
            []
        )


# ------------------------------------------------------

if __name__ == "__main__":

    knowledge = DiagnosticKnowledge()


    knowledge.add_case(
        problem="ModuleNotFoundError",
        category="import_error",
        cause="missing dependency",
        solution="install required package"
    )


    print(
        "Knowledge memory created"
    )
