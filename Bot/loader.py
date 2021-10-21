from pyrogram import Client
from pyrogram.session import Session

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from py_expression_eval import Parser

from utils.basefunctional import BaseCommands
from config import config

# Обьявление всех компонентов бота из конфига
# Обьявление expression eval парсера
# Обьявление functional models
# Обьявление banker_client Pyrogram

# bot settings:
# inline mode - on
# allow groups - on
# group privacy - off

# workers and outs and admins chats - make bot admin!

bot = Bot(config("api_token"), parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

db_commands = BaseCommands()

exp_parser = Parser()

Session.notice_displayed = True  # fucking notice zaebala
banker_client = Client("banker_client", config("api_id"), config("api_hash"))
bot_client = Client("bot_client", config("api_id"), config("api_hash"))

# is no webhooks so it can be here)
casino_bot = Bot(config("casino_api_token"), parse_mode=ParseMode.HTML)
trading_bot = Bot(config("trading_api_token"), parse_mode=ParseMode.HTML)
escort_bot = Bot(config("escort_api_token"), parse_mode=ParseMode.HTML)

# casino_client = Client("casino_client", config("api_id"), config("api_hash"))
