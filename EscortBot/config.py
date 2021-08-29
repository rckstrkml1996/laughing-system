import os

from loguru import logger
from customutils.confparse import Config


path = "../config.cfg"
section_name = "Settings"

token = os.getenv("ESC_TOKEN")  # or set it into config.cfg file))
if token is None:
    token = ""
    logger.warning("TOKEN DOES NOT SET IN ENV")

standart_config = {"escort_api_token": token, "escort_sup_username": "@escort18support"}

config = Config(section_name, path, standart_config)
