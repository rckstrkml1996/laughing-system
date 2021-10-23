import os
from secrets import token_hex

from peewee import *
from playhouse.shortcuts import ReconnectMixin

from ..confparse import Config
from ..datefunc import datetime_local_now

path = os.path.normpath(os.path.join(os.getcwd(), "../config.cfg"))
config = Config("Settings", path, {"migrate": "0"})


class DB(ReconnectMixin, MySQLDatabase):
    pass


base = DB(
    config("base_name"),
    user=config("base_user"),
    password=config("base_password"),
    host="127.0.0.1",
    port=3306,
    charset="utf8mb4",  # for emoji and symbols)
)


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
        return f"{self.id}: [{self.cid}] @{self.username} n{self.status}"


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
        return f"#{self.id} [{self.cid}] {self.balance} RUB, @{self.username} {self.fullname}"


class CasinoPayment(BaseModel):
    owner = ForeignKeyField(CasinoUser, related_name="payments")
    comment = CharField(unique=True, null=True)  # for banker null
    amount = IntegerField()
    done = IntegerField(default=0)  # 0 - not done 1 - real done 2 - fake done
    created = DateTimeField(default=datetime_local_now)


class CasinoUserHistory(BaseModel):
    owner = ForeignKeyField(CasinoUser, related_name="history")
    editor = IntegerField(default=0)  # 3 - lose 2 - win
    amount = IntegerField()
    balance = IntegerField()
    created = CharField(default=datetime_local_now)

    def __str__(self):
        return f"#{self.id} editor = {self.editor} {self.amount} RUB, {self.created}"


class EscortUser(BaseModel):
    owner = ForeignKeyField(Worker, related_name="esc_users")
    cid = IntegerField(unique=True)
    balance = IntegerField(default=0)
    username = CharField(default="Без юзернейма", null=True)
    fullname = CharField(default="Без имени")

    def __str__(self):
        return f"#{self.id} [{self.cid}] {self.balance} RUB, {self.fullname}"


class EscortPayment(BaseModel):
    owner = ForeignKeyField(EscortUser, related_name="payments")
    # amount: amount of hour - two hours - night
    amount = IntegerField()
    comment = CharField(unique=True)
    # done: 0 - not done 1 - done hour 2 - done two hours 3 - done three hours
    done = IntegerField(default=0)
    created = DateTimeField(default=datetime_local_now)

    @property
    def two_amount(self):
        return self.amount * 2

    @property
    def three_amount(self):
        return self.amount * 3

    def __str__(self):
        return f"#{self.id} amount={self.amount} done={self.done}"

class EscortGirl(BaseModel):
    owner = ForeignKeyField(Worker, related_name="escort_girls", null=True)
    name = CharField(default="Настя")
    about = CharField(default="Без описания")
    services = CharField(default="Без услуг")
    age = IntegerField(default=20)
    price = IntegerField(default=1500)
    for_all = BooleanField(default=False)

    @property
    def two_price(self):
        return self.price * 2

    @property
    def three_price(self):
        return self.price * 3

    def __str__(self):
        return f"#{self.id} age={self.age} price={self.price} name={self.name}"


class EscortGirlPhoto(BaseModel):
    owner = ForeignKeyField(EscortGirl, related_name="photos")
    saved_path = CharField()
    file_id = CharField(null=True, unique=True)  # may be delete unique = True!


class TradingUser(BaseModel):
    owner = ForeignKeyField(Worker, related_name="tdg_users")
    cid = IntegerField(unique=True)
    balance = IntegerField(default=0)
    fullname = CharField(default="Без имени")
    username = CharField(default="Юзернейм скрыт")


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
        EscortGirlPhoto,
        EscortPayment,
    ]
)
