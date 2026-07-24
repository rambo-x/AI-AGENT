"""
Telegram Bot Interface

Read-only interface for AI Agent.
"""

import json
from pathlib import Path
from datetime import datetime


REPORT_FILE = Path(
    "database/final_report.json"
)

STATE_FILE = Path(
    "database/agent_state.json"
)


class TelegramBotEngine:


    def __init__(self):

        pass



    def load_json(
        self,
        file
    ):

        if not file.exists():

            return {}

        with open(
            file,
            "r"
        ) as f:

            return json.load(f)



    def get_status(self):

        state = self.load_json(
            STATE_FILE
        )


        return {

            "time":
                datetime.now().isoformat(),

            "status":
                state.get(
                    "status",
                    "unknown"
                ),

            "issues":
                state.get(
                    "total_issues",
                    0
                ),

            "last_problem":
                state.get(
                    "last_problem",
                    "-"
                )

        }



    def get_report(self):

        report = self.load_json(
            REPORT_FILE
        )

        return report



    def handle_command(
        self,
        command
    ):

        command = command.lower().strip()


        if command == "/status":

            return self.get_status()



        if command == "/report":

            return self.get_report()



        if command == "/help":

            return {

                "commands":[

                    "/status",
                    "/report",
                    "/help"

                ]

            }



        return {

            "message":
                "Unknown command"

        }
