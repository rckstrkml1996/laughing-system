import random
from asyncio.exceptions import TimeoutError
from datetime import datetime

from aiogram import types
from aiogram.utils.emoji import emojize
from loguru import logger

from loader import dp, exp_parser, db_commands
from customutils.models import Worker, Profit
from customutils.datefunc import datetime_local_now
from data import payload
from utils.executional import (
    rub_usd_btcticker,
    get_correct_str,
    find_lolz_user,
    get_info_about_worker,
)


@dp.message_handler(commands="help", workers_chat=True)
async def help_command(message: types.Message):
    await message.reply(payload.help_text)


@dp.message_handler(commands="btc", workers_chat=True)
@dp.message_handler(commands="btc", admins_chat=True)
async def btc_price(message: types.Message):
    try:
        rub, usd = await rub_usd_btcticker()
    except AssertionError:
        rub, usd = "Неизвестно", "Хз скока"

    await message.reply(
        payload.btc_text.format(
            rub=rub,
            usd=usd,
        )
    )
    logger.debug(f"Chat User - {message.from_user.id}, get btc info")


@dp.message_handler(commands="clc", workers_chat=True)
@dp.message_handler(commands="clc", admins_chat=True)
async def clc_command(message: types.Message):
    text = message.text.replace("/clc ", "")
    try:
        result = exp_parser.parse(text).evaluate({})
    except:
        result = "хз"
    await message.reply(result)
    logger.debug(f"Chat User - {message.from_user.id}, /clc {text} result: {result}")


@dp.message_handler(commands="me", workers_chat=True)
@dp.message_handler(commands="me", admins_chat=True)
async def me_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        text = get_info_about_worker(worker)
        await message.reply(text)
        logger.debug(f"Worker - {message.from_user.id}, /me in chat, succesful.")
    except Worker.DoesNotExist:
        await message.reply("Ты не Воркер!")
        logger.debug(f"Chat User - {message.from_user.id}, /me and he does not worker")


@dp.message_handler(commands="lzt", workers_chat=True)
async def lzt_command(message: types.Message):
    try:
        json = await find_lolz_user(message.text.replace("/lzt ", "", 1))
        user = json["users"][0]

        reg_date = datetime.fromtimestamp(user["user_register_date"]).strftime(
            "%d.%m.%Y"
        )
        last_seen_date = datetime.fromtimestamp(user["user_last_seen_date"]).strftime(
            "%d.%m.%Y в %H:%M"
        )

        messages_count = user["user_message_count"]

        await message.reply(
            payload.lzt_text.format(
                permalink=user["links"]["permalink"],
                username=user["username"],
                user_title=user["user_title"],
                reg_date=reg_date,
                last_seen_date=last_seen_date,
                message_count=f"{get_correct_str(messages_count, 'сообщение', 'сообщения', 'сообщений')}",
                like_count=user["user_like_count"],
            )
        )
        logger.debug(f"User - {message.from_user.id}, /lzt get succesfully.")
    except TimeoutError:
        await message.reply(payload.lolz_down_text)
        logger.info(
            f"User - {message.from_user.id}, /lzt in chat and TimeoutError was raised."
        )
    except:
        await message.reply("Ошибка!")
        logger.info(
            f"User - {message.from_user.id}, Some Error in chat by /lzt command"
        )


@dp.message_handler(commands="cck", workers_chat=True)
@dp.message_handler(commands="cck", admins_chat=True)
async def cock_size_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        if worker.cock_size is None:
            worker.cock_size = random.randint(2, 24)
            worker.save()
        smile = (
            ":cry:"
            if worker.cock_size < 8
            else ":pensive:"
            if worker.cock_size < 16
            else ":smirk:"
        )
        await message.reply(
            payload.cck_size_text.format(size=worker.cock_size, smile=emojize(smile))
        )
    except Worker.DoesNotExist:
        logger.debug(f"User - {message.from_user.id}, /cck in chat does not Worker.")


def get_place(i):
    return emojize(
        ":1st_place_medal:"
        if i == 1
        else ":2nd_place_medal:"
        if i == 2
        else ":3rd_place_medal:"
        if i == 3
        else f"  {i}"
        if i < 10
        else f"{i}"
    )


@dp.message_handler(commands="top", workers_chat=True)
async def team_top(message: types.Message):
    logger.debug(f"User - {message.from_user.id}, wants /top in chat.")
    query = db_commands.get_topworkers_all()  # limit = 15
    all_profits = db_commands.get_profits_all()

    if query.count() == 0:
        await message.reply(payload.top_none_text)
        return  # logg

    profit_text_list = []

    for i, worker in enumerate(query):
        if worker.profits_count:
            username = (
                "Скрыт"
                if worker.username_hide
                else f"@{worker.username}"
                if worker.username
                else "Без юзернейма"
            )
            count_text = get_correct_str(
                worker.profits_count, "профит", "профита", "профитов"
            )
            profit_text_list.append(
                f"{get_place(i + 1)} {username} - <b>{int(worker.profits_sum)}</b> RUB - {count_text}"
            )

    await message.reply(
        payload.top_text.format(
            period="всё время",
            profits="\n".join(profit_text_list),
            all_profits=all_profits,
        )
    )
    logger.debug(f"User {message.from_user.id} /top in chat succesfully.")


@dp.message_handler(commands="topm", workers_chat=True)
async def team_top_day(message: types.Message):
    logger.debug(f"User - {message.from_user.id}, wants /topm in chat.")
    query = db_commands.get_topworkers_month()  # limit = 15 autodelta
    all_profits = db_commands.get_profits_month()

    if query.count() == 0:
        await message.reply(payload.top_none_text)
        return  # logg

    profit_text_list = []

    for i, worker in enumerate(query):
        if worker.profits_count:
            username = (
                "Скрыт"
                if worker.username_hide
                else f"@{worker.username}"
                if worker.username
                else "Без юзернейма"
            )
            count_text = get_correct_str(
                worker.profits_count, "профит", "профита", "профитов"
            )
            profit_text_list.append(
                f"{get_place(i + 1)} {username} - <b>{int(worker.profits_sum)}</b> RUB - {count_text}"
            )

    await message.reply(
        payload.top_text.format(
            period="месяц",
            profits="\n".join(profit_text_list),
            all_profits=all_profits,
        )
    )
    logger.debug(f"User {message.from_user.id} /topm in chat succesfully.")


@dp.message_handler(commands="topd", workers_chat=True)
async def team_top_day(message: types.Message):
    logger.debug(f"User - {message.from_user.id}, wants /topd in chat.")
    query = db_commands.get_topworkers_day()  # limit = 15
    all_profits = db_commands.get_profits_day_amount()

    if query.count() == 0:
        await message.reply(payload.top_none_text)
        return  # logg

    profit_text_list = []

    for i, worker in enumerate(query):
        if worker.profits_count:
            username = (
                "Скрыт"
                if worker.username_hide
                else f"@{worker.username}"
                if worker.username
                else "Без юзернейма"
            )
            count_text = get_correct_str(
                worker.profits_count, "профит", "профита", "профитов"
            )
            profit_text_list.append(
                f"{get_place(i + 1)} {username} - <b>{int(worker.profits_sum)}</b> RUB - {count_text}"
            )

    await message.reply(
        payload.top_text.format(
            period="день",
            profits="\n".join(profit_text_list),
            all_profits=all_profits,
        )
    )
    logger.debug(f"User {message.from_user.id} /topd in chat succesfully.")
