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
