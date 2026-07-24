from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def register_jobs(monitors):
    for monitor in monitors:
        # Jalankan sekali saat startup
        monitor.check()

        # Jadwalkan setiap 60 detik
        scheduler.add_job(
            monitor.check,
            "interval",
            seconds=60,
            id=monitor.name,
            replace_existing=True
        )
