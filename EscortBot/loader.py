import asyncio

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from loguru import logger

from data import config

"""
Обьявление всех компонентов бота из конфига
"""

loop = asyncio.get_event_loop()

bot = Bot(config.API_TOKEN, parse_mode=ParseMode.HTML, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())
