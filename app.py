from config import APP_NAME
from utils.logger import logger

from scheduler.jobs import scheduler
from scheduler.jobs import register_jobs

from monitor.loader import load_monitors


def start():

    print("=" * 40)
    print(APP_NAME)
    print("=" * 40)

    logger.info("Loading monitors...")

    monitors = load_monitors()

    logger.info(f"{len(monitors)} monitor(s) loaded.")

    register_jobs(monitors)

    logger.info("Scheduler started.")

    try:
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        logger.info("Agent stopped.")


if __name__ == "__main__":
    start()
