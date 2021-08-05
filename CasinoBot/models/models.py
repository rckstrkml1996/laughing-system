import datetime

import peewee

from config import settings  # DATABASE_FILE, SHARE

base = peewee.MySQLDatabase(
    settings.BASE_NAME,
    user=settings.BASE_USER,
    password=settings.BASE_PASSWORD,
    host='127.0.0.1',
    port=3306,
    charset='utf8mb4'  # for emoji and symbols)
)


def timenow():
    date = datetime.datetime.now()
    hour = date.hour + 3
    if hour > 23:
        hour -= 24
    return f"{hour}:{date.minute:02d}"


class BaseModel(peewee.Model):
    class Meta:
        database = base


class CasinoUser(BaseModel):
    cid = peewee.IntegerField(unique=True)
    balance = peewee.IntegerField(default=0)
    refer = peewee.IntegerField(default=0)
    ref_balance = peewee.IntegerField(default=0)
    premium = peewee.BooleanField(default=True)  # if not add and changed bal
    username = peewee.CharField(default="Юзернейм скрыт")
    bonus = peewee.IntegerField(default=0)
    fuckedup = peewee.BooleanField(default=False)
    fullname = peewee.CharField(default="Без имени")

    def __str__(self):
        return f'#{self.id} {self.cid}'


class CasinoPayment(BaseModel):
    cid = peewee.IntegerField()
    comment = peewee.CharField()
    amount = peewee.IntegerField()
    done = peewee.BooleanField(default=False)


class CasinoUserHistory(BaseModel):
    cid = peewee.IntegerField()
    amount = peewee.IntegerField()
    editor = peewee.IntegerField(default=0)
    balance = peewee.IntegerField()
    created = peewee.CharField(default=timenow)


base.connect()
base.create_tables([CasinoUser, CasinoPayment, CasinoUserHistory])
