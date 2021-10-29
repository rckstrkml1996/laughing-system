from aiogram import Dispatcher

from .main import IsWorking, IsUser


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsWorking)
    dp.filters_factory.bind(IsUser)
