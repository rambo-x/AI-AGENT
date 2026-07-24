"""
TripleSide AI Agent
Reasoning Engine v1

Layer sebelum Executor.

Flow:

Decision Report
        |
        v
Reasoning Engine
        |
        v
Action Plan
        |
        v
Executor (future)

Engine ini TIDAK melakukan perubahan server.
Hanya membuat keputusan aman.
"""


import json
from pathlib import Path
from datetime import datetime


DATABASE = Path("database")


class ReasoningEngine:


    def __init__(self):

        self.decisions = self.load_json(
            "decision_report.json"
        )

        self.memory = self.load_json(
            "memory.json"
        )

        self.report = {

            "generated_at":
                datetime.now().isoformat(),

            "system":
                "TripleSide AI Agent",

            "status":
                "analyzing",

            "issues":
                0,

            "plans":
                []

        }



    def load_json(self, filename):

        path = DATABASE / filename


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



    def analyze_problem(self, decision):


        problem = decision.get(
            "problem",
            ""
        )


        severity = decision.get(
            "severity",
            "unknown"
        )


        confidence = decision.get(
            "confidence",
            0
        )


        plan = {


            "issue":
                problem,


            "severity":
                severity,


            "analysis":
                {},


            "recommended_action":
                "",


            "auto_execute":
                False,


            "confidence":
                confidence

        }



        if "Telegram" in problem:


            plan["analysis"] = {

                "check":

                    [

                        "TELEGRAM_BOT_TOKEN",

                        "telegram_runner process",

                        "Telegram logs"

                    ]

            }


            plan["recommended_action"] = (

                "Validate Telegram configuration "
                "and confirm bot process status"

            )


            # sengaja false
            # agar AI belum mengubah server

            plan["auto_execute"] = False



        elif "healthy" in problem.lower():


            plan["analysis"] = {

                "check":

                    [

                        "system status",

                        "runtime state"

                    ]

            }


            plan["recommended_action"] = (

                "Continue monitoring"

            )


            plan["auto_execute"] = False



        else:


            plan["recommended_action"] = (

                "Manual investigation required"

            )



        return plan



    def run(self):


        decisions = self.decisions.get(
            "decisions",
            []
        )


        for decision in decisions:


            plan = self.analyze_problem(
                decision
            )


            self.report["plans"].append(
                plan
            )


        self.report["issues"] = len(
            self.report["plans"]
        )


        self.report["status"] = (
            "completed"
        )


        self.save()


        return self.report



    def save(self):

        output = (
            DATABASE /
            "reasoning_report.json"
        )


        output.write_text(

            json.dumps(

                self.report,

                indent=4

            ),

            encoding="utf-8"

        )


        print(
            "Reasoning report saved:",
            output
        )



if __name__ == "__main__":


    engine = ReasoningEngine()


    result = engine.run()


    print()

    print(
        json.dumps(
            result,
            indent=4
        )
    )
