from aiogram import types
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher import FSMContext

from loader import dp, main_bot, config
from data.states import Login
from data.texts import (
    new_user_text,
    new_user_wrong_code_text,
    welcome_text,
    newref_ref_text,
    newref_code_text,
)
from data.keyboards import welcome_keyboard
from utils.executional import get_worker_by_code, create_user


def decode_link(text: str) -> str:
    payload = text.split(" ")
    return payload[1] if len(payload) >= 2 else None


@dp.message_handler(commands=["start", "help"], state="*", is_user=False)
async def welcome_new_user(message: types.Message, state: FSMContext):
    ref_id = decode_link(message.text)
    if ref_id is None:
        await message.answer(new_user_text.format(name=message.chat.full_name))
        await Login.code.set()
    else:
        worker = get_worker_by_code(ref_id)
        if worker:
            created = create_user(
                worker,
                message.chat.id,
                message.chat.username,
                quote_html(message.chat.full_name),
            )
            if created:
                await welcome_msg(message, state)
                await main_bot.send_message(
                    worker.cid,
                    newref_ref_text.format(
                        m_id=created.id,
                        chat_id=created.cid,
                        name=created.fullname,
                    ),
                )
            else:
                await message.answer(new_user_wrong_code_text)
        else:
            await message.answer(new_user_wrong_code_text)


@dp.message_handler(state=Login.code, is_user=False)
async def welcome_code(message: types.Message, state: FSMContext):
    worker = get_worker_by_code(message.text)

    if worker:
        created = create_user(
            worker,
            message.chat.id,
            message.chat.username,
            quote_html(message.chat.full_name),
        )
        if created:
            await welcome_msg(message, state)
            await main_bot.send_message(
                worker.cid,
                newref_code_text.format(
                    m_id=created.id,
                    chat_id=created.cid,
                    name=created.fullname,
                ),
            )
        else:
            await message.answer(new_user_wrong_code_text)
    else:
        await message.answer(new_user_wrong_code_text)


@dp.message_handler(commands=["start", "help"], state="*")  # its - is_user=True
async def welcome_msg(message: types.Message, state: FSMContext):
    await state.finish()

    fullname = quote_html(message.chat.full_name)  # it may contain < and > and ..

    await message.answer(
        welcome_text.format(name=fullname, bot_name=config.escort_username),
        reply_markup=welcome_keyboard,
    )


@dp.callback_query_handler(text="welcome")
async def welcome_cb(query: types.CallbackQuery):
    fullname = quote_html(query.from_user.full_name)  # it may contain < and > and ..

    await query.message.edit_text(
        welcome_text.format(name=fullname, bot_name=config.escort_username),
        reply_markup=welcome_keyboard,
    )
