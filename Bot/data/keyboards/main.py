from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from config import config


# worker panel
menu_keyboard = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
profile_btn = KeyboardButton(emojize(":woman_tipping_hand: Мой профиль"))
casino_btn = KeyboardButton(emojize(":slot_machine: Казино"))
traiding_btn = KeyboardButton(emojize(":chart_with_upwards_trend: Трейдинг"))
escort_btn = KeyboardButton(emojize(":gift_heart: Эскорт"))
about_btn = KeyboardButton(emojize(":woman_technologist: О проекте"))
menu_keyboard.add(profile_btn)
menu_keyboard.add(casino_btn, traiding_btn, escort_btn)
menu_keyboard.add(about_btn)


render_btn = InlineKeyboardButton(
    emojize("Отрисовка :receipt:"),
    callback_data="render",
)


def panel_keyboard(namehide) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    username_btn = InlineKeyboardButton(
        f'{"Открыть" if namehide else "Скрыть"} никнейм в выплатах',
        callback_data="toggleusername",
    )
    markup.add(username_btn)
    markup.add(render_btn)

    return markup


about_project_keyboard = InlineKeyboardMarkup()
ref_btn = InlineKeyboardButton(
    emojize(":handshake: Реф. система"), callback_data="refsystem"
)
rules_btn = InlineKeyboardButton(emojize(":scroll: Правила"), callback_data="showrules")
out_btn = InlineKeyboardButton(
    emojize(":money_with_wings: Выплаты"), url=config("outs_link")
)
info_btn = InlineKeyboardButton(
    emojize(":wastebasket: Инфоканал"), url=config("reviews_link")
)
chat_btn = InlineKeyboardButton(
    emojize(":dolphin: Чат воркеров"), url=config("workers_link")
)
about_project_keyboard.add(ref_btn, rules_btn)
about_project_keyboard.add(info_btn, out_btn)
about_project_keyboard.add(chat_btn)


cas_mamoths_btn = InlineKeyboardButton(
    emojize("Мои мамонтята :elephant:"),
    callback_data="mamonths_cas",  #
)
cas_promos_btn = InlineKeyboardButton(
    emojize("Мои промокоды :receipt:"), callback_data="promos_cas"
)
# cas_fraze_btn = InlineKeyboardButton(
#     emojize("Свои фразы при выводе :book:"), callback_data="frazes_cas"
# )
cas_msg_spam_btn = InlineKeyboardButton(
    emojize("Массовая рассылка :diamond_shape_with_a_dot_inside:"),
    callback_data="all_alerts_cas",
)
cas_delete_all_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="delete_all_cas"
)


def casino_keyboard(min_dep: int):
    markup = InlineKeyboardMarkup()
    markup.add(cas_mamoths_btn)
    markup.add(cas_promos_btn)
    # markup.add(cas_fraze_btn)
    markup.add(cas_msg_spam_btn)
    markup.add(cas_delete_all_btn)

    cas_mindep_btn = InlineKeyboardButton(
        emojize(f"Минималка: {min_dep} RUB :money_with_wings:"),
        callback_data="mindep_cas",
    )

    markup.add(cas_mindep_btn)

    return markup


esc_mamoths_btn = InlineKeyboardButton(
    emojize("Мои мамонтята :elephant:"), callback_data="mamonths_esc"
)
esc_msg_spam_btn = InlineKeyboardButton(
    emojize("Массовая рассылка :diamond_shape_with_a_dot_inside:"),
    callback_data="all_alerts_esc",
)
esc_create_form = InlineKeyboardButton(
    emojize(":envelope: Создать анкету :envelope:"), callback_data="create_form_esc"
)
esc_delete_all_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="delete_all_esc"
)

escort_keyboard = InlineKeyboardMarkup()
escort_keyboard.add(esc_mamoths_btn)
escort_keyboard.add(esc_create_form)
escort_keyboard.add(esc_msg_spam_btn)
escort_keyboard.add(esc_delete_all_btn)

escort_form_keyboard = ReplyKeyboardMarkup(
    one_time_keyboard=False, resize_keyboard=True
)
escort_form_end_btn = KeyboardButton(emojize("Создать анкету"))
escort_form_back_btn = KeyboardButton(emojize("Назад"))
escort_form_keyboard.add(escort_form_end_btn)
escort_form_keyboard.add(escort_form_back_btn)

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
        emojize(":arrows_counterclockwise:"), callback_data=f"updateinfo_{uid}"
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
        emojize(":arrows_counterclockwise:"), callback_data=f"updatemamonths_{page}"
    )

    # 51 rows - 3 pages
    if rows_count > row_width:
        max_pages_count = int((rows_count + rows_count % row_width) / row_width)
        assert max_pages_count >= page and page > 0  # assertation epta

        back_num = page - 1 if page - 1 > 0 else max_pages_count
        next_num = 1 if page + 1 > max_pages_count else page + 1

        back_btn = InlineKeyboardButton(
            f"[{back_num}/{max_pages_count}]",
            callback_data=f"updatemamonths_{back_num}",
        )
        next_btn = InlineKeyboardButton(
            f"[{next_num}/{max_pages_count}]",
            callback_data=f"updatemamonths_{next_num}",
        )
        markup.add(back_btn, update_btn, next_btn)
    else:
        markup.add(update_btn)

    return markup
