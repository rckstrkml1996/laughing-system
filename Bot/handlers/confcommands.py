import random
from asyncio.exceptions import TimeoutError
from datetime import datetime

from aiogram import types
from aiogram.utils.emoji import emojize

from loader import dp, exp_parser
from data import payload
from models import Worker
from utils.executional import rub_usd_btcticker, get_correct_str, find_lolz_user, get_info_about_worker


@dp.message_handler(commands="help", workers_type=True)
async def help_command(message: types.Message):
    await message.reply(payload.help_text)


@dp.message_handler(commands="btc", workers_type=True)
async def btc_price(message: types.Message):
    rub, usd = await rub_usd_ticker()
    await message.reply(payload.btc_text.format(
        rub=rub,
        usd=usd,
    ))


@dp.message_handler(commands="clc", workers_type=True)
async def clc_command(message: types.Message):
    try:
        result = exp_parser.parse(
            message.text.replace("/clc ", "")).evaluate({})
    except:
        result = "хз"
    await message.reply(result)


@dp.message_handler(commands="me", workers_type=True)
async def me_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        text = get_info_about_worker(worker)
        await message.answer(text)
    except Worker.DoesNotExist:
        pass


@dp.message_handler(commands="lzt", workers_type=True)
async def lzt_command(message: types.Message):
    try:
        json = await find_lolz_user(message.text.replace("/lzt ", "", 1))
        user = json["users"][0]

        reg_date = datetime.fromtimestamp(
            user["user_register_date"]
        ).strftime("%d.%m.%Y")
        last_seen_date = datetime.fromtimestamp(
            user["user_last_seen_date"]
        ).strftime("%d.%m.%Y в %H:%M")

        messages_count = user["user_message_count"]

        await message.reply(payload.lzt_text.format(
            permalink=user["links"]["permalink"],
            username=user["username"],
            user_title=user["user_title"],
            reg_date=reg_date,
            last_seen_date=last_seen_date,
            message_count=f"{messages_count} {get_correct_str(messages_count, 'сообщение', 'сообщения', 'сообщений')}",
            like_count=user["user_like_count"],
        ))
    except TimeoutError:
        await message.reply(payload.lolz_down_text)
    except:
        await message.reply("Ошибка!")


@dp.message_handler(commands="cck", workers_type=True)
async def cock_size_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        if worker.cock_size is None:
            worker.cock_size = random.randint(2, 24)
            worker.save()
        smile = ":cry:" if worker.cock_size < 8 else ":pensive:" if worker.cock_size < 16 else ":smirk:"
        await message.reply(payload.cck_size_text.format(
            size=worker.cock_size,
            smile=emojize(smile)
        ))
    except Worker.DoesNotExist:
        pass
