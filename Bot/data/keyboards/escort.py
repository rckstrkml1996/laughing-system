from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

# fullcoded nahui by @ukhide
def escort_mamonths_keyboard(
    rows_count: int, page: int = 1, row_width=20
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"escupdatemamonths_{page}"
    )

    # 51 rows - 3 pages
    if rows_count > row_width:
        max_pages_count = int((rows_count + rows_count % row_width) / row_width)
        assert max_pages_count >= page and page > 0  # assertation epta

        back_num = page - 1 if page - 1 > 0 else max_pages_count
        next_num = 1 if page + 1 > max_pages_count else page + 1

        back_btn = InlineKeyboardButton(
            f"[{back_num}/{max_pages_count}]",
            callback_data=f"escupdatemamonths_{back_num}",
        )
        next_btn = InlineKeyboardButton(
            f"[{next_num}/{max_pages_count}]",
            callback_data=f"escupdatemamonths_{next_num}",
        )
        markup.add(back_btn, update_btn, next_btn)
    else:
        markup.add(update_btn)

    return markup


esc_create_girl_keyboard = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True
)
end_btn = KeyboardButton(emojize("Завершить :x:"))
esc_create_girl_keyboard.add(end_btn)

esc_delete_girl_keyboard = InlineKeyboardMarkup()
esc_delete_btn = InlineKeyboardButton(
    emojize("Удалить :x:"), callback_data="delete_form_esc"
)
esc_delete_girl_keyboard.add(esc_delete_btn)

def esc_info_keyboard(uid) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    esc_update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"escupdateinfo_{uid}"
    )
    markup.add(esc_update_btn)

    return markup