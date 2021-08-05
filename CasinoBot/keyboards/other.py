from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.emoji import emojize


cancel_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_button = KeyboardButton(emojize("Назад :arrow_up:"))
cancel_keyboard.add(cancel_button)
