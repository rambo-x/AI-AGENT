import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:

    def send_event(self, event):

        if not TELEGRAM_BOT_TOKEN:
            print("Telegram token kosong")
            return

        text = (
            "🚨 TripleSide AI Agent\n\n"
            f"Event : {event['type']}\n"
            f"Status : {event['data'].get('status')}\n"
        )

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
            },
            timeout=10,
        )
