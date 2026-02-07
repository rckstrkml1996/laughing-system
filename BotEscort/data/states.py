from aiogram.dispatcher.filters.state import State, StatesGroup


class Login(StatesGroup):
    code = State()
