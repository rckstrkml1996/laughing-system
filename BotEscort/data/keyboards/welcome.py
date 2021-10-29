from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from config import config

welcome_keyboard = InlineKeyboardMarkup()

profile_btn = InlineKeyboardButton(emojize("Профиль :wrench:"), callback_data="profile")
girls_btn = InlineKeyboardButton(emojize("Анкеты :green_heart:"), callback_data="girls")
about_btn = InlineKeyboardButton(
    emojize("О нас :grey_question:"), callback_data="about"
)

support_username = config("escort_sup_username")
support_btn = InlineKeyboardButton(
    emojize("Тех. Поддержка :sos:"), url=f"t.me/{support_username}"
)

otz_chat = config("esc_otz_chat")
resume_btn = InlineKeyboardButton(emojize("Отзывы :receipt:"), url=f"t.me/{otz_chat}")

welcome_keyboard.add(profile_btn, girls_btn, about_btn)
welcome_keyboard.add(support_btn, resume_btn)


pay_done_keyboard = InlineKeyboardMarkup()
pay_done_keyboard.add(support_btn)
