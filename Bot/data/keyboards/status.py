from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import StatusNames


def new_status_keyboard(worker_id, i: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for j, status_name in enumerate(StatusNames[:i]):
        markup.add(InlineKeyboardButton(status_name, callback_data=f"w{worker_id}_{j}"))

    return markup
