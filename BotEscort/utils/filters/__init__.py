from aiogram import Dispatcher

from .main import IsUser


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsUser)
