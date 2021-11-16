import re
from random import randint
from typing import Union, Optional
from datetime import timedelta

from aiogram.utils.markdown import quote_html
from peewee import ModelSelect, fn, JOIN, SQL
from loguru import logger

from models import (
    Profit,
    Worker,
    CasinoPayment,
    EscortPayment,
    TradingPayment,
    CasinoUser,
    EscortUser,
    TradingUser,
    CasinoUserHistory,
)
from customutils import datetime_local_now


def get_topworker_today() -> Optional[Worker]:
    date = datetime_local_now()
    try:
        return (
            Worker.select(
                Worker,
                fn.SUM(Profit.amount).alias("profits_sum"),
                fn.COUNT(Profit.id).alias("profits_count"),
            )
            .join(Profit, JOIN.LEFT_OUTER)
            .where(
                Profit.created.day == date.day,
                Profit.created.month == date.month,
                Profit.created.year == date.year,
            )
            .group_by(Worker.id)
            .order_by(SQL("profits_sum").desc())
            .limit(1)
            .get()
        )  # @Slavs027 - какашка?
    except Worker.DoesNotExist:
        return


def delete_old_payments(
    payment_type: Union[CasinoPayment, EscortPayment, TradingPayment]
) -> int:
    delta = datetime_local_now() - timedelta(days=14)
    try:  # define in drugaya func epta
        return payment_type.delete().where(payment_type.created < delta).execute()
    except Exception as ex:
        logger.exception(ex)


def get_payments_count(
    payment_type,
    pay_owner: Union[CasinoUser, EscortUser, TradingUser],
) -> int:
    return (
        payment_type.select()
        .where(
            payment_type.owner_id == pay_owner.id,
            payment_type.done == 1,
        )
        .count()
    )


def casino_history_sum(user_id, editor=0) -> int:
    return int(
        (
            CasinoUserHistory.select(
                fn.SUM(CasinoUserHistory.amount).alias("all_sum")
            ).where(
                CasinoUserHistory.owner_id == user_id,
                CasinoUserHistory.editor == editor,
            )
        )
        .execute()[0]
        .all_sum
        or 0
    )


# done in CasinoPayment!
def casino_pays_sum(user_id, done_type=2) -> int:
    return int(
        (
            CasinoPayment.select(fn.SUM(CasinoPayment.amount).alias("all_sum")).where(
                CasinoPayment.owner_id == user_id, CasinoPayment.done == done_type
            )
        )
        .execute()[0]
        .all_sum
        or 0
    )


def all_profits_sum() -> int:
    return int(
        (Profit.select(fn.SUM(Profit.amount).alias("all_profits")))
        .execute()[0]
        .all_profits
        or 0
    )


def get_profits_sum(worker_id) -> int:  # rename to get_profits_amount
    return int(
        (
            Profit.select(fn.SUM(Profit.amount).alias("all_profits")).where(
                Profit.owner_id == worker_id
            )
        )
        .execute()[0]
        .all_profits
        or 0
    )


def all_share_sum() -> int:  # rename to get_profits_share
    return int(
        (Profit.select(fn.SUM(Profit.share).alias("all_share"))).execute()[0].all_share
        or 0
    )


def get_share_sum(worker_id) -> int:
    return int(
        (
            Profit.select(fn.SUM(Profit.share).alias("all_share")).where(
                Profit.owner_id == worker_id
            )
        )
        .execute()[0]
        .all_share
        or 0
    )


def workers_by_username(username: str):
    username = re.sub(r"[^a-z0-9]", "", username)  # .lower() - replace by fn.Lower
    return Worker.select().where(
        fn.Lower(Worker.username.contains(username)), Worker.username_hide == False
    )


def get_topworkers_all(limit: int = 15):
    return (
        Worker.select(
            Worker,
            fn.SUM(Profit.amount).alias("profits_sum"),
            fn.COUNT(Profit.id).alias("profits_count"),
        )
        .join(Profit, JOIN.LEFT_OUTER)
        .group_by(Worker.id)
        .order_by(SQL("profits_sum").desc())
        .limit(limit)
    )


