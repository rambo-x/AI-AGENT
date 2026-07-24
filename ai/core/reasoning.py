"""
==========================================================
TripleSide AI Agent
AI Reasoning Layer v1.1
==========================================================

Upgrade:
- component mapping
- better historical search
- evidence generation

Tidak mengubah:
- Diagnostic Engine
- Knowledge Layer
- Dependency Analyzer

"""

import json
from pathlib import Path
from datetime import datetime


class ReasoningEngine:


    COMPONENT_MAP = {

        "runtime_error": [
            "app.py",
            "ai/",
            "database/"
        ],

        "service_failure": [
            "monitor/",
            "scheduler/",
            "events/"
        ],

        "configuration_error": [
            "config.py",
            "notifications/",
            ".env"
        ],

        "import_error": [
            "requirements.txt",
            "ai/",
            "notifications/"
        ]
    }



    KEYWORD_MAP = {

        "runtime_error": [
            "error",
            "exception",
            "traceback"
        ],

        "service_failure": [
            "stopped",
            "failed",
            "service"
        ],

        "configuration_error": [
            "token",
            "config",
            "environment"
        ]
    }



    def __init__(self):

        self.diagnostics = self.load(
            "database/diagnostics.json"
        )

        self.memory = self.load(
            "database/diagnostic_memory.json"
        )

        self.output = Path(
            "database/reasoning_report.json"
        )


    # ------------------------------------------------


    def load(self, filename):

        file = Path(filename)


        if not file.exists():

            return {}


        with file.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    # ------------------------------------------------


    def find_previous_cases(
        self,
        issue
    ):

        results = []


        keywords = []

        keywords.append(
            issue.get(
                "category",
                ""
            )
        )


        keywords.append(
            issue.get(
                "message",
                ""
            )
        )


        keywords.extend(
            issue.get(
                "possible_causes",
                []
            )
        )


        for case in self.memory.get(
            "cases",
            []
        ):

            text = json.dumps(
                case
            ).lower()


            for key in keywords:

                if key.lower() in text:

                    results.append(case)

                    break


        return results



    # ------------------------------------------------


    def find_components(
        self,
        category
    ):

        return self.COMPONENT_MAP.get(
            category,
            []
        )



    # ------------------------------------------------


    def build(self):

        reports = []


        for issue in self.diagnostics.get(
            "issues",
            []
        ):


            category = issue.get(
                "category",
                "unknown"
            )


            report = {


                "problem":
                    issue.get(
                        "message"
                    ),


                "category":
                    category,


                "affected_components":
                    self.find_components(
                        category
                    ),


                "evidence": [

                    issue.get(
                        "message"
                    ),

                    "diagnostic pattern matched"

                ],


                "previous_cases":
                    self.find_previous_cases(
                        issue
                    ),


                "recommendation":
                    issue.get(
                        "possible_causes",
                        []
                    ),


                "confidence":
                    issue.get(
                        "confidence",
                        0
                    )

            }


            reports.append(
                report
            )


        return {

            "generated_at":
                datetime.now().isoformat(),


            "status":
                "completed",


            "diagnoses":
                reports,


            "architecture":
                self.diagnostics.get(
                    "architecture"
                )

        }



    # ------------------------------------------------


    def save(self):

        result = self.build()


        with self.output.open(
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )


        return str(
            self.output
        )



if __name__ == "__main__":

    engine = ReasoningEngine()

    print(
        engine.save()
    )
