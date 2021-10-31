from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from data.texts import about_us_text, already_in_text
from data.keyboards import welcome_keyboard


@dp.callback_query_handler(text="about")
async def about(query: CallbackQuery):
    try:
        await query.message.edit_text(about_us_text, reply_markup=welcome_keyboard)
    except MessageNotModified:
        await query.answer(already_in_text)
