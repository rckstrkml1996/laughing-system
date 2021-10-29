# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

# 


render_main_keyboard = InlineKeyboardMarkup()

qiwi_balance_btn = InlineKeyboardButton(
    emojize("Киви баланс :kiwi_fruit:"), callback_data="render_qiwibalance"
)
qiwi_transfer_btn = InlineKeyboardButton(
    emojize("Киви перевод :kiwi_fruit:"), callback_data="render_qiwitrans"
)
sber_transfer_btn = InlineKeyboardButton(
    emojize("Сбер перевод :green_apple:"), callback_data="render_sbertrans"
)
back_menu_btn = InlineKeyboardButton(
    emojize("Назад :arrow_double_up:"), callback_data="menu"
)

render_main_keyboard.add(qiwi_balance_btn, qiwi_transfer_btn)
render_main_keyboard.add(sber_transfer_btn)
render_main_keyboard.add(back_menu_btn)

to_menu_keyboard = InlineKeyboardMarkup()
to_menu_btn = InlineKeyboardButton(
    emojize("Вернуться :leftwards_arrow_with_hook:"), callback_data="menu"
)
to_menu_keyboard.add(to_menu_btn)
