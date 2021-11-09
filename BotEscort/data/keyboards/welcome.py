from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

profile_btn = InlineKeyboardButton(emojize("Профиль :wrench:"), callback_data="profile")
girls_btn = InlineKeyboardButton(emojize("Анкеты :green_heart:"), callback_data="girls")
about_btn = InlineKeyboardButton(
    emojize("О нас :grey_question:"), callback_data="about"
)


def welcome_keyboard(support_username: str, otz_chat: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    support_btn = InlineKeyboardButton(
        emojize("Тех. Поддержка :sos:"), url=f"t.me/{support_username}"
    )
    resume_btn = InlineKeyboardButton(
        emojize("Отзывы :receipt:"), url=f"t.me/{otz_chat}"
    )
    markup.add(profile_btn, girls_btn, about_btn)
    markup.add(support_btn, resume_btn)

    return markup

def pay_done_keyboard(support_username: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    support_btn = InlineKeyboardButton(
        emojize("Тех. Поддержка :man-technologist:"), url=f"t.me/{support_username}"
    )
    markup.add(support_btn)

    return markup
