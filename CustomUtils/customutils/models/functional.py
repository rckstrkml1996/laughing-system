from peewee import fn

from .models import Profit


def get_profits_sum(worker_id):
    return int((
        Profit
        .select(
            fn.SUM(Profit.amount).alias("all_profits")
        )
        .where(Profit.owner_id == worker_id)
    ).execute()[0].all_profits or 0)


