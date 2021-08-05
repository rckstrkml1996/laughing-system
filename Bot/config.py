import configparser
import os
import time

path = 'config.cfg'
section_name = "Settings"


def create_config():
    token = os.getenv("BOT_TOKEN")  # or set it into config.cfg file))
    if not token:
        print("token is not String, check it")
        exit(0)
        return

    config = configparser.ConfigParser()
    config.add_section(section_name)
    config.set(section_name, "api_token", token)
    config.set(section_name, "admins_id", "1404657362:1747481892")
    config.set(section_name, "admins_chat", "-563820238")
    config.set(section_name, "workers_chat", "-577009620")
    config.set(section_name, "outs_chat", "0")
    config.set(section_name, "base_name", "ur_base_name")
    config.set(section_name, "base_user", "ur_base_user")
    config.set(section_name, "base_password", "ur_base_password")
    config.set(section_name, "casino_work", "0")
    config.set(section_name, "escort_work", "0")
    config.set(section_name, "antikino_work", "0")

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
    if ":" in value:
        return list(map(lambda i: int(i) if i.replace("-", "").isdigit() else i, value.split(":")))
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
        value = ":".join(map(lambda i: str(i), value))

    config.set(section_name, setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)


check_config_file()

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
