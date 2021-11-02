from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


# on new summary
summary_start_keyboard = InlineKeyboardMarkup()
new_summary_btn = InlineKeyboardButton(
    emojize(":rocket: Подать заявку"), callback_data="summary"
)
summary_start_keyboard.add(new_summary_btn)

# accept rules
summary_rules_keyboard = InlineKeyboardMarkup()
agree_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Принимаю"), callback_data="agreesummary"
)
summary_rules_keyboard.add(agree_btn)

# send summary to admins
summary_send_keyboard = InlineKeyboardMarkup()
send_btn = InlineKeyboardButton(
    emojize(":rocket: Отправить"), callback_data="sendsummary"
)
summary_send_keyboard.add(send_btn)

# worker blocked in bot
summary_blocked_keyboard = InlineKeyboardMarkup()
fuckurself_btn = InlineKeyboardButton(
    emojize(":speak_no_evil: Пойти нахуй!"), callback_data="fuckurself"
)
summary_blocked_keyboard.add(fuckurself_btn)

# worker accepted in bot
def summary_accepted_keyboard(
    outs_link: str,
    workers_link: str,
    reviews_link: str,
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    outs_btn = InlineKeyboardButton(
        emojize("Канал выплат :money_with_wings:"), url=f't.me/{outs_link}'
    )
    workers_btn = InlineKeyboardButton(
        emojize("Чат воркеров :man_technologist:"),
        url=f'https://t.me/joinchat/{workers_link}',
    )
    reviews_btn = InlineKeyboardButton(
        emojize("Мануалы :page_with_curl:"), url=f't.me/{reviews_link}'
    )
    markup.add(outs_btn)
    markup.add(workers_btn)
    markup.add(reviews_btn)
