from apscheduler.schedulers.blocking import BlockingScheduler

from database.state_manager import StateManager

scheduler = BlockingScheduler()

engine = StateManager()


def run_monitor(monitor):

    data = monitor.check()

    if not data:
        return

    # hanya simpan status terbaru
    engine.set(
        monitor.name.lower(),
        data
    )


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
