from os import getenv
from loguru import logger
from customutils.confparse import Config

path = "../config.cfg"
section_name = "Settings"

token = getenv("BOT_TOKEN")  # or set it into config.cfg file))
if token is None:
    logger.warning("TOKEN DOES NOT SET IN ENV")

standart_config = {
    "trading_api_token": token,
    "admins_id": "1644048831,1404657362",
    "admins_chat": "-563820238",
    "workers_chat": "-577009620",
    "outs_chat": "0",
    "base_name": "ur_base_name",
    "base_user": "ur_base_user",
    "base_password": "ur_base_password",
    "min_deposit": "300",
    "min_withdraw": "800",
    "bet_timer": "5",
    "support_username": "@tradesup_bot"
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
    "Bitcoin": "btc",
    "Qtum": "qtm",
    "Ethereum": "eth",
    "Tron": "trx",
    "Litecoin": "ltc",
    "Ripple": "xrp"
}

photos = {
    "eth": "./data/images/etc.jpg",
    "btc": "./data/images/btc.jpg",
    "ltc": "./data/images/ltc.jpg",
    "qtm": "./data/images/otm.jpg",
    "trx": "./data/images/trn.jpg",
    "xrp": "./data/images/rpl.jpg"
}
