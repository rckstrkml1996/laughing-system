from aiogram.dispatcher.filters.state import State, StatesGroup


class Withdraw(StatesGroup):
    count = State()
