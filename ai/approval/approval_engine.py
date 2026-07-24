"""
Approval Engine

Human approval gateway
before executing recovery actions.

Version 2:
Action ID based approval system.
"""


from datetime import datetime
import uuid

from ai.storage.storage import Storage



DEFAULT_APPROVAL = {

    "created_at":
        datetime.now().isoformat(),

    "requests":[]

}



class ApprovalEngine:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(root)


        if not self.storage.exists(
            "approval_requests.json"
        ):

            self.storage.save(
                "approval_requests.json",
                DEFAULT_APPROVAL
            )



    def load(self):

        return self.storage.load(

            "approval_requests.json",

            DEFAULT_APPROVAL

        )



    def save(
        self,
        data
    ):

        self.storage.save(

            "approval_requests.json",

            data

        )



    def normalize_action(
        self,
        action
    ):


        mapping = {


            "pm2 restart tripleside-ai-agent":

                "pm2_restart_ai_agent",


            "pm2_restart_ai_agent":

                "pm2_restart_ai_agent",



            "Check TELEGRAM_BOT_TOKEN":

                "check_telegram_token"


        }


        return mapping.get(
            action,
            action
        )



    def create_request(
        self,
        problem,
        action
    ):


        action_id = self.normalize_action(
            action
        )


        request = {


            "id":

                str(uuid.uuid4()),



            "created_at":

                datetime.now().isoformat(),



            "problem":

                problem,



            "action":

                action_id,



            "status":

                "pending",



            "approved_by":

                None,



            "approved_at":

                None



        }



        data = self.load()


        data["requests"].append(
            request
        )


        self.save(
            data
        )


        return request



    def approve(
        self,
        request_id,
        user="admin"
    ):


        data = self.load()


        for request in data["requests"]:


            if request["id"] == request_id:


                request["status"] = "approved"


                request["approved_by"] = user


                request["approved_at"] = (
                    datetime.now().isoformat()
                )


                self.save(
                    data
                )


                return request



        return None



if __name__ == "__main__":


    engine = ApprovalEngine()


    result = engine.create_request(

        "tripleside-ai-agent crash",

        "pm2_restart_ai_agent"

    )


    print(result)
