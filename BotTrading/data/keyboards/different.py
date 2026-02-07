from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_game
from aiogram.utils.emoji import emojize


def main_accept_out_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """user_id - id of TradingUser in database"""
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            emojize(":white_check_mark: Вывести"), callback_data=f"tdgout_{user_id}"
        )
    )

    return markup


def main_accept_add_keyboard(pay_id: int) -> InlineKeyboardMarkup:
    """pay_id - id of TradingPayment in database"""
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            emojize(":white_check_mark: Оплатить"), callback_data=f"tdgadd_{pay_id}"
        )
    )

    return markup
