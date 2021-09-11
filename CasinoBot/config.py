import os

from loguru import logger

from customutils.confparse import Config


token = os.getenv("CASINO_TOKEN")

standart_config = {
    "casino_api_token": token,
    "licence_photo": "AgACAgIAAxkBAAEOOY1gU9f3uRanl2h-YCVh3PFbprQWLQACN7QxG2NPoUrQtlfP33-xv-Tzk6IuAAMBAAMCAAN5AAMgBgACHgQ",
    "min_deposite": 500,
    "casino_sup_username": "support",
}

path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../config.cfg"))
config = Config("Settings", path, {})

MINIK = 150  # минимальная сумма пополнения

LICENCE = "AgACAgIAAxkBAAEOOY1gU9f3uRanl2h-YCVh3PFbprQWLQACN7QxG2NPoUrQtlfP33-xv-Tzk6IuAAMBAAMCAAN5AAMgBgACHgQ"

SKIP_UPDATES = True  # useless


# directory = os.path.dirname(os.path.abspath(__file__))
# words_path = os.path.join(directory, "data", "russian_nouns.txt")

# with open(words_path, "r", encoding="utf-8") as file:
#     words = file.readlines()
#     words = [s.strip("\n") for s in words]
