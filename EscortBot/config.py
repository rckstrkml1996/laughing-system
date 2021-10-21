from os import path

from customutils.confparse import Config


config_path = path.normpath(path.join(path.dirname(__file__), "../config.cfg"))
section_name = "Settings"


standart_config = {
    "escort_api_token": "urtoken",
    "skip_updates": "1",
}

config = Config(section_name, config_path, standart_config)
