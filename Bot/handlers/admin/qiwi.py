from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from qiwiapi import Qiwi
from loader import dp, config
from data.payload import (
    no_qiwis_text,
    qiwi_to_bot_text,
    wanna_add_qiwi_text,
    add_qiwi_text,
    invalid_newqiwi_text,
)
from data.keyboards import add_qiwi_keyboard, add_qiwi_sure_keyboard
from data.states import NewQiwi


@dp.message_handler(commands=["qiwi", "qiwis"], admins_chat=True, is_admin=True)
async def qiwi_command(message: Message):
    if config.qiwi_tokens is None:
        await message.reply(no_qiwis_text, reply_markup=add_qiwi_keyboard)
    else:
        await message.reply(config.qiwi_tokens)


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
        if len(data) >= 2:
            qiwi = Qiwi(data[0], data[1])  # token, proxy
        else:
            qiwi = Qiwi(data[0])  # only token

        await state.finish()
    except Exception as ex:
        print(ex)
        await message.reply(ex)

    # await message.answer(invalid_newqiwi_text)
