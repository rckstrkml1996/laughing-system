from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from config import outs_link, workers_link, reviews_link, Rates
from utils.executional import num2emoji


def code(key: int):
    markup = InlineKeyboardMarkup()

    used_btn = InlineKeyboardButton("ИСПОЛЬЗОВАН", callback_data=f"code_{key}")

    markup.add(used_btn)

    return markup


"""
summary
"""

summary_start_keyboard = InlineKeyboardMarkup()
new_summary_btn = InlineKeyboardButton(
    emojize(":rocket: Подать заявку"), callback_data="summary"
)
summary_start_keyboard.add(new_summary_btn)

summary_rules_keyboard = InlineKeyboardMarkup()
agree_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Принимаю"), callback_data="agreesummary"
)
summary_rules_keyboard.add(agree_btn)

summary_send_keyboard = InlineKeyboardMarkup()
send_btn = InlineKeyboardButton(
    emojize(":rocket: Отправить"), callback_data="sendsummary"
)
summary_send_keyboard.add(send_btn)


def summary_check_keyboard(chat_id):
    markup = InlineKeyboardMarkup()
    accept_btn = InlineKeyboardButton(
        emojize(":white_check_mark: Принять"), callback_data=f"accept_{chat_id}"
    )
    reject_btn = InlineKeyboardButton(
        emojize(":warning: Отклонить"), callback_data=f"reject_{chat_id}"
    )
    block_btn = InlineKeyboardButton(
        emojize(":no_entry_sign: Заблокировать"), callback_data=f"block_{chat_id}"
    )
    markup.add(accept_btn)
    markup.add(reject_btn, block_btn)

    return markup


summary_blocked_keyboard = InlineKeyboardMarkup()
fuckurself_btn = InlineKeyboardButton(
    emojize(":speak_no_evil: Пойти нахуй!"), callback_data="fuckurself"
)
summary_blocked_keyboard.add(fuckurself_btn)

summary_accepted_keyboard = InlineKeyboardMarkup()
outs_btn = InlineKeyboardButton(
    emojize(":revolving_hearts: Канал выплат"), url=outs_link
)
workers_btn = InlineKeyboardButton(
    emojize(":busts_in_silhouette: Чат воркеров"), url=workers_link
)
reviews_btn = InlineKeyboardButton(
    emojize(":page_with_curl: Канал отзывов"), url=reviews_link
)
summary_accepted_keyboard.add(outs_btn)
summary_accepted_keyboard.add(workers_btn)
summary_accepted_keyboard.add(reviews_btn)

"""
panel
"""
menu_keyboard = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True)
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
        f'{"Открыть" if namehide else "Скрыть"} никнейм в выплатах', callback_data="toggleusername")
    markup.add(username_btn)

    return markup


def admworkstatus_keyboard(work_status):
    markup = InlineKeyboardMarkup()

    change_work_btn = InlineKeyboardButton(
        emojize(
            ":full_moon: Сменить статус" if work_status else ":new_moon: Сменить статус"
        ), callback_data="toggleworkstatus"
    )
    markup.add(change_work_btn)

    return markup


about_project_keyboard = InlineKeyboardMarkup()
ref_btn = InlineKeyboardButton(
    emojize(":handshake: Реф. система"), callback_data="refsystem")
rules_btn = InlineKeyboardButton(
    emojize(":scroll: Правила"), callback_data="showrules")
out_btn = InlineKeyboardButton(
    emojize(":money_with_wings: Выплаты"), url=outs_link)
info_btn = InlineKeyboardButton(
    emojize(":wastebasket: Инфоканал"), url=reviews_link)
chat_btn = InlineKeyboardButton(
    emojize(":dolphin: Чат воркеров"), url=workers_link)
about_project_keyboard.add(ref_btn, rules_btn)
about_project_keyboard.add(info_btn, out_btn)
about_project_keyboard.add(chat_btn)

change_pin_keyboard = InlineKeyboardMarkup()
changeit_btn = InlineKeyboardButton(
    emojize(":pencil2: Изменить закреп"), callback_data="change_pin")
change_pin_keyboard.add(changeit_btn)

new_pin_keyboard = InlineKeyboardMarkup()
newpin_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Сохранить изменения"), callback_data="savepin")
oldpin_btn = InlineKeyboardButton(
    emojize(":x: Не сохранять"), callback_data="unsavepin")
