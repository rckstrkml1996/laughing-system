from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from data.keyboards import *
from data import payload
from config import config, edit_config


@dp.message_handler(commands="work", admins_type=True)
async def work_command(message: types.Message):
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    antikino_work = config("antikino_work")

    casino_scam = "Казино СКАМ"
    escort_scam = "Эскорт СКАМ"
    antikino_scam = "Антикино СКАМ"

    all_work = casino_work and escort_work and antikino_work

    await message.answer(
        emojize(payload.adm_work_command.format(
            casino_status=f":full_moon: {casino_scam}" if casino_work else f":new_moon: <del>{casino_scam}</del>",
            escort_status=f":full_moon: {escort_scam}" if escort_work else f":new_moon: <del>{escort_scam}</del>",
            antikino_status=f":full_moon: {antikino_scam}" if antikino_work else f":new_moon: <del>{antikino_scam}</del>",
            team_status=":full_moon: Общий статус: Ворк" if all_work else ":new_moon: Общий статус: Не ворк",
        )), reply_markup=admworkstatus_keyboard(all_work)
    )


@dp.callback_query_handler(text="toggleworkstatus", admins_type=True)
async def toggle_work_status(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        await query.answer("Ты не админ!")
        return

    casino_work = not config("casino_work")  # return bool values
    escort_work = not config("escort_work")
    antikino_work = not config("antikino_work")

    edit_config("casino_work", casino_work)
    edit_config("escort_work", escort_work)
    edit_config("antikino_work", antikino_work)

    casino_scam = "Казино СКАМ"
    escort_scam = "Эскорт СКАМ"
    antikino_scam = "Антикино СКАМ"

    all_work = casino_work and escort_work and antikino_work

    text = emojize(
        payload.adm_work_command.format(
            casino_status=f":full_moon: {casino_scam}" if casino_work else f":new_moon: <del>{casino_scam}</del>",
            escort_status=f":full_moon: {escort_scam}" if escort_work else f":new_moon: <del>{escort_scam}</del>",
            antikino_status=f":full_moon: {antikino_scam}" if antikino_work else f":new_moon: <del>{antikino_scam}</del>",
            team_status=":full_moon: Общий статус: Ворк" if all_work else ":new_moon: Общий статус: Не ворк",
        )
    )

    try:
        await query.message.edit_text(
            text, reply_markup=admworkstatus_keyboard(all_work)
        )
    except MessageNotModified:
        await query.message.edit_text(
            text + " ", reply_markup=admworkstatus_keyboard(all_work)
        )
    if all_work:
        await dp.bot.send_message(config("workers_chat"), payload.setwork_text)


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
