from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


add_qiwi_btn = InlineKeyboardButton(
    emojize("Добавить киви :information_source:"), callback_data="qiwiadd"
)


def add_qiwi_keyboard(qiwi_numbers: list = None):
    markup = InlineKeyboardMarkup()

    if qiwi_numbers is not None:
        for i, number in enumerate(qiwi_numbers):
            if i == 0:
                number = emojize(f":sparkle: {number}")

            markup.add(InlineKeyboardButton(number, callback_data=f"qiwi_{i}"))

    markup.add(add_qiwi_btn)

    return markup


add_qiwi_sure_keyboard = InlineKeyboardMarkup()
add_qiwi_sure_keyboard.add(add_qiwi_btn)


def oneqiwi_keyboard(num):
    markup = InlineKeyboardMarkup()

    add_proxy_btn = InlineKeyboardButton(
        emojize("Добавить прокси :diamond_shape_with_a_dot_inside:"),
        callback_data=f"addproxy_{num}",
    )
    delete_qiwi_btn = InlineKeyboardButton(
        emojize("Удалить :x:"), callback_data=f"qiwidelete_{num}"
    )
    back_btn = InlineKeyboardButton("Назад", callback_data="backqiwi")

    markup.add(add_proxy_btn)
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
