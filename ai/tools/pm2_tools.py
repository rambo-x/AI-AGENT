"""
PM2 Tools
TripleSide AI Agent

Read PM2 runtime information.
Safe mode:
Only inspect, never restart.
"""

import subprocess
import json
from datetime import datetime


class PM2Tools:


    def run_pm2(self):

        try:

            result = subprocess.check_output(
                [
                    "pm2",
                    "jlist"
                ],
                text=True
            )

            return json.loads(result)


        except Exception as e:

            return {
                "error": str(e)
            }



    def status(self):

        data = self.run_pm2()


        if isinstance(data, dict) and "error" in data:

            return data


        apps = []


        for app in data:

            apps.append({

                "name":
                    app.get(
                        "name"
                    ),

                "status":
                    app.get(
                        "pm2_env",
                        {}
                    ).get(
                        "status"
                    ),

                "restarts":
                    app.get(
                        "pm2_env",
                        {}
                    ).get(
                        "restart_time"
                    ),

                "memory":

                    round(
                        app.get(
                            "monit",
                            {}
                        ).get(
                            "memory",
                            0
                        )
                        /
                        1024
                        /
                        1024,
                        2
                    ),

                "cpu":

                    app.get(
                        "monit",
                        {}
                    ).get(
                        "cpu"
                    )

            })


        return {

            "checked_at":
                datetime.now().isoformat(),

            "applications":
                apps

        }



if __name__ == "__main__":


    tool = PM2Tools()


    print(
        json.dumps(
            tool.status(),
            indent=4
        )
    )
