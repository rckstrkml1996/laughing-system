from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import MessageNotModified
from loguru import logger

from loader import dp

from data.payload import (
    adm_work_command,
    services_status,
    setwork_text,
    setdontwork_text,
    casino_setwork_text,
    casino_setdontwork_text,
    escort_setwork_text,
    escort_setdontwork_text,
    trading_setwork_text,
    trading_setdontwork_text,
)
from data.keyboards import *


@dp.message_handler(commands="work", admins_chat=True)
async def work_command(message: types.Message):
    casino_work = config.casino_work
    escort_work = config.escort_work
    trading_work = config.trading_work

    all_work = casino_work and escort_work and trading_work

    await message.answer(
        adm_work_command.format(
            services_status=emojize(
                services_status.format(
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
        reply_markup=admworkstatus_keyboard(
            all_work, casino_work, escort_work, trading_work
        ),
    )
    logger.debug(f"Admin [{message.from_user.id=}] check work status.")


@dp.callback_query_handler(text="toggle_status", admins_chat=True, is_admin=True)
async def toggle_work_status(query: types.CallbackQuery):
    casino_work = config("casino_work", bool)  # return bool values
    escort_work = config("escort_work", bool)
    trading_work = config("trading_work", bool)

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

    config.casino_work = casino_work
    config.escort_work = escort_work
    config.trading_work = trading_work

    text = adm_work_command.format(
        services_status=emojize(
            services_status.format(
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
            text,
            reply_markup=admworkstatus_keyboard(
                all_work,
                casino_work,
                escort_work,
                trading_work,
            ),
        )
        logger.debug(f"Admin [{query.message.from_user.id}] changed work status.")
    except MessageNotModified:
        pass
    await dp.bot.send_message(
        config.workers_chat,
        setwork_text if all_work else setdontwork_text,
    )


# toggle_casino_status
@dp.callback_query_handler(text="toggle_casino_status", admins_chat=True, is_admin=True)
async def toggle_work_status(query: types.CallbackQuery):
    casino_work = not config("casino_work", bool)  # return bool values
    escort_work = config("escort_work", bool)
    trading_work = config("trading_work", bool)

    config.casino_work = casino_work

    all_work = casino_work and escort_work and trading_work

    text = adm_work_command.format(
        services_status=emojize(
            services_status.format(
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
            text,
            reply_markup=admworkstatus_keyboard(
                all_work,
                casino_work,
                escort_work,
                trading_work,
            ),
        )
        logger.debug(f"Admin [{query.message.from_user.id=}] changed work status.")
    except MessageNotModified:
        logger.warning("Change work status, MessageNotModified")
    await dp.bot.send_message(
        config.workers_chat,
        casino_setwork_text if casino_work else casino_setdontwork_text,
    )


# toggle_escort_status
@dp.callback_query_handler(text="toggle_escort_status", admins_chat=True, is_admin=True)
async def toggle_work_status(query: types.CallbackQuery):
    casino_work = config("casino_work", bool)  # return bool values
    escort_work = not config("escort_work", bool)
    trading_work = config("trading_work", bool)

    config.escort_work = escort_work

    all_work = casino_work and escort_work and trading_work

    text = adm_work_command.format(
        services_status=emojize(
            services_status.format(
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
            text,
            reply_markup=admworkstatus_keyboard(
                all_work,
                casino_work,
                escort_work,
                trading_work,
            ),
        )
        logger.debug(f"Admin [{query.message.from_user.id=}] changed work status.")
    except MessageNotModified:
        logger.warning("Change work status, MessageNotModified")
    await dp.bot.send_message(
        config.workers_chat,
        escort_setwork_text if escort_work else escort_setdontwork_text,
    )


# toggle_trading_status
@dp.callback_query_handler(
    text="toggle_trading_status", admins_chat=True, is_admin=True
)
async def toggle_work_status(query: types.CallbackQuery):
    casino_work = config("casino_work", bool)  # return bool values
    escort_work = config("escort_work", bool)
    trading_work = not config("trading_work", bool)

    config.trading_work = trading_work

    all_work = casino_work and escort_work and trading_work

    text = adm_work_command.format(
        services_status=emojize(
            services_status.format(
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
            text,
            reply_markup=admworkstatus_keyboard(
                all_work,
                casino_work,
                escort_work,
                trading_work,
            ),
        )
        logger.debug(f"Admin [{query.message.from_user.id=}] changed work status.")
    except MessageNotModified:
        logger.warning("Change work status, MessageNotModified")
    await dp.bot.send_message(
        config.workers_chat,
        trading_setwork_text if trading_work else trading_setdontwork_text,
    )
