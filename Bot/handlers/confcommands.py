import random
from asyncio.exceptions import TimeoutError
from datetime import datetime
from datetime import timedelta
from utils.executional import datetime_local_now


from aiogram import types
from aiogram.utils.emoji import emojize

from loader import dp, exp_parser
from data import payload
from models import Worker, Profit
from utils.executional import datetime_local_now, rub_usd_btcticker, get_correct_str, find_lolz_user


@dp.message_handler(commands="help", workers_type=True)
async def help_command(message: types.Message):
    await message.reply(payload.help_text)


@dp.message_handler(commands="btc", workers_type=True)
async def btc_price(message: types.Message):
    rub, usd = await rub_usd_btcticker()
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
                in_team=f"{in_team.days} {get_correct_str(in_team.days, 'день', 'дня', 'дней')}",
                warns=f"{worker.warns} {get_correct_str(worker.warns, 'варн', 'варна', 'варнов')}"
            )
        )
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


@dp.message_handler(commands="top", workers_type=True)
async def team_top(message: types.Message):
    top_text = emojize(":woman_raising_hand: Топ воркеров за всё время:\n")
    total_profit = 0
    index = 1
    for worker in Worker.select().order_by(Worker.ref_balance.desc()).limit(10):
        total_profit += worker.ref_balance
        profits_count = len(worker.profits)
        print(worker.profits)
        place = ":1st_place_medal:" if index == 1 else ":2nd_place_medal:" if index == 2 else ":3rd_place_medal:" if index == 3 else f"{index}"
        top_text += emojize(f"\n{place} @{worker.username} - <b>{round(worker.ref_balance)}</b> RUB - {profits_count} {get_correct_str(profits_count, 'профит', 'профита', 'профитов')}")
        index += 1
    top_text += emojize(f"\n\n:money_with_wings: Общий профит - <b>{round(total_profit)}</b> RUB")
    await message.reply(top_text)

@dp.message_handler(commands="topd", workers_type=True)
async def team_top_day(message: types.Message):
    top_text = emojize(":woman_raising_hand: Топ воркеров за сегодня:\n")
    total_profit = 0
    index = 1
    for profit in Profit.select().where(Profit.created >= datetime_local_now().replace(tzinfo=None) - timedelta(days=1)):
        worker = profit.owner
        total_profit += worker.ref_balance
        profits_count = len(worker.profits)
        place = ":1st_place_medal:" if index == 1 else ":2nd_place_medal:" if index == 2 else ":3rd_place_medal:" if index == 3 else f"{index}"
        top_text += emojize(f"\n{place} @{worker.username} - <b>{round(worker.ref_balance)}</b> RUB - {profits_count} {get_correct_str(profits_count, 'профит', 'профита', 'профитов')}")
        index += 1
    top_text += emojize(f"\n\n:money_with_wings: Общий профит - <b>{round(total_profit)}</b> RUB")
    await message.reply(top_text)

@dp.message_handler(commands="topm", workers_type=True)
async def team_top_day(message: types.Message):
    top_text = emojize(":woman_raising_hand: Топ воркеров за месяц:\n")
    total_profit = 0
    index = 1
    for profit in Profit.select().where(Profit.created >= datetime_local_now().replace(tzinfo=None) - timedelta(days=30)):
        worker = profit.owner
        total_profit += worker.ref_balance
        profits_count = len(worker.profits)
        place = ":1st_place_medal:" if index == 1 else ":2nd_place_medal:" if index == 2 else ":3rd_place_medal:" if index == 3 else f"{index}"
        top_text += emojize(f"\n{place} @{worker.username} - <b>{round(worker.ref_balance)}</b> RUB - {profits_count} {get_correct_str(profits_count, 'профит', 'профита', 'профитов')}")
        index += 1
    top_text += emojize(f"\n\n:money_with_wings: Общий профит - <b>{round(total_profit)}</b> RUB")
    await message.reply(top_text)