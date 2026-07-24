import json
from pathlib import Path
from datetime import datetime


class StateManager:

    def __init__(self, root="."):

        self.root = Path(root)

        self.state_file = (
            self.root /
            "database/agent_state.json"
        )


    def load(self):

        if not self.state_file.exists():

            return {}

        try:

            return json.loads(
                self.state_file.read_text()
            )

        except Exception:

            return {}



    def update(self, data):

        state = self.load()

        state.update(data)

        state["updated_at"] = (
            datetime.now().isoformat()
        )


        self.state_file.write_text(

            json.dumps(
                state,
                indent=4
            )

        )


        return state



    def generate_from_reports(self):

        final_report = (
            self.root /
            "database/final_report.json"
        )

        learning = (
            self.root /
            "database/learning_history.json"
        )


        issues = 0
        learned = 0
        last_problem = None


        if final_report.exists():

            data = json.loads(
                final_report.read_text()
            )

            issues = (
                data.get(
                    "summary",
                    {}
                )
                .get(
                    "total_issues",
                    0
                )
            )


            items = data.get(
                "issues",
                []
            )


            if items:

                last_problem = items[-1].get(
                    "problem"
                )


        if learning.exists():

            data = json.loads(
                learning.read_text()
            )

            learned = data.get(
                "total_learning",
                0
            )


        status = "healthy"

        if issues > 0:

            status = "warning"


        return self.update(

            {

                "status": status,

                "last_scan":
                    datetime.now().isoformat(),

                "total_issues":
                    issues,

                "learned_cases":
                    learned,

                "last_problem":
                    last_problem

            }

        )



    def save(self):

        return self.generate_from_reports()
