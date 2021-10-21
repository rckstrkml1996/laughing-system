from aiogram.types import CallbackQuery

from loader import dp
from data.payload import girls_choice_text
from data.keyboards import girls_choice_keyboard


@dp.callback_query_handler(text="girls")
async def girls_choice(query: CallbackQuery):
    await query.message.edit_text(
        girls_choice_text, reply_markup=girls_choice_keyboard()
    )
