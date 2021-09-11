import os

from loguru import logger
from customutils.confparse import Config


path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../config.cfg"))
section_name = "Settings"

token = os.getenv("ESC_TOKEN")  # or set it into config.cfg file))
if token is None:
    token = ""
    logger.warning("TOKEN DOES NOT SET IN ENV")

standart_config = {
    "esc_otz_chat": "otzif",
    "escort_api_token": token,
    "escort_sup_username": "@escort18support",
}

config = Config(section_name, path, standart_config)
