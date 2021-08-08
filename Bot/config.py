import configparser
import os

from loguru import logger
from confparse import Config


path = '../config.cfg'
section_name = "Settings"

token = os.getenv("BOT_TOKEN")  # or set it into config.cfg file))
if token is None:
    logger.warning("TOKEN DOES NOT SET IN ENV")

standart_config = {
    "api_token": token,
    "admins_id": "1404657362,1747481892",
    "admins_chat": "-563820238",
    "workers_chat": "-577009620",
    "outs_chat": "0",
    "base_name": "ur_base_name",
    "base_user": "ur_base_user",
    "base_password": "ur_base_password",
    "casino_work": "0",
    "escort_work": "0",
    "antikino_work": "0",
    "adv_team_photo": "AgACAgIAAxkBAAIL-WENYLIp8iRCBBUqsWPZK3Vk7fPPAAKyuDEbA6toSNh2SVkwoqY0AQADAgADeQADIAQ",
}

config = Config(section_name, path, standart_config)


outs_link = "https://t.me/hideteamout"
workers_link = "https://t.me/joinchat/Ripr9Br_8UcEw-fg"
reviews_link = "https://t.me/joinchat/xdsxXRzqhFhmNDAy"


BASE_NAME = "bot"
BASE_USER = "belicoff"
BASE_PASSWORD = "belicoffdev"

ADMINS_CHAT = -563820238
WORKERS_CHAT = -560381349


TIME_ZONE = 'Europe/Moscow'  # часовой пояс бота +3utc

team_start = "1 апреля 1991"

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

# useless
SKIP_UPDATES = True
