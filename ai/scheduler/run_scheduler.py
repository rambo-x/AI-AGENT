"""
AI Scheduler Runner
"""

import os
import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(BASE_DIR)
)

os.chdir(BASE_DIR)


from ai.scheduler.scheduler_engine import SchedulerEngine



if __name__ == "__main__":

    scheduler = SchedulerEngine(
        interval=3600
    )

    scheduler.start()
