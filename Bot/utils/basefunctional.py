from random import randint
from datetime import timedelta

from peewee import ModelSelect, fn, JOIN, SQL
from loguru import logger
from customutils.models import Profit, Worker
from customutils.models import CasinoUser, CasinoPayment, CasinoUserHistory
from customutils.datefunc import datetime_local_now

from config import config


class BaseCommands:
    def casino_history_sum(self, user_id, editor=0) -> int:
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
    def casino_pays_sum(self, user_id, done_type=2) -> int:
        return int(
            (
                CasinoPayment.select(
                    fn.SUM(CasinoPayment.amount).alias("all_sum")
                ).where(
                    CasinoPayment.owner_id == user_id, CasinoPayment.done == done_type
                )
            )
            .execute()[0]
            .all_sum
            or 0
        )

    def all_profits_sum(self) -> int:
        return int(
            (Profit.select(fn.SUM(Profit.amount).alias("all_profits")))
            .execute()[0]
            .all_profits
            or 0
        )

    def get_profits_sum(self, worker_id) -> int:  # rename to get_profits_amount
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

    def all_share_sum(self) -> int:  # rename to get_profits_share
        return int(
            (Profit.select(fn.SUM(Profit.share).alias("all_share")))
            .execute()[0]
            .all_share
            or 0
        )

    def get_share_sum(self, worker_id) -> int:
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

    def workers_by_username(self, username: str):
        return Worker.select().where(
            fn.Lower(Worker.username.contains(username)), Worker.username_hide == False
        )

    def get_topworkers_all(self, limit: int = 15):
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

    def get_topworkers_month(self, limit: int = 15):
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

    def get_topworkers_day(self, limit: int = 15):
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

    def get_profits_all(self) -> int:
        return int(
            Profit.select(fn.SUM(Profit.amount).alias("all_profits"))
            .execute()[0]
            .all_profits
            or 0
        )

    def get_profits_month(self) -> int:
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

    def get_profits_day(self) -> ModelSelect:
        date = datetime_local_now()
        return Profit.select().where(
            Profit.created.day == date.day,
            Profit.created.month == date.month,
            Profit.created.year == date.year,
        )

    def get_profits_day_share(self) -> int:
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

    def get_profits_day_amount(self) -> int:
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

    def get_uniq_key(self) -> int:
        key = randint(111111, 999999)
        try:
            Worker.get(uniq_key=key)
            key = self.get_uniq_key()
        except Worker.DoesNotExist:
            pass

        return key

    def create_worker(self, chat_id, name, username=None) -> Worker:
        return Worker.create(
            cid=chat_id,
            uniq_key=self.get_uniq_key(),
            name=name,
            username=username,
        )

    def workers_today(self) -> ModelSelect:
        date = datetime_local_now()
        return Worker.select().where(
            Worker.registered.day == date.day,
            Worker.registered.month == date.month,
            Worker.registered.year == date.year,
        )

    def setup_admins_statuses(self):
        for admin_id in config("admins_id"):
            try:
                worker = Worker.get(cid=admin_id)
                if worker.status == 2:
                    worker.status = 5
                    worker.save()
            except Worker.DoesNotExist:
                logger.info(f"Admin with chat_id {admin_id} not found in base.")
