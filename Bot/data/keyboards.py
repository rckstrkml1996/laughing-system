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


backpanel_keyboard = InlineKeyboardMarkup()
backpanel_btn = InlineKeyboardButton(
    emojize(":back: Назад"), callback_data="menu"
)
backpanel_keyboard.add(backpanel_btn)

profits_keyboard = InlineKeyboardMarkup()
week_btn = InlineKeyboardButton(
    emojize(":chart: За неделю"), callback_data="weekprofits"
)
profits_keyboard.add(week_btn)
profits_keyboard.add(backpanel_btn)

rate_keyboard = InlineKeyboardMarkup()
changerate_btn = InlineKeyboardButton(
    emojize(":sa: Сменить ставку"), callback_data="changerate")
rate_keyboard.add(changerate_btn)
rate_keyboard.add(backpanel_btn)

changerate_keyboard = InlineKeyboardMarkup()
for i in range(len(Rates)):
    changerate_keyboard.add(
        InlineKeyboardButton(
            emojize(
                f"{num2emoji(i + 1)} Ставка"
            ),
            callback_data=f"cr_{i}"
        )
    )
changerate_keyboard.add(backpanel_btn)


def tools_keyboard(hide):
    status = ":white_check_mark: Открыть ник" if hide else ":negative_squared_cross_mark: Скрыть ник"

    markup = InlineKeyboardMarkup()
    render_btn = InlineKeyboardButton(
        emojize(":newspaper: Отрисовка"), callback_data="render"
    )
    secretid_btn = InlineKeyboardButton(
        emojize(":keycap_number_sign: Secret-ID"), callback_data="secretid"
    )
    username_btn = InlineKeyboardButton(
        emojize(status), callback_data="toggleusername"
    )
    markup.add(render_btn)
    markup.add(secretid_btn)
    markup.add(username_btn)
    markup.add(backpanel_btn)

    return markup


render_keyboard = InlineKeyboardMarkup()
qiwibalance_btn = InlineKeyboardButton(
    emojize(":kiwi_fruit: Qiwi Баланс"), callback_data="qiwibalance")
qiwitransfer_btn = InlineKeyboardButton(
    emojize(":kiwi_fruit: Qiwi Перевод"),  callback_data="qiwitransfer")
sbertransfer_btn = InlineKeyboardButton(
    emojize(":sparkle: Сбер Перевод"),  callback_data="sbertransfer")
render_keyboard.add(qiwibalance_btn)
render_keyboard.add(qiwitransfer_btn)
render_keyboard.add(sbertransfer_btn)
render_keyboard.add(backpanel_btn)


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
    emojize("Мои мамонтята :elephant:"), callback_data="none")
promos_btn = InlineKeyboardButton(
    emojize("Мои промокоды :receipt:"), callback_data="none")
msgspam_btn = InlineKeyboardButton(
    emojize("Массовая рассылка :envelope:"), callback_data="none")
deleteall_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="none")

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
