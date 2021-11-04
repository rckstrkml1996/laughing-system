from aiogram import Dispatcher

from .working import WorkingMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(WorkingMiddleware())
