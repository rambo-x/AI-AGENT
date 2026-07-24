import json
from pathlib import Path
from datetime import datetime


class MemoryFeedback:
    def __init__(self):
        self.database = Path("database")
        self.memory_file = self.database / "diagnostic_memory.json"

    def load_memory(self):
        if not self.memory_file.exists():
            return []

        try:
            with open(self.memory_file, "r") as file:
                data = json.load(file)
                return data.get("cases", [])
        except Exception:
            return []

    def search_previous(self, problem):
        cases = self.load_memory()

        results = []

        for case in cases:
            if problem.lower() in case.get("problem", "").lower():
                results.append(case)

        return results

    def create_feedback(self, diagnosis):
        problem = diagnosis.get("problem")

        previous = self.search_previous(problem)

        return {
            "generated_at": datetime.now().isoformat(),
            "problem": problem,
            "previous_cases_found": len(previous),
            "previous_cases": previous,
            "memory_status": (
                "known_problem"
                if previous
                else "new_problem"
            )
        }

    def save(self, diagnosis):
        output = self.create_feedback(diagnosis)

        path = self.database / "memory_feedback.json"

        with open(path, "w") as file:
            json.dump(
                output,
                file,
                indent=4
            )

        return str(path)


if __name__ == "__main__":
    feedback = MemoryFeedback()

    test = {
        "problem": "ModuleNotFoundError"
    }

    print(feedback.save(test))
