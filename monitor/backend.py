from utils.logger import logger
from monitor.base import Monitor
from monitor.pm2.backend_monitor import BackendMonitor as PM2BackendMonitor


class BackendMonitor(Monitor):

    name = "Backend"

    def __init__(self):
        self.pm2_monitor = PM2BackendMonitor()

    def check(self):
        logger.info("Backend monitor executed.")

        return self.pm2_monitor.check()
