from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


cancel_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_button = KeyboardButton(emojize("Назад"))
cancel_keyboard.add(cancel_button)


def pay_accept(pay_id: int) -> InlineKeyboardMarkup:
    """pay_id - id of CasinoPayment in base"""
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            emojize(":white_check_mark: Оплатить"), callback_data=f"casadd_{pay_id}"
        )
    )

    return markup
