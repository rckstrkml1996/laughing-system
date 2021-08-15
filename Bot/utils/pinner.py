import asyncio

from peewee import fn, SQL, JOIN
from aiogram import Bot
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageTextIsEmpty

from config import config
from customutils.models import Worker, Profit
from data.payload import pin_text
from utils.executional import get_work_status, get_work_moon, rub_usd_btcticker
from utils.datefunc import datetime_local_now


async def format_pin_text(text):
    localnow = datetime_local_now().replace(tzinfo=None)
    timenow = localnow.strftime("%H:%M, %S cек")

    rub, usd = await rub_usd_btcticker()

    date = datetime_local_now().replace(tzinfo=None)
    query = (
        Worker
        .select(
            Worker,
            fn.SUM(Profit.amount).alias("profits_sum"),
        )
        .join(Profit, JOIN.LEFT_OUTER)
        .where(
            Profit.created.day == date.day,
            Profit.created.month == date.month,
            Profit.created.year == date.year
        )
        .group_by(Worker.id)
        .order_by(SQL("profits_sum").desc())
        .limit(1)
    )
    try:
        worker = query.execute()[0]
        topd_worker = f"<a href='tg://user?id={worker.cid}'>{worker.name}</a>"
    except IndexError:
        topd_worker = "Отсутсвует"

    return emojize(
        text.format(
            dyna_moon=get_work_moon(),
            services_status=get_work_status(),
            btc_usd_price=usd,
            btc_rub_price=rub,
            topd_worker=topd_worker,
            time=timenow,
            in_casino=0,
            in_trading=0,
            in_escort=0
        )
    )


async def dynapins(bot: Bot):
    if not isinstance(bot, Bot):
        raise TypeError(
            f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'")

    workers_chat = config("workers_chat")
    update_time = config("pin_update_time")
    text = await format_pin_text(pin_text())
    if text:
        message = await bot.send_message(workers_chat, text)
        await bot.pin_chat_message(workers_chat, message.message_id, disable_notification=True)

    while True:
        await asyncio.sleep(update_time)
        try:
            text = await format_pin_text(pin_text())
            await bot.edit_message_text(
                chat_id=workers_chat,
                message_id=message.message_id,
                text=text
            )
        except MessageNotModified:
            pass
        except MessageTextIsEmpty:
            pass
        except MessageToEditNotFound:
            text = await format_pin_text(pin_text())
            message = await bot.send_message(workers_chat, text)
            await bot.pin_chat_message(workers_chat, message.message_id, disable_notification=True)
