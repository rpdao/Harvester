import os
import logging

import requests

from requests.exceptions import ReadTimeout

from config.settings import CHAT_ID, BTC_IMAGE_OUTPUT
from utils.helpers import (
    delete_command_after,
    safe_delete_message,
    require_bot_active,
)
from utils.image import create_price_image

# === ВНЕШНИЕ УСТАНОВКИ ===
# == Глобальные переменные ==
bot = None

# == Установка бота ==
def set_bot(b):
    global bot
    bot = b

# === ПОЛУЧЕНИЕ ЦЕНЫ BTC ===

...

# === ОТПРАВКА ИЗОБРАЖЕНИЯ ===

...

# === ОБРАБОТЧИК КОМАНДЫ /price ===

...

__all__ = [
    "send_price_image",
    "use_price",
    "set_bot"
]
