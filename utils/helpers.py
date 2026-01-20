import os
import re
import random
import logging
import threading
import datetime

import telebot

from threading import Timer

from telebot.apihelper import ApiTelegramException

# === ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ===
bot_active = True

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
# == Экранируем спецсимволы ==

...

# == Фильтрация старых сообщений ==

...

# == Безопасное удаление сообщений ==

...

# == Удаление слэш-команд ==

...

# == Декоратор состояния слэш-команд ==

...

# == Выбор случайного фона ==

...

__all__ = [
    "escape_md",
    "is_recent",
    "safe_delete_message",
    "delete_command_after",
    "get_random_background",
    "get_points",
    "require_bot_active",
]
