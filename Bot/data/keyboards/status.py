from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_status_keyboard(
    status_names: list, worker_id: int, i: int
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for j, status_name in enumerate(status_names[:i]):
        markup.add(InlineKeyboardButton(status_name, callback_data=f"w{worker_id}_{j}"))

    return markup
