# === СТАНДАРТНЫЕ БИБЛИОТЕКИ ===
import os
import sys
import time
import logging
import threading

# === СТОРОННИЕ БИБЛИОТЕКИ ===
import psutil
import telebot

# == Telegram библиотеки ==
from requests.exceptions import ConnectionError
from telebot import TeleBot

# === ЛОКАЛЬНЫЕ ИМПОРТЫ ===
from config.settings import LOCK_FILE, TOKEN
from utils import logger
from utils import scoreboard
from utils.scheduler import run_scheduler
from utils.shutdown import shutdown_manager, stop_event

from features import discord_bridge, gm_gn, price, score, stop_start, tag
from features import game
from features.game import trivia
from features.crimson_board import register_crimson_board
from features.link import register_link_handlers

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
# == Блокировка повторного запуска ==
def is_process_running(pid: int) -> bool:
    return psutil.pid_exists(pid)

# == Пишем текущий PID в файл ==
def write_lock_file():
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

# = Проверяем LOCK файл =
def check_existing_instance():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            try:
                pid = int(f.read())
                if is_process_running(pid):
                    logging.error(f"[TG_MAIN] Бот уже запущен с PID {pid}. Выход.")
                    sys.exit(1)
                else:
                    logging.warning(
                        "[TG_MAIN] Найден старый lock-файл от неактивного процесса. "
                        "Продолжаем."
                    )
            except ValueError:
                logging.warning("[TG_MAIN] Поврежденный lock-файл. Продолжаем.")

# === ЗАПУСК ===
def run_telegram_bot():
    # Проверка и блокировка повторного запуска
    check_existing_instance()
    write_lock_file()

    # Загрузка лидерборда
    scores = scoreboard.load_scores()

    # Инициализация бота
    bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
    polling_active = threading.Event()
    polling_active.set()

    # Установка бота в модули
    game.set_bot(bot)
    game.set_save_scores(scoreboard.save_scores)
    score.register_handlers(bot)
    scoreboard.set_bot(bot)
    stop_start.stop_start_handlers(bot)
    discord_bridge.set_bot(bot)
    discord_bridge.send_photo(bot)
    gm_gn.set_bot(bot)
    price.set_bot(bot)
    tag.set_bot(bot)

    # Регистрация обработчиков
    game.register_game_handlers(bot)
    trivia.load_trivia_questions()
    gm_gn.register_handlers(bot)
    price.use_price(bot)
    tag.tag_handlers(bot)
    register_crimson_board(bot)
    register_link_handlers(bot)

    logging.info("[TG_MAIN] Telegram бот инициализирован в модули")

    # == Запуск polling в отдельном потоке ==
    def polling_loop():
        logging.info(f"[TG_MAIN] Telegram polling запущен")
        try:
            while polling_active.is_set():
                try:
                    bot.infinity_polling(
                        timeout=20,
                        long_polling_timeout=30
                    )
                except Exception as e:
                    if not stop_event.is_set():
                        logging.exception(f"[TG_MAIN] Ошибка polling: {e}")
                        time.sleep(3)
        finally:
            logging.info("[TG_MAIN] polling_loop завершён")

    polling_thread = threading.Thread(
        target=polling_loop,
        name="TG-Polling",
        daemon=True
    )
    polling_thread.start()

    logging.info(f"[TG_MAIN] Telegram бот запущен. PID: {os.getpid()}")

    # == Ожидание сигнала остановки ==
    stop_event.wait()

    # == Остановка бота ==
    logging.info(
        f"[TG_MAIN] stop_event получен, причина: {shutdown_manager.get_reason()}"
    )

    polling_active.clear()

    try:
        bot.stop_polling()
    except Exception:
        logging.exception("[TG_MAIN] Ошибка при остановке polling")

    polling_thread.join(timeout=8)

    if polling_thread.is_alive():
        logging.warning("[TG_MAIN] polling_thread не завершился за таймаут")
    else:
        logging.info("[TG_MAIN] polling_thread завершён корректно")

    logging.info("[TG_MAIN] Telegram бот остановлен")


# == Для прямого запуска (если вдруг) ==
if __name__ == "__main__":
    run_telegram_bot()