def get_topworkers_month(limit: int = 15):
    delta = datetime_local_now() - timedelta(days=30)
    return (
        Worker.select(
            Worker,
            fn.SUM(Profit.amount).alias("profits_sum"),
            fn.COUNT(Profit.id).alias("profits_count"),
        )
        .join(Profit, JOIN.LEFT_OUTER)
        .where(Profit.created >= delta)
        .group_by(Worker.id)
        .order_by(SQL("profits_sum").desc())
        .limit(limit)
    )


def get_topworkers_week(limit: int = 15):
    delta = datetime_local_now() - timedelta(days=7)
    return (
        Worker.select(
            Worker,
            fn.SUM(Profit.amount).alias("profits_sum"),
            fn.COUNT(Profit.id).alias("profits_count"),
        )
        .join(Profit, JOIN.LEFT_OUTER)
        .where(Profit.created >= delta)
        .group_by(Worker.id)
        .order_by(SQL("profits_sum").desc())
        .limit(limit)
    )


def get_topworkers_day(limit: int = 15):
    date = datetime_local_now()
    return (
        Worker.select(
            Worker,
            fn.SUM(Profit.amount).alias("profits_sum"),
            fn.COUNT(Profit.id).alias("profits_count"),
        )
        .join(Profit, JOIN.LEFT_OUTER)
        .where(
            Profit.created.day == date.day,
            Profit.created.month == date.month,
            Profit.created.year == date.year,
        )
        .group_by(Worker.id)
        .order_by(SQL("profits_sum").desc())
        .limit(limit)
    )


def get_profits_all() -> int:
    return int(
        Profit.select(fn.SUM(Profit.amount).alias("all_profits"))
        .execute()[0]
        .all_profits
        or 0
    )


def get_profits_month() -> int:
    delta = datetime_local_now() - timedelta(days=30)
    return int(
        (
            Profit.select(fn.SUM(Profit.amount).alias("all_profits")).where(
                Profit.created >= delta
            )
        )
        .execute()[0]
        .all_profits
        or 0
    )


def get_profits_week() -> int:
    delta = datetime_local_now() - timedelta(days=7)
    return int(
        (
            Profit.select(fn.SUM(Profit.amount).alias("all_profits")).where(
                Profit.created >= delta
            )
        )
        .execute()[0]
        .all_profits
        or 0
    )


def get_profits_day() -> ModelSelect:
    date = datetime_local_now()
    return Profit.select().where(
        Profit.created.day == date.day,
        Profit.created.month == date.month,
        Profit.created.year == date.year,
    )


def get_profits_day_share() -> int:
    date = datetime_local_now()
    return int(
        (
            Profit.select(fn.SUM(Profit.share).alias("all_share")).where(
                Profit.created.day == date.day,
                Profit.created.month == date.month,
                Profit.created.year == date.year,
            )
        )
        .execute()[0]
        .all_share
        or 0
    )


def get_profits_day_amount() -> int:
    date = datetime_local_now()
    return int(
        (
            Profit.select(fn.SUM(Profit.amount).alias("all_profits")).where(
                Profit.created.day == date.day,
                Profit.created.month == date.month,
                Profit.created.year == date.year,
            )
        )
        .execute()[0]
        .all_profits
        or 0
    )


def get_uniq_key() -> int:
    key = randint(111111, 999999)
    try:
        Worker.get(uniq_key=key)
        key = get_uniq_key()
    except Worker.DoesNotExist:
        pass
    return key


def create_worker(chat_id, name, username=None, referal: Worker = None) -> Worker:
    return Worker.create(
        owner=referal,
        cid=chat_id,
        uniq_key=get_uniq_key(),
        name=quote_html(name),
        username=username,
    )


def workers_today() -> ModelSelect:
    date = datetime_local_now()
    return Worker.select().where(
        Worker.registered.day == date.day,
        Worker.registered.month == date.month,
        Worker.registered.year == date.year,
    )


def set_status(worker_cid: int, status: int):
    try:
        worker = Worker.get(cid=worker_cid)
        worker.status = status
        worker.send_summary = True
        worker.save()
    except Worker.DoesNotExist:
        pass


def get_visible_mamonths_casino(worker: Worker):
    return CasinoUser.select().where(
        CasinoUser.owner == worker, CasinoUser.visible == True
    )
