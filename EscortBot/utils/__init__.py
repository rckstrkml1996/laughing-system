from aiogram import Dispatcher

from .main import IsWorking


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsWorking)
