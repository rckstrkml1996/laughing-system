import re
import random

import aiohttp
from aiogram.utils.emoji import emojize

from models import CasinoUser, CasinoUserHistory
from customutils import datetime_local_now
from loader import config, status_names
from data.texts import (
    services_status,
    casino_mamonth_info,
    escort_mamonth_info,
    me_text,
    casino_text,
    trading_text,
    mention_text,
)
from data.keyboards import cas_info_keyboard, esc_info_keyboard
from utils import basefunctional


def get_trading_info(uniq_key) -> str:
    pay_cards = "\n".join(
        list(
            map(
                lambda c: f"&#127479;&#127482; <code>{c}</code>",
                config.fake_cards.ukrainian,
            )
        )
        + list(
            map(
                lambda c: f"&#127482;&#127462; <code>{c}</code>",
                config.fake_cards.russian,
            )
        )
    )

    pay_qiwis = "\n".join(
        list(
            map(
                lambda c: f"&#127479;&#127482; <code>{c}</code>",
                config.fake_numbers.ukrainian,
            )
        )
        + list(
            map(
                lambda c: f"&#127482;&#127462; <code>{c}</code>",
                config.fake_numbers.russian,
            )
        )
    )

    return trading_text.format(
        reviews_link=config.reviews_link,
        trading_username=config.casino_username,
        trading_sup_username=config.casino_sup_username,
        worker_id=uniq_key,
        pay_cards=pay_cards,
        pay_qiwis=pay_qiwis,
    )


def get_casino_info(uniq_key) -> str:
    pay_cards = "\n".join(
        list(
            map(
                lambda c: f"&#127479;&#127482; <code>{c}</code>",
                config.fake_cards.russian,
            )
        )
        + list(
            map(
                lambda c: f"&#127482;&#127462; <code>{c}</code>",
                config.fake_cards.ukrainian,
            )
        )
    )

    pay_qiwis = "\n".join(
        list(
            map(
                lambda c: f"&#127479;&#127482; <code>{c}</code>",
                config.fake_numbers.russian,
            )
        )
        + list(
            map(
                lambda c: f"&#127482;&#127462; <code>{c}</code>",
                config.fake_numbers.ukrainian,
            )
        )
    )

    return casino_text.format(
        casino_username=config.casino_username,
        casino_sup_username=config.casino_sup_username,
        worker_id=uniq_key,
        pay_cards=pay_cards,
        pay_qiwis=pay_qiwis,
    )


def get_escort_mamonth_info(user: CasinoUser) -> str:
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")

    return (
        escort_mamonth_info.format(
            smile=random_heart(),
            uid=user.id,
            chat_id=user.cid,
            name=user.fullname,
            time=timenow,
        ),
        esc_info_keyboard(user.id),
    )


def get_casino_mamonth_info(user: CasinoUser) -> str:
    games_win = user.history.where(CasinoUserHistory.editor == 2).count()
    adds = user.history.where(CasinoUserHistory.editor == 0)
    adds_count = adds.count()
    adds_amount = basefunctional.casino_history_sum(user.id, editor=2)
    pays_amount = basefunctional.casino_history_sum(user.id)  # editor == 0
    # pays_amount = basefunctional.casino_pays_sum(user.id)  # done == 2
    games_lose = user.history.where(CasinoUserHistory.editor == 3).count()

    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")

    return (
        casino_mamonth_info.format(
            smile=random_heart(),
            wins_count=games_win,
            adds_count=adds_count,
            lose_count=games_lose,
            adds_amount=adds_amount,
            pays_accepted_amount=pays_amount,
            uid=user.id,
            chat_id=user.cid,
            name=user.fullname,
            balance=user.balance,
            time=timenow,
            fortune="Вкл"
            if user.fort_chance == 100
            else "Выкл"
            if user.fort_chance == 0
            else f"{user.fort_chance} %",
        ),
        cas_info_keyboard(user.id, user.fort_chance, user.min_deposit, user.stopped),
    )


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


def random_heart():
    return emojize(random.choice(hearts))


analogs = [
    "Работаем!",
    "Жи есс",
    "Слава что ти сделал?",
    "sudo systemctl restart mainbot",
    "Ацуруалафла-ляля",
    "Хайду 4 годика.",
    "турик - лох)",
    "BTS - Top",
    "Матросс одобряет!",
    "Настя биз ещё жива?",
    "0.14523415 Seconds",
    "Niggas in Paris",
    "UK Drill.",
]


def get_random_analog():
    return random.choice(analogs)


async def get_btcticker():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://blockchain.info/ticker") as response:
            assert response.status == 200
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
            assert response.status == 200
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


def get_work_moon():
    casino_work = config.casino_work
    escort_work = config.escort_work
    trading_work = config.trading_work

    all_work = casino_work and escort_work and trading_work

    return ":full_moon:" if all_work else ":new_moon:"


def get_work_status():
    casino_work = config.casino_work
    escort_work = config.escort_work
    trading_work = config.trading_work

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
            team_status=":full_moon: Общий статус: <b>Ворк</b>"
            if all_work
            else ":new_moon: Общий статус: <b>Не ворк</b>",
        )
    )


def get_info_about_worker(worker):
    in_team = datetime_local_now() - worker.registered

    len_profits = worker.profits.count()
    sum_profits = basefunctional.get_profits_sum(worker.id)

    try:
        middle_profits = int(sum_profits / len_profits)
    except ZeroDivisionError:
        middle_profits = 0

    return me_text.format(
        mention=mention_text.format(user_id=worker.cid, text=worker.name),
        cid=worker.cid,
        status=status_names.get_value(worker.status),
        profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
        sum_profits=sum_profits,
        middle_profits=middle_profits,
        in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
        warns=get_correct_str(worker.warns, "варн", "варна", "варнов"),
    )
