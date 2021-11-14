from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from aiogram.types import ParseMode

from customutils import Config
from utils.currencies.main import CurrencyWorker


config = Config()

currency_worker = CurrencyWorker("791fdf77-aeae-4a9c-a270-b6f5f29c7b88")

loop = asyncio.get_event_loop()

bot = Bot(token=config.trading_api_token, loop=loop, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

main_bot = Bot(token=config.api_token, parse_mode=ParseMode.HTML)
