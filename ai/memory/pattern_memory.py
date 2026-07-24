"""
Pattern Memory Engine

Analyze incident history
and detect recurring recovery patterns.
"""

from collections import defaultdict

from ai.memory.incident_memory import IncidentMemory



class PatternMemory:


    def __init__(
        self,
        root="."
    ):

        self.memory = IncidentMemory(root)



    def analyze(
        self
    ):

        incidents = self.memory.load().get(
            "incidents",
            []
        )


        patterns = defaultdict(list)


        for incident in incidents:

            problem = incident.get(
                "problem",
                "unknown"
            )

            patterns[problem].append(
                incident
            )



        result = []


        for problem, items in patterns.items():


            actions = defaultdict(int)

            success = 0


            for item in items:

                action = item.get(
                    "action",
                    "unknown"
                )

                actions[action] += 1


                if item.get(
                    "result"
                ) in [
                    "recovered",
                    "success",
                    "simulated"
                ]:

                    success += 1



            preferred_action = max(
                actions,
                key=actions.get
            )



            confidence = (
                success / len(items)
            )



            result.append({

                "pattern":
                    problem,

                "occurrences":
                    len(items),

                "actions":
                    dict(actions),

                "preferred_action":
                    preferred_action,

                "success_rate":
                    confidence,

                "confidence":
                    confidence

            })


        return result




if __name__ == "__main__":


    engine = PatternMemory()


    print(
        engine.analyze()
    )
