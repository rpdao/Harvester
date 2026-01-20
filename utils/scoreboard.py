import os
import json
import logging
import threading

from collections import defaultdict
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from wcwidth import wcswidth

from config.settings import SCORE_FILE
from utils.helpers import safe_delete_message

# === ФОРМИРОВАНИЕ ТАБЛИЦЫ ЛИДЕРОВ ===
# == Глобальные переменные ==
bot = None                                             # будет установлен извне

# == Внешние установки ==
# = Установка бота =
def set_bot(b):
    global bot
    bot = b

# == Глобальный словарь user_id -> last_page ==
user_score_pages = defaultdict(int)

# == Начисление очков за TRIVIA ==
points = 10

# == Загружаем счёт ==

...

# == Сохраняем счёт ==

...

# == Начисление очков в Roll и Reroll ==

...

# == Начисление очков в TRIVIA ==

...

# == Начисление очков в BlackJack ==

...

# === ФОРМИРОВАНИЕ ОТОБРАЕНИЯ ТАБЛИЦЫ ЛИДЕРОВ ===
# == Показ страницы лидерборда ==

...

# == Пагинация с восстановлением текущей страницы ==

...

__all__ = [
    "save_scores",
    "add_point",
    "add_point_trivia",
    "user_score_pages",
    "scores",
    "points",
    "show_score_page",
    "handle_score_pagination",
    "set_bot",
    "add_point_blackjack",
    "load_scores",
]
