from aiogram import types
from aiogram.utils.markdown import quote_html

from loader import dp

from config import config
from data.states import Login
from data.payload import new_user_text, new_user_wrong_code_text, welcome_text
from data.keyboards import welcome_keyboard
from utils.executional import get_worker_by_code, create_user


@dp.message_handler(commands=["start", "help"], is_user=False)
async def welcome_new_user(message: types.Message):
    await message.answer(new_user_text.format(name=message.chat.full_name))
    await Login.code.set()


@dp.message_handler(state=Login.code, is_user=False)
async def welcome_code(message: types.Message):
    worker = get_worker_by_code(message.text)

    if worker:
        created = create_user(
            worker,
            message.chat.id,
            message.chat.username,
            quote_html(message.chat.full_name),
        )
        if created:
            await welcome_msg(message)
    else:
        await message.answer(new_user_wrong_code_text)


@dp.message_handler(commands=["start", "help"])  # its - is_user=True
async def welcome_msg(message: types.Message):
    fullname = quote_html(message.chat.full_name)  # it may contain < and > and ..

    await message.answer(
        welcome_text.format(name=fullname, bot_name=config("escort_username")),
        reply_markup=welcome_keyboard,
    )


@dp.callback_query_handler(text="welcome")
async def welcome_cb(query: types.CallbackQuery):
    fullname = quote_html(query.from_user.full_name)  # it may contain < and > and ..

    await query.message.edit_text(
        welcome_text.format(name=fullname, bot_name=config("escort_username")),
        reply_markup=welcome_keyboard,
    )
