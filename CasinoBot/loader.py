import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from loguru import logger

from qiwi import QApi
from config import settings

"""
Обьявление всех компонентов бота из конфига
"""

loop = asyncio.get_event_loop()

bot = Bot(settings.CAS_API_TOKEN, parse_mode=ParseMode.HTML, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())

qiwis = {}

if settings.CAS_QIWI_ACCOUNTS and settings.CAS_QIWI_TOKENS:
    for i in range(len(config.CAS_QIWI_ACCOUNTS)):
        qiwis[settings.CAS_QIWI_ACCOUNTS[i]] = QApi(
            token=settings.CAS_QIWI_TOKENS[i], account=settings.CAS_QIWI_ACCOUNTS[i])

logger.info(qiwis)
