"""
TripleSide AI Agent

Decision Engine v3

Features:
- membaca log_analysis.json
- membaca system_brain.json
- menghubungkan masalah dengan modul terkait
- menyimpan decision_report.json
- belajar melalui MemoryFeedback
- membaca Pattern Memory untuk rekomendasi recovery
"""

import json
from pathlib import Path
from datetime import datetime

from ai.memory.feedback import MemoryFeedback
from ai.memory.pattern_memory import PatternMemory


class DecisionEngine:


    def __init__(
        self,
        root="."
    ):

        self.root = Path(root)

        self.memory = MemoryFeedback(
            root
        )

        self.pattern_memory = PatternMemory(
            root
        )


        self.brain = self.load_json(
            "system_brain.json"
        )


        self.report = {

            "generated_at":
                datetime.now().isoformat(),

            "system":
                "TripleSide AI Agent",

            "status":
                "completed",

            "decisions":
                []

        }



    def load_json(
        self,
        filename
    ):

        path = (
            self.root /
            "database" /
            filename
        )


        if not path.exists():

            return {}


        try:

            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )


        except Exception:

            return {}



    def save_report(
        self
    ):

        path = (
            self.root /
            "database" /
            "decision_report.json"
        )


        path.write_text(
            json.dumps(
                self.report,
                indent=4
            ),
            encoding="utf-8"
        )


        print(
            "Decision report saved:",
            path
        )



    def remember(
        self,
        problem,
        category,
        cause,
        solution
    ):

        try:

            return self.memory.save(
                {
                    "problem":
                        problem,

                    "category":
                        category,

                    "cause":
                        cause,

                    "solution":
                        solution
                }
            )


        except Exception:

            return {

                "memory_status":
                    "failed"

            }




    def get_memory_recommendation(
        self,
        problem
    ):

        try:

            patterns = (
                self.pattern_memory.analyze()
            )


            for pattern in patterns:


                stored_problem = (
                    pattern.get(
                        "pattern",
                        ""
                    )
                )


                if (

                    problem.lower()
                    in stored_problem.lower()

                    or

                    stored_problem.lower()
                    in problem.lower()

                ):


                    return {

                        "found":
                            True,


                        "previous_incidents":
                            pattern.get(
                                "occurrences",
                                0
                            ),


                        "recommended_action":
                            pattern.get(
                                "preferred_action"
                            ),


                        "success_rate":
                            pattern.get(
                                "success_rate",
                                0
                            ),


                        "confidence":
                            pattern.get(
                                "confidence",
                                0
                            )

                    }



            return {

                "found":
                    False

            }



        except Exception as e:


            return {

                "found":
                    False,

                "error":
                    str(e)

            }




    def find_component(
        self,
        keyword
    ):

        result = []


        architecture = (
            self.brain
            .get(
                "architecture",
                {}
            )
        )


        for name, files in architecture.items():


            for file in files:


                if keyword.lower() in file.lower():

                    result.append(
                        file
                    )


        return result




    def analyze_logs(
        self
    ):


        data = self.load_json(
            "log_analysis.json"
        )


        errors = data.get(
            "errors",
            []
        )


        grouped = {}



        for error in errors:


            signature = error.get(
                "signature",
                "unknown"
            )


            if signature not in grouped:


                grouped[signature] = {

                    "count":
                        0,

                    "error":
                        error

                }


            grouped[signature]["count"] += 1




        for signature, item in grouped.items():


            error = item["error"]


            if signature != "telegram_invalid_token":

                continue



            problem = (
                "Telegram authentication failure"
            )


            decision = {


                "problem":
                    problem,


                "severity":
                    "warning",


                "category":
                    "configuration_error",


                "root_cause":
                    "Invalid Telegram bot token",


                "occurrences":
                    item["count"],


                "affected_components":
                    [

                        "telegram",

                        "configuration"

                    ],


                "related_modules":
                    self.find_component(
                        "telegram"
                    )

            }



            decision["memory"] = (
                self.get_memory_recommendation(
                    problem
                )
            )


            self.report["decisions"].append(
                decision
            )



        self.save_report()


        return self.report





if __name__ == "__main__":


    engine = DecisionEngine()


    result = (
        engine.analyze_logs()
    )


    print(
        json.dumps(
            result,
            indent=4
        )
    )
