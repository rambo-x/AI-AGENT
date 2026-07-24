"""
Recovery Engine

Convert detected issues into approved action requests.

Version 3:
- Uses Action ID registry
- Approval aware
- Incident memory integration
"""

from datetime import datetime

from ai.executor.action_engine import ActionEngine
from ai.approval.approval_engine import ApprovalEngine
from ai.memory.incident_memory import IncidentMemory



class RecoveryEngine:


    def __init__(
        self,
        root="."
    ):

        self.action_engine = ActionEngine(root)

        self.approval_engine = ApprovalEngine(root)

        self.memory = IncidentMemory(root)



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



        memory_info = {

            "previous_incidents":
                len(previous),

            "found":
                len(previous) > 0

        }



        action_id = None


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



        else:


            action_id = None





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
