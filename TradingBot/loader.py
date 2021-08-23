from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from config import config


bot = Bot(config("trading_api_token"), parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
