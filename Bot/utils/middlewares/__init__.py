from aiogram import Dispatcher

from .main import KickMiddleware, UpdateWorkerMiddleware
from .throttling import ThrottlingMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(KickMiddleware())
    dispatcher.middleware.setup(UpdateWorkerMiddleware())
    dispatcher.middleware.setup(ThrottlingMiddleware(limit=0.2))
