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


def panel_keyboard(namehide):
    markup = InlineKeyboardMarkup()
    username_btn = InlineKeyboardButton(
        f'{"Открыть" if namehide else "Скрыть"} никнейм в выплатах',
        callback_data="toggleusername",
    )
    markup.add(username_btn)

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


casino_keyboard = InlineKeyboardMarkup()

my_mamoths_btn = InlineKeyboardButton(
    emojize("Мои мамонтята :elephant:"), callback_data="my_mamonths"
)
promos_btn = InlineKeyboardButton(
    emojize("Мои промокоды :receipt:"), callback_data="my_promos"
)
my_fraze_btn = InlineKeyboardButton(
    emojize("Свои фразы при выводе :book:"), callback_data="my_frazes"
)
msgspam_btn = InlineKeyboardButton(
    emojize("Массовая рассылка :diamond_shape_with_a_dot_inside:"),
    callback_data="my_all_alerts",
)
deleteall_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="my_delete_all"
)

casino_keyboard.add(my_mamoths_btn)
casino_keyboard.add(promos_btn)
casino_keyboard.add(my_fraze_btn)
casino_keyboard.add(msgspam_btn)
casino_keyboard.add(deleteall_btn)


cancel_keyboard = InlineKeyboardMarkup()
cancel_btn = InlineKeyboardButton("Отмена нахуй", callback_data="cancel")
cancel_keyboard.add(cancel_btn)


escort_keyboard = InlineKeyboardMarkup()
create_form = InlineKeyboardButton(
    emojize(":envelope: Создать анкету :envelope:"), callback_data="none"
)

escort_keyboard.add(my_mamoths_btn)
escort_keyboard.add(create_form)
escort_keyboard.add(msgspam_btn)
escort_keyboard.add(deleteall_btn)

trading_keyboard = InlineKeyboardMarkup()
my_phrases = InlineKeyboardButton(
    emojize(":open_book: Свои фразы при выводе :open_book:"), callback_data="none"
)

trading_keyboard.add(my_mamoths_btn)
trading_keyboard.add(my_phrases)
trading_keyboard.add(msgspam_btn)
trading_keyboard.add(deleteall_btn)


def cas_info_keyboard(fart, uid, minpay):
    markup = InlineKeyboardMarkup()
    cas_fart_btn = InlineKeyboardButton(
        f"Фарт: {fart} %", callback_data=f"casupdatefart_{uid}"
    )
    cas_min_btn = InlineKeyboardButton(
        f"Мин: {minpay} RUB", callback_data=f"updatemin_{uid}"
    )
    cas_info_update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"casupdateinfo_{uid}"
    )
    markup.add(cas_fart_btn, cas_min_btn)
    markup.add(cas_info_update_btn)

    return markup
