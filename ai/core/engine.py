"""
TripleSide AI Agent
Runtime Engine v2

Core execution layer.

Flow:

System Brain
      |
Decision Report
      |
Reasoning Engine
      |
Recovery Engine
      |
Action Engine
      |
Runtime State

"""

import json
from pathlib import Path
from datetime import datetime


from ai.recovery.recovery_engine import RecoveryEngine



ROOT = Path(".")

DATABASE = ROOT / "database"



class AIEngine:


    def __init__(self):


        self.brain = self.load_json(
            "system_brain.json"
        )


        self.decisions = self.load_json(
            "decision_report.json"
        )


        self.recovery = RecoveryEngine()


        self.runtime = {


            "generated_at":
                datetime.now().isoformat(),


            "system":
                "TripleSide AI Agent",


            "status":
                "initializing",


            "brain_loaded":
                False,


            "decisions_loaded":
                False,


            "reasoning":
                [],


            "actions":
                []

        }




    def load_json(
        self,
        filename
    ):


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






    def analyze_brain(self):


        if self.brain:


            self.runtime[
                "brain_loaded"
            ] = True



            architecture = self.brain.get(
                "architecture",
                {}
            )



            modules = []



            for key, items in architecture.items():


                modules.append({

                    "layer":
                        key,


                    "modules":
                        len(items)

                })



            self.runtime[
                "reasoning"
            ].append({

                "type":
                    "architecture_analysis",


                "result":
                    modules

            })







    def analyze_decisions(self):


        if self.decisions:


            self.runtime[
                "decisions_loaded"
            ] = True



        decisions = self.decisions.get(
            "decisions",
            []
        )



        for decision in decisions:


            problem = decision.get(
                "problem",
                "unknown"
            )


            severity = decision.get(
                "severity",
                "unknown"
            )



            self.runtime[
                "reasoning"
            ].append({

                "type":
                    "decision_analysis",


                "problem":
                    problem,


                "severity":
                    severity

            })




            #
            # Recovery integration
            #

            if severity in [

                "warning",
                "critical"

            ]:



                recovery = self.recovery.decide(

                    decision

                )



                self.runtime[
                    "actions"
                ].append({


                    "problem":
                        problem,


                    "severity":
                        severity,


                    "recovery_available":
                        True,


                    "recommended_action":
                        recovery[
                            "recommended_action"
                        ],


                    "execution":
                        recovery[
                            "execution"
                        ]


                })




            elif severity == "info":



                self.runtime[
                    "actions"
                ].append({

                    "problem":
                        problem,


                    "action":
                        "monitor"

                })







    def determine_status(self):


        if (

            self.runtime[
                "brain_loaded"
            ]

            and

            self.runtime[
                "decisions_loaded"
            ]

        ):


            self.runtime[
                "status"
            ] = "READY"



        else:


            self.runtime[
                "status"
            ] = "INCOMPLETE"







    def save(self):


        output = (

            DATABASE /

            "runtime_engine.json"

        )


        output.write_text(

            json.dumps(

                self.runtime,

                indent=4

            ),

            encoding="utf-8"

        )






    def run(self):


        self.analyze_brain()

        self.analyze_decisions()

        self.determine_status()

        self.save()


        return self.runtime





if __name__ == "__main__":


    engine = AIEngine()


    result = engine.run()


    print(

        json.dumps(

            result,

            indent=4

        )

    )
