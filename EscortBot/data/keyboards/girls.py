from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from utils.executional import get_escort_girls

back_welcome_btn = InlineKeyboardButton(
    emojize("Вернуться :leftwards_arrow_with_hook:"), callback_data="welcome"
)


def girls_choice_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    girls = get_escort_girls()  # EscortGirl

    for girl in girls:
        print(girl)

    markup.add(back_welcome_btn)
    return markup
