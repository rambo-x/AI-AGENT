import json
import re
from pathlib import Path
from datetime import datetime


class LogAnalyzer:


    ERROR_SIGNATURES = {

        "telegram_invalid_token": {

            "pattern": "invalidtoken",

            "type": "authentication_error",

            "component": [
                "notifications/bot.py",
                "config.py",
                ".env"
            ],

            "confidence": 0.95
        },


        "module_missing": {

            "pattern": "modulenotfounderror",

            "type": "import_error",

            "component": [
                "requirements.txt",
                "python_modules"
            ],

            "confidence": 0.90
        },


        "connection_error": {

            "pattern": "connectionerror",

            "type": "network_error",

            "component": [
                "network",
                "external_service"
            ],

            "confidence": 0.80
        },


        "permission_error": {

            "pattern": "permissionerror",

            "type": "permission_error",

            "component": [
                "filesystem"
            ],

            "confidence": 0.80
        }

    }



    def __init__(self):

        self.log_file = Path(
            "logs/agent.log"
        )

        self.output = Path(
            "database/log_analysis.json"
        )



    def sanitize(self, text):

        patterns = [

            # Telegram bot token
            r"\b\d{8,}:[A-Za-z0-9_\-]{20,}\b",

            # token=value
            r"(token[=: ]+)([^\s]+)"

        ]


        for pattern in patterns:

            if pattern.startswith("(token"):

                text = re.sub(
                    pattern,
                    r"\1[REDACTED]",
                    text,
                    flags=re.I
                )

            else:

                text = re.sub(
                    pattern,
                    "[REDACTED]",
                    text
                )


        return text



    def detect_error(self, line):

        clean = line.lower()


        for name, data in self.ERROR_SIGNATURES.items():

            if data["pattern"] in clean:

                return {

                    "signature":
                        name,

                    "type":
                        data["type"],

                    "component":
                        data["component"],

                    "message":
                        self.sanitize(line),

                    "confidence":
                        data["confidence"]

                }


        return None



    def analyze(self):

        results = []


        if not self.log_file.exists():

            return results



        lines = self.log_file.read_text(
            encoding="utf-8"
        ).splitlines()



        processed = set()



        for line_number, line in enumerate(
            lines,
            start=1
        ):

            detected = self.detect_error(
                line
            )


            if detected:

                key = (
                    detected["signature"],
                    detected["message"]
                )


                # mencegah duplikasi error sama

                if key in processed:

                    continue


                processed.add(key)


                detected["line"] = line_number


                results.append(
                    detected
                )


        return results



    def save(self):

        errors = self.analyze()


        data = {

            "generated_at":
                datetime.now().isoformat(),

            "total_errors":
                len(errors),

            "errors":
                errors

        }


        self.output.write_text(

            json.dumps(
                data,
                indent=4
            ),

            encoding="utf-8"

        )


        return str(
            self.output
        )



if __name__ == "__main__":

    analyzer = LogAnalyzer()

    print(
        analyzer.save()
    )
