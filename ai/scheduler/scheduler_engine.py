"""
Scheduler Engine

Runs AI Agent pipeline automatically.
"""

import time
from datetime import datetime

from ai.core.orchestrator import AgentOrchestrator


class SchedulerEngine:


    def __init__(
        self,
        interval=3600
    ):

        self.interval = interval

        self.running = False



    def run_once(self):

        print(
            f"[{datetime.now()}] Starting AI scan..."
        )


        agent = AgentOrchestrator()

        result = agent.save()


        print(
            f"[{datetime.now()}] Report saved: {result}"
        )


        return result



    def start(self):

        self.running = True


        print(
            "AI Scheduler started"
        )


        while self.running:


            try:

                self.run_once()


            except Exception as error:

                print(
                    "Scheduler error:",
                    error
                )


            time.sleep(
                self.interval
            )



    def stop(self):

        self.running = False


if __name__ == "__main__":


    scheduler = SchedulerEngine(
        interval=60
    )


    scheduler.start()
