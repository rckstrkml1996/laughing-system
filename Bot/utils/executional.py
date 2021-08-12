import random
from datetime import datetime

import aiohttp
import pytz

from config import TIME_ZONE

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
