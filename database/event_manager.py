import json
from pathlib import Path
from datetime import datetime

EVENT_FILE = Path("database/events.json")


class EventManager:

    def __init__(self):
        self.events = self.load()

    def load(self):
        if not EVENT_FILE.exists():
            return {}

        try:
            with open(EVENT_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self):
        with open(EVENT_FILE, "w") as f:
            json.dump(self.events, f, indent=4)

    def register(self, event_id):
        now = datetime.utcnow().isoformat()

        event = self.events.get(event_id)

        if event:
            event["count"] += 1
            event["last_seen"] = now
        else:
            self.events[event_id] = {
                "count": 1,
                "last_seen": now,
                "last_sent": None
            }

        self.save()
