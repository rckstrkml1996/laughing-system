from aiogram.dispatcher.filters.state import State, StatesGroup

"""
    bla bla bla
    mne pohui ia delau chisto pokakat
"""


class Summary(StatesGroup):
    where = State()
    experience = State()
    final = State()


class Render(StatesGroup):
    qiwi_balance = State()
    qiwi_trans = State()
    sber_trans = State()


class Pin(StatesGroup):
    change = State()
    new = State()


class NewQiwi(StatesGroup):
    main = State()


class CasinoAlert(StatesGroup):
    alert = State()
    alert_true = State()


class Alert(StatesGroup):
    # for send to bot users
    bot = State()
    bot_accept = State()
    # for send to casino users
    casino = State()
    casino_accept = State()
    # for send to escort users
    escort = State()
    escort_accept = State()
    # for send to trading users
    trading = State()
    trading_accept = State()


class BtcClient(StatesGroup):
    new_phone = State()
    new_code = State()


class MakeProfit(StatesGroup):
    main = State()


class SetProfitStick(StatesGroup):
    main = State()


class EscortNewForm(StatesGroup):
    name = State()
    about = State()
    services = State()
    age = State()
    price = State()
    photo = State()
    photos = State()


# name = CharField(default="Настя")
# about = CharField(default="Без описания")
# services = CharField(default="Без услуг")
# age = IntegerField(default=20)
# price = IntegerField(default=1500)


class ChangeMin(StatesGroup):
    main = State()


class Card(StatesGroup):
    main = State()
