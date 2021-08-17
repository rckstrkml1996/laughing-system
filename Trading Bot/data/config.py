from os import getenv
from loguru import logger
import os
from customutils.confparse import Config


API_TOKEN = "1918772845:AAEhg3PiH6u7ElEmQ4_GP_4OuAPyrGCmIBk"

SKIP_UPDATES = True

ADMINS_ID = [1644048831]

MIN_WITHDRAW = 800
MIN_DEPOSIT = 300

QIWI_TOKENS = getenv("QIWI_TOKENS")
if not QIWI_TOKENS:
	logger.error("Please specify the qiwi token... env variable - QIWI_TOKENS")
else:
	QIWI_TOKENS = [x for x in QIWI_TOKENS.split(";") if x] # среда

QIWI_ACCOUNTS = getenv("QIWI_ACCOUNTS")
if not QIWI_ACCOUNTS:
	logger.error("Please specify the qiwi token... env variable - QIWI_ACCOUNTS")
else:
	QIWI_ACCOUNTS = [x for x in QIWI_ACCOUNTS.split(";") if x] # пополнение в боте - сюда
	if len(QIWI_TOKENS) != len(QIWI_ACCOUNTS):
		logger.error("Value of tokens dont suply value of numbers")

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


logger.debug("Setup succes!")

currencies = {
	"Bitcoin" : "btc",
	"Qtum" : "qtm",
	"Ethereum" : "eth",
	"Tron" : "trx",
	"Litecoin" : "ltc",
	"Ripple" : "xrp"
}