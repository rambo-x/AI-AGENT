"""
Compatibility Bridge

Old application import:
from notifications.bot import start_bot

New Telegram engine:
ai.telegram.telegram_runner.main
"""


from ai.telegram.telegram_runner import main


def start_bot():

    return main()
