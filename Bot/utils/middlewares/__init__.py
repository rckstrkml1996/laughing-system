from aiogram import Dispatcher

from .main import AllMiddleware
from .throttling import ThrottlingMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(AllMiddleware())
    dispatcher.middleware.setup(ThrottlingMiddleware(limit=0.05))
