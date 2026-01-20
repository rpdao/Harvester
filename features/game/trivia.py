import os
import random
import logging
import threading

import telebot

from threading import Timer
from word2number import w2n

from telebot.apihelper import ApiTelegramException

from config.settings import TRIVIA_FILE, CHAT_ID, RU_NUMBERS
from features.discord_bridge import send_text
from utils.check_admin import is_admin, admin_only
from utils.helpers import (
    safe_delete_message,
    delete_command_after,
    require_bot_active,
)
from utils.scoreboard import add_point_trivia, scores, save_scores, points

# === ДОБАВЛЯЕМ ВИКТОРИНУ TRIVIA ===
# == Состояние викторины ==
used_trivia_questions = set()
trivia_questions = []                                      # нужно загрузить при запуске
trivia_game_active = False                                 # Вся викторина активна
trivia_active = False                                      # Идёт вопрос
trivia_question_pending = False                            # Готовится следующий вопрос
trivia_random_delay = None                                 # Выбор режима

# == Переменные вопроса ==
current_trivia = None
current_mask_en = None
current_mask_ru = None
hint_index = 0
hint_number = 1
hint_timer = None
hint_message_ids = []                                      # Храним все ID подсказок
last_hint_id = None                                        # ID последней подсказки
next_trivia_timer = None
question_message_id = None
question_counter = 1
first_question_sent = False

bot = None                                                 # будет установлен извне

# == Внешние установки ==
# = Установка бота =
def set_bot(b):
    global bot
    bot = b

# = Запись в лидерборд =

...

# == Загрузка вопросов ==

...

# == Вспомогательные функции TRIVIA ==
# = Простая поддержка чисел от 0 до 999 прописью на русском =

...

# = Преобразует ответ в число (если возможно) или чистит текст =

...

# = Настройка расписания =

...

# == Отправка первого вопроса ==

...

# == Отправка следующего вопроса ==

...

# == Подсказки ==

...

# == Удаление подсказок ==

...

# == Общая логика команды /rpdao_trivia ==

...

# == Регистрация обработчиков ==

...

# == Общая логика команды /rpdao_trivia_off ==

...

# == Регистрация обработчиков ==

...

# == Обработка ответов ==

...

__all__ = [
    "set_bot",
    "register_handlers",
    "set_save_scores",
    "load_trivia_questions",
    "start_trivia_handlers",
    "stop_trivia_handlers",
]
