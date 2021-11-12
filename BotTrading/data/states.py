from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    code = State()


class Add(StatesGroup):
    main = State()


class Out(StatesGroup):
    main = State()


class Bet(StatesGroup):
    amount = State()
    time = State()
