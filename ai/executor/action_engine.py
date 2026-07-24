"""
Action Engine

Executes approved recovery actions.

Version 2:
- Environment controlled execution mode
- Safe / Approval / Active mode
- Whitelist based
- No destructive execution
"""

from datetime import datetime

from ai.storage.storage import Storage
from config import AI_AGENT_MODE


DEFAULT_ACTION_LOG = {
    "created_at": datetime.now().isoformat(),
    "actions": []
}


# Allowed actions registry
# Future real execution will only happen here
ALLOWED_ACTIONS = {

    "pm2_restart_ai_agent": {

        "command":
            "pm2 restart tripleside-ai-agent",

        "risk":
            "medium",

        "require_approval":
            True

    },


    "check_backend_logs": {

        "command":
            "pm2 logs triplesidestudio-backend",

        "risk":
            "low",

        "require_approval":
            False

    }

}



class ActionEngine:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(root)


        if not self.storage.exists(
            "action_history.json"
        ):

            self.storage.save(
                "action_history.json",
                DEFAULT_ACTION_LOG
            )



    def load_history(self):

        return self.storage.load(

            "action_history.json",

            DEFAULT_ACTION_LOG

        )



    def save_history(
        self,
        data
    ):

        self.storage.save(

            "action_history.json",

            data

        )



    def get_action_definition(
        self,
        action_id
    ):

        return ALLOWED_ACTIONS.get(
            action_id
        )



    def validate_action(
        self,
        action
    ):


        blocked = [

            "rm -rf",

            "shutdown",

            "reboot",

            "mkfs",

            "format",

            "dd if="

        ]


        action_lower = action.lower()


        for command in blocked:

            if command in action_lower:

                return False


        return True



    def execute(
        self,
        action_id
    ):


        timestamp = datetime.now().isoformat()


        action = self.get_action_definition(
            action_id
        )


        if not action:


            result = {

                "timestamp":
                    timestamp,

                "action_id":
                    action_id,

                "status":
                    "blocked",

                "reason":
                    "Unknown action"

            }


            self.save_result(
                result
            )


            return result



        command = action["command"]



        if not self.validate_action(
            command
        ):


            result = {

                "timestamp":
                    timestamp,

                "action_id":
                    action_id,

                "command":
                    command,

                "status":
                    "blocked",

                "reason":
                    "Unsafe command"

            }


            self.save_result(
                result
            )


            return result



        #
        # SAFE MODE
        #

        if AI_AGENT_MODE == "safe":


            result = {

                "timestamp":
                    timestamp,

                "action_id":
                    action_id,

                "command":
                    command,

                "risk":
                    action["risk"],

                "status":
                    "simulated",

                "message":
                    "Safe mode: execution disabled"

            }



        #
        # APPROVAL MODE
        #

        elif AI_AGENT_MODE == "approval":


            result = {

                "timestamp":
                    timestamp,

                "action_id":
                    action_id,

                "command":
                    command,

                "risk":
                    action["risk"],

                "status":
                    "waiting_approval",

                "message":
                    "Action requires admin approval"

            }



        #
        # ACTIVE MODE
        #

        elif AI_AGENT_MODE == "active":


            result = {

                "timestamp":
                    timestamp,

                "action_id":
                    action_id,

                "command":
                    command,

                "risk":
                    action["risk"],

                "status":
                    "approved",

                "message":
                    "Execution allowed by active mode"

            }



        else:


            result = {

                "timestamp":
                    timestamp,

                "action_id":
                    action_id,

                "status":
                    "blocked",

                "reason":
                    "Invalid AI_AGENT_MODE"

            }



        self.save_result(
            result
        )


        return result



    def save_result(
        self,
        result
    ):

        history = self.load_history()


        history["actions"].append(
            result
        )


        self.save_history(
            history
        )





if __name__ == "__main__":


    engine = ActionEngine()


    print(

        engine.execute(

            "pm2_restart_ai_agent"

        )

    )


    print()


    print(

        engine.execute(

            "unknown_action"

        )

    )
