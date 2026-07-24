"""
Action Policy

Controls allowed AI recovery actions.

Safe mode:
- validate only
- no dangerous execution
"""


from datetime import datetime



ACTION_POLICY = {


    "pm2_restart_ai_agent": {

        "command":
            "pm2 restart tripleside-ai-agent",

        "risk":
            "medium",

        "require_approval":
            True,

        "allowed":
            True

    },


    "pm2_backend_logs": {

        "command":
            "pm2 logs triplesidestudio-backend",

        "risk":
            "low",

        "require_approval":
            False,

        "allowed":
            True

    },


    "check_telegram_token": {

        "command":
            "Check TELEGRAM_BOT_TOKEN",

        "risk":
            "low",

        "require_approval":
            False,

        "allowed":
            True

    }


}



class ActionPolicy:



    def get_action(
        self,
        action_id
    ):

        return ACTION_POLICY.get(
            action_id
        )



    def validate(
        self,
        action_id
    ):


        action = self.get_action(
            action_id
        )


        if not action:


            return {

                "allowed":
                    False,

                "reason":
                    "Unknown action"

            }



        if not action["allowed"]:


            return {

                "allowed":
                    False,

                "reason":
                    "Action blocked"

            }



        return {

            "allowed":
                True,

            "action":
                action,

            "checked_at":
                datetime.now().isoformat()

        }



if __name__ == "__main__":


    policy = ActionPolicy()


    print(
        policy.validate(
            "pm2_restart_ai_agent"
        )
    )


    print(
        policy.validate(
            "delete_database"
        )
    )
