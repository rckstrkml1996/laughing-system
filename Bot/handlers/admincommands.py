from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from data.keyboards import *
from data import payload
from utils.executional import get_work_status
from config import config


@dp.message_handler(commands="work", admins_type=True)
async def work_command(message: types.Message):
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    antikino_work = config("antikino_work")

    all_work = casino_work and escort_work and antikino_work

    await message.answer(
        payload.adm_work_command.format(
            services_status=get_work_status(),
        ),
        reply_markup=admworkstatus_keyboard(all_work)
    )


@dp.callback_query_handler(text="toggleworkstatus", admins_type=True)
async def toggle_work_status(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        await query.answer("Ты не админ!")
        return

    casino_work = not config("casino_work")  # return bool values
    escort_work = not config("escort_work")
    antikino_work = not config("antikino_work")

    config.edit_config("casino_work", casino_work)
    config.edit_config("escort_work", escort_work)
    config.edit_config("antikino_work", antikino_work)

    all_work = casino_work and escort_work and antikino_work

    text = payload.adm_work_command.format(
        services_status=get_work_status()
    )

    try:
        await query.message.edit_text(
            text, reply_markup=admworkstatus_keyboard(all_work)
        )
    except MessageNotModified:
        pass
    await dp.bot.send_message(config("workers_chat"), payload.setwork_text if all_work else payload.setdontwork_text)


""" WORKING FILE IDS AND CHANGING PHOTOS """


@dp.message_handler(content_types=["photo"], admins_type=True)
async def photo_hash(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return

    if message.caption == "/get_id":
        await message.answer(message.photo[-1].file_id)


@dp.message_handler(commands=["new_design"], admins_type=True)
async def new_design_command(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return
