"""
Incident Memory Engine

Stores previous incidents,
actions and recovery results.

Version 1:
Local JSON memory.
"""

from datetime import datetime
import uuid

from ai.storage.storage import Storage


DEFAULT_MEMORY = {
    "created_at": datetime.now().isoformat(),
    "incidents": []
}


class IncidentMemory:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(root)

        if not self.storage.exists(
            "incident_memory.json"
        ):

            self.storage.save(
                "incident_memory.json",
                DEFAULT_MEMORY
            )


    def load(self):

        return self.storage.load(
            "incident_memory.json",
            DEFAULT_MEMORY
        )


    def save(
        self,
        data
    ):

        self.storage.save(
            "incident_memory.json",
            data
        )


    def add_incident(
        self,
        problem,
        decision,
        action,
        result
    ):

        memory = self.load()


        incident = {

            "id":
                str(uuid.uuid4()),

            "timestamp":
                datetime.now().isoformat(),

            "problem":
                problem,

            "decision":
                decision,

            "action":
                action,

            "result":
                result

        }


        memory["incidents"].append(
            incident
        )


        self.save(
            memory
        )


        return incident



    def find_similar(
        self,
        keyword
    ):

        memory = self.load()


        results = []


        for incident in memory["incidents"]:

            if keyword.lower() in (
                incident["problem"]
                .lower()
            ):

                results.append(
                    incident
                )


        return results



if __name__ == "__main__":


    engine = IncidentMemory()


    print(
        engine.add_incident(
            "tripleside-ai-agent crash",
            "restart service",
            "pm2_restart_ai_agent",
            "recovered"
        )
    )


    print(
        engine.find_similar(
            "crash"
        )
    )
