import configparser
import os

from loguru import logger
from customutils.confparse import Config


path = '../config.cfg'
section_name = "Settings"

token = os.getenv("BOT_TOKEN")  # or set it into config.cfg file))
if token is None:
    logger.warning("TOKEN DOES NOT SET IN ENV")

standart_config = {
    "api_token": token,
    "admins_id": "1644048831,1404657362",
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
    "pin_path": "pin.txt",
    "pin_update_time": "15",
    "fake_cards": "u5375414101206471,r5469490010637672",
    "fake_numbers": "u380972412167,r79916219242,r79916675522,r79621768186",
}

config = Config(section_name, path, standart_config)


outs_link = "https://t.me/hideteamout"
workers_link = "https://t.me/joinchat/oV_2yUpUrA1kZThi"
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
