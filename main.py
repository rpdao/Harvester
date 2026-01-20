# === СТАНДАРТНЫЕ БИБЛИОТЕКИ ===
import os
import re
import sys
import json
import time
import signal
import logging
import threading
import datetime

from threading import Thread

# === СТОРОННИЕ БИБЛИОТЕКИ ===
import requests
import schedule

# === ЛОКАЛЬНЫЕ ИМПОРТЫ ===
from config.settings import LOCK_FILE
from utils import logger
from utils.scheduler import run_scheduler
from utils.shutdown import shutdown_manager, stop_event

# === ОТКЛЮЧЕНИЕ ЛОГОВ discord.py ===
for logger_name in ["discord", "discord.client", "discord.gateway", "discord.http"]:
    log = logging.getLogger(logger_name)
    log.setLevel(logging.WARNING)                      # Показывать только важное
    log.propagate = False

# === ИМПОРТ БОТОВ ===
from dc_bot import run_discord_bot
from tg_bot import run_telegram_bot

# === ОБРАБОТЧИК ВЫХОДА ===
shutdown_manager.bind_signals()

# === ОБЁРТКИ ДЛЯ ПОТОКОВ ===
def discord_worker():
    try:
        logging.info("[MAIN] Запуск потока Discord-бота...")
        run_discord_bot()
    except Exception as e:
        logging.error(f"[MAIN] Поток Discord завершился с ошибкой: {e}")
        shutdown_manager.shutdown("Discord worker exception")

def telegram_worker():
    try:
        logging.info("[MAIN] Запуск потока Telegram-бота...")
        run_telegram_bot()
    except Exception as e:
        logging.error(f"[MAIN] Telegram бот упал: {e}", exc_info=True)
        shutdown_manager.shutdown("Telegram worker exception")

# === ГЛАВНЫЙ ЗАПУСК ===
def main():
    logging.info("[MAIN] Запуск объединённого бота...")

    # Запускаем расписание
    schedule_thread = threading.Thread(target=run_scheduler, daemon=True)

    # Запускаем ботов
    discord_thread = threading.Thread(target=discord_worker)
    telegram_thread = threading.Thread(target=telegram_worker)

    schedule_thread.start()
    discord_thread.start()
    telegram_thread.start()

    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        logging.info("[MAIN] Ожидание завершения потоков...")
        discord_thread.join(timeout=5)
        telegram_thread.join(timeout=5)

        # Удаление LOCK-файла
        try:
            if os.path.exists(LOCK_FILE):
                os.remove(LOCK_FILE)
                logging.info("[MAIN] Lock-файл удалён. Telegram бот завершил работу.")
        except Exception as e:
            logging.error(f"[MAIN] Ошибка удаления lock-файла: {e}")

        logging.info("[MAIN] Бот завершил работу корректно.")

if __name__ == "__main__":
    main()
