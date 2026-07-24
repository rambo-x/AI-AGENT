"""
Recovery Engine

Convert detected issues into approved action requests.

Version 4:
- Uses Action ID registry
- Approval aware
- Incident memory integration
- Pattern memory recommendation
"""

from datetime import datetime

from ai.executor.action_engine import ActionEngine
from ai.approval.approval_engine import ApprovalEngine
from ai.memory.incident_memory import IncidentMemory
from ai.memory.pattern_memory import PatternMemory



class RecoveryEngine:


    def __init__(
        self,
        root="."
    ):

        self.action_engine = ActionEngine(root)

        self.approval_engine = ApprovalEngine(root)

        self.memory = IncidentMemory(root)

        self.pattern_memory = PatternMemory(root)



    def get_pattern_recommendation(
        self,
        problem
    ):

        try:

            patterns = self.pattern_memory.analyze()


            for pattern in patterns:


                stored_problem = pattern.get(
                    "pattern",
                    ""
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



    def decide(
        self,
        issue
    ):


        problem = issue.get(

            "issue",

            issue.get(

                "problem",

                "unknown"

            )

        )


        previous = self.memory.find_similar(
            problem
        )


        pattern = self.get_pattern_recommendation(
            problem
        )


        memory_info = {

            "previous_incidents":
                len(previous),

            "found":
                len(previous) > 0,

            "pattern":
                pattern

        }



        action_id = None



        #
        # 1. Use learned pattern first
        #

        if pattern.get("found"):


            confidence = pattern.get(
                "confidence",
                0
            )


            recommended = pattern.get(
                "recommended_action"
            )


            if (
                recommended
                and
                confidence >= 0.8
            ):

                action_id = recommended




        #
        # 2. Fallback rules
        #

        if not action_id:


            problem_lower = problem.lower()



            if "backend" in problem_lower:


                action_id = (
                    "check_backend_logs"
                )



            elif "telegram" in problem_lower:


                action_id = (
                    "check_telegram_config"
                )



            elif "ai-agent" in problem_lower:


                action_id = (
                    "pm2_restart_ai_agent"
                )



        if not action_id:


            return {

                "timestamp":
                    datetime.now().isoformat(),

                "problem":
                    problem,

                "memory":
                    memory_info,

                "status":
                    "no_action",

                "message":
                    "No recovery action available"

            }




        action_definition = (

            self.action_engine.get_action_definition(

                action_id

            )

        )



        if not action_definition:


            return {

                "timestamp":
                    datetime.now().isoformat(),

                "problem":
                    problem,

                "action_id":
                    action_id,

                "memory":
                    memory_info,

                "status":
                    "blocked",

                "message":
                    "Action not registered"

            }




        if action_definition.get(

            "require_approval",

            False

        ):



            approval = self.approval_engine.create_request(

                problem,

                action_id

            )



            return {


                "timestamp":
                    datetime.now().isoformat(),


                "problem":
                    problem,


                "action_id":
                    action_id,


                "memory":
                    memory_info,


                "status":
                    "waiting_approval",


                "approval":
                    approval,


                "execution":
                    {

                        "status":
                            "waiting_approval",

                        "message":
                            "Action requires admin approval"

                    }

            }



        return {


            "timestamp":
                datetime.now().isoformat(),


            "problem":
                problem,


            "action_id":
                action_id,


            "memory":
                memory_info,


            "status":
                "ready",


            "execution":
                {

                    "status":
                        "ready"

                }

        }




if __name__ == "__main__":


    engine = RecoveryEngine()


    result = engine.decide(

        {

            "problem":
                "tripleside-ai-agent crash"

        }

    )


    print(result)
