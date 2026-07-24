from notifications.notifier import TelegramNotifier


class EventDispatcher:

    def __init__(self):
        self.telegram = TelegramNotifier()

    def dispatch(self, event):

        print("Dispatch:", event["type"])

        self.telegram.send_event(event)
