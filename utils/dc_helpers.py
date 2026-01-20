import os
import re

from config.settings import LAST_PRICE, LAST_TWEET_FILE

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
# == Экранируем спецсимволы ==

...

# == Загружаем последнюю цену BTC ==

...

# == Сохраняем последнюю цену BTC ==

...

# == Загружаем последний отправленный твит ==

...

# == Сохраняем последний отправленный твит ==

...

# == Глобальные переменные ==
previous_price = load_last_price()                         # Храним предыдущую цену
last_tweet_id = load_last_tweet_id()                       # Храним предыдуший твит
seen_tweet_ids = set()

__all__ = [
    "escape_markdown",
    "previous_price",
    "save_last_price",
    "last_tweet_id",
    "save_last_tweet_id",
    "seen_tweet_ids",
]
