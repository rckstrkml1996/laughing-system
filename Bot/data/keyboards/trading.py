from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


tdng_mamoths_btn = InlineKeyboardButton(
    emojize("Мои мамонтята :elephant:"), callback_data="mamonths_tdng"
)
tdng_fraze_btn = InlineKeyboardButton(
    emojize("Свои фразы при выводе :book:"), callback_data="frazes_tdng"
)
tdng_msg_spam_btn = InlineKeyboardButton(
    emojize("Массовая рассылка :diamond_shape_with_a_dot_inside:"),
    callback_data="all_alerts_tdng",
)
tdng_delete_all_btn = InlineKeyboardButton(
    emojize("Удалить всех :warning:"), callback_data="delete_all_tdng"
)
trading_keyboard = InlineKeyboardMarkup()
trading_keyboard.add(tdng_mamoths_btn)
trading_keyboard.add(tdng_fraze_btn)
trading_keyboard.add(tdng_msg_spam_btn)
trading_keyboard.add(tdng_delete_all_btn)
