from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode


bot = Bot("1918772845:AAEhg3PiH6u7ElEmQ4_GP_4OuAPyrGCmIBk", parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())