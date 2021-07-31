from os import getenv

SKIP_UPDATES = True

# getenv("BOT_TOKEN")
API_TOKEN = "1701039985:AAEHbr0waUEnpaFOh-1hGbd5e74ivse0nk8"

ADMINS_ID = [1404657362, ]

JWT_SECRET = "belicoffneloh"  # ur secret text for encoding!

HOST = "http://127.0.0.1"

ADMINS_CHAT = -563820238
WORKERS_CHAT = 0
OUTS_CHAT = 0

outs_link = "https://t.me/hideteamout"
workers_link = "https://t.me/joinchat/Ripr9Br_8UcEw-fg"
reviews_link = "https://t.me/joinchat/xdsxXRzqhFhmNDAy"

'''
    Кастомизация
        Уровни
    
'''

StatusNames = [
    "Без статуса",
    "Заблокирован",
    "Воркер",
    "Саппорт",
    "Админ",
    "Кодер",
    "ТС",
    "Dungeon Master",
]

LevelNames = [
    "Новичок",
    "Уже смешарик",
    "Опытный",
    "Професионал",
    "Бог"
]

Rates = [  # виды ставок первая - стандартная
    (75, 65, 55),
    (70, 60, 60),
    (80, 70, 50),
]

TIME_ZONE = 'Europe/Moscow'  # часовой пояс бота +3utc
