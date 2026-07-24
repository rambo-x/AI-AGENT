"""
Normalization Matcher

Matches raw problem descriptions to a normalized signature.
"""

from ai.normalization.loader import RuleLoader


class RuleMatcher:

    def __init__(self, root="."):

        self.loader = RuleLoader(root)
        self.rules = self.loader.load()

    def match(self, text):

        if not text:
            return "unknown"

        source = str(text).lower().strip()

        # Exact signature
        if source in self.rules:
            return source

        # Exact alias
        for signature, aliases in self.rules.items():

            if source in [
                alias.lower().strip()
                for alias in aliases
            ]:
                return signature

        # Partial match
        for signature, aliases in self.rules.items():

            for alias in aliases:

                alias = alias.lower().strip()

                if alias in source:
                    return signature

                if source in alias:
                    return signature

        return source
