# === СТАНДАРТНЫЕ БИБЛИОТЕКИ ===
import os
import sys
import time
import random
import logging
import asyncio

# === СТОРОННИЕ БИБЛИОТЕКИ ===
import tweepy
import aiohttp
import discord
import requests

from discord.ext import commands
from tweepy.asynchronous import AsyncClient

# === ЛОКАЛЬНЫЕ ИМПОРТЫ ===
import utils.dc_helpers as helpers

from config.settings import BEARER_TOKEN, DISCORD_TOKEN, GUILD_ID
from features import tweets
from features.game import register_games_commands
from features import register_utils_commands
from features.dc_price import update_btc_channel_name
from features.ticket_notify import on_guild_channel_create as ticket_handler
from utils import logger
from utils.scheduler import run_scheduler
from utils.shutdown import shutdown_manager, stop_event
from utils.tweets_guard import load_twitter_block_flag

# === ЗАГРУЗКА ДАННЫХ ===
# == Загрузка последней цены $BTC ==
previous_price = helpers.load_last_price()

# == Загрузка последнего твита ==
last_tweet_id = helpers.load_last_tweet_id()

# === ИНИЦИАЛИЗАЦИЯ DISCORD КЛИЕНТА ===
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# === ИНИЦИАЛИЗАЦИЯ TWITTER КЛИЕНТА ===
twitter_client = AsyncClient(bearer_token=BEARER_TOKEN)

# == Проверка флага блокировки Twitter ==
try:
    flag = load_twitter_block_flag()
except Exception as e:
    logging.warning(f"[DC_MAIN] Не удалось загрузить флаг блокировки Twitter: {e}")
    flag = False

tweets.set_twitter_flags(flag)
logging.info(
    f"[DC_MAIN] Стартовое состояние Twitter: {'Отключено' if flag else 'Включено'}"
)

# === ХРАНИЛИЩЕ ТАСКОВ ===
background_tasks: list[asyncio.Task] = []

# === ЦИКЛЫ ЗАДАЧ ===
# == Обновление цены BTC в названии канала ==
async def btc_loop():
    await bot.wait_until_ready()
    while not stop_event.is_set():
        try:
            await update_btc_channel_name(bot)
        except Exception as e:
            logging.exception(f"[DC_MAIN] Ошибка в btc_loop: {e}")
        await asyncio.sleep(600)                               # каждые 10 минут

# == Проверка и отправка новых твитов ==
async def twitter_loop(bot, twitter_client):
    logged_disabled = False
    while not stop_event.is_set():
        try:
            if not tweets.twitter_enabled:
                logging.info("[DC_MAIN] Twitter отключён - пропуск итерации.")
                logged_disabled = True
            else:
                logged_disabled = False
                await tweets.fetch_and_send_tweets(bot, twitter_client)
        except Exception as e:
            logging.exception(f"[DC_MAIN] Ошибка в twitter_loop: {e}")
        await asyncio.sleep(1800 + random.randint(-120, 120))  # каждые ~30 минут


# === ИНИЦИАЛИЗАЦИЯ ===
# == Обработчик создания канала с тикетами ==
@bot.event
async def on_guild_channel_create(channel):
    await ticket_handler(channel)

# == Инициализация бота ==
@bot.event
async def on_ready():
    logging.info(f"[DC_MAIN] Бот вошёл как {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

    # == Запуск фоновых задач ==
    background_tasks.extend([
        asyncio.create_task(btc_loop(), name="btc_loop"),
        asyncio.create_task(twitter_loop(bot, twitter_client), name="twitter_loop"),
        asyncio.create_task(
            tweets.check_reset_twitter_flag(),
            name="check_reset_twitter_flag"
        ),
    ])

    logging.info(f"[DC_MAIN] Запущено фоновых задач: {len(background_tasks)}")

# === ЗАПУСК БОТА ===
def run_discord_bot():
    # == Установка бота в модули ==
    register_games_commands(bot)
    register_utils_commands(bot)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def runner():
        await bot.start(DISCORD_TOKEN)

    # == Основная задача ==
    main_task = loop.create_task(runner(), name="discord_runner")

    try:
        while not stop_event.is_set():
            loop.run_until_complete(asyncio.sleep(0.5))

    finally:
        logging.info(
            f"[DC_MAIN] stop_event получен, причина: {shutdown_manager.get_reason()}"
        )

        async def shutdown():
            # Отмена фоновых задач
            logging.info("[DC_MAIN] Отмена фоновых asyncio-задач...")

            for task in background_tasks:
                if not task.done():
                    task.cancel()

            if background_tasks:
                await asyncio.gather(*background_tasks, return_exceptions=True)

            logging.info("[DC_MAIN] Фоновые задачи остановлены")

            # Остановка Discord бота
            try:
                if not bot.is_closed():
                    await bot.close()
            except Exception:
                logging.exception("[DC_MAIN] Ошибка при bot.close()")

        loop.run_until_complete(shutdown())

        # Завершение main_task
        if not main_task.done():
            main_task.cancel()
            try:
                loop.run_until_complete(main_task)
            except asyncio.CancelledError:
                pass

        loop.stop()
        loop.close()

        logging.info("[DC_MAIN] Discord бот остановлен корректно")


# == Для прямого запуска ==
if __name__ == "__main__":
    run_discord_bot()
