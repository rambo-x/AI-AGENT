from monitor.pm2.reader import PM2Reader


class BackendMonitor:

    APP_NAME = "triplesidestudio-backend"

    def check(self):
        apps = PM2Reader.read()

        for app in apps:

            if app["name"] != self.APP_NAME:
                continue

            return {
                "name": app["name"],
                "status": app["pm2_env"]["status"],
                "restart": app["pm2_env"]["restart_time"],
                "cpu": app["monit"]["cpu"],
                "memory": app["monit"]["memory"],
                "uptime": app["pm2_env"]["pm_uptime"],
            }

        return None
