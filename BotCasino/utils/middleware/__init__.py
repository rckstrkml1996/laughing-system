from aiogram import Dispatcher

from .work import WorkingMiddleware


def setup_middlewares(dispatcher: Dispatcher):
    dispatcher.middleware.setup(WorkingMiddleware())
