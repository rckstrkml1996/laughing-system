from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize
from config import currencies


rules_keyboard = InlineKeyboardMarkup()
agree_btn = InlineKeyboardButton(emojize(":white_check_mark: Я принимаю правила"),
                                 callback_data="rules_agreed")
rules_keyboard.add(agree_btn)

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
up_btn = InlineKeyboardButton(emojize(":chart_with_upwards_trend: Повышение (X2)"),
                              callback_data="count")
down_btn = InlineKeyboardButton(emojize(":chart_with_downwards_trend: Понижение (X2)"),
                                callback_data="count")
back_btn = InlineKeyboardButton(emojize(":heavy_multiplication_x: Назад"), 
                                    callback_data="back")
investing_keyboard.add(up_btn)
investing_keyboard.add(down_btn)

payment_keyboard = InlineKeyboardMarkup()
start_payment_btn = InlineKeyboardButton(emojize(":money_with_wings: Перейти к оплате :money_with_wings:"),
                                         url="https://google.com")  # QIWI PAYMENT LINK
check_payment_btn = InlineKeyboardButton(emojize(":ballot_box_with_check: Проверить оплату  :ballot_box_with_check:"),
                                         callback_data="check_payment")

payment_keyboard.add(start_payment_btn)
payment_keyboard.add(check_payment_btn)
