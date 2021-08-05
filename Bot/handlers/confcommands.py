import random

from aiogram import types

from loader import dp
from data import payload
from models import Worker
from utils.executional import datetime_local_now, rub_usd_btcticker


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
    await message.reply(eval(message.text.replace("/clc", "")))


@dp.message_handler(commands="me", workers_type=True)
async def me_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

        len_profits = len(worker.profits)
        sum_profits = sum(map(lambda prft: prft.amount, worker.profits))
        try:
            middle_profits = sum_profits / len_profits
        except ZeroDivisionError:
            middle_profits = 0

        await message.reply(
            payload.me_text.format(
                cid=message.from_user.id,
                username=message.from_user.username,
                len_profits=len_profits,
                sum_profits=sum_profits,
                middle_profits=middle_profits,
                in_team=in_team.days,
            )
        )
    except Worker.DoesNotExist:
        pass


@ dp.message_handler(commands="cck", workers_type=True)
async def cock_size_command(message: types.Message):
    try:
        worker = Worker.get(cid=message.from_user.id)
        if worker.cock_size is None:
            worker.cock_size = random.randint(2, 24)
            worker.save()
        await message.reply(worker.cock_size)
    except Worker.DoesNotExist:
        pass
