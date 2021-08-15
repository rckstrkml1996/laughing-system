from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


def rules_keyboard():
    keyboard = InlineKeyboardMarkup()
    agree_btn = InlineKeyboardButton(emojize(":white_check_mark: Я принимаю правила"),
                                     callback_data="rules_agreed")
    keyboard.add(agree_btn)


    return keyboard

def main_keyboard():
    keyboard = ReplyKeyboardMarkup()
    my_ecn_btn = KeyboardButton(emojize(":chart_with_upwards_trend: Мой ECN счёт"))
    profile_btn = KeyboardButton(emojize(":briefcase: Профиль"))
    deposit_btn = KeyboardButton(emojize(":credit_card: Пополнить"))
    withdraw_btn = KeyboardButton(emojize(":bank: Вывести"))
    settings_btn = KeyboardButton(emojize(":hammer_and_wrench: Настройки"))
    keyboard.add(my_ecn_btn, profile_btn)
    keyboard.add(deposit_btn, withdraw_btn)
    keyboard.add(settings_btn)

    return keyboard