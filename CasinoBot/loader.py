import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from loguru import logger

from customutils.qiwiapi import QiwiApi
from config import config

# Обьявление всех компонентов бота из конфига


loop = asyncio.get_event_loop()

bot = Bot(config("casino_api_token"), parse_mode=ParseMode.HTML, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())
