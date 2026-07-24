import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "TripleSide AI Agent")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

WEBSITE_URL = os.getenv("WEBSITE_URL", "")
API_URL = os.getenv("API_URL", "")

BACKEND_PM2 = os.getenv("BACKEND_PM2", "")
FRONTEND_PM2 = os.getenv("FRONTEND_PM2", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
