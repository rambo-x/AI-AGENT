"""
Approval Executor

Execute approved recovery actions.

Version 2:
- Execute approved actions
- Save execution result
- Feed incident memory
"""

from datetime import datetime

from ai.storage.storage import Storage
from ai.executor.action_engine import ActionEngine
from ai.memory.incident_memory import IncidentMemory



class ApprovalExecutor:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(root)

        self.action_engine = ActionEngine(root)

        self.memory = IncidentMemory(root)



    def load_requests(self):

        return self.storage.load(
            "approval_requests.json",
            {
                "requests":[]
            }
        )



    def save_requests(
        self,
        data
    ):

        self.storage.save(
            "approval_requests.json",
            data
        )



    def execute(
        self,
        request_id
    ):


        data = self.load_requests()


        for request in data["requests"]:


            if request["id"] == request_id:


                status = request.get(
                    "status"
                )


                if status != "approved":

                    return {

                        "status":
                            "blocked",

                        "message":
                            f"Request status is {status}"

                    }



                result = self.action_engine.execute(
                    request["action"]
                )



                request["status"] = "executed"


                request["execution"] = result


                request["executed_at"] = (
                    datetime.now().isoformat()
                )



                self.save_requests(
                    data
                )



                #
                # Save learning memory
                #

                self.memory.add_incident(

                    problem=request.get(
                        "problem",
                        "unknown"
                    ),

                    decision=request.get(
                        "action",
                        "unknown"
                    ),

                    action=request.get(
                        "action",
                        "unknown"
                    ),

                    result=result.get(
                        "status",
                        "unknown"
                    )

                )



                return {

                    "timestamp":
                        datetime.now().isoformat(),

                    "request":
                        request,

                    "execution":
                        result

                }



        return {

            "error":
                "Request not found"

        }




if __name__ == "__main__":


    executor = ApprovalExecutor()


    print(

        executor.execute(

            "9b4dc7e3-5b36-4d23-9c9b-2576fe1860c3"

        )

    )
