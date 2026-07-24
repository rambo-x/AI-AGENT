"""
Approval Controller

Approve or reject recovery actions.

Protect approval lifecycle.
"""

from datetime import datetime

from ai.storage.storage import Storage



class ApprovalController:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(root)



    def load(self):

        return self.storage.load(
            "approval_requests.json",
            {
                "requests":[]
            }
        )



    def save(
        self,
        data
    ):

        self.storage.save(
            "approval_requests.json",
            data
        )



    def approve(
        self,
        request_id,
        user="admin"
    ):

        data = self.load()


        for request in data["requests"]:


            if request["id"] == request_id:


                current_status = request.get(
                    "status"
                )


                if current_status == "executed":

                    return {

                        "error":
                            "Request already executed"

                    }



                if current_status == "approved":

                    return {

                        "message":
                            "Request already approved",

                        "request":
                            request

                    }



                request["status"] = "approved"


                request["approved_by"] = user


                request["approved_at"] = (
                    datetime.now().isoformat()
                )


                self.save(
                    data
                )


                return request



        return {

            "error":
                "approval request not found"

        }




    def reject(
        self,
        request_id,
        user="admin"
    ):

        data = self.load()


        for request in data["requests"]:


            if request["id"] == request_id:


                if request.get("status") == "executed":

                    return {

                        "error":
                            "Executed request cannot be rejected"

                    }



                request["status"] = "rejected"


                request["approved_by"] = user


                request["approved_at"] = (
                    datetime.now().isoformat()
                )


                self.save(
                    data
                )


                return request



        return {

            "error":
                "approval request not found"

        }





if __name__ == "__main__":


    controller = ApprovalController()


    print(

        controller.approve(

            "bf1b108b-94a8-4ada-9925-486f80e18ffc"

        )

    )
