"""
Recovery Engine

Convert detected issues into approved action requests.

Version 2:
- Uses Action ID registry
- Compatible with ActionEngine whitelist
- Approval aware
"""

from datetime import datetime

from ai.executor.action_engine import ActionEngine
from ai.approval.approval_engine import ApprovalEngine



class RecoveryEngine:


    def __init__(
        self,
        root="."
    ):

        self.action_engine = ActionEngine(root)

        self.approval_engine = ApprovalEngine(root)



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


                "status":

                    "blocked",


                "message":

                    "Action not registered"

            }





        #
        # Approval required
        #

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





        #
        # Direct safe action
        #

        execution = self.action_engine.execute(

            action_id

        )



        return {


            "timestamp":

                datetime.now().isoformat(),


            "problem":

                problem,


            "action_id":

                action_id,


            "execution":

                execution

        }





if __name__ == "__main__":


    engine = RecoveryEngine()



    result = engine.decide(

        {

            "problem":

                "tripleside-ai-agent previous crash detected"

        }

    )


    print(result)
