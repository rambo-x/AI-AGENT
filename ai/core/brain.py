"""
TripleSide AI Agent
System Brain v2

Membaca project_graph.json
dan membangun pemahaman arsitektur sistem.
"""

import json
from pathlib import Path
from datetime import datetime


INPUT_FILE = Path(
    "database/project_graph.json"
)

OUTPUT_FILE = Path(
    "database/system_brain.json"
)


class SystemBrain:


    def __init__(self):

        self.data = self.load()



    def load(self):

        if not INPUT_FILE.exists():

            return {}

        with open(
            INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def analyze(self):

        files = self.data.get(
            "files",
            []
        )


        architecture = {

            "entrypoint": [],
            "scheduler": [],
            "telegram": [],
            "memory": [],
            "analyzers": [],
            "core": [],
            "executor": [],
            "knowledge": [],
            "storage": []

        }


        for item in files:


            path = item.get(
                "path",
                ""
            )


            if path.endswith("app.py"):
                architecture["entrypoint"].append(path)


            if "/scheduler/" in path:
                architecture["scheduler"].append(path)


            if "/telegram/" in path:
                architecture["telegram"].append(path)


            if "/memory/" in path:
                architecture["memory"].append(path)


            if "/analyzers/" in path:
                architecture["analyzers"].append(path)


            if "/core/" in path:
                architecture["core"].append(path)


            if "/executor/" in path:
                architecture["executor"].append(path)


            if "/knowledge/" in path:
                architecture["knowledge"].append(path)


            if "/storage/" in path:
                architecture["storage"].append(path)



        report = {

            "generated_at":
                datetime.now().isoformat(),


            "system":
                "TripleSide AI Agent",


            "architecture":
                architecture,


            "total_modules":
                len(files),


            "environment": self.extract_environment(),


            "capabilities": self.detect_capabilities(),


            "health_score":
                self.calculate_health()

        }


        self.save(report)


        return report



    def extract_environment(self):

        env = []


        for item in self.data.get("files", []):

            for key in item.get(
                "environment",
                []
            ):

                if key not in env:
                    env.append(key)


        return env



    def detect_capabilities(self):

        caps = []


        mapping = {

            "telegram":
                "Telegram AI Interface",

            "memory":
                "Conversation Memory",

            "analyzers":
                "System Diagnostic Engine",

            "executor":
                "Action Executor",

            "knowledge":
                "Knowledge Base",

            "scheduler":
                "Background Monitoring"

        }


        for folder, name in mapping.items():

            if self.data:

                text = json.dumps(
                    self.data
                )


                if folder in text:

                    caps.append(name)


        return caps



    def calculate_health(self):

        total = len(
            self.data.get(
                "files",
                []
            )
        )


        if total == 0:

            return 0


        if total < 20:

            return 70


        return 100



    def save(self,data):

        OUTPUT_FILE.parent.mkdir(
            exist_ok=True
        )


        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )


        print(
            "System Brain saved:",
            OUTPUT_FILE
        )



if __name__ == "__main__":


    brain = SystemBrain()

    result = brain.analyze()


    print(
        json.dumps(
            result,
            indent=4
        )
    )
