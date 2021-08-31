from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


cancel_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_button = KeyboardButton(emojize("Назад"))
cancel_keyboard.add(cancel_button)


def pay_accept(pid):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            emojize("Принять :sparkle:"), callback_data=f"payaccept_{pid}"
        )
    )
    return markup
