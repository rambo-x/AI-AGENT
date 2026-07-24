"""
TripleSide AI Agent
System Tools

Safe system inspection tools.
"""

import subprocess
import shutil
from datetime import datetime


class SystemTools:


    def now(self):

        return {
            "time":
                datetime.now().isoformat()
        }



    def disk_usage(self):

        total, used, free = shutil.disk_usage("/")


        return {

            "total_gb":
                round(total / 1024**3, 2),

            "used_gb":
                round(used / 1024**3, 2),

            "free_gb":
                round(free / 1024**3, 2)

        }



    def memory(self):

        try:

            result = subprocess.check_output(
                [
                    "free",
                    "-m"
                ]
            ).decode()


            return {
                "memory": result
            }


        except Exception as e:

            return {
                "error": str(e)
            }



    def uptime(self):

        try:

            result = subprocess.check_output(
                [
                    "uptime"
                ]
            ).decode()


            return {
                "uptime": result.strip()
            }


        except Exception as e:

            return {
                "error": str(e)
            }



    def health(self):

        return {

            "time":
                self.now(),

            "disk":
                self.disk_usage(),

            "memory":
                self.memory(),

            "uptime":
                self.uptime()

        }



if __name__ == "__main__":


    tool = SystemTools()


    import json


    print(
        json.dumps(
            tool.health(),
            indent=4
        )
    )
