import pkgutil
import importlib

from monitor.base import Monitor


def load_monitors():
    monitors = []

    package = importlib.import_module("monitor")

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):

        if module_name in ("base", "loader"):
            continue

        module = importlib.import_module(f"monitor.{module_name}")

        for obj in vars(module).values():

            if (
                isinstance(obj, type)
                and issubclass(obj, Monitor)
                and obj is not Monitor
            ):
                monitors.append(obj())

    return monitors
