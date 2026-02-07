from aiogram import Dispatcher

from .working import WorkingMiddleware
from .throtling import ThrottlingMiddleware


def setup_middlewares(dispatcher: Dispatcher):
    dispatcher.middleware.setup(WorkingMiddleware())
    dispatcher.middleware.setup(ThrottlingMiddleware(0.2))
