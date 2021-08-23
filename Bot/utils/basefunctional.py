from random import randint
from datetime import timedelta

from peewee import fn, JOIN, SQL

from customutils.models import Profit, Worker
from customutils.datefunc import datetime_local_now


class BaseCommands:
    def all_profits_sum(self) -> int:
        return int((
            Profit
            .select(
                fn.SUM(Profit.amount).alias("all_profits")
            )
        ).execute()[0].all_profits or 0)

    def get_profits_sum(self, worker_id) -> int:
        return int((
            Profit
            .select(
                fn.SUM(Profit.amount).alias("all_profits")
            )
            .where(Profit.owner_id == worker_id)
        ).execute()[0].all_profits or 0)

    def workers_by_username(self, username: str):
        return Worker.select().where(
            fn.Lower(Worker.username.contains(username)),
            Worker.username_hide == False
        )

    def get_topworkers_all(self, limit: int = 15):
        return (
            Worker
            .select(
                Worker,
                fn.SUM(Profit.amount).alias("profits_sum"),
                fn.COUNT(Profit.id).alias("profits_count")
            )
            .join(Profit, JOIN.LEFT_OUTER)
            .group_by(Worker.id)
            .order_by(SQL("profits_sum").desc())
            .limit(limit)
        )

    def get_topworkers_month(self, limit: int = 15):
        delta = datetime_local_now().replace(tzinfo=None) - timedelta(days=30)
        return (
            Worker
            .select(
                Worker,
                fn.SUM(Profit.amount).alias("profits_sum"),
                fn.COUNT(Profit.id).alias("profits_count")
            )
            .join(Profit, JOIN.LEFT_OUTER)
            .where(Profit.created >= delta)
            .group_by(Worker.id)
            .order_by(SQL("profits_sum").desc())
            .limit(limit)
        )

    def get_topworkers_day(self, limit: int = 15):
        date = datetime_local_now().replace(tzinfo=None)
        return (
            Worker
            .select(
                Worker,
                fn.SUM(Profit.amount).alias("profits_sum"),
                fn.COUNT(Profit.id).alias("profits_count")
            )
            .join(Profit, JOIN.LEFT_OUTER)
            .where(
                Profit.created.day == date.day,
                Profit.created.month == date.month,
                Profit.created.year == date.year
            )
            .group_by(Worker.id)
            .order_by(SQL("profits_sum").desc())
            .limit(limit)
        )

    def get_profits_all(self) -> int:
        return int(Profit.select(
            fn.SUM(Profit.amount).alias("all_profits")
        ).execute()[0].all_profits or 0)

    def get_profits_month(self) -> int:
        delta = datetime_local_now().replace(tzinfo=None) - timedelta(days=30)
        return int((
            Profit
            .select(fn.SUM(Profit.amount).alias("all_profits"))
            .where(Profit.created >= delta)
        ).execute()[0].all_profits or 0)

    def get_profits_day(self) -> int:
        date = datetime_local_now().replace(tzinfo=None)
        return int((
            Profit
            .select(fn.SUM(Profit.amount).alias("all_profits"))
            .where(
                Profit.created.day == date.day,
                Profit.created.month == date.month,
                Profit.created.year == date.year,
            )
        ).execute()[0].all_profits or 0)

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
