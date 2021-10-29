from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize
from config import currencies


def rules_keyboard(key):
    markup = InlineKeyboardMarkup()
    agree_btn = InlineKeyboardButton(
        emojize(":white_check_mark: Я принимаю правила"),
        callback_data=f"rulesagreed_{key}",
    )
    markup.add(agree_btn)

    return markup


main_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
my_ecn_btn = KeyboardButton(emojize(":chart_with_upwards_trend: Мой ECN счёт"))
profile_btn = KeyboardButton(emojize(":briefcase: Профиль"))
deposit_btn = KeyboardButton(emojize(":credit_card: Пополнить"))
withdraw_btn = KeyboardButton(emojize(":bank: Вывести"))
support_btn = KeyboardButton(emojize(":technologist: Тех. поддержка"))
main_keyboard.add(my_ecn_btn, profile_btn)
main_keyboard.add(deposit_btn, withdraw_btn)
main_keyboard.add(support_btn)

actives_keyboard = InlineKeyboardMarkup(row_width=2)
for name, code in currencies.items():
    actives_keyboard.add(InlineKeyboardButton(name, callback_data=code))

investing_keyboard = InlineKeyboardMarkup()
up_btn = InlineKeyboardButton(
    emojize(":chart_with_upwards_trend: Повышение (X2)"), callback_data="count"
)
down_btn = InlineKeyboardButton(
    emojize(":chart_with_downwards_trend: Понижение (X2)"), callback_data="count"
)
back_btn = InlineKeyboardButton(
    emojize(":heavy_multiplication_x: Назад"), callback_data="back"
)
investing_keyboard.add(up_btn)
investing_keyboard.add(down_btn)


def payment_keyboard(amount, number, comment):
    markup = InlineKeyboardMarkup()

    url = f"https://qiwi.com/payment/form/99?currency=RUB&amountInteger={amount}\
	&amountFraction=0&extra['account']={number}&extra['comment']={comment}"

    start_payment_btn = InlineKeyboardButton(
        emojize(":money_with_wings: Перейти к оплате :money_with_wings:"),
        url=url,
    )  # QIWI PAYMENT LINK
    check_payment_btn = InlineKeyboardButton(
        emojize(":ballot_box_with_check: Проверить оплату  :ballot_box_with_check:"),
        callback_data=f"check_{comment}",
    )

    markup.add(start_payment_btn)
    markup.add(check_payment_btn)

    return markup
