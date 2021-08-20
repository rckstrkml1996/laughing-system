from aiogram.dispatcher.filters.state import State, StatesGroup


class Withdraw(StatesGroup):
    count = State()
    requisites = State()

class Deposit(StatesGroup):
    count = State()

class Asset(StatesGroup):
    count = State()