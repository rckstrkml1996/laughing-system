from random import randint
from asyncio import sleep

from aiogram import types
from aiogram.utils.emoji import emojize
from loguru import logger

from models import Worker
from loader import dp, config
from utils import basefunctional
from data import texts
from utils.executional import (
    rub_usd_btcticker,
    get_correct_str,
    get_info_about_worker,
)


@dp.message_handler(commands="help", workers_chat=True)
async def help_command(message: types.Message):
    await message.reply(texts.help_text)


@dp.message_handler(commands="btc", workers_chat=True)
@dp.message_handler(commands="btc", admins_chat=True)
async def btc_price(message: types.Message):
    try:
        rub, usd = await rub_usd_btcticker()
    except AssertionError:
        rub, usd = "Неизвестно", "Хз скока"

    await message.reply(
        texts.btc_text.format(
            rub=rub,
            usd=usd,
        )
    )
    logger.debug(f"Chat [{message.from_user.id}], get btc info")


@dp.message_handler(commands="clc", workers_chat=True)
@dp.message_handler(commands="clc", admins_chat=True)
async def clc_command(message: types.Message):
    await message.reply("Я временно не работаю!")
    # text = message.text.replace("/clc ", "")
    # try:
    #     result = exp_parser.parse(text).evaluate({"x": 0.8, "xx": 0.7})
    # except Exception as ex:
    #     logger.error(ex)
    #     result = "хз"

    # await message.reply(result)
    # logger.debug(f"Chat [{message.from_user.id}, /clc {text} result: {result}]")


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
        logger.debug(f"Chat [{message.from_user.id}], /me and he does not worker")


@dp.message_handler(commands=["card"], workers_chat=True)
@dp.message_handler(
    regexp="(К|к)арта для прямых|(П|п)рямые переводы", workers_chat=True
)
async def somefuncnamehahahahahahaahaha(message: types.Message):
    await message.answer(config.qiwi_card)


@dp.message_handler(commands="cck", workers_chat=True)
@dp.message_handler(commands="cck", admins_chat=True)
async def cock_size_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        if worker.cock_size is None:
            worker.cock_size = randint(2, 24)
            worker.save()
        smile = (
            ":cry:"
            if worker.cock_size < 8
            else ":pensive:"
            if worker.cock_size < 16
            else ":smirk:"
        )
        await message.reply(
            texts.cck_size_text.format(size=worker.cock_size, smile=emojize(smile))
        )
    except Worker.DoesNotExist:
        logger.debug(f"[{message.from_user.id}], /cck in chat does not Worker.")


def get_place(i):
    return emojize(
        ":1st_place_medal:"
        if i == 0
        else ":2nd_place_medal:"
        if i == 1
        else ":3rd_place_medal:"
        if i == 2
        else ":hankey:"
    )


@dp.message_handler(commands="top", workers_chat=True)
@dp.message_handler(commands="top", admins_chat=True)
async def team_top(message: types.Message):
    logger.debug(f"[{message.from_user.id}], wants /top in chat.")
    query = basefunctional.get_topworkers_all(limit=10)  # limit = 15
    all_profits = basefunctional.get_profits_all()

    if query.count() == 0:
        msg = await message.reply(texts.top_none_text)
    else:
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
                    f"{get_place(i)} {username} - <b>{int(worker.profits_sum)} RUB</b> - {count_text}"
                )

        msg = await message.reply(
            texts.top_text.format(
                period="всё время",
                profits="\n".join(profit_text_list),
                all_profits=all_profits,
            ),
            disable_notification=True,
        )
        logger.debug(f"User {message.from_user.id} /top in chat succesfully.")

    await sleep(22)
    await message.delete()
    await msg.delete()


@dp.message_handler(commands="topm", workers_chat=True)
async def team_top_day(message: types.Message):
    logger.debug(f"[{message.from_user.id}], wants /topm in chat.")
    query = basefunctional.get_topworkers_month(limit=10)  # limit = 15 autodelta
    all_profits = basefunctional.get_profits_month()

    if query.count() == 0:
        msg = await message.reply(texts.top_none_text)
    else:
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
                    f"{get_place(i + 1)} {username} - <b>{int(worker.profits_sum)} RUB</b> - {count_text}"
                )

        msg = await message.reply(
            texts.top_text.format(
                period="месяц",
                profits="\n".join(profit_text_list),
                all_profits=all_profits,
            ),
            disable_notification=True,
        )
        logger.debug(f"User {message.from_user.id} /topm in chat succesfully.")

    await sleep(22)
    await message.delete()
    await msg.delete()


@dp.message_handler(commands="topd", workers_chat=True)
@dp.message_handler(commands="topd", admins_chat=True)
async def team_top_day(message: types.Message):
    logger.debug(f"[{message.from_user.id}], wants /topd in chat.")
    query = basefunctional.get_topworkers_day(limit=10)  # limit = 15
    all_profits = basefunctional.get_profits_day_amount()

    if query.count() == 0:
        msg = await message.reply(texts.top_none_text)
    else:
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
                    f"{get_place(i + 1)} {username} - <b>{int(worker.profits_sum)} RUB</b> - {count_text}"
                )

        msg = await message.reply(
            texts.top_text.format(
                period="день",
                profits="\n".join(profit_text_list),
                all_profits=all_profits,
            ),
            disable_notification=True,
        )
        logger.debug(f"User {message.from_user.id} /topd in chat succesfully.")

    await sleep(22)
    await message.delete()
    await msg.delete()
