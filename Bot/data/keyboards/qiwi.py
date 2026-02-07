from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


qiwi_add_cancel_keyboard = InlineKeyboardMarkup()
qiwi_add_btn = InlineKeyboardButton(
    emojize("Отменить :arrow_heading_up:"), callback_data="qiwiaddcancel"
)
qiwi_add_cancel_keyboard.add(qiwi_add_btn)

add_qiwi_btn = InlineKeyboardButton(
    emojize("Добавить киви :information_source:"), callback_data="qiwiadd"
)


def qiwi_keyboard(qiwi_numbers: list = None):
    markup = InlineKeyboardMarkup()

    if qiwi_numbers is not None:
        for i, number in enumerate(qiwi_numbers):
            markup.add(InlineKeyboardButton(number, callback_data=f"qiwi_{i}"))

    markup.add(add_qiwi_btn)

    return markup


def qiwi_info_keyboard(num: int):
    markup = InlineKeyboardMarkup()

    delete_qiwi_btn = InlineKeyboardButton(
        emojize("Удалить :x:"), callback_data=f"qiwidelete_{num}"
    )
    back_btn = InlineKeyboardButton("Вернуться", callback_data=f"backqiwi")

    markup.add(delete_qiwi_btn)
    markup.add(back_btn)

    return markup


def qiwi_delete_keyboard(num):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            emojize("Уверен :wastebasket:"),
            callback_data=f"suredelete_{num}",
        )
    )
    markup.add(InlineKeyboardButton("Отмена", callback_data="cancel"))

    return markup
