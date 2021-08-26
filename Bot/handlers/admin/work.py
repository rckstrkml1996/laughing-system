from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from config import config
from data import payload
from data.keyboards import *


@dp.message_handler(commands="work", admins_chat=True)
async def work_command(message: types.Message):
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    trading_work = config("trading_work")

    all_work = casino_work and escort_work and trading_work

    await message.answer(
        payload.adm_work_command.format(
            services_status=emojize(
                payload.services_status.format(
                    casino_status=f":full_moon: Казино СКАМ"
                    if casino_work
                    else f":new_moon: <del>Казино СКАМ</del>",
                    escort_status=f":full_moon: Эскорт СКАМ"
                    if escort_work
                    else f":new_moon: <del>Эскорт СКАМ</del>",
                    trading_status=f":full_moon: Трейдинг СКАМ"
                    if trading_work
                    else f":new_moon: <del>Трейдинг СКАМ</del>",
                    team_status=":full_moon: Общий статус: Ворк"
                    if all_work
                    else ":new_moon: Общий статус: Не ворк",
                )
            )
        ),
        reply_markup=admworkstatus_keyboard(all_work),
    )


@dp.callback_query_handler(text="toggleworkstatus", admins_chat=True, is_admin=True)
async def toggle_work_status(query: types.CallbackQuery):
    casino_work = config("casino_work")  # return bool values
    escort_work = config("escort_work")
    trading_work = config("trading_work")

    all_work = casino_work and escort_work and trading_work

    if all_work:
        casino_work = False
        escort_work = False
        trading_work = False
        all_work = False
    else:
        casino_work = True
        escort_work = True
        trading_work = True
        all_work = True

    config.edit_config("casino_work", casino_work)
    config.edit_config("escort_work", escort_work)
    config.edit_config("trading_work", trading_work)

    text = payload.adm_work_command.format(
        services_status=emojize(
            payload.services_status.format(
                casino_status=f":full_moon: Казино СКАМ"
                if casino_work
                else f":new_moon: <del>Казино СКАМ</del>",
                escort_status=f":full_moon: Эскорт СКАМ"
                if escort_work
                else f":new_moon: <del>Эскорт СКАМ</del>",
                trading_status=f":full_moon: Трейдинг СКАМ"
                if trading_work
                else f":new_moon: <del>Трейдинг СКАМ</del>",
                team_status=":full_moon: Общий статус: Ворк"
                if all_work
                else ":new_moon: Общий статус: Не ворк",
            )
        )
    )

    try:
        await query.message.edit_text(
            text, reply_markup=admworkstatus_keyboard(all_work)
        )
    except MessageNotModified:
        pass
    await dp.bot.send_message(
        config("workers_chat"),
        payload.setwork_text if all_work else payload.setdontwork_text,
    )
