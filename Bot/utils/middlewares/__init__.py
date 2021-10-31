from aiogram import Dispatcher

from .main import AllMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(AllMiddleware())
