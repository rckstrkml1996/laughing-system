from os import getenv
from loguru import logger
import os
from customutils.confparse import Config

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
    "min_deposit" : "300",
    "min_withdraw" : "800"
}

config = Config(section_name, path, standart_config)


outs_link = "https://t.me/hideteamout"
workers_link = "https://t.me/joinchat/oV_2yUpUrA1kZThi"
reviews_link = "https://t.me/joinchat/xdsxXRzqhFhmNDAy"

TIME_ZONE = 'Europe/Moscow'  # часовой пояс бота +3utc

'''
    Кастомизация
        Уровни
    
'''

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