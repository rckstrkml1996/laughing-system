from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import emoji
from aiogram.utils.emoji import emojize
from data.config import currencies


rules_keyboard = InlineKeyboardMarkup()
agree_btn = InlineKeyboardButton(emojize(":white_check_mark: Я принимаю правила"),
                                 callback_data="rules_agreed")
rules_keyboard.add(agree_btn)
main_keyboard = ReplyKeyboardMarkup()
my_ecn_btn = KeyboardButton(emojize(":chart_with_upwards_trend: Мой ECN счёт"))
profile_btn = KeyboardButton(emojize(":briefcase: Профиль"))
deposit_btn = KeyboardButton(emojize(":credit_card: Пополнить"))
withdraw_btn = KeyboardButton(emojize(":bank: Вывести"))
settings_btn = KeyboardButton(emojize(":hammer_and_wrench: Настройки"))
main_keyboard.add(my_ecn_btn, profile_btn)
main_keyboard.add(deposit_btn, withdraw_btn)
main_keyboard.add(settings_btn)

actives_keyboard = InlineKeyboardMarkup(row_width=2)
for name, code in currencies.items():
    actives_keyboard.add(InlineKeyboardButton(name, callback_data=code))

settings_keyboard = InlineKeyboardMarkup(row_width=2)
currency_btn = InlineKeyboardButton(emojize(":moneybag: Валюта"),
                                    callback_data="currency")
language_btn = InlineKeyboardButton(emojize("🇷🇺 Язык 🇺🇸"),
                                    callback_data="language")
support_btn = InlineKeyboardButton(emojize(":hammer_and_wrench: Тех. поддержка :hammer_and_wrench:"),
                                   callback_data="support")
settings_keyboard.add(currency_btn, language_btn)
settings_keyboard.add(support_btn)

investing_keyboard = InlineKeyboardMarkup()
up_btn = InlineKeyboardButton(emojize(":chart_with_upwards_trend: Повышение (X2)"),
                            callback_data="count")
down_btn = InlineKeyboardButton(emojize(":chart_with_downwards_trend: Понижение (X2)"),
                                callback_data="count")
investing_keyboard.add(up_btn)
investing_keyboard.add(down_btn)
