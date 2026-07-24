from utils.logger import logger
from monitor.base import Monitor


class BackendMonitor(Monitor):

    name = "Backend"

    def check(self):
        logger.info("Backend monitor executed.")
