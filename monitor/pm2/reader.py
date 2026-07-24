import json
import subprocess


class PM2Reader:

    @staticmethod
    def read():
        try:
            result = subprocess.run(
                ["pm2", "jlist"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                raise Exception(result.stderr)

            return json.loads(result.stdout)

        except Exception as e:
            print("PM2 Reader Error:", e)
            return []
