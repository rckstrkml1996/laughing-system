import sys
import asyncio

from pyrogram import Client
from pyrogram.session import Session
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from utils.pinner import DynamicPinner
from utils.payments_checker import PayChecker
from customutils.config import BotsConfig

"""
    bot settings:
        inline mode                         -   on
        allow groups                        -   on
        group privacy                       -   off
        workers and outs and admins chats   -   make bot admin!
"""

config = BotsConfig()

# for aiohttp connection by proxy, too slow for windows :(
# if sys.platform == "win32":
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

loop = asyncio.get_event_loop()

bot = Bot(config.api_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

# is no webhooks so it can be here)
casino_bot = Bot(config.casino_api_token, parse_mode=ParseMode.HTML)
trading_bot = Bot(config.trading_api_token, parse_mode=ParseMode.HTML)
escort_bot = Bot(config.escort_api_token, parse_mode=ParseMode.HTML)

payments_checker = PayChecker(bot, config)
dynapinner = DynamicPinner(bot, config)

Session.notice_displayed = True  # fucking notice zaebala
banker_client = Client("clbanker_client", config.api_id, config.api_hash)
bot_client = Client("clbot_client", config.api_id, config.api_hash)

StatusNames = [
    "Без статуса",
    "Заблокирован",
    "Воркер",
    "Модер",
    "Сапорт ТП",
    "Кодер",
    "ТС",
    "Dungeon Master",
]

alowed_values = [100, 300, 500, 750, 1000, 1500, 3000, 5000, 10000]

MinDepositValues = [config.min_deposit]
for val in alowed_values:
    if MinDepositValues[0] < val:
        MinDepositValues.append(val)


# useless
BTC_REGEX = r"BTC_CHANGE_BOT\?start=(c_[a-f0-9]{32})"
