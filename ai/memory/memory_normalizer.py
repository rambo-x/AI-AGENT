"""
Memory Normalizer

Normalizes different names of the same problem
so AI Agent memory can recognize repeated incidents.
"""

import re


class MemoryNormalizer:

    def __init__(self):
        self.rules = {
            "telegram_token": [
                "telegram authentication failure",
                "telegram_invalid_token",
                "invalid telegram bot token",
                "telegram.error.invalidtoken",
                "telegrampackage token",
                "token was rejected"
            ],

            "import_error": [
                "modulenotfounderror",
                "importerror",
                "missing package",
                "package missing"
            ],

            "service_failure": [
                "service stopped",
                "stopped status detected",
                "application crash",
                "service unavailable"
            ],

            "configuration_error": [
                "missing environment variable",
                "invalid configuration",
                ".env error",
                "config error"
            ]
        }


    def normalize(self, text):
        """
        Convert problem description into standard signature.
        """

        if not text:
            return "unknown_problem"

        value = text.lower()

        value = re.sub(
            r"[^a-z0-9_ .-]",
            "",
            value
        )


        for signature, aliases in self.rules.items():

            for alias in aliases:

                if alias in value:
                    return signature


        return value.strip()


    def compare(self, first, second):
        """
        Compare two problems.
        """

        return (
            self.normalize(first)
            ==
            self.normalize(second)
        )
