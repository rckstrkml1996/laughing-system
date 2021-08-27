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
    host="127.0.0.1",
    port=3306,
    charset="utf8mb4",  # for emoji and symbols)
)


class BaseModel(peewee.Model):
    class Meta:
        database = base


# def random_secret_id():
#     # 4294967295 chance 16(hex) ** 8(digits) - 1(notused)
#     return secrets.token_hex(4)  # hex with 8 digits


class Worker(BaseModel):
    cid = peewee.IntegerField(unique=True)
    uniq_key = peewee.IntegerField(unique=True)
    username = peewee.CharField(null=True)
    username_hide = peewee.BooleanField(default=False)
    name = peewee.CharField()
    rate = peewee.IntegerField(default=0)  # ставка
    ref_balance = peewee.FloatField(default=0)
    status = peewee.IntegerField(default=0)
    level = peewee.IntegerField(default=0)
    registered = peewee.DateTimeField(default=datetime_local_now)
    cock_size = peewee.IntegerField(null=True)
    warns = peewee.IntegerField(default=0)
    send_summary = peewee.BooleanField(default=False)
    summary_info = peewee.TextField(null=True)


class QiwiPayment(BaseModel):
    @property
    def profit(self):
        return self.profits.get()

    @profit.setter
    def profit(self, profit_obj):
        profit_obj.payment = self
        profit_obj.save(only=[Profit.payment])

    person_id = peewee.CharField()  # наш аккаунт киви
    account = peewee.CharField()  # аккаунт перевода или пополнения
    amount = peewee.IntegerField()
    currency = peewee.IntegerField(default=643)
    comment = peewee.CharField(null=True)
    date = peewee.DateTimeField()


class Profit(BaseModel):
    owner = peewee.ForeignKeyField(Worker, related_name="profits")
    amount = peewee.FloatField()
    share = peewee.FloatField()
    service = peewee.IntegerField(default=0)
    created = peewee.DateTimeField(default=datetime_local_now)
    done = peewee.BooleanField(default=False)  # dont nesessary.(S(das))
    payment = peewee.ForeignKeyField(
        QiwiPayment,
        backref="profits",
        unique=True,
        null=True,
    )


class CasinoUser(BaseModel):
    owner = peewee.ForeignKeyField(Worker, related_name="cas_users")
    cid = peewee.IntegerField(unique=True)
    balance = peewee.IntegerField(default=0)
    fort_chance = peewee.IntegerField(default=50)  # val from 0 to 100
    bonus = peewee.IntegerField(default=0)
    fuckedup = peewee.BooleanField(default=False)
    username = peewee.CharField(null=True)
    fullname = peewee.CharField(null=True)

    def __str__(self):
        return f"#{self.id} {self.cid}"


class CasinoPayment(BaseModel):
    owner = peewee.ForeignKeyField(CasinoUser, related_name="payments")
    comment = peewee.CharField(unique=True)
    amount = peewee.IntegerField()
    done = peewee.BooleanField(default=False)
    created = peewee.DateTimeField(default=datetime_local_now)


class CasinoUserHistory(BaseModel):
    owner = peewee.ForeignKeyField(CasinoUser, related_name="history")
    editor = peewee.IntegerField(default=0)
    amount = peewee.IntegerField()
    balance = peewee.IntegerField()
    created = peewee.CharField(default=datetime_local_now)


class TradingUser(BaseModel):
    cid = peewee.IntegerField(unique=True)
    balance = peewee.IntegerField(default=0)
    fullname = peewee.CharField(default="Без имени")
    username = peewee.CharField(default="Юзернейм скрыт")

    def __str__(self):
        return f"#{self.id} {self.cid}"


base.connect()
base.create_tables(
    [
        Worker,
        Profit,
        QiwiPayment,
        CasinoUser,
        CasinoUserHistory,
        CasinoPayment,
        TradingUser,
    ]
)
