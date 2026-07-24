from copy import deepcopy

from database.state_manager import StateManager
from database.event_manager import EventManager


class StateEngine:

    def __init__(self):
        self.state = StateManager()
        self.events = EventManager()

    def process(self, monitor_name, current_data):

        previous = deepcopy(self.state.get(monitor_name))

        # Pertama kali
        if previous is None:
            self.state.set(monitor_name, deepcopy(current_data))
            return False

        # Tidak berubah
        if previous == current_data:
            return False

        # Berubah
        self.state.set(monitor_name, deepcopy(current_data))

        return True
