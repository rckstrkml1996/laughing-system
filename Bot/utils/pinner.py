import asyncio
from configparser import NoOptionError

from aiogram import Bot
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import (
    MessageNotModified,
    MessageToEditNotFound,
    MessageTextIsEmpty,
    MessageToPinNotFound,
    ChatNotFound,
    MessageCantBeEdited,
)
from customutils.datefunc import datetime_local_now
from customutils.models import CasinoUser, TradingUser, EscortUser

from loader import db_commands
from config import config
from data.payload import pin_text
from utils.executional import get_work_status, get_work_moon, rub_usd_btcticker


async def format_pin_text(text):
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")

    try:
        rub, usd = await rub_usd_btcticker()
    except AssertionError:
        rub, usd = "Неизвестно", "Неизвестно"  # if btc api dont work

    query = db_commands.get_topworkers_day(limit=1)
    try:
        worker = query.execute()[0]
        topd_worker = f"<a href='tg://user?id={worker.cid}'>{worker.name}</a>"
    except IndexError:
        topd_worker = "Отсутсвует"

    in_casino = CasinoUser.select().count()
    in_trading = TradingUser.select().count()
    in_escort = EscortUser.select().count()

    return emojize(
        text.format(
            dyna_moon=get_work_moon(),
            services_status=get_work_status(),
            btc_usd_price=usd,
            btc_rub_price=rub,
            topd_worker=topd_worker,
            time=timenow,
            in_casino=in_casino,
            in_trading=in_trading,
            in_escort=in_escort,
        )
    )


async def dynapins(bot: Bot):
    if not isinstance(bot, Bot):
        raise TypeError(
            f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'"
        )

    workers_chat = config("workers_chat")
    update_time = config("pin_update_time")
    text = await format_pin_text(pin_text())
    if text:
        try:
            message_id = config("pinned_msg_id")
        except NoOptionError:
            message = await bot.send_message(workers_chat, text)
            message_id = message.message_id
            config.edit_config("pinned_msg_id", message_id)

        try:
            await bot.pin_chat_message(
                workers_chat, message_id, disable_notification=True
            )
        except MessageToPinNotFound:
            message = await bot.send_message(workers_chat, text)
            message_id = message.message_id
            config.edit_config("pinned_msg_id", message_id)
            await bot.pin_chat_message(
                workers_chat, message_id, disable_notification=True
            )
        except ChatNotFound:
            pass

    while True:
        await asyncio.sleep(update_time)
        text = await format_pin_text(pin_text())
        try:
            await bot.edit_message_text(
                chat_id=workers_chat, message_id=message_id, text=text
            )
        except MessageCantBeEdited:
            message = await bot.send_message(workers_chat, text)
            message_id = message.message_id
            config.edit_config("pinned_msg_id", message_id)
        except MessageNotModified:
            pass
        except MessageTextIsEmpty:
            pass
        except MessageToEditNotFound:
            message = await bot.send_message(workers_chat, text)
            await bot.pin_chat_message(
                workers_chat, message_id, disable_notification=True
            )
        except ChatNotFound:
            pass
