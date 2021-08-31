import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from config import config

# Обьявление всех компонентов бота из конфига


bot = Bot(config("casino_api_token"), parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

main_bot = Bot(config("api_token"), parse_mode=ParseMode.HTML)
