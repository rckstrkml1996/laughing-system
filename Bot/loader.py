from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from py_expression_eval import Parser

from utils.basefunctional import BaseCommands
from config import config

# Обьявление всех компонентов бота из конфига
# Обьявление expression eval парсера
# Обьявление functional models

bot = Bot(config("api_token"), parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

db_commands = BaseCommands()

exp_parser = Parser()


# is no webhooks so it can be here)
casino_bot = Bot(config("casino_api_token"), parse_mode=ParseMode.HTML)
