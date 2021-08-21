from os import getenv
from loguru import logger
import os
from customutils.confparse import Config

path = '../config.cfg'
section_name = "Settings"

token = os.getenv("BOT_TOKEN")  # or set it into config.cfg file))
if token is None:
    logger.warning("TOKEN DOES NOT SET IN ENV")

standart_config = {
    "trading_api_token": token,
    "outs_chat": "0",
    "base_name": "ur_base_name",
    "base_user": "ur_base_user",
    "base_password": "ur_base_password",
    "min_deposit": "300",
    "min_withdraw": "800",
    "bet_timer": "5"
}

config = Config(section_name, path, standart_config)

outs_link = "https://t.me/hideteamout"
workers_link = "https://t.me/joinchat/oV_2yUpUrA1kZThi"
reviews_link = "https://t.me/joinchat/xdsxXRzqhFhmNDAy"

'''
    Кастомизация
        Уровни
    
'''

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
    "eth": "AgACAgIAAxkBAAIER2Ee5pa3AAEl99zE1MpWE8ClvVIU_wACarUxG45a8EiYI8ytJ8__5wEAAwIAA3gAAyAE",
    "btc": "AgACAgIAAxkBAAIESWEe5siMGRlXCzWXHQOCKNIN5wnnAAJrtTEbjlrwSOWIXTIpKzIkAQADAgADeAADIAQ",
    "ltc": "AgACAgIAAxkBAAIES2Ee5tYEGsrGPuHP_zSFPreRbCgdAAJstTEbjlrwSFOEYGkLcVV_AQADAgADeQADIAQ",
    "qtm": "AgACAgIAAxkBAAIETWEe5u4hgnAcLUExP_yluQ00N1cVAAJttTEbjlrwSJMSyVIJiJtTAQADAgADeAADIAQ",
    "trx": "AgACAgIAAxkBAAIET2Ee5wdP_WZvPm54vuC30CBtlhq4AAJutTEbjlrwSHavzUQqEGafAQADAgADeAADIAQ",
    "xrp": "AgACAgIAAxkBAAIEUWEe5yHruN0VN2R8kxSeTvKPg1jKAAJvtTEbjlrwSC4OfuFLDNhUAQADAgADeQADIAQ"
}

# useless
SKIP_UPDATES = True
