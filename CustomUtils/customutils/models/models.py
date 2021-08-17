import secrets
import random

import peewee

from ..confparse import Config
from ..datefunc import datetime_local_now

config = Config("Settings", "../config.cfg", {})

base = peewee.MySQLDatabase(
    config("base_name"),
    user=config("base_user"),
    password=config("base_password"),
    host='127.0.0.1',
    port=3306,
    charset='utf8mb4'  # for emoji and symbols)
)


class BaseModel(peewee.Model):
    class Meta:
        database = base


# def random_secret_id():
#     # 4294967295 chance 16(hex) ** 8(digits) - 1(notused)
#     return secrets.token_hex(4)  # hex with 8 digits


class Worker(BaseModel):
    def random_key():
        return random.randint(100000000000, 999999999999)

    cid = peewee.IntegerField(unique=True)
    username = peewee.CharField(null=True)
    username_hide = peewee.BooleanField(default=False)
    name = peewee.CharField()
    rate = peewee.IntegerField(default=0)  # ставка
    ref_balance = peewee.FloatField(default=0)
    status = peewee.IntegerField(default=0)
    level = peewee.IntegerField(default=0)
    send_summary = peewee.BooleanField(default=False)
    summary_info = peewee.TextField(null=True)
    registered = peewee.DateTimeField(default=datetime_local_now)
    sup_key = peewee.BigIntegerField(
        default=random_key, unique=True)  # max 2**63 - 1
    cock_size = peewee.IntegerField(null=True)
    warns = peewee.IntegerField(default=0)


class CasinoUser(BaseModel):
    owner = peewee.ForeignKeyField(Worker, related_name='casusers', null=True)
    cid = peewee.IntegerField(unique=True)


class Profit(BaseModel):
    owner = peewee.ForeignKeyField(Worker, related_name='profits')
    amount = peewee.FloatField()
    share = peewee.FloatField()
    created = peewee.DateTimeField(default=datetime_local_now)


class QiwiPayment(BaseModel):
    person_id = peewee.CharField()  # наш аккаунт киви
    account = peewee.CharField(null=True)
    amount = peewee.IntegerField()
    comment = peewee.CharField(null=True)
    date = peewee.DateTimeField()
    profit = peewee.ForeignKeyField(
        Profit,
        backref='profits',
        unique=True,
        null=True
    )


base.connect()
base.create_tables([Worker, CasinoUser, Profit, QiwiPayment])
