import os
import random
import logging
import threading

from telebot.types import Message

from config.settings import CHAT_ID, GM_IMAGE_OUTPUT, GN_IMAGE_OUTPUT
from utils.helpers import (
    delete_command_after,
    safe_delete_message,
    get_random_background,
    require_bot_active,
)
from utils.image import create_greeting_image

# === ВНЕШНИЕ УСТАНОВКИ ===
# == Глобальные переменные ==
bot = None

# == Создаём списки фраз ==
GOOD_MORNING_PHRASES = [
    "Good morning Red Planet",
    "Wake up, Legends!",
    "It's time to do good",
    "Good morning Purtoricans!",
    "Happy new day, Red Planetians!"
]

GOOD_NIGHT_PHRASES = [
    "Good night Red Planet",
    "Until tomorrow, Legends!",
    "The Red Planet guards your sleep!",
    "Sleep tight, warrior of light",
    "Sweet dreams, Purtorican"
]

# == Установка бота ==
def set_bot(b):
    global bot
    bot = b

# === ОТПРАВКА ИЗОБРАЖЕНИЙ GM И GN В ЧАТ ПО КОМАНДЕ ===
# == Обработчик команды /gm ==

...

# == Обработчик команды /gn ==

...

# == Обработчик GM/GN ==
def register_handlers(bot):
    gm_bot(bot)
    gn_bot(bot)

__all__ = [
    "set_bot",
    "register_handlers"
]
