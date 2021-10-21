from aiogram import types
from aiogram.utils.markdown import quote_html

from loader import dp

from config import config
from data.payload import welcome_text
from data.keyboards import welcome_keyboard


@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    fullname = quote_html(message.chat.full_name)  # it may contain < and > and ..

    await message.answer(
        welcome_text.format(name=fullname, bot_name=config("escort_username")),
        reply_markup=welcome_keyboard,
    )
