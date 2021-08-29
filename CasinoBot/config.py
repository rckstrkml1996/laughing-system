import os

from loguru import logger

from customutils.confparse import Config

token = os.getenv("CASINO_TOKEN")

standart_config = {
    "casino_api_token": token,
    "licence_photo": "AgACAgIAAxkBAAEOOY1gU9f3uRanl2h-YCVh3PFbprQWLQACN7QxG2NPoUrQtlfP33-xv-Tzk6IuAAMBAAMCAAN5AAMgBgACHgQ",
    "min_deposite": 500,
}

path = os.path.abspath("../config.cfg")
config = Config("Settings", path, {})

MINIK = 150  # минимальная сумма пополнения

LICENCE = "AgACAgIAAxkBAAEOOY1gU9f3uRanl2h-YCVh3PFbprQWLQACN7QxG2NPoUrQtlfP33-xv-Tzk6IuAAMBAAMCAAN5AAMgBgACHgQ"

SKIP_UPDATES = True  # useless
