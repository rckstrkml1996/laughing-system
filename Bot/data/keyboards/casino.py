from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


cas_mamoths_btn = InlineKeyboardButton(
    emojize("Мои мамонтята :elephant:"),
    callback_data="casupdatemamonths_0",  #
)
# cas_promos_btn = InlineKeyboardButton(
#     emojize("Мои промокоды :receipt:"), callback_data="promos_cas"
# )
cas_msg_spam_btn = InlineKeyboardButton(
    emojize("Рассылка мамонтам :diamond_shape_with_a_dot_inside:"),
    callback_data="all_alert_cas",
)
cas_delete_all_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="delete_all_cas"
)


def casino_keyboard(min_dep: int):
    markup = InlineKeyboardMarkup()
    markup.add(cas_mamoths_btn)
    # markup.add(cas_promos_btn)
    # markup.add(cas_fraze_btn)
    markup.add(cas_msg_spam_btn)
    markup.add(cas_delete_all_btn)

    cas_mindep_btn = InlineKeyboardButton(
        emojize(f"Минималка: {min_dep} RUB :money_with_wings:"),
        callback_data="mindep_cas",
    )

    markup.add(cas_mindep_btn)

    return markup


def cas_info_keyboard(uid, fart, minpay, stopped: bool) -> InlineKeyboardMarkup:
    stopped = "Вкл" if stopped else "Выкл"

    markup = InlineKeyboardMarkup()
    cas_fart_btn = InlineKeyboardButton(
        f"Фарт: {fart} %", callback_data=f"updatefart_{uid}"
    )
    cas_min_btn = InlineKeyboardButton(
        f"Мин: {minpay} RUB", callback_data=f"updatemin_{uid}"
    )
    cas_stop_btn = InlineKeyboardButton(
        f"Тех работы: {stopped}", callback_data=f"updatestopped_{uid}"
    )
    cas_info_update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"casupdateinfo_{uid}"
    )
    markup.add(cas_fart_btn, cas_min_btn)
    markup.add(cas_stop_btn)
    markup.add(cas_info_update_btn)

    return markup


# fullcoded nahui by @ukhide
def casino_mamonths_keyboard(
    rows_count: int, page: int = 1, row_width=20
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"casupdatemamonths_{page}"
    )

    # 51 rows - 3 pages
    if rows_count > row_width:
        max_pages_count = int((rows_count + rows_count % row_width) / row_width)
        assert max_pages_count >= page and page > 0  # assertation epta

        back_num = page - 1 if page - 1 > 0 else max_pages_count
        next_num = 1 if page + 1 > max_pages_count else page + 1

        back_btn = InlineKeyboardButton(
            f"[{back_num}/{max_pages_count}]",
            callback_data=f"casupdatemamonths_{back_num}",
        )
        next_btn = InlineKeyboardButton(
            f"[{next_num}/{max_pages_count}]",
            callback_data=f"casupdatemamonths_{next_num}",
        )
        markup.add(back_btn, update_btn, next_btn)
    else:
        markup.add(update_btn)

    return markup
