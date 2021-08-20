from aiogram.dispatcher.filters.state import State, StatesGroup

'''
    bla bla bla
    mne pohui ia delau chisto pokakat
'''


class Summary(StatesGroup):
    where = State()
    experience = State()
    final = State()


class Panel(StatesGroup):
    secret_id = State()


class Render(StatesGroup):
    qiwibalance = State()
    qiwitransfer = State()
    sbertransfer = State()


class Pin(StatesGroup):
    change = State()
    new = State()


class Qiwi(StatesGroup):
    new = State()


class Casino(StatesGroup):
    commands = State()
