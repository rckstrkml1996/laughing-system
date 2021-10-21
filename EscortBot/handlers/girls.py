from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text="girls")
async def girls_main(query: CallbackQuery):
    await query.answer("dsadsadasd")