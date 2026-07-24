"""
Executor Engine

Executes recovery plans.

Version 1:
Simulation only (safe mode).
"""

from datetime import datetime

from ai.storage.storage import Storage
from ai.planner.planner_engine import PlannerEngine


DEFAULT_EXECUTION = {
    "created_at": datetime.now().isoformat(),
    "executions": []
}


class ExecutorEngine:

    def __init__(self, root="."):

        self.storage = Storage(root)

        self.planner = PlannerEngine(root)

        if not self.storage.exists(
            "executions.json"
        ):
            self.storage.save(
                "executions.json",
                DEFAULT_EXECUTION
            )


    def load(self):

        return self.storage.load(
            "executions.json",
            DEFAULT_EXECUTION
        )


    def save_database(
        self,
        data
    ):

        self.storage.save(
            "executions.json",
            data
        )


    def execute(
        self,
        problem
    ):

        plan = self.planner.plan(
            problem
        )

        actions = []

        for step in plan["steps"]:

            actions.append({

                "step": step,

                "status": "pending"

            })

        execution = {

            "timestamp":
                datetime.now().isoformat(),

            "problem":
                plan["problem"],

            "status":
                "simulated",

            "priority":
                plan["priority"],

            "estimated_time":
                plan["estimated_time"],

            "actions":
                actions

        }

        data = self.load()

        data["executions"].append(
            execution
        )

        self.save_database(
            data
        )

        return execution


    def history(self):

        return self.load().get(
            "executions",
            []
        )


if __name__ == "__main__":

    executor = ExecutorEngine()

    print(

        executor.execute(
            "Telegram authentication failure"
        )

    )
