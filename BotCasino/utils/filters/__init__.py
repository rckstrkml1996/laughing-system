from aiogram import Dispatcher

from .main import IsWorking


def setup_filters(dispatcher: Dispatcher):
    dispatcher.filters_factory.bind(IsWorking)
