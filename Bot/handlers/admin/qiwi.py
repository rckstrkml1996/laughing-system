from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from qiwiapi import Qiwi
from loader import dp, config
from data.texts import (
    no_qiwis_text,
    qiwi_to_bot_text,
    wanna_add_qiwi_text,
    add_qiwi_text,
    invalid_newqiwi_text,
    valid_newqiwi_text,
)
from data.keyboards import add_qiwi_keyboard, add_qiwi_sure_keyboard
from data.states import NewQiwi


async def qiwi_info(chat_id: int):
    """without message to call it in another handler"""
    if not config.qiwi_tokens:
        await dp.bot.send_message(
            chat_id, no_qiwis_text, reply_markup=add_qiwi_keyboard
        )
    else:
        await dp.bot.send_message(
            chat_id, config.qiwi_tokens, reply_markup=add_qiwi_keyboard
        )  # some logic


@dp.message_handler(commands=["qiwi", "qiwis"], admins_chat=True, is_admin=True)
async def qiwi_command(message: Message):
    await qiwi_info(message.chat.id)


@dp.callback_query_handler(text="qiwiadd", admins_chat=True, is_admin=True)
async def qiwi_add_admins(query: CallbackQuery):
    await query.message.edit_text(qiwi_to_bot_text)
    await dp.bot.send_message(
        query.from_user.id, wanna_add_qiwi_text, reply_markup=add_qiwi_sure_keyboard
    )


@dp.callback_query_handler(text="qiwiadd", admins_chat=False, is_admin=True)
async def qiwi_add_bot(query: CallbackQuery):
    await query.message.edit_text(add_qiwi_text)
    await NewQiwi.main.set()


@dp.message_handler(state=NewQiwi.main, is_admin=True)
async def qiwi_new(message: Message, state: FSMContext):
    data = message.text.split("\n")
    try:
        if len(data) >= 2:  # token and proxy and can be ...
            payload = {"token": data[0], "proxy_url": data[1]}
        else:  # only token
            payload = {"token": data[0], "proxy_url": None}

        Qiwi.validate(**payload)

        if isinstance(config.qiwi_tokens, list):
            qiwi_tokens = [*config.qiwi_tokens, payload]
        else:
            qiwi_tokens = [payload]

        logger.info(f"Setting up {qiwi_tokens=} in BotConfig")
        config.qiwi_tokens = qiwi_tokens

        await message.answer(valid_newqiwi_text)
        await qiwi_info(config.admins_chat)

        await state.finish()
    except ValueError:
        await message.answer(invalid_newqiwi_text)
