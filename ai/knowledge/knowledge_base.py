"""
Knowledge Base

Central knowledge repository for the AI Agent.
Uses the unified Storage layer.
"""

from ai.storage.storage import Storage


DEFAULT_KNOWLEDGE = {
    "knowledge": [
        {
            "signature": "telegram_token",
            "category": "configuration_error",
            "cause": "Invalid Telegram Bot Token",
            "solution": "Update TELEGRAM_BOT_TOKEN"
        },
        {
            "signature": "module_not_found",
            "category": "import_error",
            "cause": "Missing Python package",
            "solution": "Install missing package"
        },
        {
            "signature": "connection_refused",
            "category": "network_error",
            "cause": "Target service offline",
            "solution": "Start the service"
        },
        {
            "signature": "permission_denied",
            "category": "permission_error",
            "cause": "Insufficient permission",
            "solution": "Check file permission"
        }
    ]
}


class KnowledgeBase:

    def __init__(self, root="."):

        self.storage = Storage(root)

        if not self.storage.exists("knowledge.json"):
            self.storage.save(
                "knowledge.json",
                DEFAULT_KNOWLEDGE
            )

    def load(self):

        return self.storage.load(
            "knowledge.json",
            DEFAULT_KNOWLEDGE
        )

    def search(self, signature):

        data = self.load()

        for item in data.get("knowledge", []):

            if item.get("signature") == signature:
                return item

        return None

    def all(self):

        return self.load().get(
            "knowledge",
            []
        )

    def add(
        self,
        signature,
        category,
        cause,
        solution
    ):

        data = self.load()

        for item in data["knowledge"]:

            if item["signature"] == signature:
                return item

        entry = {
            "signature": signature,
            "category": category,
            "cause": cause,
            "solution": solution
        }

        data["knowledge"].append(entry)

        self.storage.save(
            "knowledge.json",
            data
        )

        return entry

    def remove(self, signature):

        data = self.load()

        original = len(data["knowledge"])

        data["knowledge"] = [

            item

            for item in data["knowledge"]

            if item["signature"] != signature

        ]

        if len(data["knowledge"]) != original:

            self.storage.save(
                "knowledge.json",
                data
            )

            return True

        return False

    def save(self):

        self.storage.save(
            "knowledge.json",
            self.load()
        )

        return "database/knowledge.json"
