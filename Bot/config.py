import os
from hashlib import md5

from loguru import logger
from customutils.confparse import Config


path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../config.cfg"))
section_name = "Settings"

# than change as jwt access
secrethash = md5("secretpass".encode()).hexdigest()

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
    "time_zone": "Europe/Moscow",
    "casino_work": "0",
    "escort_work": "0",
    "trading_work": "0",
    "adv_team_photo": "AgACAgIAAxkBAAIL-WENYLIp8iRCBBUqsWPZK3Vk7fPPAAKyuDEbA6toSNh2SVkwoqY0AQADAgADeQADIAQ",
    "pin_path": "pin.txt",
    "pin_update_time": "15",
    "fake_cards": "u5375414101206471,r5469490010637672",
    "fake_numbers": "u380972412167,r79916219242,r79916675522,r79621768186",
    "team_name": "Bless Team",
    "outs_link": "https://t.me/joinchat/0K4ig3Lm-4EzNzc6",
    "workers_link": "https://t.me/joinchat/6-4rJOpD17s4Y2Ey",
    "reviews_link": "https://t.me/blessinform",
    "profit_render_color": "240,230,100,255",
}

config = Config(section_name, path, standart_config)

html_style_url = "https://telegra.ph/file/0e91498d70cfc4d87afba.png"  # than i replace!


team_start = "3 сентября 2021"

"""
    Кастомизация
        Уровни

"""

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

ServiceNames = ["Казино", "Эскорт", "Трейдинг", "Прямой перевод"]

Rates = [  # виды ставок первая - стандартная
    (75, 65, 55),
    (70, 60, 60),
    (80, 70, 50),
]

# useless
SKIP_UPDATES = True
