"""
Memory Feedback

Long term diagnostic memory.

Features:
- save diagnostic cases
- search previous cases
- track incident status
- resolve old problems
- learn successful actions
"""


from datetime import datetime

from ai.storage.storage import Storage
from ai.normalization.manager import NormalizationManager



DEFAULT_MEMORY = {

    "created_at":
        datetime.now().isoformat(),

    "cases": [],

    "actions": []

}





class MemoryFeedback:


    def __init__(
        self,
        root="."
    ):

        self.storage = Storage(
            root
        )

        self.normalizer = NormalizationManager(
            root
        )


        if not self.storage.exists(
            "diagnostic_memory.json"
        ):

            self.storage.save(
                "diagnostic_memory.json",
                DEFAULT_MEMORY
            )



    def load(self):

        return self.storage.load(
            "diagnostic_memory.json",
            DEFAULT_MEMORY
        )



    def save_database(
        self,
        data
    ):

        self.storage.save(
            "diagnostic_memory.json",
            data
        )



    def normalize(
        self,
        problem
    ):

        return self.normalizer.normalize(
            problem
        )



    def search(
        self,
        problem
    ):

        normalized = self.normalize(
            problem
        )

        data = self.load()

        matches = []


        for case in data.get(
            "cases",
            []
        ):


            if case.get(
                "problem"
            ) == normalized:


                matches.append(
                    case
                )


        return matches




    def save_case(
        self,
        problem,
        category=None,
        cause=None,
        solution=None
    ):


        normalized = self.normalize(
            problem
        )


        data = self.load()


        case = {

            "timestamp":
                datetime.now().isoformat(),

            "problem":
                normalized,

            "category":
                category,

            "cause":
                cause,

            "solution":
                solution,

            "status":
                "active",

            "resolved_at":
                None,

            "resolution":
                None

        }


        data["cases"].append(
            case
        )


        self.save_database(
            data
        )


        return case





    def save(
        self,
        problem_data
    ):


        problem = problem_data.get(
            "problem",
            "unknown_problem"
        )


        category = problem_data.get(
            "category"
        )


        cause = problem_data.get(
            "cause"
        )


        solution = problem_data.get(
            "solution"
        )



        existing = self.search(
            problem
        )



        if existing:


            return {

                "problem":
                    self.normalize(
                        problem
                    ),

                "previous_cases_found":
                    len(existing),

                "previous_cases":
                    existing,

                "memory_status":
                    "known_problem"

            }




        case = self.save_case(
            problem,
            category,
            cause,
            solution
        )


        return {

            "problem":
                case["problem"],

            "previous_cases_found":
                0,

            "previous_cases":
                [],

            "memory_status":
                "new_problem"

        }





    def resolve_case(
        self,
        problem,
        resolution
    ):


        normalized = self.normalize(
            problem
        )


        data = self.load()


        updated = 0



        for case in data.get(
            "cases",
            []
        ):


            if case.get(
                "problem"
            ) == normalized:


                case["status"] = "resolved"


                case["resolved_at"] = (
                    datetime.now().isoformat()
                )


                case["resolution"] = resolution


                updated += 1




        self.save_database(
            data
        )


        return {


            "problem":
                normalized,


            "updated":
                updated,


            "status":
                "resolved"

        }





    def all_cases(self):

        return self.load().get(
            "cases",
            []
        )





    def statistics(self):


        cases = self.all_cases()


        active = len(
            [
                c for c in cases
                if c.get("status") != "resolved"
            ]
        )


        resolved = len(
            [
                c for c in cases
                if c.get("status") == "resolved"
            ]
        )


        return {

            "total":
                len(cases),

            "active":
                active,

            "resolved":
                resolved

        }




    #
    # Experience Learning
    #


    def record_action_result(
        self,
        problem,
        action,
        result
    ):


        data = self.load()


        if "actions" not in data:

            data["actions"] = []



        found = None



        for item in data["actions"]:


            if (
                item.get("problem") == problem
                and
                item.get("action") == action
            ):

                found = item

                break




        if not found:


            found = {

                "problem":
                    problem,

                "action":
                    action,

                "success":
                    0,

                "failed":
                    0

            }


            data["actions"].append(
                found
            )




        if result in (
            "success",
            "recovered",
            "simulated"
        ):

            found["success"] += 1


        else:

            found["failed"] += 1




        total = (
            found["success"]
            +
            found["failed"]
        )


        found["success_rate"] = (

            found["success"]
            /
            total

            if total

            else 0

        )



        self.save_database(
            data
        )


        return found





    def recommend_action(
        self,
        problem
    ):


        data = self.load()


        candidates = []



        for item in data.get(
            "actions",
            []
        ):


            if item.get(
                "problem"
            ) == problem:


                candidates.append(
                    item
                )



        if not candidates:


            return {

                "found":
                    False

            }





        best = max(
            candidates,
            key=lambda x:
                x.get(
                    "success_rate",
                    0
                )
        )



        return {


            "found":
                True,


            "problem":
                problem,


            "recommended_action":
                best["action"],


            "success_rate":
                best.get(
                    "success_rate",
                    0
                ),


            "confidence":
                min(
                    best.get(
                        "success",
                        0
                    )
                    /
                    5,
                    1
                )

        }





if __name__ == "__main__":


    memory = MemoryFeedback()


    print(
        memory.statistics()
    )
