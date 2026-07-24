from abc import ABC, abstractmethod


class Monitor(ABC):
    name = "Monitor"

    @abstractmethod
    def check(self):
        pass
