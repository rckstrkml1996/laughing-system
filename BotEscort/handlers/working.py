from aiogram import types

from loader import dp
from data.texts import dont_working_text


@dp.message_handler(is_working=False)
async def dont_working(message: types.Message):
    await message.reply(dont_working_text)
