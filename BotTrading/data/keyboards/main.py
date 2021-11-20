from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.emoji import emojize

main_keyboard = ReplyKeyboardMarkup()

"""
портфель
поддержка

инвестировать

пополнить
вывести

# отзывы (потом 'live выплаты')
"""


def agree_rules_keyboard(worker_id):
    markup = InlineKeyboardMarkup()
    agree_rules_btn = InlineKeyboardButton(
        emojize(":white_check_mark: Принять правила"),
        callback_data=f"agreerules_{worker_id}",
    )
    markup.add(agree_rules_btn)

    return markup


def portfile_keyboard(trading_channel_link, support_username):
    markup = InlineKeyboardMarkup(row_width=1)
    about_btn = InlineKeyboardButton(
        emojize("Мы в телеграм :sunglasses:"), url=f"t.me/{trading_channel_link}"
    )
    support_btn = InlineKeyboardButton(
        emojize("Поддержка :man_technologist:"), url=f"t.me/{support_username}"
    )
    markup.add(about_btn, support_btn)

    return markup


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

portfile_btn = KeyboardButton(emojize("Портфель :briefcase:"))
invest = KeyboardButton(emojize("Открыть ECN :chart:"))
in_btn = KeyboardButton(emojize("Пополнить :arrow_heading_down:"))
out_btn = KeyboardButton(emojize("Вывести :arrow_heading_up:"))

main_keyboard.add(portfile_btn)
main_keyboard.add(invest)
main_keyboard.add(in_btn, out_btn)


def add_keyboard(
    amount: int, public_key: str, comment: str, pay_id: int
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    payurl = f"https://oplata.qiwi.com/create?publicKey={public_key}&amount={amount}&comment={comment}"

    go_to_pay_btn = InlineKeyboardButton(
        emojize("Перейти к оплате :arrow_heading_up:"), url=payurl
    )
    pay_card_btn = InlineKeyboardButton(
        emojize("Оплатить картой :credit_card:"), callback_data="paycard"
    )
    check_btn = InlineKeyboardButton(
        emojize("Проверить оплату :white_check_mark:"), callback_data=f"check_{pay_id}"
    )

    markup.add(go_to_pay_btn, pay_card_btn, check_btn)

    return markup


def invest_keyboard(currency_names: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    for c_id, name in enumerate(currency_names):
        markup.add(InlineKeyboardButton(name, callback_data=f"curr_{c_id}"))

    return markup


def agree_ecn_keyboard(ecn_url: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("Соглашение", url=ecn_url))
    markup.add(InlineKeyboardButton("Прочитал!", callback_data="agreeecn"))

    return markup


def bet_keyboard(currency_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    bet_up_btn = InlineKeyboardButton(
        emojize("Повышение :arrow_up_small:"), callback_data=f"bet_{currency_id}_1"
    )
    bet_down_btn = InlineKeyboardButton(
        emojize("Понижение :arrow_down_small:"), callback_data=f"bet_{currency_id}_0"
    )

    markup.add(bet_up_btn, bet_down_btn)

    return markup


choice_fix_keyboard = InlineKeyboardMarkup(row_width=1)
half_min_btn = InlineKeyboardButton("30 Секунд", callback_data="tchoice_30")
min_btn = InlineKeyboardButton("1 Минута", callback_data="tchoice_60")
two_min_btn = InlineKeyboardButton("2 Минуты", callback_data="tchoice_120")
three_min_btn = InlineKeyboardButton("3 Минуты", callback_data="tchoice_180")
choice_fix_keyboard.add(half_min_btn, min_btn, two_min_btn, three_min_btn)