new_pin_keyboard.add(newpin_btn)
new_pin_keyboard.add(oldpin_btn)


casino_keyboard = InlineKeyboardMarkup()

my_mamoths_btn = InlineKeyboardButton(
    emojize(":elephant: Мои мамонтята :elephant:"), callback_data="none")
promos_btn = InlineKeyboardButton(
    emojize(":receipt: Мои промокоды :receipt:"), callback_data="none")
msgspam_btn = InlineKeyboardButton(
    emojize(":diamond_shape_with_a_dot_inside: Массовая рассылка :diamond_shape_with_a_dot_inside:"), callback_data="none")
deleteall_btn = InlineKeyboardButton(
    emojize(":warning: Удалить всех :warning:"), callback_data="none")

casino_keyboard.add(my_mamoths_btn)
casino_keyboard.add(promos_btn)
casino_keyboard.add(msgspam_btn)
casino_keyboard.add(deleteall_btn)


add_qiwi_keyboard = InlineKeyboardMarkup()
add_qiwi_btn = InlineKeyboardButton(
    emojize("Добавить киви :information_source:"), callback_data="add_qiwi")
add_qiwi_keyboard.add(add_qiwi_btn)


def qiwi_keyboard(accounts: list):
    markup = InlineKeyboardMarkup()

    for acc in accounts:
        markup.add(InlineKeyboardButton(acc, callback_data=f"qiwi_{acc}"))

    markup.add(add_qiwi_btn)

    return markup


cancel_keyboard = InlineKeyboardMarkup()
cancel_btn = InlineKeyboardButton("Отмена нахуй", callback_data="cancel")
cancel_keyboard.add(cancel_btn)

backqiwi_keyboard = InlineKeyboardMarkup()
back_btn = InlineKeyboardButton("Назад", callback_data="backqiwi")
backqiwi_keyboard.add(back_btn)
escort_keyboard = InlineKeyboardMarkup()
create_form = InlineKeyboardButton(
    emojize(":envelope: Создать анкету :envelope:"), callback_data="none")

escort_keyboard.add(my_mamoths_btn)
escort_keyboard.add(create_form)
escort_keyboard.add(msgspam_btn)
escort_keyboard.add(deleteall_btn)

trading_keyboard = InlineKeyboardMarkup()
my_phrases = InlineKeyboardButton(
    emojize(":open_book: Свои фразы при выводе :open_book:"), callback_data="none")

trading_keyboard.add(my_mamoths_btn)
trading_keyboard.add(my_phrases)
trading_keyboard.add(msgspam_btn)
trading_keyboard.add(deleteall_btn)


def cas_info_update_keyboard(uid):
    markup = InlineKeyboardMarkup()
    cas_info_update_btn = InlineKeyboardButton(
        emojize(":arrows_counterclockwise:"), callback_data=f"updateinfo_{uid}")
    markup.add(cas_info_update_btn)

    return markup


alert_keyboard = InlineKeyboardMarkup()
bot_btn = InlineKeyboardButton(
    emojize("Основной бот :robot:"),
    callback_data="alert_bot"
)
casino_bots_btn = InlineKeyboardButton(
    emojize("Казино :slot_machine:"),
    callback_data="alert_casino"
)
escort_bots_btn = InlineKeyboardButton(
    emojize("Эскорт :strawberry:"),
    callback_data="alert_escort"
)
trading_bot_btn = InlineKeyboardButton(
    emojize("Трейдинг :chart_with_upwards_trend:"),
    callback_data="alert_trading"
)
alert_keyboard.add(bot_btn)
alert_keyboard.add(casino_bots_btn)
alert_keyboard.add(escort_bots_btn, trading_bot_btn)

alert_accept_keyboard = InlineKeyboardMarkup()
alert_accept_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Подтвердить"), callback_data="alert_accept")
alert_edit_btn = InlineKeyboardButton(
    emojize(":pencil2: Изменить"), callback_data="alert_edit")
alert_reject_btn = InlineKeyboardButton(
    emojize(":x: Отменить"), callback_data="alert_reject")
alert_accept_keyboard.add(alert_accept_btn)
alert_accept_keyboard.add(alert_edit_btn, alert_reject_btn)
