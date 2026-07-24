"""
PM2 Analyzer

Analyze PM2 runtime state.

Improved:
- Detect historical crashes
- Avoid false critical alerts
- Separate current failure vs old PM2 state
"""

from datetime import datetime
import subprocess


class PM2Analyzer:


    def runtime_process_exists(self, name):

        try:

            result = subprocess.run(
                [
                    "pm2",
                    "jlist"
                ],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return False


            return name in result.stdout


        except Exception:

            return False



    def analyze(self, pm2_data):

        result = {

            "generated_at":
                datetime.now().isoformat(),

            "issues":[]

        }


        apps = pm2_data.get(
            "applications",
            []
        )


        for app in apps:

            name = app.get(
                "name",
                "unknown"
            )


            status = app.get(
                "status",
                "unknown"
            )


            restarts = app.get(
                "restarts",
                0
            )


            running = self.runtime_process_exists(
                name
            )



            #
            # Current failure
            #
            if status == "errored":


                if running:

                    result["issues"].append({

                        "problem":
                            f"{name} previous crash detected",

                        "severity":
                            "warning",

                        "cause":
                            "PM2 recorded previous failure but runtime process exists",

                        "recommendation":
                            [
                                "Review historical PM2 logs",
                                "Monitor next restart cycle"
                            ],

                        "confidence":
                            0.75

                    })


                else:

                    result["issues"].append({

                        "problem":
                            f"{name} service unavailable",

                        "severity":
                            "critical",

                        "cause":
                            "PM2 process errored and runtime process not found",

                        "recommendation":
                            [
                                "Check PM2 logs",
                                "Inspect startup error",
                                "Restart service"
                            ],

                        "confidence":
                            0.95

                    })



            #
            # Restart instability
            #
            if restarts > 100:


                result["issues"].append({

                    "problem":
                        f"{name} unstable restart history",

                    "severity":
                        "warning",

                    "cause":
                        f"Process restarted {restarts} times",

                    "recommendation":
                        [
                            "Review error logs",
                            "Check crash pattern"
                        ],

                    "confidence":
                        0.85

                })



        return result





if __name__ == "__main__":


    import json

    from ai.tools.pm2_tools import PM2Tools


    data = PM2Tools().status()


    analyzer = PM2Analyzer()


    print(

        json.dumps(
            analyzer.analyze(data),
            indent=4
        )

    )
