from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


tdng_mamoths_btn = InlineKeyboardButton(
    emojize("Мои мамонтята :elephant:"), callback_data="mamonths_tdng"
)
tdng_fraze_btn = InlineKeyboardButton(
    emojize("Свои фразы при выводе :book:"), callback_data="frazes_tdng"
)
tdng_msg_spam_btn = InlineKeyboardButton(
    emojize("Массовая рассылка :diamond_shape_with_a_dot_inside:"),
    callback_data="all_alerts_tdng",
)
tdng_delete_all_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="delete_all_tdng"
)
trading_keyboard = InlineKeyboardMarkup()
trading_keyboard.add(tdng_mamoths_btn)
trading_keyboard.add(tdng_fraze_btn)
trading_keyboard.add(tdng_msg_spam_btn)
trading_keyboard.add(tdng_delete_all_btn)


def trading_mamonths_keyboard(
    rows_count: int, page: int = 1, row_width=20
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"tdgupdatemamonths_{page}"
    )

    if rows_count > row_width:
        max_pages_count = int((rows_count + rows_count % row_width) / row_width)
        assert max_pages_count >= page and page > 0  # assertation epta

        back_num = page - 1 if page - 1 > 0 else max_pages_count
        next_num = 1 if page + 1 > max_pages_count else page + 1

        back_btn = InlineKeyboardButton(
            f"[{back_num}/{max_pages_count}]",
            callback_data=f"tdgupdatemamonths_{back_num}",
        )
        next_btn = InlineKeyboardButton(
            f"[{next_num}/{max_pages_count}]",
            callback_data=f"tdgupdatemamonths_{next_num}",
        )
        markup.add(back_btn, update_btn, next_btn)
    else:
        markup.add(update_btn)

    return markup
