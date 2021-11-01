import sys
import asyncio

from customutils import BotsConfig
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

if sys.platform == "win32":
    # print("Debug - win32")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


config = BotsConfig()

bot = Bot(config.casino_api_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

main_bot = Bot(config.api_token, parse_mode=ParseMode.HTML)
