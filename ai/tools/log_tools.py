"""
Runtime Log Tools

Collect PM2 logs safely.
"""

import subprocess
from datetime import datetime


class LogTools:


    def get_pm2_logs(
        self,
        process,
        lines=100
    ):

        try:

            result = subprocess.run(
                [
                    "pm2",
                    "logs",
                    process,
                    "--lines",
                    str(lines),
                    "--nostream"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )


            return {

                "time":
                    datetime.now().isoformat(),

                "process":
                    process,

                "logs":
                    result.stdout[-5000:],

                "errors":
                    result.stderr[-2000:]

            }


        except Exception as e:

            return {

                "error":
                    str(e)

            }



if __name__ == "__main__":

    import json


    tool = LogTools()


    print(
        json.dumps(
            tool.get_pm2_logs(
                "tripleside-ai-agent"
            ),
            indent=4
        )
    )
