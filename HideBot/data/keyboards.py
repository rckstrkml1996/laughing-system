from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from data.config import outs_link, workers_link, reviews_link, Rates
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
    emojize(":pencil2: Подать заявку"), callback_data="summary"
)
summary_start_keyboard.add(new_summary_btn)

summary_rules_keyboard = InlineKeyboardMarkup()
agree_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Принимаю"), callback_data="agreesummary"
)
summary_rules_keyboard.add(agree_btn)

summary_send_keyboard = InlineKeyboardMarkup()
send_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Отправить заявку"), callback_data="sendsummary"
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
    resize_keyboard=True, one_time_keyboard=True)
panel_btn = KeyboardButton(emojize(":snake: Hide Panel"))
menu_keyboard.add(panel_btn)

panel_keyboard = InlineKeyboardMarkup()
tools_btn = InlineKeyboardButton(
    emojize(":hammer_and_wrench: Инструменты"), callback_data="tools"
)
rate_btn = InlineKeyboardButton(
    emojize(":scales: Ставка"), callback_data="rate"
)
profits_btn = InlineKeyboardButton(
    emojize(":recycle: Профиты"), callback_data="profits"
)
panel_keyboard.add(tools_btn, rate_btn)
panel_keyboard.add(profits_btn)

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
