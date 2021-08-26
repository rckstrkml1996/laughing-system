import re
import random
from asyncio.exceptions import TimeoutError

import aiohttp
from aiohttp.client_exceptions import ClientProxyConnectionError
from aiogram.utils.emoji import emojize

from config import config
from loader import db_commands
from data.payload import services_status, me_text
from customutils.datefunc import datetime_local_now
from customutils.qiwiapi import QiwiApi

num2emojis = [
    ":zero:",
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:",
    ":seven:",
    ":eight:",
    ":nine:",
    ":keycap_ten:",
]

hearts = [
    ":red_heart:",
    ":orange_heart:",
    ":yellow_heart:",
    ":green_heart:",
    ":blue_heart:",
    ":purple_heart:",
    ":black_heart:",
    ":white_heart:",
    ":brown_heart:",
]


def num2emoji(number):
    try:
        return num2emojis[number]
    except IndexError:
        return ":1234:"


def random_heart():
    return emojize(random.choice(hearts))


def get_random_analog(general: int):
    prices = {"Л. 95 Бензина": 50.15, "Кусков Пиццы": 80, "Коробок Спичек": 20}
    price = random.choice(list(prices.keys()))
    return (
        f"Это ~ {'{:,}'.format(int(general / prices[price])).replace(',', ' ')} {price}"
    )


async def get_btcticker():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://blockchain.info/ru/ticker") as response:
            return await response.json()


async def rub_usd_btcticker():
    ticker = await get_btcticker()
    rub = ticker["RUB"]["last"]
    usd = ticker["USD"]["last"]
    return rub, usd


async def get_btcmarket_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.blockchain.info/charts/market-price"
        ) as response:
            return await response.json()


async def find_lolz_user(username):
    headers = {"Authorization": f"Bearer 0", "Cookie": "xf_logged_in=1"}
    async with aiohttp.ClientSession(
        headers=headers, timeout=aiohttp.ClientTimeout(5)
    ) as session:
        async with session.get(
            f"https://lolz.guru/api/index.php?users/find&username={username}"
        ) as response:
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
    fl = open(pin_path, "w", encoding="utf-8")
    fl.write(text)
    fl.close()


def get_work_moon():
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    trading_work = config("trading_work")

    all_work = casino_work and escort_work and trading_work

    return ":full_moon:" if all_work else ":new_moon:"


def get_work_status():
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    trading_work = config("trading_work")

    all_work = casino_work and escort_work and trading_work

    return emojize(
        services_status.format(
            casino_status=f":full_moon: Казино СКАМ"
            if casino_work
            else f":new_moon: <del>Казино СКАМ</del>",
            escort_status=f":full_moon: Эскорт СКАМ"
            if escort_work
            else f":new_moon: <del>Эскорт СКАМ</del>",
            trading_status=f":full_moon: Трейдинг СКАМ"
            if trading_work
            else f":new_moon: <del>Трейдинг СКАМ</del>",
            team_status=":full_moon: Общий статус: Ворк"
            if all_work
            else ":new_moon: Общий статус: Не ворк",
        )
    )


def get_info_about_worker(worker):
    in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

    len_profits = worker.profits.count()
    sum_profits = db_commands.get_profits_sum(worker.id)

    try:
        middle_profits = int(sum_profits / len_profits)
    except ZeroDivisionError:
        middle_profits = 0

    return me_text.format(
        cid=worker.cid,
        username=worker.username,
        profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
        sum_profits=sum_profits,
        middle_profits=middle_profits,
        in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
        warns=get_correct_str(worker.warns, "варн", "варна", "варнов"),
    )


def setup_admins_statuses():
    for admin_id in config("admins_id"):
        try:
            worker = Worker.get(cid=admin_id)
            worker.status = 5
            worker.save()
        except Worker.DoesNotExist:
            logger.info(f"Admin with chat_id {admin_id} not found in base.")


def find_token(conf_token: str):
    srch = re.search(r"\(([^\(^\)]+)\)", conf_token)
    if srch:
        return conf_token.replace(srch.group(0), "")
    return conf_token


def get_api(conf_token: str):
    srch = re.search(r"\(([^\(^\)]+)\)", conf_token)
    if srch:
        return QiwiApi(
            token=conf_token.replace(srch.group(0), ""), proxy_url=srch.group(1)
        ), srch.group(1)
    return QiwiApi(conf_token), None


def delete_api_proxy(conf_token: str):
    srch = re.search(r"\(([^\(^\)]+)\)", conf_token)
    if srch:
        tokens = config("qiwi_tokens")
        if isinstance(tokens, list):
            try:
                tokens[tokens.index(conf_token)] = conf_token.replace(srch.group(0), "")
                config.edit_config("qiwi_tokens", tokens)
            except ValueError:
                pass  # shiiit
        else:
            config.edit_config("qiwi_tokens", conf_token.replace(srch.group(0), ""))

        return srch.group(0)[1:-1]


async def check_proxy(proxy_url: str):
    url = "http://example.com"
    answer = True
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(4)) as session:
        try:
            await session.get(url, proxy=proxy_url)
        except TimeoutError:  # this is for different log
            answer = False
        except ClientProxyConnectionError:
            answer = False  # this is for different log
        finally:
            await session.close()

        return answer
