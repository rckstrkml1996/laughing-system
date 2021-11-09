from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from loader import dp, config
from data.texts import profile_text, already_in_text
from data.keyboards import welcome_keyboard


@dp.callback_query_handler(text="profile")
async def profile(query: CallbackQuery):
    try:
        await query.message.edit_text(
            profile_text.format(
                chat_id=query.from_user.id, username=query.from_user.username
            ),
            reply_markup=welcome_keyboard(
                config.escort_sup_username, config.escotz_link
            ),
        )
    except MessageNotModified:
        await query.answer(already_in_text)
