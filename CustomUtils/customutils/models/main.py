import os
from secrets import token_hex

from peewee import *
from peewee_migrate import Router
from playhouse.shortcuts import ReconnectMixin

from ..confparse import Config
from ..datefunc import datetime_local_now

path = os.path.normpath(os.path.join(os.getcwd(), "../config.cfg"))
config = Config("Settings", path, {"migrate": "0"})


class DB(ReconnectMixin, MySQLDatabase):
    def migrate(self, router: Router):
        name = token_hex(6)
        router.create(name)
        router.run()  # Run all unapplied migrations


base = DB(
    config("base_name"),
    user=config("base_user"),
    password=config("base_password"),
    host="127.0.0.1",
    port=3306,
    charset="utf8mb4",  # for emoji and symbols)
)

# if config("migrate", bool):
#     migration_router = Router(base)
#     base.migrate(migration_router)


class BaseModel(Model):
    class Meta:
        database = base


class Worker(BaseModel):
    cid = IntegerField(unique=True)
    uniq_key = IntegerField(unique=True)
    username = CharField(null=True)
    username_hide = BooleanField(default=False)
    name = CharField()
    rate = IntegerField(default=0)  # ставка
    ref_balance = FloatField(default=0)
    status = IntegerField(default=0)
    level = IntegerField(default=0)
    registered = DateTimeField(default=datetime_local_now)
    cock_size = IntegerField(null=True)
    warns = IntegerField(default=0)
    casino_min = IntegerField(default=config("min_deposit", int))
    send_summary = BooleanField(default=False)
    summary_info = TextField(null=True)

    def __str__(self):
        return f"{self.id}: [{self.cid}] {self.name}"


class QiwiPayment(BaseModel):
    @property
    def profit(self):
        return self.profits.get()

    @profit.setter
    def profit(self, profit_obj):
        profit_obj.payment = self
        profit_obj.save(only=[Profit.payment])

    person_id = CharField()  # наш аккаунт киви
    account = CharField()  # аккаунт перевода или пополнения
    amount = IntegerField()
    payment_type = CharField(default="IN")
    currency = IntegerField(default=643)
    comment = CharField(null=True)
    date = DateTimeField()


class Profit(BaseModel):
    owner = ForeignKeyField(Worker, related_name="profits")
    amount = IntegerField()
    share = IntegerField()
    service = IntegerField(default=0)
    created = DateTimeField(default=datetime_local_now)
    done = BooleanField(default=False)  # dont nesessary.(S(das))
    msg_url = CharField(null=True)
    payment = ForeignKeyField(
        QiwiPayment,
        backref="profits",
        unique=True,
        null=True,
    )


class CasinoUser(BaseModel):
    owner = ForeignKeyField(Worker, related_name="cas_users")
    cid = IntegerField(unique=True)
    balance = IntegerField(default=0)
    fort_chance = IntegerField(default=100)  # val from 0 to 100
    bonus = IntegerField(default=0)
    username = CharField(null=True)
    fullname = CharField(null=True)
    min_deposit = IntegerField(default=config("min_deposit", int))
    stopped = BooleanField(default=False)  # stopwork status for single user

    def __str__(self):
        return f"#{self.id} {self.cid}"


class EscortUser(BaseModel):
    owner = ForeignKeyField(Worker, related_name="esc_users")
    cid = IntegerField(unique=True)
    balance = IntegerField(default=0)
    username = CharField(default="Без юзернейма")
    fullname = CharField(default="Без имени")


class EscortPayment(BaseModel):
    owner = ForeignKeyField(EscortUser, related_name="payments")
    amount = IntegerField(null=True)  # sets dynamic
    comment = CharField(unique=True)
    done = IntegerField(default=0)  # 0 - not done 1 - real done 2 - fake done
    created = DateTimeField(default=datetime_local_now)


class EscortGirl(BaseModel):
    photos = CharField()
    info = CharField(default="Без описания")
    price = IntegerField(default=1500)


class CasinoPayment(BaseModel):
    owner = ForeignKeyField(CasinoUser, related_name="payments")
    comment = CharField(unique=True, null=True)  # for banker null
    amount = IntegerField()
    done = IntegerField(default=0)  # 0 - not done 1 - real done 2 - fake done
    created = DateTimeField(default=datetime_local_now)


class CasinoUserHistory(BaseModel):
    owner = ForeignKeyField(CasinoUser, related_name="history")
    editor = IntegerField(default=0)
    amount = IntegerField()
    balance = IntegerField()
    created = CharField(default=datetime_local_now)


class TradingUser(BaseModel):
    owner = ForeignKeyField(Worker, related_name="tdg_users")
    cid = IntegerField(unique=True)
    balance = IntegerField(default=0)
    fullname = CharField(default="Без имени")
    username = CharField(default="Юзернейм скрыт")

    def __str__(self):
        return f"#{self.id} {self.cid}"


class TradingPayment(BaseModel):
    owner = ForeignKeyField(TradingUser, related_name="payments")
    comment = CharField(unique=True)
    amount = IntegerField()
    done = IntegerField(default=0)  # 0 - not done 1 - real done 2 - fake done
    created = DateTimeField(default=datetime_local_now)


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
        TradingPayment,
        EscortUser,
        EscortGirl,
        EscortPayment,
    ]
)
