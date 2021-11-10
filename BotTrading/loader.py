from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from aiogram.types import ParseMode

from customutils import BotsConfig
from utils.currencies.main import CurrencyWorker


config = BotsConfig()

currency_worker = CurrencyWorker()

loop = asyncio.get_event_loop()

bot = Bot(token=config.trading_api_token, loop=loop, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

main_bot = Bot(token=config.api_token, parse_mode=ParseMode.HTML)
