import configparser
import os
import time

path = '../config.cfg'
section_name = "Settings"

token = os.getenv("BOT_TOKEN")  # or set it into config.cfg file))

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


def create_config():
    if token is None:
        print("token is None, check it")
        exit(0)
        return

    config = configparser.ConfigParser()
    config.add_section(section_name)

    for key, val in standart_config.items():
        config.set(section_name, key, val)

    with open(path, "w") as config_file:
        config.write(config_file)


def restrict_config():
    config = configparser.ConfigParser()
    config.read(path)

    for key, val in standart_config.items():
        try:
            config.get(section_name, key)
        except configparser.NoOptionError:
            config.set(section_name, key, val)

    with open(path, "w") as config_file:
        config.write(config_file)


def check_config_file():
    if not os.path.exists(path):
        create_config()
        print('Config created')


def config(what):
    config = configparser.ConfigParser()
    config.read(path)

    value = config.get(section_name, what)
    if "," in value:
        return list(map(lambda i: int(i) if i.replace("-", "").isdigit() else i, value.split(",")))
    try:
        value = int(value)
        if value == 1 or value == 0:
            return bool(value)
        return value
    except ValueError:
        return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path)

    if isinstance(value, bool):
        value = str(int(value))
    elif isinstance(value, int):
        value = str(int(value))
    elif isinstance(value, list):
        value = ",".join(map(lambda i: str(i), value))

    config.set(section_name, setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)


check_config_file()
restrict_config()


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
