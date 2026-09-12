import requests

from . import db
from .config import logger


def send_telegram(message):
    token = db.get_setting("telegram_token")
    chat_id = db.get_setting("telegram_chat_id")

    if not token or not chat_id:
        logger.info("Telegram not configured - skipping notification")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=10)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram notification: {e}")
