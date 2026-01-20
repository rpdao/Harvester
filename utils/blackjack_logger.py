import os
import logging

from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# === Инициализация COLORAMA ===

...

# === Цвета ===
TURQ = "\033[36m"                                        # бирюзовый
RESET = "\033[0m"

# === Базовый каталог для логов Blackjack ===
BASE_DIR = os.path.join("data", "logs", "blackjack")
os.makedirs(BASE_DIR, exist_ok=True)

# === Кэш логгеров, чтобы не создавать дубликаты ===
_blackjack_loggers = {}

...

__all__ = ["get_blackjack_logger"]
