import os
import json
import logging
import threading

from config.settings import MAP_FILE

# === ЗАГРУЗКА МАППИНГА СООБЩЕНИЙ ===
LOCK = threading.Lock()

...

# == Сохранение соответствия ==

...

# == Получение Telegram message_id по Discord message_id ==

...

__all__ = [
    "save_mapping",
    "get_telegram_reply_id"
]
