import json
from pathlib import Path

STATE_FILE = Path("database/state.json")


class StateManager:

    def __init__(self):
        self.state = self.load()

    def load(self):
        if not STATE_FILE.exists():
            return {}

        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=4)

    def get(self, key):
        return self.state.get(key)

    def set(self, key, value):
        self.state[key] = value
        self.save()

    def process(self, monitor_name, data):
        previous = self.get(monitor_name)

        previous_data = None

        if previous:
            previous_data = previous.get("last")

        self.set(
            monitor_name,
            {
                "last": data
            }
        )

        return previous_data != data
