"""
Normalization Loader

Loads built-in rules and user-defined rules.
"""

from pathlib import Path
import json

from ai.normalization.rules import DEFAULT_RULES


class RuleLoader:

    def __init__(self, root="."):

        self.root = Path(root)

        self.file = (
            self.root /
            "database" /
            "normalization_rules.json"
        )

        self.ensure_file()


    def ensure_file(self):

        if self.file.exists():
            return

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file.write_text(
            json.dumps(
                DEFAULT_RULES,
                indent=4
            )
        )


    def load(self):

        rules = dict(DEFAULT_RULES)

        try:

            custom = json.loads(
                self.file.read_text()
            )

        except Exception:

            custom = {}

        for signature, values in custom.items():

            if signature not in rules:

                rules[signature] = []

            for value in values:

                if value not in rules[signature]:

                    rules[signature].append(
                        value
                    )

        return rules
