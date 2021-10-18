from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


# from config import QIWI_ACCOUNTS

# cancel button
cancel_button = KeyboardButton(emojize("Назад"))

# bot main keyboard


def main_keyboard():
    main_keyboard = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    play_button = KeyboardButton(emojize("Играть :four_leaf_clover:"))
    in_button = KeyboardButton(emojize("Пополнить :arrow_down:"))
    # promo_button = KeyboardButton(emojize("Ввести промокод"))
    out_button = KeyboardButton(emojize("Вывести :arrow_up:"))
    sup_button = KeyboardButton(emojize("Информация :information_source:"))
    selfcab_button = KeyboardButton(emojize("Личный кабинет :selfie:"))
    main_keyboard.row(play_button)
    main_keyboard.row(in_button, out_button)  # promo_button
    main_keyboard.row(sup_button, selfcab_button)

    return main_keyboard


def welcome_keyboard(ref_id: int):
    welcome_keyboard = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton(
        emojize(":white_check_mark: Принять правила"), callback_data=f"accept_{ref_id}"
    )
    welcome_keyboard.add(accept_button)
    return welcome_keyboard


def add_req_keyboard(amount: int, comment: int, number):
    url = f"https://qiwi.com/payment/form/99?currency=RUB&amountInteger={amount}\
	&amountFraction=0&extra['account']={number}&extra['comment']={comment}"

    markup = InlineKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True, row_width=1
    )
    goto_button = InlineKeyboardButton(emojize("Перейти к оплате"), url=url)
    card_button = InlineKeyboardButton(
        emojize("Оплатить картой :credit_card:"), callback_data="paycard"
    )
    check_button = InlineKeyboardButton(
        emojize("Проверить оплату"), callback_data=f"check_{comment}"
    )
    markup.add(goto_button, card_button, check_button)

    return markup


qiwi_keyboard = InlineKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=1
)
# for acc in QIWI_ACCOUNTS:
qiwi_keyboard.add(InlineKeyboardButton("acc", callback_data=f"qiwi_acc"))


def payment_done_keyboard(cid, comment):
    markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    accept_button = InlineKeyboardButton(
        emojize("Пополнить"), callback_data=f"done_{cid}_{comment}"
    )
    markup.add(accept_button)
    return markup


add_type_keyboard = InlineKeyboardMarkup()
add_qiwi_btn = InlineKeyboardButton(
    emojize("Qiwi :kiwi_fruit:"),
    callback_data="qiwi_add_type",
)
add_banker_btn = InlineKeyboardButton(
    emojize("BTC Banker :briefcase:"),
    callback_data="banker_add_type",
)
add_type_keyboard.add(add_qiwi_btn)
add_type_keyboard.add(add_banker_btn)


add_banker_manual_keyboard = InlineKeyboardMarkup()
add_banker_manual_keyboard2 = InlineKeyboardMarkup()
btc_manual_btn = InlineKeyboardButton(
    emojize("Инструкция :receipt:"),
    url="https://telegra.ph/Kak-popolnit-schet-i-vypisat-chek-v-BTC-banker-10-08",
)
back_add_btn = InlineKeyboardButton(
    emojize("Назад :leftwards_arrow_with_hook:"), callback_data="back_add"
)
add_banker_manual_keyboard.add(btc_manual_btn)
add_banker_manual_keyboard.add(back_add_btn)
add_banker_manual_keyboard2.add(btc_manual_btn)
