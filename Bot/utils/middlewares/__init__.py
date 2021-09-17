from aiogram import Dispatcher

from .main import NewUsernameMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(NewUsernameMiddleware())
