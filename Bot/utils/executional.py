import random
from datetime import datetime

import aiohttp
import pytz
from aiogram.utils.emoji import emojize

from data.payload import services_status, me_text
from config import config, TIME_ZONE

local_tz = pytz.timezone(TIME_ZONE)

num2emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:',
              ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']


def datetime_local_now():
    local_dt = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # return datetime instance


def num2emoji(number):
    try:
        return num2emojis[number]
    except IndexError:
        return ":1234:"


def get_random_analog(general: int):
    prices = {"Л. 95 Бензина": 50.15, "Кусков Пиццы": 80, "Коробок Спичек": 20}
    price = random.choice(list(prices.keys()))
    return f"Это ~ {'{:,}'.format(int(general / prices[price])).replace(',', ' ')} {price}"


async def get_btcticker():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://blockchain.info/ru/ticker') as response:
            return await response.json()


async def rub_usd_btcticker():
    ticker = await get_btcticker()
    rub = ticker["RUB"]["last"]
    usd = ticker["USD"]["last"]
    return rub, usd


async def get_btcmarket_price():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.blockchain.info/charts/market-price') as response:
            return await response.json()


async def find_lolz_user(username):
    headers = {'Authorization': f'Bearer 0', 'Cookie': 'xf_logged_in=1'}
    async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(5)) as session:
        async with session.get(f'https://lolz.guru/api/index.php?users/find&username={username}') as response:
            return await response.json()


def get_correct_str(num, str1, str2, str3):
    val = num % 100

    if val > 10 and val < 20:
        return f"{num} {str3}"
    else:
        val = num % 10
        if val == 1:
            return f"{num} {str1}"
        elif val > 1 and val < 5:
            return f"{num} {str2}"
        else:
            return f"{num} {str3}"


def new_pin_text(text: str):
    pin_path = config("pin_path")
    fl = open(pin_path, "w")
    fl.write(text)
    fl.close()


def get_work_status():
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    antikino_work = config("antikino_work")

    all_work = casino_work and escort_work and antikino_work

    return emojize(
        services_status.format(
            casino_status=f":full_moon: Казино СКАМ" if casino_work else f":new_moon: <del>Казино СКАМ</del>",
            escort_status=f":full_moon: Эскорт СКАМ" if escort_work else f":new_moon: <del>Эскорт СКАМ</del>",
            antikino_status=f":full_moon: Антикино СКАМ" if antikino_work else f":new_moon: <del>Антикино СКАМ</del>",
            team_status=":full_moon: Общий статус: Ворк" if all_work else ":new_moon: Общий статус: Не ворк",
        )
    )


def get_info_about_worker(worker):
    in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

    len_profits = len(worker.profits)
    sum_profits = sum(map(lambda prft: prft.amount, worker.profits))
    try:
        middle_profits = sum_profits / len_profits
    except ZeroDivisionError:
        middle_profits = 0

    return me_text.format(
        cid=worker.cid,
        username=worker.username,
        len_profits=len_profits,
        sum_profits=sum_profits,
        middle_profits=middle_profits,
        in_team=f"{in_team.days} {get_correct_str(in_team.days, 'день', 'дня', 'дней')}",
        warns=f"{worker.warns} {get_correct_str(worker.warns, 'варн', 'варна', 'варнов')}"
    )
