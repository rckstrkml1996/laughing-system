import sys
import asyncio

from pyrogram import Client
from pyrogram.session import Session
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from utils.pinner import DynamicPinner
from utils.basefunctional import BaseCommands
from utils.payments_checker import PayChecker
from customutils.config import BotConfig

"""
    bot settings:
        inline mode                         -   on
        allow groups                        -   on
        group privacy                       -   off
        workers and outs and admins chats   -   make bot admin!
"""

config = BotConfig()

# for aiohttp connection by proxy, too slow for windows :(
if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.SelectorEventLoop())

loop = asyncio.get_event_loop()

bot = Bot(config.api_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

db_commands = BaseCommands()
payments_checker = PayChecker(config.qiwi_check_time)
dynapinner = DynamicPinner(config, bot)

Session.notice_displayed = True  # fucking notice zaebala
banker_client = Client("banker_client", config.api_id, config.api_hash)
bot_client = Client("bot_client", config.api_id, config.api_hash)

# is no webhooks so it can be here)
casino_bot = Bot(config.casino_api_token, parse_mode=ParseMode.HTML)
trading_bot = Bot(config.trading_api_token, parse_mode=ParseMode.HTML)
escort_bot = Bot(config.escort_api_token, parse_mode=ParseMode.HTML)


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

ServiceNames = ["Казино", "Эскорт", "Трейдинг", "Прямой перевод"]

alowed_values = [100, 300, 500, 750, 1000, 1500, 3000, 5000, 10000]

MinDepositValues = [config.min_deposit]
for val in alowed_values:
    if MinDepositValues[0] < val:
        MinDepositValues.append(val)


# useless
BTC_REGEX = r"BTC_CHANGE_BOT\?start=(c_[a-f0-9]{32})"
