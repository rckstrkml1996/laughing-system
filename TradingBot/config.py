from loguru import logger
from customutils.confparse import Config
import os


path = "../config.cfg"
section_name = "Settings"

directory = os.path.dirname(os.path.abspath(__file__))

token = os.getenv("BOT_TOKEN")  # or set it into config.cfg file))
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
    "support_username": "@tradesup_bot",
}

config = Config(section_name, path, standart_config)

# useless
SKIP_UPDATES = True


currencies = {
    "Bitcoin": "btc",
    "Qtum": "qtm",
    "Ethereum": "eth",
    "Tron": "trx",
    "Litecoin": "ltc",
    "Ripple": "xrp",
}

photos = {
    "eth": os.path.join(directory, "data", "images", "etc.jpg"),
    "btc": os.path.join(directory, "data", "images", "btc.jpg"),
    "ltc": os.path.join(directory, "data", "images", "ltc.jpg"),
    "qtm": os.path.join(directory, "data", "images", "otm.jpg"),
    "trx": os.path.join(directory, "data", "images", "trn.jpg"),
    "xrp": os.path.join(directory, "data", "images", "rpl.jpg"),
}
