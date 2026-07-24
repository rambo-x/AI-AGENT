from apscheduler.schedulers.blocking import BlockingScheduler

from events.dispatcher import EventDispatcher
from database.state_manager import StateEngine

scheduler = BlockingScheduler()

dispatcher = EventDispatcher()
engine = StateEngine()


def run_monitor(monitor):

    data = monitor.check()

    if not data:
        return

    should_alert = engine.process(monitor.name, data)

    if should_alert:

        dispatcher.dispatch({
            "type": monitor.name.upper(),
            "severity": "warning",
            "data": data,
        })


def register_jobs(monitors):

    for monitor in monitors:

        # jalankan sekali saat startup
        run_monitor(monitor)

        scheduler.add_job(
            run_monitor,
            "interval",
            seconds=60,
            args=[monitor],
            id=monitor.name,
            replace_existing=True,
        )
