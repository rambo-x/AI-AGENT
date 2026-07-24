"""
Approval Executor

Execute approved recovery actions.
"""

from datetime import datetime

from ai.storage.storage import Storage
from ai.executor.action_engine import ActionEngine



class ApprovalExecutor:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(root)

        self.action_engine = ActionEngine(root)



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

            "bf1b108b-94a8-4ada-9925-486f80e18ffc"

        )

    )
