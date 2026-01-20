import time
import logging

import schedule

from features.price import send_price_image
from utils.shutdown import stop_event

# === НАСТРОЙКА РАСПИСАНИЯ ===
# == Отправка цены BTC 1 раз в 4 часа ==

...

# === ЗАПУСК ПЛАНИРОВЩИКА ==

...

__all__ = ["run_scheduler"]
